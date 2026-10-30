# StudyGraph — Backlog

Ticket board for the MVP. Phases are defined in
[implementation-plan.md](implementation-plan.md); ticket states are defined in
[README.md](README.md). One ticket = one branch = one small diff.

Legend: **Pri** P0 (mandatory) / P1 (needed for a credible demo or synopsis) / P2 (optional).

## Phase 0 — Bootstrap & decisions

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-001 | P0 | Create `uv` env on Python 3.12 + `pyproject.toml`/`requirements.txt` | Done | — | `uv run python --version` reports 3.12.x; deps installed; lockfile committed |
| SG-002 | P0 | Pull and time candidate chat models | Done | — | `llama3.2:3b` answers a question in 2.9 s (measured, ADR-007) |
| SG-003 | P0 | Pull embedding model and record its dimension | Done | — | `nomic-embed-text` returns 768 dims, matching `STUDYGRAPH_EMBEDDING_DIM` (ADR-007b) |
| SG-004 | P0 | Run the Chroma server and verify heartbeat | Done | SG-001 | `/api/v2/heartbeat` responds; collection `llms_for_devs_v1` reachable |
| SG-005 | P0 | Repository skeleton + placeholder Streamlit page | Done | SG-001 | `uv run streamlit run app/main.py` renders a placeholder; folders from `10-python-style.md` exist |
| SG-006 | P2 | Verify ChromaUI (or `chroma browse`) against the server | Todo | SG-004 | Collections visible in ChromaUI `:3000` or via `chroma browse --local`; steps noted in status.md |

## Phase 1 — Walking skeleton (CLI)

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-010 | P0 | Spike PDF → Markdown conversion on a real lecture | Done | SG-020 | One lecture converted; conversion tool chosen (ADR-008) — Week 1 Markdown was supplied and is committed (ADR-013) |
| SG-011 | P0 | Spike chunk → embed → Chroma → top-k query | Done | SG-003, SG-004, SG-010 | 4 chunks returned with ids, distances and metadata (Overfitting at 0.42–0.85) |
| SG-012 | P0 | Spike grounded answer from retrieved context | Done | SG-011, SG-002 | `scripts/ask.py` answers from the retrieved Week 1 passages; evidence in [../evaluation/prompt-examples.md](../evaluation/prompt-examples.md) |

## Phase 2 — Course knowledge base

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-020 | P0 | Obtain lecture slides into the repository | Done | — | Week 1 present at `docs/RAG/llm_for_developers/source/week1/` and recorded in [../RAG/knowledge-base.md](../RAG/knowledge-base.md) |
| SG-021 | P0 | Lecture Markdown as the RAG input (`week<N>_complete_rag.md`) | Done | SG-010 | Week 1 Markdown committed; convention in ADR-013; converter for later weeks tracked as SG-025 |
| SG-022 | P0 | `app/adapters/loader.py` + `chunker.py` — heading-aware chunks + metadata + stable ids | Done | SG-021 | Deterministic ids and counts across runs (tests) |
| SG-023 | P0 | `scripts/ingest.py` — idempotent indexing with embedding metadata | Done | SG-022, SG-003 | Two consecutive runs: 57 chunks both times, no duplicates |
| SG-024 | P1 | Validate the index with sample queries and `chroma browse` | Done | SG-023 | `scripts/search.py` returns the expected Week 1 sections with distances |
| SG-025 | P1 | Convert later weeks to `week<N>/week<N>_complete_rag.md` as they are released | Todo | SG-010 | Each new week follows the ADR-013 layout and re-indexes without code changes |

## Phase 3 — Domain model & persistence

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-030 | P0 | SQLite schema + connection/transaction helpers | Done | SG-001 | Schema creates cleanly; `PRAGMA foreign_keys` on; WAL; round-trip test |
| SG-031 | P0 | Buddy repository (create/read/update/list) | Done | SG-030 | CRUD tests pass; unknown ids raise `ValidationError` |
| SG-032 | P0 | Conversation + message repositories with `BuddySnapshot` | Done | SG-030 | Snapshot stored with `snapshot_version`; immutability test passes |
| SG-033 | P0 | Domain validation + typed errors (`app/errors.py`) | Done | SG-030 | Invalid ids/values raise our errors, not `KeyError`/`sqlite3.Error` |
| SG-034 | P0 | Seed the single course (id, name, description) | Done | SG-030 | `BuddyService.seed_defaults()` creates it; Buddies reference it |

## Phase 4 — Prompt construction (4T's)

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-040 | P0 | `app/prompts/system_v1.md` + `context_block_v1.md` | Done | — | Templates reviewed; 4T's, grounding and refusal rules explicit |
| SG-041 | P0 | `app/prompts/builder.py` + task presets as data | Done | SG-040, SG-033 | Rendered prompt contains all four dimensions separately (tests) |
| SG-042 | P1 | Record model, `prompt_version` and retrieval params on each message | Done | SG-041, SG-032 | Message row carries model, prompt_version, status, sources and `retrieval_top_k` |
| SG-043 | P1 | Archive example rendered prompts (grounded vs general) | Done | SG-041 | Real grounded and general prompts captured in [../evaluation/prompt-examples.md](../evaluation/prompt-examples.md) |

