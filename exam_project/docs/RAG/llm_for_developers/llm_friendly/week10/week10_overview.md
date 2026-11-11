# Week 10 — Agent orchestration and specification-driven development

Sources: `source/week10/Agent_Orchestration_Lesson (1).pdf`, 17 pages, and the accompanying `calculator-orchestration` project. See the [text of the slides](week10_source_agent_orchestration_lesson_1_pdf.md). The conversion reads the project as teaching material and does not run its agents or generated programs.

## Two agents and an orchestrator

The Coder writes the implementation and fixes problems reported by the Reviewer. The Reviewer writes tests, examines the results and delivers feedback. The orchestrator decides the order and the stop conditions. Separate roles and tools make the responsibility concrete; a shared model can still produce shared blind spots.

Orchestration covers responsibility, handoffs, dependencies and acceptance of results. The slides compare sequential, parallel, supervisor-driven and review-based patterns. The patterns have different costs in latency, coupling, control and feedback.

## A bounded review loop

The loop allows at most three returns to the Coder. A first attempt plus three revisions gives at most four implementation attempts. Approval can end it earlier. A failure at the limit ends with failure rather than one more attempt. An agent's internal tool loop has a different limit than the outer review loop.

Shared state includes, among other things, `attempt`, `feedback_returns`, `feedback`, `passed` and `status`. Private message history and shared workflow state are different things.

## The specification comes before the implementation

The teaching project organises requirements in `docs/requirements`, architecture in `docs/architecture` and detailed design in `docs/design`. The method is described as inspired by the Unified Process, BDD, DDD and Specification-Driven Development. One bounded feature is implemented and reviewed at a time.

The Draw.io diagrams are converted into labels and edges with their endpoints. They describe both the small console calculator and its development tool; the orchestration components are not extra runtime components of the finished calculator.

## What counts as success?

The README and slides require approval of the current files, passing generated tests and fixed acceptance checks, and re-verification that the implementation still matches the reviewed version. An agent failure must not be hidden as success. Passing tests are evidence, not a general proof of correctness.

The examples distinguish between a scripted demo and a real local model call. Neither was run during the conversion. The delivered raw folder refers to individual files such as `selftest.py` and `instructor/VALIDATION.md` that are not present in the upload; these have not been invented or recreated.

## Review questions

1. Why separate the Coder and the Reviewer when they share a model?
2. How many attempts do three feedback returns give?
3. What must cross a handoff as documentation?
4. Why are tests required again after review?
5. What is the difference between the architecture of the target program and the orchestration of the development tool?