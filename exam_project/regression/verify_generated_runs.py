"""Execute each archived generated notebook and record what actually happens.

    uv run python -m regression.verify_generated_runs

The generated code is never edited. Each notebook's code cells are concatenated into a temporary
script, run with a timeout in the project root, and the exit code/stdout/stderr are written to
``regression/runs/rag/ui/<n>/execution.md``. The summary is written to
``docs/evaluation/regression-execution-2026-11-19.json``.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "regression" / "runs" / "rag" / "ui"
SUMMARY = ROOT / "docs" / "evaluation" / "regression-execution-2026-11-19.json"


def code_from_notebook(path: Path) -> str:
    """Concatenate every code cell; markdown cells are prompt/instruction only."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "code")


def first_error(stderr: str, stdout: str) -> str:
    """The last non-empty line of stderr is the exception in a normal Python traceback."""
    lines = [line.strip() for line in (stderr or stdout).splitlines() if line.strip()]
    return lines[-1] if lines else "(no error output)"


def run_one(run_dir: Path, timeout: int) -> dict[str, object]:
    """Run one generated notebook and write its execution record next to it."""
    notebook = run_dir / "output.ipynb"
    code = code_from_notebook(notebook)
    with tempfile.TemporaryDirectory(prefix="regression-run-") as temporary:
        script = Path(temporary) / "generated.py"
        script.write_text(code, encoding="utf-8")
        environment = dict(os.environ)
        environment.setdefault("MPLBACKEND", "Agg")
        try:
            completed = subprocess.run(
                [sys.executable, str(script)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""
            record = {
                "run": run_dir.name,
                "exit_code": None,
                "timed_out": True,
                "stdout": stdout[-8000:],
                "stderr": stderr[-8000:],
                "first_error": f"timeout after {timeout}s",
            }
        else:
            record = {
                "run": run_dir.name,
                "exit_code": completed.returncode,
                "timed_out": False,
                "stdout": completed.stdout[-8000:],
                "stderr": completed.stderr[-8000:],
                "first_error": "" if completed.returncode == 0 else first_error(completed.stderr, completed.stdout),
            }

    (run_dir / "execution.md").write_text(
        "\n".join(
            [
                f"# Execution record — ui/{run_dir.name}",
                "",
                f"- command: `{Path(sys.executable).name} <temporary>/generated.py`",
                f"- working directory: `{ROOT}`",
                f"- exit code: `{record['exit_code']}`",
                f"- timed out: `{record['timed_out']}`",
                f"- first error: `{record['first_error']}`",
                "",
                "## stdout",
                "",
                "```text",
                str(record["stdout"]).strip(),
                "```",
                "",
                "## stderr",
                "",
                "```text",
                str(record["stderr"]).strip(),
                "```",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    return record


def main() -> int:
    """Run every numbered generated notebook and print a compact summary."""
    parser = argparse.ArgumentParser(description="Execute the generated regression notebooks and record outcomes.")
    parser.add_argument("--timeout", type=int, default=60, help="seconds per notebook")
    args = parser.parse_args()

    directories = sorted(
        (path for path in RUNS.iterdir() if path.is_dir() and path.name.isdigit()),
        key=lambda path: int(path.name),
    )
    if not directories:
        print(f"no numbered runs under {RUNS}")
        return 1

    records = [run_one(run_dir, args.timeout) for run_dir in directories]
    SUMMARY.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{'run':<6} {'exit':<6} first error")
    print("-" * 100)
    for record in records:
        print(f"ui/{record['run']:<3} {str(record['exit_code']):<6} {record['first_error']}")
    print(f"\nwritten: {SUMMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
