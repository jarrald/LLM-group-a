```python
import pandas, train_test_split, LinearRegression, mean_absolute_error, r2_score;
import numpy as np;
import pandas.csv

try:
    # Read the CSV with pandas
    data = read_csv("ice_cream_regression.csv")

    # Define X (feature columns) and y (the target column)
    X = data.set_index('Temperature')
    y = data.set_index('Revenue')

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit LinearRegression on the training rows only
    fit = LinearRegression(X, y)

    # Predict the test rows
    predictions = fit.predict(X_train)

    # Print mean_absolute_error(y_test, predictions) and r2_score(y_test, predictions).

    print("Mean Absolute Error (y_test, predictions):", np.mean(y_test - predictions))
    print("R-squared (y_test, predictions):", np.sum(y_test**2) / sum(y_test))
    print("MAE (y_test, predictions):", np.mean(predictions))
    print("R2 (y_test, predictions):", np.sum(y_test**2) / sum(y_test))
```
