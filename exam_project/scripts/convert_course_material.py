"""Convert local course sources to traceable Markdown without executing source code."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import io
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zlib
from collections import Counter
from pathlib import Path
from typing import Any

from app.config import PROJECT_ROOT

ROOT = PROJECT_ROOT / "docs" / "RAG" / "llm_for_developers"
MARKER = "<!-- studygraph:converted-source:v1 -->"
SKIP_DIRS = {".venv", "venv", "__pycache__", ".git", "node_modules", ".pytest_cache", "runs"}
TEXT_TYPES = {".md", ".txt", ".py", ".js", ".html", ".css", ".csv"}
MEDIA_TYPES = {".mp4", ".png", ".jpg", ".jpeg"}
LANGUAGES = {".py": "python", ".js": "javascript", ".html": "html", ".css": "css", ".txt": "text"}


def source_files(root: Path) -> list[Path]:
    """Prune environments and private configuration before reading any file contents."""
    paths: list[Path] = []
    for directory, folders, files in os.walk(root):
        folders[:] = sorted(folder for folder in folders if folder.lower() not in SKIP_DIRS and not folder.startswith("."))
        for name in sorted(files):
            path = Path(directory) / name
            if name.startswith(".") or path.suffix.lower() in {".pyc", ".pyo", ".log"}:
                continue
            paths.append(path)
    return paths


def slug(text: str) -> str:
    normal = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", normal.lower()).strip("_")


def read_text(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            return data.decode(encoding).replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
        except UnicodeError:
            continue
    raise ValueError(f"Ukendt tegnkodning: {path.name}")


def fence(text: str, language: str) -> str:
    longest = max((len(match.group()) for match in re.finditer(r"`{3,}", text)), default=2)
    marks = "`" * max(3, longest + 1)
    return f"{marks}{language}\n{text.rstrip()}\n{marks}"


def code_sections(text: str, language: str) -> str:
    """Bound code passages without dropping lines or executing the example."""
    sections: list[str] = []
    lines = text.rstrip().splitlines()
    start = 0
    while start < len(lines):
        end = start
        size = 0
        while end < len(lines) and (size < 2000 or end == start) and end - start < 45:
            size += len(lines[end]) + 1
            end += 1
        sections.append(f"### Kildelinjer {start + 1}–{end}\n\n{fence(chr(10).join(lines[start:end]), language)}")
        start = end
    return "\n\n".join(sections)


def demote_headings(text: str) -> str:
    """Keep imported headings below the source title and ignore headings inside code."""
    lines: list[str] = []
    active = ""
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marks = match.group(1)
            if not active:
                active = marks
            elif marks[0] == active[0] and len(marks) >= len(active):
                active = ""
        if not active and re.match(r"^#{1,6}\s", line):
            line = re.sub(r"^(#{1,6})", lambda m: "#" * min(len(m.group()) + 2, 6), line)
        lines.append(line)
    return "\n".join(lines).strip()


def notebook_markdown(path: Path) -> str:
    notebook = json.loads(read_text(path))
    sections = ["Kildeceller er bevaret i rækkefølge. Koden er ikke kørt. Gemte outputs, billeder og kørselsnumre er udeladt; der tilføjes ingen forsøgsresultater."]
    language = notebook.get("metadata", {}).get("kernelspec", {}).get("language", "python")
    for number, cell in enumerate(notebook.get("cells", []), 1):
        content = cell.get("source", [])
        text = "".join(content) if isinstance(content, list) else content
        if not text.strip():
            continue
        body = code_sections(text, language) if cell.get("cell_type") == "code" else demote_headings(text)
        sections.append(f"## Celle {number} — {cell.get('cell_type', 'raw')}\n\n{body}")
    return "\n\n".join(sections)


def diagram_markdown(path: Path) -> str:
    root = ET.fromstring(read_text(path))
    pages = [root] if root.tag == "mxGraphModel" else list(root.findall("diagram"))
    sections: list[str] = []
    for page in pages:
        model = page if page.tag == "mxGraphModel" else page.find("mxGraphModel")
        if model is None and page.text:
            raw = zlib.decompress(base64.b64decode(page.text.strip()), -15).decode()
            model = ET.fromstring(urllib.parse.unquote(raw))
        if model is None:
            raise ValueError(f"Diagrammet kan ikke læses: {path.name}")
        cells = list(model.iter("mxCell"))
        labels = {cell.get("id"): html.unescape(re.sub(r"<[^>]+>", " ", cell.get("value", ""))).strip() for cell in cells}
        sections.append(f"## Diagram — {page.get('name', path.stem)}\n\nLabels og forbindelser fra diagrammets XML; placering og grafik er ikke gengivet.")
        for cell in cells:
            label = " ".join(labels[cell.get("id")].split())
            if cell.get("edge") == "1":
                source = labels.get(cell.get("source")) or cell.get("source", "ukendt")
                target = labels.get(cell.get("target")) or cell.get("target", "ukendt")
                sections.append(f"- Forbindelse: {source} → {target}. {label}")
            elif label:
                sections.append(f"- Element: {label}")
    return "\n\n".join(sections)


def ensure_tessdata() -> Path:
    """Cache official Tesseract language data outside the repository."""
    directory = Path(os.getenv("LOCALAPPDATA", str(Path.home() / ".cache"))) / "StudyGraph" / "tessdata"
    directory.mkdir(parents=True, exist_ok=True)
    for language in ("eng", "dan"):
        target = directory / f"{language}.traineddata"
        if not target.exists():
            url = f"https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/{language}.traineddata"
            with urllib.request.urlopen(url, timeout=60) as response:
                target.write_bytes(response.read())
    return directory


def pdf_markdown(path: Path, tessdata: Path | None) -> tuple[str, list[str], int]:
    import pymupdf

    sections: list[str] = []
    warnings: list[str] = []
    with pymupdf.open(path) as document:
        # Et eksisterende tekstlag bevares; OCR af diagrammer må ikke erstatte god tekst.
        ocr_pages: dict[int, str] = {}
        for index, page in enumerate(document):
            text = page.get_text().strip()
            if not text and (page.get_images() or page.get_drawings()):
                if tessdata is not None:
                    try:
                        textpage = page.get_textpage_ocr(language="eng+dan", dpi=200, full=True, tessdata=str(tessdata))
                        ocr_pages[index] = page.get_text(textpage=textpage).strip()
                    except Exception as exc:
                        warnings.append(f"Side {index + 1}: OCR mislykkedes ({type(exc).__name__}).")
                else:
                    warnings.append(f"Side {index + 1}: intet tekstlag; genkør med --ocr.")
        for index, page in enumerate(document):
            # PDF'ens blokorden bevarer typisk spalteordenen i artikler; ingen gættede tabeller.
            blocks = page.get_text("blocks")
            text = "\n\n".join(block[4].strip() for block in blocks if block[6] == 0 and block[4].strip())
            ocr = ocr_pages.get(index, "")
            if ocr:
                text = ocr
                warnings.append(f"Side {index + 1}: OCR anvendt; tekst kan indeholde genkendelsesfejl.")
            if not text:
                text = "Denne side indeholder ingen udtrækkelig tekst. Se originalens visuelle indhold."
                warnings.append(f"Side {index + 1}: ingen udtrækkelig tekst.")
            if page.get_images() or len(page.get_drawings()) > 5:
                text += "\n\n> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret."
            sections.append(f"## Side {index + 1}\n\n{demote_headings(text)}")
        return "\n\n".join(sections), warnings, len(document)


def text_markdown(path: Path) -> str:
    text = read_text(path)
    if path.suffix.lower() == ".csv":
        rows = list(csv.reader(io.StringIO(text)))
        if not rows:
            return "Tom datafil."

        def row(values: list[str]) -> str:
            return "| " + " | ".join(value.replace("|", "\\|").replace("\n", " ") for value in values) + " |"

        return "\n".join([row(rows[0]), row(["---"] * len(rows[0])), *(row(values) for values in rows[1:])])
    # Nogle uploadede .md-filer indeholder Python eller requirements i stedet for Markdown.
    is_python = bool(re.search(r"^(?:from \w.* import |import \w|def \w+\(|class \w+[:(])", text, re.MULTILINE))
    if path.suffix.lower() == ".md" and not is_python:
        return demote_headings(text)
    return code_sections(text, "python" if is_python else LANGUAGES.get(path.suffix.lower(), "text"))


def write_generated(path: Path, text: str) -> None:
    if path.exists() and not path.read_text(encoding="utf-8").startswith(MARKER):
        raise ValueError(f"Vil ikke overskrive håndskrevne noter: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8", newline="\n")


def video_metadata(path: Path) -> dict[str, object]:
    import imageio_ffmpeg

    result = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    duration = re.search(r"Duration: (\d+):(\d+):([\d.]+)", result.stderr)
    if duration is None:
        raise ValueError(f"Videoens varighed kunne ikke læses: {path.name}")
    return {"duration_seconds": int(duration[1]) * 3600 + int(duration[2]) * 60 + float(duration[3]), "audio": "Audio:" in result.stderr}


def convert(source: Path, output: Path, *, ocr: bool = False) -> dict[str, Any]:
    """Write per-source Markdown plus a complete, deterministic coverage manifest."""
    if not source.is_dir():
        raise ValueError(f"Kildemappen findes ikke: {source}")
    tessdata = ensure_tessdata() if ocr else None
    descriptions_path = output / "media-descriptions.json"
    descriptions = json.loads(descriptions_path.read_text(encoding="utf-8")) if descriptions_path.exists() else {}
    records: list[dict[str, Any]] = []
    seen: dict[tuple[str, str, str], str] = {}
    for path in source_files(source):
        relative = path.relative_to(source)
        if not re.fullmatch(r"week\d+", relative.parts[0], re.IGNORECASE):
            continue
        week = relative.parts[0].lower()
        suffix = path.suffix.lower()
        record: dict[str, Any] = {"source": relative.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "status": "converted", "warnings": []}
        key = (week, suffix, record["sha256"])
        if key in seen:
            record.update(status="duplicate", output=seen[key])
            records.append(record)
            continue
        try:
            if suffix == ".pdf":
                body, record["warnings"], record["pages"] = pdf_markdown(path, tessdata)
            elif suffix == ".ipynb":
                body = notebook_markdown(path)
            elif suffix == ".drawio":
                body = diagram_markdown(path)
            elif suffix in TEXT_TYPES or not suffix:
                body = text_markdown(path)
            elif suffix in MEDIA_TYPES:
                if suffix == ".mp4":
                    record["media"] = video_metadata(path)
                if relative.as_posix() not in descriptions:
                    record["status"] = "media_review"
                    record["warnings"] = ["Visuelt materiale mangler en beskrivelse i media-descriptions.json."]
                    records.append(record)
                    continue
                body = descriptions[relative.as_posix()]
                record["status"] = "described"
            else:
                record["status"] = "unsupported"
                records.append(record)
                continue
            name = f"{week}_source_{slug(relative.with_suffix('').relative_to(relative.parts[0]).as_posix())}_{suffix.lstrip('.') or 'text'}.md"
            target = output / week / name
            source_link = urllib.parse.quote(os.path.relpath(path, target.parent).replace("\\", "/"))
            title = f"Uge {int(week[4:])} — {path.stem} ({suffix.lstrip('.') or 'tekst'})"
            text = (
                f"{MARKER}\n# {title}\n\nKilde: [{relative.as_posix()}]({source_link}).\n\n"
                "Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. "
                f"Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.\n\n{body}\n"
            )
            write_generated(target, text)
            record["output"] = target.relative_to(output).as_posix()
            record["characters"] = len(text)
            seen[key] = record["output"]
        except Exception as exc:
            record.update(status="error", warnings=[f"{type(exc).__name__}: {exc}"])
        records.append(record)
        print(f"[{record['status']}] {relative.as_posix()}", flush=True)
    manifest = {"converter_version": "1", "ocr": ocr, "files": records}
    output.mkdir(parents=True, exist_ok=True)
    (output / "conversion-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Konvertér råt kursusmateriale til læsbar Markdown.")
    parser.add_argument("--source", type=Path, default=ROOT / "source")
    parser.add_argument("--output", type=Path, default=ROOT / "llm_friendly")
    parser.add_argument("--ocr", action="store_true", help="Hent dansk/engelsk OCR-sprogdata og læs billedbaserede PDF-sider.")
    arguments = parser.parse_args(argv)
    source, output = arguments.source.resolve(), arguments.output.resolve()
    if source == output or source in output.parents or output in source.parents:
        parser.error("Kilde- og outputmapper skal være adskilt.")
    manifest = convert(source, output, ocr=arguments.ocr)
    counts = Counter(record["status"] for record in manifest["files"])
    print("\nResultat: " + ", ".join(f"{status}={count}" for status, count in sorted(counts.items())))
    return 1 if counts["error"] or counts["unsupported"] or counts["media_review"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
