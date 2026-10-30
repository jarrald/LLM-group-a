# StudyGraph — Course Knowledge Base (RAG)

Implementation-facing companion to [../architecture/rag-pipeline.md](../architecture/rag-pipeline.md).
It records **how** the course material is prepared and indexed, with the exact commands.
Everything here is planned; nothing has been executed yet (see
[../plan/status.md](../plan/status.md)).

## 1. Source material

```text
data/course_material/llms-for-developers/
├── pdf/          # original lecture slides, git-ignored, not redistributed
└── markdown/     # converted Markdown, committed (reproducible RAG source)
```

- One Markdown file per source PDF, same base file name.
- The Markdown is the authoritative RAG input. It is committed so anyone can rebuild the
  index without the original slides.
- Each Markdown file starts with a small front-matter block:

```markdown
---
doc_id: lecture-03-rag
doc_name: "Lecture 3 — Retrieval-Augmented Generation"
lecture: 3
source_file: lecture-03.pdf
converted_with: <tool> <version>
converter_version: 1
---
```

- **Slides or pages that could not be converted faithfully stay out of the index** rather
  than being invented. If page numbers are unavailable, the `page` metadata field is
  omitted — never fabricated ([rag-pipeline.md](../architecture/rag-pipeline.md) §3).

## 2. Conversion (Phase 1 spike, ADR-008)

1. Convert one lecture with the candidate tool, by hand, and read the output carefully.
2. Check for: reading order, tables, code blocks, formula junk, duplicated headers/footers,
   slide numbers leaking into sentences.
3. If acceptable, script it for all lectures; re-run must be deterministic.
4. Record the tool + version in the front matter and in ADR-008.

Commands are added here once the tool is chosen (`uv run python .\scripts\convert_pdfs.py`).

## 3. Chunking

Strategy (to be validated against the real slides in SG-022):

- Split on Markdown headings first, so a heading stays with its content
  ([rag-pipeline.md](../architecture/rag-pipeline.md) §3).
- Then split long sections into chunks of **~700–900 characters with ~120 overlap**, and
  never split inside a fenced code block or a table.
- Drop chunks under ~80 characters unless they clearly carry meaning (e.g. a short definition).
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

Chunk **id** is deterministic: `f"{doc_id}:{page or 0}:{chunk_index}:{text_hash[:12]}"`.
This makes re-indexing idempotent — the same content always lands on the same id.

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

Checklist:

- [ ] Chunk count is reported and stable across two runs.
- [ ] Spot-check 3 chunks: text reads correctly and metadata points at the right lecture.
- [ ] Two sample queries return the expected lectures/slides.
- [ ] A deliberately off-topic query returns low-relevance results (so `empty` handling can
      be tested).

## 8. Open items

- Conversion tool (ADR-008) and whether slide titles become headings.
- Exact chunk size/overlap and `top_k` (to be measured, then recorded in the decision log).
- Whether lecture PDFs contain tables/code that need special handling.
- Whether a relevance threshold is meaningful for this corpus.
