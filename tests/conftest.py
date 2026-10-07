"""Shared pytest fixtures: make `model/` importable and keep module state fresh."""

import importlib
import os
import sys

import pytest

# `model/` has no __init__.py, so we add it to sys.path and import the single-file
# app directly. Tests therefore do `import ollama_workflow as m`.
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))
if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)

import ollama_workflow  # noqa: E402


@pytest.fixture(autouse=True)
def _fresh_module():
    """Reload the module before every test so config/env globals are clean."""
    importlib.reload(ollama_workflow)
    yield
