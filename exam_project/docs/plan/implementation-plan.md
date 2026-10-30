# StudyGraph — Implementation Plan

Goal: from an empty repository (only `README.md` + `docs/`) to a demonstrable MVP in
which a **local LLM** answers with and without **RAG**, the **4T's** are visibly
configurable, and the two required comparison exercises are documented.

- Stack and rationale: [../architecture/tech-stack.md](../architecture/tech-stack.md)
- Current state: [status.md](status.md) · Tickets: [backlog.md](backlog.md)
- Requirements being satisfied: [../requirements/requirements.md](../requirements/requirements.md)

## 1. Guiding strategy

1. **Walking skeleton first.** Before any UI, prove the risky part end-to-end on the
   command line: slide PDF → Markdown → chunks → embeddings → Chroma → retrieval →
   Ollama answer with sources. If this works, the rest is ordinary application work.
2. **Vertical slices after that.** Each later phase ends with something runnable
   (`pytest` green, a Streamlit page that works), not with a layer that is "ready".
3. **Depth before breadth.** One course, one chat flow, two modes. Everything optional
   (uploads, extra courses, buddy templates) waits for Phase 9.
4. **Evidence while building.** Every phase names the artifact it produces for the
   synopsis and the demo, so the documentation is written from real output, not from memory.
5. **Tests without services.** Prompt construction, snapshot behaviour, persistence and
   RAG/non-RAG routing must be testable with fakes, because demos fail when Ollama is busy.

## 2. Phase overview

