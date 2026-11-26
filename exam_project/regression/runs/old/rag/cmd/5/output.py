import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.metrics import r2_score

# Load the dataset
data = pd.read_csv('regression/datasets/ice_cream_regression.csv')
X = data[['Temperature']]
y = data['Revenue']

# Initialize and fit the RidgeCV model
ridge_cv = RidgeCV(alphas=[1e-3, 1e-2, 1e-1, 1], cv=None)
ridge_cv.fit(X, y)

# Print the chosen alpha, coefficients, and R2 score
print(f"Chosen alpha: {ridge_cv.alpha_}")
print(f"Coefficients: {ridge_cv.coef_}")
print(f"R2 score: {ridge_cv.score(X, y)}")
