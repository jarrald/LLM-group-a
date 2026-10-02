---
paths:
  - "docs/**"
  - "**/*.md"
---

# Documentation rules

- **Keep `README.md` in Danish** (existing convention). Setup/run examples use
  PowerShell code blocks.
- Every runnable command in docs must be copy-paste correct for **Windows 11 +
  PowerShell** and must match the current code (flags, env vars, ports).
- Prefer editing the **Markdown** sources (`docs/Mandatory 1.md`, `plan.md`, this file).
  Do **not** edit or regenerate the PDFs/PPTX in `docs/` or `synopsis_report/`.
- When you change behaviour (flags, env vars, API routes), update `README.md` **and**
  `AGENTS.md` so both stay accurate.
- Keep headings sentence case, use fenced code blocks with a language tag, and keep
  paragraphs short.
