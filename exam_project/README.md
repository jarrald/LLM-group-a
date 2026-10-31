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

Materialet dækker nu uge **1, 2, 3, 4, 6, 8, 9 og 10**: 85 Markdown-dokumenter og
1.659 chunks. Uge 5 og 7 findes ikke i det uploadede råmateriale.
Se [materialeoversigten](docs/RAG/llm_for_developers/llm_friendly/README.md) for kilder,
ugeoversigter, PDF-sider, notebookceller og beskrivelser af animationerne.

Efter nye uploads til `source/` kan materialet konverteres og kontrolleres lokalt:

```powershell
uv sync --group conversion
uv run --group conversion python .\scripts\convert_course_material.py --ocr
uv run --group conversion python .\scripts\check_course_material.py --verify-pdfs
uv run python .\scripts\ingest.py --recreate
```

Chroma skal køre under ingestion. `--recreate` genopbygger kursusindekset med
chunker-version 2; råmateriale og samtaler bevares. Konverteringen bruger ingen ekstern
LLM og springer `.env`, virtuelle miljøer og caches over.

### Useful CLI equivalents

```powershell
uv run python .\scripts\smoke_llm.py                 # are the models installed, and how fast?
uv run python .\scripts\search.py "What is prompt injection?" --top-k 3
uv run python .\scripts\ask.py --compare "What is overfitting?"   # RAG vs non-RAG side by side
uv run pytest -q                                     # 103 tests, no live services needed
```

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `FAIL no Markdown found inside a week<N> directory` | no `.md` under any `week<N>` directory | put the files under `docs/RAG/llm_for_developers/llm_friendly/week<N>/` |
| `Collection … is not available` / `0 chunks` | the material was never indexed | `uv run python .\scripts\ingest.py` |
| `Cannot reach the Chroma server` | server not running | `uv run chroma run --path .\data\chroma` in its own terminal |
| `chroma: command not found` | the CLI lives in `.venv\Scripts` | use `uv run chroma …` (never a bare `chroma`) |
| `Cannot reach the model …` in the chat | Ollama stopped or model missing | start Ollama, `uv run python .\scripts\smoke_llm.py` |
| `STUDYGRAPH_EMBEDDING_DIM` mismatch | different embedding model than the index | set the dimension, then `uv run python .\scripts\ingest.py --recreate` |
| Answers say "retrieval failed" | Chroma down, or collection missing | see the two rows above |

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

Current state: requirements, design, architecture, stack and plan are documented; the
application is **not implemented yet** (Phase 0 of the implementation plan). See
[`docs/plan/status.md`](docs/plan/status.md) for the live status, blockers and next steps.
