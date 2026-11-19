---
doc_id: rag.linear_regression.evaluation
title: Evaluate linear regression predictions
topic: linear_regression
doc_type: reference
version: 1
keywords: [regression metrics, MAE, MSE, RMSE, R2, R-squared, evaluation, test set]
---

# Evaluate linear regression predictions

## Evaluate held-out predictions

After fitting on `X_train, y_train`, predict `X_test` and compare the predictions with `y_test`.

    y_pred = model.predict(X_test)

    from sklearn.metrics import (
        mean_absolute_error,
        mean_squared_error,
        r2_score,
    )

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)

Metrics must compare true target values and predictions for the same samples, in the same order.

## Mean absolute error (MAE)

MAE is the average absolute difference between actual and predicted values:

    MAE = average(abs(y_true - y_pred))

Interpretation:
- MAE is non-negative.
- Lower is better; zero means perfect predictions.
- MAE uses the same units as the target.
- MAE is less sensitive to large individual errors than MSE because errors are not squared.

Use MAE when a typical absolute prediction error is easy to explain.

## Mean squared error (MSE)

MSE is the average squared difference between actual and predicted values:

    MSE = average((y_true - y_pred) ** 2)

Interpretation:
- MSE is non-negative; zero is perfect.
- Lower is better.
- Its units are the square of the target's units.
- Squaring gives large errors disproportionately more influence.

Use MSE when large errors should be penalized more heavily or when the squared-error objective is relevant.

## Root mean squared error (RMSE)

RMSE is the square root of MSE:

    RMSE = sqrt(MSE)

Interpretation:
- RMSE is non-negative; zero is perfect.
- Lower is better.
- RMSE uses the same units as the target.
- Large errors have more influence than they do under MAE.

In current scikit-learn versions, `root_mean_squared_error` is available. For broad compatibility, computing `mean_squared_error(...) ** 0.5` avoids depending on that newer convenience function.

## R-squared (R2)

R-squared is the coefficient of determination. It compares model residual error with the error from predicting the mean target value.

Interpretation:
- 1.0 is the best possible score.
- 0.0 means the model is no better than the mean-prediction baseline under the standard definition.
- A negative score is possible and means the model performs worse than that baseline on the evaluated data.
- R2 is not a percentage accuracy score.
- R2 is not proof of causation or proof that the model will generalize to every future dataset.

Use:

    from sklearn.metrics import r2_score
    score = r2_score(y_test, y_pred)

`LinearRegression.score(X_test, y_test)` also returns R-squared for a regressor.

R2 is not well-defined for a test set with fewer than two samples. If the true target is constant, special finite-value handling applies by default in `r2_score`.

## Which metric should be reported?

A useful beginner report includes:
- MAE for an intuitive typical absolute error;
- RMSE when large errors deserve extra weight;
- R2 for comparison against a mean-target baseline.

Always state the target's units when known. A metric without units or context can be misleading.

## Do not evaluate only on training data

Training metrics describe fit to the data used to estimate the coefficients. They can look optimistic and do not estimate performance on unseen samples.

For a basic workflow:
1. Split rows into train and test sets.
2. Fit on training data only.
3. Predict the test rows.
4. Calculate metrics from `y_test` and `y_pred`.

For more robust model selection, use cross-validation on the training data and reserve the test set for final evaluation.

## Avoid metric hallucinations

Never invent metric values from a code snippet. If the code has not been executed and the dataset is unavailable, explain that the metrics will be computed when the user runs it.

## Official references

- Model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html
- `mean_squared_error`: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html
- `r2_score`: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
