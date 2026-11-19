```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, LinearRegression
from sklearn.preprocessing import median_imputer, OneHotEncoder
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('regression/datasets/house prices.csv')

# Convert 'yr_built' and 'yr_renovated' to numeric
df['yr_built'] = pd.to_numeric(df['yr_built'])
df['yr_renovated'] = pd.to_numeric(df['yr_renovated'])

# One-hot encode categorical columns
df = pd.get_dummies(df, columns=['city'])

# Split data into training and testing sets
X = df.drop('price', axis=1)
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the linear regression model
model = LinearRegression()

# Fit the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Calculate Mean Absolute Error (MAE) and R-squared
mae = np.mean(np.abs(y_test - y_pred))
r2 = model.score(X_test, y_test)

# Print the results
print(f"Mean Absolute Error (MAE): {mae}")
print(f"R-squared: {r2}")
```
