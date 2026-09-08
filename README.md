# LLM-group-a — Local Multi-LLM Coding Workflow

A Flask orchestrator that runs a local, multi-LLM software development workflow
across two separate Ollama endpoints:

```
requirement → Architect (FR1) → Tech lead (FR2) → parallel coding workers (FR3)
```

Every role is bound to an endpoint + model through configuration (Hard Requirement 1).

## Requirements

- Python 3.10+
- Ollama running, with the models pulled (see below)

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Two local endpoints

Start Ollama on its default port and a second instance on port 11435:

```powershell
ollama serve                                   # endpoint A: http://127.0.0.1:11434
$env:OLLAMA_HOST = "127.0.0.1:11435"
ollama serve                                   # endpoint B: http://127.0.0.1:11435
```

On Windows, run the second `ollama serve` in its own terminal.

Pull the models:

```powershell
ollama pull qwen2.5-coder:7b
ollama pull llama3.2:3b
```

## Configuration

Routing is defined in `config.yaml` (roles → endpoint + model). Every value can
be overridden with environment variables — see `.env.example`. Example:

```powershell
$env:ARCHITECT_MODEL = "qwen2.5-coder:7b"
$env:TECH_LEAD_MODEL = "llama3.2:3b"
$env:WORKER_COUNT    = "2"
```

## Run

Web dashboard (http://127.0.0.1:5000):

```powershell
python ollama_workflow.py --web
```

Headless pipeline run:

```powershell
python ollama_workflow.py --run "Build a minimal task manager REST API ..."
```

Check the endpoints:

```powershell
python ollama_workflow.py --health
```

## API

- `GET /api/health` — endpoint + model availability
- `POST /api/workflow` — start a run; JSON body `{"requirement": "..."}` → `202` + `run_id`
- `GET /api/runs` — list runs
- `GET /api/runs/<id>` — run status + artifacts
- `GET /api/runs/<id>/file?path=...` — read an artifact file

## Output

Each run is written to `workspace/<run_id>/`:

- `docs/` — architecture artifacts (system overview, component design, deployment topology, ADRs, OpenAPI)
- `tickets/tickets.json` — tech-lead tickets (scope, acceptance criteria, DoD, dependencies)
- `repo/` — the multi-file implementation produced by the coding workers
- `changes.diff` — reviewable diff of the generated code
- `run.json` — manifest (config snapshot, stage/ticket statuses, artifact list)

## Tests

```powershell
python -m pytest
```

## Known limitations / risks

- Small local models occasionally emit malformed JSON/YAML; each agent retries
  once with feedback, then fails the ticket in isolation.
- When several tickets touch the same file, the last writer wins (no merge).
  The tech-lead prompt encourages disjoint file ownership to avoid this.
- Runs are deterministic in structure, not in generated content.
