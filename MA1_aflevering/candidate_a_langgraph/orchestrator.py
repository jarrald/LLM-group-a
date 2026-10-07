"""Candidate A -- LangGraph multi-LLM orchestration workflow (recommended).

A config-driven, checkpointed pipeline that binds every software role to a
model on one of *two separate local Ollama endpoints* and collaboratively
produces a complete set of software artifacts for a small target project:

    architecture -> tickets -> code (N>2 parallel workers) -> tests
    -> test execution -> bounded repair loop -> docs -> deploy validation
    -> quality report -> git commit

Everything is driven by config/endpoints.yaml; routing is never hard-coded.

Run (from the repository root):
    python candidate_a_langgraph/orchestrator.py --project demo_project
    python candidate_a_langgraph/orchestrator.py --config config/endpoints.alt.yaml
    python candidate_a_langgraph/orchestrator.py --control review
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict

import yaml
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Target project specification (the "product brief" every role works from).
# Keeping this short is deliberate: it is the shared contract that prevents
# context drift between agents.
# ---------------------------------------------------------------------------
PROJECT_NAME = "TaskFlow API"
PROJECT_BRIEF = f"""
Build "{PROJECT_NAME}": a tiny, dependency-free task/todo REST API in pure
Python 3 standard library (http.server + json). No third-party runtime deps.

Required modules (exact paths):
- src/taskflow/__init__.py        (package marker, exposes VERSION)
- src/taskflow/store.py           (class TaskStore: in-memory CRUD)
- src/taskflow/service.py         (class TaskService: validation + business rules)
- src/taskflow/api.py             (HTTP handler + make_server())
- src/taskflow/__main__.py        (starts the server on PORT env or 8080)

Domain rules:
- A Task has: id (int), title (str, required, 1..100 chars), done (bool, default False).
- create(title) -> Task ; list() -> list[Task] ; get(id) -> Task|None ;
  update(id, title=None, done=None) -> Task|None ; delete(id) -> bool.
- create() must reject an empty/whitespace/too-long title with ValueError.
- Ids are assigned sequentially starting at 1.

SHARED CONTRACT (every worker MUST follow this exactly - no extra modules):
- A Task is a PLAIN DICT: {{"id": int, "title": str, "done": bool}}. There is
  NO Task class and NO models.py anywhere in this project.
- store.py defines ONLY `class TaskStore` with EXACT methods: __init__(),
  create(title)->dict, list()->list[dict], get(id)->dict|None,
  update(id, title=None, done=None)->dict|None, delete(id)->bool.
  create() raises ValueError on an empty/whitespace/too-long title and assigns
  the next sequential int id. delete() returns True if removed else False.
- service.py defines ONLY `class TaskService`, constructed as TaskService(store).
  It MUST delegate with EXACTLY these calls and nothing else:
  return self.store.create(title) / self.store.list() / self.store.get(id) /
  self.store.update(id, title, done) / self.store.delete(id).
  NEVER access self.store.tasks or self.store.next_id directly.
- api.py defines make_server(host: str, port: int) -> http.server.HTTPServer.
  Its FIRST two import lines MUST be exactly:
    from taskflow.store import TaskStore
    from taskflow.service import TaskService
  Create ONE shared instance (module-level: service = TaskService(TaskStore()))
  and have the handler use it. Request bodies are JSON (json.loads); EVERY
  response body MUST be produced with json.dumps (never str()/repr) and sent
  with Content-Type: application/json and a correct Content-Length header.
- __main__.py reads the PORT env var (default 8080), builds the server with
  make_server and calls serve_forever().
- Do NOT create or import any module other than the five listed above.

