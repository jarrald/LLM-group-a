# StudyGraph — Project Status

**Last updated:** 2026-10-30 · **Branch:** `mandatory-1` (commit `ee24e04`) ·
**Current phase:** 0 — Bootstrap & decisions (not started)

This is the file to read first in a new session. It must always reflect reality, not intent.

## 1. One-paragraph summary

The product and its documentation are designed (requirements, architecture, data model, RAG
pipeline, UX, Buddy design). **No application code exists yet.** The technology stack has
been proposed and recorded ([tech-stack.md](../architecture/tech-stack.md),
[decision-log.md](decision-log.md)), the work is planned
([implementation-plan.md](implementation-plan.md)) and ticketed ([backlog.md](backlog.md)).
The next step is Phase 0: create the Python 3.12 environment, pull a chat and an embedding
model into Ollama, and confirm the Chroma server runs.

## 2. What exists today

| Area | State |
|---|---|
| Requirements, design, architecture docs | Done (`docs/requirements`, `docs/design`, `docs/architecture`) |
| Tracking docs (`docs/plan`) | Done — this session |
| Technology stack | Proposed, pending the Phase 0 model spike |
| Application code (`app/`, `scripts/`, `tests/`) | **None** |
| Course material in the repo | **None** — the lecture PDFs are not in `data/course_material/` yet |
| Environment (uv, deps) | Not created |
| Chroma index | Not created |
| Evaluation results | Templates only, no data |

## 3. Environment verified on 2026-10-30

| Check | Result |
|---|---|
| `python --version` (default) | 3.14.7 — *not* the project target |
| Available interpreters | 3.10, uv-managed 3.12.12 |
| `uv` | present at `C:\Users\novij\.local\bin\uv.exe` |
| Ollama | 0.35.1 installed; server answered on `http://127.0.0.1:11434` |
| Ollama models | `tester`, `deploy`, `docs` — **no chat model, no embedding model pulled** |
| Python packages (streamlit, chromadb, langgraph, ollama) | **not installed** |
| Chroma server | not running |

Consequence: SG-002, SG-003 and SG-004 are the first real actions, and nothing can be
demonstrated before they succeed.

## 4. Open decisions

| Decision | ADR | Blocking |
|---|---|---|
| Chat model choice | ADR-007 (Proposed) | Phase 1+ |
| Embedding model & dimension | ADR-007b (Proposed) | Phase 1+ |
| PDF → Markdown tool | ADR-008 (Proposed) | Phase 1 |
| Chunk size, overlap, `top_k` | — (to be added) | Phase 2/5 |
| Supplementary uploads in V1? | — (to be added) | Phase 9 |

## 5. Blockers

| Blocker | Impact | Next action |
|---|---|---|
| Course lecture PDFs are not in the repository | Phase 1 and 2 cannot start; the knowledge base is the product's core | Someone with access to the course material puts the PDFs in `data/course_material/llms-for-developers/pdf/` (git-ignored) and lists them here |
| No chat/embedding model pulled | No local generation possible | SG-002 / SG-003 |
| No decision yet on which machine/GPU the demo runs on | Model size must match the hardware | Confirm before SG-002 |

## 6. Next three actions

1. **SG-001** — `uv venv --python 3.12`, `uv add streamlit chromadb langgraph ollama`,
   `uv add --dev pytest ruff mypy`; commit `pyproject.toml` + lockfile.
2. **SG-002 / SG-003** — `ollama pull llama3.2:3b`, `ollama pull qwen2.5:7b`,
   `ollama pull nomic-embed-text`; measure one answer per chat model; close ADR-007/007b.
3. **SG-004** — `chroma run --path .\data\chroma` in a background job and verify
   `Invoke-RestMethod http://localhost:8000/api/v2/heartbeat`.

## 7. Resume checklist for a new session or agent

- [ ] Read this file, [backlog.md](backlog.md) and the relevant design/architecture doc.
- [ ] Confirm the phase in §1 is still accurate; if not, fix it first.
- [ ] Pick a `Ready` ticket with no open dependencies; create a branch for it.
- [ ] Run `uv run pytest -q` before and after the change.
- [ ] Update the ticket state and rewrite §5–§7 of this file before ending the session.

## 8. Session log

| Date | Session focus | Outcome |
|---|---|---|
| 2026-10-30 | Project setup: rules, tracking docs, plan | `.clinerules/` created; `docs/plan/`, `docs/architecture/tech-stack.md`, `docs/RAG/knowledge-base.md`, `docs/evaluation/*` created; environment audited; Phase 0 defined. No code written (by design). |
