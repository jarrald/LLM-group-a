# StudyGraph

**A local LLM-powered study assistant using Retrieval-Augmented Generation (RAG).**

StudyGraph helps students understand and revise their course material through an AI assistant grounded in their actual lecture slides and notes.

The application uses a predefined knowledge base built from course slides converted from PDF to Markdown. Students can ask questions, request explanations of difficult concepts, and generate practice questions based on the available course material. They can also upload additional materials to extend the knowledge base.

The project explores how locally running language models and Retrieval-Augmented Generation can support learning by grounding AI-generated answers in relevant course materials.

## Key Features

- **Course-specific answers:** Retrieve relevant information from predefined course materials before generating responses.
- **Source references:** Help students trace answers back to the relevant course materials.
- **Study assistance:** Get explanations and generate practice questions based on course content.
- **Optional document uploads:** Extend the knowledge base with personal notes and supplementary materials.
- **Local inference:** Explore running the language model and retrieval pipeline locally without relying on external LLM APIs.

## Technology

| Concern | Choice |
|---|---|
| Language | Python 3.12 (managed with `uv`) |
| Interface | Streamlit |
| Orchestration | LangGraph |
| Vector store | ChromaDB (local server) + ChromaUI for inspection |
| Local LLM | Ollama (chat + embedding models) |
| Application data | SQLite |

Full rationale, versions, runtime topology and the decisions still open:
[`docs/architecture/tech-stack.md`](docs/architecture/tech-stack.md).

## Running it locally

Prerequisites: **Python 3.12** (handled by `uv`), **Ollama** running, and PowerShell on
Windows. Three local processes: Ollama, the Chroma server, and the app.

```powershell
# 1. once: environment + models (~2.3 GB download)
uv sync
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# 2. terminal 1: vector store (keep it running)
uv run chroma run --path .\data\chroma

# 3. once, and after adding course material: index the lectures
uv run python .\scripts\ingest.py

# 4. terminal 2: the app
uv run streamlit run app/main.py
```

Open <http://localhost:8501>. Pages: **Chat** (start a conversation from a Buddy, choose the
Task per message, read the sources), **Buddies** (create/edit the three T's and the course
material), **About** (models, index size, data locations).

**Check your setup in one command:**

```powershell
uv run python .\scripts\doctor.py
```

It verifies the interpreter, prompt templates, course material, both Ollama models, the Chroma
server and the index, and prints the exact command to fix anything that is missing.

### Course material

The RAG input is every Markdown file inside a `week<N>` directory:

```text
docs/RAG/llm_for_developers/
├── source/…                         # original PDFs and notebooks (git-ignored)
└── llm_friendly/
    ├── week1/week1_complete_rag.md
    ├── week2/week2_prompt_engineering_rag.md
    └── week3/week3_overview.md, week3_hallucinations.md, …
```

The material now covers weeks **1, 2, 3, 4, 6, 8, 9 and 10**: 85 Markdown documents and
1,660 chunks. Weeks 5 and 7 are not in the uploaded raw material. The corpus is written in
English so that it matches the language of the embedding model; the only exception is the two
deliberate language-sample corpora in `week3`.
See the [material overview](docs/RAG/llm_for_developers/llm_friendly/README.md) for sources,
week overviews, PDF pages, notebook cells and descriptions of the animations.

After new uploads to `source/`, the material can be converted and checked locally:

```powershell
uv sync --group conversion
uv run --group conversion python .\scripts\convert_course_material.py --ocr
uv run --group conversion python .\scripts\check_course_material.py --verify-pdfs
uv run python .\scripts\ingest.py --recreate
```

Chroma must be running during ingestion. `--recreate` rebuilds the course index with
chunker version 2; raw material and conversations are preserved. The conversion uses no
external LLM and skips `.env`, virtual environments and caches.

The index records a fingerprint of the material it was built from. `doctor.py` compares it
with what is on disk and says when the index is stale, so a translated or corrected lecture
cannot silently be answered from the previous index:

```powershell
uv run python .\scripts\doctor.py      # "Index freshness: index matches the 1660 chunks on disk"
```

### Changing the embedding model

The embedding model is configuration, not code (`STUDYGRAPH_EMBED_MODEL`, dimension
`STUDYGRAPH_EMBEDDING_DIM`). A different model produces vectors that cannot be compared with
an existing index, so the collection metadata pins the model and the dimension and the app
refuses to query a mismatch. Change both and rebuild:

```powershell
$env:STUDYGRAPH_EMBED_MODEL = "nomic-embed-text"
$env:STUDYGRAPH_EMBEDDING_DIM = "768"
uv run python .\scripts\ingest.py --recreate
```

Rebuilding all 1,660 chunks took 14 s on this machine; the 2026-10-31 run on CPU took 569 s.

