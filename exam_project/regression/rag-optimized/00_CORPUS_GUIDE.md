---
doc_id: rag.linear_regression.corpus_guide
title: Corpus guide and retrieval contract
topic: linear_regression
doc_type: index
version: 1
keywords: [RAG, retrieval, scikit-learn, LinearRegression, corpus, Gemma 3 270M]
---

# Corpus guide: scikit-learn linear regression

## Purpose

This corpus teaches a small language model to explain and generate correct, conservative Python code for ordinary least-squares (OLS) regression using scikit-learn's `LinearRegression`.

It is deliberately narrow. It does not attempt to teach all of scikit-learn, statistics, or machine learning.

## Canonical task

Given a tabular dataset, identify one numeric target column `y` and one or more predictor columns `X`, split rows into training and test sets, fit `LinearRegression` on training data only, predict the test data, and evaluate predictions with regression metrics.

## Retrieval routing

Use the following routing rules before answering:

| User intent | Retrieve |
|---|---|
| "What is linear regression?", slope, intercept, OLS | `01_LINEAR_REGRESSION_CONCEPTS.md` |
| sklearn import, fit, predict, `X`/`y` shapes, DataFrame | `02_SKLEARN_LINEAR_REGRESSION_WORKFLOW.md` |
| MAE, MSE, RMSE, R-squared, evaluation | `03_REGRESSION_EVALUATION.md` |
| leakage, multicollinearity, residuals, assumptions, bad results | `04_DIAGNOSTICS_AND_COMMON_FAILURES.md` |
| complete runnable example, predict a new row, reusable function | `05_WORKED_EXAMPLES.md` |
| ambiguous request, response policy, abstention, tool execution | `06_SMALL_MODEL_RESPONSE_PLAYBOOK.md` |

For a complete "build and evaluate a model" request, retrieve documents 02, 03, and 05. Add 04 when the user asks why results are poor or whether a model is appropriate.

## Retrieval units

- Each file is a topic-focused document.
- Headings are designed as semantic chunk boundaries.
- Keep each heading with the explanatory paragraph, code example, and caveat that belong to it.
- Prefer retrieving one to three relevant chunks, not the entire corpus.
- Do not split a code block from the text that explains its inputs and outputs.
- Keep metadata/frontmatter out of the user-facing answer unless the user asks about the corpus.

## Answer contract for the model

1. Use `sklearn.linear_model.LinearRegression` for ordinary least-squares linear regression.
2. Use `X` for a 2D feature matrix and `y` for a 1D target vector in the common single-target case.
3. Fit only on training data. Never fit on test data before evaluation.
4. Call `predict` with the same feature columns, in the same order, used during fitting.
5. Report metrics on held-out test data, not training data, unless explicitly discussing training fit.
6. Never invent a dataset's column names, numerical results, or model quality.
7. If the data or target is unspecified, ask for the target column and predictor columns, or provide a clearly labeled template.
8. If exact arithmetic matters, run Python/NumPy/scikit-learn rather than guessing numeric outputs.
9. Distinguish regression (numeric target) from classification (categorical target).
10. Do not claim that linear regression proves causation.

## Version policy

The examples use the stable public scikit-learn API. Some estimator parameters vary across scikit-learn versions. Prefer the simple constructor `LinearRegression()` unless a user asks about a specific parameter. Do not hallucinate version-specific defaults.

## Source of truth

- Linear models guide: https://scikit-learn.org/stable/modules/linear_model.html
- `LinearRegression` API: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
- Model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html
- `train_test_split` API: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
