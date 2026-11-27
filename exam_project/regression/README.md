# Local-AI development test

Paste a prompt about scikit-learn, get a runnable file back. That is the whole experiment:
is a local model + retrieval good enough to write code you can actually use?

## Setup (once, ~1–2 minutes)

The retrieval corpus is a **third-party scikit-learn source checkout**. It is git-ignored
(~23 MB, 1 600+ files), so a fresh clone of this repository does **not** contain it — it has
to be downloaded before the index can be built:

```powershell
uv run python -m regression.fetch_corpus          # downloads scikit-learn into regression/scikit-learn-main
uv run python -m regression.rag --build-index     # chunk + embed both sources, embeddinggemma
```

`fetch_corpus.py` downloads the repository archive (no `git` needed) and writes
`regression/scikit-learn-main/.corpus.json` with the ref, the commit GitHub reports for it and
the `scikit-learn.__version__` the checkout declares. The default ref is `main`. The current
2026-11-19 experiment uses the **lean** profile and `embeddinggemma`: 566 chunks (12 scikit-learn
files + 7 project guides). The older qwen-era, source-only 962-chunk and guide-inclusive 1,041-chunk
runs are archived under `runs/old/`. To pin a release instead:

```powershell
uv run python -m regression.fetch_corpus --ref 1.6.1 --force
uv run python -m regression.rag --build-index --recreate
```

The index needs no server: it is an in-process Chroma database in `regression/.chroma`.

**The active index combines two sources:**

| Source | What | Citation path |
|---|---|---|
| `regression/scikit-learn-main/` | the third-party checkout, filtered by the active `INCLUDE` profile in `rag.py` | `sklearn/…`, `examples/…`, `doc/…` |
| `regression/rag-optimized-lean/*.md` | the **current** guidance set: concepts, workflow, metrics, diagnostics, worked examples, mixed-type pipeline | `rag-optimized-lean/<file>.md` |
| `regression/rag-optimized/*.md` | the older, larger guidance set (kept for the archived runs) | `rag-optimized/<file>.md` |

The guidance documents are **optional and automatic**: every `*.md` under that folder is
chunked by heading and indexed next to the source, so a rebuild picks up edits. They are cited
with their own path, so the run record shows whether an excerpt came from the library or from
our own notes. The index stores a fingerprint of every indexed file, so editing a document and
querying without rebuilding fails with the exact `--recreate` command instead of answering from
the old text.

To build the **source-only** index that the runs recorded before 2026-11-11 used, point the
extra corpus at a path that does not exist:

```powershell
$env:RAG_EXTRA_CORPUS = "none"
uv run python -m regression.rag --build-index --recreate
```

**Check the setup in one command:**

```powershell
uv run python -m regression.rag --status
```

It prints the corpus path and provenance, the collection with its chunk count and metadata,
and the chat/embedding models. A stale or foreign index is reported as `STALE:` with the
command that rebuilds it.

## Use

```powershell
uv run python -m regression.chat
uv run python -m regression.chat --list-models     # what is installed, and what can chat
```

- Paste your prompt. It can span several lines — press Enter on an empty line to send.
- CLI runs land in `regression/runs/rag/cmd/<n>/`; web runs land in `regression/runs/rag/ui/<n>/`. Files are `.py`, or `.ipynb` if you ask for a notebook.
- One-shot from the shell: `--ask "..."`. Another model: `--model llama3.2:3b`.

Example prompt:

```text
Please make a jupyter notebook that does a linear regression
on the dataset at regression/datasets/ice_cream_regression.csv
```

## Web interface

```powershell
uv run streamlit run regression\web.py
```

Opens `http://localhost:8501`. Paste instructions, attach any text file you want the model to
read, pick how many scikit-learn excerpts to include (0 = only your files), press Generate.
The answer streams in, is saved to `regression/runs/rag/ui/<n>/`, and can be downloaded.

