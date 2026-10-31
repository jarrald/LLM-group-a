<!-- studygraph:converted-source:v1 -->
# Uge 6 — local_rag (pdf)

Kilde: [week6/local_rag.pdf](../../source/week6/local_rag.pdf).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Side 1

Local RAG in practice

Documents → retrieval → grounded answer → application

LLM for Developers

Goal: run, understand, and modify working local RAG packages.

Pipeline

PDF / TXT / MD

↓

chunks + embeddings

↓

Chroma retrieval

↓

answer from context

1

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 2

Three packages — one problem

All three packages answer questions from documents. The difference is where the responsibility is placed.

LLM for Developers

Package
Interface
Retrieval owner
Model access

1 · Custom RAG CLI
Terminal
Our Python code + Chroma
Ollama

2 · Custom RAG Web
Browser + Flask
Same Python RAG core + Chroma
Ollama

3 · OpenWebUI 
Knowledge Web
Browser + backend
OpenWebUI Knowledge
OpenWebUI 
 model
→

Same user goal: ask questions about your documents and get grounded answers.
Different implementation choice: how much of the RAG pipeline your application owns.

2

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 3

Package structure and responsibilities

Use this overview when you move between the three supplied folders.

LLM for Developers

Package 1 — CLI

docs/
ingest.py
chunking.py
rag_helpers.py
ask.py

Owns:
• document loading
• chunking
• embeddings
• retrieval
• model call

Package 2 — Web

Same RAG core
app.py
templates/index.html
static/app.js
static/style.css

Adds:
• browser UI
• Flask API
• JSON request/response

Package 3 — OpenWebUI

app.py
templates/index.html
static/app.js
.env
OpenWebUI Knowledge

Moves to OpenWebUI:
• ingestion
• retrieval
• model selection

3

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 4

What RAG actually is

LLM for Developers

• RAG is not a special model.
• It is a workflow around a model.
• Relevant chunks are retrieved first.
• The answer is generated after that context is 
added.

documents
chunks
embeddings

top-k retrieval
answer

Key idea
The retrieval step decides what context the model sees.

4

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 5

Grounding rules

LLM for Developers

• Answer only from the retrieved context.
• If the answer is not in the context, say: I don’t 
know.
• Show simple references like [1] and [2].
• Good retrieval matters more than confident 
wording.

Expected answer pattern

Question
What file types are supported?

Retrieved chunks
[1] ... PDF, TXT, MD ...
[2] ... supported input types ...

Answer
The starter supports PDF, TXT, and MD. [1] [2]

Also test
Ask something missing and confirm that the answer becomes “I don’t know.”

5

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 6

Live setup and first run

Follow along while the first package is set up and tested.

LLM for Developers

Models
Assume Ollama is already installed.
Pull models only if needed:
ollama pull qwen3:4b
ollama pull embeddinggemma

python -m venv .venv

pip install -r requirements.txt

Step 1
python ingest.py

Step 2
python ask.py

Test
Ask one supported question and one 
unsupported question.

The package should already work. The first goal is to reproduce the run on your own machine before changing anything.

6

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 7

Ingestion and question flow

This is what happened during the first run.

LLM for Developers

Ingestion

documents
extract
chunk
embed
store

Question

question
embed
retrieve
context
model
answer

The important split

Ingestion prepares the index.

Question flow uses that index to 
answer from retrieved context.

7

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 8

Exercise: add JSON support

Small modification to prove that you understand where file loading belongs.

LLM for Developers

1
Find where supported file types are handled.

2
Add support for .json files.

3
Put a JSON document in docs/.

4
Re-run ingestion.

5
Ask a question whose answer exists in the JSON file.

6
Confirm that unsupported questions still answer “I don’t know.”

Why JSON?
It is familiar, needs no heavy library, and forces 
you to decide how structured data becomes text 
for retrieval.

Optional thought
How should nested JSON be represented so that 
chunks are useful?

8

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 9

Website chatbox on top of local RAG

Browser → Flask API → same RAG core → Ollama

LLM for Developers

Browser
HTML + JS

Flask
/api/chat

RAG core
answer_ques

tion()

Ollama
/api/chat

Docs +
Chroma

New idea: the RAG logic has not changed. We have added a browser client and an HTTP boundary.

9

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 10

Keep the API close to Ollama

A familiar request shape lowers friction for the browser client.

LLM for Developers

POST /api/chat
{
  "model": "qwen3:4b",
  "stream": false,
  "messages": [
    {"role": "user",
     "content": "What does the doc say about ...?"}
  ]

}

{
  "model": "qwen3:4b",
  "message": {
    "role": "assistant",
    "content": "... [1] [2]"
  },
  "citations": [ ... ],
  "grounded": true,
  "no_answer": false

}

Frontend sends messages, not a special RAG payload.
Backend adds citations and grounded/no_answer flags.

10

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 11

End-to-end request flow

Follow the question from the browser to the answer and back.

LLM for Developers

