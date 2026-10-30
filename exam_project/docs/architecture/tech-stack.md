# StudyGraph — Technology Stack

Status: **proposed stack, pending team sign-off** (see
[decision log](../plan/decision-log.md)). This document resolves most of the open
decisions listed in [architecture.md](architecture.md) §8, [requirements.md](../requirements/requirements.md) §7
and [rag-pipeline.md](rag-pipeline.md) §10.

Verified on 2026-10-30 on the development machine (Windows 11, PowerShell 7).

## 1. Stack summary

| Concern | Choice | Version basis | Why |
|---|---|---|---|
| Language | Python **3.12**, managed with **uv** | uv-managed `cpython-3.12.12` already present | Avoids missing wheels on the machine default (3.14.7); `uv` gives reproducible, lockable environments |
| UI | **Streamlit** | 1.66.1 | Chat primitives (`st.chat_message`, `st.chat_input`, `st.write_stream`), multi-page, app-testable, no JS build step |
| Orchestration | **LangGraph** | 1.2.18 | Explicit graph for RAG / non-RAG routing and the retrieval-failure branch; state carries sources to the UI; matches a course topic |
| Vector store | **ChromaDB**, **server mode** | 1.5.9 | Simple local vector DB; server mode is required for the inspection UIs; metadata filtering (course, lecture) |
| Vector store UI | **ChromaUI** (inspection only) | [Riko136/ChromaUI](https://github.com/Riko136/ChromaUI), Node ≥ 20, port 3000 | Visual browsing of collections/chunks during development and demo; **not** part of the delivered runtime |
| Embeddings | **Ollama** embedding model, default proposal `nomic-embed-text` (768-d) | via `ollama.embed()` | One local runtime for chat and embeddings; no `torch`/`onnxruntime`; fixed dimension |
| LLM | **Ollama**, chat model **TBD** (candidates `llama3.2:3b`, `qwen2.5:7b`) | Ollama 0.35.1 installed | Assignment requires locally running generation |
| App persistence | **SQLite** via stdlib `sqlite3` | Python stdlib | Buddies, conversations, messages, snapshots; transactional; zero new dependency; inspectable |
| Prompts | Markdown templates in `app/prompts/` + Python builder | — | Visible, diffable, versionable; the 4T's stay inspectable |
| Tests | **pytest** + `streamlit.testing.v1.AppTest` | — | Matches repo-root convention |
| Lint / types | **ruff**, **mypy** | repo-root `pyproject.toml` | Already configured for the repository |
| Experiment only | **scikit-learn**, numpy | — | Linear-regression half of the required comparison exercise |

## 2. Runtime topology

```text
┌────────────────────────────┐
│ Browser                    │
│  Streamlit UI  :8501       │
└─────────────┬──────────────┘
              │ calls services (never adapters directly)
┌─────────────▼──────────────┐        ┌──────────────────────────┐
│ app/ (Streamlit + services)│───────▶│ Ollama server :11434     │
│  LangGraph chat flow       │  HTTP  │  chat model + embed model│
└──────┬──────────────┬──────┘        └──────────────────────────┘
       │              │
       │ HTTP         │ sqlite3
┌──────▼──────────┐ ┌─▼─────────────────┐     ┌──────────────────┐
│ Chroma server   │ │ data/studygraph.db│     │ ChromaUI :3000   │
│ :8000 (vectors) │ │ buddies, convos,  │◀────│ (dev tool only)  │
└─────────────────┘ │ messages          │     └──────────────────┘
                    └───────────────────┘
```

Three processes are required for the app; ChromaUI is an optional fourth, developer-only.

## 3. Planned dependencies

Runtime (`requirements.txt` / `pyproject.toml [project.dependencies]`):

```text
streamlit>=1.66,<2
chromadb>=1.5,<2
langgraph>=1.2,<2
ollama>=0.6
```

Development: `pytest`, `ruff`, `mypy`.

Experiment only (kept out of the app runtime): `scikit-learn`, `numpy`.

Nothing else gets added without a decision-log entry. In particular **no LangChain**
(the README currently says LangChain — it is superseded by LangGraph), no ORM, no pydantic
in our own code, no `sentence-transformers`/`torch`.

## 4. Decisions this document makes explicit

1. **Chroma in server mode**, started with `chroma run --path .\data\chroma`, because
   ChromaUI, `chromadb-admin` and `chroma browse` all attach to a running server. The app
   uses `chromadb.HttpClient`; tests use `EphemeralClient`.
2. **Embeddings are computed in our code** (`app/adapters/embedder.py`) and passed to
   Chroma explicitly. Chroma's default embedding function is not used — it downloads an
   ONNX model and would add an `onnxruntime` dependency plus a silent 384-d default.
3. **ChromaUI is tooling, not product.** It is a small third-party project (Node ≥ 20,
   Express backend on `:3000` plus a Vite dev server; connects to a Chroma server with
   tenant/database fields). If it is unavailable, the official
   `chroma browse <collection> --local` terminal UI or `chromadb-admin` (`:3434`) are
   acceptable substitutes. The delivered application must not depend on any of them.
4. **SQLite for application data**, Chroma only for vectors. Snapshot JSON is stored
   alongside a `snapshot_version` so old conversations keep working.
5. **uv + Python 3.12** for the project environment, while the machine default stays 3.14.7.

## 5. Open items requiring sign-off

| Item | Why it is still open | How it gets closed |
|---|---|---|
| Chat model (size/quality vs. hardware) | No general chat model is pulled on the machine yet; only custom `tester`/`deploy`/`docs` models exist | Phase 0 spike: pull two candidates, time one answer, judge quality on 3 course questions |
| Embedding model & dimension | `nomic-embed-text` proposed but not yet pulled or measured | Phase 1 spike: compare retrieval quality and speed of one or two embedding models |
| Chunk size / overlap / `top_k` | Depends on the real slide structure | Phase 2, measured against real questions |
| PDF → Markdown conversion tool | Depends on slide layout quality | Phase 1 spike on the real lecture PDFs |
| Whether supplementary uploads are in V1 | Optional per requirements §5.2 | Decide after the core flow works |

## 6. Environment facts (verified 2026-10-30)

| Fact | Value |
|---|---|
| Default Python | 3.14.7 (`C:\Python314\python.exe`) |
| Other interpreters | 3.10 (`C:\Program Files\Python310`), uv-managed 3.12.12 |
| `uv` | `C:\Users\novij\.local\bin\uv.exe` |
| Ollama | 0.35.1 installed; server answered on `http://127.0.0.1:11434` during the check |
| Ollama models present | `tester:latest`, `deploy:latest`, `docs:latest` — **no chat model, no embedding model** |
| streamlit / chromadb / langgraph / ollama (Python) | **not installed** in the global environment |
| Repo state | branch `mandatory-1`, commit `ee24e04`; `exam_project/` contains only `README.md` + `docs/` |
