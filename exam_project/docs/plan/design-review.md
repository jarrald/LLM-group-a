# StudyGraph — UI Design Review

Review of the draw.io mocks in [`../../Designs/`](../../Designs/) against the written design,
requirements and architecture. Reviewed 2026-10-30.

Source files: `ChatPage.drawio`, `StudyBuddies.drawio`, `StudySessions.drawio`,
`MyProgress.drawio` — each contains the same five pages (`conceptual diagram`,
`01 - My Study Buddy`, `02 - My Study Sessions`, `03 - My Progress and Test Cards`,
`Side-5`). Exported PNGs cover Dashboard, Chat, Study Buddies, Study Sessions and
Progress / Test Cards.

Screens present in the mocks: **Dashboard**, **Chat**, **My Study Buddies**,
**My Study Sessions**, **My Progress & Test Cards**, **Settings**.

## 1. Summary

The mocks are a coherent, attractive product — but they describe a *broader* product than
the MVP in `docs/`, and they **drop the one feature the assignment grades hardest: the
optional course association that drives RAG**. Two findings block UI work; the rest are
wording, scope and visual consistency.

| Severity | Count | IDs |
|---|---|---|
| Blocker | 2 | D-01, D-02 |
| High | 2 | D-03, D-04 |
| Medium | 4 | D-05 … D-08 |
| Low | 4 | D-09 … D-12 |

Nothing in the mocks was modified; this document only records gaps and proposes resolutions.

## 2. Findings

### D-01 — Blocker: the mocks store **Task** on the Buddy

**Evidence:** the four "4 Ts" cards are *Traits, Area of expertise (Tasks), Tones, Targets*,
and the Buddy Preview "ACTIVE CONFIGURATION" reads `Traits: Friendly, Patient /
Tasks: Explain, Quiz / Tone: Casual / Target: Exam preparation`. The customisation step is
"2. CUSTOMIZE ALEX … TASKS — What it does".

