"""Load lecture Markdown from the course material directory.

Layout (ADR-013):

```text
docs/RAG/llm_for_developers/
├── source/week1/              # original PDFs and exercise files (git-ignored)
└── week1/week1_complete_rag.md
```

The Markdown is the authoritative RAG input. Metadata is derived from the path and the
first ``#`` heading — the course files are never modified.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

_WEEK_DIRECTORY = re.compile(r"^week(\d+)$")
_H1 = re.compile(r"^#\s+(?P<title>.+?)\s*$")


@dataclass(frozen=True, slots=True)
class LectureDocument:
    """One lecture's Markdown, ready to be chunked."""

    doc_id: str
    doc_name: str
    lecture: int
    course_id: str
    path: Path
    text: str


def read_lecture_title(text: str, fallback: str) -> str:
    """Return the first level-1 heading of ``text``, or ``fallback`` if there is none."""
    for line in text.splitlines():
        match = _H1.match(line)
        if match:
            return match.group("title").strip()
    return fallback


def load_lecture(path: Path, course_id: str) -> LectureDocument:
    """Load a single ``week<N>_complete_rag.md`` file."""
    lecture = int(_WEEK_DIRECTORY.match(path.parent.name).group(1))  # type: ignore[union-attr]
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    doc_id = f"week-{lecture}"
    return LectureDocument(
        doc_id=doc_id,
        doc_name=read_lecture_title(text, fallback=f"Week {lecture}"),
        lecture=lecture,
        course_id=course_id,
        path=path,
        text=text,
    )


def discover_lectures(directory: Path, course_id: str) -> list[LectureDocument]:
    """Find every ``week<N>/week<N>_complete_rag.md`` under ``directory``, ordered by week."""
    if not directory.is_dir():
        raise FileNotFoundError(f"course material directory not found: {directory}")

    documents: list[LectureDocument] = []
    for week_directory in sorted(directory.iterdir()):
        if not week_directory.is_dir() or not _WEEK_DIRECTORY.match(week_directory.name):
            continue
        markdown_path = week_directory / f"{week_directory.name}_complete_rag.md"
        if not markdown_path.is_file():
            logger.warning("skipping %s: %s not found", week_directory.name, markdown_path.name)
            continue
        documents.append(load_lecture(markdown_path, course_id))

    documents.sort(key=lambda document: document.lecture)
    return documents
