---
doc_id: rag.linear_regression.mixed_type_pipeline
title: Mixed-type pandas data with ColumnTransformer and Pipeline
topic: linear_regression
doc_type: procedure
version: 1
keywords: [ColumnTransformer, Pipeline, OneHotEncoder, SimpleImputer, categorical, missing values, house prices]
---

# Mixed-type pandas data with ColumnTransformer and Pipeline

## When this applies

Use this workflow when a CSV contains a numeric target and a mixture of numeric and text
(categorical) feature columns. `LinearRegression` cannot fit text columns directly, so the
categorical columns must be encoded and missing values must be imputed inside a pipeline.

## Identify the columns

```python
target_column = "Price"
numeric_features = ["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "yr_built"]
categorical_features = ["waterfront", "view", "condition", "city"]
```

Use the real column names from the dataset preview. Never put the target column in the feature
lists.

## Build the preprocessing pipeline

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])

preprocess = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features),
])
```

## Fit the regression pipeline

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

X = df[numeric_features + categorical_features]
y = df[target_column]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = Pipeline([
    ("preprocess", preprocess),
    ("regression", LinearRegression()),
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, predictions))
print("R2:", r2_score(y_test, predictions))
```

## Important rules

- Split the rows before fitting the pipeline. The imputer and encoder are learned from the
  training rows only.
- Keep the target out of `X`; otherwise the model learns the answer.
- Use `handle_unknown="ignore"` so a category seen only in the test rows does not crash prediction.
- If a column is numeric but stored as text, convert it with `pd.to_numeric(..., errors="coerce")`
  before the split, or treat it as categorical.
- Do not use `accuracy_score` for a numeric target; use MAE, MSE, RMSE or R2.
