# Deployment Validation

Validation performed on the `mandatory-1` branch (Windows 11, PowerShell 7).

| Check | Command | Result |
| --- | --- | --- |
| Syntax compiles | `python -m py_compile .\model\ollama_workflow.py` | OK |
| Dependency install | `python -m pip install -r requirements.txt` | OK (Flask 3.1.3) |
| Unit tests | `python -m pytest -q` | 16 passed |
| Lint | `python -m ruff check model tests` | All checks passed |
| Format | `python -m ruff format --check model tests` | 5 files already formatted |
| Type check | `python -m mypy model` | Success |
| Health endpoint | `GET /api/health` | `200 {"status":"ok","endpoints":{...}}` |
| Config routing | `endpoint_for()` with distinct endpoints | routes architect→A, others→B |

## Deployment checklist

- [x] Application runs from CLI and `--web`.
- [x] Both endpoints reachable and role→endpoint routing is configuration-based.
- [x] Required environment variables documented (`README.md`, `docs/runbook.md`).
- [x] Health check available (`/api/health`).
- [x] Tests and static checks pass.
- [x] No model endpoint exposed publicly (loopback only).

## Environment / configuration documentation

See `README.md` (Danish setup guide) and `docs/SETUP_GUIDE.md` (English
reproduction guide).
