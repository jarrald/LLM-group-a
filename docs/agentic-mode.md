# Agentic mode — tool calling, file operations, tests and context

Analysis mode (`run_workflow`) lets every agent answer with plain text. Agentic
mode (`run_agentic_workflow`) lets selected agents **call tools**, so the workflow
can produce real multi-file changes and run tests itself. It is the part that
satisfies the assignment's *implementation*, *testing & quality*, *predictability*
and *context management* requirements.

## Running it

```powershell
# Dry run: agents propose file changes as unified diffs, nothing is written or run
python .\model\ollama_workflow.py --agentic "<requirement>"

# Approve and apply: write files and run allowlisted commands
python .\model\ollama_workflow.py --agentic --apply "<requirement>"

# Custom sandbox directory
python .\model\ollama_workflow.py --agentic --apply --workspace workspace\demo "<requirement>"
```

The same is available over HTTP: `POST /api/workflow` with
`{"requirement": "...", "mode": "agentic", "apply": true}`.

## Tool calling

Agents talk to Ollama's `/api/chat` endpoint with a `tools` array. Four tools are
exposed: `list_files`, `read_file`, `write_file` and `run_command`. `run_tool_agent`
loops until the model answers without a tool call, or until `MAX_AGENT_ROUNDS`.

Local models differ in how they emit tool calls:

| Model | Emits structured `tool_calls` | Fallback needed |
| --- | --- | --- |
| `llama3.1:8b`, `qwen3.5:9b` | yes | no |
| `qwen2.5-coder:7b`, `llama3.2:3b` | no (writes the call as JSON text) | yes |

When the structured field is empty, `_extract_tool_calls_from_content` recovers a
call that the model wrote as JSON in its text (including fenced ` ```json ` blocks
and the `arguments`/`parameters` key variants). Only known tool names are accepted.

## File operations

All file work happens inside the sandbox (`WORKSPACE_DIR`, default `workspace/`).
`ToolRuntime._resolve` rejects any path that escapes the sandbox, so an agent
cannot write outside it. Every `write_file` produces a unified diff; with `--apply`
the file is written, otherwise only the diff is recorded.

## Test running

`run_command` executes a command with `subprocess` (no shell) in the sandbox and
records its exit code and output. It is restricted to an allowlist:

```text
python -m pytest | python -m unittest | python -m ruff | python -m mypy | python -m compileall | pytest | ruff | mypy
```

Without `--apply`, commands are only *planned* (recorded, not executed).

## Context management

The functional agents run **in order**, and each one receives the previous
artifacts as explicit context (artifact handoff) instead of everyone seeing only
the original requirement:

```text
architecture -> tech_lead -> implementation -> testing_quality -> documentation -> deployment
                                                                        |
                                            predictability, reproducibility, context_management, security (parallel)
```

Each handoff is bounded by `CONTEXT_BUDGET` characters and logged in the result's
`handoffs` list (with a `truncated` flag), so context loss is never silent. When a
repository or document set grows, raise `CONTEXT_BUDGET`; the truncation marker
always shows what was dropped.

## Predictability & control

Agentic mode defaults to a **plan + diff** flow: nothing is written or executed
without `--apply`, and every change is shown as a reviewable diff. This is the
"plan + diffs for review before execution" control mechanism from the assignment.

## Failure modes & recovery

| Failure | Detection | Recovery |
| --- | --- | --- |
| Model does not emit `tool_calls` | empty `tool_calls` field | content fallback parser recovers the call |
| Model lacks tool support entirely | no tool call in content either | agent degrades to text; the round ends |
| Agent loops on tool calls | `MAX_AGENT_ROUNDS` reached | loop stops; partial result is kept |
| Path escapes the sandbox | `ValueError` in `_resolve` | call is rejected with an error string |
| Unsafe command | allowlist check | command is rejected; nothing runs |
| Context grows too large | `_bounded` truncation | artifact is truncated with an explicit marker |
