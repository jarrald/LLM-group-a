# Gemma 3 270M — scikit-learn Linear Regression RAG corpus

This package contains seven Markdown documents designed for retrieval-augmented generation (RAG).

## Files
- `00_CORPUS_GUIDE.md` — routing, retrieval boundaries, answer contract
- `01_LINEAR_REGRESSION_CONCEPTS.md` — concepts and terminology
- `02_SKLEARN_LINEAR_REGRESSION_WORKFLOW.md` — API and end-to-end workflow
- `03_REGRESSION_EVALUATION.md` — MAE, MSE, RMSE, R-squared
- `04_DIAGNOSTICS_AND_COMMON_FAILURES.md` — leakage, residuals, multicollinearity, debugging
- `05_WORKED_EXAMPLES.md` — runnable examples and reusable function
- `06_SMALL_MODEL_RESPONSE_PLAYBOOK.md` — small-model behavior and evaluation queries

## Suggested ingestion defaults
Start with heading-aware Markdown splitting:
- chunk by `##` sections, retaining the parent `#` title and relevant metadata;
- target 350–650 tokens per chunk;
- overlap 40–80 tokens only when a section must be split;
- do not split code blocks from their explanation;
- store `doc_id`, `title`, `topic`, `doc_type`, `keywords`, and section heading as metadata;
- use cosine similarity with the embedding model's recommended normalization;
- retrieve top 3–5 chunks, then optionally rerank to top 2–3.

Do not blindly use a fixed character splitter across the corpus. Section-aware chunking preserves the relationship between instructions, examples, and caveats.

## Quality evaluation
Run the eight test prompts in `06_SMALL_MODEL_RESPONSE_PLAYBOOK.md`. Check:
1. retrieval relevance (did the right document/section appear?);
2. factual correctness;
3. runnable code;
4. shape correctness;
5. no leakage;
6. no fabricated numerical outputs;
7. correct metric interpretation.

A useful initial retrieval target is that the correct document appears in the top 3 for each query. Track answer correctness separately from retrieval hit rate.

## Important limitation
RAG supplies relevant information; it does not update model weights or guarantee arithmetic. For reliable fitting and numeric predictions, let Gemma generate validated Python and execute it in a sandbox with restricted permissions. Do not expose arbitrary filesystem, network, or shell access to model-generated code.

## Sources
The source URLs are included in the relevant Markdown files. Core official references:
- https://scikit-learn.org/stable/modules/linear_model.html
- https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
- https://scikit-learn.org/stable/modules/model_evaluation.html
