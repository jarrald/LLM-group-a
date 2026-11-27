# StudyGraph exam synopsis

The LaTeX source for the final synopsis is in this directory. The compiled document is
`build/main.pdf`. The five-page limit includes the compact title page and bibliography.

## Structure

- `main.tex` — document setup, title page, abstract, introduction, and research questions.
- `sections/` — theory, StudyGraph implementation, experiments, discussion, and conclusion.
- `references.bib` — verified academic references.
- `build.ps1` — PowerShell build script.

## Build

With [Tectonic](https://tectonic-typesetting.org/) on `PATH`, run from `exam_project/`:

```powershell
.\report\build.ps1
```

The script also uses the local portable compiler at `report/.tools/tectonic/tectonic.exe` when
that optional build tool is present. Tectonic resolves BibTeX and reruns automatically.

When the project's optional conversion dependencies are installed, the PDF checks can be run with:

```powershell
uv run --group conversion python .\report\verify_report.py
```

The check fails above five pages and verifies author emails, required sections, result values,
bibliography entries, and unresolved citation markers.

## Evidence boundary

The numerical prediction table is explicitly labelled as archived exploratory evidence from
9 November 2026. The controlled 19 November experiment evaluates code execution, not numerical
prediction; its MAE is unavailable because all six generated programs failed. These result sets
are intentionally not combined. No application source or experimental data is changed by the
report build.
