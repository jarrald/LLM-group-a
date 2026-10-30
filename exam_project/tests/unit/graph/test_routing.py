"""Graph routing tests with fakes: RAG vs non-RAG, and retrieval failure handling."""

from __future__ import annotations

from datetime import datetime, timezone

from app.config import PROJECT_ROOT
from app.domain.buddy import Buddy, BuddySnapshot
from app.domain.conversation import RetrievalStatus, SourceReference
from app.domain.retrieval import RetrievalResult, RetrievedPassage
from app.graph.build import build_study_graph, route_by_snapshot
from app.prompts.builder import PromptBuilder, TaskSpec

PROMPTS_DIR = PROJECT_ROOT / "app" / "prompts"

PASSAGE = RetrievedPassage(chunk_id="week-1:0003:abcdef", doc_name="Week 1", section="Overfitting", text="Overfitting means making a model too sensitive and wrong.")
SOURCE = SourceReference(chunk_id="week-1:0003:abcdef", doc_id="week-1", doc_name="Week 1", section="Overfitting", lecture=1, distance=0.53, snippet="Overfitting means…")


class FakeRetriever:
    def __init__(self, result: RetrievalResult) -> None:
        self.result = result
        self.calls: list[tuple[str, int | None]] = []

    def retrieve(self, query: str, top_k: int | None = None) -> RetrievalResult:
        self.calls.append((query, top_k))
        return self.result


class FakeChatModel:
    model_name = "fake:model"

    def __init__(self, answer: str = "A fake but well-formed answer.") -> None:
        self.answer = answer
        self.seen: list[list[dict[str, str]]] = []

    def complete(self, messages: list[dict[str, str]]) -> str:
        self.seen.append(messages)
        return self.answer


def make_snapshot(course_id: str | None) -> BuddySnapshot:
    now = datetime.now(timezone.utc)
    buddy = Buddy(id="b1", name="Tutor", target="Beginner", tone="Friendly", traits=("Patient",), course_id=course_id, created_at=now, updated_at=now)
    return BuddySnapshot.from_buddy(buddy)


def run_graph(snapshot: BuddySnapshot, retrieval: RetrievalResult) -> tuple[dict[str, object], FakeRetriever, FakeChatModel]:
    retriever = FakeRetriever(retrieval)
    chat_model = FakeChatModel()
    graph = build_study_graph(retriever=retriever, chat_model=chat_model, prompt_builder=PromptBuilder(PROMPTS_DIR), course_name="LLMs for Developers", top_k=4)
    state = graph.invoke({"snapshot": snapshot, "task": TaskSpec.from_preset(), "user_message": "What is overfitting?", "history": []})
    return state, retriever, chat_model


def test_route_by_snapshot_depends_only_on_course_association() -> None:
    assert route_by_snapshot({"snapshot": make_snapshot("llms_for_devs")}) == "retrieve"
    assert route_by_snapshot({"snapshot": make_snapshot(None)}) == "build_prompt"


def test_general_conversation_never_calls_the_retriever() -> None:
    state, retriever, chat_model = run_graph(make_snapshot(None), RetrievalResult.skipped())

    assert retriever.calls == []
    assert state["retrieval"].status is RetrievalStatus.SKIPPED  # type: ignore[union-attr]
    assert len(chat_model.seen) == 1
    assert state["answer"] == "A fake but well-formed answer."


def test_general_prompt_contains_no_course_context() -> None:
    state, _, chat_model = run_graph(make_snapshot(None), RetrievalResult.skipped())

    system = chat_model.seen[0][0]["content"]
    assert "COURSE MATERIAL" not in system
    assert "not linked to any course" in system
    assert state["prompt"].context_block is None  # type: ignore[union-attr]


def test_course_conversation_retrieves_and_keeps_sources() -> None:
    result = RetrievalResult(status=RetrievalStatus.OK, passages=(PASSAGE,), sources=(SOURCE,), scores=(0.53,), top_k=4)
    state, retriever, chat_model = run_graph(make_snapshot("llms_for_devs"), result)

    assert retriever.calls == [("What is overfitting?", 4)]
    assert state["retrieval"].status is RetrievalStatus.OK  # type: ignore[union-attr]
    assert state["retrieval"].sources == (SOURCE,)  # type: ignore[union-attr]
    assert "COURSE MATERIAL" in chat_model.seen[0][0]["content"]
    assert "week-1:0003:abcdef" in chat_model.seen[0][0]["content"]


def test_empty_retrieval_is_not_reported_as_grounded() -> None:
    result = RetrievalResult(status=RetrievalStatus.EMPTY, top_k=4)
    state, retriever, chat_model = run_graph(make_snapshot("llms_for_devs"), result)

    assert retriever.calls
    assert state["retrieval"].status is RetrievalStatus.EMPTY  # type: ignore[union-attr]
    assert "found no relevant passages" in chat_model.seen[0][0]["content"]


def test_failed_retrieval_is_distinct_from_empty_and_does_not_crash() -> None:
    result = RetrievalResult.failed("chroma is down", top_k=4)
    state, _, chat_model = run_graph(make_snapshot("llms_for_devs"), result)

    assert state["retrieval"].status is RetrievalStatus.FAILED  # type: ignore[union-attr]
    assert state["retrieval"].status is not RetrievalStatus.EMPTY  # type: ignore[union-attr]
    assert state["retrieval"].error == "chroma is down"  # type: ignore[union-attr]
    assert state["answer"]
    assert "found no relevant passages" in chat_model.seen[0][0]["content"]
