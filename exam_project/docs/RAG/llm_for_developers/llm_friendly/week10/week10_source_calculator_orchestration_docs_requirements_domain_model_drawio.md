<!-- studygraph:converted-source:v1 -->
# Uge 10 — domain-model (drawio)

Kilde: [week10/calculator-orchestration/docs/requirements/domain-model.drawio](../../source/week10/calculator-orchestration/docs/requirements/domain-model.drawio).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Diagram — Calculator domain model

Labels og forbindelser fra diagrammets XML; placering og grafik er ikke gengivet.

- Element: Calculation

- Element: Operand Finite numeric value

- Element: Operator + - * /

- Element: Result Finite numeric value

- Element: Calculation error Zero divisor / unsupported operator Non-finite number or result

- Forbindelse: Calculation → Operand
Finite numeric value. has 2

- Forbindelse: Calculation → Operator
+  -  *  /. uses 1

- Forbindelse: Calculation → Result
Finite numeric value. produces 1 on success

- Forbindelse: Calculation → Calculation error
Zero divisor / unsupported operator
Non-finite number or result. produces 1 on failure
