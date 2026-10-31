---
paths:
  - "tests/**"
  - "**/test_*.py"
  - "conftest.py"
---

# Testing rules

- **Framework:** `pytest`, run with `uv run pytest -q` from `exam_project/`.
- **Layout:** `tests/unit/` (pure, fast, no I/O), `tests/integration/` (real SQLite temp
  file, in-memory `EphemeralClient` Chroma, fake LLM). Mirror the `app/` package layout.
- **No live services in unit tests.** Never require a running Ollama server or Chroma
  server. Inject fakes through the adapter protocols; use `chromadb.EphemeralClient()`
  where a real vector store is needed.
- **Integration marker:** tests that *do* require a live Chroma/Ollama are marked
  `@pytest.mark.integration` and excluded by default
  (`uv run pytest -q -m "not integration"`). The default run must be green offline.
- **Naming:** `test_<unit>_<behaviour>`, one behaviour per test, arrange-act-assert.

## Behaviour that must be covered before the MVP is "done"

- Prompt builder emits Task, Tone, Traits and Target; omitting a dimension is visible
  in the rendered prompt (4T's are demonstrable, not implied).
- Buddy snapshot is immutable: editing a Buddy never changes an existing conversation.
- RAG routing: a course-associated conversation calls the retriever; a no-course
  conversation **never touches** the retriever (assert the fake was not called).
- Retrieval outcomes are distinguished: `ok`, `empty`, `failed`, `skipped` — a failure
  is never reported as a successful grounded answer.
- Source references are propagated from retrieved chunks to the stored assistant
  message, and are absent when retrieval was skipped or empty.
- Validation errors for empty messages, unknown Buddy/course ids, invalid Traits.
- Persistence survives a reconnect: write, close, reopen the same SQLite file, read back.

## UI tests

- Use Streamlit's `streamlit.testing.v1.AppTest` for the pages. Keep pages thin so most
  logic is testable without `AppTest`; assert on rendered text/state, not on internals.
- `AppTest` must run with fake adapters (no network, no real DB file).

## Housekeeping

- Do not commit `.pytest_cache/`, `__pycache__/`, `.coverage`, `coverage.xml`.
- A flaky test is a bug: fix or delete it, never `@pytest.mark.skip` it silently.
