"""Conversion safeguards: source coverage, code preservation and private-file exclusion."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.convert_course_material import MARKER, convert, diagram_markdown, notebook_markdown, source_files, text_markdown


def test_source_discovery_prunes_private_configuration_and_environments(tmp_path: Path) -> None:
    for relative in ("week6/notes.txt", "week6/.env", "week6/.env.example", "week6/.venv/secret.txt", "week6/__pycache__/cached.pyc"):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("private or course content", encoding="utf-8")

    assert [path.relative_to(tmp_path).as_posix() for path in source_files(tmp_path)] == ["week6/notes.txt"]


def test_notebook_preserves_cells_without_claiming_saved_outputs_as_results(tmp_path: Path) -> None:
    path = tmp_path / "lesson.ipynb"
    path.write_text(
        json.dumps(
            {
                "cells": [
                    {"cell_type": "markdown", "source": ["# Overskrift\n", "Forklaring."]},
                    {"cell_type": "code", "source": ["# Kommentar\n", "print(123)"], "outputs": [{"text": ["SENSITIVE OUTPUT"]}]},
                ]
            }
        ),
        encoding="utf-8",
    )

    converted = notebook_markdown(path)

    assert "Forklaring." in converted
    assert "# Kommentar\nprint(123)" in converted
    assert "SENSITIVE OUTPUT" not in converted
    assert converted.index("Forklaring.") < converted.index("print(123)")


def test_mislabeled_markdown_is_rendered_as_python(tmp_path: Path) -> None:
    path = tmp_path / "README.md"
    path.write_text("import os\n\n# Kommentar\nprint(os.name)\n", encoding="utf-8")

    converted = text_markdown(path)

    assert "```python" in converted
    assert "# Kommentar" in converted


def test_drawio_preserves_relationship_endpoints(tmp_path: Path) -> None:
    path = tmp_path / "architecture.drawio"
    path.write_text(
        '<mxfile><diagram name="Flow"><mxGraphModel><root><mxCell id="a" value="Coder"/><mxCell id="b" value="Reviewer"/><mxCell id="c" edge="1" source="a" target="b" value="review"/></root></mxGraphModel></diagram></mxfile>',
        encoding="utf-8",
    )

    converted = diagram_markdown(path)

    assert "Coder → Reviewer" in converted
    assert "review" in converted


def test_conversion_is_repeatable_and_deduplicates_identical_sources(tmp_path: Path) -> None:
    source, output = tmp_path / "source", tmp_path / "llm_friendly"
    (source / "week6").mkdir(parents=True)
    for name in ("notes.txt", "notes (2).txt"):
        (source / "week6" / name).write_text("Undervisningsmateriale om retrieval.\n", encoding="utf-8")

    first = convert(source, output)
    first_files = {path.name: path.read_bytes() for path in output.rglob("*.md")}
    second = convert(source, output)

    assert first == second
    assert {record["status"] for record in first["files"]} == {"converted", "duplicate"}
    assert first_files == {path.name: path.read_bytes() for path in output.rglob("*.md")}
    assert len(first_files) == 1
    assert all(content.startswith(MARKER.encode()) for content in first_files.values())