HTTP surface (JSON):
- GET    /tasks            -> 200 [Task,...]
- POST   /tasks  {{"title"}} -> 201 Task | 400 {{"error"}}
- GET    /tasks/<id>       -> 200 Task | 404
- PATCH  /tasks/<id>       -> 200 Task | 400 | 404
- DELETE /tasks/<id>       -> 204 | 404
- GET    /healthz          -> 200 {{"status":"ok"}}
""".strip()


# ---------------------------------------------------------------------------
# Configuration + endpoint client
# ---------------------------------------------------------------------------
def load_config(path: Path) -> dict[str, Any]:
    cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if "endpoints" not in cfg or len(cfg["endpoints"]) < 2:
        raise SystemExit("config must declare at least two endpoints")
    return cfg


def endpoint_url(cfg: dict[str, Any], name: str) -> str:
    return cfg["endpoints"][name]["base_url"]


def role_target(cfg: dict[str, Any], role: str) -> tuple[str, str]:
    """Return (base_url, model) for a role, resolved through the config."""
    spec = cfg["roles"][role]
    return endpoint_url(cfg, spec["endpoint"]), spec["model"]


class LLMClient:
    """Thin wrapper around ChatOllama bound to a specific endpoint."""

    def __init__(self, cfg: dict[str, Any]) -> None:
        self.cfg = cfg
        self.defaults = cfg.get("defaults", {})
        self.calls: list[dict[str, Any]] = []

    def _build(self, base_url: str, model: str) -> ChatOllama:
        return ChatOllama(
            model=model,
            base_url=base_url,
            temperature=self.defaults.get("temperature", 0.2),
            num_ctx=self.defaults.get("num_ctx", 8192),
            num_predict=self.defaults.get("num_predict", 1400),
        )

    def chat(
        self,
        role: str,
        system: str,
        user: str,
        *,
        endpoint_override: str | None = None,
        model_override: str | None = None,
        retries: int = 2,
    ) -> str:
        if endpoint_override:
            base_url = endpoint_url(self.cfg, endpoint_override)
            model = model_override or self.cfg["roles"][role]["model"]
        else:
            base_url, model = role_target(self.cfg, role)
            if model_override:
                model = model_override
        last_err: Exception | None = None
        for attempt in range(retries + 1):
            t0 = time.time()
            try:
                llm = self._build(base_url, model)
                out = llm.invoke(
                    [SystemMessage(content=system), HumanMessage(content=user)]
                )
                text = out.content if isinstance(out.content, str) else str(out.content)
                self.calls.append(
                    {
                        "role": role,
                        "endpoint": base_url,
                        "model": model,
                        "seconds": round(time.time() - t0, 1),
                        "chars": len(text),
                        "ok": True,
                    }
                )
                return text
            except Exception as exc:  # noqa: BLE001 - recorded + retried
                last_err = exc
                self.calls.append(
                    {
                        "role": role,
                        "endpoint": base_url,
                        "model": model,
                        "seconds": round(time.time() - t0, 1),
                        "ok": False,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
                time.sleep(2)
        raise RuntimeError(f"role '{role}' failed after retries: {last_err}")


# ---------------------------------------------------------------------------
# Tolerant output parsing (local 7B models rarely emit perfect structure)
# ---------------------------------------------------------------------------
FENCE_RE = re.compile(r"```[ \t]*([a-zA-Z0-9_+-]*)[ \t]*\r?\n(.*?)```", re.DOTALL)
FILE_HINT_RE = re.compile(
    r"^\s*(?:#|//|<!--|;|\*)\s*(?:file|filename|path)\s*[:=]\s*(.+?)\s*(?:-->)?\s*$",
    re.IGNORECASE,
)
HEADING_FILE_RE = re.compile(
    r"^#{1,6}\s*(?:file|filename|path)\s*[:=]\s*(.+?)\s*$", re.IGNORECASE
)


def sanitize_relpath(raw: str) -> str | None:
    """Normalise a model-proposed path to a safe project-relative POSIX path."""
    p = raw.strip().strip("`").strip("\"'").rstrip(":").strip()
    p = p.replace("\\", "/").lstrip("/")
    p = re.sub(r"^\./", "", p)
    if not p or ".." in p.split("/") or p.startswith("~"):
        return None
    return p


def extract_files(text: str, default_path: str | None = None) -> dict[str, str]:
    """Extract {path: content} from fenced blocks using several path hints.

    Handles:  '# file: path' on the line before a fence, on the first line
    inside a fence, as a markdown heading, or a bare filename in the fence
    info-string. Falls back to `default_path` when only one unnamed block
    exists.
    """
    files: dict[str, str] = {}
    pending: list[str] = []
    lines = text.splitlines()

    hint_at: dict[int, str] = {}
    for i, line in enumerate(lines):
        m = FILE_HINT_RE.match(line) or HEADING_FILE_RE.match(line)
        if m:
            cand = sanitize_relpath(m.group(1))
            if cand:
                hint_at[i] = cand

    for m in FENCE_RE.finditer(text):
        info = m.group(1).strip()
        body = m.group(2)
        path: str | None = None
        first, _, rest = body.partition("\n")
        inner = FILE_HINT_RE.match(first)
        if inner:
            cand = sanitize_relpath(inner.group(1))
            if cand:
                path, body = cand, rest
        if path is None:
            fence_line = text[: m.start()].count("\n")
            for back in range(1, 4):
                if (fence_line - back) in hint_at:
                    path = hint_at[fence_line - back]
                    break
        if path is None and info:
            for token in info.split():
                cand = sanitize_relpath(token)
                if cand and ("/" in cand or "." in cand):
                    path = cand
                    break
        if path:
            files[path] = body.strip("\n")
        else:
            pending.append(body.strip("\n"))

    if not files:
        files = _extract_marker_sections(text)
    if not files and pending and default_path:
        files[default_path] = (
            pending[0] if len(pending) == 1 else "\n\n".join(pending)
        )
    return files


def _extract_marker_sections(text: str) -> dict[str, str]:
    """Fallback for header-style files: '# file: <path>' followed by prose (no fence).

    The docs model often emits several documents as plain sections delimited by
    '# file:' header lines rather than fenced blocks.
    """
    lines = text.splitlines()
    markers: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = FILE_HINT_RE.match(line) or HEADING_FILE_RE.match(line)
        if m:
            cand = sanitize_relpath(m.group(1))
            if cand:
                markers.append((i, cand))
    if not markers:
        return {}
    out: dict[str, str] = {}
    for idx, (line_no, path) in enumerate(markers):
        end = markers[idx + 1][0] if idx + 1 < len(markers) else len(lines)
        body = "\n".join(lines[line_no + 1:end]).strip("\n")
        if body:
            out[path] = body
    return out


def extract_json(text: str) -> Any | None:
    """Best-effort JSON extraction from a possibly chatty model reply."""
    candidates = [text, *re.findall(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)]
    for candidate in candidates:
        s = candidate.strip()
        starts = [i for i in (s.find("["), s.find("{")) if i != -1]
        if not starts:
            continue
        start = min(starts)
        for end in range(len(s), start, -1):
            try:
                return json.loads(s[start:end])
            except Exception:  # noqa: BLE001
                continue
    return None


# ---------------------------------------------------------------------------
# Filesystem / process / git helpers
# ---------------------------------------------------------------------------
def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_files(base: Path, files: dict[str, str]) -> list[str]:
    """Write {relpath: content} under `base`; returns the written paths."""
    written: list[str] = []
    for rel, content in files.items():
        safe = sanitize_relpath(rel)
        if not safe:
            continue
        target = base / safe
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.rstrip("\n") + "\n", encoding="utf-8")
        written.append(safe)
    return written


def run(cmd: list[str], cwd: Path, timeout: int = 300,
        env: dict[str, str] | None = None) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired as exc:
        return 124, f"TIMEOUT after {timeout}s: {exc}"
    except FileNotFoundError as exc:
        return 127, f"NOT FOUND: {exc}"


def run_pytest(project: Path) -> dict[str, Any]:
    code, out = run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider"], project)

    def find(pat: str) -> int | None:
        m = re.search(pat, out)
        return int(m.group(1)) if m else None

    passed = find(r"(\d+) passed")
    failed = find(r"(\d+) failed")
    errors = find(r"(\d+) error")
    if passed is None or failed is None:
        # Fallback when the summary line is absent: derive from the progress
        # line (e.g. ".F.......") plus the FAILED/ERROR lines.
        failed = failed if failed is not None else len(re.findall(r"^FAILED ", out, re.M))
        errors = errors if errors is not None else len(re.findall(r"^ERROR ", out, re.M))
        total = 0
        for line in out.splitlines():
            m = re.match(r"^([.FsxXeE]+)\s", line)
            if m:
                total = len(m.group(1))
                break
        passed = max(0, total - failed - errors) if total else (passed or 0)
    return {
        "exit_code": code,
        "passed": passed or 0,
        "failed": failed or 0,
        "errors": errors or 0,
        "output": out,
        "passed_ok": code == 0,
    }


def static_checks(project: Path) -> dict[str, Any]:
    """Compile every .py file (a dependency-free syntax/lint baseline)."""
    results: list[dict[str, Any]] = []
    for py in sorted(project.rglob("*.py")):
        if any(part in {".git", ".venv", "__pycache__"} for part in py.parts):
            continue
        code, out = run([sys.executable, "-m", "py_compile", str(py)], project)
        results.append({"file": str(py.relative_to(project)), "ok": code == 0, "detail": out.strip()})
    return {"checked": len(results), "failures": [r for r in results if not r["ok"]], "results": results}


def git(project: Path, *args: str) -> tuple[int, str]:
    return run(["git", *args], project)


def git_ensure_repo(project: Path) -> None:
    if not (project / ".git").exists():
        git(project, "init", "-q")
        git(project, "branch", "-M", "main")
    # keep commits reproducible: local identity for this demo repo
    git(project, "config", "user.name", "llm-workflow-bot")
    git(project, "config", "user.email", "bot@example.local")


def git_commit_all(project: Path, message: str) -> tuple[int, str]:
    git(project, "add", "-A")
    return git(project, "commit", "-q", "-m", message)


def git_diff(project: Path) -> str:
    _, out = git(project, "--no-pager", "diff", "--stat", "HEAD")
    _, out2 = git(project, "--no-pager", "diff", "HEAD")
    return out + "\n" + out2


# ---------------------------------------------------------------------------
# Always-present scaffolding (engineering glue, not model output)
# ---------------------------------------------------------------------------
SCAFFOLD_FILES: dict[str, str] = {
    "pytest.ini": "[pytest]\npythonpath = . src\ntestpaths = tests\naddopts = -q\n",
    "conftest.py": (
        "# Ensures the project root is importable during test collection.\n"
        "import pathlib\nimport sys\n\n"
        "sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))\n"
    ),
    "src/__init__.py": "",
    "src/taskflow/__init__.py": '"""TaskFlow API package."""\n\nVERSION = "0.1.0"\n',
    ".gitignore": "__pycache__/\n*.pyc\n.pytest_cache/\n.venv/\n",
}


# ---------------------------------------------------------------------------
# Pipeline state + role prompts
# ---------------------------------------------------------------------------
class FlowState(TypedDict, total=False):
    run_id: str
    project_dir: str
    run_dir: str
    control: str
    max_repair: int
    architecture: str
    adr: str
    openapi: str
    tickets: list[dict[str, Any]]
    tickets_raw: str
    code_files: dict[str, str]
    test_files: dict[str, str]
    test_result: dict[str, Any]
    repair_rounds: int
    docs_files: dict[str, str]
    deploy_files: dict[str, str]
    deploy_validation: dict[str, Any]
    quality_report: str
    context_manifest: dict[str, Any]
    events: list[str]


ARCH_SYS = (
    "You are a senior software architect. Produce concise, concrete Markdown. "
    "No preamble, no apologies."
)
ADR_SYS = (
    "You are a software architect writing an Architecture Decision Record. "
    "Use the sections: Title, Status, Context, Decision, Consequences. Markdown only."
)
OPENAPI_SYS = (
    "You are an API designer. Output ONLY a single fenced ```yaml block containing a "
    "valid OpenAPI 3.0.3 document. No prose."
)
TECHLEAD_SYS = (
    "You are a tech lead. Break work into small tickets. Output ONLY a fenced ```json "
    "block: a JSON array of objects with keys id, title, scope, acceptance_criteria "
    "(array of strings), depends_on (array of ids). No prose."
)
CODER_SYS = (
    "You are a Python developer. Output ONLY fenced code blocks. Every block MUST be "
    "immediately preceded by a line exactly like: # file: <relative/path.py>. "
    "Pure Python 3 standard library only. No prose outside the blocks."
)
TESTER_SYS = (
    "You are a QA engineer. Write pytest tests using only the standard library and "
    "pytest. Output ONLY fenced code blocks, each preceded by: # file: <path>. "
    "Import the implementation as `from taskflow.store import ...` / "
    "`from taskflow.service import ...`."
)
DOCS_SYS = "You are a technical writer. Produce concise Markdown. No preamble."
DEPLOY_SYS = (
    "You are a DevOps engineer. Produce deployment artifacts. Output ONLY fenced code "
    "blocks, each preceded by: # file: <path>. Keep them minimal and correct."
)


def arch_prompt() -> str:
    return (
        f"{PROJECT_BRIEF}\n\n"
        "Write a Markdown architecture document with these sections: "
        "## Components (a table of component -> responsibility), "
        "## Interface contracts (the HTTP endpoints and JSON shapes), "
        "## Deployment topology (single process, stdlib http.server, port 8080, container), "
        "## Constraints and risks. Keep it under 350 words."
    )


def adr_prompt(architecture: str) -> str:
    return (
        f"{PROJECT_BRIEF}\n\nArchitecture summary:\n{architecture[:1500]}\n\n"
        "Write ADR-0001 recording the decision to implement the API with the Python "
        "standard library (http.server) instead of a web framework."
    )


def openapi_prompt() -> str:
    return f"{PROJECT_BRIEF}\n\nProduce the OpenAPI 3.0.3 document for these endpoints."


def techlead_prompt(architecture: str) -> str:
    return (
        f"{PROJECT_BRIEF}\n\nArchitecture:\n{architecture[:1500]}\n\n"
        "Produce 4 tickets that partition the implementation by file: "
        "T1 = src/taskflow/store.py, T2 = src/taskflow/service.py, "
        "T3 = src/taskflow/api.py, T4 = src/taskflow/__main__.py. "
        "Each ticket needs scope, acceptance criteria and dependency ordering. "
        "T1 has no dependencies; T2, T3 and T4 each depend ONLY on T1 (they all "
        "build on the store contract, so they can be implemented in parallel)."
    )


def coder_prompt(ticket: dict[str, Any], repair: str | None = None,
                 context: str | None = None) -> str:
    base = (
        f"{PROJECT_BRIEF}\n\nYour ticket:\n"
        f"- id: {ticket.get('id')}\n- title: {ticket.get('title')}\n"
        f"- scope: {ticket.get('scope')}\n"
        f"- acceptance criteria: {ticket.get('acceptance_criteria')}\n\n"
        "Implement ONLY the file(s) named in the scope. Respect the SHARED "
        "CONTRACT exactly: a Task is a plain dict and you may import only from the "
        "five listed modules (there is no models.py). Output the file(s) as fenced "
        "blocks each preceded by '# file: <path>'."
    )
    if context:
        base += (
            "\n\nThese files are ALREADY IMPLEMENTED - your code MUST be compatible "
            "with their exact signatures (do not redefine them):\n" + context
        )
    if repair:
        base += (
            "\n\nThe previous attempt FAILED the tests. Fix ONLY the file(s) in your "
            "scope so they satisfy the callers/callees shown below.\n"
            "--- test output ---\n" + repair[-2500:]
        )
    return base


def tester_prompt(code_files: dict[str, str], repair: str | None = None) -> str:
    impl = "\n\n".join(
        f"# file: {p}\n```python\n{c}\n```"
        for p, c in code_files.items()
        if p.endswith(".py")
    )
    base = (
        f"{PROJECT_BRIEF}\n\nImplementation under test:\n{impl}\n\n"
        "Write focused pytest tests in tests/test_store.py and tests/test_service.py "
        "covering: sequential ids, empty/whitespace/too-long title rejected with "
        "ValueError, get/update/delete behaviour, and list ordering. Also write "
        "tests/test_api.py: an integration test that imports `make_server` from "
        "taskflow.api, binds it to port 0 on 127.0.0.1, serves it in a daemon "
        "thread, and uses urllib to assert GET /healthz is 200 and that POST /tasks "
        "with a JSON body (json.dumps of a dict with the title field, Content-Type "
        "application/json) returns 201 and a JSON response, then GET /tasks works. "
        "Only the standard library and pytest."
    )
    if repair:
        base += (
            "\n\nYour previous TESTS failed. Fix the TEST files (not the "
            "implementation). Common pitfalls to avoid:\n"
            "- urllib.request.urlopen() does NOT accept a 'method' argument. Build "
            "urllib.request.Request(url, data=..., method='POST') and pass THAT to "
            "urlopen.\n"
            "- Always send Content-Type: application/json for JSON bodies.\n"
            "- Read the response body once and decode it as UTF-8 before json.loads.\n"
            "--- test output ---\n" + repair[-2000:]
        )
    return base


def docs_prompt(state: "FlowState") -> str:
    return (
        f"{PROJECT_BRIEF}\n\nArchitecture:\n{state.get('architecture','')[:1200]}\n\n"
        "Produce three Markdown documents as fenced blocks each preceded by '# file:':\n"
        "1) README.md  (what it is, install, run `python -m taskflow`, run tests)\n"
        "2) docs/api-usage.md (curl examples for every endpoint)\n"
        "3) docs/runbook.md (start/stop, PORT env, health check, common failures)"
    )


def deploy_prompt() -> str:
    return (
        f"{PROJECT_BRIEF}\n\n"
        "Produce deployment artifacts as fenced blocks each preceded by '# file:':\n"
        "1) Dockerfile (python:3.12-slim, copy src, run `python -m taskflow`, EXPOSE 8080)\n"
        "2) deploy/validate_deploy.py - a stdlib-only script whose FIRST lines are:\n"
        "   import os, sys, time, socket, threading, urllib.request\n"
        "   sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))\n"
        "   then `from taskflow.api import make_server`. It must: pick a free TCP\n"
        "   port with socket, build the server via make_server('127.0.0.1', port),\n"
        "   run serve_forever() in a daemon thread, then poll\n"
        "   http://127.0.0.1:<port>/healthz and http://127.0.0.1:<port>/tasks with\n"
        "   urllib for up to 5 seconds until both return 200. On success print\n"
        "   'DEPLOY OK' and sys.exit(0); on failure print the error and sys.exit(1).\n"
        "3) docs/environment.md (env vars and ports)"
    )


# ---------------------------------------------------------------------------
# Runtime holder + LangGraph nodes
# ---------------------------------------------------------------------------
RT: dict[str, Any] = {}


def _save(name: str, text: str) -> None:
    (RT["run_dir"] / name).write_text(text, encoding="utf-8")


def _events(state: FlowState, msg: str) -> list[str]:
    return list(state.get("events", [])) + [msg]


def _default_path_for(ticket: dict[str, Any]) -> str:
    scope = str(ticket.get("scope", ""))
    m = re.search(r"(src/[\w/]+\.py)", scope)
    if m:
        return m.group(1)
    tid = str(ticket.get("id", "x")).lower()
    return f"src/taskflow/{tid}.py"


def node_architect(state: FlowState) -> dict[str, Any]:
    client: LLMClient = RT["client"]
    arch = client.chat("architect", ARCH_SYS, arch_prompt())
    adr = client.chat("architect", ADR_SYS, adr_prompt(arch))
    raw = client.chat("architect", OPENAPI_SYS, openapi_prompt())
    openapi = extract_files(raw, "api/openapi.yaml").get("api/openapi.yaml") or raw
    files = {
        "docs/architecture.md": arch,
        "docs/adr/0001-adr-stdlib-http-server.md": adr,
        "api/openapi.yaml": openapi,
    }
    write_files(RT["staged"], files)
    _save("01_architecture.md", arch)
    _save("02_adr.md", adr)
    _save("03_openapi.yaml", openapi)
    return {"architecture": arch, "adr": adr, "openapi": openapi,
            "events": _events(state, "architect -> docs/architecture.md, ADR-0001, api/openapi.yaml")}


def node_techlead(state: FlowState) -> dict[str, Any]:
    client: LLMClient = RT["client"]
    raw = client.chat("techlead", TECHLEAD_SYS, techlead_prompt(state["architecture"]))
    _save("04_tickets_raw.md", raw)
    data = extract_json(raw)
    fallback = [
        {"id": "T1", "title": "Implement in-memory store",
         "scope": "src/taskflow/store.py", "acceptance_criteria":
         ["create assigns sequential ids from 1", "get/update/delete behave per spec"],
         "depends_on": []},
        {"id": "T2", "title": "Implement service validation",
         "scope": "src/taskflow/service.py", "acceptance_criteria":
         ["empty/whitespace/too-long title raises ValueError", "delegates CRUD to store"],
         "depends_on": ["T1"]},
        {"id": "T3", "title": "Implement HTTP API",
         "scope": "src/taskflow/api.py", "acceptance_criteria":
         ["make_server(host, port) returns a configured HTTPServer",
          "routes match the OpenAPI contract", "returns correct status codes"],
         "depends_on": ["T1"]},
        {"id": "T4", "title": "Implement entrypoint",
         "scope": "src/taskflow/__main__.py", "acceptance_criteria":
         ["reads PORT env (default 8080)", "serves via make_server"],
         "depends_on": ["T1"]},
    ]
    tickets = data if isinstance(data, list) and data else fallback
    used_fallback = not (isinstance(data, list) and data)
    (RT["run_dir"] / "tickets.json").write_text(json.dumps(tickets, indent=2), encoding="utf-8")
    note = " (fallback: model JSON unparseable)" if used_fallback else ""
    return {"tickets": tickets, "tickets_raw": raw,
            "events": _events(state, f"techlead -> {len(tickets)} tickets{note}")}


def _ticket_path(ticket: dict[str, Any]) -> str:
    return _default_path_for(ticket)


def _batches(tickets: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Group tickets into dependency-ordered batches (Kahn's algorithm).

    Tickets with no unmet dependencies run together (in parallel); a batch only
    starts once every dependency has been produced, and its output is handed to
    the next batch as context. This is how the workflow honours the tech lead's
    dependency ordering while still parallelising within a batch.
    """
    by_id = {str(t.get("id")): t for t in tickets}
    deps = {str(t.get("id")): [str(d) for d in (t.get("depends_on") or [])]
            for t in tickets}
    done: set[str] = set()
    batches: list[list[dict[str, Any]]] = []
    remaining = list(by_id)
    while remaining:
        ready = [tid for tid in remaining
                 if all(d in done or d not in by_id for d in deps[tid])]
        if not ready:  # defensive: break dependency cycles
            ready = remaining[:]
        batches.append([by_id[tid] for tid in ready])
        done.update(ready)
        remaining = [t for t in remaining if t not in ready]
    return batches


