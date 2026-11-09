<!-- studygraph:converted-source:v1 -->
# Uge 6 — style (css)

Kilde: [week6/style.css](../../source/week6/style.css).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

### Kildelinjer 1–45

```python
import os
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, render_template, request

from rag_helpers import CHAT_MODEL, answer_question

TOP_K = int(os.getenv("TOP_K", "4"))
PORT = int(os.getenv("PORT", "5000"))

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", default_model=CHAT_MODEL)


@app.get("/health")
def health() -> Any:
    return jsonify({"status": "ok"})


def get_last_user_message(messages: List[Dict[str, Any]]) -> Optional[str]:
    for message in reversed(messages):
        if message.get("role") == "user":
            content = str(message.get("content", "")).strip()
            if content:
                return content
    return None


@app.post("/api/chat")
def api_chat() -> Any:
    payload = request.get_json(silent=True) or {}
    messages = payload.get("messages") or []
    question = str(payload.get("question", "")).strip() or get_last_user_message(messages)
    model = str(payload.get("model", "")).strip() or CHAT_MODEL

    if not question:
        return jsonify({"error": "Missing question or user message."}), 400

    result = answer_question(question, top_k=TOP_K, model=model)

    return jsonify(
```

### Kildelinjer 46–61

```python
        {
            "model": model,
            "message": {
                "role": "assistant",
                "content": result["answer"],
            },
            "done": True,
            "citations": result["citations"],
            "grounded": result["grounded"],
            "no_answer": result["no_answer"],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
```
