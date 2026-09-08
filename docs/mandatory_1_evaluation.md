# Assignment: Local Multi-LLM Coding Workflow Evaluation

## Objective

Identify the most viable way to run a **local, multi-LLM workflow** that can collaboratively produce software artifacts across the full software-development lifecycle:

* Architecture
* Implementation
* Testing
* Documentation
* Deployment validation

The workflow must use **local model backends**.

You must evaluate **at least two candidate approaches** and recommend one.

> **Important:** After your delivery, you must review one of the other deliveries. Otherwise, you risk not getting a pass on this assignment and may lose the opportunity to go to the exam in this class.

---

# 1. Hard Requirements

## 1.1 Multiple Local Endpoints

The solution must:

* Support a minimum of **2 separate local model endpoints**.
* Support different local LLM servers/hosts.
* Allow switching or routing between endpoints through **configuration**.
* Not require manual rewiring of the workflow each time the model endpoint changes.

Examples of local endpoints could include different local LLM servers or hosts.

## 1.2 Open Source

The tooling used must be **open source**.

There is no requirement for the tooling to use an OSI-approved license.

---

# 2. Functional Requirements

The proposed solution must support a workflow covering all of the following responsibilities.

These responsibilities may be implemented as:

* Distinct agents
* A structured pipeline
* A combination of agents and pipeline stages

All responsibilities must be covered.

---

## 2.1 Architecture Responsibility

The workflow must produce architecture artifacts such as:

* Component decomposition
* Component responsibilities
* Interface contracts

  * OpenAPI specification
  * Equivalent API/interface specification
* Deployment topology
* Deployment constraints
* Architecture Decision Records (ADRs)

### Expected Output

Example artifacts:

```text
docs/
├── architecture/
│   ├── system-overview.md
│   ├── component-design.md
│   ├── deployment-topology.md
│   └── adr/
│       ├── ADR-001-model-routing.md
│       └── ADR-002-agent-architecture.md
└── api/
    └── openapi.yaml
```

---

## 2.2 Tech Lead Responsibility

The workflow must break work into incremental tasks/tickets.

Each task should contain:

* Scope boundaries
* Acceptance criteria
* Definition of Done
* Dependencies
* Dependency ordering

Example:

```text
Ticket: Implement user authentication API

Scope:
- Add authentication endpoint
- Add token validation
- Add authentication tests

Out of scope:
- Frontend authentication UI
- OAuth integration

Acceptance criteria:
- POST /auth/login returns a valid token
- Invalid credentials return HTTP 401
- Tests cover successful and failed authentication

Dependencies:
- Database schema
- User repository
```

---

## 2.3 Implementation Responsibility

The solution must support:

* Multiple coding workers, **N ≥ 2**, or
* A credible equivalent design that allows work to be parallelized or partitioned.

The workflow must also:

* Produce multi-file changes.
* Work against a repository.
* Allow changes to be reviewed.
* Integrate work from multiple implementation tasks/workers.

---

## 2.4 Testing & Quality Responsibility

The workflow must:

* Create tests.
* Run tests.
* Support appropriate testing levels:

  * Unit tests
  * Integration tests
  * Other relevant tests

It must also produce a **quality report** containing:

* Test results
* Static analysis results

  * Linting
  * Type checking
  * Formatting checks
  * Other relevant static checks
* Known limitations
* Known risks

Example:

```text
Quality Report

Tests:
- Unit tests: 42 passed
- Integration tests: 8 passed
- Failed: 0

Static checks:
- Linter: passed
- Type checker: passed
- Formatter: passed

Known limitations:
- External service integration is mocked
- Performance testing has not been performed

Risks:
- Local model may occasionally generate inconsistent implementations
```

---

## 2.5 Documentation Responsibility

The workflow must produce or update developer and user documentation.

Required documentation includes:

### README

Must cover:

* Installation
* Setup
* Configuration
* Running the application
* Running tests

### API Usage

If the project exposes an API, document:

* Available endpoints
* Request formats
* Response formats
* Authentication
* Example usage

### Operational Documentation

Include:

* Runbook notes
* Troubleshooting
* Configuration
* Deployment considerations

