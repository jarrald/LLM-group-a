<!-- studygraph:converted-source:v1 -->
# Week 10 — deployment (drawio)

Source: [week10/calculator-orchestration/docs/architecture/deployment.drawio](../../source/week10/calculator-orchestration/docs/architecture/deployment.drawio).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

## Diagram — Single computer deployment

Labels and edges from the diagram XML; placement and graphics are not reproduced.

- Element: Python process LangGraph outer workflow Coder + reviewer LangChain agents

- Element: Ollama localhost:11434 One shared local model CPU inference, sequential requests

- Element: Repository inputs (read only) Stories + acceptance criteria Draw.io models

- Element: Run directory calculator.py + test_calculator.py logs, snapshots, final report

- Edge: Python process
LangGraph outer workflow
Coder + reviewer LangChain agents → Ollama localhost:11434
One shared local model
CPU inference, sequential requests. model requests

- Edge: Repository inputs (read only)
Stories + acceptance criteria
Draw.io models → Python process
LangGraph outer workflow
Coder + reviewer LangChain agents. design context

- Edge: Python process
LangGraph outer workflow
Coder + reviewer LangChain agents → Run directory
calculator.py + test_calculator.py
logs, snapshots, final report. tools and test execution
