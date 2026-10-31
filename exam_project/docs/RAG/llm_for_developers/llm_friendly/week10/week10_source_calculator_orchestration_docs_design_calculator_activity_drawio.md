<!-- studygraph:converted-source:v1 -->
# Uge 10 — calculator-activity (drawio)

Kilde: [week10/calculator-orchestration/docs/design/calculator-activity.drawio](../../source/week10/calculator-orchestration/docs/design/calculator-activity.drawio).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Diagram — Console calculation activity

Labels og forbindelser fra diagrammets XML; placering og grafik er ikke gengivet.

- Element: Start console

- Element: Read first number, operator, second number and parse numbers

- Element: Parsing succeeded?

- Element: Calculator.calculate

- Element: Calculation succeeded?

- Element: Print Result Exit 0

- Element: Print Error: Invalid number Exit 1

- Element: Print Error: domain message Exit 1

- Forbindelse: Start console → Read first number, operator,
second number and parse numbers. 

- Forbindelse: Read first number, operator,
second number and parse numbers → Parsing
succeeded?. 

- Forbindelse: Parsing
succeeded? → Calculator.calculate. yes

- Forbindelse: Parsing
succeeded? → Print Error: Invalid number
Exit 1. no

- Forbindelse: Calculator.calculate → Calculation
succeeded?. 

- Forbindelse: Calculation
succeeded? → Print Result
Exit 0. yes

- Forbindelse: Calculation
succeeded? → Print Error: domain message
Exit 1. ValueError
