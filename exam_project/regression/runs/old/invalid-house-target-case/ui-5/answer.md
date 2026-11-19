```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, LinearRegression
from sklearn.preprocessing import median_imputer, OneHotEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# Read the CSV
df = pd.read_csv('regression/datasets/house prices.csv')

# Define X (feature columns) and y (the target column)
X = df[['sqft_living', 'sqft_lot', 'bedrooms', 'bathrooms', 'floors', 'waterfront', 'view', 'condition']]
y = df['price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit LinearRegression on the training rows only
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the test rows
predictions = model.predict(X_test)

# Print the mean absolute error and R2 score
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f'MAE: {mae}')
print(f'R2: {r2}')
```