### Design Documentation

Include:

* Architecture
* Design decisions
* Component responsibilities
* Important technical decisions

---

## 2.6 Deployment Validation Responsibility

The workflow must validate deployability using at least one of the following:

* Deployment checklist
* Deployment script
* Container build/deployment configuration
* Environment/configuration documentation

Example:

```text
Deployment Validation

[✓] Application builds successfully
[✓] Docker image builds successfully
[✓] Required environment variables documented
[✓] Configuration validated
[✓] Health check available
[✓] Tests pass
[✓] Deployment configuration validated
```

---

# 3. Non-Functional Requirements

## 3.1 Predictability & Control

The workflow must provide at least one control mechanism.

Acceptable mechanisms include:

### Option A — Ask Before Execution

The system asks for approval before:

* Running commands
* Editing files

### Option B — Plan + Diff

The workflow produces:

1. A plan
2. Proposed changes
3. A diff for review
4. Execution only after review/approval

The chosen mechanism must be explained and demonstrated.

---

## 3.2 Reproducibility

The workflow must support version control using **Git**.

Changes must be available as:

* Git commits, or
* Clearly reviewable diffs

It must be possible to run the same workflow twice and receive **comparable outputs/progress**, even if the generated content is not identical.

The report should explain:

* How prompts/configuration are versioned
* How artifacts are stored
* How changes are reviewed
* How workflow runs can be reproduced

---

## 3.3 Context Management

The workflow must explain how it avoids **silent context loss**.

Possible mechanisms include:

* Artifact handoffs
* Explicit summaries
* Scoped context
* Persistent task files
* Architecture documents
* Structured task definitions
* Git history
* Shared project state

The report must also explain how the workflow behaves as the project grows.

Consider:

* Repository size
* Documentation size
* Number of files
* Number of tasks
* Number of agents
* Context-window limitations

The proposed solution should explain how it prevents the LLMs from receiving unnecessary or excessive context.

---

## 3.4 Security Baseline

The workflow must **not require an unauthenticated model endpoint to be publicly exposed**.

Local model endpoints should remain appropriately protected.

The report should explain:

* Network exposure
* Authentication where applicable
* Access boundaries
* Secrets/configuration handling
* Risks associated with local model servers

---

# 4. Evaluation Requirements

At least **two candidate toolchains** must be evaluated.

The evaluation should compare the approaches against the requirements above.

---

## 4.1 Candidate Toolchain #1

### Overview

Describe:

* Toolchain name
* Main components
* Architecture
* Why it is a candidate

### Setup Complexity

Evaluate:

* Time to first working run
* Required dependencies
* Required services
* Configuration complexity
* Number of moving parts

### Capability Coverage

Identify which responsibilities are:

* Supported natively
* Supported with configuration
* Require custom glue/code

Evaluate:

* Architecture
* Tech lead/task planning
* Implementation
* Testing
* Quality reporting
* Documentation
* Deployment validation

### Multi-Endpoint Support

Explain:

* How it connects to two separate local model endpoints
* How endpoints are configured
* How routing/switching works
* Whether different roles can use different endpoints

Example:

```text
Architecture Agent → Local Model A
Tech Lead Agent    → Local Model A
Coding Worker 1    → Local Model B
Coding Worker 2    → Local Model B
Testing Agent      → Local Model A
Documentation      → Local Model B
```

### Failure Modes

Evaluate what is most likely to break first:

* Context management
* Tool calling
* File operations
* Command execution
* Test execution
* Model availability
* Parallel workers
* Merge conflicts

Explain:

* How failures are detected
* How failures are recovered
* What requires human intervention

### Overall Assessment

Summarize:

* Strengths
* Weaknesses
* Best use cases
* Requirement gaps

---

# 5. Candidate Toolchain #2

Repeat the same evaluation structure.

## Overview

Describe:

* Toolchain name
* Main components
* Architecture
* Why it is a candidate

## Setup Complexity

Evaluate:

* Time to first working run
* Required dependencies
* Required services
* Configuration complexity
* Number of moving parts

## Capability Coverage

Identify:

