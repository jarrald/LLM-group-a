"""Tests for the lecture loader (path-derived metadata, discovery, raw-material exclusion)."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.adapters.loader import discover_lectures, load_lecture, read_lecture_title, week_number

COURSE_ID = "llms_for_devs"


def write_document(root: Path, relative: str, body: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def test_read_lecture_title_returns_first_h1() -> None:
    text = "intro\n# Real Title\n## Section\n"

    assert read_lecture_title(text, fallback="Fallback") == "Real Title"


def test_read_lecture_title_falls_back_without_h1() -> None:
    assert read_lecture_title("only body text", fallback="Fallback") == "Fallback"


def test_week_number_reads_the_directory_below_the_root(tmp_path: Path) -> None:
    path = tmp_path / "llm_friendly" / "week3" / "week3_overview.md"

    assert week_number(path, tmp_path) == 3


def test_week_number_is_none_outside_a_week_directory(tmp_path: Path) -> None:
    assert week_number(tmp_path / "notes" / "random.md", tmp_path) is None


def test_load_lecture_derives_metadata_from_path_and_heading(tmp_path: Path) -> None:
    path = write_document(tmp_path, "week3/week3_hallucinations.md", "# Week 3 — Hallucinations\n\n## Why it matters\n\nBody.\n")

    document = load_lecture(path, COURSE_ID, tmp_path)

    assert document.doc_id == "week3_hallucinations"
    assert document.lecture == 3
    assert document.doc_name == "Week 3 — Hallucinations"
    assert document.course_id == COURSE_ID
    assert document.path == path
    assert "## Why it matters" in document.text


def test_load_lecture_normalises_windows_line_endings(tmp_path: Path) -> None:
    path = write_document(tmp_path, "week1/week1.md", "# Title\r\n\r\nline one\r\n")

    assert "\r" not in load_lecture(path, COURSE_ID, tmp_path).text


def test_load_lecture_rejects_a_path_outside_a_week_directory(tmp_path: Path) -> None:
    path = write_document(tmp_path, "notes.md", "# Notes\n")

    with pytest.raises(ValueError, match="not inside a week"):
        load_lecture(path, COURSE_ID, tmp_path)


def test_discover_lectures_finds_nested_weeks_and_multiple_files_per_week(tmp_path: Path) -> None:
    write_document(tmp_path, "llm_friendly/week1/week1_complete_rag.md", "# Week one\n\nbody\n")
    write_document(tmp_path, "llm_friendly/week3/week3_overview.md", "# Week three overview\n\nbody\n")
    write_document(tmp_path, "llm_friendly/week3/week3_hallucinations.md", "# Week three hallucinations\n\nbody\n")

    documents = discover_lectures(tmp_path, COURSE_ID)

    assert [(document.lecture, document.doc_id) for document in documents] == [
        (1, "week1_complete_rag"),
        (3, "week3_hallucinations"),
        (3, "week3_overview"),
    ]


def test_discover_lectures_excludes_raw_material(tmp_path: Path) -> None:
    write_document(tmp_path, "llm_friendly/week1/week1_complete_rag.md", "# Week one\n\nbody\n")
    write_document(tmp_path, "source/week3/Web Resources.md", "# Resources\n\nlinks\n")

    documents = discover_lectures(tmp_path, COURSE_ID)

    assert [document.doc_id for document in documents] == ["week1_complete_rag"]


def test_discover_lectures_ignores_markdown_outside_week_directories(tmp_path: Path) -> None:
    write_document(tmp_path, "llm_friendly/week1/week1_complete_rag.md", "# Week one\n\nbody\n")
    write_document(tmp_path, "llm_friendly/README.md", "# Not a lecture\n\nbody\n")

    assert [document.doc_id for document in discover_lectures(tmp_path, COURSE_ID)] == ["week1_complete_rag"]


def test_discover_lectures_returns_empty_when_no_week_exists(tmp_path: Path) -> None:
    (tmp_path / "week1").mkdir()

    assert discover_lectures(tmp_path, COURSE_ID) == []


def test_discover_lectures_raises_for_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="course material directory"):
        discover_lectures(tmp_path / "does-not-exist", COURSE_ID)
