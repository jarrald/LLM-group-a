"""Focused tests for the workflow's parsers and control mechanism (no LLM calls).

Run:  python -m pytest candidate_a_langgraph/test_control.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import orchestrator as orch  # noqa: E402


def test_extract_files_marker_sections():
    text = "# file: README.md\n\nhello\n\n# file: docs/a.md\n\nworld\n"
    files = orch.extract_files(text)
    assert files["README.md"].strip() == "hello"
    assert files["docs/a.md"].strip() == "world"


def test_extract_files_fenced_with_preceding_hint():
    text = "# file: src/x.py\n\n```python\nprint('hi')\n```\n"
    files = orch.extract_files(text)
    assert "src/x.py" in files
    assert "print('hi')" in files["src/x.py"]


def test_sanitize_relpath_blocks_traversal():
    assert orch.sanitize_relpath("../etc/passwd") is None
    assert orch.sanitize_relpath("/abs/x.py") == "abs/x.py"


def test_batches_respects_dependencies():
    tickets = [
        {"id": "T1", "depends_on": []},
        {"id": "T2", "depends_on": ["T1"]},
        {"id": "T3", "depends_on": ["T1"]},
    ]
    batches = orch._batches(tickets)
    assert [t["id"] for t in batches[0]] == ["T1"]
    assert sorted(t["id"] for t in batches[1]) == ["T2", "T3"]


def test_review_mode_does_not_touch_project(tmp_path):
    project = tmp_path / "proj"
    project.mkdir()
    (project / "keep.txt").write_text("original", encoding="utf-8")
    staged = tmp_path / "staged"
    staged.mkdir()
    (staged / "new.txt").write_text("new", encoding="utf-8")
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    orch.RT.clear()
    orch.RT.update(project=project, staged=staged, run_dir=run_dir, cfg={}, client=None)
    orch.node_apply({"run_id": "t", "control": "review"})

    assert (project / "keep.txt").read_text(encoding="utf-8") == "original"
    assert not (project / "new.txt").exists()
    assert (run_dir / "diff.patch").exists()


def test_apply_mode_syncs_project(tmp_path):
    project = tmp_path / "proj"
    project.mkdir()
    (project / "old.txt").write_text("old", encoding="utf-8")
    staged = tmp_path / "staged"
    staged.mkdir()
    (staged / "new.txt").write_text("new", encoding="utf-8")
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    orch.RT.clear()
    orch.RT.update(project=project, staged=staged, run_dir=run_dir, cfg={}, client=None)
    orch.node_apply({"run_id": "t", "control": "apply"})

    assert (project / "new.txt").read_text(encoding="utf-8").strip() == "new"
    assert not (project / "old.txt").exists()
