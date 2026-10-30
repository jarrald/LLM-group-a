# StudyGraph — RAG vs. Non-RAG Evaluation

Template and protocol for the applied comparison required by the assignment
("be able to demonstrate how retrieval affects an answer") and described in
[../design/rag-comparison.md](../design/rag-comparison.md).

**Status:** not run yet. Fill every `TBD` from an actual run; never estimate a value.

## 1. Fixed configuration (must be identical in both arms)

| Setting | Value |
|---|---|
| Chat model | TBD (ADR-007) |
| Embedding model | TBD (ADR-007b) |
| Collection | `llms_for_devs_v1` |
| `prompt_version` | `system_v1` |
| Target / Tone / Traits | Beginner / Friendly and encouraging / Patient, explanatory |
| Task | Explain a concept |
| `temperature`, `num_ctx` | TBD from config |
| `top_k` | 4 |
| History | none (fresh conversation per question, single turn) |

The **only** intended difference: Buddy `A` has course = *LLMs for Developers*, Buddy `B`
has no course. Names are for identification only and are not injected into the prompt.

Command used (once the app exists):

```powershell
uv run python .\scripts\run_evaluation.py --questions .\docs\evaluation\questions.csv
```

## 2. Question set

| ID | Question | Expected to be covered by the slides? | Note |
|---|---|---|---|
| Q1 | TBD | yes | a definition question |
| Q2 | TBD | yes | an "explain the mechanism" question |
| Q3 | TBD | yes | a terminology question specific to the course |
| Q4 | TBD | yes | a question whose answer spans two lectures |
| Q5 | TBD | yes | a "how does X differ from Y" question |
| Q6 | TBD | yes | a practical/example question |
| Q7 | TBD | **no** | outside the course material — tests honest uncertainty |
| Q8 | TBD | **no** | plausible but not in the slides — tests hallucination control |

## 3. Results

| ID | Mode | Answer (verbatim, trimmed) | Retrieved sources | Factual correctness (1–5) | Course alignment (1–5) | Relevance (1–5) | Grounding (1–5) | Uncertainty handling | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | RAG | TBD | TBD | TBD | TBD | TBD | TBD | TBD | |
| Q1 | non-RAG | TBD | — (skipped) | TBD | TBD | TBD | — | TBD | |
| Q2 | RAG | TBD | TBD | TBD | TBD | TBD | TBD | TBD | |
| Q2 | non-RAG | TBD | — (skipped) | TBD | TBD | TBD | — | TBD | |
| … | | | | | | | | | |
| Q7 | RAG | TBD | TBD (expected low relevance) | TBD | TBD | TBD | TBD | TBD | must not claim course support |
| Q7 | non-RAG | TBD | — | TBD | TBD | TBD | — | TBD | |

Rating scale: 1 = clearly wrong/unsupported … 5 = fully correct and fully supported.

Summary per mode (fill after rating):

| Mode | Mean factual | Mean course alignment | Mean relevance | Mean grounding | Answers presented as grounded when not |
|---|---|---|---|---|---|
| RAG | TBD | TBD | TBD | TBD | TBD |
| non-RAG | TBD | TBD | TBD | n/a | TBD |

## 4. Observations (2–3 concrete examples)

For each observation, record the question, what retrieval returned, and how the two answers
differed. Example structure:

> **Q3 (RAG vs non-RAG).** Retrieval returned `lecture-0X:…` and `lecture-0Y:…`. The RAG
> answer used the course's own term "<term>"; the non-RAG answer used the generic term
> "<term>" and TBD. Neither answer was wrong, but only the RAG answer aligned with the
> slides.

## 5. Limitations to state in the synopsis

- Small, hand-written question set and subjective ratings.
- One model, one configuration, one corpus; results are not generalisable.
- LLM output is non-deterministic even with fixed parameters.
- Retrieval quality is bounded by PDF→Markdown conversion and chunking.
- The non-RAG arm may still know the material from pretraining, so a "good" non-RAG answer
  is not evidence against RAG.
