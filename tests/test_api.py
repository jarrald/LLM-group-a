"""Flask route tests using the built-in test client (no live services)."""

import ollama_workflow as m


def test_health_ok_reports_endpoints(monkeypatch):
    monkeypatch.setattr(
        m,
        "verify_models",
        lambda: {
            "http://arch": ["qwen2.5-coder:7b"],
            "http://worker": ["llama3.2:3b"],
        },
    )
    client = m.app.test_client()
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert "endpoints" in data
    assert set(data["models"]) == {"qwen2.5-coder:7b", "llama3.2:3b"}


def test_health_error_when_verify_fails(monkeypatch):
    def boom():
        raise RuntimeError("nede")

    monkeypatch.setattr(m, "verify_models", boom)
    client = m.app.test_client()
    resp = client.get("/api/health")
    assert resp.status_code == 503
    assert resp.get_json()["status"] == "error"


def test_workflow_rejects_empty_requirement():
    client = m.app.test_client()
    resp = client.post("/api/workflow", json={"requirement": "   "})
    assert resp.status_code == 400


def test_workflow_returns_run_result(monkeypatch):
    monkeypatch.setattr(
        m,
        "run_workflow",
        lambda requirement: {"requirement": requirement, "agent_count": 10, "agents": []},
    )
    client = m.app.test_client()
    resp = client.post("/api/workflow", json={"requirement": "x"})
    assert resp.status_code == 200
    assert resp.get_json()["agent_count"] == 10
