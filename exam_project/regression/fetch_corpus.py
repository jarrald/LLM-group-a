"""Download the scikit-learn source that ``regression/rag.py`` indexes.

    uv run python -m regression.fetch_corpus                 # download the main branch
    uv run python -m regression.fetch_corpus --ref 1.6.1    # a release tag instead
    uv run python -m regression.fetch_corpus --force         # replace an existing copy
    uv run python -m regression.fetch_corpus --check         # exit 1 if it is missing

The corpus is third-party source (~23 MB, 1 600+ files). It is git-ignored and therefore
**not** part of a clone of this repository, so it has to be downloaded once before the index
can be built or the chat/web interfaces can retrieve anything.

``RAG_CORPUS_ROOT`` (the variable ``rag.py`` already honours) overrides the destination.
After a download, ``<corpus>/.corpus.json`` records where the copy came from, which ref it
is, the commit GitHub reports for that ref and the ``scikit-learn.__version__`` it declares,
so a run can be traced back to its corpus. The index stores a fingerprint of the corpus it
was built from, so re-downloading (or updating) the corpus is detected instead of silently
mixing two versions of the source in one collection.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import sys
import tempfile
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REGRESSION = Path(__file__).resolve().parent

#: Destination, resolved exactly the way ``rag.py`` resolves its corpus root.
CORPUS = Path(os.getenv("RAG_CORPUS_ROOT", REGRESSION / "scikit-learn-main"))

REPOSITORY = "scikit-learn/scikit-learn"
GIT_URL = f"https://github.com/{REPOSITORY}.git"
ARCHIVE_URL = f"https://codeload.github.com/{REPOSITORY}/zip/{{ref}}"

#: Default ref. ``main`` is what the recorded runs used (their checkout reported
#: ``sklearn.__version__ == "1.10.dev0"``); pass ``--ref`` to pin a release tag instead.
DEFAULT_REF = os.getenv("RAG_CORPUS_REF", "main")

#: Files/directories the index patterns in ``rag.py`` need. Present => usable corpus.
MARKERS = (
    "sklearn/__init__.py",
    "sklearn/linear_model/_base.py",
    "sklearn/model_selection/_split.py",
    "sklearn/metrics/_regression.py",
    "doc/modules/linear_model.rst",
    "examples/linear_model",
)

PROVENANCE_FILE = ".corpus.json"


def provenance_path(corpus: Path = CORPUS) -> Path:
    """Where the provenance record for ``corpus`` lives."""
    return corpus / PROVENANCE_FILE


def corpus_ready(corpus: Path = CORPUS) -> bool:
    """True when every marker file the index needs exists under ``corpus``."""
    return corpus.is_dir() and not missing_markers(corpus)


def missing_markers(corpus: Path = CORPUS) -> list[str]:
    """The markers that are absent, so the user can see what is actually wrong."""
    return [marker for marker in MARKERS if not (corpus / marker).exists()]


def read_provenance(corpus: Path = CORPUS) -> dict[str, object]:
    """The recorded provenance, or an empty dict when the copy predates this script."""
    path = provenance_path(corpus)
    if not path.is_file():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _remove_tree(path: Path) -> None:
    """Remove a directory even when Windows marks files read-only (git objects do)."""
    if not path.exists():
        return

    def _retry(function: object, target: str, _error: object) -> None:
        os.chmod(target, stat.S_IWRITE)
        function(target)  # type: ignore[operator]

    shutil.rmtree(path, onexc=_retry)


def _download_archive(ref: str, destination: Path) -> None:
    """Fetch the repository zip for ``ref`` and unpack it into ``destination``."""
    url = ARCHIVE_URL.format(ref=ref)
    with tempfile.TemporaryDirectory(prefix="sklearn-corpus-") as temporary:
        archive = Path(temporary) / "corpus.zip"
        print(f"downloading {url}")
        try:
            urllib.request.urlretrieve(url, archive)
        except OSError as exc:
            raise RuntimeError(f"cannot download {url}: {exc}. Check the network or pass a ref that exists (--ref main).") from exc
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(Path(temporary) / "unpacked")
        root = next((item for item in (Path(temporary) / "unpacked").iterdir() if item.is_dir()), None)
        if root is None:
            raise RuntimeError(f"the archive downloaded from {url} was empty")
        shutil.copytree(root, destination)


def _commit_of(ref: str) -> str | None:
    """Ask the GitHub API which commit ``ref`` points at; ``None`` when that is not possible."""
    request = urllib.request.Request(f"https://api.github.com/repos/{REPOSITORY}/commits/{ref}", headers={"User-Agent": "studygraph-regression"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:  # noqa: S310 - fixed https URL
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, json.JSONDecodeError, KeyError):
        return None
    commit = payload.get("sha") if isinstance(payload, dict) else None
    return str(commit) if commit else None


def _version_of(corpus: Path) -> str:
    """``__version__`` as declared by the checkout, without importing it."""
    init = corpus / "sklearn" / "__init__.py"
    if not init.is_file():
        return "unknown"
    for line in init.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("__version__"):
            return line.split("=", 1)[-1].strip().strip('"').strip("'")
    return "unknown"


def fetch(ref: str = DEFAULT_REF, corpus: Path = CORPUS, force: bool = False) -> dict[str, object]:
    """Make sure ``corpus`` holds a usable scikit-learn checkout; return its provenance."""
    corpus = Path(corpus)
    if corpus_ready(corpus) and not force:
        record = read_provenance(corpus)
        print(f"corpus already present: {corpus} ({record.get('ref', 'unknown ref')}, {record.get('commit', 'unknown commit')})")
        print("pass --force to download it again")
        return record

    work = corpus.parent / f".{corpus.name}.download"
    _remove_tree(work)
    work.parent.mkdir(parents=True, exist_ok=True)

    _download_archive(ref, work)

    try:
        absent = [marker for marker in MARKERS if not (work / marker).exists()]
        if absent:
            raise RuntimeError(f"the checkout of '{ref}' has no {', '.join(absent)}; pass a scikit-learn ref that contains those paths")

        record: dict[str, object] = {
            "source": GIT_URL,
            "ref": ref,
            "commit": _commit_of(ref),
            "version": _version_of(work),
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "python_files": sum(1 for _ in work.rglob("*.py")),
        }
        (work / PROVENANCE_FILE).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
    except Exception:
        _remove_tree(work)  # never leave a half-usable corpus behind
        raise

    _remove_tree(corpus)
    shutil.move(str(work), str(corpus))
    print(f"corpus ready: {corpus}")
    print(f"              version {record['version']}, ref {record['ref']}, commit {record['commit'] or 'unknown'}")
    return record


def main(argv: list[str] | None = None) -> int:
    """CLI entry point; returns a process exit code."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    parser = argparse.ArgumentParser(description="Download the scikit-learn corpus used by regression/rag.py.")
    parser.add_argument("--ref", default=DEFAULT_REF, help=f"branch or tag to download (default {DEFAULT_REF})")
    parser.add_argument("--force", action="store_true", help="download again even if a usable corpus is present")
    parser.add_argument("--check", action="store_true", help="only report whether the corpus is usable")
    parser.add_argument("--corpus", type=Path, default=CORPUS, help=f"destination directory (default {CORPUS})")
    arguments = parser.parse_args(argv)

    if arguments.check:
        if corpus_ready(arguments.corpus):
            record = read_provenance(arguments.corpus)
            print(f"OK   {arguments.corpus} ({record.get('ref', 'unknown ref')}, {record.get('commit', 'unknown commit')})")
            return 0
        print(f"FAIL {arguments.corpus} is not usable; missing: {', '.join(missing_markers(arguments.corpus))}")
        print("     fix: uv run python -m regression.fetch_corpus")
        return 1

    try:
        fetch(ref=arguments.ref, corpus=arguments.corpus, force=arguments.force)
    except RuntimeError as exc:
        print(f"FAIL {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
