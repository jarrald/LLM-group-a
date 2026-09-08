import pytest

from workflow.artifacts import (
    ArtifactError,
    FileBlock,
    extract_json,
    extract_yaml,
    parse_file_blocks,
    safe_target_path,
    write_file_blocks,
)


def test_parse_explicit_blocks_preserves_fences_inside():
    text = (
        "=== FILE: app.py ===\n"
        "def f():\n"
        "    return '```not a fence```'\n"
        "=== END FILE ===\n"
        "=== FILE: docs/readme.md ===\n"
        "# Hi\n"
        "=== END FILE ===\n"
    )
    blocks = parse_file_blocks(text)
    assert [b.path for b in blocks] == ["app.py", "docs/readme.md"]
    assert "```not a fence```" in blocks[0].content


def test_parse_fenced_fallback():
    text = "```path: app.py\nprint('hi')\n```\n```path: docs/x.md\n# X\n```"
    blocks = parse_file_blocks(text)
    assert [b.path for b in blocks] == ["app.py", "docs/x.md"]


def test_parse_none():
    assert parse_file_blocks("just prose, nothing here") == []


def test_extract_json_from_fence_and_bare():
    assert extract_json('Here:\n```json\n{"tickets": []}\n```') == {"tickets": []}
    assert extract_json('prefix {"a": 1, "b": [1, 2]} suffix') == {"a": 1, "b": [1, 2]}


def test_extract_json_returns_none_on_garbage():
    assert extract_json("no json here") is None


def test_extract_yaml():
    data = extract_yaml("```yaml\nopenapi: 3.0.3\ninfo: {}\npaths: {}\n```")
    assert data["openapi"] == "3.0.3"


def test_safe_target_path_rejects_traversal(tmp_path):
    with pytest.raises(ArtifactError):
        safe_target_path(tmp_path, "../evil.py")
    with pytest.raises(ArtifactError):
        safe_target_path(tmp_path, "/etc/passwd")
    with pytest.raises(ArtifactError):
        safe_target_path(tmp_path, "C:\\Windows\\evil.txt")


def test_write_file_blocks(tmp_path):
    written = write_file_blocks(tmp_path, [FileBlock(path="a/b/c.txt", content="hello\n")])
    assert written == ["a/b/c.txt"]
    assert (tmp_path / "a" / "b" / "c.txt").read_text() == "hello\n"