def _run_coders(state: FlowState, repair: str | None = None) -> dict[str, str]:
    client: LLMClient = RT["client"]
    tickets: list[dict[str, Any]] = state["tickets"]
    pool = RT["cfg"].get("worker_pool", {})
    endpoints = pool.get("endpoints") or list(RT["cfg"]["endpoints"].keys())
    max_workers = max(1, min(pool.get("max_workers", 3), len(tickets)))

    collected: dict[str, str] = dict(state.get("code_files", {})) if repair else {}

    # On repair, only re-run the workers whose file is named in the failure.
    targets = tickets
    if repair:
        mentioned = set(re.findall(r"([\w/\\.]*taskflow[\w/\\.]*\.py)", repair))
        names = {m.split("\\")[-1].split("/")[-1] for m in mentioned}
        sel = [t for t in tickets
               if _ticket_path(t) in mentioned or _ticket_path(t).split("/")[-1] in names]
        if sel:
            targets = sel

    # Stable endpoint assignment: ticket index -> endpoint (round-robin), so both
    # servers are used regardless of how the tickets are batched.
    order = {str(t.get("id")): i for i, t in enumerate(tickets)}

    def work(i: int, ticket: dict[str, Any]) -> tuple[str, str, dict[str, str]]:
        ep = endpoints[i % len(endpoints)]
        context = "\n\n".join(
            f"# file: {p}\n```python\n{c}\n```" for p, c in sorted(collected.items())
        ) or None
        text = client.chat("coder", CODER_SYS,
                           coder_prompt(ticket, repair, context), endpoint_override=ep)
        return str(ticket.get("id")), ep, extract_files(text, _ticket_path(ticket))

    for batch in _batches(targets):
        with cf.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(work, order[str(t.get("id"))], t) for t in batch]
            for fut in cf.as_completed(futures):
                tid, ep, files = fut.result()
                collected.update(files)
                _save(f"05_code_{tid}_{ep}.md",
                      json.dumps({"endpoint": ep, "files": list(files)}, indent=2))
    write_files(RT["staged"], collected)
    return collected


