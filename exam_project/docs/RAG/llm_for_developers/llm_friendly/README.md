# Readable course material

The material is organised by the folders in `../source/`. The available weeks are **1, 2, 3, 4, 6, 8, 9 and 10**. There are no source folders for week 5 or 7, so no teaching content has been created for them.

## Reading guide

The original hand-written notes from weeks 1-3 are preserved. The new `week<N>_overview.md` files give a topic-by-topic entry point to the later weeks. Files with `_source_` contain the text, code, data or visual description of a single source. PDF conversions are divided by the page numbers of the original, so a passage can be checked against the source.

| Week | Entry point to the material | Documents | RAG chunks |
|---|---|---:|---:|
| 1 | [ML, regression and course introduction](week1/week1_complete_rag.md) | 7 | 124 |
| 2 | [The four T's and local AI](week2/week2_prompt_engineering_rag.md) | 2 | 36 |
| 3 | [Gradient descent, embeddings and societal aspects](week3/week3_overview.md) | 21 | 1,212 |
| 4 | [Local APIs, Ollama and OpenWebUI](week4/week4_overview.md) | 2 | 22 |
| 6 | [RAG, Chroma and web integration](week6/week6_overview.md) | 24 | 89 |
| 8 | [LLM Agents and Agentic LLMs](week8/week8_overview.md) | 2 | 23 |
| 9 | [Parameter fitting, validation and animations](week9/week9_overview.md) | 5 | 39 |
| 10 | [Agent orchestration and specification-driven development](week10/week10_overview.md) | 22 | 115 |
| Total | | **85** | **1,660** |

The document counts are unchanged since 2026-10-31; the chunk counts were measured again on
2026-11-09 after the corpus was translated to English (`scripts/check_course_material.py`),
which moved week 1 from 123 to 124 chunks. Chunker version 2.

The Chroma collection was rebuilt from the translated material on 2026-11-10: **1,660 chunks**,
chunker version 2, `nomic-embed-text`, corpus digest `62313c4629307e08`. `scripts/doctor.py`
reports every check as OK, including that the index still matches the material on disk. The
[retrieval checks](retrieval-check.json) record concrete queries, document ids and distances;
they were regenerated against that index by `scripts/check_retrieval.py` and all seven checks
(weeks 4, 6, 8, 9, 10 plus two probes) pass. They verify that the material is reachable; they
are not the formal RAG evaluation.

A broad gradient-descent query ranks week 9 first and still reaches the week 3 notes within the
top six, because the topic is repeated in both weeks. An English CNN query that did not find the
Danish video notes in the pre-translation corpus (2026-10-31) now returns week 9 in its first
four hits, as expected once question and material share a language. Cross-language retrieval
quality is assessed in phase 7.
## Coverage and limitations

`conversion-manifest.json` records all 73 relevant sources with SHA-256, output file, status and any OCR notes. 68 sources are text-converted, four media have visual descriptions, and one identical duplicate reuses a conversion. The 15 PDFs cover 346 pages. The check also compares the original text layer with the Markdown, so that text does not disappear silently during conversion.

- The PDF text blocks are preserved in source order. Layout, columns and tables are not a perfect visual facsimile; the order of mathematical symbols may need checking. Key formulas from week 9 have been checked visually and written readably in the week overview.
- The scanned assignment description from week 3 was OCR-read in Danish and English. OCR can confuse characters, for example `AI` and `Al`; the existing topic notes help with reading it.
- Notebook cells are preserved in order without being run. Stored outputs and embedded images are omitted and are not presented as new experimental results.
- Python, JavaScript, HTML, CSS and text are reference content. Large code files are divided into sections with line numbers. A misleading file extension does not cause the content to be rewritten as something else.
- Draw.io diagrams are reproduced as labels and edges, not merely as detached names.
- Three videos without sound are described from six frame samples per video. The descriptions are not a transcription of every frame. The descriptions and the image notes are maintained in `media-descriptions.json`.
- `.env`, hidden configuration files, virtual environments, caches and generated runs are skipped before the content is read. No local API key has been taken from a `.env` file.
- The sources in `week6` use several different week numbers in their titles. The folder placement is preserved, and the original titles appear in the source conversions.
- The two language-sample corpora in `week3` (`corpus.txt`, `danish_corpus.txt`) are kept in their original language on purpose: they are the lecture's example of comparing English and Danish text with the same embedding model. Every other document is in English.

## Re-running the conversion

Run from `exam_project/` in PowerShell:

```powershell
uv sync --group conversion
uv run --group conversion python .\scripts\convert_course_material.py --ocr
uv run --group conversion python .\scripts\check_course_material.py --verify-pdfs
```

The conversion group contains PyMuPDF and the bundled FFmpeg reader for video metadata. On its first run OCR downloads the official English and Danish Tesseract language data to the user's local cache outside the repository. No external LLM is used. The sources are not modified, and the script refuses to overwrite hand-written notes. Generated files carry a dedicated marker.

When the Markdown changes, the local index must be rebuilt. Start Chroma in a separate terminal first, then run ingestion:

```powershell
uv run chroma run --host 127.0.0.1 --path .\data\chroma
```

```powershell
uv run python .\scripts\ingest.py --recreate
uv run python .\scripts\search.py "What is the difference between an LLM Agent and an Agentic LLM?"
```

`--recreate` rebuilds the course collection in Chroma from the Markdown. It does not change the raw material or the conversation database. It is required after the switch to chunker version 2, which protects code comments and embedded code fences from being interpreted as Markdown headings.