| Phase | Name | Est. | Depends on | Exit criterion (must be true before moving on) |
|---|---|---|---|---|
| 0 | Bootstrap & decisions | 0.5 d | — | `uv run streamlit run app/main.py` shows a placeholder page; chat + embedding model chosen; `chroma run` healthy |
| 1 | Walking skeleton (CLI spike) | 0.5–1 d | 0 | `uv run python .\scripts\spike_rag.py "question"` prints retrieved chunk ids/scores **and** a grounded answer from a local model |
| 2 | Course knowledge base ingestion | 0.5 d | 1 | `scripts/ingest.py` re-indexes the course material idempotently; `chroma browse llms_for_devs_v1 --local` shows chunks with metadata |
| 3 | Domain model + SQLite persistence | 1 d | 0 | Buddies, conversations, messages and snapshots survive an app restart; unit tests cover snapshot immutability |
| 4 | Prompt construction (4T's) | 0.5 d | 3 | A test renders a prompt containing Task, Tone, Traits, Target and the context block, and the version is stored on the message |
| 5 | LangGraph chat flow + Ollama client | 1 d | 2, 4 | A course conversation retrieves and cites; a no-course conversation provably never calls the retriever |
| 6 | Streamlit UI | 1 d | 3, 5 | The five user journeys in [../design/user-experience.md](../design/user-experience.md) §2 are walkable in the browser with error states |
| 7 | RAG vs non-RAG evaluation | 0.5 d | 6 | A results table with paired answers and ratings exists in `docs/evaluation/` |
| 8 | Linear regression vs LLM+RAG experiment | 0.5 d | 1 (parallel) | A results table with actual values, both predictions and an error measure exists |
| 9 | Hardening, packaging, synopsis | 1 d | 6, 7, 8 | `README.md` reproduces the app from scratch; `pytest`/`ruff`/`mypy` clean; synopsis ≤ 5 pages |

Phases 8 and 9 (documentation part) can run in parallel with 6–7 if there is more than
one person. Phases 0–2 are the highest-risk work and should not be parallelised away.

## 3. Phase details

### Phase 0 — Bootstrap & decisions (0.5 d)

Work:

1. `uv venv --python 3.12` in `exam_project/`, then `uv add streamlit chromadb langgraph ollama`
   and `uv add --dev pytest ruff mypy`; create `pyproject.toml` (project metadata; ruff/mypy
   sections inherited from the repo-root config).
2. Pull candidates: `ollama pull llama3.2:3b`, `ollama pull qwen2.5:7b`,
   `ollama pull nomic-embed-text`. Time one short answer on each chat model and record it.
3. Start Chroma: `chroma run --path .\data\chroma`, verify `http://localhost:8000/api/v2/heartbeat`.
4. Create the skeleton (`app/`, `scripts/`, `tests/unit/`, `tests/integration/`, empty
   `data/course_material/llms-for-developers/{pdf,markdown}`).
5. Fill in `ADR-001` … `ADR-006` in the [decision log](decision-log.md) with the measured
   model choice.

Exit evidence: a placeholder Streamlit page, a heartbeat from Chroma, a note with the
chosen chat model and its measured response time.

### Phase 1 — Walking skeleton, CLI only (0.5–1 d)

Work: `scripts/spike_rag.py` with no abstractions — convert one lecture PDF to Markdown,
cut into chunks, embed with Ollama, add to Chroma, take a question, embed it, query top-4,
print ids/scores/metadata, and ask the local model to answer with a strict "only use the
context" instruction.

Exit evidence: terminal output showing the retrieved chunks and an answer **whose claims
are traceable to those chunks** — this is also the first "how retrieval affects an answer"
demo. Note in the decision log which conversion tool and chunking approach survived.

### Phase 2 — Course knowledge base ingestion (0.5 d)

Work: promote the spike into `app/adapters/loader.py`, `app/adapters/chunker.py`,
`scripts/ingest.py`. Metadata per chunk: `course_id`, `doc_id`, `doc_name`, `lecture`,
`page`, `chunk_index`, `text_hash`. Stable chunk ids (`sha1` of doc + page + index + hash)
so a re-run never duplicates. Collection name and embedding metadata recorded
(see [../RAG/knowledge-base.md](../RAG/knowledge-base.md)).

Exit evidence: run ingest twice → identical chunk count; browsing the collection shows the
metadata; two sample queries return the expected slides.

### Phase 3 — Domain model + SQLite persistence (1 d)

Work: schema for `buddies`, `conversations`, `messages` (and `courses` seeded with the one
course); repositories with explicit transactions; `BuddySnapshot` serialisation with
`snapshot_version`; validation functions and typed errors.

Exit evidence: unit tests for snapshot immutability, reopen-and-read persistence, and
validation failures; the acceptance criteria 5–10 in the traceability table below.

### Phase 4 — Prompt construction and the 4T's (0.5 d)

Work: `app/prompts/system_v1.md`, `context_block_v1.md`, `app/prompts/builder.py` taking
`BuddySnapshot` + `TaskSpec` + history + retrieved chunks; task presets (explain, summarise,
quiz, compare, review) as data; `prompt_version` recorded.

Exit evidence: a rendered prompt (saved under `docs/evaluation/` as an example) where each
of the four dimensions is visibly separate, plus tests asserting a missing dimension is
detectable.

### Phase 5 — LangGraph flow + Ollama client (1 d)

Work: `app/adapters/ollama_client.py` (chat + embed, explicit options, timeouts, typed
errors); `app/graph/state.py` (`StudyGraphState`), `nodes.py`, `build.py`
(`prepare → route → retrieve? → build_prompt → generate → finalize`); retrieval status
enum; sources propagated into state and persisted.

Exit evidence: tests proving non-RAG conversations never call the retriever, and that a
retrieval failure is surfaced as failure rather than an empty success; one real streamed
answer.

### Phase 6 — Streamlit UI (1 d)

Work: `app/main.py` with pages Chat, Buddies, Conversations, About; Buddy form grouped as
Identity / Teaching style / Course grounding; mode badge ("Course-grounded" / "General");
sources in an expander; loading, empty, error and save-failure states; disabled input
during generation.

Exit evidence: the five journeys in [../design/user-experience.md](../design/user-experience.md) §2
are walkable; a Playwright pass over the main flow; `AppTest` coverage of the chat page.

### Phase 7 — RAG vs non-RAG evaluation (0.5 d)

Work: 8–10 question set (6 answerable from the course, 2–3 deliberately not covered), one
paired Buddy configuration with and without the course, fixed generation parameters,
results captured in [../evaluation/rag-comparison-results.md](../evaluation/rag-comparison-results.md)
with ratings for factual correctness, course alignment, relevance, grounding, uncertainty.

Exit evidence: the comparison table plus 2–3 quoted examples where retrieval visibly
changed the answer.

### Phase 8 — Linear regression vs local LLM + RAG (0.5 d, separate track)

Work: per
[../evaluation/regression-vs-rag.md](../evaluation/regression-vs-rag.md): dataset with a
train/reference split and held-out test inputs, a scikit-learn baseline, a RAG collection
built **only** from the reference portion, the same held-out inputs given to the LLM,
absolute error / MAE for both, and a short discussion of why they differ.

Exit evidence: the results table with real values and the recorded retrieved documents.

### Phase 9 — Hardening, packaging, synopsis (1 d)

Work: full `pytest`/`ruff`/`mypy` pass; error messages verified by stopping Ollama and
Chroma; `README.md` rewritten as a setup guide (prerequisites, model pull, ingest, run,
test, troubleshooting); demo script; synopsis (≤ 5 pages) assembled from the phase
evidence; `docs/plan/status.md` finalised.

Exit evidence: a clean machine-level walkthrough of the README by someone who did not
write it, plus the synopsis draft.

## 4. Traceability — acceptance criteria to work

Source: [requirements.md](../requirements/requirements.md) §6 (acceptance criteria 1–16)
and the assignment's mandatory criteria.

| # | Acceptance criterion (short) | Implemented in | Proven by |
|---|---|---|---|
| 1 | User can send messages and get AI responses | Phase 5, 6 | Manual run + `AppTest` |
| 2 | Create a Buddy with name, Target, Tone, Traits | Phase 3, 6 | Unit test + UI journey 2.2 |
| 3 | Optionally associate a Buddy with the course | Phase 3, 6 | Unit test + UI journey |
| 4 | Course dropdown has course + no-course | Phase 6 | `AppTest` assertion |
| 5 | Buddies persist across restarts | Phase 3 | Reopen test |
| 6 | Reuse a saved Buddy across conversations | Phase 3, 6 | Unit test |
| 7 | Conversations and messages persist | Phase 3 | Reopen test |
| 8 | Each conversation stores a snapshot | Phase 3 | Unit test |
| 9 | Editing a Buddy does not change old conversations | Phase 3 | Snapshot immutability test |
| 10 | Snapshots survive Buddy deletion | Phase 3 | Unit test |
| 11 | Course Buddy triggers course retrieval | Phase 5 | Retriever-called test |
| 12 | No-course Buddy does not retrieve | Phase 5 | Retriever-not-called test |
| 13 | Both modes use the same configuration + Task | Phase 4, 5 | Prompt-diff test |
| 14 | Modes are comparable with other variables fixed | Phase 7 | Evaluation table |
| 15 | Common errors handled without crashes/data loss | Phase 6, 9 | Failure-mode checklist |
| 16 | 4T's visibly influence behaviour | Phase 4, 6 | Rendered prompt + two prompt variants |
| M1 | Local LLM generates the answers | Phase 5 | Model metadata per message; no external API in code |
| M2 | RAG demonstrably affects an answer | Phase 7 | Paired answers with/without retrieval |
| M3 | 4T's applied meaningfully and explained | Phase 4, synopsis | Prompt templates + synopsis section |
| M4 | ML concept, data prep, limitations reflected | Phase 2, 8, synopsis | Knowledge-base doc + experiment discussion |
| M5 | Regression vs LLM+RAG comparison | Phase 8 | `docs/evaluation/regression-vs-rag.md` |

## 5. Explicit non-goals for the MVP

Anything here needs a new `ADR` and must not delay phases 0–7:

- Multiple managed courses, course creation UI, per-course settings.
- Multi-user accounts, authentication, sharing or publishing Buddies.
- A dedicated evaluation dashboard inside the app.
- Multi-agent LangGraph topologies, tool calling, web search.
- Fine-tuning or training any model.
- Deployment beyond localhost, Docker images, CI pipelines.
- Streaming token-by-token cancellation and other production concerns.

## 6. Demo script (target: 8 minutes)

1. Show `chroma run` + ChromaUI/`chroma browse` with the indexed course chunks (proves RAG data).
2. Create a Buddy "Patient Tutor" (Target/Tone/Traits) **with** the course → ask a
   course-specific question → open the sources expander → point at the retrieved slides.
3. Create the paired Buddy **without** the course → ask the identical question → compare
   the two answers side by side.
4. Restart the app → both conversations and both Buddies are still there, snapshots intact.
5. Stop Ollama → send a message → show the error state (no crash, no fake answer).
6. Show the evaluation table and the regression-vs-RAG table.

## 7. Working rhythm

- One ticket per branch and per session; `uv run pytest -q` green before moving on.
- Phase-boundary review: re-read [risks.md](risks.md), update [status.md](status.md),
  confirm the exit criterion with a real run, then start the next phase.
- If a phase overruns by more than ~50 %, cut scope (P2 first, then P1 source references)
  instead of dropping the comparison exercises — those are mandatory.