def node_coders(state: FlowState) -> dict[str, Any]:
    files = _run_coders(state)
    n_batches = len(_batches(state["tickets"]))
    return {"code_files": files,
            "events": _events(state,
                f"coders -> {len(files)} files in {n_batches} dependency-ordered "
                f"batch(es): {sorted(files)}")}


def node_repair(state: FlowState) -> dict[str, Any]:
    """Targeted repair: rewrite implicated implementation and/or test files."""
    failure = state["test_result"]["output"]
    rounds = state.get("repair_rounds", 0) + 1
    code_files = dict(state.get("code_files", {}))
    test_files = dict(state.get("test_files", {}))
    notes: list[str] = []

    mentions_tests = bool(re.search(r"tests?[/\\][\w/\\.]*\.py", failure))
    mentions_src = bool(re.search(r"src[/\\][\w/\\.]*\.py", failure))

    if mentions_src or not mentions_tests:
        rewritten = _run_coders(state, repair=failure)
        code_files.update(rewritten)
        notes.append(f"{len(rewritten)} impl file(s)")

    if mentions_tests:
        raw = RT["client"].chat("tester", TESTER_SYS,
                                tester_prompt(code_files, repair=failure))
        tf = extract_files(raw, "tests/test_generated.py")
        write_files(RT["staged"], tf)
        test_files.update(tf)
        _save(f"06_tests_repair{rounds}.md", raw)
        notes.append(f"{len(tf)} test file(s)")

    return {"code_files": code_files, "test_files": test_files, "repair_rounds": rounds,
            "events": _events(state, f"repair round {rounds}: rewrote " + ", ".join(notes))}


