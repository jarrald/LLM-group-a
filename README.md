# LLM-group-a

> **Rapport (Mandatory 1):** Sammenligningen af kandidat-værktøjerne og anbefalingen
> ligger i `docs/synopsis.md` (Hermes Agent vs. OpenHands), og gengivelsesguiden
> ligger i `docs/SETUP_GUIDE.md`. Denne README dokumenterer derudover det
> Flask-baserede prototype-workflow, som også er beholdt i repoet som reference.

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

Åbn derefter http://127.0.0.1:5000 i browseren. Workflowet understøtter to
separate lokale endpoints (et hard krav i opgaven): arkitekt-roller kører mod
`ARCHITECT_ENDPOINT`, og reviewer-/worker-roller kører mod `WORKER_ENDPOINT`.
Sættes kun `OLLAMA_URL`, falder begge endpoints tilbage på den ene server.

Modellerne skal være installeret på den endpoint, de kører mod:

```powershell
ollama pull qwen2.5-coder:7b
ollama pull llama3.2:3b
```

Endpoint, model og parallelisme styres udelukkende med miljøvariabler:

```powershell
$env:ARCHITECT_ENDPOINT = "http://127.0.0.1:11434"
$env:WORKER_ENDPOINT     = "http://127.0.0.1:11435"
$env:ARCHITECT_MODEL     = "qwen2.5-coder:7b"
$env:WORKER_MODEL        = "llama3.2:3b"
python .\model\ollama_workflow.py --web
```

| Variabel | Standard | Formål |
| --- | --- | --- |
| `OLLAMA_URL` | `http://localhost:11434` | Fælles endpoint, hvis kun én server bruges |
| `ARCHITECT_ENDPOINT` | `OLLAMA_URL` | Endpoint for arkitekt-roller (architecture, tech_lead, implementation) |
| `WORKER_ENDPOINT` | `OLLAMA_URL` | Endpoint for reviewer-/worker-roller (øvrige syv agenter) |
| `ARCHITECT_MODEL` | `qwen2.5-coder:7b` | Model for arkitekt-roller |
| `WORKER_MODEL` | `llama3.2:3b` | Model for reviewer-/worker-roller |
| `MAX_PARALLEL_AGENTS` | `2` | Maks. samtidige Ollama-kald (RAM-beskyttelse) |

API'et har `GET /api/health` til kontrol af Ollama og `POST /api/workflow`
med JSON-feltet `requirement`.

Workflowet bruger 10 specialiserede agenter, som kører parallelt:

- Funktionelle krav: Architecture, Tech Lead, Implementation, Testing & Quality, Documentation og Deployment Validation.
- Non-funktionelle krav: Predictability & Control, Reproducibility, Context Management og Security Baseline.

De to lokale Ollama-modeller bruges som model-backends for agenterne. Fordelingen
af agent → model ligger i dictionary'en `AGENTS`, og routing af agent → endpoint
styres af `ARCHITECT_ROLE_AGENTS` + `endpoint_for()` i `model/ollama_workflow.py`.

`Traits`, `Tasks`, `Tone` og `Targets` er prædefineret øverst i Python-filen som
`DEFAULT_TRAITS`, `DEFAULT_TASKS`, `DEFAULT_TONE` og `DEFAULT_TARGETS`. De vises
ikke i browseren, men kan ændres direkte i koden.

## Tests og statiske checks

```powershell
python -m pip install pytest ruff mypy

python -m pytest -q                  # unit-test (16 tests)
python -m ruff check model tests     # lint
python -m ruff format --check model tests
python -m mypy model                 # type-check
```

Konfigurationen til `ruff` og `mypy` ligger i `pyproject.toml`.

## Leverancer (dokumentation)

- `docs/architecture/` — komponentdesign, deployment-topologi og ADR'er.
- `docs/api/openapi.yaml` — API-kontrakt.
- `docs/tickets/ticket-breakdown.md` — tech lead task-opdeling.
- `docs/quality_report.md` — test-/static-check-resultater, begrænsninger og risici.
- `docs/runbook.md` — drift og fejlfinding.
- `docs/deployment-validation.md` — deploy-validering.
- `docs/synopsis.md` — synopsis (7–10 sider) med sammenligning og anbefaling.
- `docs/SETUP_GUIDE.md` — engelsk trin-for-trin gengivelsesguide.
