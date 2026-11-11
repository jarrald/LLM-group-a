"""Tests for the corpus digest that makes a stale index detectable."""

from __future__ import annotations

from pathlib import Path

from app.adapters.chunker import chunk_document, chunks_digest
from app.adapters.loader import LectureDocument


def make_document(path: Path, text: str) -> LectureDocument:
    return LectureDocument(doc_id="week-1", doc_name="Week 1", lecture=1, course_id="llms_for_devs", path=path, text=text)


TEXT = """# Week 1

## 1. Foundations

A model is a simplified representation of a problem, kept short enough for a chunk.

## 2. Overfitting

Overfitting happens when a model memorises the training data instead of the pattern.
"""


def test_chunks_digest_ignores_chunk_order(tmp_path: Path) -> None:
    chunks = chunk_document(make_document(tmp_path / "week1.md", TEXT))

    assert chunks_digest(chunks) == chunks_digest(list(reversed(chunks)))


def test_chunks_digest_changes_when_the_material_changes(tmp_path: Path) -> None:
    before = chunk_document(make_document(tmp_path / "week1.md", TEXT))
    after = chunk_document(make_document(tmp_path / "week1.md", TEXT.replace("memorises", "memorizes")))

    assert chunks_digest(before) != chunks_digest(after)


def test_chunks_digest_is_stable_across_rebuilds(tmp_path: Path) -> None:
    first = chunk_document(make_document(tmp_path / "week1.md", TEXT))
    second = chunk_document(make_document(tmp_path / "week1.md", TEXT))

    assert chunks_digest(first) == chunks_digest(second)
    assert len(chunks_digest(first)) == 16
