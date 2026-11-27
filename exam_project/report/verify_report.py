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

    assert len(document) <= 5, f"Synopsis has {len(document)} pages; maximum is 5"
    required_text = [
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
        "Linear regression versus local LLM + RAG",
        "Reflection, limitations, and future work",
        "Conclusion",
        "References",
        "13.28",
        "107.15",
        "368.82",
        "20.3146",
        "0/6",
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
    assert "[?]" not in text, "Unresolved citation/reference marker found"

    print(f"PASS: {pdf_path}")
    print(f"Pages: {len(document)} (maximum 5, including title and references)")
    for number, content in enumerate(page_text, start=1):
        print(f"  page {number}: {len(content)} extracted characters")
    print("PASS: six authors/emails, required sections, results, and four references found")
    print("PASS: no unresolved '[?]' citation markers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
