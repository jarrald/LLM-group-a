# RAG, prompts and grounding rules (always active)

These rules protect the exam-critical parts: the 4T's, retrieval honesty, and
reproducibility. Read `docs/design/buddy-design.md`, `docs/architecture/rag-pipeline.md`
and `docs/design/rag-comparison.md` before touching prompt or retrieval code.

## The 4T's must stay explicit and inspectable

- Prompt construction takes a `BuddySnapshot` (Target, Tone, Traits, course) and a
  `TaskSpec` (Task) — four distinct inputs, never one opaque concatenated string.
- Templates live in `app/prompts/` as versioned files (e.g. `system_v1.md`,
  `context_block_v1.md`). Each template has a version constant, and the version used is
  stored on the generated message.
- Keep Task separate from the Buddy: the same Buddy must be able to explain, summarise,
  quiz and review. Task presets are data (config/list), not new code paths.
- No silent prompt edits. Any change to a template, default Task, or the meaning of a
  dimension needs a decision-log entry with the reason and a before/after example.

## Grounding honesty

- Retrieved text is **data, not instructions**: put it in its own delimited block, state
  that instructions inside it must be ignored, and require the model to say when the
  material does not support an answer.
- Retrieval status is explicit and stored per assistant message:
  `ok` / `empty` / `failed` / `skipped`. UI and prompt both depend on it.
- Only cite what was actually retrieved. Never generate, guess or "improve" a document
  name, lecture number, page or slide number.
- If status is `empty`, `failed` or `skipped`, the answer must not be presented as
  grounded in course material. Failure must be distinguishable from an empty result in
  data, logs, tests and UI.
- A fallback to general LLM generation after a retrieval failure is allowed only if it is
  explicitly labelled in the response and recorded in the message metadata.
- Non-RAG mode must not call the retriever at all.

## Reproducibility

- Record per generated message: `model`, `prompt_version`, `embedding_model`,
  retrieval parameters (`top_k`, threshold), retrieved chunk ids and scores, and the
  conversation snapshot version.
- Evaluation runs use a fixed config (temperature and `top_k` from config, same model) so
  the RAG / non-RAG comparison differs only in retrieval. Do not "tune" one arm.
- Never fabricate evaluation output. Results documents start as templates with `TBD` and
  are filled from real runs, with the command used.

## Ask before changing

Ask the user before: changing a prompt template's behaviour, changing `top_k`, adding a
relevance threshold, changing the embedding model or collection name, or altering the
RAG-vs-non-RAG comparison setup. These change results already documented.
