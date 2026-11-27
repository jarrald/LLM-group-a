"""Read-only recalculation of quantitative claims for the synopsis audit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.adapters.chunker import chunk_document, chunks_digest  # noqa: E402
from app.adapters.loader import discover_lectures  # noqa: E402
from regression import rag  # noqa: E402


def numerical_experiment() -> None:
    frame = pd.read_csv(ROOT / "regression" / "datasets" / "ice_cream_regression.csv")
    features = frame[["Temperature"]].to_numpy()
    target = frame["Revenue"].to_numpy()
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.15, random_state=42)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.15, random_state=42)

    print("\nNUMERICAL EXPERIMENT")
    print(f"dataset shape: {frame.shape}; columns: {list(frame.columns)}")
    for name, count in (("train", len(x_train)), ("validation", len(x_val)), ("test", len(x_test))):
        print(f"  {name}: {count} rows = {100 * count / len(frame):.4f}%")

    model = LinearRegression().fit(x_train, y_train)
    print(f"fitted coefficients: slope={float(model.coef_[0]):.9f}, intercept={float(model.intercept_):.9f}")
    for name, x_part, y_part in (("train", x_train, y_train), ("validation", x_val, y_val), ("test", x_test, y_test)):
        predicted = model.predict(x_part)
        print(
            f"  {name}: R2={r2_score(y_part, predicted):.6f}, "
            f"RMSE={np.sqrt(mean_squared_error(y_part, predicted)):.6f}, "
            f"MAE={mean_absolute_error(y_part, predicted):.6f}"
        )

    ordered = pd.DataFrame({"Temperature": x_test.ravel(), "Revenue": y_test}).sort_values("Temperature").reset_index(drop=True)
    cases = ordered.iloc[[0, len(ordered) // 2, len(ordered) - 1]].reset_index(drop=True)
    selected_predictions = model.predict(cases[["Temperature"]])
    print(f"three selected rows are a subset of the same {len(x_test)} test rows")
    for index, case in enumerate(cases.itertuples(), start=1):
        print(
            f"  case {index}: temperature={case.Temperature:.6f}, actual={case.Revenue:.6f}, "
            f"linear={selected_predictions[index - 1]:.6f}"
        )
    print(f"selected-three linear MAE={mean_absolute_error(cases['Revenue'], selected_predictions):.6f}")

    report = json.loads((ROOT / "regression" / "runs" / "old" / "predict" / "report.json").read_text(encoding="utf-8"))
    raw_cases = report["cases"]
    actual = np.array([case["actual_revenue"] for case in raw_cases])
    for key, label in (("linear_regression", "linear"), ("llm_rag", "LLM+RAG"), ("llm_no_rag", "LLM no RAG")):
        predictions = np.array([case[key] if key == "linear_regression" else case[key]["value"] for case in raw_cases])
        print(f"  archived raw-{label} predictions={predictions.tolist()}; MAE={np.mean(np.abs(actual - predictions)):.6f}")
    rag_mae = np.mean(np.abs(actual - np.array([case["llm_rag"]["value"] for case in raw_cases])))
    bare_mae = np.mean(np.abs(actual - np.array([case["llm_no_rag"]["value"] for case in raw_cases])))
    print(f"  within-run RAG/no-RAG MAE reduction={100 * (1 - rag_mae / bare_mae):.6f}%")
    print(f"  LLM+RAG / linear MAE ratio={rag_mae / mean_absolute_error(cases['Revenue'], selected_predictions):.6f}")

    train = pd.DataFrame({"Temperature": x_train.ravel(), "Revenue": y_train}).sort_values("Temperature").reset_index(drop=True)
    positions = np.linspace(0, len(train) - 1, 12).round().astype(int)
    references = train.iloc[positions]
    print(f"  12 reference rows selected from training only:\n{references.to_string(index=False)}")


def studygraph_corpus() -> None:
    source_root = ROOT / "docs" / "RAG" / "llm_for_developers"
    documents = discover_lectures(source_root, "llms_for_devs")
    chunks = [chunk for document in documents for chunk in chunk_document(document)]
    print("\nSTUDYGRAPH CORPUS")
    print(f"documents={len(documents)}; weeks={sorted({document.lecture for document in documents})}")
    print(f"chunks={len(chunks)}; digest={chunks_digest(chunks)}")


def controlled_experiment() -> None:
    records = json.loads((ROOT / "docs" / "evaluation" / "regression-execution-2026-11-19.json").read_text(encoding="utf-8"))
    print("\nCONTROLLED CODE GENERATION")
    print(f"runs={len(records)}; exit-zero={sum(record['exit_code'] == 0 for record in records)}; nonzero={sum(record['exit_code'] != 0 for record in records)}")
    for record in records:
        print(f"  ui/{record['run']}: exit={record['exit_code']}; timed_out={record['timed_out']}; first={record['first_error']}")

    sources = rag._indexable_files()
    rows: list[tuple[str, dict[str, object]]] = []
    skipped = 0
    for label, path in sources:
        for chunk in rag._chunks_for(label, path.read_text(encoding="utf-8", errors="replace")):
            if len(str(chunk["text"]).strip()) < rag.MIN_CHUNK_CHARS:
                skipped += 1
            else:
                rows.append((label, chunk))
    guidance = sum(label.startswith(f"{rag.EXTRA_CORPUS.name}/") for label, _ in sources)
    print("\nREGRESSION CORPUS")
    print(f"files={len(sources)} ({len(sources) - guidance} scikit-learn + {guidance} guides)")
    print(f"chunks={len(rows)}; skipped shorter than {rag.MIN_CHUNK_CHARS}={skipped}")
    print(f"expected metadata={rag._index_metadata()}")
    import chromadb  # noqa: E402

    client = chromadb.PersistentClient(path=str(rag.CHROMA_PATH))
    collection = client.get_collection(rag.COLLECTION, embedding_function=None)
    print(f"stored collection={rag.COLLECTION}; count={collection.count()}; metadata={collection.metadata}")


if __name__ == "__main__":
    numerical_experiment()
    studygraph_corpus()
    controlled_experiment()
