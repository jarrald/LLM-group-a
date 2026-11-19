# StudyGraph — RAG vs. non-RAG comparison

**Status:** one recorded comparison, used as an exploratory demonstration. This is **not** the
planned 8-question evaluation; it is the one real paired run we have, and it is enough to show that
retrieval changes the answer. No new runs were made for this document.

## 1. Fixed configuration

Both answers used the same model, 4T configuration, question and prompt version. The only
difference was the course association, which controls whether retrieval runs.

| Setting | Value |
|---|---|
| Chat model | `llama3.2:3b` |
| Embedding model | `nomic-embed-text` (768-d) |
| Collection at the time of the run | `llms_for_devs_v1`, 57 chunks |
| `prompt_version` | `system_v1` |
| Task | Explain a concept |
| Tone | Friendly and conversational |
| Traits | Patient, Analytical |
| Target | Student familiar with the fundamentals |
| `top_k` | 4 |
| History | none (single turn) |
| Question | “What is overfitting?” |

The collection has since grown to the full course corpus; this document records the run as it was
made, not a re-run against the current index.

## 2. What retrieval returned

The course-grounded arm retrieved four passages:

- `week-1:0017` — Overfitting (distance 0.472)
- `week-1:0018` — Outliers (0.912)
- `week-1:0016` — In-class exercise 1.2, fit a model using a spreadsheet (0.962)
- `week-1:0014` — What does “training” mean? (0.978)

The general arm skipped retrieval and received no course passages.


## 3. Observed difference

| Aspect | Course-grounded (RAG) | General (no retrieval) |
|---|---|---|
| Retrieval | 4 course passages, top hit Overfitting at 0.472 | skipped, 0 passages |
| Definition | Used the course's informal definition: a model that is “too sensitive and wrong” | Generic definition: too closely fitted to training data, poor generalisation |
| Example | Referred to the course's first-degree vs eighth-degree illustration and the in-class spreadsheet exercise | Used a leaf-recognition analogy and a house-price example |
| Course alignment | High — it used the lecture's own framing and terms | Low — correct ML explanation, but not tied to the course |
| Grounding claim | Presented the answer as based on the retrieved course material | Explicitly answered from general knowledge, with no course claim |

The RAG answer did not merely sound different; it reused the specific material that retrieval
returned. The general answer was still substantially correct, but it could have been written
without the course.

## 4. Conclusion

This single paired run demonstrates the intended RAG effect: with retrieval, the answer follows the
course's own definition, example and terminology; without retrieval, the model falls back to a
generic explanation. It does **not** establish how often this happens, and it is not a full
evaluation.

## 5. Limitations

- One question, one model, one configuration and one corpus snapshot.
- The collection at the time held 57 chunks; the current course index is larger.
- LLM output is non-deterministic even with fixed parameters.
- The non-RAG model may already know “overfitting” from pretraining, so a good general answer is
  not evidence against retrieval.
- No numeric rating was assigned; the comparison is qualitative.

## 6. Raw evidence

The complete paired output, both rendered prompts and the retrieved sources are in
[`prompt-examples.md`](prompt-examples.md). The command used was:

```powershell
uv run python .\scripts\ask.py --compare --show-prompt "What is overfitting?"
```