* Native capabilities
* Configurable capabilities
* Custom glue/code required

## Multi-Endpoint Support

Explain:

* Connection to two local model endpoints
* Endpoint configuration
* Routing/switching
* Role-specific model assignment

## Failure Modes

Evaluate:

* Context failures
* Tool-calling failures
* File-operation failures
* Command/test failures
* Model failures
* Parallelization failures
* Merge conflicts

Explain detection and recovery mechanisms.

## Overall Assessment

Summarize:

* Strengths
* Weaknesses
* Best use cases
* Requirement gaps

---

# 6. Candidate Comparison

Use a comparison table to make the differences clear.

| Requirement                   | Candidate 1 | Candidate 2 |
| ----------------------------- | ----------- | ----------- |
| Open source                   |             |             |
| Two local endpoints           |             |             |
| Configurable routing          |             |             |
| Role-specific models          |             |             |
| Architecture workflow         |             |             |
| Tech lead/task planning       |             |             |
| Multiple coding workers       |             |             |
| Multi-file repository changes |             |             |
| Testing                       |             |             |
| Quality reporting             |             |             |
| Documentation                 |             |             |
| Deployment validation         |             |             |
| Git/reviewable changes        |             |             |
| Context management            |             |             |
| Human approval/control        |             |             |
| Reproducibility               |             |             |
| Security baseline             |             |             |
| Setup complexity              |             |             |
| Overall suitability           |             |             |

---

# 7. Recommended Workflow

Select one candidate and explain why it is the recommended solution.

## 7.1 High-Level Architecture

Describe the complete workflow.

Example:

```text
                    ┌─────────────────────┐
                    │     User / Git      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Workflow Manager  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌────────────┐
       │ Architect  │   │ Tech Lead  │   │  Planner   │
       └─────┬──────┘   └─────┬──────┘   └─────┬──────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                     ┌─────────────────┐
                     │ Shared Artifacts│
                     │ / Git Repository│
                     └────────┬────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          ┌─────────────┐           ┌─────────────┐
          │ Coding      │           │ Coding      │
          │ Worker 1    │           │ Worker 2    │
          └──────┬──────┘           └──────┬──────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                     ┌─────────────────┐
                     │ Testing / QA    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Documentation   │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Deployment      │
                     │ Validation      │
                     └─────────────────┘
```

Replace the example architecture with the actual architecture of the recommended toolchain.

---

# 8. Local Model Endpoint Architecture

Document the two local model endpoints.

| Endpoint   | Purpose | Host | Model | Port | Configuration |
| ---------- | ------- | ---- | ----- | ---- | ------------- |
| Endpoint A |         |      |       |      |               |
| Endpoint B |         |      |       |      |               |

Explain:

* How each endpoint is started
* How the workflow discovers/connects to it
* How the endpoint is selected
* How roles are mapped to endpoints
* How endpoints can be replaced without changing the workflow

Example configuration:

```yaml
models:
  architecture:
    endpoint: local-a
    model: model-name-a

  tech_lead:
    endpoint: local-a
    model: model-name-a

  coding:
    endpoint: local-b
    model: model-name-b

  testing:
    endpoint: local-a
    model: model-name-a

  documentation:
    endpoint: local-b
    model: model-name-b
```

---

# 9. End-to-End Demo Workflow

The demo should demonstrate the complete workflow.

## Step 1 — Start Local Model Endpoints

Start both local model servers.

Verify that both endpoints are reachable.

```text
Endpoint A: ______________________

Endpoint B: ______________________
```

## Step 2 — Initialize Repository

```bash
git clone <repository>
cd <repository>
```

Document the required setup.

## Step 3 — Architecture

The architecture responsibility should produce:

* Component architecture
* Interfaces/API specification
* Deployment topology
* ADR(s)

Expected artifacts:

```text
docs/
├── architecture/
├── adr/
└── api/
```

## Step 4 — Task Breakdown

The tech lead should produce incremental tasks.

Each task must contain:

* Scope
* Acceptance criteria
* Definition of Done
* Dependencies

## Step 5 — Parallel Implementation

Run at least two coding workers or demonstrate the equivalent parallelized design.

Example:

