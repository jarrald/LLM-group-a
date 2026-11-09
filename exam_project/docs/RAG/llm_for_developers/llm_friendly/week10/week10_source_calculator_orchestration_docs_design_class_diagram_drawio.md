<!-- studygraph:converted-source:v1 -->
# Week 10 — class-diagram (drawio)

Source: [week10/calculator-orchestration/docs/design/class-diagram.drawio](../../source/week10/calculator-orchestration/docs/design/class-diagram.drawio).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

## Diagram — Calculator class design

Labels and edges from the diagram XML; placement and graphics are not reproduced.

- Element: ConsoleApp ------------------------ - calculator: Calculator ------------------------ + __init__(calculator: Calculator) + run() -> int

- Element: Calculator ------------------------ + calculate(a: float, operator: str, b: float) -> float Raises ValueError for invalid operation, zero divisor or non-finite values

- Element: Module entry point if __name__ == "__main__": raise SystemExit( ConsoleApp(Calculator()).run())

- Edge: ConsoleApp
------------------------
- calculator: Calculator
------------------------
+ __init__(calculator: Calculator)
+ run() -> int → Calculator
------------------------
+ calculate(a: float, operator: str,
    b: float) -> float
Raises ValueError for invalid operation,
zero divisor or non-finite values. uses 1 (constructor injection)

- Edge: Module entry point
if __name__ == "__main__":
    raise SystemExit(
        ConsoleApp(Calculator()).run()) → ConsoleApp
------------------------
- calculator: Calculator
------------------------
+ __init__(calculator: Calculator)
+ run() -> int. constructs and runs
