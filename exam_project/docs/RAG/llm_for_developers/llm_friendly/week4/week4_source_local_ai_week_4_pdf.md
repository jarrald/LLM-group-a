<!-- studygraph:converted-source:v1 -->
# Uge 4 — Local AI week 4 (pdf)

Kilde: [week4/Local AI week 4.pdf](../../source/week4/Local%20AI%20week%204.pdf).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Side 1

august 2026

Week 4

Local LLM APIs in code (Ollama + OpenWebUI)
Openwebui interface and models 
ComfyUI install
Connect Ollama and OpenWEBUI

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 2

What “connect to the API” means

• Reach the service on localhost (correct port).
• List available models (sanity check).
• Send a chat request and read the answer from 
the response JSON.

Local base URLs

Ollama:    http://localhost:11434
OpenWebUI: http://localhost:3000

Sanity checks

Ollama models:    GET
http://localhost:11434/api/tags
OpenWebUI models: GET
http://localhost:3000/api/models

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 3

Ollama API — list models (sanity check)

HTTP request

Method: GET
URL:    http://localhost:11434/api/tags
Headers: (none)
Body:    (none)

Good response

HTTP 200 + JSON containing a “models” array.
Copy the model name exactly (including any :tag).

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 4

Ollama API — chat (prompt → answer)

HTTP request

Method: POST
URL:    http://localhost:11434/api/chat
Headers:
  Content-Type: application/json
Body (JSON):
{
  "model": "gemma3",
  "messages": [
    {"role": "user", "content": "Give 3 bullet tips for clean 
code."}
  ],
  "stream": false
}

Read the answer here

HTTP 200 JSON:
{
  "message": {
    "role": "assistant",
    "content": "..."
  },
  "done": true
}

Use: message.content

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 5

Ollama API — common failure modes

• Connection refused → Ollama not running or wrong port (11434).
• HTTP 404 → wrong endpoint path (use /api/chat or /api/tags).
• Model not found → copy model name exactly from /api/tags.
• Timeouts → increase client timeout for slow hardware / large models.
• Streaming confusion → set "stream": false to get one JSON response.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 6

Configure OpenWebUI

Models

• Check that the local model backend is connected.
• Make the model visible in OpenWebUI.
• Copy model names exactly when using APIs later.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 7

4T’s in OpenWebUI

Use the same prompting structure from prompt engineering when configuring model behavior.

Traits
Task
Tone
Target

The point is not only to run a model, but to make it answer in a controlled and useful

way.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 8

OpenWebUI API — authentication (API key)

• OpenWebUI typically requires an API key (Bearer token).
• Generate an API key in the OpenWebUI UI settings and treat it as a secret.

List models (sanity check)

Method: GET
URL:    http://localhost:3000/api/models
Headers:
  Authorization: Bearer <YOUR_OPENWEBUI_API_KEY>
  Content-Type: application/json
Body: (none)

Good response: HTTP 200 + JSON list of models.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 9

OpenWebUI API — chat (OpenAI-compatible shape)

HTTP request

Method: POST
URL:    http://localhost:3000/api/chat/completions
Headers:
  Authorization: Bearer <YOUR_OPENWEBUI_API_KEY>
  Content-Type: application/json
Body (JSON):
{
  "model": "llama3.1",
  "messages": [
    {"role": "user", "content": "Explain REST APIs in 3 sentences."}
  ]
}

Read the answer here

HTTP 200 JSON:
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "..."
      }
    }
  ]
}

Use: choices[0].message.content

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 10

OpenWebUI API — common failure modes

• HTTP 401/403 → missing/invalid Authorization header (Bearer token).
• HTTP 404 → wrong URL (use /api/models or /api/chat/completions).
• Model not available → copy model name exactly from /api/models.
• Timeouts / slow responses → increase timeout; try smaller model.
• Empty output → read choices[0].message.content.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 11

Quick troubleshooting (diagnose by HTTP result)

If you see … do this

Connection refused
  → service not running OR wrong port

HTTP 404
  → endpoint path wrong

HTTP 401/403 (OpenWebUI)
  → missing/invalid Bearer token

HTTP 400
  → JSON invalid OR wrong field names

Timeout
  → increase client timeout; try a smaller model; set stream:false for Ollama

HTTP 500
  → server error; retry; inspect server logs; try a simpler prompt/model

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 12

AI Models

Models, setup and local tooling

• Local model runtime
• OpenWebUI
• ComfyUI
• Model choice and configuration

Goal: get the local AI stack running and understand where models fit.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 13

Setup

• ComfyUI
   – Install ComfyUI from GitHub.
   – Use it as the local image-generation backend.
   – Connect it later through OpenWebUI.

Reference

https://github.com/comfyanonymous/ComfyUI

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 14

Configure OpenWebUI to use ComfyUI

• OpenWebUI acts as the user interface.
• ComfyUI acts as the image-generation backend.
• Configuration connects the two so students can test image workflows from one 
place.

OpenWebUI  →  ComfyUI

UI/chat layer → image workflow backend

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 15

Rest of today: workshop on your mandatory 
assignment

THE END ;)

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.
