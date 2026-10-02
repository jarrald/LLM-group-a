# Context hygiene (always active)

Goal: keep the context window small and relevant. This repo contains large generated
and binary artifacts that must never be pulled into context.

## Never read, search, open or `@`-mention
- Anything under `__pycache__/`, or any `*.pyc` / `*.pyo` / `*.pyd` file.
- `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.tox/`, `.venv/`, `venv/`.
- `workspace/` — generated Ollama run output, regenerated on every demo.
- Binary documents: `*.pdf`, `*.pptx`, `*.docx`, `*.xlsx`, images.
- Log files: `*.log`.

Use `docs/Mandatory 1.md` (text) instead of `docs/Mandatory 1.pdf`.

## What to work with instead
- The only active source file is `model/ollama_workflow.py`.
- `workflow/`, `webapp/` and `tests/` currently contain **only** stale
  `__pycache__` bytecode — their `.py` sources were removed. Do not treat them as
  source, do not import them, do not "fix" them.
- Prefer `read_files` on specific paths over broad recursive searches.
- When searching, scope to `model/`, `docs/` or `tests/` explicitly.

These rules are backed by `.clineignore`. See `AGENTS.md` §6 for the full list.
