# Operational Runbook

## Prerequisites

- Windows 11 + PowerShell 7, Python 3.9+, Git, Ollama.
- Models pulled: `qwen2.5-coder:7b` and `llama3.2:3b`.

## Start the endpoints

```powershell
# Endpoint A (architect-role)
$env:OLLAMA_HOST = "127.0.0.1:11434"; ollama serve

# Endpoint B (worker/reviewer) — separate process/terminal
$env:OLLAMA_HOST = "127.0.0.1:11435"; ollama serve
```

## Configure and run the workflow

```powershell
$env:ARCHITECT_ENDPOINT = "http://127.0.0.1:11434"
$env:WORKER_ENDPOINT     = "http://127.0.0.1:11435"
$env:ARCHITECT_MODEL     = "qwen2.5-coder:7b"
$env:WORKER_MODEL        = "llama3.2:3b"

python .\model\ollama_workflow.py "Lav en todo-app med login" --json
# or start the web app
python .\model\ollama_workflow.py --web
```

## Health checks

```powershell
# CLI: the workflow verifies both endpoints before running
# Web:  GET http://127.0.0.1:5000/api/health  -> {"status":"ok","endpoints":{...}}
```

## Run tests and static checks

```powershell
python -m pytest -q
python -m ruff check model tests
python -m ruff format --check model tests
python -m mypy model
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Ollama svarer ikke på <endpoint>` | Endpoint not running | Start the matching `ollama serve` on that port |
| `Modellen <m> er ikke installeret` | Model missing on that endpoint | `ollama pull <m>` on that endpoint |
| Timeout / RAM exhaustion | Too many concurrent calls | Lower `MAX_PARALLEL_AGENTS` |

## Deployment considerations

- Bind Ollama and Flask to `127.0.0.1`; do not expose model endpoints publicly.
- Keep secrets out of code; use environment variables.
