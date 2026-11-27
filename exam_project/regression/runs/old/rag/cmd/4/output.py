import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the dataset
data = pd.read_csv('regression/datasets/ice_cream_regression.csv')

# Extract features and target
X = data[['Temperature']]
y = data['Revenue']

# Initialize and fit the LinearRegression model
model = LinearRegression()
model.fit(X, y)

# Print the coefficients
print("Intercept:", model.intercept_)
print("Coefficient:", model.coef_)
