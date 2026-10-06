# runB_native_v2 - STALLED (evidence preserved)

Configuration: --config config/endpoints.crewai.yaml --run-id runB_native_v2
Native features enabled: memory=True (+ native Ollama embedder), output_file,
create_directory, output_pydantic, guardrail, async_execution.

Outcome: the crew started, printed its routing table, and then produced NO task
output and NO further log lines for ~18 minutes. Ollama showed no resident model
and no request activity (/api/ps empty on 11435; architect idle on 11434), i.e.
the process was not waiting on the model - it was hung inside CrewAI.
stdout was redirected to runs/runB_native_v2_stdout.txt, stderr to
runs/runB_native_v2_stderr.txt (0 bytes).

Isolated probe result (candidate_b_crewai/_probe_native.py): a SINGLE-task crew
with memory=True completed successfully, so native memory itself works; it is the
combination with the full multi-task/async crew that hangs.

Conclusion recorded in docs/synopsis.md: Crew(memory=True) is native but not
reliable in a multi-task local crew; it also attaches memory tools to every
agent, which requires tool-capable models.
