<!-- studygraph:converted-source:v1 -->
# Uge 6 — app (py)

Kilde: [week6/openwebui_demo/app.py](../../source/week6/openwebui_demo/app.py).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

### Kildelinjer 1–45

```python
import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import requests

load_dotenv()

OPENWEBUI_BASE_URL = os.getenv("OPENWEBUI_BASE_URL", "http://localhost:3000").rstrip("/")
OPENWEBUI_API_KEY = os.getenv("OPENWEBUI_API_KEY")
OPENWEBUI_MODEL = os.getenv("OPENWEBUI_MODEL", "my-model-enterprice-architect")
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "Use attached knowledge when relevant. If the answer is not in the knowledge, say so clearly.",
)
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", model_name=OPENWEBUI_MODEL)


@app.post("/chat")
def chat():
    try:
        body = request.get_json(silent=True) or {}
        user_message = (body.get("message") or "").strip()

        if not user_message:
            return jsonify({"error": "Message is required."}), 400

        if not OPENWEBUI_API_KEY:
            return jsonify({"error": "OPENWEBUI_API_KEY is missing in .env"}), 500

        payload = {
            "model": OPENWEBUI_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.2,
            "stream": False,
        }
```

### Kildelinjer 46–90

```python

        headers = {
            "Authorization": f"Bearer {OPENWEBUI_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{OPENWEBUI_BASE_URL}/api/chat/completions",
            headers=headers,
            json=payload,
            timeout=600,
        )

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        response.raise_for_status()
        data = response.json()

        answer = None

        choices = data.get("choices") or []
        if choices:
            answer = (choices[0].get("message") or {}).get("content")

        if answer is None and isinstance(data.get("message"), dict):
            answer = data["message"].get("content")

        if answer is None and isinstance(data.get("response"), str):
            answer = data.get("response")

        if answer is None:
            return jsonify({
                "error": "Unexpected OpenWebUI response format",
                "raw": data,
            }), 502

        return jsonify({"answer": answer, "raw": data})

    except requests.HTTPError as exc:
        body = exc.response.text if exc.response is not None else str(exc)
        return jsonify({"error": "OpenWebUI request failed", "details": body}), 502
    except Exception as exc:
        app.logger.exception("Chat handler failed")
        return jsonify({"error": "Unexpected backend error", "details": str(exc)}), 500
```

### Kildelinjer 91–94

```python


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=FLASK_DEBUG)
```
