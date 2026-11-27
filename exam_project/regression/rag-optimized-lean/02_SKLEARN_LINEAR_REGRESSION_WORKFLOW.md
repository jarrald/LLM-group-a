---
doc_id: rag.linear_regression.sklearn_workflow
title: scikit-learn LinearRegression API and workflow
topic: linear_regression
doc_type: procedure
version: 1
keywords: [scikit-learn, sklearn, LinearRegression, fit, predict, X, y, DataFrame, train_test_split]
---

# scikit-learn LinearRegression workflow

## Canonical import

    from sklearn.linear_model import LinearRegression

The estimator class is `sklearn.linear_model.LinearRegression`. It implements ordinary least-squares linear regression.

## Input shape rules: X and y

For the usual single-target regression task:
- `X` must be 2D with shape `(n_samples, n_features)`.
- `y` must be 1D with shape `(n_samples,)`.
- Each row in `X` must correspond to the target value at the same row in `y`.
- Every feature column must be numeric or transformed into a numeric representation before fitting.
- The feature columns supplied to `predict` must match the training features and their order.

Correct one-feature shape:

    X = df[["square_feet"]]  # DataFrame: 2D
    y = df["price"]          # Series: 1D

Common shape mistake:

    X = df["square_feet"]    # Series: 1D; wrong shape for X

If selecting one feature from a pandas DataFrame, use double brackets to keep `X` 2D.

## Minimal fit and predict

    from sklearn.linear_model import LinearRegression

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

`fit` learns the coefficients from training data. `predict` returns predictions for the supplied feature rows.

## Recommended train/test workflow

Split the data before fitting. Fit only on the training partition. Evaluate on the held-out test partition.

    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    # df is an already-loaded pandas DataFrame.
    target_column = "price"
    feature_columns = ["square_feet", "bedrooms"]

    X = df[feature_columns]
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Intercept:", model.intercept_)
    print("Coefficients:", model.coef_)
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("MSE:", mean_squared_error(y_test, y_pred))
    print("RMSE:", mean_squared_error(y_test, y_pred) ** 0.5)
    print("R2:", r2_score(y_test, y_pred))

This is a template. Replace the example column names with columns that actually exist in the user's data.

## Using a pandas DataFrame

Prefer selecting features by explicit column names:

    feature_columns = ["age", "income", "account_tenure"]
    X = df[feature_columns]
    y = df["annual_spend"]

Keep `feature_columns` in a variable so exactly the same order can be used for new prediction rows.

Avoid selecting every column blindly. The target must not accidentally appear inside `X`, and identifiers or text fields should not be included as numeric features without a reason.

## Predicting a new sample

The new input must have one row and the same feature columns in the same order as training:

    new_customer = pd.DataFrame(
        [[35, 62000, 4]],
        columns=["age", "income", "account_tenure"]
    )
    predicted_spend = model.predict(new_customer)
    print(predicted_spend[0])

For a single feature, `model.predict([[1200]])` is a valid 2D input if the model was trained with exactly one feature.

## Useful fitted attributes

- `model.coef_`: learned coefficient or coefficients.
- `model.intercept_`: learned intercept; it is `0.0` when `fit_intercept=False`.
- `model.n_features_in_`: number of features observed during fitting.
- `model.feature_names_in_`: feature names, when fitting used feature names that are all strings.

For a single target, `coef_` is normally a 1D array with one value per feature. Do not assume that `coef_` is a scalar when multiple features are used.

## Constructor defaults and restraint

For a normal baseline, use:

    model = LinearRegression()

The default behavior fits an intercept. Set `fit_intercept=False` only when there is a sound reason, such as data already being centered or the model being required to pass through the origin by the problem definition.

Do not add obscure constructor arguments to a beginner example. If a user asks about parameters, consult the installed scikit-learn version's API documentation because supported options and defaults can change between versions.

## Missing values and categorical features

`LinearRegression` should not be presented as a general-purpose raw-data cleaner. Inspect the dataset before fitting:
- Missing values generally need an explicit imputation strategy.
- Categorical columns need encoding.
- Text columns need an appropriate feature extraction strategy.
- Train-fitted preprocessing must be learned only from training data.

For robust preprocessing, use a scikit-learn `Pipeline` and `ColumnTransformer`; retrieve official preprocessing documentation before generating a detailed mixed-type pipeline.

## Common API errors

**Error: Expected 2D array, got 1D array instead**

Cause: a pandas Series or one-dimensional list was passed as `X`.

Fix: use `df[["feature"]]` instead of `df["feature"]`, or reshape a NumPy array to `(-1, 1)`.

**Error: X and y have inconsistent numbers of samples**

Cause: `X` and `y` have different row counts or were filtered/reordered separately.

Fix: create both from the same DataFrame rows and check `len(X) == len(y)`.

**Prediction feature mismatch**

Cause: new data has a different number, order, or names of features.

Fix: build prediction data with the exact training feature columns in the same order.

## Official references

- `LinearRegression` API: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
- Linear models guide: https://scikit-learn.org/stable/modules/linear_model.html
- `train_test_split`: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
