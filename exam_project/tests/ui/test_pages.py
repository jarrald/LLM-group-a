"""AppTest coverage for the Streamlit pages, with fake adapters (no network, no real DB)."""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from app.adapters.sqlite_store import SqliteStore
from app.config import PROJECT_ROOT, load_config
from app.domain.conversation import RetrievalStatus
from app.domain.retrieval import RetrievalResult, RetrievedPassage
from app.graph.build import build_study_graph
from app.prompts.builder import PromptBuilder
from app.services.buddy_service import BuddyService
from app.services.chat_service import ChatService
from app.ui.clients import Services

PROMPTS_DIR = PROJECT_ROOT / "app" / "prompts"
PASSAGE = RetrievedPassage(chunk_id="week-1:0017:47dbf22f4bc8", doc_name="Week 1", section="Overfitting", text="Overfitting means making a model too sensitive and wrong.")


class FakeRetriever:
    def __init__(self, result: RetrievalResult) -> None:
        self.result = result

    def retrieve(self, query: str, top_k: int | None = None) -> RetrievalResult:
        return self.result


class FakeChatModel:
    model_name = "fake:model"

    def complete(self, messages: list[dict[str, str]]) -> str:
        return "A fake answer about overfitting."

    def stream(self, messages: list[dict[str, str]]):
        yield from ("A fake ", "answer ", "about overfitting.")


def make_services(tmp_path: Path, retrieval: RetrievalResult | None = None) -> Services:
    config = load_config()
    store = SqliteStore(tmp_path / "ui.db")
    buddies = BuddyService(store, config)
    course = buddies.seed_defaults()
    graph = build_study_graph(
        retriever=FakeRetriever(retrieval or RetrievalResult.skipped()),
        chat_model=FakeChatModel(),
        prompt_builder=PromptBuilder(PROMPTS_DIR),
        course_name=course.name,
        top_k=4,
    )
    return Services(config=config, buddies=buddies, chat=ChatService(store, graph, config), course_name=course.name, store=store)


def run_page(monkeypatch: pytest.MonkeyPatch, module_name: str, services: Services, session_state: dict[str, object] | None = None) -> AppTest:
    module = __import__(module_name, fromlist=["render"])
    monkeypatch.setattr(module, "get_services", lambda: services)
    app = AppTest.from_string("from " + module_name + " import render\nrender()")
    for key, value in (session_state or {}).items():
        app.session_state[key] = value
    return app.run(timeout=30)


def test_buddies_page_lists_the_default_pair(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    services = make_services(tmp_path)

    app = run_page(monkeypatch, "app.ui.buddies_page", services)

    assert not app.exception
    rendered = " ".join(element.value for element in app.markdown)
    assert "Patient Tutor" in rendered
    assert "General Tutor" in rendered


def test_chat_page_without_a_conversation_shows_the_hint(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    services = make_services(tmp_path)

    app = run_page(monkeypatch, "app.ui.chat_page", services)

    assert not app.exception
    rendered = " ".join(element.value for element in app.markdown)
    assert "Chat with your buddy" in rendered


def test_chat_page_shows_the_grounded_badge_and_sources(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    retrieval = RetrievalResult(status=RetrievalStatus.OK, passages=(PASSAGE,), sources=(), scores=(0.42,), top_k=4)
    services = make_services(tmp_path, retrieval)
    buddy = next(buddy for buddy in services.buddies.list_buddies() if buddy.is_course_grounded)
    conversation = services.chat.start_conversation(buddy)
    services.chat.send_message(conversation.id, "What is overfitting?")

    app = run_page(monkeypatch, "app.ui.chat_page", services, {"conversation_id": conversation.id})

    assert not app.exception
    rendered = " ".join(element.value for element in app.markdown)
    assert "Course-grounded" in rendered
    assert "A fake answer about overfitting." in rendered


def test_chat_page_shows_the_general_badge_for_a_buddy_without_a_course(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    services = make_services(tmp_path)
    buddy = next(buddy for buddy in services.buddies.list_buddies() if not buddy.is_course_grounded)
    conversation = services.chat.start_conversation(buddy)

    app = run_page(monkeypatch, "app.ui.chat_page", services, {"conversation_id": conversation.id})

    assert not app.exception
    rendered = " ".join(element.value for element in app.markdown)
    assert "General" in rendered
    assert "Course-grounded" not in rendered
