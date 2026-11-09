<!-- studygraph:converted-source:v1 -->
# Week 10 — domain-model (drawio)

Source: [week10/calculator-orchestration/docs/requirements/domain-model.drawio](../../source/week10/calculator-orchestration/docs/requirements/domain-model.drawio).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

## Diagram — Calculator domain model

Labels and edges from the diagram XML; placement and graphics are not reproduced.

- Element: Calculation

- Element: Operand Finite numeric value

- Element: Operator + - * /

- Element: Result Finite numeric value

- Element: Calculation error Zero divisor / unsupported operator Non-finite number or result

- Edge: Calculation → Operand
Finite numeric value. has 2

- Edge: Calculation → Operator
+  -  *  /. uses 1

- Edge: Calculation → Result
Finite numeric value. produces 1 on success

- Edge: Calculation → Calculation error
Zero divisor / unsupported operator
Non-finite number or result. produces 1 on failure
