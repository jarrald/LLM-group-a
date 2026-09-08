"""FR1: Architecture responsibility.

Produces architecture artifacts (component decomposition, interface contracts,
deployment topology, ADRs) plus an OpenAPI specification, and writes them to
``workspace/<run_id>/docs/``.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from ..artifacts import FileBlock, clip_text, extract_yaml, parse_file_blocks, write_file_blocks
from ..llm_client import LLMClient
from ..prompts import ARCHITECT_SYSTEM, architect_docs_prompt, architect_openapi_prompt
from . import StageResult

REQUIRED_DOCS = ("system-overview.md", "component-design.md", "deployment-topology.md")
OPENAPI_PATH = "docs/api/openapi.yaml"


@dataclass
class ArchitectOutput:
    result: StageResult
    tech_lead_context: str
    worker_context: str


def _block_for(blocks: List[FileBlock], suffix: str) -> Optional[FileBlock]:
    for block in blocks:
        if block.path.endswith(suffix):
            return block
    return None


def _content(block: Optional[FileBlock]) -> str:
    return block.content if block else ""


def _has_adr(blocks: List[FileBlock]) -> bool:
    return any("/adr/" in b.path for b in blocks)


def _canonical_docs_blocks(blocks: List[FileBlock]) -> List[FileBlock]:
    """Normalise emitted paths to the canonical ``docs/...`` layout."""
    out: List[FileBlock] = []
    for block in blocks:
        name = Path(block.path).name
        lower = block.path.lower()
        if name == "system-overview.md":
            path = "docs/architecture/system-overview.md"
        elif name == "component-design.md":
            path = "docs/architecture/component-design.md"
        elif name == "deployment-topology.md":
            path = "docs/architecture/deployment-topology.md"
        elif "adr" in lower:
            path = f"docs/architecture/adr/{name}"
        elif name == "openapi.yaml":
            path = "docs/api/openapi.yaml"
        else:
            path = block.path
        out.append(FileBlock(path=path, content=block.content))
    return out


def run_architect(
    client: LLMClient,
    requirement: str,
    run_dir: Path,
    *,
    max_retries: int = 1,
) -> ArchitectOutput:
    started = time.time()
    docs_dir = run_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    # 1) Markdown architecture artifacts.
    docs_prompt = architect_docs_prompt(requirement)
    docs_blocks: List[FileBlock] = []
    attempts = 0
    last_error: Optional[str] = None
    while True:
        raw = client.chat(ARCHITECT_SYSTEM, docs_prompt)
        docs_blocks = parse_file_blocks(raw)
        missing = [s for s in REQUIRED_DOCS if _block_for(docs_blocks, s) is None]
        if not missing and _has_adr(docs_blocks):
            break
        last_error = "missing: " + (", ".join(missing) if missing else "ADR")
        attempts += 1
        if attempts > max_retries:
            return ArchitectOutput(
                result=StageResult(
                    ok=False, error=last_error, retries_used=attempts,
                    duration_s=time.time() - started,
                ),
                tech_lead_context="",
                worker_context="",
            )
        docs_prompt = architect_docs_prompt(requirement) + (
            f"\n\nIMPORTANT: previous reply was incomplete ({last_error}). "
            "Reply again with ALL requested files."
        )

    write_file_blocks(run_dir, _canonical_docs_blocks(docs_blocks))

    overview = _content(_block_for(docs_blocks, "system-overview.md"))
    components = _content(_block_for(docs_blocks, "component-design.md"))
    component_summary = clip_text(components, 6000, "component-design.md")
    overview_summary = clip_text(overview, 3000, "system-overview.md")
    tech_lead_context = overview_summary + "\n\n" + component_summary

    # 2) OpenAPI specification.
    openapi_prompt = architect_openapi_prompt(requirement, component_summary)
    oa_attempts = 0
    while True:
        raw = client.chat(ARCHITECT_SYSTEM, openapi_prompt)
        blocks = parse_file_blocks(raw)
        openapi_block = _block_for(blocks, "openapi.yaml")
        spec_text = openapi_block.content if openapi_block else raw
        spec = extract_yaml(spec_text)
        if isinstance(spec, dict) and spec.get("openapi") and spec.get("paths"):
            write_file_blocks(run_dir, [FileBlock(path=OPENAPI_PATH, content=spec_text)])
            break
        oa_attempts += 1
        if oa_attempts > max_retries:
            return ArchitectOutput(
                result=StageResult(
                    ok=False,
                    error="OpenAPI spec not valid (needs openapi + paths)",
                    retries_used=oa_attempts,
                    duration_s=time.time() - started,
                ),
                tech_lead_context="",
                worker_context="",
            )
        openapi_prompt = architect_openapi_prompt(requirement, component_summary) + (
            "\n\nIMPORTANT: previous reply was rejected. Emit a single valid "
            "OpenAPI 3.0.3 YAML file block with openapi, info, paths."
        )

    return ArchitectOutput(
        result=StageResult(
            ok=True,
            retries_used=attempts + oa_attempts,
            duration_s=time.time() - started,
            detail="architecture artifacts + OpenAPI spec",
        ),
        tech_lead_context=tech_lead_context,
        worker_context=component_summary,
    )