```text
Worker 1 → Feature A
Worker 2 → Feature B
```

Each worker should produce reviewable changes.

## Step 6 — Review Changes

Inspect:

```bash
git status
git diff
git log
```

Review the generated changes before merging.

## Step 7 — Testing

Run the project's test suite.

Example:

```bash
pytest
```

or the appropriate project-specific command.

Record:

* Tests executed
* Passed tests
* Failed tests
* Test coverage where relevant

## Step 8 — Static Checks

Run relevant checks.

Examples:

```bash
ruff check .
mypy .
```

or equivalent tools for the chosen language.

Record the results.

## Step 9 — Documentation

Verify/update:

* README
* API documentation
* Runbook
* Design documentation

## Step 10 — Deployment Validation

Perform at least one deployment validation activity.

Examples:

```bash
docker build .
```

or:

```bash
./scripts/validate-deployment.sh
```

Document the result.

---

# 10. Quality Report

The final workflow should produce a quality report.

## Test Results

| Test Type   | Command | Result |
| ----------- | ------- | ------ |
| Unit        |         |        |
| Integration |         |        |
| Other       |         |        |

## Static Checks

| Check      | Command | Result |
| ---------- | ------- | ------ |
| Lint       |         |        |
| Type check |         |        |
| Format     |         |        |
| Other      |         |        |

## Known Limitations

Document limitations such as:

* Model quality
* Context-window limitations
* Tool-calling reliability
* Parallel worker coordination
* Merge conflicts
* Slow inference
* Hardware requirements

## Known Risks

Document technical and operational risks and how they can be mitigated.

---

# 11. Functional Requirement Traceability

Demonstrate that every functional requirement is covered.

| Requirement              | Implementation | Evidence |
| ------------------------ | -------------- | -------- |
| Architecture             |                |          |
| Component decomposition  |                |          |
| Interface contracts      |                |          |
| Deployment topology      |                |          |
| ADRs                     |                |          |
| Tech lead task breakdown |                |          |
| Scope boundaries         |                |          |
| Acceptance criteria      |                |          |
| Dependency ordering      |                |          |
| Multiple coding workers  |                |          |
| Multi-file changes       |                |          |
| Test creation            |                |          |
| Test execution           |                |          |
| Quality report           |                |          |
| Static checks            |                |          |
| Developer documentation  |                |          |
| User documentation       |                |          |
| API documentation        |                |          |
| Runbook                  |                |          |
| Design documents         |                |          |
| Deployment validation    |                |          |

---

# 12. Non-Functional Requirement Traceability

| Requirement                                 | Solution | Evidence |
| ------------------------------------------- | -------- | -------- |
| Predictability & control                    |          |          |
| Human approval / plan + diff                |          |          |
| Git/version control                         |          |          |
| Reviewable changes                          |          |          |
| Reproducibility                             |          |          |
| Context management                          |          |          |
| Scaling with repository size                |          |          |
| Security baseline                           |          |          |
| No public unauthenticated endpoint required |          |          |

---

# 13. Failure Modes & Recovery

Document the expected failure scenarios.

| Failure                       | Detection | Recovery | Human Intervention |
| ----------------------------- | --------- | -------- | ------------------ |
| Model endpoint unavailable    |           |          |                    |
| Context overflow              |           |          |                    |
| Tool call failure             |           |          |                    |
| File operation failure        |           |          |                    |
| Test failure                  |           |          |                    |
| Static check failure          |           |          |                    |
| Worker conflict               |           |          |                    |
| Git merge conflict            |           |          |                    |
| Invalid generated code        |           |          |                    |
| Deployment validation failure |           |          |                    |

---

# 14. Tradeoffs

Discuss the major tradeoffs of the recommended approach.

Consider:

* Complexity vs. flexibility
* Model quality vs. hardware requirements
* Parallelism vs. coordination complexity
* Automation vs. human control
* Context size vs. performance
* Reproducibility vs. LLM nondeterminism
* Local privacy vs. infrastructure complexity
* Setup time vs. long-term maintainability

---

# 15. Recommendation

Provide a clear recommendation.

The recommendation should answer:

