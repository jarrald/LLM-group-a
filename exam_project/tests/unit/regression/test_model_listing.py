"""Tests for the Ollama model listing behind the regression model picker."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from regression.rag import LocalModel, list_models


class FakeOllama:
    """The two calls ``list_models`` makes, without a server."""

    def __init__(self, models: dict[str, tuple[list[str], float, str, str]]) -> None:
        self._models = models

    def list(self) -> SimpleNamespace:
        entries = [
            SimpleNamespace(
                model=name,
                size=int(size_gb * 1_000_000_000),
                details=SimpleNamespace(family=family, parameter_size=parameter_size),
            )
            for name, (_, size_gb, family, parameter_size) in self._models.items()
        ]
        return SimpleNamespace(models=entries)

    def show(self, model: str) -> SimpleNamespace:
        capabilities = self._models[model][0]
        if capabilities == ["boom"]:
            raise ConnectionError("show failed")
        return SimpleNamespace(capabilities=capabilities)


INSTALLED = {
    "qwen2.5-coder:7b": (["completion", "tools"], 4.7, "qwen2", "7.6B"),
    "llama3.2:3b": (["completion"], 2.0, "llama", "3.2B"),
    "nomic-embed-text:latest": (["embedding"], 0.3, "nomic-bert", "137M"),
    "mystery:1b": (["boom"], 0.8, "mystery", "1B"),
}


def test_list_models_offers_only_chat_capable_models_by_default() -> None:
    names = [model.name for model in list_models(client=FakeOllama(INSTALLED))]  # type: ignore[arg-type]

    assert names == ["llama3.2:3b", "mystery:1b", "qwen2.5-coder:7b"]


def test_list_models_marks_embedding_models_when_asked_for_everything() -> None:
    models = list_models(chat_only=False, client=FakeOllama(INSTALLED))  # type: ignore[arg-type]

    embedding = [model for model in models if not model.can_chat]
    assert [model.name for model in embedding] == ["nomic-embed-text:latest"]


def test_list_models_keeps_a_model_whose_capabilities_cannot_be_read() -> None:
    mystery = [model for model in list_models(client=FakeOllama(INSTALLED)) if model.name == "mystery:1b"]

    assert mystery and mystery[0].can_chat is True


def test_list_models_reports_size_family_and_parameter_count() -> None:
    model = next(model for model in list_models(client=FakeOllama(INSTALLED)) if model.name == "qwen2.5-coder:7b")

    assert model == LocalModel(name="qwen2.5-coder:7b", size_gb=4.7, family="qwen2", parameter_size="7.6B", can_chat=True)
    assert model.detail == "qwen2 · 7.6B · 4.7 GB"


def test_list_models_surfaces_a_connection_error() -> None:
    class Dead:
        def list(self) -> SimpleNamespace:
            raise ConnectionError("nothing listening")

    with pytest.raises(ConnectionError, match="nothing listening"):
        list_models(client=Dead())  # type: ignore[arg-type]
