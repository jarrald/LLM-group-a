<!-- studygraph:converted-source:v1 -->
# Uge 10 — Agent_Orchestration_Lesson (1) (pdf)

Kilde: [week10/Agent_Orchestration_Lesson (1).pdf](../../source/week10/Agent_Orchestration_Lesson%20%281%29.pdf).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Side 1

Agent orchestration

01

Specification-based development

Python · LangGraph · LangChain · Ollama

LLM for Developers

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 2

Exam-project questions

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 3

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 4

Two agents and an orchestrator

04

Coder: writes the code and fixes problems reported by the reviewer.

Reviewer: checks the code, runs tests and gives feedback.

Orchestrator: decides which agent runs next and when the process stops.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 5

What orchestration adds

05

Responsibilities: which agent owns each task?

Handoffs: what information and evidence cross the boundary?

Coordination: what must complete before the next task?

Completion: who accepts results and who stops the workflow?

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 6

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 7

Two agents need a reason

07

Coder owns implementation. Reviewer owns tests and findings.

Separate permissions make responsibilities concrete.

Sharing a model saves resources but can preserve shared blind spots.

Extra handoffs cost time and tokens.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 8

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 9

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 10

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 11

Setup: Python environment

11

Windows PowerShell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt

Linux / macOS
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt

Use the virtual-environment Python executable for the remaining commands.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 12

Setup: model and tool-call check

12

ollama pull qwen2.5-coder:1.5b
ollama list
python check_environment.py

Expected: echo_number(number=7)
Then: PASS

A successful smoke test checks connectivity and one tool call.
It does not establish coding or review quality.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 13

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 14

Run the workflow

14

python selftest.py

python main.py --demo --allow-local-execution

python main.py --allow-local-execution

The first run is scripted. The second uses the local model.
Both execute tests and record graph transitions.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 15

The routing decision

15

if state["passed"]:
    return "finish"

if state["feedback_returns"] < 3:
    return "feedback"

return "finish"

The feedback node increments the counter before returning to coder.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 16

What counts as success?

16

Reviewer submits approval for the current files.

Generated tests and fixed acceptance checks both pass.

Fresh verification matches the reviewed implementation.

No agent invocation error occurred in the attempt.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 17

Run the generated calculator

17

python runs/YOUR_RUN_ID/calculator.py

First number: 12
Operation (+, -, *, /): /
Second number: 4
Result: 3.0

Then try division by zero, an unsupported operator and invalid input.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.
