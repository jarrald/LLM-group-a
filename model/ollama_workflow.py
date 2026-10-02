"""Run ten specialized agents against local Ollama model backends."""

import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
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
                    body: JSON.stringify({requirement: document.getElementById('requirement').value})
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


def print_readable_result(result: dict[str, object]) -> None:
    """Printer workflow-resultatet i en form, der er nem at læse i terminalen."""
    print(f"KRAV\n{result['requirement']}")
    print(f"\nAGENTER ({result['agent_count']})")
    agents = cast(list[dict[str, str]], result["agents"])
    for agent in agents:
        print(f"\n--- {agent['name']} ({agent['model']} @ {agent['endpoint']}) ---\n{agent['result']}")


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
    # Frontenden sender kun projektkravet. Traits, Tasks, Tone og Targets er
    # prædefineret i Python-filen og ændres der, hvis gruppen ønsker det.
    data = request.get_json(silent=True) or {}
    requirement = str(data.get("requirement", "")).strip()
    if not requirement:
        return jsonify({"error": "Feltet requirement må ikke være tomt."}), 400

    try:
        return jsonify(run_workflow(requirement))
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503


# Starter enten Flask-websiden eller workflowet fra terminalen.
def main() -> int:
    # --web bruges, når programmet skal fungere som Flask-server.
    if "--web" in sys.argv:
        app.run(host="127.0.0.1", port=5000, debug=False)
        return 0

    # Uden --web køres programmet fra terminalen. --json vælger rå JSON-output;
    # ellers vises resultatet i et mere læsbart format.
    json_output = "--json" in sys.argv
    arguments = [argument for argument in sys.argv[1:] if argument != "--json"]
    requirement = " ".join(arguments).strip()
    if not requirement:
        requirement = input("Hvad skal systemet kunne?\n> ").strip()
    if not requirement:
        print("Du skal skrive et behov.", file=sys.stderr)
        return 1

    # Workflowet kan både læse et krav fra kommandolinjen og spørge brugeren.
    try:
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
    if json_output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_readable_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
