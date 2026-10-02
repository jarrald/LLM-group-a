# Tech Lead — Task Breakdown

Incremental tickets for the implemented feature: **configuration-driven routing to
two separate local Ollama endpoints.**

## Ticket 1 — Introduce two configurable endpoints

- **Scope:** add `ARCHITECT_ENDPOINT` and `WORKER_ENDPOINT` (both defaulting to
  `OLLAMA_URL`), and an `endpoint_for()` router.
- **Out of scope:** changing the agent registry semantics; changing model names.
- **Acceptance criteria:**
  - `endpoint_for("architecture")` returns `ARCHITECT_ENDPOINT`.
  - `endpoint_for("security")` returns `WORKER_ENDPOINT`.
  - Setting only `OLLAMA_URL` keeps both endpoints equal.
- **Definition of done:** unit tests pass; `ruff check` and `mypy` pass.
- **Dependencies:** none.

## Ticket 2 — Route agent calls through the selected endpoint

- **Scope:** thread `endpoint` through `ask_ollama`; record `endpoint` on each
  agent result; surface it in CLI and web output.
- **Out of scope:** introducing a new agent; changing prompts.
- **Acceptance criteria:** each agent result carries `endpoint`; `/api/health`
  reports both endpoints.
- **Definition of done:** 16 tests pass; `run_workflow` returns 10 agents with a
  non-empty `endpoint` field.
- **Dependencies:** Ticket 1.

## Ticket 3 — Per-endpoint model verification

- **Scope:** `_installed_models(endpoint)` + `verify_models()` checking each
  endpoint for the model its roles need.
- **Acceptance criteria:** a missing model on either endpoint raises a clear
  `RuntimeError`; `/api/health` returns `503` on failure.
- **Definition of done:** error-path tests pass; manual health check documented.
- **Dependencies:** Ticket 1.

## Ticket 4 — Tests, static checks and documentation

- **Scope:** add `tests/` (config, workflow, API), `pyproject.toml` (ruff + mypy),
  and update `README.md` + `AGENTS.md`.
- **Acceptance criteria:** `pytest` green; `ruff check`, `ruff format --check`,
  `mypy` clean; docs describe the two-endpoint setup.
- **Definition of done:** quality report (`docs/quality_report.md`) records real
  results.
- **Dependencies:** Tickets 1–3.
