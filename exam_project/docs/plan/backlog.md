# StudyGraph — Backlog

Ticket board for the MVP. Phases are defined in
[implementation-plan.md](implementation-plan.md); ticket states are defined in
[README.md](README.md). One ticket = one branch = one small diff.

Legend: **Pri** P0 (mandatory) / P1 (needed for a credible demo or synopsis) / P2 (optional).

## Phase 0 — Bootstrap & decisions

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-001 | P0 | Create `uv` env on Python 3.12 + `pyproject.toml`/`requirements.txt` | Ready | — | `uv run python --version` reports 3.12.x; deps installed; lockfile committed |
| SG-002 | P0 | Pull and time candidate chat models (`llama3.2:3b`, `qwen2.5:7b`) | Ready | — | Both models answer one prompt; measured seconds/answer recorded in ADR-007 |
| SG-003 | P0 | Pull embedding model and record its dimension | Ready | — | `ollama show <model>` + an embed call returning a vector of known length |
| SG-004 | P0 | Run the Chroma server and verify heartbeat | Ready | SG-001 | `chroma run --path .\data\chroma` up; `Invoke-RestMethod http://localhost:8000/api/v2/heartbeat` succeeds |
| SG-005 | P0 | Repository skeleton + placeholder Streamlit page | Ready | SG-001 | `uv run streamlit run app/main.py` renders a placeholder; folders from `10-python-style.md` exist |
| SG-006 | P2 | Verify ChromaUI (or `chroma browse`) against the server | Todo | SG-004 | Collections visible in ChromaUI `:3000` or via `chroma browse --local`; steps noted in status.md |

## Phase 1 — Walking skeleton (CLI)

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-010 | P0 | Spike PDF → Markdown conversion on a real lecture | Blocked (needs SG-020) | SG-020 | One lecture converted; conversion tool chosen (ADR-008) |
| SG-011 | P0 | Spike chunk → embed → Chroma → top-k query | Todo | SG-003, SG-004, SG-010 | Query returns 4 chunks with ids, distances and metadata |
| SG-012 | P0 | Spike grounded answer from retrieved context | Todo | SG-011, SG-002 | Model answers a course question using only the retrieved context |

## Phase 2 — Course knowledge base

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-020 | P0 | Obtain lecture slides into `data/course_material/llms-for-developers/pdf/` | Blocked (material not in repo) | — | PDFs present locally (git-ignored) and the list of files is recorded in the RAG doc |
| SG-021 | P0 | `app/adapters/loader.py` — PDF → cleaned Markdown | Todo | SG-010 | Deterministic output; artefacts cleaned; Markdown committed |
| SG-022 | P0 | `app/adapters/chunker.py` — slide-aware chunks + metadata + stable ids | Todo | SG-021 | Same input twice → identical ids and count; metadata complete |
| SG-023 | P0 | `scripts/ingest.py` — idempotent indexing with embedding metadata | Todo | SG-022, SG-003 | Two consecutive runs report the same chunk count, no duplicates |
| SG-024 | P1 | Validate the index with sample queries and `chroma browse` | Todo | SG-023 | Two recorded queries return the expected lectures/slides |

## Phase 3 — Domain model & persistence

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-030 | P0 | SQLite schema + connection/transaction helpers | Todo | SG-001 | Schema creates cleanly; `PRAGMA foreign_keys` verified; test round-trip |
| SG-031 | P0 | Buddy repository (create/read/update/list) | Todo | SG-030 | CRUD tests pass; validation rejects blank name and empty Traits |
| SG-032 | P0 | Conversation + message repositories with `BuddySnapshot` | Todo | SG-030 | Snapshot stored with `snapshot_version`; immutability test passes |
| SG-033 | P0 | Domain validation + typed errors (`app/errors.py`) | Todo | SG-030 | Invalid ids/values raise our errors, not `KeyError`/`sqlite3.Error` |
| SG-034 | P0 | Seed the single course (id, name, description) | Todo | SG-030 | Course row exists on first run; referenced by Buddies |

## Phase 4 — Prompt construction (4T's)

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-040 | P0 | `app/prompts/system_v1.md` + `context_block_v1.md` | Todo | — | Templates reviewed; 4T's, grounding and refusal rules explicit |
| SG-041 | P0 | `app/prompts/builder.py` + task presets as data | Todo | SG-040, SG-033 | Rendered prompt contains all four dimensions separately; preset list works |
| SG-042 | P1 | Record `prompt_version` (and retrieval params) on each message | Todo | SG-041, SG-032 | Message row carries model, prompt_version, top_k |
| SG-043 | P1 | Archive example rendered prompts (grounded vs general) | Todo | SG-041 | Two prompt examples stored under `docs/evaluation/` |

## Phase 5 — LangGraph flow & local LLM

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-050 | P0 | `app/adapters/ollama_client.py` (chat + embed, options, timeouts) | Todo | SG-002 | Fakeable unit test + one real call; failures raise `LlmUnavailableError` |
| SG-051 | P0 | `app/adapters/embedder.py` (single source of embeddings) | Todo | SG-003 | Dimension constant exported and validated against collection metadata |
| SG-052 | P0 | `app/adapters/retriever.py` + retrieval status enum | Todo | SG-011, SG-051 | Returns chunks + metadata; distinguishes `ok`/`empty`/`failed` |
| SG-053 | P0 | LangGraph state, nodes, conditional routing | Todo | SG-052, SG-041 | Graph compiles; non-RAG path never calls the retriever (test) |
| SG-054 | P0 | Chat service — one turn end-to-end + persistence | Todo | SG-053, SG-032 | Turn stores user + assistant messages with sources and status |

## Phase 6 — Streamlit UI

| ID | Pri | Title | State | Depends on | Done when |
|---|---|---|---|---|---|
| SG-060 | P0 | App shell + navigation (Chat / Buddies / Conversations / About) | Todo | SG-005 | Pages navigate; clients and graph cached with `cache_resource` |
| SG-061 | P0 | Buddies page — create/edit/list, grouped form, course dropdown | Todo | SG-031, SG-034 | Journey 2.2 works end to end; "No course" is the default |
| SG-062 | P0 | Chat page — new conversation from a Buddy, message flow, streaming | Todo | SG-054, SG-060 | A grounded and a general conversation both work in the browser |
| SG-063 | P0 | Conversations page — list, reopen, continue | Todo | SG-032, SG-060 | Journey 2.4 works after an app restart |
| SG-064 | P1 | Mode badge + sources expander | Todo | SG-062 | Mode visible per conversation; sources shown only when retrieval delivered chunks |
| SG-065 | P1 | Loading / empty / retrieval-empty / error / save-failure states | Todo | SG-062 | Stopping Ollama or Chroma yields an actionable message, not a traceback |
| SG-066 | P1 | `AppTest` coverage for chat + buddies pages | Todo | SG-061, SG-062 | Tests run offline with fake adapters |

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