app.js
POST /api/chat
app.py
answer_question()
JSON response
browser

Why server-side?
The browser does not hold documents, embeddings, or 
retrieval logic.

Changing docs
Rebuild the local index with ingest.py before querying.

11

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 12

Work with Package 2

Get the website version running using what you learned from Package 1.

LLM for Developers

1
Start from the supplied website package.

2
Configure it using what you learned in Package 1.

3
Run the backend and open the browser chatbox.

4
Ask one supported and one unsupported question.

5
Trace the request: app.js → app.py → RAG core → response.

6
If time permits: add the same .json support from Package 1.

Architectural check
If Package 2 reuses the same RAG core, where 
should JSON support be implemented?

Goal
Recognise what changed: the interface and API 
boundary, not the retrieval logic.

12

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 13

OpenWebUI Knowledge behind the website

Same website idea. Different owner of the retrieval layer.

LLM for Developers

Package 2 — our backend owns RAG

Frontend
  ↓
Backend
  ↓
Retrieval code + Chroma
  ↓
Ollama

Package 3 — OpenWebUI owns RAG

Frontend
  ↓
Backend
  ↓
OpenWebUI API
  ↓
Knowledge + model

The website barely changes. The important change is where ingestion, retrieval, and model selection are configured.

13

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 14

Set up Knowledge in OpenWebUI

This is the RAG setup for Package 3.

LLM for Developers

1
Open OpenWebUI.

2
Go to Workspace → Knowledge.

3
Create a Knowledge Base.

4
Add or upload the documents.

5
Wait for OpenWebUI to index the files.

6
Attach the Knowledge Base to the model or reference it from the API.

Responsibility moved
The package no longer owns document extraction, 
embedding, vector storage, or retrieval.

Practical note
The backend still needs the OpenWebUI URL, API 
token, model, and Knowledge/collection choice.

14

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 15

OpenWebUI API with Knowledge

The backend calls OpenWebUI instead of calling Ollama and Chroma directly.

LLM for Developers

POST /api/chat/completions
Authorization: Bearer <token>

{
  "model": "selected-model",
  "messages": [
    {"role": "user",
     "content": "What does the document say?"}
  ],
  "files": [
    {"type": "collection", "id": "knowledge-id"}
  ]

}

Package 2
Our backend performs retrieval and calls Ollama.

Package 3
Our backend asks OpenWebUI. OpenWebUI 
performs retrieval and calls the model.

Keep this configurable: URL, token, model, and

Knowledge ID.

15

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 16

OpenWebUI request flow

The path looks similar, but the retrieval layer has moved.

LLM for Developers

app.js
Flask backend
OpenWebUI API
Knowledge

retrieval
model
response

What our code still owns
Browser UI, backend route, configuration, and response 
handling.

What OpenWebUI owns
Knowledge Base, retrieval behaviour, and model connection.

16

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 17

Work with Package 3

Run the OpenWebUI Knowledge version and compare responsibility with Package 2.

LLM for Developers

1
Configure OpenWebUI URL and API token.

2
Select the model and Knowledge collection.

3
Start the supplied website package.

4
Ask the same supported and unsupported questions.

5
Identify what is no longer implemented in local Python RAG code.

6
If time permits: use your own Knowledge collection.

Comparison question
Which solution gives you more control? Which 
solution is faster to integrate?

Takeaway
The same website can hide very different backend 
architectures.

17

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 18

GGUF model into Ollama

Import a model so it can be used like the other Ollama models.

LLM for Developers

Hugging Face

GGUF file

Create
Modelfile

ollama

create

ollama run

+ API test

Path: Hugging Face GGUF 
 Modelfile 
 Ollama model 
 terminal and API.
→
→
→

18

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 19

Build the model and run it

We do this part together.

LLM for Developers

Modelfile
FROM ./model.gguf

ollama create my-model -f Modelfile

ollama run my-model

curl http://localhost:11434/api/generate -d '{
  "model": "my-model",
  "prompt": "Say hello in one short sentence.",
  "stream": false

}'

Create the file, create the model, run it, and test it by API.

19

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 20

Use the same model across the stack

The imported model can move through the tools you have already used.

LLM for Developers

Terminal

prompt

Ollama

API

OpenWebUI

model

Website

flow

Follow the same model: terminal 
 API 
 OpenWebUI 
 the website packages.
→
→
→

20

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 21

Possible expansions

Pick one extension that fits your use case. The goal is to adapt the package, not implement every idea.

LLM for Developers

• Make PDFs with images work using OCR or a vision model.

• Add more file types: DOCX, HTML, CSV, JSON, source code, 
PowerPoint, or Excel.

• Add upload instead of copying files into docs/.

• Add document selector, metadata filters, or multiple knowledge 
bases.

• Add streaming responses, clickable citations, or better error 
messages.

Choose one extension
Pick one extension that matters for your use case, or 
define your own.

Suggested focus
Better to finish one useful extension and explain it 
clearly than start many unrelated changes.

21

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.
