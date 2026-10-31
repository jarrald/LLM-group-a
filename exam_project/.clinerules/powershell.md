# Windows PowerShell execution rules

This workspace runs on **Windows 11 + PowerShell 7 (`pwsh`)** inside VS Code. Every
command you emit must be paste-able into PowerShell and execute unchanged.

> Reference: the longer version of these rules lives in the parent repository at
> `..\.clinerules\powershell.md`. It is not loaded for this workspace; this file is the
> compact, binding summary.

## Hard rules

- Never wrap a command in quotes: `python script.py`, not `'python script.py'`.
- Never emit Bash: no `&&`, `||`, `export`, `source`, `chmod`, `rm -rf`, `cp`, `mv`,
  `touch`, `cat >`, `ls -la`, `./script.sh`, `bash -c`, `$'...'`.
- Chain commands with `;`, not `&&`.
- Never use `curl`; use `Invoke-WebRequest` / `Invoke-RestMethod`.
- Use raw strings for Windows paths inside Python (`r"C:\path\file.txt"`).
- Prefer `read_files`/`search_codebase` over `grep`, `find`, `sed`, `awk`, `Select-String`.

## Python and uv

- Prefer `uv run <cmd>` so the 3.12 environment is used automatically, e.g.
  `uv run streamlit run app/main.py`, `uv run pytest -q`, `uv run python .\scripts\ingest.py`.
- Install only through `uv add` / `uv sync` (or `uv pip install`), never into the global
  3.14 interpreter and never with a bare global `pip`.
- Avoid `python -c "..."` beyond a trivial one-liner: write a temporary script, run it,
  delete it.

## File operations

| Task | Cmdlet |
|---|---|
| delete | `Remove-Item -LiteralPath <path> -Force` |
| delete tree | `Remove-Item -LiteralPath <path> -Recurse -Force` |
| copy / move / rename | `Copy-Item` / `Move-Item` / `Rename-Item` |
| exists | `Test-Path` |
| create dir | `New-Item -ItemType Directory -Path <path>` |
| read / write / append | `Get-Content` / `Set-Content` / `Add-Content` |

Before any recursive or forced delete, confirm the exact target first (for example with
`-WhatIf`). Never delete `data/chroma/` unless the user asks for a re-index.

## Long-running processes

`chroma run --path .\data\chroma`, `ollama serve` and `streamlit run` block the terminal.
Start them as background jobs when you need to keep working:

```powershell
Start-Job -Name chroma -ScriptBlock { chroma run --path .\data\chroma }
Get-Job -Name chroma | Receive-Job -Keep
Stop-Job -Name chroma; Remove-Job -Name chroma
```

If a command fails: read the error, find the root cause, fix, retry **once**. Do not
repeat near-identical broken commands.
