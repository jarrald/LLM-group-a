"""Check the compiled synopsis without changing the report or project evidence."""

from pathlib import Path
import unicodedata

import pymupdf


def main() -> int:
    pdf_path = Path(__file__).resolve().parent / "build" / "main.pdf"
    document = pymupdf.open(pdf_path)
    page_text = [page.get_text() for page in document]
    text = unicodedata.normalize("NFKC", " ".join("\n".join(page_text).split()))
    canonical = "".join(character for character in text.casefold() if character.isalnum() or character == "@")

    for page_number, page in enumerate(document, start=1):
        bounds = page.rect
        for block in page.get_text("blocks"):
            x0, y0, x1, y1 = block[:4]
            assert x0 >= -1 and y0 >= -1 and x1 <= bounds.width + 1 and y1 <= bounds.height + 1, (
                f"Text block outside page {page_number} bounds: {(x0, y0, x1, y1)}"
            )

    assert len(document) <= 5, f"Synopsis has {len(document)} pages; maximum is 5"
    required_text = [
        "Local Language Models and Machine Learning",
        "Applications, Experiments, and Implications",
        "How does StudyGraph use a local LLM and course material to help students study?",
        "How accurate were our three approaches---manual linear regression, local LLM with RAG, and local LLM without RAG---when predicting ice-cream revenue?",
        "Could the smaller local LLMs use retrieved documentation to generate working regression code?",
        "Ahmad Alkaseb",
        "Aleksandr Uktamovich Sorokin",
        "Jafar Alsukafi",
        "Jeppe Jeppsson",
        "Frederik Nicolajsen",
        "Roman Ghazi",
        "cph-aa540@stud.ek.dk",
        "also1002@stud.ek.dk",
        "jaal0002@stud.ek.dk",
        "jeje1006@stud.ek.dk",
        "frni1004@stud.ek.dk",
        "rogh1000@stud.ek.dk",
        "Abstract",
        "Introduction and research questions",
        "Relevant course concepts",
        "StudyGraph: implementation and architecture",
        "Manual regression versus local LLM prediction",
        "Reflection, limitations, and future work",
        "Conclusion",
        "References",
        "13.28",
        "107.15",
        "368.82",
        "20.3146",
        "72.2%",
        "12.8%",
        "15.0%",
        "same 75-row test set",
        "first-/eighth-degree example",
        "Manual regression",
        "LLM without RAG",
        "100.00",
        "1500.00",
        "1000.00",
        "0/6",
        "llama3.2:3b",
        "nomic-embed-text",
        "768-dimensional",
        "85 Markdown documents",
        "1,660 chunks",
        "900 characters",
        "120-character overlap",
        "qwen2.5-coder:7b",
        "21.2581",
        "49.8138",
        "32.55",
        "542.61",
        "918.39",
        "55.49",
        "55.39",
        "551.31",
        "552.82",
        "910.21",
        "630.00",
        "gemma3:270m",
        "gemma3:1b",
        "embeddinggemma",
        "566 chunks",
        "16,384",
        "Implemented StudyGraph turn flow",
        "Actual 4T implementation and purpose",
        "Predictions for the same three held-out inputs",
        "Controlled runs of 19 November 2026",
        "Prompt injection is a risk when an LLM processes external documents or user messages.",
        "is_jailbreak()",
        "six known jailbreak phrases",
        "we did not conduct a comprehensive security evaluation",
        "we did not systematically evaluate ambiguity handling.",
        "evaluate StudyGraph with real questions and users",
        "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "Attention Is All You Need",
        "Efficient Estimation of Word Representations in Vector Space",
        "Scikit-learn: Machine Learning in Python",
    ]
    missing = []
    for value in required_text:
        normalised = unicodedata.normalize("NFKC", value).casefold()
        expected = "".join(character for character in normalised if character.isalnum() or character == "@")
        if expected not in canonical:
            missing.append(value)
    assert not missing, f"Missing required PDF text: {missing}"
    forbidden_text = ["privacy", "hardware", "external AI services", "hosted inference", "accessibility", "societal study"]
    remaining = []
    for value in forbidden_text:
        normalised = unicodedata.normalize("NFKC", value).casefold()
        unexpected = "".join(character for character in normalised if character.isalnum())
        if unexpected in canonical:
            remaining.append(value)
    assert not remaining, f"Removed societal discussion still present: {remaining}"
    outdated_text = ["a different set of test rows", "described as 70/15/15", "confirm with our teacher"]
    remaining_outdated = []
    for value in outdated_text:
        normalised = unicodedata.normalize("NFKC", value).casefold()
        unexpected = "".join(character for character in normalised if character.isalnum())
        if unexpected in canonical:
            remaining_outdated.append(value)
    assert not remaining_outdated, f"Outdated experimental wording still present: {remaining_outdated}"
    assert "[?]" not in text, "Unresolved citation/reference marker found"

    print(f"PASS: {pdf_path}")
    print(f"Pages: {len(document)} (maximum 5, including title and references)")
    for number, content in enumerate(page_text, start=1):
        print(f"  page {number}: {len(content)} extracted characters")
    print("PASS: new title, three research questions, six authors/emails, and required sections found")
    print("PASS: implementation details, all prediction values, table/figure captions, and four references found")
    print("PASS: concise workshop reflection found; removed societal discussion absent")
    print("PASS: no unresolved '[?]' citation markers")
    print("PASS: all extracted text blocks lie within page boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
