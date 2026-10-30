"""Integration tests: the chat service persists turns with their provenance."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.adapters.sqlite_store import SqliteStore
from app.config import PROJECT_ROOT, load_config
from app.domain.conversation import RetrievalStatus
from app.domain.retrieval import RetrievalResult, RetrievedPassage
from app.errors import LlmUnavailableError, ValidationError
from app.graph.build import build_study_graph
from app.prompts.builder import PromptBuilder
from app.services.buddy_service import BuddyService
from app.services.chat_service import ChatService

PROMPTS_DIR = PROJECT_ROOT / "app" / "prompts"
PASSAGE = RetrievedPassage(chunk_id="week-1:0003:abcdef", doc_name="Week 1", section="Overfitting", text="Overfitting means making a model too sensitive and wrong.")


class FakeRetriever:
    def __init__(self, result: RetrievalResult) -> None:
        self.result = result
        self.calls = 0

    def retrieve(self, query: str, top_k: int | None = None) -> RetrievalResult:
        self.calls += 1
        return self.result


class FakeChatModel:
    model_name = "fake:model"

    def __init__(self, answer: str = "A grounded answer.") -> None:
        self.answer = answer
        self.fail = False

    def complete(self, messages: list[dict[str, str]]) -> str:
        if self.fail:
            raise LlmUnavailableError("ollama is down")
        return self.answer

    def stream(self, messages: list[dict[str, str]]):
        if self.fail:
            raise LlmUnavailableError("ollama is down")
        for token in ("A streamed ", "grounded ", "answer."):
            yield token


def build_service(tmp_path: Path, retrieval: RetrievalResult, *, fail: bool = False) -> tuple[ChatService, BuddyService, FakeRetriever]:
    config = load_config()
    store = SqliteStore(tmp_path / "studygraph.db")
    buddies = BuddyService(store, config)
    buddies.seed_defaults()
    retriever = FakeRetriever(retrieval)
    chat_model = FakeChatModel()
    chat_model.fail = fail
    graph = build_study_graph(retriever=retriever, chat_model=chat_model, prompt_builder=PromptBuilder(PROMPTS_DIR), course_name="LLMs for Developers", top_k=4)
    return ChatService(store, graph, config), buddies, retriever


def test_start_conversation_freezes_the_buddy_snapshot(tmp_path: Path) -> None:
    service, buddies, _ = build_service(tmp_path, RetrievalResult.skipped())
    buddy = buddies.create_buddy(name="Patient Tutor", target="Beginner", tone="Friendly", traits=["Patient"], course_id="llms_for_devs")

    conversation = service.start_conversation(buddy)
    buddies.update_buddy(buddy.id, name="Exam Coach", target="Advanced", tone="Direct", traits=["Critical"], course_id=None)

    assert conversation.buddy_snapshot.buddy_name == "Patient Tutor"
    assert service.get_conversation(conversation.id).buddy_snapshot.course_id == "llms_for_devs"


def test_grounded_turn_stores_status_sources_and_provenance(tmp_path: Path) -> None:
    retrieval = RetrievalResult(status=RetrievalStatus.OK, passages=(PASSAGE,), sources=(), scores=(0.5,), top_k=4)
    service, buddies, retriever = build_service(tmp_path, retrieval)
    buddy = buddies.create_buddy(name="Tutor", target="Beginner", tone="Friendly", traits=["Patient"], course_id="llms_for_devs")
    conversation = service.start_conversation(buddy)

    result = service.send_message(conversation.id, "What is overfitting?")

    assert retriever.calls == 1
    assert result.is_grounded is True
    assert result.prompt.dimensions["Target"] == "Beginner"
    messages = service.get_messages(conversation.id)
    assert [message.content for message in messages] == ["What is overfitting?", "A grounded answer."]
    assert messages[1].retrieval_status is RetrievalStatus.OK
    assert messages[1].model == "fake:model"
    assert messages[1].prompt_version == "system_v1"


def test_general_turn_never_calls_the_retriever(tmp_path: Path) -> None:
    service, buddies, retriever = build_service(tmp_path, RetrievalResult.skipped())
    buddy = buddies.create_buddy(name="General", target="Beginner", tone="Friendly", traits=["Patient"], course_id=None)
    conversation = service.start_conversation(buddy)

    result = service.send_message(conversation.id, "What is overfitting?")

    assert retriever.calls == 0
    assert result.retrieval.status is RetrievalStatus.SKIPPED
    assert service.get_messages(conversation.id)[1].sources == ()


def test_failed_retrieval_is_stored_as_failed_without_sources(tmp_path: Path) -> None:
    service, buddies, _ = build_service(tmp_path, RetrievalResult.failed("chroma is down", top_k=4))
    buddy = buddies.create_buddy(name="Tutor", target="Beginner", tone="Friendly", traits=["Patient"], course_id="llms_for_devs")
    conversation = service.start_conversation(buddy)

    result = service.send_message(conversation.id, "What is overfitting?")

    assert result.retrieval.status is RetrievalStatus.FAILED
    assert result.is_grounded is False
    assert service.get_messages(conversation.id)[1].retrieval_status is RetrievalStatus.FAILED
    assert service.get_messages(conversation.id)[1].sources == ()


def test_failed_generation_leaves_the_conversation_untouched(tmp_path: Path) -> None:
    service, buddies, _ = build_service(tmp_path, RetrievalResult.skipped(), fail=True)
    buddy = buddies.create_buddy(name="Tutor", target="Beginner", tone="Friendly", traits=["Patient"], course_id=None)
    conversation = service.start_conversation(buddy)

    with pytest.raises(LlmUnavailableError):
        service.send_message(conversation.id, "This should fail")

    assert service.get_messages(conversation.id) == []


def test_empty_message_is_rejected_before_anything_is_stored(tmp_path: Path) -> None:
    service, buddies, retriever = build_service(tmp_path, RetrievalResult.skipped())
    buddy = buddies.create_buddy(name="Tutor", target="Beginner", tone="Friendly", traits=["Patient"], course_id="llms_for_devs")
    conversation = service.start_conversation(buddy)

    with pytest.raises(ValidationError, match="must not be empty"):
        service.send_message(conversation.id, "   ")

    assert service.get_messages(conversation.id) == []
    assert retriever.calls == 0


def test_unknown_course_is_rejected(tmp_path: Path) -> None:
    _, buddies, _ = build_service(tmp_path, RetrievalResult.skipped())

    with pytest.raises(ValidationError, match="Unknown course id"):
        buddies.create_buddy(name="Tutor", target="Beginner", tone="Friendly", traits=["Patient"], course_id="nope")


def test_streaming_turn_matches_the_stored_answer(tmp_path: Path) -> None:
    service, buddies, _ = build_service(tmp_path, RetrievalResult.skipped())
    buddy = buddies.create_buddy(name="Tutor", target="Beginner", tone="Friendly", traits=["Patient"], course_id=None)
    conversation = service.start_conversation(buddy)

    tokens: list[str] = []
    result = service.send_message(conversation.id, "What is overfitting?", on_token=tokens.append)

    assert "".join(tokens) == "A streamed grounded answer."
    assert result.assistant_message.content == "A streamed grounded answer."
    assert service.get_messages(conversation.id)[1].content == "A streamed grounded answer."


def test_retrieval_top_k_is_persisted(tmp_path: Path) -> None:
    retrieval = RetrievalResult(status=RetrievalStatus.OK, passages=(PASSAGE,), sources=(), scores=(0.5,), top_k=4)
    service, buddies, _ = build_service(tmp_path, retrieval)
    buddy = buddies.create_buddy(name="Tutor", target="Beginner", tone="Friendly", traits=["Patient"], course_id="llms_for_devs")
    conversation = service.start_conversation(buddy)

    service.send_message(conversation.id, "What is overfitting?")

    assert service.get_messages(conversation.id)[1].retrieval_top_k == 4


def test_seeding_creates_the_default_buddy_pair(tmp_path: Path) -> None:
    _, buddies, _ = build_service(tmp_path, RetrievalResult.skipped())

    seeded = buddies.list_buddies()

    assert {buddy.name for buddy in seeded} == {"Patient Tutor", "General Tutor"}
    assert {buddy.is_course_grounded for buddy in seeded} == {True, False}
    assert len({(buddy.target, buddy.tone, buddy.traits) for buddy in seeded}) == 1, "the pair must differ only in course"
