"""Run ten specialized agents against local Ollama model backends."""

import difflib
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import cast

from flask import Flask, jsonify, render_template_string, request

# Ollama kører lokalt på disse adresser. Miljøvariabler gør det muligt at ændre
# server eller modeller uden at redigere Python-filen.
#
# Hard requirement om "minimum 2 separate lokale endpoints" løses her:
# arkitekt-roller kører mod ARCHITECT_ENDPOINT, mens reviewer-/worker-roller
# kører mod WORKER_ENDPOINT. Sættes kun OLLAMA_URL, falder begge tilbage på den,
# så eksisterende opsætninger stadig virker uden ændringer.
DEFAULT_ENDPOINT = os.getenv("OLLAMA_URL", "http://localhost:11434")
ARCHITECT_ENDPOINT = os.getenv("ARCHITECT_ENDPOINT", DEFAULT_ENDPOINT)
WORKER_ENDPOINT = os.getenv("WORKER_ENDPOINT", DEFAULT_ENDPOINT)
ARCHITECT_MODEL = os.getenv("ARCHITECT_MODEL", "qwen2.5-coder:7b")
WORKER_MODEL = os.getenv("WORKER_MODEL", "llama3.2:3b")
MAX_PARALLEL_AGENTS = int(os.getenv("MAX_PARALLEL_AGENTS", "2"))

# --- Agentisk udførelseslag (tool calling, fil-operationer, testkørsel) ---
# Ud over analyse-tilstanden kan workflowet køre agentisk: udvalgte agenter må
# kalde værktøjer og dermed skrive rigtige filer og køre tests. Alt kan styres
# med miljøvariabler og overstyres på kommandolinjen.
# Sandkasse-mappen, hvor agenterne må læse og skrive. Den er git-ignoreret.
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", "workspace")
# Hvor mange tegn af hvert tidligere artefakt der gives videre som kontekst.
# Grænsen forhindrer, at konteksten vokser ukontrolleret (context management).
CONTEXT_BUDGET = int(os.getenv("CONTEXT_BUDGET", "6000"))
# Maks. antal værktøjs-runder pr. agent, før løkken stopper af sikkerhedshensyn.
MAX_AGENT_ROUNDS = int(os.getenv("MAX_AGENT_ROUNDS", "8"))
# Kommandoer må kun starte med et af disse præfikser (sikkerhedsallowlist).
ALLOWED_COMMAND_PREFIXES = (
    "python -m pytest",
    "python -m unittest",
    "python -m ruff",
    "python -m mypy",
    "python -m compileall",
    "pytest",
    "ruff",
    "mypy",
)

# Arkitekt-rolle-agenter kører mod ARCHITECT_ENDPOINT; alle øvrige agenter
# (reviewer-/worker-roller) kører mod WORKER_ENDPOINT.
ARCHITECT_ROLE_AGENTS = {"architecture", "tech_lead", "implementation"}

# Disse fire værdier er faste standarder for alle agenter. De kan ændres her i
# koden, men brugeren skal ikke udfylde dem i browseren.
DEFAULT_TRAITS = "Specialiserede softwareudviklingsroller med tydelige ansvarsområder"
DEFAULT_TASKS = "Analysér kravet, lav konkrete leverancer, acceptance criteria og risici"
DEFAULT_TONE = "Konkret, teknisk, kortfattet og handlingsorienteret"
DEFAULT_TARGETS = "Softwareudviklere, tech leads og undervisere, der skal kunne efterprøve resultatet"

