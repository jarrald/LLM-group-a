# Context hygiene (always active)

Goal: keep the context window small and relevant. This workspace is **only** the
`exam_project` (StudyGraph) sub-project.

## Scope boundaries

- Work exclusively inside `exam_project/`. The parent repository contains unrelated
  completed deliverables (`MA1_aflevering/`, `MA2_aflevering/`, `workspace/`,
  `output/`, `model/`, `prompting and societal implications/`). Do not read, search,
  import or "fix" them.
- The parent `.clinerules/` and `AGENTS.md` describe a different project (a Flask
  Ollama workflow). Their *structure* is a convention to mirror, their *content* is
  not a rule for this project.

## Never read, search, `@`-mention or commit

- `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.venv/`.
- `data/chroma/` — Chroma's binary SQLite + HNSW index files. Query the HTTP API or
  use `chroma browse` instead of opening these files.
- Lecture slides as `*.pdf`/`*.pptx`. Work from the converted Markdown in
  `data/course_material/**/markdown/`. The course-provided assignment file
  `docs/exam_project_requirements_llm_for_developers_joint_teaching_draft_v4.md`
  is the text version to use.
- `.streamlit/secrets.toml`, `.env`, `*.log`, model blobs, `.zip`.
- Ollama/Chroma model caches outside this repo.

## What to work with instead

- Read `README.md`, `docs/plan/status.md` and `docs/plan/decision-log.md` first; they
  state where the project actually is.
- Prefer `read_files` on explicit paths over broad recursive searches. When searching,
  scope to `app/`, `scripts/`, `tests/`, `docs/` or `data/course_material/`.
- Use the **cocoindex** semantic search tool to locate code by meaning instead of
  opening many files.
- Use the **context7** tools for library documentation (Streamlit, LangGraph, Chroma,
  Ollama). Do not paste whole upstream docs into the chat; extract only the API you need.
- Use the **playwright** tools only to verify the running Streamlit UI; never as a
  substitute for reading code.

These rules are backed by `exam_project/.clineignore`.
