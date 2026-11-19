```python
import pandas, train_test_split, LinearRegression, mean_absolute_error and r2_score;
import numpy as np;
import pandas.csv

try:
    # Read the CSV with pandas
    data = pd.read_csv('ice_cream_regression.csv')

    # Define X (feature columns) and y (the target column)
    X = data[['Temperature', 'Revenue']]
    y = data['Revenue']

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit LinearRegression on the training rows only
    fit = LinearRegression(X, y)
    fit.fit(X, y)

    # Predict the test rows
    predictions = fit.predict(X)

    # Print mean_absolute_error(y_test, predictions) and r2_score(y_test, predictions).

    print(mean_absolute_error(y_test, predictions) and r2_score(y_test, predictions))
except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
