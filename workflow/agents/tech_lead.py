"""FR2: Tech lead responsibility.

Breaks the architecture into incremental tickets with scope boundaries,
acceptance criteria / definition-of-done, and dependency ordering. Writes
``workspace/<run_id>/tickets/tickets.json``.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from ..artifacts import extract_json
from ..llm_client import LLMClient
from ..prompts import TECH_LEAD_SYSTEM, tech_lead_prompt
from . import StageResult


class TicketError(Exception):
    """Raised when the tech-lead output is not a valid ticket list."""


@dataclass
class Ticket:
    id: str
    title: str
    scope: List[str] = field(default_factory=list)
    out_of_scope: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)
    definition_of_done: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    files_touched: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "scope": self.scope,
            "out_of_scope": self.out_of_scope,
            "acceptance_criteria": self.acceptance_criteria,
            "definition_of_done": self.definition_of_done,
            "depends_on": self.depends_on,
            "files_touched": self.files_touched,
        }


def _as_list(value: object) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def parse_tickets(data: object) -> List[Ticket]:
    if isinstance(data, dict):
        data = data.get("tickets")
    if not isinstance(data, list) or not data:
        raise TicketError("no 'tickets' list found in tech-lead output")

    tickets: List[Ticket] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise TicketError(f"ticket at index {index} is not an object")
        tid = str(item.get("id") or f"T{index + 1}").strip()
        title = str(item.get("title") or "").strip() or f"Ticket {tid}"
        tickets.append(
            Ticket(
                id=tid,
                title=title,
                scope=_as_list(item.get("scope")),
                out_of_scope=_as_list(item.get("out_of_scope")),
                acceptance_criteria=_as_list(item.get("acceptance_criteria")),
                definition_of_done=_as_list(item.get("definition_of_done")),
                depends_on=_as_list(item.get("depends_on")),
                files_touched=_as_list(item.get("files_touched")),
            )
        )

    ids = [t.id for t in tickets]
    if len(set(ids)) != len(ids):
        raise TicketError("duplicate ticket ids")
    for ticket in tickets:
        ticket.depends_on = [d for d in ticket.depends_on if d in ids and d != ticket.id]
    return tickets


def run_tech_lead(
    client: LLMClient,
    requirement: str,
    architecture_context: str,
    run_dir: Path,
    *,
    max_retries: int = 1,
) -> Tuple[StageResult, List[Ticket]]:
    started = time.time()
    tickets_dir = run_dir / "tickets"
    tickets_dir.mkdir(parents=True, exist_ok=True)

    prompt = tech_lead_prompt(requirement, architecture_context)
    attempts = 0
    last_error: Optional[str] = None
    while True:
        raw = client.chat(TECH_LEAD_SYSTEM, prompt)
        data = extract_json(raw)
        try:
            tickets = parse_tickets(data)
        except TicketError as exc:
            last_error = str(exc)
            attempts += 1
            if attempts > max_retries:
                return (
                    StageResult(
                        ok=False, error=last_error, retries_used=attempts,
                        duration_s=time.time() - started, raw_chars=len(raw),
                    ),
                    [],
                )
            prompt = tech_lead_prompt(requirement, architecture_context) + (
                f"\n\nIMPORTANT: previous reply was invalid ({last_error}). "
                "Reply again with ONLY the JSON object."
            )
            continue
        break

    (tickets_dir / "tickets.json").write_text(
        json.dumps({"tickets": [t.to_dict() for t in tickets]}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return (
        StageResult(
            ok=True,
            retries_used=attempts,
            duration_s=time.time() - started,
            raw_chars=len(raw),
            detail=f"{len(tickets)} tickets",
        ),
        tickets,
    )
