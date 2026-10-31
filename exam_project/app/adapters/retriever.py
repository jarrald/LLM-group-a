"""Retrieval from the local Chroma collection.

Retrieval never raises for a backend problem: it returns ``status = failed`` with the error,
so the graph can tell a broken retriever from an empty result and the UI can say which
happened (NFR-04, ``50-rag-prompts-and-grounding.md``).
"""

from __future__ import annotations

import logging

from app.adapters.chroma_client import get_chroma_client, get_course_collection
from app.adapters.embedder import OllamaEmbedder
from app.config import Config
from app.domain.conversation import RetrievalStatus, SourceReference
from app.domain.retrieval import RetrievalResult, RetrievedPassage

logger = logging.getLogger(__name__)

SNIPPET_CHARS = 300


class ChromaRetriever:
    """Default retriever: the course collection, embedded with the local model."""

    def __init__(self, config: Config) -> None:
        self._config = config

    def retrieve(self, query: str, top_k: int | None = None) -> RetrievalResult:
        limit = top_k or self._config.top_k
        try:
            collection = get_course_collection(get_chroma_client(self._config), self._config)
            query_vector = OllamaEmbedder(self._config).embed_query(query)
            # Chroma types the argument as numpy arrays; a list of vectors is valid at runtime.
            result = collection.query(query_embeddings=[query_vector], n_results=limit, include=["documents", "metadatas", "distances"])  # type: ignore[arg-type]
        except Exception as exc:
            logger.warning("retrieval failed: %s", exc)
            return RetrievalResult.failed(str(exc), top_k=limit)

        ids = (result.get("ids") or [[]])[0]
        documents = (result.get("documents") or [[]])[0]
        metadatas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]

        passages: list[RetrievedPassage] = []
        sources: list[SourceReference] = []
        scores: list[float] = []
        for chunk_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
            if not text or not metadata:
                continue
            metadata = dict(metadata)
            doc_name = str(metadata.get("doc_name", ""))
            section = str(metadata.get("section", ""))
            passages.append(RetrievedPassage(chunk_id=chunk_id, doc_name=doc_name, section=section, text=text))
            sources.append(
                SourceReference(
                    chunk_id=chunk_id,
                    doc_id=str(metadata.get("doc_id", "")),
                    doc_name=doc_name,
                    section=section,
                    lecture=None if metadata.get("lecture") is None else int(str(metadata["lecture"])),
                    distance=None if distance is None else float(distance),
                    snippet=" ".join(text.split())[:SNIPPET_CHARS],
                )
            )
            scores.append(float(distance) if distance is not None else float("nan"))

        logger.info("retrieval: %d passages for %r", len(passages), query[:60])
        if not passages:
            return RetrievalResult(status=RetrievalStatus.EMPTY, top_k=limit)
        return RetrievalResult.from_matches(tuple(passages), tuple(sources), tuple(scores), limit)