def node_tester(state: FlowState) -> dict[str, Any]:
    client: LLMClient = RT["client"]
    raw = client.chat("tester", TESTER_SYS, tester_prompt(state["code_files"]))
    files = extract_files(raw, "tests/test_generated.py")
    write_files(RT["staged"], files)
    _save("06_tests_raw.md", raw)
    return {"test_files": files,
            "events": _events(state, f"tester -> {len(files)} test files: {sorted(files)}")}


def node_run_tests(state: FlowState) -> dict[str, Any]:
    res = run_pytest(RT["staged"])
    _save("07_test_output.txt", res["output"])
    return {"test_result": res,
            "events": _events(state,
                f"pytest: rc={res['exit_code']} passed={res['passed']} "
                f"failed={res['failed']} errors={res['errors']}")}


def route_after_tests(state: FlowState) -> str:
    res = state["test_result"]
    if res["passed_ok"]:
        return "continue"
    if state.get("repair_rounds", 0) < state.get("max_repair", 2):
        return "repair"
    return "continue"


def node_docs(state: FlowState) -> dict[str, Any]:
    client: LLMClient = RT["client"]
    raw = client.chat("docs", DOCS_SYS, docs_prompt(state))
    files = extract_files(raw, "README.md")
    write_files(RT["staged"], files)
    _save("08_docs_raw.md", raw)
    return {"docs_files": files,
            "events": _events(state, f"docs -> {len(files)} files: {sorted(files)}")}


