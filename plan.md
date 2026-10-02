# Mandatory 1 delivery plan

## Goal

Turn the existing local Ollama/Flask prototype into a submission-ready Mandatory 1 delivery within approximately 100 minutes. The focus is demonstrating every requirement with reproducible evidence, rather than rebuilding the project.

## Current assessment

The repository already contains:

- A runnable Python/Flask workflow with ten specialised responsibilities.
- Two model roles (`qwen2.5-coder:7b` and `llama3.2:3b`).
- A README, a synopsis PDF, and presentation material.

The main gaps to close are:

1. Two separately configurable local endpoint URLs. The current workflow uses one `OLLAMA_URL` for both models.
2. Explicit, reproducible evidence for the full demo workflow.
3. Architecture, ticket, ADR, API-contract, quality-report, deployment-validation, and traceability artifacts.
4. Automated tests and recorded static-check results.
5. A clearly structured comparison of two candidate toolchains and recommendation.
6. The mandatory review of another group. This needs that group's actual delivery or notes.

## Recommended workflow

```text
Endpoint A (local Ollama host A) --> Architect, Tech Lead, QA
Endpoint B (local Ollama host B) --> Coding workers, Documentation
                                      |
                         Python workflow coordinator
                                      |
                    versioned artifacts + Git diffs + reports
```

Configuration should expose endpoint and model selection independently, for example:

```text
ARCHITECT_ENDPOINT=http://127.0.0.1:11434
WORKER_ENDPOINT=http://127.0.0.1:11435
ARCHITECT_MODEL=qwen2.5-coder:7b
WORKER_MODEL=llama3.2:3b
```

This makes endpoint routing configuration-based and directly addresses the assignment's hard requirement.

## Work allocation and schedule

| Time | Owner | Work | Evidence / Definition of Done |
| --- | --- | --- | --- |
| 0-10 min | Everyone | Confirm the two toolchains being evaluated, endpoint A/B hosts and models, and the selected recommendation. | Both candidate names and endpoint configuration are agreed. |
| 10-40 min | Codex + Person 1 | Upgrade the workflow for endpoint-specific configuration; add endpoint health checks, saved artifacts, plan/diff control evidence, and deployment validation. | A config-driven run proves both endpoints are contacted; validation output is saved. |
| 10-40 min | Person 2 | Complete the setup guide. | A third party can install prerequisites, start both endpoints, configure roles, run the demo, tests, and validation. |
| 10-45 min | Person 3 | Complete synopsis sections: comparison, recommendation, failure modes, trade-offs, and functional/non-functional traceability. | Every requirement has an evidence reference; synopsis remains 7-10 pages. |
| 10-45 min | Person 4 | Review another group's delivery. | Completed review with group name, concrete strengths/weaknesses, coverage assessment, and adoption/change recommendations. |
| 45-70 min | Codex + Person 1 | Add and run automated tests and relevant static checks; write the quality report. | Real commands and pass/fail results are recorded, including limitations and risks. |
| 45-70 min | Persons 2-4 | Incorporate setup, report, and peer-review material into synopsis and slides. | Documentation uses the final configuration and real command results. |
| 70-90 min | Everyone | Run the end-to-end demo once. | Capture endpoint health, generated architecture/tickets, parallel worker evidence, test results, updated docs, and deployment validation. |
| 90-100 min | Everyone | Final submission review. | Checklist is complete; Git diff/commit is reviewable; files are named and packaged correctly. |

## Candidate-toolchain position

Use two toolchains that the group can accurately describe and support with evidence:

1. **Custom Python/Flask coordinator + Ollama** (recommended): lightweight, fully controllable, open source, configuration-driven endpoint routing, and easy to demonstrate locally.
2. **OpenHands + Ollama** (comparison candidate): broader coding-agent automation but more setup complexity, higher hardware/context cost, and less direct control over the group-specific workflow.

Do not claim to have run OpenHands unless the group has actually done so. It can still be evaluated as a documented candidate, provided the synopsis distinguishes documented evaluation from the demonstrated selected workflow.

## Required demo evidence

Before submission, collect these real outputs:

- Endpoint A and B health-check responses.
- The versioned configuration mapping roles to endpoints/models.
- Generated architecture output, including components, interface contract, deployment topology, and ADR.
- Tech-lead tickets with scope, out-of-scope work, acceptance criteria, Definition of Done, and dependencies.
- Evidence of at least two partitioned coding-worker responsibilities and reviewable multi-file changes.
- Test and static-check commands with actual results.
- Quality report with results, limitations, risks, and mitigations.
- Updated README, API documentation, operational runbook, and design documentation.
- Deployment checklist or script output.
- `git status`, `git diff`, and/or `git log` evidence for reviewability and reproducibility.
- Completed review of another group's work.

## Final acceptance checklist

- [ ] Two separate local endpoints are configured and demonstrated.
- [ ] Routing changes through configuration, not code rewiring.
- [ ] Tooling is open source.
- [ ] All six functional responsibilities are covered by artifacts and/or demo output.
- [ ] Plan + diff or an equivalent human-control mechanism is demonstrated.
- [ ] Git-based reproducibility and context-management strategies are explained.
- [ ] Local-only network exposure and secrets handling are documented.
- [ ] Two toolchains are compared and one is recommended with rationale.
- [ ] Synopsis is 7-10 pages and includes the other-group review.
- [ ] Setup guide enables an independent reproduction of the demo.
