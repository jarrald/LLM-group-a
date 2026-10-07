# Setup Guide — Reproducing the Local Multi-LLM Workflow

This guide lets a third party reproduce both candidate workflows from scratch:
two local model endpoints, the toolchain configured to use them, and a demo
workflow that produces architecture output, an implemented feature, executed
tests, updated docs, and a deployment-validation step.

All commands are PowerShell (Windows). Equivalent POSIX commands are noted.

---

## 1. Prerequisites

| Tool | Version used | Why |
|---|---|---|
| Ollama | 0.35.x | the two local model servers |
| Python | 3.11–3.14 (3.14 used here) | Candidate A runtime |
| `uv` | 0.10+ | isolated venv for Candidate B |
| Git | any recent | reproducibility (commits + diffs) |

**Docker is not required.** The deploy-validation requirement is satisfied by the
generated `deploy/validate_deploy.py` script plus `docs/environment.md`. The
generated `Dockerfile` is optional extra output and is **not** built or verified
by this workflow.

### Two separate Python environments

The candidates have disjoint dependencies, so they run on different interpreters.
Using the wrong one is the most common setup error:

| Candidate | Interpreter | Install once |
|---|---|---|
| **A — LangGraph** | your **system Python** | `pip install pyyaml langgraph langchain-ollama pytest` |
| **B — CrewAI** | **`.venv-crewai`** (created in §6) | `uv pip install crewai ollama pytest` |

Running Candidate A from inside `.venv-crewai` fails with
`ModuleNotFoundError: No module named 'langchain_core'`. Run `deactivate` first.

---

## 2. Configure TWO local model endpoints

The workflow requires **two separate local endpoints**. Ollama listens on
`127.0.0.1:11434` by default, so start a **second instance** on another port.
Each instance is just another `ollama serve` process with a different
`OLLAMA_HOST`.

```powershell
# Terminal 1 — first instance (the default; skip if Ollama Desktop is already running)
ollama serve                          # http://localhost:11434

# Terminal 2 — second instance on port 11435
$env:OLLAMA_HOST="127.0.0.1:11435"
ollama serve                          # http://localhost:11435
```

Both processes run side by side and are independent: the workflow can talk to
either one at the same time. Leave both terminals open while you run the
workflow.

### You only pull the models ONCE

Ollama keeps **one shared model store** on disk — by default
`%USERPROFILE%\.ollama\models` on Windows (`~/.ollama/models` on Linux/macOS).
Both instances read that same directory, which is why `ollama list` shows the
same models on both ports. So pull each model **once** and both endpoints can
serve it — no duplicate download, no wasted storage:

```powershell
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:7b
ollama pull deepseek-coder:6.7b
```

(The only way the two instances would have separate stores is if you explicitly
set a different `OLLAMA_MODELS` path for one of them — don't, unless you want
that.)

### Verify both endpoints

```powershell
curl.exe -s http://localhost:11434/api/tags
curl.exe -s http://localhost:11435/api/tags
```

### Named role models

The default config references role-named tags (`architect:latest`, `coder:latest`,
…). This repository already contains the exact `Modelfile`s used to create them
in `modelfiles/`, e.g. `modelfiles/architect.Modelfile`:

```
FROM llama3.1:8b
PARAMETER num_ctx 8192
```

Create all six role tags **once** — like `pull`, `create` writes to the same
shared model store, so both endpoints can serve them:

```powershell
foreach ($role in 'architect','techlead','coder','tester','docs','deploy') {
    ollama create "$role`:latest" -f "modelfiles\$role.Modelfile"
}
```

If you prefer not to create role tags, just edit `config/endpoints.yaml` and set
each `model:` to a base tag (e.g. `llama3.1:8b`) — routing is config-only.

---

## 3. Configure the toolchain to use both endpoints

All routing lives in **one file**: `config/endpoints.yaml`.

```yaml
endpoints:
  alpha: { base_url: "http://localhost:11434", description: "Ollama server A" }
  beta:  { base_url: "http://localhost:11435", description: "Ollama server B" }

roles:
  architect: { endpoint: alpha, model: "architect:latest" }
  techlead:  { endpoint: alpha, model: "techlead:latest" }
  coder:     { endpoint: beta,  model: "coder:latest" }
  tester:    { endpoint: beta,  model: "tester:latest" }
  docs:      { endpoint: alpha, model: "docs:latest" }
  deploy:    { endpoint: beta,  model: "deploy:latest" }

worker_pool:
  endpoints: [alpha, beta]
  max_workers: 3
