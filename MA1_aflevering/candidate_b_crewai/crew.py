"""Candidate B -- CrewAI role-based multi-agent orchestration (NATIVE features).

This version deliberately uses ONLY CrewAI's built-in capabilities, so the
comparison against Candidate A (LangGraph) is fair:

  * multi-endpoint per role        -> LLM(model="ollama/<tag>", base_url=...)
  * real files on disk             -> Task(output_file=..., create_directory=True)
  * structured output              -> Task(output_pydantic=<pydantic model>)
  * contract enforcement + retries -> Task(guardrail=..., guardrail_max_retries=...)
  * parallel coding workers (N>2)  -> Task(async_execution=True)
  * cross-task memory / context    -> Crew(memory=True) + native Ollama embedder

Deliberately NOT attempted (CrewAI has no built-in for these; see the synopsis
"what CrewAI cannot do by default" section): running pytest, running a deploy
validator, git diff/commit, or generating a quality report. The small post-run
block at the bottom is an *evaluation harness* (our measurement), not part of
the crew.

Run (from the repository root, inside the crewai venv):
    .venv-crewai\\Scripts\\python.exe candidate_b_crewai/crew.py --run-id runB_native
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

PROJECT_NAME = "TaskFlow API"
PROJECT_BRIEF = (
    'Build "TaskFlow API": a tiny, dependency-free task/todo REST API in pure '
    "Python 3 standard library (http.server + json). Required modules: "
    "src/taskflow/store.py (class TaskStore, in-memory CRUD), "
    "src/taskflow/service.py (class TaskService, validation), "
    "src/taskflow/api.py (defines make_server(host, port)), "
    "src/taskflow/__main__.py (reads PORT env, default 8080). "
    "A Task is a PLAIN DICT {id, title, done}; there is NO models.py. "
    "SHARED CONTRACT - every module must match exactly: "
    "TaskStore has create(title)->dict, list()->list[dict], get(id)->dict|None, "
    "update(id, title=None, done=None)->dict|None, delete(id)->bool; "
    "TaskService is built as TaskService(store), imports "
    "'from taskflow.store import TaskStore' and delegates every call to self.store "
    "(never touches store internals); "
    "api.py imports both TaskStore and TaskService, parses JSON request bodies and "
    "serialises every response with json.dumps (never str()), and implements "
    "GET /tasks, POST /tasks, GET /tasks/<id>, PATCH /tasks/<id>, "
    "DELETE /tasks/<id> and GET /healthz."
)


# ---------------------------------------------------------------------------
# Native structured output models
# ---------------------------------------------------------------------------
from pydantic import BaseModel, Field  # noqa: E402


class Ticket(BaseModel):
    id: str = Field(description="Ticket id, e.g. T1")
    title: str
    scope: str = Field(description="The file this ticket implements")
    acceptance_criteria: list[str]
    depends_on: list[str] = Field(default_factory=list)


class TicketPlan(BaseModel):
    tickets: list[Ticket]


# ---------------------------------------------------------------------------
# Native guardrails (CrewAI contract: one parameter, return (bool, Any); the
# return annotation MUST be omitted because this module uses PEP 563 strings).
# ---------------------------------------------------------------------------
def contract_guardrail(*markers: str):
    """Build a guardrail that requires the given markers in the task output."""

    def _guard(output):
        raw = getattr(output, "raw", None)
        text = raw if isinstance(raw, str) else str(output)
        missing = [m for m in markers if m not in text]
        if missing:
            return (False, f"Shared-contract violation, missing: {missing}")
        return (True, output)

    _guard.__name__ = "contract_guardrail_" + "_".join(m.strip("<>/ ") for m in markers)[:40]
    return _guard


# ---------------------------------------------------------------------------
# Config + LLM binding (multi-endpoint)
# ---------------------------------------------------------------------------
def load_config(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def make_llm(cfg: dict, role: str):
    from crewai import LLM

    spec = cfg["roles"][role]
    base_url = cfg["endpoints"][spec["endpoint"]]["base_url"]
    print(f"  {role:<10} -> {spec['endpoint']} ({base_url})  model={spec['model']}")
    return LLM(
        model=f"ollama/{spec['model']}",
        base_url=base_url,
        temperature=cfg.get("defaults", {}).get("temperature", 0.2),
        timeout=cfg.get("defaults", {}).get("request_timeout_s", 900),
    )


def build_agents(cfg: dict) -> dict:
    from crewai import Agent

    return {
        "architect": Agent(
            role="Software Architect",
            goal="Produce component decomposition, interface contracts, deployment topology and an ADR",
            backstory="You design small, dependency-free Python services and document them precisely.",
            llm=make_llm(cfg, "architect"),
            verbose=False,
            allow_delegation=False,
        ),
        "techlead": Agent(
            role="Tech Lead",
            goal="Break the work into tickets with scope, acceptance criteria and dependency ordering",
            backstory="You partition work by file so several developers can implement it.",
            llm=make_llm(cfg, "techlead"),
            verbose=False,
            allow_delegation=False,
        ),
        "tester": Agent(
            role="QA Engineer",
            goal="Write focused pytest tests for the file under test",
            backstory="You test edge cases such as invalid titles and missing ids.",
            llm=make_llm(cfg, "tester"),
            verbose=False,
            allow_delegation=False,
        ),
        "docs": Agent(
            role="Technical Writer",
            goal="Produce a single clear Markdown document for the requested artifact",
            backstory="You write concise, runnable Markdown.",
            llm=make_llm(cfg, "docs"),
            verbose=False,
            allow_delegation=False,
        ),
        "deploy": Agent(
            role="DevOps Engineer",
            goal="Produce one deployment artifact at a time",
            backstory="You keep deployment artifacts minimal and correct.",
            llm=make_llm(cfg, "deploy"),
            verbose=False,
            allow_delegation=False,
        ),
    }


def make_coder_agent(cfg: dict):
    """A FRESH coder agent per parallel task.

    CrewAI's native async_execution runs tasks concurrently, but an Agent's
    executor is not re-entrant ("Executor is already running..."), so parallel
    coding tasks must NOT share a single Agent instance.
    """
    from crewai import Agent

    return Agent(
        role="Python Developer",
        goal="Implement exactly the file in the ticket, honouring the shared contract",
        backstory="You write clean standard-library Python that matches the agreed signatures.",
        llm=make_llm(cfg, "coder"),
        verbose=False,
        allow_delegation=False,
    )


def build_tasks(agents: dict, cfg: dict, staged: Path, guardrails_on: bool,
                coders: list):
    """One task per artifact, so CrewAI's native output_file writes real files."""
    from crewai import Task

    def out(*parts: str) -> str:
        return str((staged.joinpath(*parts)).resolve())

    def guard(*markers: str):
        return contract_guardrail(*markers) if guardrails_on else None

    t_arch = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite a Markdown architecture document with "
        "sections: Components (table), Interface contracts, Deployment topology, "
        "Constraints and risks.",
        expected_output="A concise Markdown architecture document.",
        agent=agents["architect"],
        output_file=out("docs", "architecture.md"),
        create_directory=True,
    )
    t_plan = Task(
        description=f"{PROJECT_BRIEF}\n\nBreak the work into exactly 4 tickets, one per "
        "file: src/taskflow/store.py (T1), src/taskflow/service.py (T2), "
        "src/taskflow/api.py (T3), src/taskflow/__main__.py (T4). "
        "T1 has no dependencies; T2, T3 and T4 each depend only on T1.",
        expected_output="A JSON object with a 'tickets' array of 4 tickets.",
        agent=agents["techlead"],
        context=[t_arch],
        output_pydantic=TicketPlan,
        output_file=out("tickets.json"),
        create_directory=True,
        guardrail=guard("tickets"),
        guardrail_max_retries=1,
    )

    def code_task(path, deps, markers, parallel, coder):
        return Task(
            description=f"{PROJECT_BRIEF}\n\nImplement ONLY {path}. "
            "Output only the Python source for that one file - no prose, no fences.",
            expected_output=f"Python source code for {path}.",
            agent=coder,
            context=[t_plan, *deps],
            output_file=out(*path.split("/")),
            create_directory=True,
            guardrail=guard(*markers),
            guardrail_max_retries=1,
            async_execution=parallel,
        )

    t_store = code_task("src/taskflow/store.py", [],
                        ("class TaskStore", "def create", "def delete"), False, coders[0])
    t_service = code_task("src/taskflow/service.py", [t_store],
                          ("class TaskService", "self.store"), True, coders[1])
    t_api = code_task("src/taskflow/api.py", [t_store],
                      ("make_server", "json.dumps"), True, coders[2])
    t_main = code_task("src/taskflow/__main__.py", [t_store],
                       ("make_server",), True, coders[3])

    t_test_store = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite a pytest test file for src/taskflow/store.py. "
        "Output only the Python source - no prose, no fences.",
        expected_output="Python pytest source for tests/test_store.py.",
        agent=agents["tester"],
        context=[t_store],
        output_file=out("tests", "test_store.py"),
        create_directory=True,
    )
    t_test_service = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite a pytest test file for src/taskflow/service.py, "
        "including ValueError cases for empty/whitespace/too-long titles. "
        "Output only the Python source - no prose, no fences.",
        expected_output="Python pytest source for tests/test_service.py.",
        agent=agents["tester"],
        context=[t_service],
        output_file=out("tests", "test_service.py"),
        create_directory=True,
    )
    t_test_api = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite a pytest integration test for src/taskflow/api.py "
        "that starts make_server on a free port in a daemon thread and asserts "
        "GET /healthz is 200 and POST /tasks then GET /tasks work. "
        "Output only the Python source - no prose, no fences.",
        expected_output="Python pytest source for tests/test_api.py.",
        agent=agents["tester"],
        context=[t_api],
        output_file=out("tests", "test_api.py"),
        create_directory=True,
    )
    t_readme = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite README.md: what it is, how to run it, "
        "how to run the tests.",
        expected_output="A Markdown README.",
        agent=agents["docs"],
        context=[t_arch],
        output_file=out("README.md"),
        create_directory=True,
    )
    t_usage = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite docs/api-usage.md with a curl example for "
        "every endpoint.",
        expected_output="A Markdown API usage document.",
        agent=agents["docs"],
        context=[t_arch],
        output_file=out("docs", "api-usage.md"),
        create_directory=True,
    )
    t_runbook = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite docs/runbook.md: start/stop, PORT env, "
        "health check, common failures.",
        expected_output="A Markdown runbook.",
        agent=agents["docs"],
        context=[t_arch],
        output_file=out("docs", "runbook.md"),
        create_directory=True,
    )
    t_env = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite docs/environment.md listing the env vars "
        "and ports.",
        expected_output="A short Markdown environment document.",
        agent=agents["deploy"],
        context=[t_arch],
        output_file=out("docs", "environment.md"),
        create_directory=True,
    )
    t_docker = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite a Dockerfile (python:3.12-slim, copy src, "
        "run the package, EXPOSE 8080). Output only the Dockerfile contents.",
        expected_output="A Dockerfile.",
        agent=agents["deploy"],
        context=[t_api],
        output_file=out("Dockerfile"),
        create_directory=True,
    )
    t_validator = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite deploy/validate_deploy.py: a stdlib-only "
        "script that inserts src on sys.path, imports make_server from taskflow.api, "
        "starts it on a free port in a daemon thread, polls GET /healthz and GET /tasks "
        "with urllib until both return 200, prints 'DEPLOY OK' and exits 0. "
        "Output only the Python source.",
        expected_output="Python source for deploy/validate_deploy.py.",
        agent=agents["deploy"],
        context=[t_api],
        output_file=out("deploy", "validate_deploy.py"),
        create_directory=True,
    )

    return [
        t_arch, t_plan, t_store, t_service, t_api, t_main,
        t_test_store, t_test_service, t_test_api,
        t_readme, t_usage, t_runbook, t_env, t_docker, t_validator,
    ]


