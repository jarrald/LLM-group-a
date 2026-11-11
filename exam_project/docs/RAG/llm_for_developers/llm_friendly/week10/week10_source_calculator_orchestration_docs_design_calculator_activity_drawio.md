<!-- studygraph:converted-source:v1 -->
# Week 10 — calculator-activity (drawio)

Source: [week10/calculator-orchestration/docs/design/calculator-activity.drawio](../../source/week10/calculator-orchestration/docs/design/calculator-activity.drawio).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

## Diagram — Console calculation activity

Labels and edges from the diagram XML; placement and graphics are not reproduced.

- Element: Start console

- Element: Read first number, operator, second number and parse numbers

- Element: Parsing succeeded?

- Element: Calculator.calculate

- Element: Calculation succeeded?

- Element: Print Result Exit 0

- Element: Print Error: Invalid number Exit 1

- Element: Print Error: domain message Exit 1

- Edge: Start console → Read first number, operator,
second number and parse numbers. 

- Edge: Read first number, operator,
second number and parse numbers → Parsing
succeeded?. 

- Edge: Parsing
succeeded? → Calculator.calculate. yes

- Edge: Parsing
succeeded? → Print Error: Invalid number
Exit 1. no

- Edge: Calculator.calculate → Calculation
succeeded?. 

- Edge: Calculation
succeeded? → Print Result
Exit 0. yes

- Edge: Calculation
succeeded? → Print Error: domain message
Exit 1. ValueError
