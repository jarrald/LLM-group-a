# Python & project conventions (always active)

- **Runtime:** Python **3.12**, managed with `uv` (`uv venv --python 3.12`, `uv run ...`).
  The machine default is 3.14.7; do **not** target it, because several planned wheels
  (chromadb/onnxruntime/streamlit transitive deps) are not reliably available there.
  Never claim a package supports 3.14 without verifying it.
- **Platform:** Windows 11 + PowerShell 7 (`pwsh`). All commands must be copy-paste
  correct for PowerShell (see `powershell.md`).
- **Language:** code, comments, docstrings, prompts, UI strings and docs in **English**
  in this sub-project. (The parent repo uses Danish; that does not apply here.)
  Identifiers in English.

## Layering (do not violate)

```text
app/main.py            Streamlit entry point (pages only, no business logic)
app/ui/                Streamlit views/widgets (no prompts, no clients)
app/services/          use cases: buddy, conversation, chat/turn orchestration
app/graph/             LangGraph definition, state, routing, nodes
app/domain/            dataclasses + validation, pure, no I/O
app/adapters/          ollama_client, chroma_client, sqlite repo, embedder
app/prompts/           prompt templates (*.md) + builder
app/config.py          all environment reading
scripts/               CLI entry points (ingest, reindex, smoke tests)
tests/                 unit + integration tests
```

- A Streamlit page must call a **service function**, never an adapter directly.
- Domain code must not import Streamlit, LangGraph, Chroma or Ollama.
- Adapters must be swappable behind small protocols/interfaces so tests can inject fakes.

## Style

- Type hints on every public function; PEP 604 unions (`str | None`) and PEP 585
  generics (`dict[str, object]`, `list[Chunk]`).
- Domain models are `@dataclass(frozen=True, slots=True)`. No ORM and no pydantic in
  our own code; validation happens in explicit `validate_*` functions raising our own errors.
- Absolute imports only (`from app.domain.buddy import BuddySnapshot`).
- `logging` module only (module-level `logger = logging.getLogger(__name__)`); no `print`
  in `app/` (scripts may print).
- Errors: define them in `app/errors.py` (e.g. `ValidationError`, `LlmUnavailableError`,
  `RetrievalError`, `PersistenceError`). Never use a bare `except:`, never swallow an
  exception silently, never turn a failure into an empty success.
- Formatting: 4 spaces, double quotes, no trailing whitespace. The repo-root
  `pyproject.toml` configures ruff with `line-length = 240`; match that config rather
  than reformatting unrelated files.
- Timestamps are timezone-aware UTC (`datetime.now(timezone.utc)`), serialised as ISO-8601.
- Never hardcode a model name, endpoint, port, path or collection name — read it from
  `app/config.py`, which reads `os.getenv(<NAME>, <default>)`.
- Keep generation parameters (temperature, `num_ctx`, top-k) in config with explicit
  defaults; evaluation runs must be repeatable from the same config.
- Do not use `os.chdir`. Resolve paths from `app/config.py`.

## Dependencies

- Planned set (confirm before adding anything else): `streamlit`, `chromadb`,
  `langgraph`, `ollama`, `pytest`, `ruff`, `mypy`, plus `scikit-learn`/`numpy` only for
  the separate regression experiment.
- Adding a dependency requires: update `requirements.txt`/`pyproject.toml`, an entry in
  `docs/plan/decision-log.md`, and an explicit note in the change summary.
