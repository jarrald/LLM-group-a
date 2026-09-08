"""Run a small two-model workflow against a local Ollama server."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
ARCHITECT_MODEL = os.getenv("ARCHITECT_MODEL", "qwen2.5-coder:7b")
REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "llama3.2:3b")

app = Flask(__name__)

INDEX_HTML = """
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
        pre { white-space: pre-wrap; background: #f1f3f5; padding: 16px; border-radius: 6px; }
        #status { min-height: 24px; margin-top: 16px; }
    </style>
</head>
<body>
    <h1>Local Multi-LLM Workflow</h1>
    <p>Skriv hvad systemet skal kunne. Ollama-modellerne laver derefter en arkitekturplan og et review.</p>
    <form id="workflow-form">
        <textarea id="requirement" placeholder="Eksempel: Jeg skal bruge en webshop med login og produkter..."></textarea>
        <button type="submit">Kør workflow</button>
    </form>
    <div id="status"></div>
    <pre id="result"></pre>
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
                result.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                status.textContent = 'Fejl: ' + error.message;
            }
        });
    </script>
</body>
</html>
"""


def ask_ollama(model: str, prompt: str) -> str:
    request_data = json.dumps(
        {"model": model, "prompt": prompt, "stream": False}
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=request_data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Kunne ikke forbinde til Ollama på {OLLAMA_URL}. "
            "Start Ollama og prøv igen."
        ) from error

    if "error" in result:
        raise RuntimeError(f"Ollama-fejl for {model}: {result['error']}")
    return result["response"]


def verify_models() -> list[str]:
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=10) as response:
            installed = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Ollama svarer ikke på {OLLAMA_URL}. Er Ollama startet?"
        ) from error

    installed_names = {model["name"] for model in installed.get("models", [])}
    missing = [
        model
        for model in (ARCHITECT_MODEL, REVIEWER_MODEL)
        if model not in installed_names
    ]
    if missing:
        raise RuntimeError(
            "Disse modeller er ikke installeret i Ollama: "
            + ", ".join(missing)
            + ". Kør `ollama pull MODELNAVN` eller ret miljøvariablerne."
        )
    return [ARCHITECT_MODEL, REVIEWER_MODEL]


def run_workflow(requirement: str) -> dict[str, str | list[str]]:
    models = verify_models()
    architecture = ask_ollama(
        ARCHITECT_MODEL,
        """Du er softwarearkitekt. Lav en kort, konkret plan for følgende behov.
Returner præcis disse overskrifter: Components, API, Tasks, Acceptance criteria.
Behov:
"""
        + requirement,
    )
    review = ask_ollama(
        REVIEWER_MODEL,
        """Du er tech lead og reviewer. Gennemgå behovet og arkitekturplanen.
Find mangler, foreslå tests og lav en kort deployment-checkliste.
Behov:
"""
        + requirement
        + "\nArkitekturplan:\n"
        + architecture,
    )
    return {
        "requirement": requirement,
        "models": models,
        "architecture": architecture,
        "review_and_tests": review,
    }


@app.get("/")
def index():
    return render_template_string(INDEX_HTML)


@app.get("/api/health")
def health():
    try:
        models = verify_models()
    except RuntimeError as error:
        return jsonify({"status": "error", "error": str(error)}), 503
    return jsonify({"status": "ok", "models": models})


@app.post("/api/workflow")
def workflow_api():
    data = request.get_json(silent=True) or {}
    requirement = str(data.get("requirement", "")).strip()
    if not requirement:
        return jsonify({"error": "Feltet requirement må ikke være tomt."}), 400

    try:
        return jsonify(run_workflow(requirement))
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503


def main() -> int:
    parser = argparse.ArgumentParser(description="Kør workflowet med to lokale Ollama-modeller.")
    parser.add_argument("requirement", nargs="?", help="Det behov, der skal analyseres")
    parser.add_argument("--output", default="output/workflow-result.json")
    parser.add_argument("--web", action="store_true", help="Start Flask-webserveren")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    if args.web:
        app.run(host=args.host, port=args.port, debug=False)
        return 0

    requirement = args.requirement or input("Hvad skal systemet kunne?\n> ").strip()
    if not requirement:
        print("Du skal skrive et behov.", file=sys.stderr)
        return 1

    try:
        result = run_workflow(requirement)
    except RuntimeError as error:
        print(f"Fejl: {error}", file=sys.stderr)
        return 1

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Færdig. Resultatet er gemt i {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())