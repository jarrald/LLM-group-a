---
doc_id: rag.linear_regression.examples
title: Worked scikit-learn linear regression examples
topic: linear_regression
doc_type: examples
version: 1
keywords: [example, runnable code, toy data, predict, coefficients, one feature, multiple features]
---

# Worked examples: scikit-learn linear regression

## Example 1: one feature with a tiny dataset

This example uses synthetic data where the target follows an exact linear rule. It demonstrates the API, not real-world model quality.

    import numpy as np
    from sklearn.linear_model import LinearRegression

    X = np.array([[1], [2], [3], [4], [5]], dtype=float)
    y = np.array([3, 5, 7, 9, 11], dtype=float)

    model = LinearRegression()
    model.fit(X, y)

    print("Intercept:", model.intercept_)
    print("Coefficient:", model.coef_[0])
    print("Prediction for x=6:", model.predict([[6]])[0])

Expected result (up to floating-point precision):
- intercept approximately `1.0`;
- coefficient approximately `2.0`;
- prediction for `x=6` approximately `13.0`.

The learned relationship is `predicted_y = 1 + 2*x`.

## Example 2: multiple features

    import numpy as np
    from sklearn.linear_model import LinearRegression

    X = np.array([
        [1000, 2],
        [1500, 3],
        [2000, 3],
        [2500, 4],
        [3000, 5],
    ], dtype=float)

    y = np.array([200000, 280000, 330000, 400000, 480000], dtype=float)

    model = LinearRegression()
    model.fit(X, y)

    print("Intercept:", model.intercept_)
    print("Coefficients:", model.coef_)

    new_home = np.array([[1800, 3]], dtype=float)
    prediction = model.predict(new_home)
    print("Predicted price:", prediction[0])

The first feature is square footage and the second is bedroom count. The coefficients are in the same order as the columns of `X`. The data are illustrative and do not establish a meaningful real-estate pricing model.

## Example 3: complete train/test/evaluate template with pandas

    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    # Replace this with your own data loading step.
    df = pd.read_csv("data.csv")

    target_column = "target"
    feature_columns = ["feature_a", "feature_b"]

    X = df[feature_columns]
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print(f"MAE: {mean_absolute_error(y_test, y_pred):.3f}")
    print(f"RMSE: {mean_squared_error(y_test, y_pred) ** 0.5:.3f}")
    print(f"R2: {r2_score(y_test, y_pred):.3f}")

    coefficients = pd.Series(model.coef_, index=feature_columns)
    print("Intercept:", model.intercept_)
    print("Coefficients:")
    print(coefficients)

Before running, verify that the target and feature columns exist, that the target is numeric, and that missing values and categorical columns have been handled appropriately.

## Example 4: a reusable function

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    def train_linear_regression(df, feature_columns, target_column):
        if target_column in feature_columns:
            raise ValueError("The target column must not be included in features.")

        missing = [
            column
            for column in [*feature_columns, target_column]
            if column not in df.columns
        ]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        X = df[feature_columns]
        y = df[target_column]

        if not all(dtype.kind in "iuf" for dtype in X.dtypes):
            raise TypeError("All feature columns must be numeric for this example.")
        if not (y.dtype.kind in "iuf"):
            raise TypeError("The target column must be numeric for regression.")
        if X.isna().any().any() or y.isna().any():
            raise ValueError("Handle missing values before fitting.")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        metrics = {
            "mae": mean_absolute_error(y_test, predictions),
            "mse": mean_squared_error(y_test, predictions),
            "rmse": mean_squared_error(y_test, predictions) ** 0.5,
            "r2": r2_score(y_test, predictions),
        }
        return model, metrics

This deliberately small function rejects missing and non-numeric data instead of silently guessing how to preprocess them. It expects a pandas DataFrame and numeric columns.

## Example 5: calculate a prediction manually from fitted values

For a one-feature model:

    prediction = model.intercept_ + model.coef_[0] * feature_value

For multiple features:

    prediction = model.intercept_ + sum(
        coefficient * feature_value
        for coefficient, feature_value in zip(model.coef_, feature_values)
    )

Prefer `model.predict(...)` in production code. Manual calculation is useful for understanding the fitted equation and checking a simple result.

## Example 6: verify feature order

If training used:

    feature_columns = ["age", "income", "tenure"]

Then prediction input must use that exact feature order:

    new_row = pd.DataFrame(
        [[30, 50000, 2]],
        columns=feature_columns
    )
    prediction = model.predict(new_row)

Do not silently reorder or omit columns. Keep the feature list from training and reuse it.

## Example limitations

These examples are for teaching the basic API. They do not cover time-series splitting, grouped observations, sample weights, sparse matrices, multi-output targets, or production preprocessing. Choose a split strategy that matches the data-generating process.
