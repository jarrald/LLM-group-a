"""Unit tests for the agentic tool layer (sandbox, file ops, command gate)."""

import ollama_workflow as m


def test_write_file_rejects_path_traversal(tmp_path):
    runtime = m.ToolRuntime(str(tmp_path))
    result = runtime.write_file("../evil.txt", "x")
    assert "uden for workspace" in result
    assert not (tmp_path.parent / "evil.txt").exists()


def test_write_file_dry_run_records_diff_without_writing(tmp_path):
    runtime = m.ToolRuntime(str(tmp_path))
    result = runtime.write_file("src/app.py", "print(1)\n")
    assert "foreslået" in result
    assert not (tmp_path / "src" / "app.py").exists()
    assert len(runtime.changes) == 1
    change = runtime.changes[0]
    assert change["path"] == "src/app.py"
    assert change["written"] is False
    assert "+print(1)" in change["diff"]


def test_write_file_apply_creates_file(tmp_path):
    runtime = m.ToolRuntime(str(tmp_path), apply=True)
    runtime.write_file("src/app.py", "print(1)\n")
    assert (tmp_path / "src" / "app.py").read_text(encoding="utf-8") == "print(1)\n"
    assert runtime.changes[0]["written"] is True


def test_write_file_diff_shows_overwrite(tmp_path):
    (tmp_path / "notes.txt").write_text("old\n", encoding="utf-8")
    runtime = m.ToolRuntime(str(tmp_path), apply=True)
    runtime.write_file("notes.txt", "new\n")
    diff = runtime.changes[0]["diff"]
    assert "-old" in diff
    assert "+new" in diff


def test_list_files_and_read_file(tmp_path):
    runtime = m.ToolRuntime(str(tmp_path), apply=True)
    runtime.write_file("a.txt", "hello")
    runtime.write_file("pkg/b.txt", "world")
    listing = runtime.list_files(".")
    assert "a.txt" in listing
    assert "pkg/b.txt" in listing
    assert runtime.read_file("a.txt") == "hello"


def test_read_missing_file_reports_error(tmp_path):
    runtime = m.ToolRuntime(str(tmp_path))
    assert "findes ikke" in runtime.read_file("nope.txt")


def test_run_command_rejects_disallowed_command(tmp_path):
    runtime = m.ToolRuntime(str(tmp_path), apply=True)
    result = runtime.run_command("rm -rf /")
    assert "Afvist" in result
    assert runtime.commands == []


def test_run_command_dry_run_is_only_planned(tmp_path):
    runtime = m.ToolRuntime(str(tmp_path))
    result = runtime.run_command("python -m pytest -q")
    assert "Planlagt" in result
    assert runtime.commands[0]["executed"] is False


def test_run_command_apply_executes_allowlisted_command(tmp_path):
    runtime = m.ToolRuntime(str(tmp_path), apply=True)
    result = runtime.run_command("python -m pytest --version")
    assert runtime.commands[0]["executed"] is True
    assert runtime.commands[0]["exit_code"] == 0
    assert "exit=0" in result


def test_dispatch_reports_unknown_tool(tmp_path):
    runtime = m.ToolRuntime(str(tmp_path))
    assert "Ukendt værktøj" in runtime.dispatch("nope", {})
