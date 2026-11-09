import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load data
data = np.loadtxt('data.csv', delimiter=',')
X = data[:, :-1]
y = data[:, -1]

# Fit linear regression
model = LinearRegression()
model.fit(X, y)

# Print coefficients
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Predict and calculate mean squared error
y_pred = model.predict(X)
mse = mean_squared_error(y, y_pred)
print("Mean Squared Error:", mse)
