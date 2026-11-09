<!-- studygraph:converted-source:v1 -->
# Uge 10 — deployment (drawio)

Kilde: [week10/calculator-orchestration/docs/architecture/deployment.drawio](../../source/week10/calculator-orchestration/docs/architecture/deployment.drawio).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Diagram — Single computer deployment

Labels og forbindelser fra diagrammets XML; placering og grafik er ikke gengivet.

- Element: Python process LangGraph outer workflow Coder + reviewer LangChain agents

- Element: Ollama localhost:11434 One shared local model CPU inference, sequential requests

- Element: Repository inputs (read only) Stories + acceptance criteria Draw.io models

- Element: Run directory calculator.py + test_calculator.py logs, snapshots, final report

- Forbindelse: Python process
LangGraph outer workflow
Coder + reviewer LangChain agents → Ollama localhost:11434
One shared local model
CPU inference, sequential requests. model requests

- Forbindelse: Repository inputs (read only)
Stories + acceptance criteria
Draw.io models → Python process
LangGraph outer workflow
Coder + reviewer LangChain agents. design context

- Forbindelse: Python process
LangGraph outer workflow
Coder + reviewer LangChain agents → Run directory
calculator.py + test_calculator.py
logs, snapshots, final report. tools and test execution
