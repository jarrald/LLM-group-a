"""Tests for the corpus downloader's checks (no network is used here)."""

from __future__ import annotations

from pathlib import Path

from regression import fetch_corpus


def make_corpus(root: Path, markers: tuple[str, ...] = fetch_corpus.MARKERS) -> Path:
    for marker in markers:
        path = root / marker
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('__version__ = "1.10.dev0"\n', encoding="utf-8")
        else:
            path.mkdir(parents=True, exist_ok=True)
    return root


def test_corpus_ready_requires_every_marker(tmp_path: Path) -> None:
    corpus = make_corpus(tmp_path / "corpus")

    assert fetch_corpus.corpus_ready(corpus) is True


def test_corpus_ready_is_false_for_an_empty_directory(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()

    assert fetch_corpus.corpus_ready(corpus) is False
    assert "sklearn/__init__.py" in fetch_corpus.missing_markers(corpus)


def test_corpus_ready_is_false_for_a_missing_directory(tmp_path: Path) -> None:
    assert fetch_corpus.corpus_ready(tmp_path / "absent") is False


def test_read_provenance_returns_empty_dict_without_a_record(tmp_path: Path) -> None:
    corpus = make_corpus(tmp_path / "corpus")

    assert fetch_corpus.read_provenance(corpus) == {}


def test_read_provenance_reads_the_record_written_at_download_time(tmp_path: Path) -> None:
    corpus = make_corpus(tmp_path / "corpus")
    fetch_corpus.provenance_path(corpus).write_text('{"ref": "main", "commit": "abc", "version": "1.10.dev0"}\n', encoding="utf-8")

    record = fetch_corpus.read_provenance(corpus)

    assert record["ref"] == "main"
    assert record["commit"] == "abc"


def test_version_of_reads_the_declared_version(tmp_path: Path) -> None:
    corpus = make_corpus(tmp_path / "corpus")

    assert fetch_corpus._version_of(corpus) == "1.10.dev0"


def test_check_reports_a_missing_corpus(tmp_path: Path) -> None:
    assert fetch_corpus.main(["--check", "--corpus", str(tmp_path / "absent")]) == 1


def test_check_reports_a_usable_corpus(tmp_path: Path) -> None:
    corpus = make_corpus(tmp_path / "corpus")

    assert fetch_corpus.main(["--check", "--corpus", str(corpus)]) == 0