### Useful CLI equivalents

```powershell
uv run python .\scripts\smoke_llm.py                 # are the models installed, and how fast?
uv run python .\scripts\search.py "What is prompt injection?" --top-k 3
uv run python .\scripts\check_retrieval.py           # re-run the recorded retrieval checks
uv run python .\scripts\ask.py --compare "What is overfitting?"   # RAG vs non-RAG side by side
uv run pytest -q                                     # 119 tests, no live services needed
```

### The separate regression experiment

`regression/` holds the *other* experiment (linear regression vs. local LLM + RAG on the same
held-out rows). It has its own corpus — a scikit-learn source checkout — which is third-party
source, git-ignored and therefore **downloaded** rather than committed:

```powershell
uv run python -m regression.fetch_corpus          # ~23 MB, once
uv run python -m regression.rag --build-index     # source + guidance docs, in-process Chroma
uv run python .\regression\compare-predictions.py # the comparison, RAG and no-RAG arms
```

The index holds the scikit-learn source and the project's own guidance documents in
`regression/rag-optimized/`; `RAG_EXTRA_CORPUS=none` builds the source-only index.

`uv run python -m regression.rag --status` prints the corpus provenance and the index state.
Details, prompts and the recorded runs: [`regression/README.md`](regression/README.md).

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `FAIL no Markdown found inside a week<N> directory` | no `.md` under any `week<N>` directory | put the files under `docs/RAG/llm_for_developers/llm_friendly/week<N>/` |
| `Collection … is not available` / `0 chunks` | the material was never indexed | `uv run python .\scripts\ingest.py` |
| `Collection … does not match the current configuration` | the index was built with another chunker/embedding model | `uv run python .\scripts\ingest.py --recreate` |
| `Index freshness … index holds chunks from different material` | the material changed after the last indexing run (e.g. the English translation) | `uv run python .\scripts\ingest.py --recreate` |
| `Cannot reach the Chroma server` | server not running | `uv run chroma run --path .\data\chroma` in its own terminal |
| `chroma: command not found` | the CLI lives in `.venv\Scripts` | use `uv run chroma …` (never a bare `chroma`) |
| `Cannot reach the model …` in the chat | Ollama stopped or model missing | start Ollama, `uv run python .\scripts\smoke_llm.py` |
| `STUDYGRAPH_EMBEDDING_DIM` mismatch | different embedding model than the index | set the dimension, then `uv run python .\scripts\ingest.py --recreate` |
| `ModuleNotFoundError: matplotlib` / `sklearn` in `regression/*.ipynb` | `uv sync` installs only what `pyproject.toml` declares, and prunes everything else | `uv sync`, then restart the kernel (ADR-021) |
| `the scikit-learn corpus is missing` (regression) | the third-party corpus is git-ignored and was never downloaded | `uv run python -m regression.fetch_corpus` |
| `the index in …\.chroma does not match the corpus/settings` (regression) | new corpus, ref or `RAG_EMBED_MODEL` | `uv run python -m regression.rag --build-index --recreate` |
| Answers say "retrieval failed" | Chroma down, or collection missing | see the rows above |

Local data lives in `data/` (`studygraph.db`, `chroma/`) and is git-ignored. Delete
`data/studygraph.db` to start with a fresh database and the seeded Buddy pair.


Additional documentation is maintained in the [`docs/`](docs/) directory:

- **Plan & tracking:** [`docs/plan/`](docs/plan/) — current status, implementation plan,
  backlog, decision log, risks. Start with [`status.md`](docs/plan/status.md).
- **Design:** [`docs/design/`](docs/design/) — product goals, user needs, scope, and design decisions.
- **Architecture:** [`docs/architecture/`](docs/architecture/) — system components, data flow,
  stack, and RAG implementation.
- **Requirements:** [`docs/requirements/`](docs/requirements/) — functional and non-functional requirements.
- **Knowledge base:** [`docs/RAG/`](docs/RAG/) — how course material is prepared, chunked and indexed.
- **Evaluation:** [`docs/evaluation/`](docs/evaluation/) — RAG vs. non-RAG comparison and the
  linear regression vs. LLM + RAG experiment.

## Project Status

StudyGraph is an educational software prototype exploring local LLMs and Retrieval-Augmented
Generation for course-specific study assistance.

Current state: the application is working — three Streamlit pages on top of the same services the
CLI uses, 119 passing tests and an 85-document course corpus (1,660 chunks). The Chroma index was
rebuilt from the translated English corpus on 2026-11-10 (`llms_for_devs_v1`, 1,660 chunks,
corpus digest `62313c4629307e08`), so course-grounded answers come from the current material;
`doctor.py` now reports when the index and the material on disk diverge. See
[`docs/plan/status.md`](docs/plan/status.md) for the live status, blockers and next steps.