def node_deploy(state: FlowState) -> dict[str, Any]:
    client: LLMClient = RT["client"]
    raw = client.chat("deploy", DEPLOY_SYS, deploy_prompt())
    files = extract_files(raw)
    write_files(RT["staged"], files)
    _save("09_deploy_raw.md", raw)

    script = RT["staged"] / "deploy" / "validate_deploy.py"
    if script.exists():
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(
            [str(RT["staged"] / "src"), str(RT["staged"]), env.get("PYTHONPATH", "")]
        ).strip(os.pathsep)
        code, out = run([sys.executable, str(script)], RT["staged"], timeout=120, env=env)
        val = {"ran": True, "exit_code": code, "ok": code == 0, "output": out}
    else:
        val = {"ran": False, "ok": False, "output": "validate_deploy.py was not produced by the model"}
    _save("10_deploy_validation.txt", val["output"])
    return {"deploy_files": files, "deploy_validation": val,
            "events": _events(state,
                f"deploy -> {len(files)} files; validation "
                f"{'OK' if val.get('ok') else 'FAILED'}")}


def diff_dirs(old_root: Path, new_root: Path) -> tuple[str, dict[str, int]]:
    import difflib

    rels: set[str] = set()
    for base in (old_root, new_root):
        if base.exists():
            for p in base.rglob("*"):
                if p.is_file() and not any(
                    part in {".git", "__pycache__", ".pytest_cache"} for part in p.parts
                ):
                    rels.add(p.relative_to(base).as_posix())
    out: list[str] = []
    stat = {"added": 0, "changed": 0, "unchanged": 0}
    for rel in sorted(rels):
        a, b = old_root / rel, new_root / rel
        atext = a.read_text(encoding="utf-8", errors="replace").splitlines() if a.exists() else []
        btext = b.read_text(encoding="utf-8", errors="replace").splitlines() if b.exists() else []
        if atext == btext:
            stat["unchanged"] += 1
            continue
        stat["changed" if a.exists() else "added"] += 1
        out.extend(difflib.unified_diff(atext, btext, fromfile=f"a/{rel}", tofile=f"b/{rel}", lineterm=""))
    return "\n".join(out), stat


