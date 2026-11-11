# StudyGraph — Course Knowledge Base (RAG)

Implementation-facing companion to [../architecture/rag-pipeline.md](../architecture/rag-pipeline.md).
It records **how** the course material is prepared and indexed, with the exact commands.
Source conversion and the offline check were completed on 2026-10-31. See the
[material overview](llm_for_developers/llm_friendly/README.md) for the individual weeks,
source coverage and known limitations.

## 1. Source material

```text
docs/RAG/llm_for_developers/
├── source/week1/…                 # originals: PDFs, notebooks, csv, txt, png (git-ignored)
└── llm_friendly/
    ├── week1/week1_complete_rag.md
    ├── week2/week2_prompt_engineering_rag.md
    └── week3/week3_overview.md, week3_ambiguity_semantic_drift.md,
        week3_gradient_descent_and_embeddings.md, week3_hallucinations.md,
        week3_prompt_injection_security.md,
        week3_literature_review_assignment_and_resources.md
```

- One directory per lecture, one or more Markdown documents inside it:
  `docs/RAG/llm_for_developers/llm_friendly/week<N>/*.md` (ADR-020).
- The Markdown is the authoritative RAG input and is **committed**, so the index can be
  rebuilt without the original slides. Large sources (`source/**`, `*.pdf`, `*.png`) are
  git-ignored and never indexed.
- The course files are **not modified**: metadata is derived from the path and the document
  header — `doc_id` = the file stem (`week3_hallucinations`), `lecture` = `<N>` from the
  directory, `doc_name` = the first `#` heading.
- The material now covers **weeks 1, 2, 3, 4, 6, 8, 9 and 10**: **85 documents and 1,660 chunks**.
  73 relevant sources are covered by the manifest, including 15 PDFs with 346 pages.
  Weeks 5 and 7 are not in the raw material. Hand-written notes and source conversions are
  separated by their file names; the new week overviews give a topic-by-topic entry point.
- Sections use `## N. …` / `### …` headings, prose and bullet lists, which suits
  heading-first chunking.

- **Slides or pages that could not be converted faithfully stay out of the index** rather
  than being invented. If page numbers are unavailable, the `page` metadata field is
  omitted — never fabricated ([rag-pipeline.md](../architecture/rag-pipeline.md) §3).

## 2. Source conversion (ADR-023)

`scripts/convert_course_material.py` converts all available weeks locally.
PyMuPDF 1.28.2 preserves the PDF text layer page by page and OCR-reads image-based pages
with Danish/English Tesseract language data. Notebooks are converted cell by cell without
execution or stored outputs. Code and data are preserved; Draw.io becomes labels and edges.
The animations have visual descriptions and verified metadata from FFmpeg.

```powershell
uv sync --group conversion
uv run --group conversion python .\scripts\convert_course_material.py --ocr
uv run --group conversion python .\scripts\check_course_material.py --verify-pdfs
```

The original week 1-3 notes are preserved. The manifest records the source hash, the output
and any OCR notes. `.env`, environments and caches are skipped. Graphical detail, OCR
characters and mathematical layout still need critical reading; they are not verified
automatically. The generated scaffolding and the media descriptions are in English
(2026-11-09), so the indexed corpus is monolingual apart from the two deliberate
language-sample corpora in `week3`.

## 3. Chunking

Strategy (to be validated against the real slides in SG-022):

- Split on Markdown headings first, so a heading stays with its content
  ([rag-pipeline.md](../architecture/rag-pipeline.md) §3).
- Then split long sections into chunks of **900 characters with 120 overlap** (ADR-015),
  and never split inside a fenced code block or a table.
- Drop chunks under **80** characters unless they clearly carry meaning (e.g. a short definition).

Implemented in `app/adapters/chunker.py` (`CHUNKER_VERSION = "2"`, ADR-023).
Checked against the current material: **85 documents → 1,660 chunks** (measured 2026-11-09).
Code comments and headings inside code fences do not create new Markdown sections.
Larger source files are therefore split into complete code blocks with line numbers before chunking.
- Every chunk inherits `course_id`, `doc_id`, `doc_name`, `lecture`, `page` (when known)
  plus `chunk_index` and `text_hash`.

Rationale for slides: they are short and fragmented, so heading-first splitting preserves
the topic, and the overlap carries context across slide boundaries.

## 4. Metadata schema (per chunk)

| Field | Type | Notes |
|---|---|---|
| `course_id` | str | `llms_for_devs` |
| `doc_id` | str | from front matter, e.g. `lecture-03-rag` |
| `doc_name` | str | human-readable, used for citations |
| `lecture` | int | from front matter, omitted if unknown |
| `page` | int | slide/page number, omitted if unknown |
| `chunk_index` | int | position within the document |
| `text_hash` | str | sha1 of the normalised chunk text |
| `index_version` | str | `v1`, bumped when the chunker changes |

Chunk **id** is deterministic: `f"{doc_id}:{chunk_index:04d}:{text_hash[:12]}"`, e.g.
`week3_prompt_injection_security:0007:1a2b3c4d5e6f`. This makes re-indexing idempotent — the
same content always lands on the same id (ADR-015). Chroma stores no `chunk_id` metadata field
because the record id *is* the chunk id.

