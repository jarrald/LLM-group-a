"""Unit tests for the Ollama helpers and workflow runner (no live services)."""

import json
import urllib.error

import ollama_workflow as m
import pytest


class _FakeResponse:
    def __init__(self, payload: bytes):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):
        return self._payload


def test_ask_ollama_posts_to_given_endpoint(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout=300):
        captured["url"] = request.get_full_url()
        captured["data"] = request.data
        return _FakeResponse(json.dumps({"response": "svar"}).encode("utf-8"))

    monkeypatch.setattr(m.urllib.request, "urlopen", fake_urlopen)
    result = m.ask_ollama("mod", "prompt", "http://127.0.0.1:11435")
    assert result == "svar"
    assert captured["url"] == "http://127.0.0.1:11435/api/generate"
    assert json.loads(captured["data"].decode("utf-8"))["model"] == "mod"


def test_ask_ollama_raises_on_connection_error(monkeypatch):
    def fake_urlopen(request, timeout=300):
        raise urllib.error.URLError("nede")

    monkeypatch.setattr(m.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(RuntimeError):
        m.ask_ollama("mod", "prompt", "http://127.0.0.1:11435")


def test_installed_models_parses_tags(monkeypatch):
    def fake_urlopen(url, timeout=10):
        payload = {"models": [{"name": "a"}, {"name": "b"}]}
        return _FakeResponse(json.dumps(payload).encode("utf-8"))

    monkeypatch.setattr(m.urllib.request, "urlopen", fake_urlopen)
    assert m._installed_models("http://x") == {"a", "b"}


def test_installed_models_raises_when_unreachable(monkeypatch):
    def fake_urlopen(url, timeout=10):
        raise urllib.error.URLError("nede")

    monkeypatch.setattr(m.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(RuntimeError):
        m._installed_models("http://x")


def test_verify_models_returns_endpoint_map(monkeypatch):
    monkeypatch.setattr(
        m,
        "_installed_models",
        lambda endpoint: {"qwen2.5-coder:7b", "llama3.2:3b"},
    )
    result = m.verify_models()
    assert "qwen2.5-coder:7b" in result[m.ARCHITECT_ENDPOINT]
    assert "llama3.2:3b" in result[m.WORKER_ENDPOINT]


def test_verify_models_raises_when_model_missing(monkeypatch):
    monkeypatch.setattr(m, "_installed_models", lambda endpoint: set())
    with pytest.raises(RuntimeError):
        m.verify_models()


def test_run_workflow_runs_all_agents_and_marks_endpoint(monkeypatch):
    monkeypatch.setattr(m, "ARCHITECT_ENDPOINT", "http://arch")
    monkeypatch.setattr(m, "WORKER_ENDPOINT", "http://worker")
    monkeypatch.setattr(
        m,
        "verify_models",
        lambda: {
            "http://arch": ["qwen2.5-coder:7b"],
            "http://worker": ["llama3.2:3b"],
        },
    )
    monkeypatch.setattr(m, "ask_ollama", lambda model, prompt, endpoint: f"{model}@{endpoint}")

    result = m.run_workflow("krav")
    assert result["agent_count"] == len(m.AGENTS)
    assert len(result["agents"]) == len(m.AGENTS)
    for agent in result["agents"]:
        assert agent["endpoint"] in ("http://arch", "http://worker")
        assert agent["result"].startswith(agent["model"] + "@")
    # Results are ordered back to the fixed registry order.
    assert [a["name"] for a in result["agents"]] == list(m.AGENTS)
