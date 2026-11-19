"""Check what the regression index retrieves for the queries the experiment actually uses.

    uv run python -m regression.eval_retrieval --top-k 5

Set `RAG_COLLECTION`, `RAG_EMBED_MODEL`, `RAG_CORPUS_PROFILE` and `RAG_EXTRA_CORPUS` before the
command to point at a particular index. The script does not call a chat model; it only embeds the
query, queries Chroma and prints the retrieved citations. `hit@k` is a coarse, reproducible check:
it is true when any expected file appears in the top-k citations.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from regression import rag


@dataclass(frozen=True)
class Query:
    """One retrieval probe and the files that should be enough to answer it."""

    name: str
    text: str
    expected: tuple[str, ...]


QUERIES = (
    Query(
        "ice-cream prompt",
        "Write a complete runnable Python notebook cell that trains and evaluates a linear "
        "regression. Use the CSV at regression/datasets/ice_cream_regression.csv with columns "
        "Temperature and Revenue. Use pandas and scikit-learn: train_test_split(random_state=42), "
        "fit LinearRegression on the training rows only, predict the test rows, print MAE and R2.",
        ("02_SKLEARN_LINEAR_REGRESSION_WORKFLOW", "linear_model/_base.py", "05_WORKED_EXAMPLES"),
    ),
    Query(
        "API recipe",
        "Use sklearn.linear_model.LinearRegression with train_test_split, fit on X_train, "
        "predict X_test and print mean_absolute_error and r2_score.",
        ("02_SKLEARN_LINEAR_REGRESSION_WORKFLOW", "_base.py", "_split.py", "_regression.py"),
    ),
    Query(
        "house prices",
        "Read regression/datasets/house prices.csv with pandas, predict the Price column from "
        "the other columns, and one-hot encode the categorical columns.",
        ("_column_transformer.py", "_encoders.py", "02_SKLEARN_LINEAR_REGRESSION_WORKFLOW", "04_DIAGNOSTICS"),
    ),
    Query(
        "preprocessing",
        "Handle missing values and categorical features before LinearRegression with "
        "ColumnTransformer and Pipeline.",
        ("_column_transformer.py", "_base.py", "pipeline.py", "04_DIAGNOSTICS"),
    ),
    Query(
        "metrics",
        "Evaluate regression predictions with mean absolute error, RMSE and R2.",
        ("03_REGRESSION_EVALUATION", "_regression.py"),
    ),
    Query(
        "shape error",
        "scikit-learn raises Expected 2D array, got 1D array instead when fitting "
        "LinearRegression.",
        ("02_SKLEARN_LINEAR_REGRESSION_WORKFLOW", "_base.py"),
    ),
)


def first_match(hits: list[rag.Hit], expected: tuple[str, ...]) -> int | None:
    """One-based rank of the first hit whose path contains an expected label."""
    for rank, hit in enumerate(hits, start=1):
        if any(label in hit.path for label in expected):
            return rank
    return None


def main() -> int:
    """Print a compact retrieval table and the hit@k count."""
    parser = argparse.ArgumentParser(description="Check retrieval quality for the regression corpus.")
    parser.add_argument("--top-k", type=int, default=5, help="excerpts to retrieve per query")
    parser.add_argument("--verbose", action="store_true", help="print every retrieved citation with its distance")
    args = parser.parse_args()

    print(f"collection : {rag.COLLECTION}")
    print(f"embedding  : {rag.EMBED_MODEL}")
    print(f"profile    : {rag.CORPUS_PROFILE}")
    print(f"guides     : {rag.EXTRA_CORPUS}")
    print(f"top_k      : {args.top_k}")
    print()
    print(f"{'query':<18} {'hit@k':<6} {'rank':<5} first matching citation")
    print("-" * 100)

    matched = 0
    for query in QUERIES:
        hits = rag.retrieve(query.text, top_k=args.top_k)
        rank = first_match(hits, query.expected)
        if rank is not None:
            matched += 1
        first = next((hit.cite for hit in hits if any(label in hit.path for label in query.expected)), "-")
        print(f"{query.name:<18} {str(rank is not None):<6} {str(rank or '-'):<5} {first}")
        if args.verbose:
            for position, hit in enumerate(hits, start=1):
                print(f"    [{position}] {hit.distance:.3f}  {hit.cite}")

    print("-" * 100)
    print(f"hit@{args.top_k}: {matched}/{len(QUERIES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