1. Which candidate toolchain should be selected?
2. Why is it better suited to the requirements?
3. What are its main disadvantages?
4. What compromises are necessary?
5. Why are those compromises acceptable?
6. How does it compare against the rejected alternative?

### Recommended Solution

**Selected toolchain:** ______________________________

### Rationale

---

---

---

---

# 16. Required Deliverables

## 16.1 Synopsis

Produce a **7–10 page synopsis** covering:

* Candidate toolchains compared
* Architecture of the recommended workflow
* How each functional requirement is satisfied
* Tradeoffs
* Risks
* Failure modes
* Recommendation
* Rationale
* Review of another group's work

---

## 16.2 Setup Guide

Produce a short but complete setup guide that allows a third party to reproduce the workflow.

The guide must include:

### Prerequisites

* Operating system
* Required runtime
* Required tools
* Required hardware
* Git
* Local model servers

### Installation

Step-by-step installation instructions.

### Model Endpoints

Instructions for:

* Starting endpoint 1
* Starting endpoint 2
* Verifying both endpoints
* Configuring endpoint addresses
* Configuring model selection

### Toolchain Configuration

Explain:

* Configuration files
* Agent/role configuration
* Endpoint routing
* Model selection
* Environment variables

### Demo Workflow

The demo must produce:

* [ ] Architecture output
* [ ] At least one implemented feature
* [ ] Tests executed
* [ ] Test results
* [ ] Documentation updates
* [ ] Deployment validation

### Verification

Provide commands that allow a third party to verify the complete workflow.

---

# 17. Review of Another Group's Work

A review of another group's delivery is required.

## Group Reviewed

**Group:** ______________________________

## Toolchain / Approach

---

## Strengths

1. ---
2. ---
3. ---

## Weaknesses

1. ---
2. ---
3. ---

## Requirement Coverage

| Requirement              | Assessment | Comments |
| ------------------------ | ---------- | -------- |
| Multiple local endpoints |            |          |
| Open source              |            |          |
| Architecture             |            |          |
| Tech lead                |            |          |
| Implementation           |            |          |
| Testing & QA             |            |          |
| Documentation            |            |          |
| Deployment validation    |            |          |
| Predictability & control |            |          |
| Reproducibility          |            |          |
| Context management       |            |          |
| Security                 |            |          |

## Overall Assessment

---

---

## What We Would Adopt

---

## What We Would Change

---

---

# 18. Final Checklist

Before submitting, verify all requirements.

### Hard Requirements

* [ ] At least 2 separate local model endpoints
* [ ] Endpoint routing/switching is configuration-based
* [ ] Open-source tooling

### Functional Requirements

* [ ] Architecture artifacts
* [ ] Component decomposition
* [ ] Interface contracts
* [ ] Deployment topology
* [ ] ADRs
* [ ] Tech lead task breakdown
* [ ] Scope boundaries
* [ ] Acceptance criteria
* [ ] Dependency ordering
* [ ] At least 2 coding workers or equivalent parallel design
* [ ] Multi-file repository changes
* [ ] Tests created
* [ ] Tests executed
* [ ] Quality report
* [ ] Static checks
* [ ] Known risks/limitations
* [ ] README
* [ ] API documentation where relevant
* [ ] Runbook
* [ ] Design documentation
* [ ] Deployment validation

### Non-Functional Requirements

* [ ] Human control mechanism
* [ ] Git/version control
* [ ] Reviewable diffs or commits
* [ ] Reproducible workflow
* [ ] Context management strategy
* [ ] Strategy for large repositories/documentation
* [ ] Security baseline
* [ ] No requirement for publicly exposed unauthenticated model endpoint

### Deliverables

* [ ] 7–10 page synopsis
* [ ] At least 2 candidate toolchains compared
* [ ] Recommended solution
* [ ] Recommendation rationale
* [ ] Failure-mode analysis
* [ ] Tradeoff analysis
* [ ] Complete setup guide
* [ ] Demo workflow
* [ ] Architecture output
* [ ] Implemented feature
* [ ] Test results
* [ ] Updated documentation
* [ ] Deployment validation
* [ ] Review of another group's work