**Conflicts with:** [buddy-design.md](../design/buddy-design.md) §3.1 ("Task belongs to the
current interaction rather than the reusable Buddy configuration"), §8 ("Allow different
Tasks without requiring new Buddies"), [requirements.md](../requirements/requirements.md)
FR-09 / §2.5, and [data-model.md](../architecture/data-model.md) (Buddy has no Task field).

**Why it matters:** Task is one of the four graded dimensions. If it is baked into the
Buddy, the same Buddy can no longer explain *and* quiz, and the exam demo "one Buddy, two
Tasks, visibly different prompts" disappears.

**Recommendation:** keep Task off the Buddy (as documented). The Buddy form keeps
Traits / Tone / Target (+ course); Task stays a per-message selector or free text. If the
team prefers the mock, amend FR-09 and the data model — as a deliberate ADR, not drift.

### D-02 — Blocker: the course association is missing everywhere

**Evidence:** no screen contains a course selector, a "No course" option, a grounding badge,
or any indication whether an answer is course-grounded.

**Conflicts with:** [design.md](../design/design.md) §5.3 "Explicit course grounding",
FR-05 (course dropdown with `No course` default), [user-experience.md](../design/user-experience.md)
§2.2 / §3.2, and the whole [rag-comparison.md](../design/rag-comparison.md) workflow.

**Why it matters:** without a visible course toggle there is no RAG vs non-RAG demo, which is
a mandatory exam criterion (M2 in [implementation-plan.md](../plan/implementation-plan.md) §4).

**Recommendation:** add (a) a "Course grounding" group to the Buddy form with
`No course` (default) / `LLMs for Developers`, and (b) a read-only mode badge in the chat
header, e.g. `Course-grounded` vs `General`.

### D-03 — High: three screens are outside V1 scope

**Evidence:** **Dashboard** (duplicates buddy creation), **My Progress & Test Cards**
(TOTAL QUESTIONS 128, CORRECT ANSWERS 94, ACCURACY 73 %, weekly accuracy chart,
PERFORMANCE BY SUBJECT, a test-card runner with submitted answers), **Settings** (no defined
content).

**Conflicts with:** [design.md](../design/design.md) §6 (V1 workflow) and §8 (progress
tracking is a *future opportunity*), [user-experience.md](../design/user-experience.md) §7
(V1 UX boundaries), and the [implementation-plan.md](../plan/implementation-plan.md) §5
non-goals. There is also no quiz-attempt or progress entity in the data model.

**Recommendation:** keep Dashboard / Progress / Settings as post-MVP; build Chat, Buddies and
Sessions first. A quiz remains possible as a *Task* inside chat, which costs almost nothing.

### D-04 — High: the chat screen shows no retrieval evidence

**Evidence:** the conversation area is the literal placeholder `<Conversation>`; the only
controls are a text input and **Send**. No sources, no grounding indicator, no
"nothing relevant was found" state, no example prompts for an empty conversation.

**Conflicts with:** [user-experience.md](../design/user-experience.md) §3.1 (source
references in chat) and §4 (empty / loading / retrieval-empty states),
[rag-pipeline.md](../architecture/rag-pipeline.md) §8 (source references).

**Recommendation:** design the message bubble with a sources row (`Sources (3)` expander) and
a distinct state for "retrieved, but nothing relevant".

### D-05 — Medium: a Buddy selector inside an active conversation

**Evidence:** the chat header has `Select buddy ▾`.

**Conflicts with:** FR-08 and ADR-010 — a conversation stores an immutable Buddy snapshot;
switching mid-conversation would silently change its behaviour (NFR-09).

**Recommendation:** the selector applies to *new* conversations only; in an existing
conversation show the Buddy read-only, or make "switch" create a new conversation.

### D-06 — Medium: the second dimension has two different names across the mock files

**Evidence:** `ChatPage.drawio` and `StudyBuddies.drawio` say **"Area of expertise"**;
`MyProgress.drawio` and `StudySessions.drawio` say **"TASKS"** for the same card. Within a
single screen, the tab reads "AREA OF EXPERTISE" while the preview lists "Tasks: …".

**Recommendation:** pick one label ("Task"), then re-export all files from one source page so
the copies cannot drift again.

### D-07 — Medium: the mocks assume multiple subjects, the product supports one course

**Evidence:** `Subject: All subjects`, `All subjects ▾` filters, `PERFORMANCE BY SUBJECT`
with Biology / Mathematics / History, sessions tagged `Alex • Biology`.

**Conflicts with:** [requirements.md](../requirements/requirements.md) §2.2 and FR-05 — one
predefined course (*LLMs for Developers*) in V1; creating courses is out of scope.

**Recommendation:** replace "Subject" with "Course" and use course-appropriate sample
content, so the mock doubles as demo preparation.

### D-08 — Medium: Buddy fields that do not exist in the data model

**Evidence:** `Avatar`, `Subject`, `Difficulty: Adaptive`, `Response length: Balanced`
("3. ADDITIONAL CUSTOMIZATION").

**Conflicts with:** [data-model.md](../architecture/data-model.md) §2.1 (ID, Name, Target,
Tone, Traits, Course ID, timestamps). "Difficulty: Adaptive" and "Response length" would also
become new prompt dimensions that nobody has designed or tested.

**Recommendation:** drop them for V1, or add them to the data model, the snapshot and the
prompt builder as an explicit ADR (cheap: two extra template variables).

### D-09 — Low: product naming

**Evidence:** all mocks say **STUDY BUDDY** / **STUDY BUDDY WORKSPACE**; the README, docs and
course material call the product **StudyGraph**.

**Recommendation:** pick one before more screenshots are produced — the synopsis will quote
the mock, so the name must match.

### D-10 — Low: inconsistent navigation label

**Evidence:** the chat/dashboard mock's sidebar says `My AI Buddy`; the other three say
`My Study Buddy`.

**Recommendation:** one label, e.g. `My Buddies`.

### D-11 — Low: two visual themes and weak contrast

**Evidence:** the Dashboard + Chat mock is dark; the other three screens are light pastel. The
light theme puts pastel text on pastel cards (e.g. "TASKS / What it does", the stat labels),
which is below the contrast goal in [user-experience.md](../design/user-experience.md) §6.

**Recommendation:** choose the dark theme (it matches the chat screen and Streamlit's dark
mode) and darken the text tokens before writing CSS.

### D-12 — Low: predefined Buddies as the primary entry point

**Evidence:** the mocks lead with three ready Buddies (ALEX, PROFESSOR, EXAM COACH);
`buddy-design.md` §2 says templates "do not need to be implemented as predefined templates in
V1" and names different personas (Patient Tutor, Exam Coach, Socratic Mentor).

**Recommendation:** seed two or three Buddies on first run — it makes the first-time journey
in UX §2.1 work without configuration and costs one seed module. Rename them to match the
docs, or update the docs.

## 3. What the mocks get right (keep)

- **Sessions page** wording "Each conversation remains associated with the buddy that created
  it" matches the snapshot concept (FR-08) exactly.
- The **local storage note** matches the local-first requirement (NFR-05).
- The **Buddy preview card** with an "ACTIVE CONFIGURATION" summary is a good way to make the
  4T's visible — reuse it, with Task removed from the card (D-01).
- Search/filter controls on Sessions are a natural P2 extension of FR-02.

## 4. Decisions needed before UI work

| # | Decision | Options | Blocks |
|---|---|---|---|
| 1 | Where does Task live? | (a) per message only *(docs)* · (b) default Task on the Buddy + per-message override | D-01, prompt builder, data model |
| 2 | Course selector + grounding badge | (a) add to Buddy form and chat header *(recommended)* · (b) another mechanism | D-02, the RAG demo |
| 3 | V1 screen set | (a) Chat + Buddies + Sessions *(recommended)* · (b) include Dashboard / Progress / Settings | D-03, Phase 6 |
| 4 | Extra Buddy fields | (a) drop Avatar / Subject / Difficulty / Response length · (b) add to model and prompts | D-08 |
| 5 | Product name + theme | StudyGraph or Study Buddy; dark or light | D-09, D-11 |

Until decisions 1–3 are made, only build what is independent of the screen set: environment,
config, domain model, prompt builder, retrieval and the LangGraph flow (Phases 0–5). Phase 6
(UI) starts afterwards.

## 5. Suggested V1 screen set (if decision 3a is taken)

```text
StudyGraph
├── Chat       conversation list + chat + mode badge + sources expander
├── Buddies    list, create, edit (Traits / Tone / Target / Course grounding)
└── About      what it does, which model, how RAG works, where data is stored
```

Dashboard, Progress / Test Cards and Settings move to the "future opportunities" list in
[design.md](../design/design.md) §8 and stay out of the P0/P1 backlog.

## 7. Resolution log

| Date | Finding | Resolution |
|---|---|---|
| 2026-10-30 | **D-01** Task on the Buddy | **Resolved by decision (ADR-017):** a Buddy stores Traits/Tone/Target + course; Task is chosen per message in the chat. The mocks' four-card widget is superseded. |
| 2026-10-30 | **D-02** No course association in the UI | **Resolved by decision:** the Buddy form gets a "Course material" dropdown (`None` default, `LLMs for Developers`), and the chat header shows a read-only mode badge (`Course-grounded` / `General`) plus a sources expander. |
| 2026-10-30 | **D-03** Out-of-scope screens | **Resolved by decision (ADR-018):** three pages — Chat, Buddies, About. Dashboard, Progress/Test Cards and Settings stay in `design.md` §8 as future work. |
| 2026-10-30 | D-04 … D-06 | Addressed in the implementation: sources + status notice in chat (D-04), the Buddy selector only starts *new* conversations (D-05), one label "Task" (D-06). |

Still open, but **not blocking** the app (they only matter if the mocks are reused as
screenshots in the synopsis): D-07 subjects, D-08 extra Buddy fields, D-09 branding, D-10 nav
label, D-11 theme, D-12 predefined Buddies as the entry point.

### Checklist for whoever updates the drawio files

1. Replace the four "4 Ts" cards with three: **Traits**, **Tone**, **Target**; add a
   **Course material** dropdown card (`None` / `LLMs for Developers`).
2. Remove `Tasks:` from the Buddy preview "ACTIVE CONFIGURATION" block.
3. Add a Task selector to the chat screen, above the input, and a mode badge in its header.
4. Add a `Sources (n)` expander to assistant messages, and a "no relevant material found"
   state.
5. Change `Select buddy ▾` in the chat header to a read-only Buddy chip (the selector
   belongs to "new conversation").
6. Replace "Subject"/"All subjects" with "Course"; drop Avatar/Difficulty/Response length.
7. Pick one product name (StudyGraph) and one theme (dark), one nav label.
8. Delete the Dashboard, Progress/Test Cards and Settings frames, or move them to a clearly
   labelled "post-MVP" page.


- Findings are referenced from [status.md](status.md) §5 (blockers) and
  [risks.md](risks.md) (R-15, R-16).
- Each resolution becomes an ADR in [decision-log.md](decision-log.md) before code changes.


