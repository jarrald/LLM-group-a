"""Environment-variable parsing and endpoint routing."""

import importlib

import ollama_workflow as m


def _reload():
    importlib.reload(m)


def test_endpoint_defaults_fall_back_to_ollama_url(monkeypatch):
    monkeypatch.delenv("OLLAMA_URL", raising=False)
    monkeypatch.delenv("ARCHITECT_ENDPOINT", raising=False)
    monkeypatch.delenv("WORKER_ENDPOINT", raising=False)
    _reload()
    assert m.ARCHITECT_ENDPOINT == "http://localhost:11434"
    assert m.WORKER_ENDPOINT == "http://localhost:11434"


def test_endpoints_are_independently_configurable(monkeypatch):
    monkeypatch.setenv("ARCHITECT_ENDPOINT", "http://127.0.0.1:11434")
    monkeypatch.setenv("WORKER_ENDPOINT", "http://127.0.0.1:11435")
    _reload()
    assert m.ARCHITECT_ENDPOINT == "http://127.0.0.1:11434"
    assert m.WORKER_ENDPOINT == "http://127.0.0.1:11435"


def test_model_defaults(monkeypatch):
    monkeypatch.delenv("ARCHITECT_MODEL", raising=False)
    monkeypatch.delenv("WORKER_MODEL", raising=False)
    _reload()
    assert m.ARCHITECT_MODEL == "qwen2.5-coder:7b"
    assert m.WORKER_MODEL == "llama3.2:3b"


def test_architect_role_agents_route_to_architect_endpoint(monkeypatch):
    monkeypatch.setattr(m, "ARCHITECT_ENDPOINT", "http://arch")
    monkeypatch.setattr(m, "WORKER_ENDPOINT", "http://worker")
    for name in m.ARCHITECT_ROLE_AGENTS:
        assert m.endpoint_for(name) == "http://arch"


def test_non_architect_agents_route_to_worker_endpoint(monkeypatch):
    monkeypatch.setattr(m, "ARCHITECT_ENDPOINT", "http://arch")
    monkeypatch.setattr(m, "WORKER_ENDPOINT", "http://worker")
    for name in m.AGENTS:
        if name not in m.ARCHITECT_ROLE_AGENTS:
            assert m.endpoint_for(name) == "http://worker"
