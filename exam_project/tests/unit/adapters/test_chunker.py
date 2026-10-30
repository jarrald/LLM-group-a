"""Tests for heading-aware chunking: determinism, provenance and boundaries."""

from __future__ import annotations

from pathlib import Path

from app.adapters.chunker import chunk_document
from app.adapters.loader import LectureDocument


def make_document(path: Path, text: str, lecture: int = 1) -> LectureDocument:
    return LectureDocument(
        doc_id=f"week-{lecture}",
        doc_name=f"Week {lecture}",
        lecture=lecture,
        course_id="llms_for_devs",
        path=path,
        text=text,
    )


SIMPLE = """# Week 1

Intro paragraph that is long enough to be kept as its own chunk by the chunker.

## 1. Machine learning foundations

A model is a simplified representation of a problem. Its usefulness depends on whether it
serves the intended purpose.

### Overfitting

Overfitting happens when a model memorises the training data instead of learning the
underlying pattern, which shows up as a high training score and a poor validation score.
"""


def test_chunk_document_is_deterministic(tmp_path: Path) -> None:
    document = make_document(tmp_path / "week1.md", SIMPLE)

    first = chunk_document(document)
    second = chunk_document(make_document(tmp_path / "week1.md", SIMPLE))

    assert [chunk.chunk_id for chunk in first] == [chunk.chunk_id for chunk in second]
    assert [chunk.text for chunk in first] == [chunk.text for chunk in second]


def test_chunk_document_keeps_heading_with_each_chunk(tmp_path: Path) -> None:
    document = make_document(tmp_path / "week1.md", SIMPLE)

    chunks = chunk_document(document)

    overfitting = [chunk for chunk in chunks if "Overfitting happens" in chunk.text]
    assert overfitting, "expected a chunk containing the overfitting paragraph"
    assert overfitting[0].text.startswith("### Overfitting")


def test_chunk_document_tracks_heading_path_as_section(tmp_path: Path) -> None:
    document = make_document(tmp_path / "week1.md", SIMPLE)

    chunks = chunk_document(document)

    overfitting = [chunk for chunk in chunks if "Overfitting happens" in chunk.text][0]
    assert overfitting.section == "1. Machine learning foundations > Overfitting"


def test_chunk_document_reports_provenance(tmp_path: Path) -> None:
    document = make_document(tmp_path / "week1.md", SIMPLE, lecture=4)

    chunk = chunk_document(document)[0]

    assert chunk.doc_id == "week-4"
    assert chunk.lecture == 4
    assert chunk.course_id == "llms_for_devs"
    assert chunk.doc_name == "Week 4"
    assert chunk.chunk_id.startswith("week-4:0000:")
    assert len(chunk.text_hash) == 12


def test_chunk_document_ids_are_unique(tmp_path: Path) -> None:
    document = make_document(tmp_path / "week1.md", SIMPLE)

    chunks = chunk_document(document)

    assert len({chunk.chunk_id for chunk in chunks}) == len(chunks)


def test_chunk_document_respects_max_chars(tmp_path: Path) -> None:
    body = "\n\n".join(f"Paragraph {index} " + ("filler text " * 20) for index in range(12))
    document = make_document(tmp_path / "week1.md", f"## Long section\n\n{body}\n")

    chunks = chunk_document(document, max_chars=400)

    assert len(chunks) > 1
    assert max(len(chunk.text) for chunk in chunks) <= 400


def test_chunk_document_keeps_fenced_code_whole(tmp_path: Path) -> None:
    code_block = "```python\n" + "\n".join(f"value_{index} = {index}" for index in range(60)) + "\n```"
    document = make_document(tmp_path / "week1.md", f"## Code\n\n{code_block}\n")

    chunks = chunk_document(document, max_chars=300)

    assert len(chunks) == 1
    assert chunks[0].text.count("```") == 2


def test_chunk_document_drops_heading_only_stubs(tmp_path: Path) -> None:
    document = make_document(tmp_path / "week1.md", f"# Title\n\n## Contents\n\n## 1. Real section\n\n{SIMPLE}\n")

    chunks = chunk_document(document)

    assert all("## Contents" != chunk.text.strip() for chunk in chunks)


def test_chunk_document_retains_all_substantive_text(tmp_path: Path) -> None:
    document = make_document(tmp_path / "week1.md", SIMPLE)

    joined = " ".join(chunk.text for chunk in chunk_document(document))

    assert "A model is a simplified representation" in joined
    assert "high training score and a poor validation score" in joined
