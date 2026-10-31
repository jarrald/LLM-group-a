r"""Ask StudyGraph a question from the terminal.

This is the end-to-end smoke demo: real local model, real retrieval, real 4T prompt, with a
throw-away SQLite file so nothing is left behind.

    uv run python .\scripts\ask.py "What is overfitting?"
    uv run python .\scripts\ask.py --compare "What is overfitting?"
    uv run python .\scripts\ask.py --task "Quiz me" --show-prompt "Test me on model fitting"

``--compare`` asks the identical question twice with the same 4T configuration: once with the
course (RAG) and once without it. That is the RAG vs non-RAG demonstration.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from app.adapters.ollama_client import OllamaChatClient
from app.adapters.retriever import ChromaRetriever
from app.adapters.sqlite_store import SqliteStore
from app.config import get_config
from app.domain.buddy import Buddy
from app.errors import StudyGraphError
from app.graph.build import build_study_graph
from app.prompts.builder import PromptBuilder, TaskSpec
from app.services.buddy_service import BuddyService
from app.services.chat_service import ChatService, TurnResult

TARGET = "Student familiar with the fundamentals"
TONE = "Friendly and conversational"
TRAITS = ["Patient", "Analytical"]


def build_stack(database_path: Path) -> tuple[BuddyService, ChatService, str]:
    config = get_config()
    store = SqliteStore(database_path)
    buddies = BuddyService(store, config)
    course = buddies.seed_defaults()
    graph = build_study_graph(
        retriever=ChromaRetriever(config),
        chat_model=OllamaChatClient(config),
        prompt_builder=PromptBuilder(config.prompts_dir),
        course_name=course.name,
        top_k=config.top_k,
    )
    return buddies, ChatService(store, graph, config), course.name


def make_buddy(buddies: BuddyService, *, course_id: str | None, label: str) -> Buddy:
    return buddies.create_buddy(name=label, target=TARGET, tone=TONE, traits=TRAITS, course_id=course_id)


def report(result: TurnResult, *, show_prompt: bool) -> None:
    retrieval = result.retrieval
    print(f"Retrieval   : {retrieval.status.value} ({retrieval.passage_count} passages, top_k={retrieval.top_k})")
    if retrieval.error:
        print(f"Error       : {retrieval.error}")
    for source in retrieval.sources:
        distance = f"{source.distance:.3f}" if source.distance is not None else "?"
        print(f"  - {source.label()}  [{source.chunk_id}] distance={distance}")
    print("Dimensions  : " + " | ".join(f"{name}={value}" for name, value in result.prompt.dimensions.items()))
    print(f"Provenance  : model={result.assistant_message.model} prompt_version={result.assistant_message.prompt_version}")
    if show_prompt:
        print("\n--- rendered system prompt ---")
        print(result.prompt.system)
        print("--- end prompt ---\n")
    print("Answer      :")
    print(result.assistant_message.content)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    parser = argparse.ArgumentParser(description="Ask StudyGraph a question locally.")
    parser.add_argument("question", help="the question to ask")
    parser.add_argument("--compare", action="store_true", help="ask with and without course grounding")
    parser.add_argument("--course", action="store_true", help="only the course-grounded answer")
    parser.add_argument("--general", action="store_true", help="only the answer without the course")
    parser.add_argument("--task", default="Explain a concept", help="task preset (default: 'Explain a concept')")
    parser.add_argument("--show-prompt", action="store_true", help="print the rendered system prompt")
    arguments = parser.parse_args(argv)

    config = get_config()
    task = TaskSpec.from_preset(arguments.task)

    with tempfile.TemporaryDirectory(prefix="studygraph-") as temporary_directory:
        buddies, chat, course_name = build_stack(Path(temporary_directory) / "smoke.db")
        modes: list[tuple[str, str | None]]
        if arguments.compare or not (arguments.course or arguments.general):
            modes = [("COURSE-GROUNDED (RAG)", config.course_id), ("GENERAL (no retrieval)", None)]
        elif arguments.general:
            modes = [("GENERAL (no retrieval)", None)]
        else:
            modes = [("COURSE-GROUNDED (RAG)", config.course_id)]

        print(f"Course      : {course_name} ({config.collection_name})")
        print(f"Model       : {config.chat_model}  |  embeddings: {config.embed_model}")
        print(f"Task        : {task.name}")
        print(f"Question    : {arguments.question}\n")

        for label, course_id in modes:
            buddy = make_buddy(buddies, course_id=course_id, label=f"CLI {label}")
            conversation = chat.start_conversation(buddy)
            print(f"=== {label} ===")
            report(chat.send_message(conversation.id, arguments.question, task=task), show_prompt=arguments.show_prompt)
            print()

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StudyGraphError as exc:
        print(f"FAIL  {exc}")
        raise SystemExit(2)
