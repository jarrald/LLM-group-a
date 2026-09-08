"""Workflow agents (Architect, Tech lead, Worker)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class StageResult:
    """Outcome of a single agent stage (or a single worker ticket)."""

    ok: bool
    files: List[str] = field(default_factory=list)
    error: Optional[str] = None
    detail: Optional[str] = None
    retries_used: int = 0
    duration_s: float = 0.0
    raw_chars: int = 0

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "files": self.files,
            "error": self.error,
            "detail": self.detail,
            "retries_used": self.retries_used,
            "duration_s": round(self.duration_s, 2),
            "raw_chars": self.raw_chars,
        }
