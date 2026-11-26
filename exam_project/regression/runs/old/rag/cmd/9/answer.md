```python
# %% Import necessary libraries
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# %% Load the dataset
data = pd.read_csv('regression/datasets/ice_cream_regression.csv')

# %% Prepare the data
X = data[['Temperature']]
y = data['Revenue']

# %% Create and fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# %% Make predictions
y_pred = model.predict(X)

# %% Evaluate the model
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

# %% Print the results
print(f"Intercept: {model.intercept_}")
print(f"Coefficient: {model.coef_[0]}")
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")
```
