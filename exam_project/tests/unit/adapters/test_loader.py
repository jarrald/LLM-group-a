"""Tests for the lecture loader (path-derived metadata, discovery)."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.adapters.loader import discover_lectures, load_lecture, read_lecture_title

COURSE_ID = "llms_for_devs"


def write_week(root: Path, week: int, body: str) -> Path:
    week_directory = root / f"week{week}"
    week_directory.mkdir(parents=True, exist_ok=True)
    path = week_directory / f"week{week}_complete_rag.md"
    path.write_text(body, encoding="utf-8")
    return path


def test_read_lecture_title_returns_first_h1() -> None:
    text = "intro\n# Real Title\n## Section\n"

    assert read_lecture_title(text, fallback="Fallback") == "Real Title"


def test_read_lecture_title_falls_back_without_h1() -> None:
    assert read_lecture_title("only body text", fallback="Fallback") == "Fallback"


def test_load_lecture_derives_metadata_from_path_and_heading(tmp_path: Path) -> None:
    path = write_week(tmp_path, 3, "# Week 3 — Embeddings\n\n## Why it matters\n\nBody.\n")

    document = load_lecture(path, COURSE_ID)

    assert document.doc_id == "week-3"
    assert document.lecture == 3
    assert document.doc_name == "Week 3 — Embeddings"
    assert document.course_id == COURSE_ID
    assert document.path == path
    assert "## Why it matters" in document.text


def test_load_lecture_normalises_windows_line_endings(tmp_path: Path) -> None:
    path = write_week(tmp_path, 1, "# Title\r\n\r\nline one\r\n")

    document = load_lecture(path, COURSE_ID)

    assert "\r" not in document.text


def test_discover_lectures_orders_by_week_and_ignores_other_directories(tmp_path: Path) -> None:
    write_week(tmp_path, 2, "# Week two\n\nbody\n")
    write_week(tmp_path, 1, "# Week one\n\nbody\n")
    (tmp_path / "source").mkdir()
    (tmp_path / "source" / "Week1.pdf").write_text("not markdown", encoding="utf-8")

    documents = discover_lectures(tmp_path, COURSE_ID)

    assert [document.lecture for document in documents] == [1, 2]


def test_discover_lectures_skips_week_directory_without_markdown(tmp_path: Path) -> None:
    write_week(tmp_path, 1, "# Week one\n\nbody\n")
    (tmp_path / "week2").mkdir()

    documents = discover_lectures(tmp_path, COURSE_ID)

    assert [document.lecture for document in documents] == [1]


def test_discover_lectures_raises_for_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="course material directory"):
        discover_lectures(tmp_path / "does-not-exist", COURSE_ID)
