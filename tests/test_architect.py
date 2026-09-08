from pathlib import Path

from workflow.agents.architect import run_architect


class FakeClient:
    """Returns a fixed sequence of chat responses."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def chat(self, system, user):
        self.calls += 1
        return self.responses.pop(0)


DOCS = (
    "=== FILE: docs/architecture/system-overview.md ===\n"
    "# System Overview\n"
    "=== END FILE ===\n"
    "=== FILE: docs/architecture/component-design.md ===\n"
    "# Components\n"
    "=== END FILE ===\n"
    "=== FILE: docs/architecture/deployment-topology.md ===\n"
    "# Topology\n"
    "=== END FILE ===\n"
    "=== FILE: docs/architecture/adr/ADR-001-test.md ===\n"
    "# ADR\n"
    "=== END FILE ===\n"
)

OPENAPI = (
    "=== FILE: docs/api/openapi.yaml ===\n"
    "openapi: 3.0.3\n"
    "info: {}\n"
    "paths:\n"
    "  /health:\n"
    "    get: {}\n"
    "=== END FILE ===\n"
)


def test_architect_writes_canonical_paths(tmp_path):
    client = FakeClient([DOCS, OPENAPI])
    output = run_architect(client, "demo", tmp_path, max_retries=0)

    assert output.result.ok
    assert (tmp_path / "docs" / "architecture" / "system-overview.md").is_file()
    assert (tmp_path / "docs" / "architecture" / "component-design.md").is_file()
    assert (tmp_path / "docs" / "architecture" / "deployment-topology.md").is_file()
    assert (tmp_path / "docs" / "architecture" / "adr" / "ADR-001-test.md").is_file()
    assert (tmp_path / "docs" / "api" / "openapi.yaml").is_file()
    # Must not produce the old doubled prefix.
    assert not (tmp_path / "docs" / "docs").exists()
