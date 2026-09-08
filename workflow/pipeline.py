"""Pipeline orchestration: Architect -> Tech lead -> Worker pool.

Parallelism (FR3): tickets are grouped into dependency waves; every ticket in a
wave is dispatched concurrently to the coding-worker pool
(``ThreadPoolExecutor`` with ``workflow.worker_count`` workers).
"""

from __future__ import annotations

import difflib
import itertools
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .agents.architect import run_architect
from .agents.tech_lead import Ticket, run_tech_lead
from .agents.worker import run_worker
from .artifacts import list_files
from .config import AppConfig
from .llm_client import LLMClient


class DependencyCycleError(Exception):
    """Raised when ticket dependencies contain a cycle."""


@dataclass
class TicketRecord:
    ticket_id: str
    title: str
    status: str  # ok | failed | skipped
    worker: Optional[str] = None
    files: List[str] = field(default_factory=list)
    error: Optional[str] = None
    duration_s: float = 0.0

    def to_dict(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "title": self.title,
            "status": self.status,
            "worker": self.worker,
            "files": self.files,
            "error": self.error,
            "duration_s": round(self.duration_s, 2),
        }


class RunProgress:
    """Thread-safe live progress shared between the pipeline thread and the UI."""

    def __init__(self, run_id: str, requirement: str) -> None:
        self._lock = threading.Lock()
        self._data = {
            "run_id": run_id,
            "requirement": requirement,
            "status": "running",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "stages": {},
            "tickets": {},
            "error": None,
        }

    def set_stage(self, name: str, status: str, detail: Optional[str] = None) -> None:
        with self._lock:
            self._data["stages"][name] = {"status": status, "detail": detail}

    def set_ticket(self, ticket_id: str, status: str, detail: Optional[str] = None) -> None:
        with self._lock:
            self._data["tickets"][ticket_id] = {"status": status, "detail": detail}

    def finish(self, status: str, error: Optional[str] = None) -> None:
        with self._lock:
            self._data["status"] = status
            self._data["error"] = error

    def snapshot(self) -> dict:
        with self._lock:
            return json.loads(json.dumps(self._data))


@dataclass
class RunResult:
    run_id: str
    requirement: str
    status: str
    workspace_dir: Path
    stages: Dict[str, dict]
    tickets: List[dict]
    duration_s: float
    error: Optional[str] = None


class StageFailure(Exception):
    """Raised when a required stage fails and the run cannot continue."""

    def __init__(self, stage: str, message: str) -> None:
        super().__init__(f"{stage}: {message}")
        self.stage = stage
        self.message = message


def plan_waves(tickets: List[Ticket]) -> List[List[str]]:
    """Return ticket ids grouped into dependency waves (Kahn's algorithm)."""
    ids = [t.id for t in tickets]
    deps = {t.id: {d for d in t.depends_on if d in ids} for t in tickets}
    waves: List[List[str]] = []
    remaining = dict(deps)
    while remaining:
        ready = sorted(i for i, d in remaining.items() if not d)
        if not ready:
            raise DependencyCycleError(
                "dependency cycle among tickets: " + ", ".join(sorted(remaining))
            )
        waves.append(ready)
        for i in ready:
            del remaining[i]
        for i, d in remaining.items():
            d -= set(ready)
    return waves


