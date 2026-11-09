<!-- studygraph:converted-source:v1 -->
# Week 10 — orchestration (drawio)

Source: [week10/calculator-orchestration/docs/architecture/orchestration.drawio](../../source/week10/calculator-orchestration/docs/architecture/orchestration.drawio).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

## Diagram — Bounded coder and reviewer orchestration

Labels and edges from the diagram XML; placement and graphics are not reproduced.

- Element: Read immutable design returns = 0

- Element: Coder write calculator.py

- Element: Reviewer / tester read code, write tests, run tests

- Element: Review accepts AND fresh checks pass?

- Element: SUCCESS write report and stop

- Element: returns < 3?

- Element: Increment returns Send latest feedback to coder

- Element: FAILURE write unresolved findings

- Edge: Read immutable design
returns = 0 → Coder
write calculator.py. 

- Edge: Coder
write calculator.py → Reviewer / tester
read code, write tests, run tests. 

- Edge: Reviewer / tester
read code, write tests, run tests → Review accepts AND
fresh checks pass?. 

- Edge: Review accepts AND
fresh checks pass? → SUCCESS
write report and stop. yes

- Edge: Review accepts AND
fresh checks pass? → returns < 3?. no

- Edge: returns < 3? → Increment returns
Send latest feedback to coder. yes

- Edge: Increment returns
Send latest feedback to coder → Coder
write calculator.py. 

- Edge: returns < 3? → FAILURE
write unresolved findings. no