```

To switch routing, edit this file **or** pass an alternative profile:

```powershell
python candidate_a_langgraph/orchestrator.py --config config/endpoints.alt.yaml
```

`endpoints.alt.yaml` swaps every role to the opposite endpoint — proving that
switching endpoints is configuration-driven, not manual rewiring.

---

## 4. Run the demo workflow (Candidate A — recommended)

```powershell
# from the repository root
python candidate_a_langgraph/orchestrator.py --run-id demo --project demo_project
```

What happens, in order:

1. **architect** → `docs/architecture.md`, `docs/adr/0001-*.md`, `api/openapi.yaml`
2. **techlead** → `tickets.json` (scope, acceptance criteria, dependency order)
3. **coders** → N>2 parallel workers, one per ticket, run in dependency-ordered
   batches across both endpoints → `src/taskflow/*.py`
4. **tester** → `tests/test_store.py`, `tests/test_service.py`, `tests/test_api.py`
5. **run_tests** → executes pytest and captures results
6. **repair** (conditional) → rewrites only the implicated files, bounded retries
7. **docs** → `README.md`, `docs/api-usage.md`, `docs/runbook.md`
8. **deploy** → `Dockerfile`, `deploy/validate_deploy.py`, `docs/environment.md`,
   then executes the validator
9. **quality** → `reports/quality_report.md`
10. **apply** → unified diff vs `demo_project`, then copy + `git commit`

Every step's raw output and the final artifacts land in `runs/<run-id>/`.

### Review mode (control before execution)

```powershell
python candidate_a_langgraph/orchestrator.py --run-id review --control review
```

In `review` mode nothing is written to `demo_project`; instead
`runs/<run-id>/diff.patch` and `runs/<run-id>/staged/` contain the proposed
changes for inspection.

---

## 5. Verify the generated artifacts

```powershell
Get-ChildItem demo_project -Recurse -File | Select-Object FullName

# run the generated tests
python -m pytest demo_project -q

# run the generated deploy validation
python demo_project/deploy/validate_deploy.py     # prints DEPLOY OK on success

# inspect the quality report and routing evidence
Get-Content runs\demo\quality_report.md
Get-Content runs\demo\run_manifest.json
```

---

## 6. Candidate B (CrewAI)

CrewAI has many dependencies, so use an isolated venv:

```powershell
uv venv .venv-crewai --python 3.12
.venv-crewai\Scripts\Activate.ps1
uv pip install crewai ollama pytest
```

- `ollama` is required by CrewAI's **native Ollama embedder** (needed if you use
  `Crew(memory=True)`).
- `pytest` is only for the host-side evaluation harness.

Run the **native** crew (recommended):

```powershell
.venv-crewai\Scripts\python.exe candidate_b_crewai\crew.py `
    --config config/endpoints.crewai.yaml `
    --run-id runB_native `
    --no-memory
```

Or the **baseline** crew used for the "before" comparison:

```powershell
.venv-crewai\Scripts\python.exe candidate_b_crewai\crew_naive.py --run-id runB_naive
```

**Two things to know (both documented in `docs/synopsis.md` §4.2.1):**

1. **Use `--no-memory`.** `Crew(memory=True)` is native, but it attaches
   *"Search memory"* / *"Save to memory"* tools to **every** agent, so any role
   bound to a model without the `tools` capability (e.g. `tester:latest`,
   deepseek-coder) gets HTTP 400 `does not support tools` from Ollama and CrewAI
   retries instead of falling back. It also hung our full multi-task crew.
   `config/endpoints.crewai.yaml` re-binds the `tester` role to a tool-capable
   model (`coder:latest`) as a config-only demonstration.
2. **CrewAI's `output_file` writes the model output verbatim**, so the generated
   `.py` files arrive wrapped in ```markdown fences and are not directly
   runnable. Stripping the fences is glue, and CrewAI has no built-in for it.

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: langchain_core` (Candidate A) | you are inside `.venv-crewai` | run `deactivate` — Candidate A needs the system Python |
| `ModuleNotFoundError: crewai` (Candidate B) | you are outside `.venv-crewai` | activate the venv: `.venv-crewai\Scripts\Activate.ps1` |
| `Connection refused` on 11435 | second instance not started | start `ollama serve` with `OLLAMA_HOST=127.0.0.1:11435` |
| Model not found | the tag was never pulled/created | `ollama pull` / `ollama create` **once** — both instances share one model store |
| Very slow first call | model cold start | expected (10–20 s); warm calls are faster |
| CrewAI crew hangs with no output | `memory=True` in a multi-task crew | add `--no-memory` |
| Ollama HTTP 400 `does not support tools` | CrewAI memory tools sent to a model without tool support | `--no-memory`, or bind a tool-capable model (`endpoints.crewai.yaml`) |
| `ModuleNotFoundError: taskflow` in deploy validator | `src` not on `sys.path` | the orchestrator sets `PYTHONPATH`; the generated script also inserts `src` |
| pytest collection error | a worker imported a module that does not exist | the repair loop rewrites the implicated file; see `quality_report.md` |
| `crewai` install fails | Python too new for some deps | use `uv venv --python 3.12` as shown |