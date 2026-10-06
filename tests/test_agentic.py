"""Tests for the agentic pipeline (tool calling, handoff, ordering)."""

import ollama_workflow as m


def _tool_call(name, arguments):
    return {"function": {"name": name, "arguments": arguments}}


def test_run_tool_agent_executes_tool_calls_then_finishes(tmp_path, monkeypatch):
    calls = {"count": 0}

    def fake_chat(model, messages, tools, endpoint, timeout=300):
        calls["count"] += 1
        if calls["count"] == 1:
            return {"role": "assistant", "content": "", "tool_calls": [_tool_call("write_file", {"path": "hello.py", "content": "print('hi')\n"})]}
        return {"role": "assistant", "content": "færdig", "tool_calls": []}

    monkeypatch.setattr(m, "chat_ollama", fake_chat)
    runtime = m.ToolRuntime(str(tmp_path), apply=True)
    result = m.run_tool_agent("implementation", "mod", "http://x", "sys", "user", runtime)
    assert result["result"] == "færdig"
    assert result["rounds"] == 2
    assert result["tools"][0]["tool"] == "write_file"
    assert (tmp_path / "hello.py").read_text(encoding="utf-8") == "print('hi')\n"


def test_run_tool_agent_stops_at_max_rounds(tmp_path, monkeypatch):
    def always_tool(model, messages, tools, endpoint, timeout=300):
        return {"role": "assistant", "content": "", "tool_calls": [_tool_call("list_files", {})]}

    monkeypatch.setattr(m, "chat_ollama", always_tool)
    runtime = m.ToolRuntime(str(tmp_path))
    result = m.run_tool_agent("implementation", "mod", "http://x", "sys", "user", runtime, max_rounds=3)
    assert result["rounds"] == 3


def test_bounded_truncates_and_marks():
    bounded, truncated = m._bounded("x" * 100, 10)
    assert truncated is True
    assert bounded.startswith("x" * 10)
    assert "afkortet" in bounded


def test_bounded_keeps_short_text():
    bounded, truncated = m._bounded("kort", 100)
    assert bounded == "kort"
    assert truncated is False


def test_agentic_workflow_runs_all_agents_with_handoff(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "ARCHITECT_ENDPOINT", "http://arch")
    monkeypatch.setattr(m, "WORKER_ENDPOINT", "http://worker")
    monkeypatch.setattr(m, "verify_models", lambda: {"http://arch": ["qwen2.5-coder:7b"], "http://worker": ["llama3.2:3b"]})
    monkeypatch.setattr(m, "ask_ollama", lambda model, prompt, endpoint: f"{model}@{endpoint}")
    monkeypatch.setattr(m, "chat_ollama", lambda model, messages, tools, endpoint, timeout=300: {"role": "assistant", "content": f"tool-{model}", "tool_calls": []})

    result = m.run_agentic_workflow("krav", workspace_dir=str(tmp_path), apply=False)
    assert result["mode"] == "agentic"
    assert result["agent_count"] == len(m.AGENTS)
    assert set(result["artifacts"]) == set(m.AGENTIC_STAGES)
    assert [a["name"] for a in result["agents"]] == m.AGENTIC_STAGES + m.AGENTIC_REVIEWS
    assert len(result["handoffs"]) > 0
    # The first handoff goes from the first stage to the second stage.
    assert result["handoffs"][0]["from"] == "architecture"


def test_agentic_workflow_dry_run_does_not_write_files(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "verify_models", lambda: {m.ARCHITECT_ENDPOINT: [m.ARCHITECT_MODEL], m.WORKER_ENDPOINT: [m.WORKER_MODEL]})
    monkeypatch.setattr(m, "ask_ollama", lambda model, prompt, endpoint: "tekst")

    def fake_chat(model, messages, tools, endpoint, timeout=300):
        return {"role": "assistant", "content": "ok", "tool_calls": [_tool_call("write_file", {"path": "generated.txt", "content": "x"})]}

    monkeypatch.setattr(m, "chat_ollama", fake_chat)
    result = m.run_agentic_workflow("krav", workspace_dir=str(tmp_path), apply=False, max_rounds=1)
    assert not (tmp_path / "generated.txt").exists()
    assert result["changes"]
    assert all(change["written"] is False for change in result["changes"])


def test_extract_tool_calls_reads_arguments_key():
    calls = m._extract_tool_calls_from_content('{"name": "write_file", "arguments": {"path": "a.py", "content": "x"}}')
    assert calls[0]["function"]["name"] == "write_file"
    assert calls[0]["function"]["arguments"]["path"] == "a.py"


def test_extract_tool_calls_reads_parameters_key():
    calls = m._extract_tool_calls_from_content('{"name":"write_file","parameters":{"path":"a.py","content":"x"}}')
    assert calls[0]["function"]["arguments"]["content"] == "x"


def test_extract_tool_calls_ignores_unknown_tools():
    assert m._extract_tool_calls_from_content('{"name": "delete_everything", "arguments": {}}') == []


def test_extract_tool_calls_reads_fenced_json():
    text = 'Her er kaldet:\n```json\n{"name": "run_command", "arguments": {"command": "python -m pytest -q"}}\n```'
    calls = m._extract_tool_calls_from_content(text)
    assert calls[0]["function"]["name"] == "run_command"


def test_run_tool_agent_recovers_tool_call_from_text(tmp_path, monkeypatch):
    calls = {"count": 0}

    def fake_chat(model, messages, tools, endpoint, timeout=300):
        calls["count"] += 1
        if calls["count"] == 1:
            return {"role": "assistant", "content": '{"name": "write_file", "arguments": {"path": "from_text.py", "content": "print(1)\\n"}}', "tool_calls": []}
        return {"role": "assistant", "content": "done", "tool_calls": []}

    monkeypatch.setattr(m, "chat_ollama", fake_chat)
    runtime = m.ToolRuntime(str(tmp_path), apply=True)
    result = m.run_tool_agent("implementation", "mod", "http://x", "sys", "user", runtime)
    assert (tmp_path / "from_text.py").read_text(encoding="utf-8") == "print(1)\n"
    assert result["rounds"] == 2
