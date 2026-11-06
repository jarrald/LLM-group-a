"""Narrow tool surface; local execution is NOT a security sandbox."""
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from langchain_core.tools import tool

ROOT = Path(__file__).resolve().parent

def fingerprint(work: Path) -> str:
    return hashlib.sha256(b"\0".join((work/n).read_bytes() if (work/n).exists() else b""
                                    for n in ("calculator.py","test_calculator.py"))).hexdigest()

def execute_checks(work: Path, timeout: int = 30) -> dict:
    reports = {}
    for label,path in (("generated",work/"test_calculator.py"),
                       ("acceptance",ROOT/"checks/acceptance_checks.py")):
        if not path.exists():
            reports[label] = {"passed":False,"output":"Missing test file","returncode":2}
            continue
        try:
            # No model-supplied commands, arguments or working directories.
            result = subprocess.run([sys.executable,"-I","-B",str(ROOT/"checks/run_suite.py"),str(path)],
                                    cwd=work,text=True,capture_output=True,timeout=timeout)
            reports[label] = {"passed":result.returncode==0,"returncode":result.returncode,
                              "output":(result.stdout+result.stderr)[-12000:]}
        except subprocess.TimeoutExpired:
            reports[label] = {"passed":False,"returncode":124,"output":f"Test timeout ({timeout}s)"}
    reports["passed"] = all(reports[k]["passed"] for k in ("generated","acceptance"))
    reports["fingerprint"] = fingerprint(work)
    return reports

def compact_evidence(report: dict) -> str:
    return json.dumps({k:{"passed":report[k]["passed"],"output":report[k]["output"][-2600:]}
                       for k in ("generated","acceptance")})

class WorkspaceTools:
    def __init__(self, work: Path, log):
        self.work, self.log = work, log
        self.evidence = None
        self.verdict = None

    def reset_review(self):
        self.evidence = None
        self.verdict = None

    def tools_for(self, role: str):
        allowed_write = "calculator.py" if role == "coder" else "test_calculator.py"

        @tool
        def read_file(filename: str) -> str:
            """Read calculator.py or test_calculator.py from this run's workspace."""
            if filename not in ("calculator.py","test_calculator.py"):
                return "ERROR: filename is not allowed"
            path=self.work/filename
            self.log("tool",{"role":role,"tool":"read_file","filename":filename})
            return path.read_text() if path.exists() else "File does not exist yet."

        @tool
        def write_file(filename: str, content: str) -> str:
            """Write a complete Python file. Coder writes calculator.py; reviewer writes test_calculator.py."""
            if filename != allowed_write:
                return f"ERROR: this role may only write {allowed_write}"
            if len(content)>18000:
                return "ERROR: file too large; keep this exercise concise"
            try: ast.parse(content)
            except SyntaxError as exc: return f"ERROR: invalid Python syntax: {exc}"
            (self.work/filename).write_text(content,encoding="utf-8")
            self.evidence=None; self.verdict=None
            self.log("tool",{"role":role,"tool":"write_file","filename":filename})
            return "Saved."

        @tool
        def run_tests() -> str:
            """Run generated unittest tests and fixed acceptance checks; return actual test evidence."""
            self.evidence=execute_checks(self.work)
            self.log("tests",self.evidence)
            return compact_evidence(self.evidence)

        @tool
        def submit_review(approved: bool, findings: str) -> str:
            """Submit review after running tests. Cite AC IDs and explain design compliance or defects."""
            if not self.evidence or self.evidence["fingerprint"] != fingerprint(self.work):
                return "ERROR: run tests after the latest file change before submitting review"
            if approved and not self.evidence["passed"]:
                return "ERROR: tests failed; approved must be false"
            if not findings.strip(): return "ERROR: supply review findings"
            self.verdict={"approved":approved,"findings":findings[:4000],
                          "fingerprint":fingerprint(self.work)}
            self.log("review",self.verdict)
            return "Review recorded. Finish your turn."

        return [read_file,write_file] if role=="coder" else [read_file,write_file,run_tests,submit_review]