LIMITATIONS = [
    "7B-class local models occasionally omit a required file; the pipeline records "
    "which artifacts were produced instead of silently dropping them.",
    "Model-authored tests may under-specify edge cases; the quality report is the "
    "source of truth for what actually passed.",
    "Repair rounds are bounded (see max_repair_rounds in config) to keep runs "
    "predictable; unresolved failures are reported rather than looped forever.",
    "The deploy validator uses a stdlib in-process server, not a real container "
    "build (Docker daemon is optional); the Dockerfile is validated by inspection.",
]


def node_quality(state: FlowState) -> dict[str, Any]:
    client: LLMClient = RT["client"]
    checks = static_checks(RT["staged"])
    tr = state["test_result"]
    dv = state.get("deploy_validation", {})
    lines = [
        f"# Quality Report - {PROJECT_NAME}",
        f"\nRun id: `{state['run_id']}`  |  control mode: `{state.get('control','apply')}`\n",
        "## Test results",
        f"- pytest exit code: {tr['exit_code']}",
        f"- passed: {tr['passed']}  failed: {tr['failed']}  errors: {tr['errors']}",
        f"- repair rounds used: {state.get('repair_rounds', 0)}",
        "\n```text\n" + tr["output"][-3000:] + "\n```",
        "\n## Static checks (py_compile)",
        f"- files checked: {checks['checked']}  syntax failures: {len(checks['failures'])}",
    ]
    for f in checks["failures"]:
        lines.append(f"  - {f['file']}: {f['detail'][:200]}")
    lines.append("\n## Deployment validation")
    if dv.get("ran"):
        lines.append(f"- deploy/validate_deploy.py exit code {dv['exit_code']} -> "
                     f"{'OK' if dv.get('ok') else 'FAILED'}")
        lines.append("\n```text\n" + dv["output"][-1500:] + "\n```")
    else:
        lines.append(f"- not run: {dv.get('output', '')}")
    lines += [
        "\n## Model calls (endpoint routing evidence)",
        "| role | endpoint | model | seconds | ok |",
        "|---|---|---|---|---|",
    ]
    for c in client.calls:
        lines.append(f"| {c['role']} | {c['endpoint']} | {c['model']} | "
                     f"{c.get('seconds', '')} | {c.get('ok')} |")
    lines.append("\n## Known limitations / risks")
    lines += [f"- {x}" for x in LIMITATIONS]
    report = "\n".join(lines)
    (RT["run_dir"] / "quality_report.md").write_text(report, encoding="utf-8")
    write_files(RT["staged"], {"reports/quality_report.md": report})
    return {"quality_report": report,
            "events": _events(state, "quality -> reports/quality_report.md")}


def node_apply(state: FlowState) -> dict[str, Any]:
    """Diff staged output vs the live project; apply + commit only in 'apply' mode."""
    project: Path = RT["project"]
    staged: Path = RT["staged"]
    diff_text, stat = diff_dirs(project, staged)
    (RT["run_dir"] / "diff.patch").write_text(diff_text, encoding="utf-8")

    applied = False
    commit = ""
    if state.get("control", "apply") == "apply":
        project.mkdir(parents=True, exist_ok=True)
        for child in list(project.iterdir()):
            if child.name == ".git":
                continue
            if child.is_dir():
                shutil.rmtree(child, ignore_errors=True)
            else:
                child.unlink()
        for p in staged.rglob("*"):
            if p.is_file():
                rel = p.relative_to(staged)
                dst = project / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dst)
        git_ensure_repo(project)
        msg = (f"feat: {PROJECT_NAME} generated by LangGraph multi-LLM workflow "
               f"(run {state['run_id']})")
        code, out = git_commit_all(project, msg)
        commit = out.strip().splitlines()[0] if out.strip() else f"commit rc={code}"
        applied = True

    summary = {"added": stat["added"], "changed": stat["changed"],
               "applied": applied, "commit": commit}
    (RT["run_dir"] / "apply_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return {"events": _events(state,
            f"apply: +{stat['added']} files, ~{stat['changed']} changed, applied={applied} {commit}")}


