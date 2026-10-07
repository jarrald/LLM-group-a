"""Probe: which agent/task causes CrewAI to send native tool schemas?

CrewAI only sends tool schemas when an agent has at least one tool, and the
`tester:latest` model (deepseek-coder) does not advertise tool support, so
Ollama rejects the request with HTTP 400. This probe aborts at the first
agent that would send tools and prints the tool names.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import crewai.agent.core as core  # noqa: E402

_orig = core.Agent._supports_native_tool_calling


def patched(self, tools):
    if tools:
        names = [getattr(t, "name", repr(t)) for t in tools]
        print(f">>> agent={self.role!r} WOULD SEND TOOLS: {names}", flush=True)
        raise SystemExit(0)
    return _orig(self, tools)


core.Agent._supports_native_tool_calling = patched

import crew  # noqa: E402

sys.exit(crew.main(["--run-id", "_probe_tools"]))
