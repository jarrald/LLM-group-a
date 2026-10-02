---
paths:
  - "tests/**"
  - "**/test_*.py"
  - "**/*_test.py"
---

# Testing rules

- **Framework:** `pytest` (previously pytest 8.2.2). Install with
  `python -m pip install pytest` and run `python -m pytest -q` from the repo root.
- **Note:** `tests/` currently holds only stale `__pycache__` bytecode — no test
  sources exist. If you add tests, create real `test_*.py` files here.
- **No live services:** tests must not require a running Ollama server. Monkeypatch
  `urllib.request.urlopen` and/or `ask_ollama` instead of making network calls.
- **Naming:** `test_<unit>_<behavior>`, one behaviour per test, arrange-act-assert.
- **Coverage targets:** pure helpers and config/env parsing (`os.getenv` defaults),
  `verify_models` error paths, and the Flask routes (`/api/health`, `/api/workflow`)
  using Flask's test client.
- Do not commit `.pytest_cache/` or `__pycache__/` (already covered by `.gitignore`
  and `.clineignore`).