# Hver agent har ét afgrænset ansvar. Agenternes prompts køres parallelt.
AGENTS = {
    "architecture": (ARCHITECT_MODEL, "Funktionelt krav: Architecture responsibility. Lav komponenter, ansvar, interface/API-kontrakter, deployment-topologi og ADR-forslag."),
    "tech_lead": (ARCHITECT_MODEL, "Funktionelt krav: Tech lead responsibility. Opdel arbejdet i tickets med scope, out of scope, acceptance criteria, definition of done og afhængigheder."),
    "implementation": (ARCHITECT_MODEL, "Funktionelt krav: Implementation responsibility. Beskriv hvordan mindst to coding workers kan paralleliseres, hvilke filer de ændrer, og hvordan ændringer integreres og reviewes."),
    "testing_quality": (WORKER_MODEL, "Funktionelt krav: Testing & quality responsibility. Foreslå unit/integration tests, testkørsel, statiske checks, quality report, kendte begrænsninger og risici."),
    "documentation": (WORKER_MODEL, "Funktionelt krav: Documentation responsibility. Planlæg README, API-brug, runbook, konfiguration og design-/ADR-dokumentation."),
    "deployment": (WORKER_MODEL, "Funktionelt krav: Deployment validation responsibility. Lav en deploy-checkliste eller script-plan med build, container, miljøvariabler, health check og konfiguration."),
    "predictability": (WORKER_MODEL, "Non-funktionelt krav: Predictability & control. Beskriv plan, diff, approval-flow og hvordan kommandoer eller filændringer kontrolleres."),
    "reproducibility": (WORKER_MODEL, "Non-funktionelt krav: Reproducibility. Beskriv Git-flow, versionering og hvordan samme workflow kan køres igen med sammenlignelige resultater."),
    "context_management": (WORKER_MODEL, "Non-funktionelt krav: Context management. Beskriv artifact handoffs, summaries, scoping og hvordan workflowet håndterer større repositories og dokumenter."),
    "security": (WORKER_MODEL, "Non-funktionelt krav: Security baseline. Beskriv lokal endpoint-sikkerhed, netværksadgang, secrets og hvorfor en offentlig unauthenticated model endpoint ikke er nødvendig."),
}

# Flask-objektet samler webadresserne og starter selve webserveren.
app = Flask(__name__)

# Frontenden ligger her i samme fil for at holde projektet enkelt. Den sender
# brugerens formular til /api/workflow med JavaScript og viser svaret bagefter.
INDEX_HTML = r"""
<!doctype html>
<html lang="da">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Local LLM Workflow</title>
    <style>
        body { max-width: 900px; margin: 40px auto; padding: 0 20px; font: 16px system-ui, sans-serif; color: #18202a; }
        textarea { width: 100%; min-height: 140px; padding: 12px; box-sizing: border-box; font: inherit; }
        button { margin-top: 12px; padding: 10px 18px; cursor: pointer; }
        #result { background: #f1f3f5; padding: 16px; border-radius: 6px; line-height: 1.5; }
        #result pre { background: #20252b; color: #f1f3f5; padding: 12px; overflow-x: auto; }
        #result code { background: #e2e6ea; padding: 2px 4px; }
        #result h3 { margin-bottom: 6px; }
        #result ul, #result ol { padding-left: 24px; }
        #status { min-height: 24px; margin-top: 16px; }
    </style>
</head>
<body>
    <h1>Local Multi-LLM Workflow</h1>
    <p>Skriv hvad systemet skal kunne. Ti specialiserede agenter analyserer derefter kravet parallelt.</p>
    <form id="workflow-form">
        <textarea id="requirement" placeholder="Eksempel: Jeg skal bruge en webshop med login og produkter..."></textarea>
        <label for="mode">Tilstand:</label>
        <select id="mode">
            <option value="analysis">Analyse (kun tekst)</option>
            <option value="agentic">Agentisk (skriv filer + kør tests)</option>
        </select>
        <label for="apply">Anvend ændringer (ellers kun forslag):</label>
        <input type="checkbox" id="apply">
        <label for="format">Vis resultat som:</label>
        <select id="format">
            <option value="readable">Pænt format</option>
            <option value="json">JSON</option>
        </select>
        <button type="submit">Kør workflow</button>
    </form>
    <div id="status"></div>
    <div id="result"></div>
    <script>
        const form = document.getElementById('workflow-form');
        const status = document.getElementById('status');
        const result = document.getElementById('result');
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            status.textContent = 'Arbejder... Det kan tage lidt tid, mens begge modeller svarer.';
            result.textContent = '';
            try {
                const response = await fetch('/api/workflow', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        requirement: document.getElementById('requirement').value,
                        mode: document.getElementById('mode').value,
                        apply: document.getElementById('apply').checked
                    })
                });
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || 'Ukendt fejl');
                status.textContent = 'Færdig';
                if (document.getElementById('format').value === 'json') {
                    result.textContent = JSON.stringify(data, null, 2);
                } else {
                    result.innerHTML = formatResult(data);
                }
            } catch (error) {
                status.textContent = 'Fejl: ' + error.message;
            }
        });

        function formatResult(data) {
            const agents = data.agents.map(agent => `
                <section>
                    <h3>${escapeHtml(agent.name)} (${escapeHtml(agent.model)} · ${escapeHtml(agent.endpoint)})</h3>
                    ${renderMarkdown(agent.result)}
                </section>
            `).join('');
            return `<h2>Krav</h2><p>${escapeHtml(data.requirement)}</p>
                <h2>Agenter (${data.agent_count})</h2>${agents}`;
        }

        // Gør modeltekst med almindelig Markdown læsbar som HTML.
        function renderMarkdown(markdown) {
            let html = escapeHtml(markdown);
            html = html.replace(/^### (.*)$/gm, '<h4>$1</h4>');
            html = html.replace(/^## (.*)$/gm, '<h3>$1</h3>');
            html = html.replace(/^# (.*)$/gm, '<h2>$1</h2>');
            html = html.replace(/^[-*] (.*)$/gm, '<li>$1</li>');
            html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
            html = html.replace(/^\d+\. (.*)$/gm, '<li>$1</li>');
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
            html = html.replace(/\n\n/g, '</p><p>');
            html = html.replace(/\n/g, '<br>');
            return '<p>' + html + '</p>';
        }

        // Modeloutput må escapes, før det sættes ind som HTML.
        function escapeHtml(value) {
            return String(value)
                .replaceAll('&', '&amp;')
                .replaceAll('<', '&lt;')
                .replaceAll('>', '&gt;')
                .replaceAll('"', '&quot;')
                .replaceAll("'", '&#039;');
        }
    </script>
</body>
</html>
"""


