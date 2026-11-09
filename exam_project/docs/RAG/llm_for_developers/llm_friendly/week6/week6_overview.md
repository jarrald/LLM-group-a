# Week 6 — Local RAG from document to application

Sources: `source/week6/local_rag.pdf` and the accompanying code examples. See the [full text of the slides](week6_source_local_rag_pdf.md). The folder is called `week6`, even though some included files call themselves Week 8 or Week 10. The week placement follows the uploaded folder; the original titles of the files are preserved.

## RAG is a workflow

RAG is not a particular model. Documents are loaded, split into chunks and turned into embeddings, which are stored in Chroma. When a question is asked, the question is embedded, the relevant chunks are retrieved, and the model receives them as context before generating the answer.

Ingestion and question answering are two different courses of events: ingestion prepares the index, while a question uses the index. If the documents change, the index must be updated.

## Three packages and where the responsibility sits

| Package | Interface | Who handles retrieval? | Model access |
|---|---|---|---|
| Custom RAG CLI | Terminal | Python code and Chroma | Ollama |
| Custom RAG web | Browser and Flask | The same Python RAG core | Ollama |
| OpenWebUI Knowledge web | Browser and backend | OpenWebUI Knowledge | OpenWebUI API |

In the web package the interface and the HTTP boundary change, while the retrieval core is reused. The browser sends the question to the backend, which adds retrieval and returns the answer, the source references and the grounding status. In the Knowledge variant, ingestion, embeddings and retrieval move into OpenWebUI.

## Grounding and testing

The rule in the material is to answer from the context and to say "I don't know" when the answer is not there. Source references such as `[1]` and `[2]` must be traceable to the retrieved chunks. Both a supported question and a question without an answer in the material must be tested.

This rule is the behaviour of the teaching package. StudyGraph's own prompt strategy lives in the project's prompt files and may have an explicitly marked general fallback.

## Exercise: JSON support

The slides ask you to find the document loading, add `.json`, place a document in the document folder, re-run ingestion and ask a question whose answer is only in the JSON file. The exercise examines where structured data should be turned into retrievable text; it is not a claimed result of having changed the teaching code.

## Code and source files

`week6_source_*.md` preserve Python, frontend code, texts and configuration descriptions. Code is divided into sections with the original line numbers and has not been executed. Several `.md` files in the raw material actually contain Python or package lists; the conversion shows their real content rather than guessing from the file name. Virtual environments, caches and `.env` are not teaching content in the index.

## Review questions

1. What is the difference between ingestion and retrieval when a question is asked?
2. What changes from the CLI to the Flask web package?
3. Who owns retrieval in the OpenWebUI variant?
4. Where should JSON support be added if two interfaces share the RAG core?
5. How do you test that an answer does not invent support from the documents?