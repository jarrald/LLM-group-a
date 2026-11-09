# StudyGraph — Course Knowledge Base (RAG)

Implementation-facing companion to [../architecture/rag-pipeline.md](../architecture/rag-pipeline.md).
It records **how** the course material is prepared and indexed, with the exact commands.
Kildekonvertering og offline kontrol er gennemført 2026-10-31. Se
[materialeoversigten](llm_for_developers/llm_friendly/README.md) for de enkelte uger,
kildedækning og kendte begrænsninger.

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
- Materialet dækker nu **uge 1, 2, 3, 4, 6, 8, 9 og 10**: **85 dokumenter og 1.659 chunks**.
  73 relevante kilder er dækket af manifestet, herunder 15 PDF'er med 346 sider.
  Uge 5 og 7 findes ikke i råmaterialet. Håndskrevne noter og kildekonverteringer er
  adskilt gennem filnavnene; nye ugeoversigter giver en emneopdelt indgang.
- Sections use `## N. …` / `### …` headings, prose and bullet lists, which suits
  heading-first chunking.

- **Slides or pages that could not be converted faithfully stay out of the index** rather
  than being invented. If page numbers are unavailable, the `page` metadata field is
  omitted — never fabricated ([rag-pipeline.md](../architecture/rag-pipeline.md) §3).

## 2. Kildekonvertering (ADR-021)

`scripts/convert_course_material.py` konverterer alle tilgængelige uger lokalt.
PyMuPDF 1.28.2 bevarer PDF'ens tekstlag side for side og OCR-læser billedbaserede sider
med dansk/engelsk Tesseract-sprogdata. Notebooks konverteres celle for celle uden
kørsel eller gemte outputs. Kode og data bevares; Draw.io bliver labels og forbindelser.
Animationerne har visuelle beskrivelser og kontrollerede metadata fra FFmpeg.

```powershell
uv sync --group conversion
uv run --group conversion python .\scripts\convert_course_material.py --ocr
uv run --group conversion python .\scripts\check_course_material.py --verify-pdfs
```

De oprindelige uge 1–3-noter er bevaret. Manifestet registrerer kildehash, output og
OCR-bemærkninger. `.env`, miljøer og caches springes over. Grafiske detaljer, OCR-tegn
og matematiske layout kræver fortsat kritisk læsning; de er ikke automatisk verificeret.

## 3. Chunking

Strategy (to be validated against the real slides in SG-022):

- Split on Markdown headings first, so a heading stays with its content
  ([rag-pipeline.md](../architecture/rag-pipeline.md) §3).
- Then split long sections into chunks of **900 characters with 120 overlap** (ADR-015),
  and never split inside a fenced code block or a table.
- Drop chunks under **80** characters unless they clearly carry meaning (e.g. a short definition).

Implemented in `app/adapters/chunker.py` (`CHUNKER_VERSION = "2"`, ADR-021).
Kontrolleret på det aktuelle materiale: **85 dokumenter → 1.659 chunks**.
Kodekommentarer og overskrifter inde i code fences opretter ikke nye Markdown-afsnit.
Større kildefiler opdeles derfor i komplette kodeblokke med linjenumre før chunking.
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
  `index_version`, `created_at`.
- Embeddings come from `app/adapters/embedder.py` (Ollama, ADR-004) and are passed to Chroma
  explicitly; Chroma's default embedding function is not used.
- Startup validation compares configured `embedding_model`/dimension with the collection
  metadata. Mismatch → refuse to query and tell the user to re-index (never mix dimensions).

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
uv run python .\scripts\ingest.py
chroma browse llms_for_devs_v1 --local
```

Historisk kontrol (2026-10-30 mod `llms_for_devs_v1`, uge 1–3, chunker-version 1):

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

Aktuel indeksering 2026-10-31: `uv run python .\scripts\ingest.py --recreate` gennemført.
**1.659 vektorer upsertet, collection count = 1.659**, chunker-version 2, embeddings med
`nomic-embed-text` (768 dimensioner). Embedding på CPU tog 569,1 sekunder.

## 8. Open items

- Visuel kvalitetskontrol af komplekse PDF-tabeller og formler (værktøjet er valgt i ADR-021).
- Exact chunk size/overlap and `top_k` (to be measured, then recorded in the decision log).
- Whether lecture PDFs contain tables/code that need special handling.
- Whether a relevance threshold is meaningful for this corpus.
