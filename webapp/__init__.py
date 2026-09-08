"""Flask dashboard and REST API for the multi-LLM workflow."""

from __future__ import annotations

import json
import re
import threading
from pathlib import Path
from typing import Dict, Optional

from flask import Flask, abort, jsonify, render_template, request

from workflow.artifacts import list_files, safe_target_path
from workflow.config import AppConfig, load_config
from workflow.llm_client import model_available, probe_endpoint
from workflow.pipeline import Pipeline, RunProgress

_RUN_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def _valid_run_id(run_id: str) -> bool:
    return bool(run_id) and bool(_RUN_ID_RE.match(run_id)) and ".." not in run_id


def collect_health(config: AppConfig) -> dict:
    endpoints = [probe_endpoint(name, url).__dict__ for name, url in config.endpoints.items()]
    roles = []
    for rname, role in config.roles.items():
        ep = next((e for e in endpoints if e["name"] == role.endpoint_name), None)
        installed = ep.get("models", []) if ep else []
        available = model_available(role.model, installed) if (ep and ep["ok"]) else False
        roles.append(
            {
                "role": rname,
                "endpoint": role.endpoint_name,
                "url": role.endpoint_url,
                "model": role.model,
                "model_available": available,
            }
        )
    all_endpoints_ok = all(e["ok"] for e in endpoints)
    all_models_ok = all(r["model_available"] for r in roles)
    if all_endpoints_ok and all_models_ok:
        status = "ok"
    elif any(e["ok"] for e in endpoints):
        status = "degraded"
    else:
        status = "down"
    return {
        "status": status,
        "endpoints": endpoints,
        "roles": roles,
        "worker_count": config.workflow.worker_count,
    }


def create_app(config: Optional[AppConfig] = None) -> Flask:
    app = Flask(__name__)
    app.config["WORKFLOW_CONFIG"] = config if config is not None else load_config()
    cfg: AppConfig = app.config["WORKFLOW_CONFIG"]

    root = Path.cwd()
    workspace_root = root / cfg.workflow.workspace_dir
    runs: Dict[str, RunProgress] = {}
    runs_lock = threading.Lock()

    def _pipeline() -> Pipeline:
        return Pipeline(cfg, workspace_root=workspace_root, root_dir=root)

    @app.get("/")
    def index():
        return render_template("index.html", health=collect_health(cfg), runs=_list_runs())

    @app.get("/api/health")
    def api_health():
        return jsonify(collect_health(cfg))

    @app.post("/api/workflow")
    def api_workflow():
        payload = request.get_json(silent=True) or {}
        requirement = str(payload.get("requirement") or "").strip()
        if not requirement:
            return jsonify({"error": "field 'requirement' is required"}), 400
        pipeline = _pipeline()
        run_id = pipeline.new_run_id()
        progress = RunProgress(run_id, requirement)
        with runs_lock:
            runs[run_id] = progress

        def _execute():
            try:
                pipeline.run(requirement, run_id=run_id, progress=progress)
            except Exception as exc:  # noqa: BLE001
                progress.finish("failed", str(exc))

        threading.Thread(target=_execute, name=f"run-{run_id}", daemon=True).start()
        return (
            jsonify(
                {
                    "run_id": run_id,
                    "status": "running",
                    "monitor": f"/runs/{run_id}",
                    "api": f"/api/runs/{run_id}",
                }
            ),
            202,
        )

    @app.get("/runs/<run_id>")
    def run_page(run_id: str):
        if not _valid_run_id(run_id):
            abort(404)
        return render_template("run.html", run_id=run_id)

    @app.get("/api/runs")
    def api_runs():
        return jsonify({"runs": _list_runs()})

    @app.get("/api/runs/<run_id>")
    def api_run(run_id: str):
        if not _valid_run_id(run_id):
            abort(404)
        run_dir = workspace_root / run_id
        with runs_lock:
            progress = runs.get(run_id)
        live = progress.snapshot() if progress else None
        manifest = None
        manifest_path = run_dir / "run.json"
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                manifest = None
        if live is None and manifest is None:
            abort(404)
        return jsonify(
            {
                "run_id": run_id,
                "live": live,
                "manifest": manifest,
                "artifacts": list_files(run_dir),
            }
        )

    @app.get("/api/runs/<run_id>/file")
    def api_run_file(run_id: str):
        if not _valid_run_id(run_id):
            abort(404)
        run_dir = workspace_root / run_id
        rel = request.args.get("path", "")
        try:
            target = safe_target_path(run_dir, rel)
        except Exception:  # noqa: BLE001
            abort(400)
        if not target.is_file():
            abort(404)
        return (
            target.read_text(encoding="utf-8", errors="replace"),
            200,
            {"Content-Type": "text/plain; charset=utf-8"},
        )

    def _list_runs() -> list:
        result = []
        if not workspace_root.exists():
            return result
        for entry in sorted(workspace_root.iterdir(), key=lambda p: p.name, reverse=True):
            if not entry.is_dir():
                continue
            status = "running"
            requirement = ""
            manifest_path = entry / "run.json"
            if manifest_path.exists():
                try:
                    data = json.loads(manifest_path.read_text(encoding="utf-8"))
                    status = data.get("status", "unknown")
                    requirement = data.get("requirement", "")
                except (ValueError, OSError):
                    status = "error"
            result.append({"run_id": entry.name, "status": status, "requirement": requirement})
        return result

    return app
