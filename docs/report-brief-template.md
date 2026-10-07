# Report brief — Mandatory 1 synopsis (input pack for the report author)

> This is the single source of truth for whoever (or whatever) writes the synopsis.
> Put it at `main-folder/report/brief.md`, next to the three project folders.
> Fill in every `<...>` placeholder, then have the AI write `report/synopsis.md`.

## 0. Rules for the writer

- Cite the **raw result files** for every number (path + file). Never invent metrics.
- Distinguish "documented/compared" from "actually ran". We ran all four candidates.
- Cover the **required deliverable** in `docs/Mandatory 1.md` (synopsis + setup guide).
- **The peer review of another group is mandatory.** Reserve a section for it.
- Keep the recommended workflow's architecture and a requirement-traceability table.

## 1. The assignment (spec)

Hard requirements: 2+ local endpoints, switchable/routable via **configuration**;
open source. Functional: architecture, tech lead, implementation (N>2 workers,
multi-file changes), testing & quality (creates **and runs** tests), documentation,
deploy validation. Non-functional: predictability & control (ask-before-run/edit or
plan+diffs), reproducibility (git / reviewable diffs), context management, security
baseline (no public unauthenticated endpoint).

Evaluation axes (per candidate): setup complexity, capability coverage,
multi-endpoint support, failure modes, recommendation.

Deliverables: synopsis 7-10 pages (candidates compared, architecture of the
recommended workflow, requirement-by-requirement coverage, tradeoffs/risks/failure
modes, recommendation + rationale, peer review) **and** a short setup guide.

## 2. Candidates

| # | Candidate | Folder | Status | Evidence |
| --- | --- | --- | --- | --- |
| 1 | LangGraph | `../langgraph-vs-crewai/<...>` | ran | `<results/...>` |
| 2 | CrewAI | `../langgraph-vs-crewai/<...>` | ran | `<results/...>` |
| 3 | Custom Python/Flask coordinator | `../LLM-group-a` | ran | `docs/quality_report.md`, `docs/agentic-mode.md` |
| 4 | Aider | `../aider-experiment/<...>` | ruled out | `<notes>` |

## 3. Framing for candidate 3 (own orchestration)

Present it as the **baseline** the frameworks are measured against, not a footnote:

> LangGraph and CrewAI provide orchestration primitives; in both cases we still had
> to write the tools, sandboxing, plan/diff control and context handoff ourselves.
> Candidate 3 is the smallest implementation that satisfies every requirement —
> including the hard 2-endpoint requirement — with zero framework glue.

## 4. Framing for candidate 4 (Aider)

A **documented negative result**, used as evidence for the *failure modes* axis:
no native role routing / multi-endpoint binding, so N workers + two endpoints needed
extensive custom glue. Keep it factual (we ran it; here is what broke).

## 5. Multi-endpoint facts to state per candidate

- CrewAI: per-agent `LLM(model=..., base_url=...)` -> role-to-endpoint binding is
  configuration, close to our `endpoint_for()`.
- LangGraph: routing is explicit graph code over per-endpoint clients.
- Aider: no clean role-to-endpoint binding.
- Our coordinator: `ARCHITECT_ENDPOINT` / `WORKER_ENDPOINT` env vars.

## 6. Tool-calling reality (shared failure mode)

Local models differ: `llama3.1:8b` and `qwen3.5:9b` emit structured `tool_calls`;
`qwen2.5-coder:7b` and `llama3.2:3b` emit the call as JSON text. Record which model
each candidate used, or the comparison is not apples-to-apples.

## 7. Section skeleton + page budget

| Section | Pages |
| --- | --- |
| Objective, method, candidate overview | 0.5 |
| Per-candidate evaluation (4 x 5 axes) | 3-4 |
| Architecture of recommended workflow | 1 |
| Requirement traceability table (requirement -> evidence) | 1 |
| Tradeoffs, risks, failure modes | 1 |
| Recommendation + rationale | 0.5 |
| Peer review of another group (mandatory) | 0.5-1 |
| Setup guide (appendix) | excluded |
