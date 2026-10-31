"""Check source coverage, conversion provenance and deterministic RAG chunking."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter

from app.adapters.chunker import chunk_document
from app.adapters.loader import discover_lectures
from scripts.convert_course_material import ROOT, source_files


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Kontrollér kildekonvertering og RAG-materiale uden live services.")
    parser.add_argument("--verify-pdfs", action="store_true", help="Kontrollér også at PDF-tekstlaget er bevaret (kræver conversion-gruppen).")
    args = parser.parse_args(argv)
    source, output = ROOT / "source", ROOT / "llm_friendly"
    manifest = json.loads((output / "conversion-manifest.json").read_text(encoding="utf-8"))
    records = {record["source"]: record for record in manifest["files"]}
    actual = {path.relative_to(source).as_posix(): path for path in source_files(source)}
    errors: list[str] = []
    if set(records) != set(actual):
        errors.append(f"Manifest og kilder afviger: {sorted(set(records) ^ set(actual))}")
    for name, record in records.items():
        if name not in actual:
            continue
        if hashlib.sha256(actual[name].read_bytes()).hexdigest() != record["sha256"]:
            errors.append(f"Kilden er ændret siden konverteringen: {name}")
        if record["status"] not in {"converted", "duplicate", "described"}:
            errors.append(f"Kilden er ikke færdigbehandlet: {name} ({record['status']})")
        target = output / record.get("output", "missing.md")
        if not target.is_file():
            errors.append(f"Markdown mangler: {name}")
            continue
        text = target.read_text(encoding="utf-8")
        if "\ufffd" in text or "\x00" in text:
            errors.append(f"Ugyldige tegn i {target.name}")
        if args.verify_pdfs and actual[name].suffix.lower() == ".pdf":
            import pymupdf

            with pymupdf.open(actual[name]) as document:
                if len(re.findall(r"^## Side \d+$", text, re.MULTILINE)) != len(document):
                    errors.append(f"PDF-sider mangler: {name}")
                # Det oprindelige tekstlag skal være bevaret; OCR-sider kontrolleres visuelt.
                expected = Counter(re.findall(r"\w+", "\n".join(page.get_text() for page in document)))
                found = Counter(re.findall(r"\w+", text))
                missing = expected - found
                if missing:
                    errors.append(f"PDF-tekst mangler i {name}: {sum(missing.values())} tokens")
    documents = discover_lectures(ROOT, "llms_for_devs")
    identifiers = [document.doc_id for document in documents]
    if len(identifiers) != len(set(identifiers)):
        errors.append("Dokument-id'er er ikke entydige.")
    chunk_ids: list[str] = []
    counts: Counter[int] = Counter()
    for document in documents:
        chunks = chunk_document(document)
        if not chunks:
            errors.append(f"Ingen chunks for {document.doc_id}")
        if chunks != chunk_document(document):
            errors.append(f"Ikke-deterministisk chunking for {document.doc_id}")
        counts[document.lecture] += len(chunks)
        chunk_ids.extend(chunk.chunk_id for chunk in chunks)
    if len(set(chunk_ids)) != len(chunk_ids):
        errors.append("Chunk-id'er er ikke entydige.")
    for week in sorted(counts):
        print(f"Uge {week}: {sum(document.lecture == week for document in documents)} dokumenter, {counts[week]} chunks")
    print(f"\nKilder: {len(records)}; PDF-sider: {sum(record.get('pages', 0) for record in records.values())}")
    print(f"RAG: {len(documents)} dokumenter, {len(chunk_ids)} chunks")
    for error in errors:
        print(f"FEJL: {error}")
    print(f"\n{'FEJL' if errors else 'OK'}: {len(errors)} fejl.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
