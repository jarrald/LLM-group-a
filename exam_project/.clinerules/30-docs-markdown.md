---
paths:
  - "docs/**"
  - "**/*.md"
---

# Documentation rules

- **Language:** English in this sub-project. Headings in sentence case, short paragraphs,
  fenced code blocks always tagged with a language, PowerShell for every runnable command.
- **Source of truth:** `docs/requirements/`, `docs/architecture/`, `docs/design/` describe
  the product. `docs/plan/` describes how it gets built. Do not duplicate content between
  them — state it once and link.
- **Read-only:** `docs/exam_project_requirements_llm_for_developers_joint_teaching_draft_v4.md`
  is the course-provided assignment. Never edit it; reference it.
- Every runnable command in docs must be copy-paste correct for **Windows 11 + PowerShell**
  and must match the current code (flags, env vars, ports, file paths).

## Keeping the tracking docs current

| File | Update when |
|---|---|
| `docs/plan/status.md` | at the end of every work session (what works, what is next, blockers) |
| `docs/plan/backlog.md` | a ticket changes state or scope |
| `docs/plan/decision-log.md` | any technical decision is taken, changed or rejected |
| `docs/plan/risks.md` | a risk appears, changes severity or is closed |
| `docs/plan/implementation-plan.md` | a phase is completed or re-scoped |
| `docs/architecture/tech-stack.md` | a library, model, port or storage choice changes |

- When a decision changes, update the decision log **and** the affected design/architecture
  document in the same change.
- Never write measured numbers (accuracy, latency, MAE, ratings) that were not actually
  produced by a run. Use `TBD` in templates, and record the command/config next to results.
- Do not edit or regenerate binary deliverables (PDF/PPTX).
- Do not invent page or slide references for course material; if the metadata does not
  exist, say it is unavailable.
