"""Candidate B -- CrewAI role-based multi-agent orchestration (evaluated).

A "crew" of six role agents (architect, tech lead, coder, tester, docs, deploy)
where each agent is bound to a model on a *different* local Ollama endpoint via
the config file. Tasks run sequentially and the host script collects the text
output into the same artifact layout as Candidate A so the two can be compared.

Run (from the repository root, inside a venv with crewai installed):
    python candidate_b_crewai/crew.py --run-id runB_demo
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

PROJECT_NAME = "TaskFlow API"
PROJECT_BRIEF = (
    'Build "TaskFlow API": a tiny, dependency-free task/todo REST API in pure '
    "Python 3 standard library (http.server + json). Modules: "
    "src/taskflow/store.py (class TaskStore, in-memory CRUD), "
    "src/taskflow/service.py (class TaskService, validation: empty/whitespace/"
    "too-long title raises ValueError), src/taskflow/api.py (HTTP handler + "
    "make_server()), src/taskflow/__main__.py (starts server on PORT or 8080). "
    "A Task has id (int, sequential from 1), title (str, 1..100), done (bool). "
    "A Task is a PLAIN DICT {id,title,done}; there is no models.py, and modules "
    "may only import from the five listed files."
)


def load_config(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def make_llm(cfg: dict, role: str):
    """Bind a CrewAI LLM to the endpoint configured for a role."""
    from crewai import LLM

    spec = cfg["roles"][role]
    base_url = cfg["endpoints"][spec["endpoint"]]["base_url"]
    return LLM(
        model=f"ollama/{spec['model']}",
        base_url=base_url,
        temperature=cfg.get("defaults", {}).get("temperature", 0.2),
        timeout=cfg.get("defaults", {}).get("request_timeout_s", 900),
    )


def build_agents(cfg: dict):
    from crewai import Agent

    return {
        "architect": Agent(
            role="Software Architect",
            goal="Produce component decomposition, interface contracts and deployment topology",
            backstory="You design small, dependency-free Python services.",
            llm=make_llm(cfg, "architect"),
            verbose=False,
            allow_delegation=False,
        ),
        "techlead": Agent(
            role="Tech Lead",
            goal="Break work into incremental tickets with scope, acceptance criteria and ordering",
            backstory="You split work by file so multiple coders can work in parallel.",
            llm=make_llm(cfg, "techlead"),
            verbose=False,
            allow_delegation=False,
        ),
        "coder": Agent(
            role="Python Developer",
            goal="Implement the ticketed files using only the standard library",
            backstory="You always emit fenced code blocks headed by '# file: <path>'.",
            llm=make_llm(cfg, "coder"),
            verbose=False,
            allow_delegation=False,
        ),
        "tester": Agent(
            role="QA Engineer",
            goal="Write pytest tests covering the acceptance criteria",
            backstory="You test edge cases such as invalid titles and missing ids.",
            llm=make_llm(cfg, "tester"),
            verbose=False,
            allow_delegation=False,
        ),
        "docs": Agent(
            role="Technical Writer",
            goal="Produce README, API usage and runbook documentation",
            backstory="You write concise, runnable Markdown docs.",
            llm=make_llm(cfg, "docs"),
            verbose=False,
            allow_delegation=False,
        ),
        "deploy": Agent(
            role="DevOps Engineer",
            goal="Produce a Dockerfile and a stdlib deploy-validation script",
            backstory="You keep deployment artifacts minimal and correct.",
            llm=make_llm(cfg, "deploy"),
            verbose=False,
            allow_delegation=False,
        ),
    }


def build_tasks(agents: dict):
    from crewai import Task

    t_arch = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite a Markdown architecture document with "
        "sections: Components (table), Interface contracts, Deployment topology, "
        "Constraints and risks.",
        expected_output="A concise Markdown architecture document.",
        agent=agents["architect"],
    )
    t_plan = Task(
        description=f"{PROJECT_BRIEF}\n\nBreak the work into 3 tickets by file "
        "(store.py, service.py, api.py). For each: id, title, scope, acceptance "
        "criteria, depends_on.",
        expected_output="A JSON array of 3 tickets.",
        agent=agents["techlead"],
        context=[t_arch],
    )
    t_code = Task(
        description=f"{PROJECT_BRIEF}\n\nImplement store.py, service.py and api.py. "
        "Output ONLY fenced code blocks, each immediately preceded by a line "
        "'# file: <relative/path.py>'.",
        expected_output="Three fenced Python code blocks with file headers.",
        agent=agents["coder"],
        context=[t_plan],
    )
    t_test = Task(
        description=f"{PROJECT_BRIEF}\n\nWrite pytest tests in tests/test_store.py and "
        "tests/test_service.py. Import as 'from taskflow.store import TaskStore'.",
        expected_output="Two fenced Python test files with file headers.",
        agent=agents["tester"],
        context=[t_code],
    )
    t_docs = Task(
        description=f"{PROJECT_BRIEF}\n\nProduce README.md, docs/api-usage.md and "
        "docs/runbook.md as fenced blocks each preceded by '# file:'.",
        expected_output="Three fenced Markdown documents.",
        agent=agents["docs"],
        context=[t_arch],
    )
    t_deploy = Task(
        description=f"{PROJECT_BRIEF}\n\nProduce Dockerfile and "
        "deploy/validate_deploy.py (stdlib-only; starts the server on a free port, "
        "hits /healthz and /tasks, prints 'DEPLOY OK'). Fenced blocks with '# file:'.",
        expected_output="Two fenced files with file headers.",
        agent=agents["deploy"],
        context=[t_code],
    )
    return [t_arch, t_plan, t_code, t_test, t_docs, t_deploy]


# --- minimal tolerant parser (mirrors Candidate A so results are comparable) ---
FENCE_RE = re.compile(r"```[ \t]*([a-zA-Z0-9_+-]*)[ \t]*\r?\n(.*?)```", re.DOTALL)
FILE_HINT_RE = re.compile(
    r"^\s*(?:#|//)\s*(?:file|filename|path)\s*[:=]\s*(.+?)\s*$", re.IGNORECASE
)


def extract_files(text: str) -> dict[str, str]:
    files: dict[str, str] = {}
    lines = text.splitlines()
    hint_at: dict[int, str] = {}
    for i, line in enumerate(lines):
        m = FILE_HINT_RE.match(line)
        if m:
            p = m.group(1).strip().strip("`").strip("\"'")
            if p and ".." not in p.split("/"):
                hint_at[i] = p.replace("\\", "/").lstrip("/")
    for m in FENCE_RE.finditer(text):
        body = m.group(2)
        path = None
        first, _, rest = body.partition("\n")
        inner = FILE_HINT_RE.match(first)
        if inner:
            path, body = inner.group(1).strip().strip("`").strip("\"'"), rest
        if path is None:
            fl = text[: m.start()].count("\n")
            for back in range(1, 4):
                if (fl - back) in hint_at:
                    path = hint_at[fl - back]
                    break
        if path:
            files[path.replace("\\", "/").lstrip("/")] = body.strip("\n")
    return files


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="CrewAI multi-LLM workflow (Candidate B)")
    ap.add_argument("--config", default=str(ROOT / "config" / "endpoints.yaml"))
    ap.add_argument("--run-id", default=None)
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
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"[run {run_id}] building crew (6 role agents, 2 endpoints)")
    agents = build_agents(cfg)
    tasks = build_tasks(agents)
    crew = Crew(agents=list(agents.values()), tasks=tasks,
                process=Process.sequential, verbose=False)

    result = crew.kickoff()

    collected: dict[str, str] = {}
    for i, task in enumerate(tasks, start=1):
        out = getattr(task, "output", None)
        text = getattr(out, "raw", None) or (str(out) if out is not None else "")
        (run_dir / f"task{i}_{task.agent.role.replace(' ', '_')}.md").write_text(
            text, encoding="utf-8")
        collected.update(extract_files(text))

    staged = run_dir / "staged"
    for rel, content in collected.items():
        target = staged / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.rstrip("\n") + "\n", encoding="utf-8")

    (run_dir / "crew_result.txt").write_text(str(result), encoding="utf-8")
    summary = {"run_id": run_id, "config": str(args.config),
               "roles": cfg["roles"], "artifacts": sorted(collected)}
    (run_dir / "run_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"files collected: {sorted(collected)}")
    print(f"run artifacts: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())