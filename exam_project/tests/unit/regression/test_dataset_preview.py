"""Tests for the dataset preview that gives the model real column names."""

from __future__ import annotations

from pathlib import Path

from regression.rag import _dataset_preview


def test_dataset_preview_handles_a_path_with_spaces(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    data = tmp_path / "datasets" / "house prices.csv"
    data.parent.mkdir()
    data.write_text("id,Price,sqft_living\n1,100,20\n2,200,30\n", encoding="utf-8")

    preview = _dataset_preview("read datasets/house prices.csv and predict Price")

    assert "## Dataset preview" in preview
    assert "Price" in preview
    assert "Use these exact column names." in preview


def test_dataset_preview_handles_a_plain_filename(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    data = tmp_path / "ice_cream_regression.csv"
    data.write_text("Temperature,Revenue\n10,100\n", encoding="utf-8")

    preview = _dataset_preview("read ice_cream_regression.csv")

    assert "Temperature,Revenue" in preview
