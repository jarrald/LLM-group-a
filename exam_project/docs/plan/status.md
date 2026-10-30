# StudyGraph — Project Status

**Last updated:** 2026-10-30 (session 4) · **Branch:** `mandatory-1` ·
**Current phase:** 6 of 9 complete (0–6) — evaluation next

This is the file to read first in a new session. It must always reflect reality, not intent.

## 1. One-paragraph summary

**StudyGraph is a working app.** Three Streamlit pages (Chat, Buddies, About) sit on top of the
same services the CLI uses: a Buddy is created with the three T's (Traits, Tone, Target) and an
optional course material, a conversation freezes that configuration, the Task is chosen per
message, answers stream token by token, and a course-grounded answer lists the retrieved
chunks with their distances while a general answer says so explicitly. Verified in the browser
on 2026-10-30. 90 tests pass; ruff and mypy are clean. What remains: the formal RAG
evaluation (Phase 7), the linear-regression comparison (Phase 8) and packaging + synopsis
(Phase 9).

## 2. What exists today

| Area | State |
|---|---|
| Requirements, design, architecture docs | Done (`docs/requirements`, `docs/design`, `docs/architecture`) |
| Tracking docs (`docs/plan`) | Done, incl. [design-review.md](design-review.md) + resolution log |
| Environment (`uv`, deps) | **Done** — CPython 3.12, deps, project installed editable |
| Domain model, snapshots, SQLite persistence | **Done** |
| Prompt construction (three T's + Task, versioned templates) | **Done** |
| Ingestion + retrieval (57 chunks, `ok/empty/failed/skipped`) | **Done** |
| LangGraph chat flow (batch + streaming) | **Done** |
| Services (Buddy, Chat) + seeded default Buddy pair | **Done** |
| **Streamlit UI: Chat, Buddies, About** | **Done** — streaming, mode badge, sources expander |
| CLI tools (`smoke_llm`, `ingest`, `search`, `ask`) | **Done** |
| Evaluation results | Templates + one exploratory run; the formal table is next |
| Tests | **90 passing** (unit, integration, UI via `AppTest`) |

## 3. Environment verified on 2026-10-30

| Check | Result |
|---|---|
| Project interpreter | CPython **3.12** in `.venv` |
| Installed packages | streamlit 1.66.1, chromadb 1.5.9, langgraph 1.2.18, ollama 0.6.3 |
| `uv run pytest` | 90 passed |
| `uv run ruff check .` / `uv run mypy app` | clean / clean (33 files) |
| Ollama | `llama3.2:3b` (2.9 s short answer), `nomic-embed-text` (768 d) |
| Chroma | `http://localhost:8000`, `llms_for_devs_v1`, 57 chunks |
| App | `uv run streamlit run app/main.py` → `http://localhost:8501`, dark theme |
| Browser run | Buddy created with course → 📚 Course-grounded + `Sources (4)` (0.425/0.689/0.793/0.794); Buddy without course → 🧠 General, no sources |

## 4. Open decisions

| Decision | ADR | Blocking |
|---|---|---|
| PDF → Markdown tool | ADR-008 (Proposed) — only needed if later weeks arrive as PDFs | later weeks |
| Relevance threshold / final `top_k` | — to be added after Phase 7 | evaluation only |
| Supplementary uploads in V1? | — to be added | Phase 9 |

Resolved: chat model (ADR-007), embeddings (ADR-007b), chunking (ADR-015), three T's + Task
per message (ADR-017), three pages (ADR-018), additive migrations (ADR-019).

## 5. Blockers

| Blocker | Impact | Next action |
|---|---|---|
| Week 2+ course material not yet available | Evaluation rests on a single lecture | Add each week as `week<N>/week<N>_complete_rag.md` and re-run `ingest.py` (R-02) |

Nothing else blocks progress.

## 6. Next three actions

1. **Phase 7 — evaluation** (`SG-070` … `SG-072`): 8–10 questions (including 2–3 the slides do
   not cover), answers from the app or `ask.py --compare`, ratings filled into
   `docs/evaluation/rag-comparison-results.md`.
2. **Phase 8 — regression comparison** (`SG-080` … `SG-084`): `Salary_Data.csv`, sklearn
   baseline, RAG collection from the reference split only, MAE table in
   `docs/evaluation/regression-vs-rag.md`.
3. **Phase 9 — packaging** (`SG-090` … `SG-094`): failure-mode pass, README polish, demo
   rehearsal, synopsis (≤ 5 pages).

## 7. Resume checklist for a new session or agent

- [ ] Read this file, [backlog.md](backlog.md), [design-review.md](design-review.md) §4 and the relevant design/architecture doc.
- [ ] Confirm the phase in §1 is still accurate; if not, fix it first.
- [ ] Pick a `Ready` ticket with no open dependencies; create a branch for it.
- [ ] Run `uv run pytest -q` before and after the change.
- [ ] Update the ticket state and rewrite §5–§7 of this file before ending the session.

## 8. Session log

| Date | Session focus | Outcome |
|---|---|---|
| 2026-10-30 | Project setup: rules, tracking docs, plan | `.clinerules/` created; `docs/plan/`, `docs/architecture/tech-stack.md`, `docs/RAG/knowledge-base.md`, `docs/evaluation/*` created; environment audited; Phase 0 defined. No code written (by design). |
| 2026-10-30 (2) | Design review + Phase 0 bootstrap | `docs/plan/design-review.md` with 12 findings (D-01…D-12); Phase 0 started: `pyproject.toml`, `.python-version`, `requirements.txt`, `app/{__init__,errors,config,main}.py`, `tests/{conftest,unit/test_config}.py`; `uv sync` on CPython 3.12; 10 tests pass; ruff and mypy clean; course material discovered and docs re-aligned; ADR-013/014 added. |
| 2026-10-30 (3) | Phases 1–5: chunking, index, prompts, graph, services | Models verified (`llama3.2:3b` 2.9 s, `nomic-embed-text` 768-d); Chroma server up; loader + chunker + embedder + retriever + chroma client; `scripts/{smoke_llm,ingest,search,ask}.py`; 57 chunks indexed idempotently; retrieval verified (Overfitting section, distance 0.416); domain model + SQLite store; 4T prompt builder with grounding rules; LangGraph routing + Ollama client + Buddy/Chat services; **83 tests**, ruff and mypy clean; end-to-end `--compare` run recorded. |
| 2026-10-30 (4) | Phase 6: Streamlit UI + decisions | ADR-017 (three T's, Task per message), ADR-018 (three pages), ADR-019 (additive migrations); FR-14 reworded; streaming through the same graph (state `on_token`); seeded Buddy pair (FR-14); `retrieval_top_k` persisted; pages `app/ui/{chat,buddies,about}_page.py` + `clients.py` + `components.py`; dark theme in `.streamlit/config.toml`; **90 tests** (incl. 4 AppTest), ruff/mypy clean; verified in the browser: grounded answer + `Sources (4)` and general answer without sources. |
