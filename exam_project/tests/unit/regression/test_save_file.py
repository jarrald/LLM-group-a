"""Tests for archiving a run: notebook detection and code extraction from a stream."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from regression.rag import Answer, extract_code, save_file, wants_notebook

CODE = "import pandas as pd\nfrom sklearn.linear_model import LinearRegression\n\nmodel = LinearRegression().fit([[1]], [2])\nprint(model)\n"


def make_answer(text: str) -> Answer:
    return Answer(text=text, hits=[], seconds=1.0, tokens_per_second=None, model="gemma3:270m")


@pytest.mark.parametrize(
    "prompt",
    [
        "Can you give me a full .ipynb file that does linear regression?",
        "Please make a jupyter notebook that does a linear regression",
        "make me a notebook",
        "output.ipynb",
    ],
)
def test_wants_notebook_recognises_the_usual_phrasings(prompt: str) -> None:
    assert wants_notebook(prompt) is True


@pytest.mark.parametrize("prompt", ["write a python script", "give me a .py file", "explain linear regression"])
def test_wants_notebook_is_false_for_script_requests(prompt: str) -> None:
    assert wants_notebook(prompt) is False


def test_save_file_writes_a_notebook_for_an_ipynb_request(tmp_path: Path) -> None:
    answer = make_answer(f"```python\n{CODE}```\n")

    saved = save_file("Can you give me a full .ipynb file that does linear regression?", answer, run_dir=tmp_path)

    assert saved.name == "output.ipynb"
    notebook = json.loads(saved.read_text(encoding="utf-8"))
    sources = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "code")
    assert "LinearRegression().fit" in sources
    assert (tmp_path / "prompt.md").is_file()
    assert (tmp_path / "answer.md").is_file()


def test_save_file_keeps_the_raw_answer_next_to_the_extracted_code(tmp_path: Path) -> None:
    raw = f"I will use the retrieved guide.\n\n```python\n{CODE}```\n\nThis came from the guide."
    answer = make_answer(raw)

    saved = save_file("write a python script please", answer, run_dir=tmp_path)

    assert saved.name == "output.py"
    assert "LinearRegression().fit" in saved.read_text(encoding="utf-8")
    recorded = (tmp_path / "answer.md").read_text(encoding="utf-8")
    assert "I will use the retrieved guide." in recorded
    assert "This came from the guide." in recorded


def test_save_file_writes_a_script_when_no_notebook_is_requested(tmp_path: Path) -> None:
    answer = make_answer(f"```python\n{CODE}```\n")

    saved = save_file("write a python script please", answer, run_dir=tmp_path)

    assert saved.name == "output.py"
    assert "LinearRegression().fit" in saved.read_text(encoding="utf-8")


def test_extract_code_keeps_an_unclosed_fence() -> None:
    answer = "```python\nimport pandas as pd\ndf = pd.read_csv('x.csv')\n"

    assert extract_code(answer) == "import pandas as pd\ndf = pd.read_csv('x.csv')\n"


def test_extract_code_ignores_an_empty_block() -> None:
    assert extract_code("```python\n```") is None


def test_save_file_keeps_unclosed_code_instead_of_the_raw_answer(tmp_path: Path) -> None:
    answer = make_answer("```python\nimport pandas as pd\nprint('hi')\n")

    saved = save_file("write a python script please", answer, run_dir=tmp_path)

    assert saved.name == "output.py"
    assert "print('hi')" in saved.read_text(encoding="utf-8")
