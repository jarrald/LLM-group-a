"""LangGraph orchestration of one chat turn.

    route ──(course)──▶ retrieve ──▶ build_prompt ──▶ generate ──▶ END
      └────(no course)───────────────▶ build_prompt

Routing depends only on the conversation's :class:`BuddySnapshot`, never on the Buddy's
name or prompt text. Nodes are thin wrappers around injected collaborators, so the whole
flow is testable with fakes (``40-stack-and-architecture.md``, ADR-006).
"""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from app.adapters.protocols import ChatModel, Retriever
from app.domain.retrieval import RetrievalResult
from app.graph.state import StudyGraphState
from app.prompts.builder import PromptBuilder


def route_by_snapshot(state: StudyGraphState) -> str:
    """Pure routing decision: course-associated conversations retrieve, others never do."""
    return "retrieve" if state["snapshot"].is_course_grounded else "build_prompt"


def build_study_graph(
    *,
    retriever: Retriever,
    chat_model: ChatModel,
    prompt_builder: PromptBuilder,
    course_name: str,
    top_k: int | None = None,
) -> Any:
    """Compile the chat graph for one process."""

    def route_node(state: StudyGraphState) -> dict[str, object]:
        if state["snapshot"].is_course_grounded:
            return {}
        return {"retrieval": RetrievalResult.skipped()}

    def retrieve_node(state: StudyGraphState) -> dict[str, object]:
        return {"retrieval": retriever.retrieve(state["user_message"], top_k=top_k)}

    def build_prompt_node(state: StudyGraphState) -> dict[str, object]:
        retrieval = state.get("retrieval") or RetrievalResult.skipped()
        bundle = prompt_builder.build(
            snapshot=state["snapshot"],
            task=state["task"],
            user_message=state["user_message"],
            history=state.get("history", []),
            passages=retrieval.passages,
            course_name=course_name,
        )
        return {"prompt": bundle}

    def generate_node(state: StudyGraphState) -> dict[str, object]:
        bundle = state["prompt"]
        on_token = state.get("on_token")
        if on_token is None:
            return {"answer": chat_model.complete(bundle.messages), "model": chat_model.model_name}

        pieces: list[str] = []
        for token in chat_model.stream(bundle.messages):
            pieces.append(token)
            on_token(token)
        return {"answer": "".join(pieces).strip(), "model": chat_model.model_name}

    graph: StateGraph = StateGraph(StudyGraphState)
    graph.add_node("route", route_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("build_prompt", build_prompt_node)
    graph.add_node("generate", generate_node)

    graph.set_entry_point("route")
    graph.add_conditional_edges("route", route_by_snapshot, {"retrieve": "retrieve", "build_prompt": "build_prompt"})
    graph.add_edge("retrieve", "build_prompt")
    graph.add_edge("build_prompt", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
