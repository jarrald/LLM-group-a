# Setup and classroom run guide

## 1. Prepare the computer
Use Python 3.11 or 3.12, Ollama, an editor, and draw.io desktop or https://app.diagrams.net/.
The supplied package was checked on Python 3.12. No GPU is required. Total RAM has not been
specified, so performance and fit must be checked on the weakest actual student computer.
Install Python from https://www.python.org/downloads/ and Ollama from https://ollama.com/download.
On Linux follow Ollama's official installation guide. Windows/macOS can use their installers.
Keep Ollama running. Its default endpoint is http://localhost:11434.

Use a disposable VM for running agent-generated Python. It executes with your user permissions.
No Docker, cloud hosting, paid subscriptions or API keys are required by this example.

## 2. Open the project and create a virtual environment
Extract the ZIP, open a terminal in `calculator-orchestration`, and verify `python --version`.

Windows PowerShell (activation is unnecessary):
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe selftest.py
```

Linux/macOS:
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python selftest.py
```
If Ubuntu reports that venv is unavailable, install its python3-venv package first.
Use the relevant virtual-environment Python executable wherever `python` appears below.
`requirements.txt` pins direct dependencies; `requirements-lock.txt` also pins transitive
versions from the validated environment. If your OS/Python cannot install the lock, use the
direct file and re-run selftest; do not assume an untested dependency combination works.

## 3. Download and verify one small model
```bash
ollama pull qwen2.5-coder:1.5b
ollama list
python check_environment.py
```
The 1.5B Q4_K_M model download is about 986 MB; runtime RAM is greater than the download size.
This is a small-model candidate, not a promise of reliable code generation or tool calling.
The smoke test must show a valid echo_number tool call. It is necessary but not sufficient.
The Python configuration forces CPU inference with num_gpu=0, uses four threads, and requests
8192 context tokens. Only one model call runs at a time. The same weights serve both agents.
If you have more RAM and the candidate performs poorly, test `qwen2.5-coder:3b`:
```bash
ollama pull qwen2.5-coder:3b
python check_environment.py --model qwen2.5-coder:3b
```
This larger tag is about 1.9 GB to download. Do not assume it fits every machine.
Download models before class. First model loading is slower than subsequent requests.
Use `ollama ps` and your OS task manager to inspect model residency, CPU and RAM.

## 4. Inspect the design inputs
Open these files with draw.io (File > Open From > Device):
- `docs/requirements/domain-model.drawio`: conceptual operands, operation, result and errors.
- `docs/design/class-diagram.drawio`: Calculator and ConsoleApp signatures and dependency.
- `docs/design/calculator-activity.drawio`: successful and unsuccessful console execution.
- `docs/architecture/orchestration.drawio`: coordination and the exact retry boundary.
- `docs/architecture/deployment.drawio`: one machine, one model, two logical agents.

Read `docs/requirements/user-stories.md` and `docs/architecture/calculator-architecture.md`. Keep the public interfaces and AC identifiers consistent.
The domain model is conceptual; it does not require a Python class for every concept.
To see precisely what agents receive:
```bash
python design_reader.py
```
The reader extracts labels and edges from uncompressed draw.io XML, without vision or OCR.
The supplied files use plain-text labels. When editing, retain uncompressed XML and plain text
labels (disable formatted text if necessary). If draw.io saves compressed data, export XML with
compression disabled and save over the .drawio file, then run design_reader.py again.
The orchestration/deployment diagrams are teaching documentation; the worker context receives
the domain, class and calculator-activity diagrams, the calculator architecture notes,
and all stories and acceptance criteria.

## 5. Verify execution plumbing without waiting for a model
```bash
python main.py --demo --allow-local-execution
python main.py --demo-fail --allow-local-execution
```
These are SCRIPTED runs. They do not call an LLM or measure model quality.
The first deliberately writes an addition bug, detects it with real tests, then fixes it:
expect success at attempt 2 with 1 feedback return. The second preserves the bug:
expect failure at attempt 4 with 3 feedback returns, and process exit code 1.
Both create source, tests, traces and final reports in separate runs directories.

## 6. Run the actual two-agent workflow
```bash
python main.py --allow-local-execution
```
Or use the larger candidate you already downloaded:
```bash
python main.py --model qwen2.5-coder:3b --allow-local-execution
```
Follow `agent_start`, file-tool actions and graph transitions in the console. Detailed messages,
actual test output and elapsed times are in events.jsonl. The run may legitimately fail.
Tools are intentionally narrow: coder can write only calculator.py; reviewer can write only
test_calculator.py. Neither has a tool to modify the authoritative design.
Subprocess execution itself is not a security boundary (see README).

## 7. Run and inspect the generated calculator
Copy the exact path printed by main.py, for example:
```bash
python runs/YOUR_RUN_ID/calculator.py
```
Enter 12, /, 4 on separate prompts. Expect Result: 3 or 3.0. Try 1, /, 0 and then invalid input.
Inspect the run's report.json, generated tests, and attempt-*/review.json.
If the outcome is failure, the file may still exist; its existence is not evidence of success.
For a known working manual demonstration independent of model output:
```bash
python instructor/reference_calculator.py
```

## 8. Troubleshooting
| Symptom | Action |
|---|---|
| Connection refused | Start Ollama; check localhost:11434. Use --base-url only for your intended endpoint. |
| Model not found | Pull the exact tag used by --model. |
| No tool calls / only code in chat | Check smoke test. Try the larger candidate if RAM allows; otherwise use scripted demo. |
| Slow or swapping | Close other applications; lower --threads to 2 if needed; use the 1.5B tag. |
| Context too small | Keep prompts/feedback concise. --context 4096 reduces RAM but may truncate useful context; revalidate. |
| GraphRecursionError inside an agent | Model used too many tool steps; inspect trace. This is distinct from the three feedback returns. |
| Syntax / missing class / failed tests | Inspect reviewer feedback and code snapshots; these are valid exercise findings. |
| Tests time out | Investigate generated code. Each test-suite child has a 30-second timeout. |
| All checks pass but review rejects | Inspect design findings. LLM review may be correct or mistaken. Discuss the evidence. |

Model HTTP calls have a 300-second timeout. There is no promised wall-clock completion time.
Do not spend the entire exercise waiting: the teacher can use scripted runs after a slow smoke test.

## References
- LangGraph: https://docs.langchain.com/oss/python/langgraph/overview
- LangChain agents: https://docs.langchain.com/oss/python/langchain/agents
- ChatOllama: https://docs.langchain.com/oss/python/integrations/chat/ollama
- Model: https://ollama.com/library/qwen2.5-coder:1.5b
- Ollama: https://docs.ollama.com/
- draw.io: https://www.drawio.com/doc/
