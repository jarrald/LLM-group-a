"""Check source coverage, conversion provenance and deterministic RAG chunking."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

from app.adapters.chunker import chunk_document
from app.adapters.loader import discover_lectures
from scripts.convert_course_material import ROOT, file_digest, source_files


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Check source conversion and RAG material without live services.")
    parser.add_argument("--verify-pdfs", action="store_true", help="Also verify that the PDF text layer is preserved (requires the conversion group).")
    args = parser.parse_args(argv)
    source, output = ROOT / "source", ROOT / "llm_friendly"
    manifest = json.loads((output / "conversion-manifest.json").read_text(encoding="utf-8"))
    records = {record["source"]: record for record in manifest["files"]}
    actual = {path.relative_to(source).as_posix(): path for path in source_files(source)}
    errors: list[str] = []
    if set(records) != set(actual):
        errors.append(f"Manifest and sources differ: {sorted(set(records) ^ set(actual))}")
    for name, record in records.items():
        if name not in actual:
            continue
        if file_digest(actual[name]) != record["sha256"]:
            errors.append(f"The source changed after the conversion: {name}")
        if record["status"] not in {"converted", "duplicate", "described"}:
            errors.append(f"The source was not fully processed: {name} ({record['status']})")
        target = output / record.get("output", "missing.md")
        if not target.is_file():
            errors.append(f"Markdown is missing: {name}")
            continue
        text = target.read_text(encoding="utf-8")
        if "\ufffd" in text or "\x00" in text:
            errors.append(f"Invalid characters in {target.name}")
        if args.verify_pdfs and actual[name].suffix.lower() == ".pdf":
            import pymupdf

            with pymupdf.open(actual[name]) as document:
                if len(re.findall(r"^## Page \d+$", text, re.MULTILINE)) != len(document):
                    errors.append(f"PDF pages are missing: {name}")
                # The original text layer must be preserved; OCR pages are verified visually.
                expected = Counter(re.findall(r"\w+", "\n".join(page.get_text() for page in document)))
                found = Counter(re.findall(r"\w+", text))
                missing = expected - found
                if missing:
                    errors.append(f"PDF text is missing in {name}: {sum(missing.values())} tokens")
    documents = discover_lectures(ROOT, "llms_for_devs")
    identifiers = [document.doc_id for document in documents]
    if len(identifiers) != len(set(identifiers)):
        errors.append("Document ids are not unique.")
    chunk_ids: list[str] = []
    counts: Counter[int] = Counter()
    for document in documents:
        chunks = chunk_document(document)
        if not chunks:
            errors.append(f"No chunks for {document.doc_id}")
        if chunks != chunk_document(document):
            errors.append(f"Non-deterministic chunking for {document.doc_id}")
        counts[document.lecture] += len(chunks)
        chunk_ids.extend(chunk.chunk_id for chunk in chunks)
    if len(set(chunk_ids)) != len(chunk_ids):
        errors.append("Chunk ids are not unique.")
    for week in sorted(counts):
        print(f"Week {week}: {sum(document.lecture == week for document in documents)} documents, {counts[week]} chunks")
    print(f"\nSources: {len(records)}; PDF pages: {sum(record.get('pages', 0) for record in records.values())}")
    print(f"RAG: {len(documents)} documents, {len(chunk_ids)} chunks")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"\n{'ERROR' if errors else 'OK'}: {len(errors)} errors.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
