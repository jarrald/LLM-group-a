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

## Agentisk tilstand (tool calling, filer og tests)

Analyse-tilstanden ovenfor lader hver agent svare med ren tekst. Den agentiske
tilstand lader i stedet udvalgte agenter kalde værktøjer, så workflowet kan
skrive rigtige filer og køre tests. Det dækker opgavens implementation-,
testing- og predictability-krav:

```powershell
# 1) Tør kørsel: agenterne foreslår filændringer som diffs (intet skrives)
python .\model\ollama_workflow.py --agentic "Lav en Python-funktion add(a, b) med en pytest-test"

# 2) Godkend og gennemfør: skriv filerne og kør de tilladte kommandoer
python .\model\ollama_workflow.py --agentic --apply "Lav en Python-funktion add(a, b) med en pytest-test"

# Egen sandkasse-mappe i stedet for standarden (workspace/)
python .\model\ollama_workflow.py --agentic --apply --workspace workspace\demo "Dit krav"
```

Agenten arbejder kun inde i sandkassen og må kun køre kommandoer på en
allowlist (`python -m pytest`, `python -m ruff`, `python -m mypy`, …). Uden
`--apply` vises ændringerne som unified diffs til gennemsyn (plan + diff), så
intet skrives eller køres uden godkendelse.

| Flag | Betydning |
| --- | --- |
| `--agentic` | Kør den agentiske pipeline i stedet for analyse |
| `--apply` | Skriv filer og kør kommandoer (ellers kun forslag) |
| `--workspace DIR` | Sandkasse-mappe (standard `workspace/`) |
| `--json` | Udskriv rå JSON |

> Tool calling: `llama3.1:8b` og `qwen3.5:9b` sender strukturerede værktøjskald.
> De mindre standardmodeller (`qwen2.5-coder:7b`, `llama3.2:3b`) skriver kaldet
> som JSON i teksten; workflowet genkender og udfører det alligevel.

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
| `WORKSPACE_DIR` | `workspace` | Sandkasse-mappe for agentens fil-operationer |
| `CONTEXT_BUDGET` | `6000` | Maks. tegn af hvert artefakt der gives videre som kontekst |
| `MAX_AGENT_ROUNDS` | `8` | Maks. værktøjs-runder pr. agent |

API'et har `GET /api/health` til kontrol af Ollama og `POST /api/workflow`
med JSON-feltet `requirement`. Feltet `mode` (`analysis` eller `agentic`) vælger
tilstand, og `apply` (`true`/`false`) afgør, om ændringer gennemføres.

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

python -m pytest -q                  # unit-test (40 tests)
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
- `docs/agentic-mode.md` — den agentiske tilstand: tool calling, fil-operationer, testkørsel og kontekststyring.
- `docs/synopsis.md` — synopsis (7–10 sider) med sammenligning og anbefaling.
- `docs/SETUP_GUIDE.md` — engelsk trin-for-trin gengivelsesguide.
