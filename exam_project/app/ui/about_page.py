"""About page: what the app does, which local models it uses, and where data lives."""

from __future__ import annotations

import streamlit as st

from app.adapters.chroma_client import get_chroma_client, get_course_collection
from app.errors import StudyGraphError
from app.ui.clients import get_services
from app.ui.components import inject_css, page_header


def _collection_status(collection_name: str) -> str:
    services = get_services()
    try:
        collection = get_course_collection(get_chroma_client(services.config), services.config)
    except StudyGraphError as exc:
        return f"unavailable — {exc}"
    return f"`{collection_name}`, {collection.count()} chunks indexed"


def render() -> None:
    services = get_services()
    config = services.config
    inject_css()
    page_header("About StudyGraph", "A local study assistant that answers from your course material.")

    st.markdown(
        "StudyGraph keeps a **Buddy** — a reusable teaching configuration (Traits, Tone, Target and an "
        "optional course) — and freezes that configuration into every conversation you start. "
        "The **Task** (explain, summarise, quiz…) is chosen per message."
    )

    st.subheader("Answers and grounding")
    st.markdown(
        "- A Buddy linked to **LLMs for Developers** retrieves passages from the indexed lecture material "
        "before answering, and the answer lists its sources.\n"
        "- A Buddy with **no course** never retrieves; the answer is general and is labelled as such.\n"
        "- If retrieval fails or finds nothing, the answer says so instead of pretending to be grounded."
    )

    st.subheader("Everything runs locally")
    st.table(
        {
            "Component": ["Chat model", "Embedding model", "Vector store", "Application data"],
            "Value": [
                config.chat_model,
                f"{config.embed_model} ({config.embedding_dim} dims)",
                _collection_status(config.collection_name),
                str(config.db_path),
            ],
        }
    )

    st.caption(f"Ollama: {config.ollama_base_url} · Chroma: {config.chroma_url} · prompt {config.prompts_dir.name} · top-k {config.top_k}")
    st.caption("No conversation ever leaves this machine: generation and embeddings are local.")


if __name__ == "__main__":
    render()
