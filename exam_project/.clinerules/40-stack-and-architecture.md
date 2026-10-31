# Stack & architecture conventions (always active)

Stack: **Python 3.12 + Streamlit + ChromaDB + LangGraph + Ollama**, SQLite for
application data. Rationale and open items: `docs/architecture/tech-stack.md`.

## Runtime topology (three local processes)

| # | Process | Default | Started by |
|---|---|---|---|
| 1 | Ollama server | `http://127.0.0.1:11434` | user (must be running) |
| 2 | Chroma server | `http://localhost:8000` | `chroma run --path .\data\chroma` |
| 3 | Streamlit app | `http://localhost:8501` | `uv run streamlit run app/main.py` |

Optional process 4: a Chroma inspection UI (ChromaUI / `chromadb-admin` /
`chroma browse`) — developer tooling only, never a runtime dependency of the app.

## ChromaDB

- The app talks to the **server** via `chromadb.HttpClient(host=..., port=...)`.
  Never open a `PersistentClient` on a path that a `chroma run` server owns — the two
  will fight over the SQLite file.
- Tests use `chromadb.EphemeralClient()`; never a real directory.
- **Compute embeddings ourselves** through `app/adapters/embedder.py` and pass them
  explicitly (`collection.add(..., embeddings=...)`, `collection.query(query_embeddings=...)`).
  Do not rely on Chroma's default embedding function: it downloads an ONNX model, adds an
  `onnxruntime` dependency, and silently changes dimensions if the default changes.
- One collection per course+version, e.g. `llms_for_devs_v1`. Never rename it silently;
  a rename is a decision-log entry plus a re-index.
- Store `embedding_model`, `embedding_dim`, `chunker_version`, `index_version` in the
  collection metadata and validate them on startup. On mismatch: fail loudly with a
  message telling the user to re-index. Never mix dimensions in one collection.

## LangGraph

- The graph lives in `app/graph/` and is compiled once per process
  (`@st.cache_resource` in Streamlit, module-level in tests).
- State is a typed `TypedDict` (`StudyGraphState`). Nodes return **partial** state
  updates; routing functions are pure and side-effect free.
- The graph is the single place that decides RAG vs non-RAG, based on the conversation's
  Buddy snapshot — never on the Buddy's name, Traits or prompt text.
- Nodes must stay thin wrappers over service/domain functions so they can be tested with
  fakes. Do not put prompt assembly, SQL or HTTP calls directly in node bodies.
- Use LangGraph for orchestration that earns its place (conditional retrieval, retrieval
  failure branch, state passed to the UI for sources). Do not grow it into a multi-agent
  system: that is explicitly out of MVP scope.

## Streamlit

- `app/main.py` is the entry point; use `st.navigation`/`st.Page` for the pages:
  Chat, Buddies, Conversations, About.
- Clients, the compiled graph and the SQLite connection factory go in `@st.cache_resource`.
  Per-user state (current conversation, selected Buddy) goes in `st.session_state`.
- One rerun must not re-index, re-embed or reconnect a server. Guard with `cache_resource`.
- Chat UI: `st.chat_message`, `st.chat_input`, `st.write_stream` for streaming tokens.
  `st.chat_input` is called at the top level of the page body, not inside a column or form.
- Say clearly in the UI whether a conversation is **course-grounded** or **general**;
  show sources in an `st.expander`. Never present a non-grounded answer as course-grounded.
- All user-visible errors are caught in the page and rendered as `st.error(...)` with a
  retry hint; the app must not crash on a stopped Ollama or Chroma server.

## Ollama

- Use the `ollama` Python client with an explicit `Client(host=config.ollama_base_url)`.
- Always pass explicit `options` (at minimum `temperature`, `num_ctx`) and a request
  timeout; wrap failures in `LlmUnavailableError` / `LlmGenerationError`.
- Never shell out to the `ollama` CLI from application code. CLI use belongs in
  `scripts/` and in documentation only.
- Embeddings use the same server (`ollama.embed(...)`), not a second runtime.

## SQLite application data

- `PRAGMA foreign_keys = ON`, `journal_mode = WAL`, one short-lived connection per
  operation, explicit transactions for multi-row writes (conversation + first message).
- Store the Buddy snapshot as JSON in its own column **plus** a `snapshot_version` field;
  never rely on the live Buddy row to reconstruct an old conversation.
- Changing the schema means a migration script under `scripts/` and a decision-log entry.
  No destructive schema edits on a populated database.
