import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Load the data
data = pd.read_csv('path_to_your_file.csv')

# Explore the data
print("Shape of the data:", data.shape)
print("Description of the data:", data.describe())
print("Missing values:", data.isnull().sum())

# Fit a simple linear regression
X = data['Temperature'].values.reshape(-1, 1)
y = data['Revenue'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

# Predict and plot
y_pred = model.predict(X)

plt.scatter(X, y, color='blue', label='Actual')
plt.plot(X, y_pred, color='red', label='Predicted')
plt.xlabel('Temperature')
plt.ylabel('Revenue')
plt.title('Revenue vs Temperature')
plt.legend()
plt.show()

# Print coefficients, intercept, MAE, and R2
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)
print("MAE:", mean_absolute_error(y, y_pred))
print("R2:", r2_score(y, y_pred))