# ---------------------------------------------------------------------------
# Evaluation harness -- OUR measurement, NOT part of the crew. CrewAI has no
# built-in way to run tests, so we do it here and label it as harness output.
# ---------------------------------------------------------------------------
def run_pytest(staged: Path) -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [str(staged / "src"), str(staged), env.get("PYTHONPATH", "")]
    ).strip(os.pathsep)
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q"],
            cwd=str(staged), capture_output=True, text=True, env=env, timeout=300,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        return {"exit_code": proc.returncode, "output": out}
    except Exception as exc:  # noqa: BLE001
        return {"exit_code": 124, "output": f"pytest could not run: {exc}"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="CrewAI multi-LLM workflow (Candidate B, native features)")
    ap.add_argument("--config", default=str(ROOT / "config" / "endpoints.yaml"))
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--no-memory", action="store_true", help="disable Crew(memory=True)")
    ap.add_argument("--no-guardrails", action="store_true", help="disable native guardrails")
    ap.add_argument("--no-evaluate", action="store_true", help="skip the pytest harness")
    args = ap.parse_args(argv)

    try:
        from crewai import Crew, Process
    except Exception as exc:  # noqa: BLE001
        print(f"crewai is not installed: {exc}")
        print("Install it in an isolated venv (see docs/setup-guide.md).")
        return 2

    cfg = load_config(Path(args.config))
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = ROOT / "runs" / run_id
    staged = run_dir / "staged"
    staged.mkdir(parents=True, exist_ok=True)

    print(f"[run {run_id}] endpoints:")
    for name, spec in cfg["endpoints"].items():
        print(f"  {name}: {spec['base_url']}")
    print(f"[run {run_id}] role -> endpoint:")
    agents = build_agents(cfg)
    print(f"[run {run_id}] coding workers (one agent per parallel task):")
    coders = [make_coder_agent(cfg) for _ in range(4)]
    tasks = build_tasks(agents, cfg, staged, guardrails_on=not args.no_guardrails,
                        coders=coders)

    crew_kwargs: dict = {
        "agents": list(agents.values()) + coders,
        "tasks": tasks,
        "process": Process.sequential,
        "verbose": False,
    }
    if not args.no_memory:
        crew_kwargs["memory"] = True
        crew_kwargs["embedder"] = {
            "provider": "ollama",
            "config": {
                "model_name": "embeddinggemma:latest",
                "url": cfg["endpoints"]["alpha"]["base_url"] + "/api/embeddings",
            },
        }

    status, error = "ok", ""
    try:
        crew = Crew(**crew_kwargs)
        result = crew.kickoff()
        (run_dir / "crew_result.txt").write_text(str(result), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        status, error = "failed", f"{type(exc).__name__}: {exc}"
        (run_dir / "crew_error.txt").write_text(error, encoding="utf-8")
        print(f"[run {run_id}] crew FAILED: {error}")

    for i, task in enumerate(tasks, start=1):
        out = getattr(task, "output", None)
        text = getattr(out, "raw", None) or (str(out) if out is not None else "")
        (run_dir / f"task{i}_{task.agent.role.replace(' ', '_')}.txt").write_text(
            text, encoding="utf-8")

    written = sorted(p.relative_to(staged).as_posix()
                     for p in staged.rglob("*") if p.is_file())

    pytest_result = ({"exit_code": None, "output": "harness disabled"}
                     if args.no_evaluate else run_pytest(staged))
    (run_dir / "test_output.txt").write_text(pytest_result["output"], encoding="utf-8")

    manifest = {
        "run_id": run_id,
        "config": str(args.config),
        "crew_status": status,
        "crew_error": error,
        "memory": not args.no_memory,
        "guardrails": not args.no_guardrails,
        "roles": cfg["roles"],
        "files_written_by_output_file": written,
        "pytest_exit_code": pytest_result["exit_code"],
    }
    (run_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"\n[run {run_id}] crew status: {status}")
    print(f"files written by output_file ({len(written)}): {written}")
    print(f"pytest exit code (harness): {pytest_result['exit_code']}")
    print(f"run artifacts: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
