# Week 4 — Local LLM APIs and OpenWebUI

Source: `source/week4/Local AI week 4.pdf`, 15 pages. The full text is in the [source conversion](week4_source_local_ai_week_4_pdf.md). This is a reading guide to the material, not a new installation guide with verified API versions.

## From a local model to an API call

The lecture distinguishes between reaching the local service, checking model names and sending a chat request. In the examples Ollama uses port 11434, while OpenWebUI uses port 3000. A model name must be copied with its exact tag from the service's model list.

In the Ollama examples `GET /api/tags` reads the model list, while `POST /api/chat` receives `model`, `messages` and `stream`. With `stream: false` the answer is read from `message.content` in a single JSON response. Streaming changes how the client must read the response.

## OpenWebUI and the four T's

OpenWebUI exposes the models through its own interface and can configure model behaviour with Traits, Task, Tone and Target. The API examples use Bearer authentication. The model list is at `/api/models`, and the chat example uses `/api/chat/completions`. They are examples from the lecture and must be kept separate from Ollama's own endpoints.

An API key must be kept out of shared notes and Git. The uploaded `.env` files are therefore neither converted nor indexed.

## Troubleshooting by HTTP result

| Symptom in the material | Check |
|---|---|
| Connection refused | Is the right service running on the right port? |
| HTTP 404 | Is the endpoint path correct? |
| HTTP 401/403 | Is the OpenWebUI token present and valid? |
| HTTP 400 | Are the JSON and field names correct? |
| Timeout | Try a smaller model, a longer timeout or a non-streamed response. |
| HTTP 500 | Investigate the server error and try a simpler request. |

## ComfyUI and workshop

The slides introduce ComfyUI as a local backend for image generation and OpenWebUI as an interface that can be connected to it. The rest of the day is reserved for a workshop on the mandatory assignment. The slides do not document that any particular installation was carried out.

## Review questions

1. Why is the model list checked before a chat request?
2. What does `stream: false` change for the client's handling of the response?
3. How do the Ollama and OpenWebUI endpoints differ?
4. What do 404 and 401 respectively tell you about the error?
5. What role does OpenWebUI play relative to ComfyUI?