The sidebar **lists the chat models installed in Ollama** (embedding-only models such as
`nomic-embed-text` are filtered out using each model's capabilities) and starts on
`RAG_CHAT_MODEL`. Switch models between runs without editing anything; **Refresh model list**
re-reads Ollama after a `ollama pull`. The model that actually answered is shown under the
result and recorded as `- model:` in the run's `prompt.md`, so runs made with different models
stay distinguishable. If Ollama is not running, the picker says so and falls back to a text
field instead of breaking the page.

Attached files are **not** embedded: their text goes into the prompt in full, because a small
file loses more than it gains from top-k retrieval. Above 20,000 characters the page warns you
and sends only what fits. Nothing is kept between sessions. Each run folder also receives a copy of the attached files and its path is given to the model, so generated code can read the data instead of inventing a placeholder path.

## Configuration

Everything is read from the environment, so an experiment can be changed without editing code:

| Variable | Default | Meaning |
|---|---|---|
| `RAG_CHAT_MODEL` | `qwen2.5-coder:7b` | Ollama chat model (also `--model` on `chat.py`; the web picker overrides it) |
| `RAG_EMBED_MODEL` | `embeddinggemma` | embedding model for the corpus and the query |
| `RAG_TOP_K` | `4` | excerpts per prompt (also `--top-k`; `0` = no retrieval) |
| `RAG_COLLECTION` | `sklearn_lean_gemma` | collection name inside `regression/.chroma` |
| `RAG_CORPUS_PROFILE` | `lean` | `lean` = only the regression APIs; `full` = the older broad checkout |
| `RAG_EXTRA_CORPUS` | `regression/rag-optimized-lean` | folder of extra `*.md` guidance documents |
| `RAG_MIN_CHUNK_CHARS` | `80` | skip title-only chunks shorter than this |
| `RAG_TEMPERATURE` | `0.2` | generation temperature |
| `RAG_NUM_CTX` | `16384` | Ollama context window; raised from 8k for the six-run experiment |
| `RAG_CORPUS_ROOT` | `regression/scikit-learn-main` | where the corpus lives |
| `RAG_OLLAMA_URL` | `http://127.0.0.1:11434` | Ollama endpoint |

**Changing the embedding model** means rebuilding the index — the stored vectors would no
longer match the query vectors:

```powershell
$env:RAG_EMBED_MODEL = "embeddinggemma"
uv run python -m regression.rag --build-index --recreate
```

The collection records the model, the chunker version and a fingerprint of the corpus it was
built from. Building, querying or `--status` on an index that was made by something else
fails with the exact rebuild command instead of returning meaningless neighbours.

## The four T's

The page has optional Task / Tone / Target / Traits fields. Anything you fill in is prefixed to the instruction as a bullet list and recorded verbatim in `prompt.md`, so the report can show exactly which framing produced which output. Empty fields are simply left out.

## The old house-price baseline

The cloud-agent house-price notebook is archived at
`runs/old/cloud/deepseek/house-price-manual.ipynb`; it is development history, not part of the
current six-run comparison. See [`runs/old/README.md`](runs/old/README.md) for the archive map.

## Run archive

Every run, from the command line or the web page, is written to its own numbered folder:

```text
runs/rag/ui/1/prompt.md    runs/rag/ui/1/answer.md
runs/rag/ui/1/output.ipynb runs/rag/ui/1/screenshot.png
```

`prompt.md` holds the instruction verbatim, the excerpts used with their distances, the
complete system + user prompt that was sent, and the generation settings. `output.*` is the
extracted file the model produced (`.md` when it returned no code); when a code block was
extracted, `answer.md` keeps the complete raw answer next to it. The old runs `cmd/1-4` and
`ui/1-2` were backfilled from the old `out/` folder, so their excerpt lists say "not recorded" and
they have no `answer.md`; they are now under `runs/old/`.

Old runs are archived under `runs/old/` (CLI/UI, cloud, prediction) and `regression/old/`.
They are development history, not part of the current comparison. The old evaluation documents are
in [`docs/evaluation/old/`](../docs/evaluation/old/).

## Current experiment (2026-11-19)

The current regression experiment is six browser runs: three model × dataset pairs, each with
`top_k=0` and `top_k=4`. Round 2 adds an explicit **Dataset block** (exact path + header and first
row) to every instruction; round 1 is archived under `runs/old/round-1-ui/`. Setup: lean corpus
(566 chunks), `embeddinggemma`, `top_k=4`, `num_ctx=16384`, temperature 0.2. Full record:
[`docs/evaluation/regression-experiment-2026-11-19.md`](../docs/evaluation/regression-experiment-2026-11-19.md).
The teacher-approved small-model comparison is
[`docs/evaluation/regression-vs-rag.md`](../docs/evaluation/regression-vs-rag.md); the execution
evidence and detailed evaluation are in
[`docs/evaluation/regression-evaluation-2026-11-19.md`](../docs/evaluation/regression-evaluation-2026-11-19.md).

| Run | Model | Dataset | `top_k` |
|---|---|---:|---:|
| `ui/1` | `gemma3:270m` | `ice_cream_regression.csv` | 0 |
| `ui/2` | `gemma3:270m` | `ice_cream_regression.csv` | 4 |
| `ui/3` | `gemma3:1b` | `ice_cream_regression.csv` | 0 |
| `ui/4` | `gemma3:1b` | `ice_cream_regression.csv` | 4 |
| `ui/5` | `gemma3:1b` | `house prices.csv` | 0 |
| `ui/6` | `gemma3:1b` | `house prices.csv` | 4 |

All six generated programs were executed in an isolated subprocess; **none runs** (0/6). The
execution records are `execution.md` in each run folder; interpretation is in
`docs/evaluation/regression-evaluation-2026-11-19.md`. No prediction accuracy has been computed.
Every run folder also has `prompt.md`, `answer.md`, `output.ipynb` and `screenshot.png`. The older
`qwen2.5-coder:7b` prediction comparison is historical only; it is archived under
`docs/evaluation/old/regression-vs-rag.md`, `docs/evaluation/old/prepare-data.md` and
`runs/old/predict/`.


## What happens

1. Your prompt is embedded and matched against every indexed chunk: **566** pieces of the lean
   corpus (12 scikit-learn files + 7 project guidance documents, state of 2026-11-19).
2. The top 4 excerpts are put in the prompt, marked as *data, not instructions*. The system prompt
   forbids copying excerpt headers or citations into the answer.
3. If your prompt names a `.csv` that exists, its first lines are included so the model uses the
   real column names instead of guessing.
4. The answer's Python block is written to a file. Generated notebooks get one extra first
   cell so relative paths resolve wherever you open them.

## Files

| Path | What |
|---|---|
| `fetch_corpus.py` | downloads the scikit-learn corpus (git-ignored) and records its provenance |
| `rag.py` | index build, index checks, retrieval, model listing, one Ollama call, writing the file; `--status` |
| `chat.py` | the prompt loop (`--list-models`, `--model`) |
| `web.py` | the Streamlit page (model picker, attachments, 0–12 excerpts, streaming, download) |
| `compare-predictions.py` | the old prediction comparison; historical, not part of the teacher-approved experiment |
| `PROMPTS.md` | every prompt the model sees, plus the ones already run |
| `.chroma/` | the index (git-ignored) |
| `runs/rag/` | the current six runs (`ui/1`–`ui/6`): `prompt.md` + `output.ipynb` + `answer.md` + `screenshot.png` |
| `runs/old/` | all previous runs (`rag/`, `cloud/`, `predict/`) and the discarded setup-error runs |
| `runs/old/predict/` | old results of `compare-predictions.py`; historical only |
| `non-llm.ipynb` | the hand-written ice-cream regression (70/15/15 split, three plots) |
| `old/ollama-no-rag.md` | the old `Qwen2.5:9B` no-retrieval baseline |
| `datasets/` | `ice_cream_regression.csv`, `ice_cream_polynomial.csv`, `house prices.csv` |
| `scikit-learn-main/` | the corpus, downloaded by `fetch_corpus.py` (git-ignored, ~23 MB, `main` @ `1.10.dev0`) |
| `rag-optimized-lean/` | the 7 guidance Markdown files used by the current index |
| `rag-optimized/` | the older, larger guidance set, kept for the archived runs |

## If something goes wrong

| Symptom | Fix |
|---|---|
| `the scikit-learn corpus is missing` | `uv run python -m regression.fetch_corpus` |
| `no index in …\.chroma` | `uv run python -m regression.rag --build-index` |
| `does not match the corpus/settings` | `uv run python -m regression.rag --build-index --recreate` (new corpus, ref or embedding model) |
| `cannot download …` in `fetch_corpus.py` | no network, or a ref that does not exist: retry, or use `--ref main` |
| Generation hangs | another model may be loading: check `ollama ps` |
| Code has wrong column names | include the CSV path in the prompt so it sees the header |
| Nothing relevant retrieved | ask with more scikit-learn words (`LinearRegression`, `train_test_split`, …) |
