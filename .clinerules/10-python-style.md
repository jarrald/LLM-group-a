# Python & project conventions (always active)

- **Target:** Python 3.9+ (locally tested on 3.14). Windows 11 + PowerShell (`pwsh`).
- **Single-file design:** keep the Flask app, inline HTML frontend, `AGENTS` registry and
  `main()` together in `model/ollama_workflow.py`. Do not split it up unless asked.
- **Language:** comments, prompts and user-facing strings in **Danish**; identifiers and
  docstrings in **English**.
- **Configuration:** read everything through `os.getenv("<NAME>", <default>)`
  (`OLLAMA_URL`, `ARCHITECT_ENDPOINT`, `WORKER_ENDPOINT`, `ARCHITECT_MODEL`,
  `WORKER_MODEL`, `MAX_PARALLEL_AGENTS`). Never hardcode an endpoint or model name.
- **Dependencies:** standard library first (`urllib.request` talks to Ollama). Only Flask
  is a runtime dependency — if you add another, update `requirements.txt`.
- **Typing:** annotate functions; the codebase uses PEP 585 generics (`dict[str, object]`,
  `list[...]`). Keep `main() -> int` and the `if __name__ == "__main__":` guard.
- **Formatting:** 4-space indent, double quotes, no trailing whitespace. Match the
  existing file's style rather than reformatting it.
- **Verify:** run `python .\model\ollama_workflow.py "<requirement>"` (or `--web`) and
  report the exact command + result. Do not claim success without running it.
