```python
import pandas, train_test_split, LinearRegression, mean_absolute_error and r2_score;
import numpy as np;
import pandas.csv

try:
    # Read the CSV with pandas
    data = pd.read_csv('ice_cream_regression.csv')

    # Define X (feature columns) and y (target column)
    X = data[['Temperature', 'Revenue']]
    y = data['Revenue']

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit LinearRegression on the training rows only
    fit = LinearRegression(X, y)
    fit.fit(X, y)

    # Predict the test rows
    predictions = fit.predict(X)

    # Print mean_absolute_error(y_test, predictions) and r2_score(y_test, predictions).

    # If the data has categorical columns, one-hot encode them with ColumnTransformer and OneHotEncoder.
    # Never use pd.LinearRegression, never fit on the test rows, and never invent column names: use the
    # columns shown in the dataset preview. If a notebook is requested, separate cells with `# %%`.

    # Response:
    print(f"Mean Absolute Error (y_test, predictions): {mean_absolute_error(y_test, predictions)}")
    print(f"R-squared (y_test, predictions): {r2_score(y_test, predictions)}")
```
