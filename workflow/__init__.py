"""Local multi-LLM coding workflow (Flask orchestrator).

Implements the first three functional responsibilities of the assignment:

- FR1 Architecture:   produce architecture artifacts + an OpenAPI spec.
- FR2 Tech lead:      break work into tickets (scope, DoD, dependencies).
- FR3 Implementation: run N >= 2 parallel coding workers producing multi-file
                      changes in a repository.

Hard Requirement 1 (>=2 local endpoints + config-based routing) is handled by
:mod:`workflow.config`.
"""

__version__ = "0.1.0"
