---
doc_id: rag.linear_regression.diagnostics
title: Linear regression diagnostics and common failure modes
topic: linear_regression
doc_type: troubleshooting
version: 1
keywords: [diagnostics, residuals, overfitting, underfitting, multicollinearity, leakage, outliers, assumptions]
---

# Linear regression diagnostics and common failure modes

## Train score is high but test score is poor

Possible causes:
- overfitting or an unrepresentative train/test split;
- data leakage or duplicated/related observations across partitions;
- distribution shift between training and test data;
- outliers or unstable relationships;
- too many weak or noisy features.

Recommended checks:
1. Confirm that the test set was not used during fitting or preprocessing.
2. Compare train and test metrics.
3. Inspect residuals and large-error samples.
4. Verify that the split reflects the real prediction scenario.
5. Use cross-validation on training data for model selection.

Do not immediately claim one cause without inspecting the data.

## Data leakage

Data leakage occurs when information unavailable at prediction time influences model training or evaluation.

Examples:
- fitting an imputer or scaler on the full dataset before splitting;
- including a feature that is calculated using the target;
- including information recorded after the event being predicted;
- accidentally including the target column in `X`;
- using test-set results repeatedly to tune the model.

Prevent leakage by splitting first and fitting preprocessing only on training data. A scikit-learn `Pipeline` helps keep transformations and model fitting together.

## Multicollinearity

Multicollinearity occurs when two or more features are strongly linearly related.

Consequences:
- individual coefficients can become unstable;
- coefficient signs or magnitudes may be unintuitive;
- small data changes can produce large coefficient changes;
- prediction may still be reasonable even when individual coefficients are hard to interpret.

Possible responses:
- inspect feature correlations and domain relationships;
- remove redundant features when justified;
- collect more informative data;
- consider regularized models such as Ridge when coefficient stability is important.

Do not say that correlated features always make predictions inaccurate. The main concern is often coefficient variance and interpretability.

## Outliers and influential observations

OLS minimizes squared residuals, so large residuals can have a strong influence on the fitted coefficients.

Recommended checks:
- inspect residuals;
- inspect unusual feature values;
- verify data-entry errors;
- determine whether extreme observations are valid members of the target population.

Do not automatically delete outliers. Removing valid observations can bias the model. Consider robust methods if the problem warrants them.

## Nonlinear relationship

A straight-line model may underfit when the relationship is curved or otherwise nonlinear.

Check:
- scatterplots of target against important features;
- residuals versus predicted values;
- whether residuals show a systematic curve.

Possible next steps:
- add justified transformations or interaction terms;
- use polynomial features within a pipeline;
- compare with a nonlinear model using the same evaluation protocol.

Do not assume that adding polynomial terms is always beneficial. Validate the change on held-out data.

## Residual patterns

A residual is:

    residual = actual_value - predicted_value

A residual plot can reveal patterns:
- curved pattern: possible nonlinearity;
- widening spread: possible non-constant error variance;
- clusters: possible missing groups or omitted variables;
- isolated large residuals: possible unusual or influential observations.

Residual plots are diagnostic evidence, not automatic proof that a specific assumption is violated.

## Extrapolation

A prediction far outside the feature values seen during training is extrapolation. A linear relationship observed within the training range may not continue beyond it.

Warn the user when a requested prediction is outside the observed feature range. Do not present extrapolated predictions as reliably supported by the data.

## Missing values and categorical variables

Raw `LinearRegression` should not be assumed to handle arbitrary missing values or text categories.

Use appropriate preprocessing:
- impute missing numeric values;
- encode categorical features;
- fit preprocessing on training data only;
- use a `Pipeline` and `ColumnTransformer` for a repeatable workflow.

For detailed preprocessing code, consult the official scikit-learn preprocessing documentation rather than inventing transformer behavior.

## Regression or classification?

If the target is a measured numeric quantity, regression may be appropriate.

If the target is a class label, use a classification estimator. Do not use `LinearRegression` simply because the user says "predict a category".

## Official references

- Linear models guide (including multicollinearity discussion): https://scikit-learn.org/stable/modules/linear_model.html
- Model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html
- Preprocessing guide: https://scikit-learn.org/stable/modules/preprocessing.html
