# Quality Report

Results from a real run of the test and static-check toolchain on the current
`mandatory-1` branch.

## Test results

| Test type | Command | Result |
| --- | --- | --- |
| Unit (pytest) | `python -m pytest -q` | `16 passed in 0.11s` |

Covered units: environment-variable parsing (defaults + endpoint routing), the
Ollama helpers (`ask_ollama`, `_installed_models`, `verify_models`), the parallel
workflow runner (`run_workflow`), and the Flask routes (`/api/health`,
`/api/workflow`).

## Static checks

| Check | Command | Result |
| --- | --- | --- |
| Lint | `python -m ruff check model tests` | `All checks passed` |
| Format | `python -m ruff format --check model tests` | `5 files already formatted` |
| Type check | `python -m mypy model` | `Success: no issues found in 1 source file` |

Tool configuration lives in `pyproject.toml` (ruff `line-length = 240`,
`target-version = "py39"`, lint rules `E F I W`, `line-ending = "cr-lf"`; mypy
`ignore_missing_imports` for Flask).

## Known limitations

- Tests monkeypatch `urllib.request.urlopen` and `ask_ollama`; they do **not**
  require a running Ollama server, so the suite is deterministic and offline.
- No automated end-to-end test performs a real LLM generation — that is exercised
  by the manual demo (`docs/SETUP_GUIDE.md`) to avoid non-deterministic assertions.
- The two endpoints are unit-tested independently; a full two-server run is
  documented rather than asserted in CI.

## Known risks

- Local models are non-deterministic, so generated artifacts vary between runs
  (mitigated by versioning the workflow config and prompts in Git).
- `qwen2.5-coder:7b` / `llama3.2:3b` are small models; output quality depends on
  prompt framing and host hardware.
- Parallel Ollama calls are bounded by `MAX_PARALLEL_AGENTS` (default `2`) to avoid
  RAM exhaustion on modest hardware.
