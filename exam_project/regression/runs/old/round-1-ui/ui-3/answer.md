```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Read the CSV
data = pd.read_csv('regression/datasets/ice_cream_regression.csv')

# Define X (feature columns) and y (the target column)
X = data[['Temperature']]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit LinearRegression on the training rows only
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the test rows
predictions = model.predict(X_test)

# Print mean_absolute_error and r2_score
mae = np.mean(np.abs(predictions - y_test))
r2 = np.mean(np.square(predictions - y_test))

print(f'Mean Absolute Error: {mae}')
print(f'R-squared: {r2}')
```