## Phase 5 — LangGraph flow & local LLM

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-050 | P0 | `app/adapters/ollama_client.py` (chat + embed, options, timeouts) | Done | SG-002 | Real call works; failures raise `LlmUnavailableError`; streaming available |
| SG-051 | P0 | `app/adapters/embedder.py` (single source of embeddings) | Done | SG-003 | Dimension validated against config; mismatches raise `EmbeddingError` |
| SG-052 | P0 | `app/adapters/retriever.py` + retrieval status enum | Done | SG-011, SG-051 | Returns passages + sources; distinguishes `ok`/`empty`/`failed`, never raises |
| SG-053 | P0 | LangGraph state, nodes, conditional routing | Done | SG-052, SG-041 | Graph compiles; non-RAG path never calls the retriever (test) |
| SG-054 | P0 | Chat service — one turn end-to-end + persistence | Done | SG-053, SG-032 | Turn stores user + assistant messages with sources and status |

## Phase 6 — Streamlit UI

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-060 | P0 | App shell + navigation (Chat / Buddies / About) | Done | SG-005 | `st.navigation` with three pages; services and graph cached with `cache_resource` |
| SG-061 | P0 | Buddies page — create/edit/list, three T's, course dropdown | Done | SG-031, SG-034 | Created a Buddy with course material in the browser; "None" is the default |
| SG-062 | P0 | Chat page — new conversation from a Buddy, message flow, streaming | Done | SG-054, SG-060 | Grounded and general conversations both work in the browser |
| SG-063 | P0 | Conversation list / reopen / continue | Done | SG-032, SG-060 | Lives in the Chat sidebar (ADR-018); reopening shows stored messages |
| SG-064 | P1 | Mode badge + sources expander | Done | SG-062 | 📚/🧠 badge per conversation; sources only when retrieval delivered chunks |
| SG-065 | P1 | Empty / retrieval-empty / error states | Done (partly) | SG-062 | Empty conversation hint, retrieval notice and LLM error path done; stopping **Chroma** mid-session still to verify by hand |
| SG-066 | P1 | `AppTest` coverage for chat + buddies pages | Done | SG-061, SG-062 | 4 tests, offline, fake adapters |

## Phase 7 — RAG vs non-RAG evaluation

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-070 | P1 | Write the evaluation question set (8–10, incl. unanswerable ones) | Todo | SG-024 | Questions stored in the results doc with expected sources |
| SG-071 | P1 | Run the paired protocol (same Buddy, ±course, fixed settings) | Todo | SG-062, SG-070 | Every question answered in both modes with config recorded |
| SG-072 | P1 | Fill results + discussion (grounding, uncertainty, failures) | Todo | SG-071 | Ratings table plus 2–3 quoted examples and limitations |

## Phase 8 — Linear regression vs local LLM + RAG

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-080 | P1 | Choose dataset, define input/target, split train/reference vs held-out test | Todo | — | Split stored as CSV; test targets never exposed to either approach |
| SG-081 | P1 | scikit-learn linear regression baseline + predictions | Todo | SG-080 | Predictions and absolute error/MAE computed and recorded |
| SG-082 | P1 | RAG collection built from the reference portion only | Todo | SG-003 | Collection documented; retrieved docs logged per test case |
| SG-083 | P1 | LLM predictions for the same held-out inputs (no code execution) | Todo | SG-082, SG-002 | Predictions recorded verbatim with the retrieved context |
| SG-084 | P1 | Comparison table + discussion (why they differ; when a trained model wins) | Todo | SG-081, SG-083 | Table with actual values and both error measures |

## Phase 9 — Hardening, packaging, synopsis

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-090 | P1 | Failure-mode hardening pass | Todo | SG-065 | Checklist of 8 failure modes verified by hand |
| SG-091 | P0 | `README.md` as setup guide (prereqs, models, ingest, run, test, troubleshooting) | Todo | SG-062 | A second person reproduces the app using only the README |
| SG-092 | P1 | `pytest` / `ruff` / `mypy` sweep + coverage of critical modules | Todo | SG-054, SG-066 | All three commands clean; results pasted into status.md |
| SG-093 | P1 | Demo script rehearsal (8 min, see the plan §6) | Todo | SG-091 | Rehearsed twice, including the stopped-Ollama step |
| SG-094 | P0 | Synopsis draft (≤ 5 pages) | Todo | SG-072, SG-084 | All five required sections present, evidence-linked |

## Phase 10 — Optional (only after everything above)

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-100 | P2 | Supplementary document upload into a personal collection | Todo | SG-023 | Upload → index → retrieve, clearly separated from the course collection |
| SG-101 | P2 | Buddy duplication and deletion | Todo | SG-031 | Snapshot of existing conversations preserved on delete |
| SG-102 | P2 | Conversation renaming / titles | Todo | SG-032 | Rename persists; default title derived from the first message |

## Additions log

New tickets are appended with the next free number in their phase block. Do not renumber;
cancel by setting the state to `Done` with a note, or delete only if never started.

