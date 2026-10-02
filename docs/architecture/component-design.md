# Component Design

The application is intentionally a **single file** (`model/ollama_workflow.py`) that
combines the CLI, the Flask API, the inline HTML frontend, the agent registry and
`main()`.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| Configuration constants | Read endpoints, models and concurrency from `os.getenv(...)` with defaults. |
| `AGENTS` registry | Maps each agent name to `(model, responsibility-prompt)`. |
| `ARCHITECT_ROLE_AGENTS` + `endpoint_for()` | Route each agent to `ARCHITECT_ENDPOINT` or `WORKER_ENDPOINT`. |
| `ask_ollama(model, prompt, endpoint)` | POST a prompt to `/api/generate` on a specific endpoint and return the response. |
| `_installed_models(endpoint)` / `verify_models()` | Verify each endpoint serves the model its roles need, before running. |
| `run_workflow(requirement)` | Run all ten agents in parallel with `ThreadPoolExecutor`, bounded by `MAX_PARALLEL_AGENTS`, and return a structured result. |
| `print_readable_result(...)` | Human-readable terminal output (shows model **and** endpoint per agent). |
| Flask routes (`/`, `/api/health`, `/api/workflow`) | Web frontend + JSON API. |
| `main()` | CLI entry point (`--web`, `--json`); saves the result to `output/workflow-result.json`. |

## Data flow

1. A requirement arrives via CLI argument, stdin prompt, or `POST /api/workflow`.
2. `verify_models()` confirms both endpoints serve the required models.
3. Each agent is submitted to the thread pool; `endpoint_for()` selects the target
   endpoint.
4. Results are collected, sorted back into the fixed registry order, and returned
   as a `dict[str, object]` with `requirement`, `context`, `models`, `endpoints`,
   `agent_count` and `agents` (each agent carrying `name`, `model`, `endpoint`,
   `result`).

## Interface contract

The HTTP API is specified in `docs/api/openapi.yaml`.