# Sender en prompt til en bestemt lokal Ollama-model på en given endpoint.
def ask_ollama(model: str, prompt: str, endpoint: str) -> str:
    # Ollama bruger et JSON-kald til /api/generate. stream=False betyder, at vi
    # venter på hele svaret, før vi sender det videre til næste model.
    request_data = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    request = urllib.request.Request(
        f"{endpoint}/api/generate",
        data=request_data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError(f"Kunne ikke forbinde til Ollama på {endpoint}. Start Ollama, prøv igen, eller øg timeouten i koden.") from error

    # Ollama kan returnere en fejl i et ellers gyldigt HTTP-svar.
    if "error" in result:
        raise RuntimeError(f"Ollama-fejl for {model}: {result['error']}")
    return result["response"]


# Henter listen over modeller, som en given Ollama-server har installeret.
def _installed_models(endpoint: str) -> set[str]:
    # /api/tags indeholder listen over modeller, som Ollama har installeret.
    try:
        with urllib.request.urlopen(f"{endpoint}/api/tags", timeout=10) as response:
            installed = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise RuntimeError(f"Ollama svarer ikke på {endpoint}. Er Ollama startet?") from error
    return {model["name"] for model in installed.get("models", [])}


# Kontrollerer, at de valgte modeller findes på deres respektive endpoints.
def verify_models() -> dict[str, list[str]]:
    # Hver endpoint kontrolleres for den model, dens roller skal bruge. Hvis
    # begge endpoints peger på samme server, kontrolleres serveren kun én gang.
    checks = [
        (ARCHITECT_ENDPOINT, ARCHITECT_MODEL),
        (WORKER_ENDPOINT, WORKER_MODEL),
    ]
    endpoints: dict[str, list[str]] = {}
    for endpoint, model in checks:
        installed_names = _installed_models(endpoint)
        if model not in installed_names:
            raise RuntimeError(f"Modellen {model} er ikke installeret på {endpoint}. Kør `ollama pull MODELNAVN` eller ret miljøvariablerne.")
        if model not in endpoints.setdefault(endpoint, []):
            endpoints[endpoint].append(model)
    return endpoints


# Vælger hvilken lokal endpoint en agent kører mod, ud fra agentens rolle.
def endpoint_for(agent_name: str) -> str:
    if agent_name in ARCHITECT_ROLE_AGENTS:
        return ARCHITECT_ENDPOINT
    return WORKER_ENDPOINT


# Kører de ti agenter parallelt, så en langsom agent ikke blokerer de andre.
def run_workflow(requirement: str) -> dict[str, object]:
    # Begge endpoints kontrolleres én gang, før vi starter de ti agentkald.
    endpoints = verify_models()
    models = sorted({model for endpoint_models in endpoints.values() for model in endpoint_models})
    context = f"Traits (roller og behaviors): {DEFAULT_TRAITS}\nTasks: {DEFAULT_TASKS}\nTone: {DEFAULT_TONE}\nTargets (målgruppe og mål): {DEFAULT_TARGETS}"

    def run_agent(agent_name: str) -> dict[str, str]:
        model, responsibility = AGENTS[agent_name]
        endpoint = endpoint_for(agent_name)
        prompt = f"Du er agenten {agent_name}. {responsibility}\n\nProjektkrav:\n{requirement}\n\nFælles arbejdsramme:\n{context}\n\nReturner et konkret, kort og handlingsorienteret forslag."
        return {
            "name": agent_name,
            "model": model,
            "endpoint": endpoint,
            "result": ask_ollama(model, prompt, endpoint),
        }

    # Vi kører stadig agenterne parallelt, men begrænser antallet af samtidige
    # kald. Lokale Ollama-servere kan ellers løbe tør for RAM eller timeout.
    agent_results = []
    with ThreadPoolExecutor(max_workers=min(MAX_PARALLEL_AGENTS, len(AGENTS))) as executor:
        futures = {executor.submit(run_agent, agent_name): agent_name for agent_name in AGENTS}
        for future in as_completed(futures):
            agent_results.append(future.result())

    # Futures afsluttes i vilkårlig rækkefølge, så resultatet sorteres tilbage
    # til den faste kravrækkefølge, når det vises til brugeren.
    agent_results.sort(key=lambda agent: list(AGENTS).index(agent["name"]))
    return {
        "requirement": requirement,
        "context": {
            "traits": DEFAULT_TRAITS,
            "tasks": DEFAULT_TASKS,
            "tone": DEFAULT_TONE,
            "targets": DEFAULT_TARGETS,
        },
        "models": models,
        "endpoints": endpoints,
        "agent_count": len(agent_results),
        "agents": agent_results,
    }


# ---------------------------------------------------------------------------
# Agentisk udførelseslag: tool calling, fil-operationer og testkørsel.
#
# Analyse-tilstanden (run_workflow) lader hver agent svare med ren tekst. Den
# agentiske tilstand (run_agentic_workflow) lader udvalgte agenter kalde
# værktøjer, så workflowet kan producere rigtige multi-fil-ændringer og selv
# køre tests. Det dækker implementation-, testing- og predictability-kravene,
# som ren tekst ikke kan indfri.
# ---------------------------------------------------------------------------

# Værktøjsskemaer eksponeres for modellerne via Ollama's function-calling. De er
# bevidst små, så små lokale modeller kan følge dem.
TOOL_SCHEMAS: list[dict[str, object]] = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List filer i workspace, eventuelt under en undermappe.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Relativ sti, standard '.'"}},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Læs en UTF-8 tekstfil fra workspace.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Relativ filsti"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Opret eller overskriv en UTF-8 tekstfil i workspace med det fulde indhold.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relativ filsti"},
                    "content": {"type": "string", "description": "Fuldt filindhold"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Kør en tilladt kommando i workspace, fx 'python -m pytest -q'.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string", "description": "Kommando fra allowlisten"}},
                "required": ["command"],
            },
        },
    },
]


