"""Load lecture Markdown from the course material directory.

Layout (ADR-020): the RAG input is every ``*.md`` inside a ``week<N>`` directory under the
configured root, so a week may contain one or several documents. Raw material (original PDFs,
notebooks, ``source/``) is never indexed.

```text
docs/RAG/llm_for_developers/
├── source/week1/…                     # originals (git-ignored binaries)
└── llm_friendly/
    ├── week1/week1_complete_rag.md
    ├── week2/week2_prompt_engineering_rag.md
    └── week3/week3_overview.md, week3_hallucinations.md, …
```

Metadata is derived from the path and the first ``#`` heading — the course files are never
modified.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

_WEEK_DIRECTORY = re.compile(r"^week(\d+)$", re.IGNORECASE)
_H1 = re.compile(r"^#\s+(?P<title>.+?)\s*$")
_RAW_MATERIAL_DIRECTORY = "source"


@dataclass(frozen=True, slots=True)
class LectureDocument:
    """One lecture document, ready to be chunked."""

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


def week_number(path: Path, root: Path) -> int | None:
    """Return the week number of ``path``, taken from a ``week<N>`` directory below ``root``."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        return None
    for part in relative.parts[:-1]:
        match = _WEEK_DIRECTORY.match(part)
        if match:
            return int(match.group(1))
    return None


def load_lecture(path: Path, course_id: str, root: Path) -> LectureDocument:
    """Load a single Markdown lecture that lives inside a ``week<N>`` directory."""
    lecture = week_number(path, root)
    if lecture is None:
        raise ValueError(f"{path} is not inside a week<N> directory below {root}")

    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return LectureDocument(
        doc_id=path.stem,
        doc_name=read_lecture_title(text, fallback=f"Week {lecture}"),
        lecture=lecture,
        course_id=course_id,
        path=path,
        text=text,
    )


def discover_lectures(directory: Path, course_id: str) -> list[LectureDocument]:
    """Find every Markdown lecture under ``directory``, ordered by week and file name."""
    if not directory.is_dir():
        raise FileNotFoundError(f"course material directory not found: {directory}")

    documents: list[LectureDocument] = []
    for path in sorted(directory.rglob("*.md")):
        relative_parts = [part.lower() for part in path.relative_to(directory).parts]
        if _RAW_MATERIAL_DIRECTORY in relative_parts:
            logger.debug("skipping raw material: %s", path)
            continue
        if week_number(path, directory) is None:
            logger.debug("skipping %s: not inside a week<N> directory", path)
            continue
        documents.append(load_lecture(path, course_id, directory))

    documents.sort(key=lambda document: (document.lecture, document.doc_id))
    return documents
