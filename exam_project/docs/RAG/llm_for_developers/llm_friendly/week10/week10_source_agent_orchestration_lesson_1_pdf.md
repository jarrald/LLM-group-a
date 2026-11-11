<!-- studygraph:converted-source:v1 -->
# Week 10 — Agent_Orchestration_Lesson (1) (pdf)

Source: [week10/Agent_Orchestration_Lesson (1).pdf](../../source/week10/Agent_Orchestration_Lesson%20%281%29.pdf).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

## Page 1

Agent orchestration

01

Specification-based development

Python · LangGraph · LangChain · Ollama

LLM for Developers

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 2

Exam-project questions

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 3

Agent, Agentic and Orchestration

03

Course concept
What it describes

LLM Agent
The LLM chooses how to progress towards a goal.

Agentic LLM
Developer-defined transitions govern execution.

Agent orchestration
Coordination across agents and tasks.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 4

Two agents and an orchestrator

04

Coder: writes the code and fixes problems reported by the reviewer.

Reviewer: checks the code, runs tests and gives feedback.

Orchestrator: decides which agent runs next and when the process stops.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 5

What orchestration adds

05

Responsibilities: which agent owns each task?

Handoffs: what information and evidence cross the boundary?

Coordination: what must complete before the next task?

Completion: who accepts results and who stops the workflow?

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 6

Coordination patterns

06

Pattern
Control and trade-off

Sequential
Known order and simple dependencies. Waiting is explicit.

Parallel
Independent tasks run together. Results need merging.

Supervisor
A coordinator delegates dynamically. Decisions need inspection.

Review loop
Feedback drives revision. Requires an explicit limit.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 7

Two agents need a reason

07

Coder owns implementation. Reviewer owns tests and findings.

Separate permissions make responsibilities concrete.

Sharing a model saves resources but can preserve shared blind spots.

Extra handoffs cost time and tokens.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 8

Specification-based development

Inspired by Unified Process, BDD, DDD and Specification-Driven Development.

Repository folder
Specification documents

docs/requirements
User stories or use cases, domain models
and acceptance requirements

docs/architecture
System structure and architectural decisions
using UML, C4 or other suitable models

docs/design
Detailed UML design, such as classes
and interactions

Give the agent the repository, connecting requirements to architecture and design.

Implement and review one feature at a time.

08

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 9

The bounded review loop

09

Coder
implementation

Reviewer / tester

review + tests
Acceptance gate

Feedback to coder
maximum 3 returns

Failure and returns < 3
Pass: finish with 
SUCCESS

Fail at limit: finish with 
FAILURE

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 10

Shared state and private context

10

State / context
Purpose

attempt
Counts coding attempts, starting at 1

feedback_returns
Counts handoffs back to coder, from 0 to 3

feedback
Latest findings and actual test evidence

passed / status
Controls routing and records the final outcome

Private agent messages
Fresh per invocation. Stored in the run trace

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 11

Setup: Python environment

11

Windows PowerShell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt

Linux / macOS
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt

Use the virtual-environment Python executable for the remaining commands.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 12

Setup: model and tool-call check

12

ollama pull qwen2.5-coder:1.5b
ollama list
python check_environment.py

Expected: echo_number(number=7)
Then: PASS

A successful smoke test checks connectivity and one tool call.
It does not establish coding or review quality.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 13

Agent tools and boundaries

13

Coder
Reviewer / tester

Read implementation and tests
Read implementation and tests

Write calculator.py
Write test_calculator.py

Finish after saving
Run real tests and inspect results

Receive latest feedback
Submit an approving or rejecting review

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 14

Run the workflow

14

python selftest.py

python main.py --demo --allow-local-execution

python main.py --allow-local-execution

The first run is scripted. The second uses the local model.
Both execute tests and record graph transitions.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 15

The routing decision

15

if state["passed"]:
    return "finish"

if state["feedback_returns"] < 3:
    return "feedback"

return "finish"

The feedback node increments the counter before returning to coder.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 16

What counts as success?

16

Reviewer submits approval for the current files.

Generated tests and fixed acceptance checks both pass.

Fresh verification matches the reviewed implementation.

No agent invocation error occurred in the attempt.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 17

Run the generated calculator

17

python runs/YOUR_RUN_ID/calculator.py

First number: 12
Operation (+, -, *, /): /
Second number: 4
Result: 3.0

Then try division by zero, an unsupported operator and invalid input.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.
