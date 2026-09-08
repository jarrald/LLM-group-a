from pathlib import Path

import pytest

from workflow.config import load_config
from workflow.llm_client import EndpointHealth

ROOT = Path(__file__).resolve().parents[1]


def _canned_health(name, url):
    return EndpointHealth(
        name=name, url=url, ok=True, models=["qwen2.5-coder:7b", "llama3.2:3b"]
    )


@pytest.fixture()
def client(tmp_path, monkeypatch):
    from webapp import create_app

    cfg = load_config(str(ROOT / "config.yaml"))
    cfg.workflow.workspace_dir = str(tmp_path)

    monkeypatch.setattr(
        "webapp.probe_endpoint", lambda name, url, timeout=5: _canned_health(name, url)
    )
    app = create_app(cfg)
    app.config["TESTING"] = True
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert len(data["endpoints"]) >= 2
    assert len(data["roles"]) >= 3


def test_workflow_requires_requirement(client):
    response = client.post("/api/workflow", json={})
    assert response.status_code == 400
    assert "requirement" in response.get_json()["error"]


def test_runs_list_empty(client):
    response = client.get("/api/runs")
    assert response.status_code == 200
    assert response.get_json() == {"runs": []}
