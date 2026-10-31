<!-- studygraph:converted-source:v1 -->
# Uge 10 — class-diagram (drawio)

Kilde: [week10/calculator-orchestration/docs/design/class-diagram.drawio](../../source/week10/calculator-orchestration/docs/design/class-diagram.drawio).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Diagram — Calculator class design

Labels og forbindelser fra diagrammets XML; placering og grafik er ikke gengivet.

- Element: ConsoleApp ------------------------ - calculator: Calculator ------------------------ + __init__(calculator: Calculator) + run() -> int

- Element: Calculator ------------------------ + calculate(a: float, operator: str, b: float) -> float Raises ValueError for invalid operation, zero divisor or non-finite values

- Element: Module entry point if __name__ == "__main__": raise SystemExit( ConsoleApp(Calculator()).run())

- Forbindelse: ConsoleApp
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

- Forbindelse: Module entry point
if __name__ == "__main__":
    raise SystemExit(
        ConsoleApp(Calculator()).run()) → ConsoleApp
------------------------
- calculator: Calculator
------------------------
+ __init__(calculator: Calculator)
+ run() -> int. constructs and runs
