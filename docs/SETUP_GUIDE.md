# Setup Guide — Reproduce the Recommended Workflow (Hermes + Ollama)

This guide lets a third party reproduce the recommended local multi-LLM workflow
(**Hermes Agent** routing to two local Ollama endpoints) on Windows 11 +
PowerShell 7.

## 1. Prerequisites

- Windows 11, PowerShell 7 (`pwsh`).
- [Ollama](https://ollama.com) installed and on `PATH`.
- Enough disk + RAM for a tool-calling model. `qwen2.5-coder:32b` is ~20 GB and
  benefits from 24 GB+ RAM/VRAM; CPU-only works but is slower.
- Git (for reviewing the agent's file changes).

## 2. Install Ollama and pull the models

```powershell
ollama --version
ollama pull qwen2.5-coder:32b   # primary tool-calling model
ollama pull qwen2.5-coder:7b    # optional secondary/fallback model
```

> Tool calling matters: Hermes edits files and runs commands through tool calls.
> Use a model that supports tool calling (`qwen2.5-coder:32b` or `gemma4:31b`).
> Small chat-only models (e.g. `llama3.2:3b`) cannot call tools.

## 3. Start two local model endpoints

Open two terminals and run one Ollama server in each:

```powershell
# Terminal 1 — Endpoint A (primary)
$env:OLLAMA_HOST = "127.0.0.1:11434"
$env:OLLAMA_CONTEXT_LENGTH = "64000"
ollama serve
```

```powershell
# Terminal 2 — Endpoint B (secondary / fallback)
$env:OLLAMA_HOST = "127.0.0.1:11435"
$env:OLLAMA_CONTEXT_LENGTH = "64000"
ollama serve
```

> Hermes requires ~64k tokens of context for agentic tool use. Ollama defaults to
> 2048–4096, so `OLLAMA_CONTEXT_LENGTH=64000` (or a `Modelfile` with
> `PARAMETER num_ctx 64000`) is required.

Verify both endpoints:

```powershell
Invoke-RestMethod http://127.0.0.1:11434/api/tags
Invoke-RestMethod http://127.0.0.1:11435/api/tags
```

## 4. Install Hermes

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Confirm it is on `PATH` (open a new terminal if needed):

```powershell
hermes doctor
```

## 5. Configure Hermes

Run the interactive setup and choose a **Custom endpoint**:

```powershell
hermes setup
```

- Base URL: `http://localhost:11434/v1`
- API key: leave empty (Ollama needs none)
- Model: `qwen2.5-coder:32b`

Or edit `~/.hermes/config.yaml` directly:

```yaml
model:
  default: qwen2.5-coder:32b
provider: custom
base_url: http://localhost:11434/v1
context_length: 64000
```

### Two endpoints (the hard requirement)

Hermes routes between multiple providers via **Provider Routing** (priority,
whitelist/blacklist) and automatic **fallback providers**. Add the second Ollama
endpoint (`http://localhost:11435/v1`) as an additional provider and set its
routing priority/fallback in `~/.hermes/config.yaml`. See the Hermes
*AI Providers / Provider Routing* documentation for the exact keys.

## 6. Run a demo task

```powershell
# Start Hermes in a project directory and give it a coding task
cd C:\path\to\project
hermes
# > Add a POST /api/login endpoint with tests, run the tests, and update the README.
```

Review the resulting file diffs and checkpoints (`/rollback` to undo).

## 7. Run tests and record results

```powershell
python -m pytest -q
python -m ruff check .
```

Record the results in your quality report, and validate deployment with your
checklist or script.
