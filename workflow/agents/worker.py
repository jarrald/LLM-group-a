"""FR3: coding worker.

A single worker call implements exactly one ticket and returns complete files.
The pipeline runs multiple workers concurrently (see ``workflow.pipeline``).
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from ..artifacts import ArtifactError, parse_file_blocks, write_file_blocks
from ..llm_client import LLMClient
from ..prompts import WORKER_SYSTEM, worker_prompt
from . import StageResult
from .tech_lead import Ticket


def run_worker(
    client: LLMClient,
    ticket: Ticket,
    architecture_context: str,
    repo_dir: Path,
    *,
    max_retries: int = 1,
    worker_name: str = "worker",
) -> StageResult:
    started = time.time()
    prompt = worker_prompt(ticket.to_dict(), architecture_context)
    attempts = 0
    last_error: Optional[str] = None
    while True:
        raw = client.chat(WORKER_SYSTEM, prompt)
        try:
            blocks = parse_file_blocks(raw)
            if not blocks:
                raise ArtifactError("no file blocks found in worker output")
            written = write_file_blocks(repo_dir, blocks)
        except Exception as exc:  # noqa: BLE001 - isolate failures per ticket
            last_error = str(exc)
            attempts += 1
            if attempts > max_retries:
                return StageResult(
                    ok=False,
                    error=last_error,
                    retries_used=attempts,
                    duration_s=time.time() - started,
                    raw_chars=len(raw),
                    detail=f"{worker_name} failed ticket {ticket.id}",
                )
            prompt = worker_prompt(ticket.to_dict(), architecture_context) + (
                f"\n\nIMPORTANT: previous reply failed to parse ({last_error}). "
                "Reply again using the file-block format EXACTLY."
            )
            continue
        return StageResult(
            ok=True,
            files=written,
            retries_used=attempts,
            duration_s=time.time() - started,
            raw_chars=len(raw),
            detail=f"{worker_name} implemented {ticket.id}",
        )
