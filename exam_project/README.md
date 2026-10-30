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

## Project Documentation

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