class Pipeline:
    def __init__(
        self,
        config: AppConfig,
        workspace_root: Optional[Path] = None,
        root_dir: Optional[Path] = None,
    ) -> None:
        self.config = config
        self.root_dir = Path(root_dir or Path.cwd())
        self.workspace_root = Path(
            workspace_root or (self.root_dir / config.workflow.workspace_dir)
        )

    def new_run_id(self) -> str:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_id = f"run-{stamp}"
        counter = 1
        while (self.workspace_root / run_id).exists():
            counter += 1
            run_id = f"run-{stamp}-{counter}"
        return run_id

    def client_for(self, role_name: str) -> LLMClient:
        return LLMClient.for_role(
            self.config.roles[role_name], self.config.workflow.request_timeout_seconds
        )

    def run(
        self,
        requirement: str,
        run_id: Optional[str] = None,
        progress: Optional[RunProgress] = None,
    ) -> RunResult:
        run_id = run_id or self.new_run_id()
        progress = progress or RunProgress(run_id, requirement)
        started = time.time()

        run_dir = self.workspace_root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "docs").mkdir(exist_ok=True)
        (run_dir / "tickets").mkdir(exist_ok=True)
        (run_dir / "repo").mkdir(exist_ok=True)

        stages: Dict[str, dict] = {}
        ticket_records: List[TicketRecord] = []
        status = "failed"
        error: Optional[str] = None

        try:
            # ---- Stage 1: Architect (FR1) ----
            progress.set_stage("architect", "running")
            arch = run_architect(
                self.client_for("architect"),
                requirement,
                run_dir,
                max_retries=self.config.workflow.max_retries,
            )
            stages["architect"] = arch.result.to_dict()
            if not arch.result.ok:
                raise StageFailure("architect", arch.result.error or "failed")
            progress.set_stage("architect", "ok", arch.result.detail)

            # ---- Stage 2: Tech lead (FR2) ----
            progress.set_stage("tech_lead", "running")
            tl_result, tickets = run_tech_lead(
                self.client_for("tech_lead"),
                requirement,
                arch.tech_lead_context,
                run_dir,
                max_retries=self.config.workflow.max_retries,
            )
            stages["tech_lead"] = tl_result.to_dict()
            if not tl_result.ok or not tickets:
                raise StageFailure("tech_lead", tl_result.error or "no tickets")
            progress.set_stage("tech_lead", "ok", tl_result.detail)

            # ---- Stage 3: Workers (FR3) ----
            waves = plan_waves(tickets)
            ticket_map = {t.id: t for t in tickets}
            failed_ids: set = set()
            worker_names = itertools.cycle(
                [f"worker-{i + 1}" for i in range(self.config.workflow.worker_count)]
            )
            name_lock = threading.Lock()
            repo_dir = run_dir / "repo"

            def next_worker() -> str:
                with name_lock:
                    return next(worker_names)

            def do_ticket(tid: str) -> TicketRecord:
                ticket = ticket_map[tid]
                wname = next_worker()
                result = run_worker(
                    self.client_for("worker"),
                    ticket,
                    arch.worker_context,
                    repo_dir,
                    max_retries=self.config.workflow.max_retries,
                    worker_name=wname,
                )
                return TicketRecord(
                    ticket_id=tid,
                    title=ticket.title,
                    status="ok" if result.ok else "failed",
                    worker=wname,
                    files=result.files,
                    error=result.error,
                    duration_s=result.duration_s,
                )

            with ThreadPoolExecutor(
                max_workers=self.config.workflow.worker_count,
                thread_name_prefix="coding-worker",
            ) as pool:
                for wave_no, wave in enumerate(waves, 1):
                    progress.set_stage(
                        "workers", "running", f"wave {wave_no}/{len(waves)}: {wave}"
                    )
                    runnable = [
                        tid
                        for tid in wave
                        if not any(d in failed_ids for d in ticket_map[tid].depends_on)
                    ]
                    for tid in wave:
                        if tid not in runnable:
                            ticket_records.append(
                                TicketRecord(
                                    ticket_id=tid,
                                    title=ticket_map[tid].title,
                                    status="skipped",
                                )
                            )
                            progress.set_ticket(tid, "skipped", "dependency failed")
                    futures = {pool.submit(do_ticket, tid): tid for tid in runnable}
                    for future in as_completed(futures):
                        record = future.result()
                        ticket_records.append(record)
                        progress.set_ticket(
                            record.ticket_id,
                            record.status,
                            f"{record.worker}: {len(record.files)} files"
                            if record.status == "ok"
                            else record.error,
                        )
                        if record.status == "failed":
                            failed_ids.add(record.ticket_id)

            stages["workers"] = {
                "ok": True,
                "detail": (
                    f"{len(ticket_records)} tickets processed across {len(waves)} waves"
                ),
            }
            progress.set_stage("workers", "ok", stages["workers"]["detail"])

            if any(r.status == "failed" for r in ticket_records):
                status = "completed_with_failures"
            else:
                status = "completed"
        except StageFailure as exc:
            error = str(exc)
            progress.set_stage(exc.stage, "failed", exc.message)
        except DependencyCycleError as exc:
            error = str(exc)
        except Exception as exc:  # noqa: BLE001 - surface unexpected failures
            error = f"unexpected error: {exc}"

        duration_s = time.time() - started
        diff_path = self._write_diff(run_dir / "repo", run_dir / "changes.diff")
        artifacts = list_files(run_dir)
        manifest = {
            "run_id": run_id,
            "requirement": requirement,
            "status": status if not error else "failed",
            "started_at": progress.snapshot().get("started_at"),
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "duration_s": round(duration_s, 2),
            "config": self._config_summary(),
            "stages": stages,
            "tickets": [r.to_dict() for r in ticket_records],
            "artifacts": artifacts,
            "diff": diff_path.name if diff_path else None,
            "error": error,
        }
        (run_dir / "run.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        progress.finish(manifest["status"], error)
        return RunResult(
            run_id=run_id,
            requirement=requirement,
            status=manifest["status"],
            workspace_dir=run_dir,
            stages=stages,
            tickets=[r.to_dict() for r in ticket_records],
            duration_s=duration_s,
            error=error,
        )

    def _config_summary(self) -> dict:
        return {
            "endpoints": self.config.endpoints,
            "roles": {
                name: {
                    "endpoint": r.endpoint_name,
                    "url": r.endpoint_url,
                    "model": r.model,
                }
                for name, r in self.config.roles.items()
            },
            "worker_count": self.config.workflow.worker_count,
        }

    @staticmethod
    def _write_diff(repo_dir: Path, diff_path: Path) -> Optional[Path]:
        files = sorted(p for p in repo_dir.rglob("*") if p.is_file())
        if not files:
            return None
        chunks: List[str] = []
        for path in files:
            rel = path.relative_to(repo_dir).as_posix()
            content = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
            chunks.append(
                "".join(
                    difflib.unified_diff(
                        [], content, fromfile="/dev/null", tofile=f"b/{rel}", lineterm=""
                    )
                )
            )
        diff_path.write_text("".join(chunks), encoding="utf-8")
        return diff_path
