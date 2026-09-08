"""Parsing and writing of LLM-generated artifacts (files, JSON, YAML).

Agents emit multi-file output using an explicit file-block format so that the
generated content itself can contain markdown code fences without confusing the
parser::

    === FILE: relative/path/to/file.py ===
    ...file content...
    === END FILE ===

A markdown-fenced fallback (`` ```path: relative/path ``` ``) is also supported
because small local models occasionally wrap output in fences anyway.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional

import yaml


class ArtifactError(Exception):
    """Raised when generated artifacts cannot be parsed or written safely."""


@dataclass(frozen=True)
class FileBlock:
    path: str
    content: str


_HEADER_RE = re.compile(r"^\s*={2,}\s*FILE:\s*(.+?)\s*={2,}\s*$")
_END_RE = re.compile(r"^\s*={2,}\s*END\s+FILE\s*={2,}\s*$", re.IGNORECASE)
_FENCE_RE = re.compile(r"```(?P<info>[^\n`]*)\n(?P<body>.*?)```", re.DOTALL)
_EXTENSION_RE = re.compile(
    r"\.(?:md|markdown|py|ya?ml|json|txt|html?|css|js|ts|toml|ini|cfg|sh|sql|env)$",
    re.IGNORECASE,
)


def sanitize_rel_path(rel_path: str) -> str:
    path = rel_path.strip().strip("'\"`").replace("\\", "/")
    return re.sub(r"^\./", "", path)


def safe_target_path(base_dir: Path, rel_path: str) -> Path:
    rel = sanitize_rel_path(rel_path)
    if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
        raise ArtifactError(f"unsafe artifact path: {rel_path!r}")
    target = (base_dir / rel).resolve()
    base = base_dir.resolve()
    if target != base and base not in target.parents:
        raise ArtifactError(f"path escapes workspace: {rel_path!r}")
    return target


def _parse_explicit_blocks(text: str) -> List[FileBlock]:
    blocks: List[FileBlock] = []
    current_path: Optional[str] = None
    current: List[str] = []

    def close() -> None:
        nonlocal current_path, current
        if current_path is not None:
            content = "\n".join(current).strip("\n") + "\n"
            blocks.append(FileBlock(path=current_path, content=content))
        current_path = None
        current = []

    for line in text.splitlines():
        header = _HEADER_RE.match(line)
        if header:
            close()
            current_path = sanitize_rel_path(header.group(1))
            continue
        if _END_RE.match(line) and current_path is not None:
            close()
            continue
        if current_path is not None:
            current.append(line)
    close()

    # Keep the last occurrence when a path is emitted more than once.
    deduped: dict = {}
    for block in blocks:
        deduped[block.path] = block
    return list(deduped.values())


def _parse_fenced_blocks(text: str) -> List[FileBlock]:
    blocks: List[FileBlock] = []
    for match in _FENCE_RE.finditer(text):
        info = (match.group("info") or "").strip()
        path: Optional[str] = None
        pm = re.match(r"path[:=]\s*(.+)$", info, re.IGNORECASE)
        if pm:
            path = pm.group(1).strip()
        elif "/" in info or _EXTENSION_RE.search(info):
            path = info
        if path:
            blocks.append(FileBlock(path=sanitize_rel_path(path), content=match.group("body")))
    return blocks


def parse_file_blocks(text: str) -> List[FileBlock]:
    explicit = _parse_explicit_blocks(text)
    if explicit:
        return explicit
    return _parse_fenced_blocks(text)


def write_file_blocks(base_dir: Path, blocks: List[FileBlock]) -> List[str]:
    written: List[str] = []
    for block in blocks:
        target = safe_target_path(base_dir, block.path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(block.content, encoding="utf-8")
        written.append(block.path)
    return written


def _first_bracket_chunk(text: str) -> Optional[str]:
    for opener, closer in (("{", "}"), ("[", "]")):
        start = text.find(opener)
        if start == -1:
            continue
        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(text)):
            ch = text[i]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
            elif ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]
    return None


def extract_json(text: str) -> Any:
    candidates: List[str] = []
    fence = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        candidates.append(fence.group(1).strip())
    chunk = _first_bracket_chunk(text)
    if chunk:
        candidates.append(chunk)
    candidates.append(text.strip())
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None


def extract_yaml(text: str) -> Optional[dict]:
    candidates: List[str] = []
    fence = re.search(r"```(?:yaml|yml)?\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        candidates.append(fence.group(1))
    candidates.append(text)
    for candidate in candidates:
        try:
            data = yaml.safe_load(candidate)
        except yaml.YAMLError:
            continue
        if isinstance(data, dict):
            return data
    return None


def clip_text(text: str, limit: int, label: str = "") -> str:
    """Clip a string for scoped context handoff (avoid silent context loss)."""
    if len(text) <= limit:
        return text
    half = limit // 2
    return (
        f"[{label} clipped to {limit} chars]\n"
        f"{text[:half]}\n... [truncated] ...\n{text[-half:]}"
    )


def list_files(root: Path) -> List[str]:
    if not root.exists():
        return []
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
