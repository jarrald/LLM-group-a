"""Tests for what the regression index includes (third-party source + guidance Markdown)."""

from __future__ import annotations

from pathlib import Path

from regression.rag import _chunks_for, _extra_markdown_files, _indexable_files, _strip_front_matter

SOURCE = Path("sklearn/linear_model/_base.py")


def make_checkout(root: Path) -> Path:
    path = root / SOURCE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("class LinearRegression:\n    pass\n", encoding="utf-8")
    return root


def make_guidance(root: Path) -> Path:
    (root / "nested").mkdir(parents=True)
    (root / "01_workflow.md").write_text("# Workflow\n\n## Fit\n\nUse LinearRegression().fit(X, y).\n", encoding="utf-8")
    (root / "nested" / "02_examples.md").write_text("# Examples\n\n## One feature\n\nExample text.\n", encoding="utf-8")
    (root / "notes.txt").write_text("not indexed", encoding="utf-8")
    return root


def test_extra_markdown_files_are_found_recursively_and_sorted(tmp_path: Path) -> None:
    guidance = make_guidance(tmp_path / "rag-optimized")

    found = [path.name for path in _extra_markdown_files(guidance)]

    assert found == ["01_workflow.md", "02_examples.md"]


def test_extra_markdown_files_are_empty_without_the_folder(tmp_path: Path) -> None:
    assert _extra_markdown_files(tmp_path / "absent") == []


def test_indexable_files_label_guidance_documents_with_their_folder(tmp_path: Path) -> None:
    corpus = make_checkout(tmp_path / "scikit-learn-main")
    guidance = make_guidance(tmp_path / "rag-optimized")

    labels = [label for label, _ in _indexable_files(corpus, guidance)]

    assert "sklearn/linear_model/_base.py" in labels
    assert "rag-optimized/01_workflow.md" in labels
    assert "rag-optimized/nested/02_examples.md" in labels
    assert not any(label.endswith(".txt") for label in labels)


def test_indexable_files_without_guidance_are_the_source_only_corpus(tmp_path: Path) -> None:
    corpus = make_checkout(tmp_path / "scikit-learn-main")

    labels = [label for label, _ in _indexable_files(corpus, tmp_path / "absent")]

    assert labels == ["sklearn/linear_model/_base.py"]


def test_strip_front_matter_removes_the_yaml_block() -> None:
    text = "---\ndoc_id: rag.linear_regression.concepts\ntitle: Concepts\n---\n\n# Linear regression\n\nBody.\n"

    assert _strip_front_matter(text) == "# Linear regression\n\nBody.\n"


def test_strip_front_matter_leaves_markdown_without_metadata_alone() -> None:
    text = "# Linear regression\n\nBody.\n"

    assert _strip_front_matter(text) == text


def test_guidance_chunks_do_not_contain_yaml_front_matter() -> None:
    text = "---\ndoc_id: rag.linear_regression.examples\nkeywords: [sklearn, LinearRegression]\n---\n\n# Worked examples\n\n## One feature\n\n" + ("Use LinearRegression().fit(X, y) on a DataFrame. " * 5)

    chunks = _chunks_for("rag-optimized/05_WORKED_EXAMPLES.md", text)

    assert chunks
    assert all("doc_id" not in str(chunk["text"]) for chunk in chunks)
    assert any("LinearRegression().fit" in str(chunk["text"]) for chunk in chunks)
