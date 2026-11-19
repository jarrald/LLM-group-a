```python
# %% Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# %% Load the dataset
data = pd.read_csv('regression/datasets/ice_cream_regression.csv')

# %% Prepare the data
X = data[['Temperature']]
y = data['Revenue']

# %% Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# %% Create a linear regression model
model = LinearRegression()

# %% Train the model
model.fit(X_train, y_train)

# %% Make predictions
y_pred = model.predict(X_test)

# %% Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# %% Plot the results
import matplotlib.pyplot as plt

plt.scatter(X_test, y_test, color='blue', label='Actual')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predicted')
plt.xlabel('Temperature')
plt.ylabel('Revenue')
plt.title('Linear Regression of Ice Cream Revenue')
plt.legend()
plt.show()
```
