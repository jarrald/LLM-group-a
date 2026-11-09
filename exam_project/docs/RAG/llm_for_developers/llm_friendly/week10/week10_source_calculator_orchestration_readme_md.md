<!-- studygraph:converted-source:v1 -->
# Uge 10 — README (md)

Kilde: [week10/calculator-orchestration/README.md](../../source/week10/calculator-orchestration/README.md).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

### Agent orchestration: Calculator development

Python + LangGraph + LangChain + Ollama. One computer, CPU-only baseline, one shared model.
No paid API or LangSmith account is required. Download/install requires internet access.

Start with [SETUP.md](SETUP.md). This is a complete starter repository; initialise Git if desired.
The live agents generate the calculator. The instructor reference is separate and is not fed to them.

#### Repository map
- `docs/requirements/user-stories.md`: authoritative stories and AC-01 through AC-10.
- `docs/**/*.drawio`: editable uncompressed diagrams, directly readable in draw.io.
- `design_reader.py`: extracts model labels AND relationship endpoints for text-only agents.
- `workflow.py`: outer LangGraph state, transitions and three-return limit.
- `agents.py`: two LangChain agents with different instructions and tools, same Ollama model.
- `agent_tools.py`: role-specific file tools, fixed test runner and review submission.
- `main.py`: CLI, new run directories, trace, attempt snapshots and final report.
- `check_environment.py`: connection and tool-calling smoke test.
- `checks/`: fixed acceptance evidence owned by the teacher.
- `selftest.py`: offline orchestration tests.
- `instructor/`: reference calculator, scripted demo test fixture and teacher guide.
- `demo.py`: explicitly scripted fallback, not an LLM run.

#### Architecture and outcome
Coder writes `calculator.py`. Reviewer writes `test_calculator.py`, runs tests, then submits findings.
LangGraph controls sequencing and returns feedback at most three times. Initial attempt plus
three revisions means at most four coding attempts and four review rounds. A successful review
can stop earlier. A failure at attempt four finishes with failure, not an additional retry.

Success requires a recorded approving review, matching current file fingerprints, passing
generated tests, passing fixed acceptance checks, and no agent invocation error in that attempt.
The fixed checks are re-run after the reviewer finishes. Passing tests is evidence, not proof.
An agent's tool-loop recursion limit is separate from the three feedback returns.
Model timeouts and infrastructure errors are reported; a broken environment should be fixed
before class rather than left to consume the revision budget.

#### Generated files
Each run creates `runs/<timestamp>/` with source, tests, JSONL events, attempt snapshots,
and `report.json`. The final console output prints the exact command for running the calculator.
Old runs are preserved. No resume/checkpoint feature is implied by these logs.

#### Course terminology
LLM Agent: model chooses how to progress. Agentic LLM: developer-defined transitions govern
execution. Orchestration: coordination of agents/tasks. These are related dimensions.
Here each worker chooses tools while the outer code enforces order and limits.
This is the course taxonomy, not a claim that industry uses these labels uniformly.

#### Execution boundary
The local test runner executes generated Python with the current user's permissions.
Narrow tool paths and timeouts are not a sandbox. Use a disposable teaching VM without
credentials or unrelated files. `--allow-local-execution` acknowledges this mode.
Agent-written Python could bypass tool restrictions if malicious; this is not a hardened service.

#### Validation status
See `instructor/VALIDATION.md` for actual checks and remaining live-model limitations.

#### Specification-based development
Steffen's method is inspired by Unified Process, Behaviour-Driven Development, Domain-Driven Design and Specification-Driven Development.
Prepare the repository before asking the agent to implement a feature:
- `docs/requirements`: user stories or use cases, domain model and acceptance requirements.
- `docs/architecture`: system structure and architectural decisions, using suitable UML/C4 models.
- `docs/design`: detailed UML design that connects the requirements to the implementation.
Give the agent the repository and a clearly bounded feature assignment. Implement and review
one feature at a time. The selected feature in this small demonstration is the console calculator;
US-01 and US-02 describe its arithmetic and console behaviour. The demo is a bounded
feature implementation loop, not a backlog scheduler.