# ---------------------------------------------------------------------------
# Graph assembly
# ---------------------------------------------------------------------------
def build_graph():
    g = StateGraph(FlowState)
    g.add_node("architect", node_architect)
    g.add_node("techlead", node_techlead)
    g.add_node("coders", node_coders)
    g.add_node("tester", node_tester)
    g.add_node("run_tests", node_run_tests)
    g.add_node("repair", node_repair)
    g.add_node("docs", node_docs)
    g.add_node("deploy", node_deploy)
    g.add_node("quality", node_quality)
    g.add_node("apply", node_apply)

    g.add_edge(START, "architect")
    g.add_edge("architect", "techlead")
    g.add_edge("techlead", "coders")
    g.add_edge("coders", "tester")
    g.add_edge("tester", "run_tests")
    g.add_conditional_edges("run_tests", route_after_tests,
                            {"repair": "repair", "continue": "docs"})
    g.add_edge("repair", "run_tests")
    g.add_edge("docs", "deploy")
    g.add_edge("deploy", "quality")
    g.add_edge("quality", "apply")
    g.add_edge("apply", END)
    return g.compile()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LangGraph multi-LLM workflow (Candidate A)")
    ap.add_argument("--config", default=str(ROOT / "config" / "endpoints.yaml"))
    ap.add_argument("--project", default=str(ROOT / "demo_project"))
    ap.add_argument("--control", choices=["apply", "review"], default="apply")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--max-repair", type=int, default=None)
    args = ap.parse_args(argv)

    cfg = load_config(Path(args.config))
    project = Path(args.project).resolve()
    run_id = args.run_id or utc_stamp()
    run_dir = (ROOT / "runs" / run_id).resolve()
    staged = run_dir / "staged"
    run_dir.mkdir(parents=True, exist_ok=True)
    staged.mkdir(parents=True, exist_ok=True)
    write_files(staged, SCAFFOLD_FILES)

    RT.clear()
    RT.update(cfg=cfg, client=LLMClient(cfg), project=project, run_dir=run_dir, staged=staged)

    max_repair = (args.max_repair if args.max_repair is not None
                  else cfg.get("defaults", {}).get("max_repair_rounds", 2))

    print(f"[run {run_id}] config={args.config}  control={args.control}")
    for name, spec in cfg["endpoints"].items():
        print(f"[run {run_id}] endpoint {name}: {spec['base_url']}")
    routing = ", ".join(f"{r}->{s['endpoint']}:{s['model']}" for r, s in cfg["roles"].items())
    print(f"[run {run_id}] routing: {routing}")

    state: FlowState = {
        "run_id": run_id, "project_dir": str(project), "run_dir": str(run_dir),
        "control": args.control, "max_repair": max_repair, "repair_rounds": 0, "events": [],
    }
    graph = build_graph()
    final = graph.invoke(state)

    context_manifest = {
        "principle": "Each role receives a SCOPED subset of upstream artifacts, never "
                     "the whole repository. Handoffs happen through files on disk plus "
                     "an explicit, bounded prompt context.",
        "scoping": {
            "architect": "PROJECT_BRIEF only",
            "techlead": "PROJECT_BRIEF + architecture.md (truncated to 1500 chars)",
            "coder": "PROJECT_BRIEF + its own ticket + code of already-produced "
                     "dependency files (context handoff, not the whole repo)",
            "tester": "PROJECT_BRIEF + the implementation files under test",
            "docs": "PROJECT_BRIEF + architecture.md (truncated to 1200 chars)",
            "deploy": "PROJECT_BRIEF only",
        },
        "growth_behaviour": "Prompt size stays bounded because only dependency-ordered "
                            "artifacts are passed forward; raw model output is kept on "
                            "disk under runs/<id>/ rather than accumulated in context.",
    }
    (run_dir / "context_manifest.json").write_text(
        json.dumps(context_manifest, indent=2), encoding="utf-8")

    manifest = {
        "run_id": run_id,
        "config": str(args.config),
        "control": args.control,
        "endpoints": cfg["endpoints"],
        "roles": cfg["roles"],
        "events": final.get("events", []),
        "test_result": {k: v for k, v in final.get("test_result", {}).items() if k != "output"},
        "deploy_validation": {k: v for k, v in final.get("deploy_validation", {}).items() if k != "output"},
        "llm_calls": RT["client"].calls,
        "artifacts": {
            "architecture": bool(final.get("architecture")),
            "tickets": len(final.get("tickets", [])),
            "code_files": sorted(final.get("code_files", {})),
            "test_files": sorted(final.get("test_files", {})),
            "docs_files": sorted(final.get("docs_files", {})),
            "deploy_files": sorted(final.get("deploy_files", {})),
        },
    }
    (run_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("\n=== workflow events ===")
    for e in final.get("events", []):
        print(" -", e)
    tr = final.get("test_result", {})
    print(f"\ntests: passed={tr.get('passed')} failed={tr.get('failed')} errors={tr.get('errors')}")
    print(f"run artifacts: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