## 5. Collection, embeddings and versioning

- Collection: **`llms_for_devs_v1`** (ADR-009).
- Collection metadata: `course_id`, `embedding_model`, `embedding_dim`, `chunker_version`,
  `corpus_digest` (written by `ingest.py`, ADR-025).
- Embeddings come from `app/adapters/embedder.py` (Ollama, ADR-004) and are passed to Chroma
  explicitly; Chroma's default embedding function is not used.
- Startup validation compares configured `embedding_model`/dimension and `chunker_version`
  with the collection metadata. Mismatch → refuse to query and tell the user to re-index
  (never mix dimensions).
- `corpus_digest` is a 16-character SHA-1 over the sorted chunk ids, so it changes whenever
  the material or the chunking changes (e.g. the 2026-11-09 translation). It is only compared
  where the corpus is read (`ingest.py`, `doctor.py`), not on every query, because computing
  it means re-chunking the corpus. `doctor.py` reports a stale index instead of letting the
  app answer from material that no longer exists.
- Changing the embedding model is a configuration change plus a re-index; the model and its
  dimension must be changed together (`STUDYGRAPH_EMBED_MODEL`, `STUDYGRAPH_EMBEDDING_DIM`,
  `uv run python .\scripts\ingest.py --recreate`, see the README).

## 6. Retrieval

| Parameter | v1 default | Notes |
|---|---|---|
| `top_k` | 4 | config, not hardcoded |
| Distance metric | Chroma default for the collection (`l2`/`cosine` per collection config) | recorded in the collection metadata |
| Relevance threshold | none initially; evaluate on top-1 distance before introducing one | a threshold that silently drops everything is worse than showing an empty result |
| Query text | current user message | follow-up questions may need history-aware rewriting; decide after Phase 7 |
| Metadata filter | `course_id` only | keeps collections reusable if more courses appear |

The retriever returns a status alongside the chunks — `ok`, `empty`, `failed` — and never
collapses "nothing relevant" into "no retrieval happened".

## 7. Verification (run after every re-index)

```powershell
uv run python .\scripts\ingest.py --recreate
uv run python .\scripts\check_retrieval.py          # rewrites retrieval-check.json
uv run python .\scripts\doctor.py                   # every check OK, including freshness
uv run python .\scripts\search.py "What is prompt injection and how can it be defended against?" --top-k 3
```

Historical check (2026-10-30 against `llms_for_devs_v1`, weeks 1–3, chunker version 1):

- [x] Chunk count is reported and stable across two runs — **153** both times (idempotent).
- [x] A fresh collection built from a clean run (`STUDYGRAPH_COLLECTION=repro_check_v1`)
      also produced 153 chunks, so the index is reproducible from the repository alone.
- [x] Spot-check: chunk text reads correctly and metadata points at the right document
      (e.g. `week3_prompt_injection_security` → section `1. What is prompt injection?`).
- [x] Sample queries return the expected sections:
      `"What is prompt injection and how can it be defended against?"` → prompt injection 0.417,
      direct injection 0.483, defensive design 0.494; `"How does gradient descent reduce loss?"`
      → gradient descent 0.334, week-3 overview 0.385; `"What is overfitting…?"` → Overfitting 0.42.
- [ ] An off-topic query must return low-relevance results so that `empty` handling can be
      exercised — still to record (belongs to the Phase 7 question set).

Current index, rebuilt **2026-11-10** from the translated English corpus:
`uv run python .\scripts\ingest.py --recreate` upserted **1,660 chunks** into
`llms_for_devs_v1` (chunker version 2, `nomic-embed-text`, 768 dimensions,
`corpus_digest 62313c4629307e08`). Embedding all 1,660 chunks took **14.0 s** on this machine;
the 2026-10-31 run on CPU took 569.1 s for 1,659 chunks. `doctor.py` reports
`Course index llms_for_devs_v1: 1660 chunks` and `Index freshness index matches the 1660
chunks on disk`.

The retrieval checks were re-run against that index (`scripts/check_retrieval.py`,
`retrieval-check.json`, 2026-11-10, top 6): all five week checks (weeks 4, 6, 8, 9, 10) find
their own week, and both probes pass — the broad gradient-descent query ranks week 9 first and
still reaches week 3 within the top six, and the English CNN query that previously missed the
Danish video notes now returns week 9 in its first four hits. Distances are recorded exactly as
retrieved; nothing was filtered or tuned to make a check pass.

Before this rebuild the server held the 2026-10-31 index (chunker version 1, 153 chunks), so
the chunker-version check made every grounded answer fail with a re-index hint. That is the
failure mode the metadata validation exists for; it now also covers the corpus itself.

## 8. Open items

- Visual quality check of complex PDF tables and formulas (the tool is chosen in ADR-023).
- Exact chunk size/overlap and `top_k` (to be measured, then recorded in the decision log).
- Whether lecture PDFs contain tables/code that need special handling.
- Whether a relevance threshold is meaningful for this corpus.
