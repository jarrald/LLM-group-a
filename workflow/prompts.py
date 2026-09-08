"""Prompt templates for the workflow agents.

Prompts are kept here (and versioned in git) so workflow runs are reproducible
and prompts can be reviewed/tuned without touching agent code.
"""

from __future__ import annotations

import json

FILE_FORMAT_RULES = """OUTPUT FORMAT (critical):
Write every file using EXACTLY this format, with nothing else before, between or after the blocks:

=== FILE: <relative/path/to/file> ===
<complete file content>
=== END FILE ===

Rules:
- One block per file. Use the exact relative paths requested.
- Do NOT wrap the blocks in markdown code fences.
- Content inside a block may use markdown/code normally.
- Do not add explanations outside the FILE blocks."""

ARCHITECT_SYSTEM = """You are the Architecture agent in a local multi-LLM software development workflow.
You turn a single product requirement into precise, concrete, implementation-ready architecture artifacts.
You always respond with complete file contents in the required file-block format and nothing else."""

TECH_LEAD_SYSTEM = """You are the Tech Lead agent in a local multi-LLM software development workflow.
You turn architecture artifacts into an incremental delivery plan of small tickets.
You respond ONLY with a single JSON object -- no markdown fences, no commentary."""

WORKER_SYSTEM = """You are a coding worker agent in a local multi-LLM software development workflow.
You implement EXACTLY ONE assigned ticket and produce complete, working source files.
You never leave TODOs or placeholder pass statements, and never implement another ticket's scope.
You always respond with complete files in the required file-block format and nothing else."""


def architect_docs_prompt(requirement: str) -> str:
    return (
        "Requirement:\n"
        f"{requirement}\n\n"
        "Produce the following architecture artifacts for a small, practical implementation:\n\n"
        "1. docs/architecture/system-overview.md\n"
        "   Purpose, main behaviour, key quality goals, tech stack summary.\n"
        "2. docs/architecture/component-design.md\n"
        "   One section per component (3-6 components) with: name, responsibility,\n"
        "   interfaces it exposes (REST routes / functions), and dependencies.\n"
        "3. docs/architecture/deployment-topology.md\n"
        "   How the system runs locally (processes, ports), deployment constraints\n"
        "   (local-only, no public endpoints), and environment/config needs.\n"
        "4. docs/architecture/adr/ADR-001-technology-choices.md\n"
        "   A short ADR (Context / Decision / Consequences) for the main technology choice.\n"
        "5. docs/architecture/adr/ADR-002-<topic>.md\n"
        "   One further important decision, with a meaningful filename replacing <topic>.\n\n"
        + FILE_FORMAT_RULES
    )


def architect_openapi_prompt(requirement: str, component_summary: str) -> str:
    return (
        "Requirement:\n"
        f"{requirement}\n\n"
        "Component summary:\n"
        f"{component_summary}\n\n"
        "Produce docs/api/openapi.yaml: a complete, valid OpenAPI 3.0.3 specification\n"
        "for the HTTP API. Include info, one path item per endpoint, request/response\n"
        "schemas, and the top-level fields `openapi`, `info`, and `paths`.\n\n"
        + FILE_FORMAT_RULES
    )


def tech_lead_prompt(requirement: str, architecture_context: str) -> str:
    return (
        "Requirement:\n"
        f"{requirement}\n\n"
        "Architecture context:\n"
        f"{architecture_context}\n\n"
        "Break the work into 4-6 tickets that two parallel coding workers can implement.\n"
        "Respond with ONLY this JSON structure:\n"
        '{"tickets": [\n'
        '  {\n'
        '    "id": "T1",\n'
        '    "title": "short imperative title",\n'
        '    "scope": ["what is included"],\n'
        '    "out_of_scope": ["what is explicitly excluded"],\n'
        '    "acceptance_criteria": ["verifiable criteria"],\n'
        '    "definition_of_done": ["DoD items"],\n'
        '    "depends_on": ["ids of tickets that must finish first, or []"],\n'
        '    "files_touched": ["relative file paths this ticket creates or changes"]\n'
        "  }\n"
        "]}\n\n"
        "Rules:\n"
        "- ids are T1, T2, ...; depends_on may only reference earlier ticket ids.\n"
        "- Partition by FILE: each relative file path may appear in exactly ONE ticket's\n"
        "  files_touched. Never share a file between tickets.\n"
        "- Make most tickets independent (depends_on = []) so workers run in parallel.\n"
        "  Use a dependency only when a ticket genuinely cannot be written first.\n"
        "- Each ticket owns a cohesive set of files (e.g. data model, API routes,\n"
        "  config + logging, health check).\n"
        "- Tickets together must cover every component from the architecture.\n"
        "- Output raw JSON only."
    )


def worker_prompt(ticket: dict, architecture_context: str) -> str:
    return (
        "Assigned ticket (JSON):\n"
        f"{json.dumps(ticket, indent=2, ensure_ascii=False)}\n\n"
        "Architecture context:\n"
        f"{architecture_context}\n\n"
        "Implement this ticket now.\n"
        "- Write complete file contents for every file in `files_touched` (you may add\n"
        "  a few extra small files if strictly required).\n"
        "- These files are owned solely by this ticket; write complete, runnable,\n"
        "  self-contained files.\n"
        "- Use Python 3.10 and Flask where relevant. No external services; in-memory\n"
        "  storage is fine. Keep the implementation self-consistent.\n\n"
        + FILE_FORMAT_RULES
    )
