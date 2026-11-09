<!-- studygraph:converted-source:v1 -->
# Uge 10 — orchestration (drawio)

Kilde: [week10/calculator-orchestration/docs/architecture/orchestration.drawio](../../source/week10/calculator-orchestration/docs/architecture/orchestration.drawio).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Diagram — Bounded coder and reviewer orchestration

Labels og forbindelser fra diagrammets XML; placering og grafik er ikke gengivet.

- Element: Read immutable design returns = 0

- Element: Coder write calculator.py

- Element: Reviewer / tester read code, write tests, run tests

- Element: Review accepts AND fresh checks pass?

- Element: SUCCESS write report and stop

- Element: returns < 3?

- Element: Increment returns Send latest feedback to coder

- Element: FAILURE write unresolved findings

- Forbindelse: Read immutable design
returns = 0 → Coder
write calculator.py. 

- Forbindelse: Coder
write calculator.py → Reviewer / tester
read code, write tests, run tests. 

- Forbindelse: Reviewer / tester
read code, write tests, run tests → Review accepts AND
fresh checks pass?. 

- Forbindelse: Review accepts AND
fresh checks pass? → SUCCESS
write report and stop. yes

- Forbindelse: Review accepts AND
fresh checks pass? → returns < 3?. no

- Forbindelse: returns < 3? → Increment returns
Send latest feedback to coder. yes

- Forbindelse: Increment returns
Send latest feedback to coder → Coder
write calculator.py. 

- Forbindelse: returns < 3? → FAILURE
write unresolved findings. no
