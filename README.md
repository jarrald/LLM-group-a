# LLM-group-a

## Start Flask-workflowet

Installer Python-afhængigheden:

```powershell
python -m pip install -r requirements.txt
```

Start webappen:

```powershell
python ollama_workflow.py --web
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
python ollama_workflow.py --web
```

API'et har `GET /api/health` til kontrol af Ollama og `POST /api/workflow`
med JSON-feltet `requirement`.
