# Working agreement & verification (always active)

## Before editing

1. Read `docs/plan/status.md` (where the project is) and the relevant design/architecture doc.
2. Restate the task in one or two sentences, list the files you intend to touch, then edit.
3. Work on **one ticket at a time** from `docs/plan/backlog.md`, on a branch named after it.
4. Do not restructure the project, introduce a framework or rename modules unasked.

## Verification — required, not optional

Run and report the **exact command and its real output** before claiming something works:

```powershell
uv run pytest -q
uv run ruff check .
uv run mypy app
uv run streamlit run app/main.py
```

- If you could not run something (service down, dependency missing), say so explicitly
  and describe what remains unverified. Never present "should work" as "works".
- Never fabricate measured results, test counts, timings or evaluation scores.
- A change that touches retrieval or prompt construction must be verified with a real
  run showing retrieved chunk ids and the final answer, not only with mocks.

## Definition of done for a ticket

- [ ] Code + tests added, default test run green.
- [ ] `ruff check` and `mypy app` clean (or the new issues are explained).
- [ ] `docs/plan/backlog.md` updated (status), `docs/plan/status.md` updated at session end.
- [ ] Any decision taken is recorded in `docs/plan/decision-log.md`.
- [ ] No secrets, generated data, model files or PDFs staged for commit.

## Never do

- Never commit `data/chroma/`, `.venv/`, `.env`, `.streamlit/secrets.toml`, model blobs,
  or lecture PDFs.
- Never call an online LLM API from the application. Online assistants may be used to
  *develop* the project, but the delivered app must generate its answers locally (this is
  an explicit non-negotiable requirement of the assignment).
- Never put prompts inline in UI code or SQL in views.
- Never silently swallow an exception to make the demo look clean.
- Never edit the course-provided requirements file.

## Ask the user first when

- Adding or upgrading a dependency.
- Changing the layering, the SQLite schema, the collection name, or the embedding model.
- Changing prompt templates, `top_k`, or anything that invalidates recorded results.
- Deleting files, branches, or data directories.
