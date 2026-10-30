# StudyGraph — Project Tracking

This folder is the working memory of the project: what we are building, in which order,
what is decided, and what is true right now. The `docs/design`, `docs/architecture` and
`docs/requirements` folders describe the product; `docs/plan` describes the work.

## Index

| File | Purpose | Cadence |
|---|---|---|
| [status.md](status.md) | Single source of truth for "where are we now": environment, what works, blockers, next 3 actions | update at the end of every session |
| [implementation-plan.md](implementation-plan.md) | Phased plan from empty repository to demonstrable MVP, with exit criteria and exam evidence | update when a phase completes or is re-scoped |
| [backlog.md](backlog.md) | Ticket list (`SG-xxx`) with priority, dependencies and state | update whenever a ticket moves |
| [decision-log.md](decision-log.md) | Numbered technical decisions (`ADR-xxx`) with status and consequences | add an entry for every technical choice |
| [risks.md](risks.md) | Risk register with impact, mitigation and owner | review at every phase boundary |
| [../architecture/tech-stack.md](../architecture/tech-stack.md) | Chosen stack, versions, runtime topology, open items | when a library/model/port changes |
| [../RAG/knowledge-base.md](../RAG/knowledge-base.md) | How course material is prepared, chunked, indexed and retrieved | when the pipeline changes |
| [../evaluation/rag-comparison-results.md](../evaluation/rag-comparison-results.md) | RAG vs. non-RAG evaluation template and results | after each evaluation run |
| [../evaluation/regression-vs-rag.md](../evaluation/regression-vs-rag.md) | Required comparison exercise: linear regression vs. local LLM + RAG | its own small track |

## How to use these documents

1. **Starting a session:** read [status.md](status.md), then the top "Ready" tickets in
   [backlog.md](backlog.md). Never start work that is not in the backlog.
2. **During work:** one ticket at a time. If a decision is needed, add an `ADR-xxx`
   entry first, then implement.
3. **Ending a session:** move ticket states in the backlog and rewrite the "now/next"
   part of [status.md](status.md). Leave the repo in a state where `uv run pytest -q` passes.

## Ticket states

| State | Meaning |
|---|---|
| `Todo` | defined, not started, dependencies may be open |
| `Ready` | defined, all dependencies done — can be picked up |
| `Doing` | actively being worked (ideally one per person) |
| `Blocked` | cannot proceed; the reason is in the row |
| `Done` | code + tests + docs merged, verified by a real run |

## Priority levels

- **P0** — required for the MVP and for the exam's mandatory criteria (local LLM, RAG,
  4T's, comparison exercise).
- **P1** — required for a credible demo and the synopsis (evaluation, error handling,
  setup guide).
- **P2** — nice to have; must never delay P0/P1 (supplementary uploads, buddy duplication).

## Branch convention

`feat/sg-0xx-short-name`, `docs/sg-0xx-short-name`, `fix/sg-0xx-short-name`.
The exam delivery branch is `mandatory-1`. Small doc-only commits may go straight to it.