# Udfører agenternes værktøjskald inden for et sandkasse-workspace.
class ToolRuntime:
    """Håndhæver workspace-sandkassen og registrerer alle ændringer.

    Filændringer og kommandoer registreres altid, men udføres kun fysisk når
    ``apply`` er sand. Ellers returneres et forslag (plan + diff), så ændringer
    kan gennemgås og godkendes først (predictability & control).
    """

    def __init__(self, root: str, apply: bool = False, max_read_chars: int = 20000) -> None:
        # Root gemmes som en absolut sti, så relative_to() virker på de resolvede filstier.
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.apply = apply
        self.max_read_chars = max_read_chars
        self.changes: list[dict[str, object]] = []
        self.commands: list[dict[str, object]] = []

    # Sikrer at stien bliver inde i workspace, så agenten ikke skriver udenfor.
    def _resolve(self, relative: str) -> Path:
        candidate = (self.root / str(relative)).resolve()
        root = self.root.resolve()
        if candidate != root and root not in candidate.parents:
            raise ValueError(f"Stien '{relative}' ligger uden for workspace og afvises.")
        return candidate

    def list_files(self, path: str = ".") -> str:
        try:
            target = self._resolve(path)
        except ValueError as error:
            return f"Fejl: {error}"
        if not target.exists():
            return f"Fejl: stien '{path}' findes ikke."
        if target.is_file():
            return f"{target.relative_to(self.root).as_posix()} ({target.stat().st_size} bytes)"
        files = sorted(item.relative_to(self.root).as_posix() for item in target.rglob("*") if item.is_file())
        return "\n".join(files) if files else "(ingen filer)"

    def read_file(self, path: str) -> str:
        try:
            target = self._resolve(path)
        except ValueError as error:
            return f"Fejl: {error}"
        if not target.is_file():
            return f"Fejl: filen '{path}' findes ikke."
        content = target.read_text(encoding="utf-8", errors="replace")
        if len(content) > self.max_read_chars:
            content = content[: self.max_read_chars] + "\n[... filen er afkortet ...]"
        return content

    def write_file(self, path: str, content: str) -> str:
        try:
            target = self._resolve(path)
        except ValueError as error:
            return f"Fejl: {error}"
        previous = ""
        if target.is_file():
            previous = target.read_text(encoding="utf-8", errors="replace")
        diff = "".join(
            difflib.unified_diff(
                previous.splitlines(keepends=True),
                str(content).splitlines(keepends=True),
                fromfile=f"a/{path}",
                tofile=f"b/{path}",
            )
        )
        if self.apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(content), encoding="utf-8")
        self.changes.append({"path": target.relative_to(self.root).as_posix(), "written": self.apply, "diff": diff})
        status = "skrevet" if self.apply else "foreslået (ikke skrevet)"
        return f"OK: {path} {status} ({len(str(content))} tegn)."

    def run_command(self, command: str) -> str:
        command = str(command).strip()
        allowed = any(command == prefix or command.startswith(prefix + " ") for prefix in ALLOWED_COMMAND_PREFIXES)
        if not allowed:
            return f"Afvist: '{command}' er ikke på allowlisten. Tilladt: {', '.join(ALLOWED_COMMAND_PREFIXES)}."
        if not self.apply:
            self.commands.append({"command": command, "executed": False, "exit_code": None, "output": ""})
            return f"Planlagt (ikke kørt): {command}. Kør igen med --apply for at udføre."
        try:
            completed = subprocess.run(shlex.split(command), cwd=self.root, capture_output=True, text=True, timeout=300)
        except (OSError, subprocess.SubprocessError) as error:
            return f"Fejl ved kørsel af '{command}': {error}"
        output = (completed.stdout + completed.stderr).strip()
        self.commands.append({"command": command, "executed": True, "exit_code": completed.returncode, "output": output[:4000]})
        return f"exit={completed.returncode}\n{output[:4000]}"

    # Sender et værktøjskald videre til den rigtige metode ud fra værktøjets navn.
    def dispatch(self, name: str, arguments: dict[str, object]) -> str:
        try:
            if name == "list_files":
                return self.list_files(str(arguments.get("path", ".")))
            if name == "read_file":
                return self.read_file(str(arguments.get("path", "")))
            if name == "write_file":
                return self.write_file(str(arguments.get("path", "")), str(arguments.get("content", "")))
            if name == "run_command":
                return self.run_command(str(arguments.get("command", "")))
        except (KeyError, TypeError) as error:
            return f"Fejl: kunne ikke udføre værktøjet '{name}': {error}"
        return f"Ukendt værktøj: {name}"


