# LLM-group-a

LLM elective for Software Development. Reviewing two open source toolchains.

## Notebook workflow

The implementation is in [notebooks/local_multi_llm_workflow.ipynb](notebooks/local_multi_llm_workflow.ipynb).
It uses a sequential two-worker design:

1. Worker 1 handles functional requirements: service behavior, API contract, architecture artifacts and functional tests.
2. Worker 2 runs only after Worker 1 passes validation. It handles non-functional requirements: documentation, static checks, deployment validation, reproducibility and the quality report.

## Setup

Install Python 3.11+, Jupyter, pytest, Git and Ollama:

```powershell
python -m pip install jupyter pytest
```

Pull the models used by the default configuration:

```powershell
ollama pull qwen2.5-coder:7b
ollama pull llama3.2:3b
```

The assignment requires two separate local model endpoints. Start two local Ollama services in separate terminals:

```powershell
$env:OLLAMA_HOST='127.0.0.1:11434'; ollama serve
$env:OLLAMA_HOST='127.0.0.1:11435'; ollama serve
```

Open WebUI can be used to inspect models manually, but the notebook connects directly to the Ollama HTTP APIs. Endpoint URLs and models can be changed without editing worker prompts:

```powershell
$env:LLM_ENDPOINT_A='http://127.0.0.1:11434'
$env:LLM_ENDPOINT_B='http://127.0.0.1:11435'
$env:LLM_MODEL_A='qwen2.5-coder:7b'
$env:LLM_MODEL_B='llama3.2:3b'
jupyter notebook
```

Run the notebook cells from top to bottom. It creates `generated_workflow/`, executes the functional worker, runs its tests, and only then starts the non-functional worker. Review generated changes with Git before accepting them.
