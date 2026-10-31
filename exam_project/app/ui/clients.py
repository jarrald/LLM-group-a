"""Service wiring for the Streamlit pages.

Everything expensive (SQLite store, graph, clients) is built once per process and cached,
so a rerun never reconnects a server or re-indexes anything.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import streamlit as st

from app.adapters.ollama_client import OllamaChatClient
from app.adapters.retriever import ChromaRetriever
from app.adapters.sqlite_store import SqliteStore
from app.config import Config, get_config
from app.graph.build import build_study_graph
from app.prompts.builder import PromptBuilder
from app.services.buddy_service import BuddyService
from app.services.chat_service import ChatService


@dataclass(frozen=True, slots=True)
class Services:
    """The objects a page needs, all long-lived."""

    config: Config
    buddies: BuddyService
    chat: ChatService
    course_name: str
    store: SqliteStore


def build_services(config: Config) -> Services:
    """Assemble the object graph. Also used by tests with fakes for retriever/chat model."""
    store = SqliteStore(config.db_path)
    buddies = BuddyService(store, config)
    course = buddies.seed_defaults()
    graph = build_study_graph(
        retriever=ChromaRetriever(config),
        chat_model=OllamaChatClient(config),
        prompt_builder=PromptBuilder(config.prompts_dir),
        course_name=course.name,
        top_k=config.top_k,
    )
    return Services(config=config, buddies=buddies, chat=ChatService(store, graph, config), course_name=course.name, store=store)


@st.cache_resource(show_spinner=False)
def get_services() -> Any:
    """Cached services for this process."""
    return build_services(get_config())


def reset_services() -> None:
    """Drop the cached services (tests, and after a configuration change)."""
    get_services.clear()
