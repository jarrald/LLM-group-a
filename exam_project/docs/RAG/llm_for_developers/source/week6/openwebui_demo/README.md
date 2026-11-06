# Week 10 - Tiny website using OpenWebUI API

This demo shows a tiny frontend calling your backend, and the backend calling OpenWebUI.

## Goal
Use a custom website frontend while OpenWebUI handles the model call and any attached Knowledge.

Architecture:

```text
frontend -> Flask backend -> OpenWebUI API -> model + attached Knowledge
```

## What students should already have
- OpenWebUI running
- A model available in OpenWebUI
- A personal API key from OpenWebUI
- Optional but recommended: a Knowledge collection attached to the model in OpenWebUI

## Files
- `app.py` - tiny Flask backend
- `templates/index.html` - tiny frontend page
- `static/app.js` - browser-side request code
- `.env.example` - configuration template
- `requirements.txt` - Python packages

## Setup
### 1. Create and activate a Python environment
```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env`
Copy `.env.example` to `.env` and update the values.

Required values:
- `OPENWEBUI_BASE_URL`
- `OPENWEBUI_API_KEY`
- `OPENWEBUI_MODEL`

Example:

```text
OPENWEBUI_BASE_URL=http://localhost:3000
OPENWEBUI_API_KEY=your_api_key_here
OPENWEBUI_MODEL=my-model
SYSTEM_PROMPT=Use attached knowledge when relevant. If the answer is not in the knowledge, say so clearly.
```

### 4. Run the backend
```bash
python app.py
```

### 5. Open the website
Open:
- `http://127.0.0.1:5000`

## Demo flow for class
1. Ask a normal question
2. Ask a question that should rely on the attached Knowledge
3. Explain that the browser is not calling OpenWebUI directly
4. Show that the token stays in the backend

## Important note about behavior
The most useful classroom assumption is:
- attach Knowledge to a model in the OpenWebUI UI
- call that model through the API
- get knowledge-backed behavior

But the exact behavior depends on mode:
- in default mode, OpenWebUI can auto-inject relevant knowledge
- in native function-calling mode, the model must actively use knowledge tools

For this classroom demo, default mode is the safer choice.
