# LLM-group-a

## Start Flask-workflowet

Installer Python-afhængigheden:

```powershell
python -m pip install -r requirements.txt
```

Kør workflowet direkte fra terminalen:

```powershell
python .\model\ollama_workflow.py
```

Programmet spørger derefter, hvad systemet skal kunne. Du kan også skrive
kravet direkte:

```powershell
python .\model\ollama_workflow.py "Lav en todo-app med login"
```

Terminalen viser resultatet som læsbar tekst. Tilføj `--json`, hvis resultatet
også skal udskrives som JSON:

```powershell
python .\model\ollama_workflow.py "Lav en todo-app med login" --json
```

Start webappen:

```powershell
python .\model\ollama_workflow.py --web
```

Åbn derefter http://127.0.0.1:5000 i browseren. Ollama skal køre på
`http://localhost:11434`, og modellerne skal være installeret:

```powershell
ollama pull qwen2.5-coder:7b
ollama pull llama3.2:3b
```

Modellerne kan ændres uden kodeændringer:

```powershell
$env:ARCHITECT_MODEL = "qwen2.5-coder:7b"
$env:REVIEWER_MODEL = "llama3.2:3b"
python .\model\ollama_workflow.py --web
```

API'et har `GET /api/health` til kontrol af Ollama og `POST /api/workflow`
med JSON-feltet `requirement`.

Workflowet bruger 10 specialiserede agenter, som kører parallelt:

- Funktionelle krav: Architecture, Tech Lead, Implementation, Testing & Quality, Documentation og Deployment Validation.
- Non-funktionelle krav: Predictability & Control, Reproducibility, Context Management og Security Baseline.

De to lokale Ollama-modeller bruges som model-backends for agenterne. Fordelingen
ændres i `model/ollama_workflow.py` i dictionary'en `AGENTS`.

`Traits`, `Tasks`, `Tone` og `Targets` er prædefineret øverst i Python-filen som
`DEFAULT_TRAITS`, `DEFAULT_TASKS`, `DEFAULT_TONE` og `DEFAULT_TARGETS`. De vises
ikke i browseren, men kan ændres direkte i koden.