# Sender en samtale til Ollama's /api/chat og returnerer assistent-beskeden.
def chat_ollama(model: str, messages: list[dict[str, object]], tools: list[dict[str, object]], endpoint: str, timeout: int = 300) -> dict[str, object]:
    payload: dict[str, object] = {"model": model, "messages": messages, "stream": False}
    if tools:
        payload["tools"] = tools
    request = urllib.request.Request(
        f"{endpoint}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError(f"Kunne ikke forbinde til Ollama på {endpoint}. Start Ollama og prøv igen.") from error
    if "error" in result:
        raise RuntimeError(f"Ollama-fejl for {model}: {result['error']}")
    return cast(dict[str, object], result.get("message", {}))


# Ollama giver værktøjsargumenter som dict; andre backends sender en JSON-streng.
def _tool_call_arguments(call: dict[str, object]) -> dict[str, object]:
    function = call.get("function")
    if not isinstance(function, dict):
        return {}
    arguments = function.get("arguments", {})
    if isinstance(arguments, str):
        try:
            parsed = json.loads(arguments)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return arguments if isinstance(arguments, dict) else {}


# Navnene på de værktøjer, som fallback-parseren må genkende i modeltekst.
KNOWN_TOOL_NAMES = {str(schema["function"]["name"]) for schema in TOOL_SCHEMAS}  # type: ignore[index]


# Normaliserer et løst JSON-objekt til formen {"function": {"name": ..., "arguments": ...}}.
def _normalise_tool_call(item: object) -> dict[str, object] | None:
    if not isinstance(item, dict):
        return None
    function = item.get("function")
    name = item.get("name") or item.get("tool")
    arguments = item.get("arguments") or item.get("parameters") or item.get("input")
    if isinstance(function, dict):
        name = name or function.get("name")
        arguments = arguments or function.get("arguments")
    if not isinstance(name, str) or name not in KNOWN_TOOL_NAMES:
        return None
    return {"function": {"name": name, "arguments": arguments if isinstance(arguments, dict) else {}}}


# Redder værktøjskald, som en model har skrevet som JSON-tekst i stedet for i
# Ollama's strukturerede tool_calls-felt. Det gør små lokale modeller brugbare.
def _extract_tool_calls_from_content(content: str) -> list[dict[str, object]]:
    text = (content or "").strip()
    if not text:
        return []
    text = re.sub(r"```[a-zA-Z]*", "", text).replace("```", "")
    candidates = [text]
    depth = 0
    start = -1
    for index, char in enumerate(text):
        if char == "{":
            if depth == 0:
                start = index
            depth += 1
        elif char == "}" and depth > 0:
            depth -= 1
            if depth == 0 and start != -1:
                candidates.append(text[start : index + 1])
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        calls = []
        for item in parsed if isinstance(parsed, list) else [parsed]:
            call = _normalise_tool_call(item)
            if call is not None:
                calls.append(call)
        if calls:
            return calls
    return []


# Lader en agent kalde værktøjer i en løkke, indtil den svarer uden værktøjskald.
def run_tool_agent(
    agent_name: str,
    model: str,
    endpoint: str,
    system_prompt: str,
    user_prompt: str,
    runtime: ToolRuntime,
    max_rounds: int = MAX_AGENT_ROUNDS,
) -> dict[str, object]:
    messages: list[dict[str, object]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    transcript: list[dict[str, object]] = []
    rounds = 0
    content = ""
    while rounds < max_rounds:
        rounds += 1
        message = chat_ollama(model, messages, TOOL_SCHEMAS, endpoint)
        messages.append(message)
        content = str(message.get("content", "") or "")
        tool_calls = message.get("tool_calls") or []
        if not isinstance(tool_calls, list) or not tool_calls:
            # Nogle lokale modeller lægger kaldet i teksten i stedet for i det
            # strukturerede felt. Vi redder dem ud, så workflowet stadig virker.
            tool_calls = _extract_tool_calls_from_content(content)
        if not tool_calls:
            break
        for call in tool_calls:
            if not isinstance(call, dict):
                continue
            function = call.get("function", {})
            name = str(function.get("name", "")) if isinstance(function, dict) else ""
            arguments = _tool_call_arguments(call)
            result = runtime.dispatch(name, arguments)
            transcript.append({"tool": name, "arguments": arguments, "result": result[:400]})
            messages.append({"role": "tool", "content": result})
    return {"name": agent_name, "model": model, "endpoint": endpoint, "rounds": rounds, "result": content, "tools": transcript}


# Afkorter tekst til et kontekstbudget og markerer, at der er udeladt noget.
def _bounded(text: str, limit: int) -> tuple[str, bool]:
    text = text or ""
    if limit <= 0 or len(text) <= limit:
        return text, False
    return text[:limit] + f"\n[... afkortet: {len(text) - limit} tegn udeladt ...]", True


# Rækkefølgen de funktionelle agenter kører i. Hvert trin får de tidligere
# artefakter som eksplicit kontekst (artifact handoff).
AGENTIC_STAGES = ["architecture", "tech_lead", "implementation", "testing_quality", "documentation", "deployment"]
# De fire non-funktionelle reviews kører parallelt til sidst med alle artefakter.
AGENTIC_REVIEWS = ["predictability", "reproducibility", "context_management", "security"]
# Disse agenter må kalde værktøjer (skrive filer, køre kommandoer).
TOOL_AGENTS = {"implementation", "testing_quality", "documentation", "deployment"}

TOOL_SYSTEM_PROMPT = (
    "Du er en softwareudviklingsagent med adgang til værktøjer i et sandkasse-workspace. "
    "Brug write_file til at oprette eller opdatere filer, read_file og list_files til at "
    "undersøge koden, og run_command til at køre tilladte kommandoer som 'python -m pytest -q'. "
    "Skriv komplette, kørbare filer. Afslut med en kort opsummering af, hvad du ændrede."
)


# Giver de tidligere artefakter videre som afgrænset kontekst og logger handoffet.
def _handoff_context(artifacts: dict[str, str], budget: int, handoffs: list[dict[str, object]], target: str) -> str:
    if not artifacts:
        return "(ingen tidligere artefakter)"
    blocks = []
    for name, text in artifacts.items():
        bounded, truncated = _bounded(text, budget)
        handoffs.append({"from": name, "to": target, "chars": len(bounded), "truncated": truncated})
        blocks.append(f"### {name}\n{bounded}")
    return "\n\n".join(blocks)


# Kører den agentiske pipeline: funktionelle trin i rækkefølge med artefakt-
# handoff, derefter de fire non-funktionelle reviews parallelt.
def run_agentic_workflow(
    requirement: str,
    *,
    apply: bool = False,
    workspace_dir: str | None = None,
    context_budget: int | None = None,
    max_rounds: int | None = None,
) -> dict[str, object]:
    endpoints = verify_models()
    models = sorted({model for endpoint_models in endpoints.values() for model in endpoint_models})
    workspace = workspace_dir or WORKSPACE_DIR
    budget = CONTEXT_BUDGET if context_budget is None else context_budget
    rounds_limit = MAX_AGENT_ROUNDS if max_rounds is None else max_rounds
    runtime = ToolRuntime(workspace, apply=apply)
    context = f"Traits (roller og behaviors): {DEFAULT_TRAITS}\nTasks: {DEFAULT_TASKS}\nTone: {DEFAULT_TONE}\nTargets (målgruppe og mål): {DEFAULT_TARGETS}"
    artifacts: dict[str, str] = {}
    handoffs: list[dict[str, object]] = []
    agent_results: list[dict[str, object]] = []

    # Funktionelle trin kører sekventielt, så hvert trin kan bygge på de forrige.
    for stage in AGENTIC_STAGES:
        model, responsibility = AGENTS[stage]
        endpoint = endpoint_for(stage)
        prior = _handoff_context(artifacts, budget, handoffs, stage)
        user_prompt = f"Projektkrav:\n{requirement}\n\nFælles arbejdsramme:\n{context}\n\nTidligere artefakter:\n{prior}\n\nDin opgave: {responsibility}"
        if stage in TOOL_AGENTS:
            agent_result = run_tool_agent(stage, model, endpoint, TOOL_SYSTEM_PROMPT, user_prompt, runtime, rounds_limit)
        else:
            agent_result = {"name": stage, "model": model, "endpoint": endpoint, "rounds": 1, "result": ask_ollama(model, user_prompt, endpoint), "tools": []}
        artifacts[stage] = str(agent_result["result"])
        agent_results.append(agent_result)

    # Non-funktionelle reviews får hele artefakt-sættet og kører parallelt.
    def run_review(agent_name: str) -> dict[str, object]:
        model, responsibility = AGENTS[agent_name]
        endpoint = endpoint_for(agent_name)
        prior = _handoff_context(artifacts, budget, handoffs, agent_name)
        prompt = f"Projektkrav:\n{requirement}\n\nFælles arbejdsramme:\n{context}\n\nProducerede artefakter:\n{prior}\n\nDin opgave: {responsibility}"
        return {"name": agent_name, "model": model, "endpoint": endpoint, "rounds": 1, "result": ask_ollama(model, prompt, endpoint), "tools": []}

    with ThreadPoolExecutor(max_workers=min(MAX_PARALLEL_AGENTS, len(AGENTIC_REVIEWS))) as executor:
        futures = {executor.submit(run_review, agent_name): agent_name for agent_name in AGENTIC_REVIEWS}
        for future in as_completed(futures):
            agent_results.append(future.result())

    order = AGENTIC_STAGES + AGENTIC_REVIEWS
    agent_results.sort(key=lambda agent: order.index(cast(str, agent["name"])))
    return {
        "requirement": requirement,
        "mode": "agentic",
        "applied": apply,
        "workspace": str(runtime.root),
        "context_budget": budget,
        "context": {
            "traits": DEFAULT_TRAITS,
            "tasks": DEFAULT_TASKS,
            "tone": DEFAULT_TONE,
            "targets": DEFAULT_TARGETS,
        },
        "models": models,
        "endpoints": endpoints,
        "agent_count": len(agent_results),
        "agents": agent_results,
        "artifacts": artifacts,
        "changes": runtime.changes,
        "commands": runtime.commands,
        "handoffs": handoffs,
    }


def print_readable_result(result: dict[str, object]) -> None:
    """Printer workflow-resultatet i en form, der er nem at læse i terminalen."""
    print(f"KRAV\n{result['requirement']}")
    if result.get("mode"):
        print(f"\nTILSTAND: {result['mode']} (anvendt: {result.get('applied')}, workspace: {result.get('workspace')})")
    print(f"\nAGENTER ({result['agent_count']})")
    agents = cast(list[dict[str, str]], result["agents"])
    for agent in agents:
        print(f"\n--- {agent['name']} ({agent['model']} @ {agent['endpoint']}) ---\n{agent['result']}")
    changes = cast(list[dict[str, object]], result.get("changes") or [])
    if changes:
        print(f"\nFILÆNDRINGER ({len(changes)})")
        for change in changes:
            print(f"\n--- {change['path']} (skrevet: {change['written']}) ---\n{change['diff']}")
    commands = cast(list[dict[str, object]], result.get("commands") or [])
    if commands:
        print(f"\nKOMMANDOER ({len(commands)})")
        for command in commands:
            print(f"- {command['command']} -> udført: {command['executed']}, exit: {command['exit_code']}")


# Viser frontend-siden i browseren.
@app.get("/")
def index():
    # Flask sender HTML-siden til browseren, når brugeren åbner forsiden.
    return render_template_string(INDEX_HTML)


# Giver status på Ollama og de valgte modeller.
@app.get("/api/health")
def health():
    # Dette endpoint kan bruges til hurtigt at se, om Ollama er tilgængelig.
    try:
        endpoints = verify_models()
    except RuntimeError as error:
        return jsonify({"status": "error", "error": str(error)}), 503
    models = sorted({model for endpoint_models in endpoints.values() for model in endpoint_models})
    return jsonify({"status": "ok", "endpoints": endpoints, "models": models})


# Modtager brugerens krav fra frontend og starter workflowet.
@app.post("/api/workflow")
def workflow_api():
    # Frontenden sender projektkravet og (valgfrit) tilstand. Traits, Tasks,
    # Tone og Targets er prædefineret i Python-filen og ændres der, hvis gruppen
    # ønsker det.
    data = request.get_json(silent=True) or {}
    requirement = str(data.get("requirement", "")).strip()
    if not requirement:
        return jsonify({"error": "Feltet requirement må ikke være tomt."}), 400

    # mode="agentic" lader agenterne skrive filer og køre tests. apply styrer,
    # om ændringerne faktisk gennemføres eller kun foreslås til godkendelse.
    mode = str(data.get("mode", "analysis"))
    try:
        if mode == "agentic":
            return jsonify(run_agentic_workflow(requirement, apply=bool(data.get("apply", False))))
        return jsonify(run_workflow(requirement))
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503


# Flag der kan sættes på kommandolinjen. Flag med en værdi står i VALUE_FLAGS.
BOOLEAN_FLAGS = {"--web", "--json", "--agentic", "--apply"}
VALUE_FLAGS = {"--workspace"}


# Deler kommandolinjen op i flag, flag-værdier og selve kravet.
def _parse_arguments(arguments: list[str]) -> tuple[set[str], dict[str, str], str]:
    flags: set[str] = set()
    values: dict[str, str] = {}
    requirement_parts: list[str] = []
    index = 0
    while index < len(arguments):
        token = arguments[index]
        if token in BOOLEAN_FLAGS:
            flags.add(token)
        elif token in VALUE_FLAGS and index + 1 < len(arguments):
            values[token] = arguments[index + 1]
            index += 1
        else:
            requirement_parts.append(token)
        index += 1
    return flags, values, " ".join(requirement_parts).strip()


# Starter enten Flask-websiden eller workflowet fra terminalen.
def main() -> int:
    flags, values, requirement = _parse_arguments(sys.argv[1:])

    # --web bruges, når programmet skal fungere som Flask-server.
    if "--web" in flags:
        app.run(host="127.0.0.1", port=5000, debug=False)
        return 0

    # Uden --web køres programmet fra terminalen. --agentic vælger den agentiske
    # tilstand, og --apply afgør, om ændringer gennemføres eller kun foreslås.
    if not requirement:
        requirement = input("Hvad skal systemet kunne?\n> ").strip()
    if not requirement:
        print("Du skal skrive et behov.", file=sys.stderr)
        return 1

    # Workflowet kan både læse et krav fra kommandolinjen og spørge brugeren.
    try:
        if "--agentic" in flags:
            result = run_agentic_workflow(requirement, apply="--apply" in flags, workspace_dir=values.get("--workspace"))
        else:
            result = run_workflow(requirement)
    except RuntimeError as error:
        print(f"Fejl: {error}", file=sys.stderr)
        return 1

    # JSON-filen gemmes altid, så resultatet kan bruges af andre værktøjer.
    output_path = "output/workflow-result.json"
    os.makedirs("output", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=2, ensure_ascii=False)
    print(f"Færdig. Resultatet er gemt i {output_path}")
    if "--json" in flags:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_readable_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
