"""Split lecture Markdown into retrieval-sized chunks.

Design (see ``docs/RAG/knowledge-base.md`` §3):

- The document is cut at Markdown headings first, so a heading stays with its content.
- Every chunk repeats its own heading, so it is understandable on its own.
- Long sections are split on paragraph boundaries with a character overlap; fenced code
  blocks are never cut in half.
- Chunk ids are deterministic, which makes re-indexing idempotent.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from app.adapters.loader import LectureDocument

CHUNKER_VERSION = "2"
DEFAULT_MAX_CHARS = 900
DEFAULT_OVERLAP_CHARS = 120
MIN_CHUNK_CHARS = 80

_HEADING = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
_FENCE = "```"


@dataclass(frozen=True, slots=True)
class Chunk:
    """One retrievable piece of a lecture with its provenance."""

    chunk_id: str
    doc_id: str
    course_id: str
    doc_name: str
    lecture: int
    section: str
    chunk_index: int
    text: str
    text_hash: str


@dataclass(frozen=True, slots=True)
class _Block:
    section: str
    heading_line: str
    body: str


def _blocks(text: str) -> list[_Block]:
    """Cut the document into heading-led blocks, tracking the heading path."""
    blocks: list[_Block] = []
    stack: list[tuple[int, str]] = []
    heading_line = ""
    body_lines: list[str] = []
    active_fence = ""

    def flush() -> None:
        body = "\n".join(body_lines).strip()
        section = " > ".join(title for level, title in stack if level > 1)
        blocks.append(_Block(section=section, heading_line=heading_line, body=body))

    for line in text.split("\n"):
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            marks = fence_match.group(1)
            if not active_fence:
                active_fence = marks
            elif marks[0] == active_fence[0] and len(marks) >= len(active_fence):
                active_fence = ""
            body_lines.append(line)
            continue
        if active_fence:
            body_lines.append(line)
            continue
        match = _HEADING.match(line)
        if match:
            flush()
            level = len(match.group("marks"))
            title = match.group("title")
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            heading_line = line.rstrip()
            body_lines = []
        else:
            body_lines.append(line)
    flush()
    return [block for block in blocks if block.heading_line or block.body]


def _paragraphs(text: str) -> list[str]:
    """Split on blank lines, but never inside a fenced code block."""
    paragraphs: list[str] = []
    current: list[str] = []
    active_fence = ""
    for line in text.split("\n"):
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            marks = fence_match.group(1)
            if not active_fence:
                active_fence = marks
            elif marks[0] == active_fence[0] and len(marks) >= len(active_fence):
                active_fence = ""
        if not active_fence and not line.strip() and current:
            paragraphs.append("\n".join(current).strip())
            current = []
        else:
            current.append(line)
    if current:
        paragraphs.append("\n".join(current).strip())
    return [paragraph for paragraph in paragraphs if paragraph]


def _overlap_tail(text: str, overlap: int) -> str:
    """Return the last ``overlap`` characters of ``text``, snapped to a word boundary."""
    if overlap <= 0 or not text:
        return ""
    tail = text[-overlap:]
    space = tail.find(" ")
    if space != -1:
        tail = tail[space + 1 :]
    return "" if _FENCE in tail else tail.strip()


def _split_long_text(text: str, budget: int, overlap: int) -> list[str]:
    """Hard-split an oversized paragraph, preferring line and word boundaries."""
    pieces: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + budget, len(text))
        if end < len(text):
            window = text[start:end]
            newline = window.rfind("\n")
            if newline > budget // 2:
                end = start + newline
            else:
                space = window.rfind(" ")
                if space > budget // 2:
                    end = start + space
        piece = text[start:end].strip()
        if piece:
            pieces.append(piece)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return pieces


def _split_body(body: str, budget: int, overlap: int) -> list[str]:
    """Group paragraphs into pieces of at most ``budget`` characters."""
    pieces: list[str] = []
    current = ""
    for paragraph in _paragraphs(body):
        if len(paragraph) > budget:
            if current:
                pieces.append(current)
                current = ""
            if re.search(r"(?m)^\s*(?:`{3,}|~{3,})", paragraph):
                pieces.append(paragraph)  # a code block is kept whole, even if oversized
            else:
                pieces.extend(_split_long_text(paragraph, budget, overlap))
            continue
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if len(candidate) <= budget:
            current = candidate
            continue
        pieces.append(current)
        tail = _overlap_tail(current, overlap)
        current = f"{tail}\n\n{paragraph}" if tail else paragraph
        if len(current) > budget:
            current = paragraph
    if current:
        pieces.append(current)
    return pieces


def chunk_document(
    document: LectureDocument,
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap: int = DEFAULT_OVERLAP_CHARS,
    min_chars: int = MIN_CHUNK_CHARS,
) -> list[Chunk]:
    """Turn one lecture into deterministic, self-describing chunks."""
    chunks: list[Chunk] = []
    index = 0

    for block in _blocks(document.text):
        budget = max(max_chars - len(block.heading_line) - 2, 200)
        if len(block.heading_line) + 2 + len(block.body) <= max_chars:
            pieces = [block.body]
        else:
            pieces = _split_body(block.body, budget, overlap)

        for piece in pieces:
            text = f"{block.heading_line}\n\n{piece}".strip() if block.heading_line else piece.strip()
            if len(text) < min_chars:
                continue
            text_hash = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
            chunks.append(
                Chunk(
                    chunk_id=f"{document.doc_id}:{index:04d}:{text_hash}",
                    doc_id=document.doc_id,
                    course_id=document.course_id,
                    doc_name=document.doc_name,
                    lecture=document.lecture,
                    section=block.section,
                    chunk_index=index,
                    text=text,
                    text_hash=text_hash,
                )
            )
            index += 1

    return chunks
