---
doc_id: rag.linear_regression.concepts
title: Linear regression concepts and terminology
topic: linear_regression
doc_type: concept
version: 1
keywords: [linear regression, ordinary least squares, OLS, slope, intercept, coefficient, residual, feature, target]
---

# Linear regression concepts

## What is linear regression?

Linear regression is a supervised learning method used to predict a numeric target from one or more input features. It represents the predicted target as a linear combination of the features.

For one feature:

    predicted_y = intercept + coefficient * x

For multiple features:

    predicted_y = intercept + coefficient_1 * x_1 + ... + coefficient_p * x_p

In scikit-learn, `LinearRegression` fits an ordinary least-squares (OLS) linear model.

## What does ordinary least squares minimize?

OLS chooses coefficients that minimize the sum of squared residuals on the training data.

A residual is the observed target minus the model's prediction:

    residual_i = y_i - predicted_y_i

The objective is:

    minimize sum((y_i - predicted_y_i) ** 2)

The fitted model minimizes this quantity for the training examples. It does not guarantee low error on unseen data.

## Feature, target, coefficient, and intercept

- **Feature (`X`)**: input variable(s) used to make predictions. In scikit-learn, `X` is normally 2D: rows are samples and columns are features.
- **Target (`y`)**: numeric value the model learns to predict. For a single target, `y` is normally 1D.
- **Coefficient (`coef_`)**: estimated weight for each feature. Holding other features fixed, a one-unit increase in a feature changes the model's prediction by that coefficient.
- **Intercept (`intercept_`)**: predicted target when all features equal zero, when an intercept is fitted.
- **Prediction (`predict`)**: model output for supplied feature rows.
- **Residual**: observed target minus predicted target.

A coefficient describes an association within the fitted model. It does not, by itself, establish a causal effect.

## Interpreting a one-feature model

Suppose a fitted model is:

    predicted_price = 12000 + 850 * engine_size_liters

Interpretation:
- The intercept is 12,000 in the target's units.
- The coefficient is 850 target units per one engine-size unit.
- Increasing engine size by one liter changes the model's predicted price by 850, according to this fitted model.

Do not interpret the intercept as meaningful if zero is outside the useful range of the feature or has no real-world meaning.

## Linear does not mean one input feature

A model can use many features and still be linear in its coefficients:

    y_hat = b0 + b1*x1 + b2*x2 + b3*x3

The model is linear in the parameters `b0`, `b1`, `b2`, and `b3`. Feature transformations can be used, but the transformed design matrix must be constructed correctly. For example, polynomial features create nonlinear curves in the original input while remaining linear in the fitted coefficients.

## When is linear regression a reasonable baseline?

It is a useful first model when:
- the target is numeric;
- a linear additive relationship is a plausible approximation;
- a simple, interpretable baseline is useful;
- training examples are representative of the data where predictions will be used.

It may perform poorly when relationships are strongly nonlinear, important variables are missing, outliers dominate the fit, or the data distribution changes.

## Regression is not classification

Use regression when the output is a numeric quantity, such as price, temperature, demand, or duration.

Use classification when the output is a category, such as spam/not spam or red/blue/green. `LinearRegression` is not a classifier. Logistic regression is a classification algorithm despite the word "regression" in its name.

## Important limitations

- A high training score does not prove good generalization.
- Correlated features can make individual coefficient estimates unstable.
- Outliers can strongly influence least-squares fitting.
- Linear regression does not automatically handle missing values or arbitrary text columns.
- Predictions outside the observed feature range are extrapolations and may be unreliable.
- Association is not causation.

## Retrieval cues

Retrieve this document for questions containing: "what is linear regression", "OLS", "least squares", "slope", "intercept", "coefficient", "residual", "feature", "target", "regression vs classification".
