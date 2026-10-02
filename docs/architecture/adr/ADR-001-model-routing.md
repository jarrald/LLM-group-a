# ADR-001: Configuration-driven model routing

- **Status:** Accepted
- **Date:** 2026-10-02

## Context

The assignment requires a minimum of two separate local model endpoints and the
ability to switch/route between them **via configuration**, not manual rewiring.
The prototype originally used a single `OLLAMA_URL` for every agent.

## Decision

Introduce two independently configurable endpoints:

- `ARCHITECT_ENDPOINT` (defaults to `OLLAMA_URL`)
- `WORKER_ENDPOINT` (defaults to `OLLAMA_URL`)

Architect-role agents (`architecture`, `tech_lead`, `implementation`) route to
`ARCHITECT_ENDPOINT`; all other agents route to `WORKER_ENDPOINT`. Routing is
implemented in `endpoint_for()` using the `ARCHITECT_ROLE_AGENTS` set.

## Consequences

- **Positive:** switching endpoints or hosts is a pure environment-variable change;
  different roles can be bound to different models/hosts.
- **Positive:** backward compatible — setting only `OLLAMA_URL` keeps both roles on
  one server.
- **Negative:** two more environment variables to document and validate in the
  health check (`/api/health` now reports both endpoints).
