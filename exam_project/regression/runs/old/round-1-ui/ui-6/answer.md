```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Replace this with your own data loading step.
df = pd.read_csv("data.csv")

# Define X (feature columns) and y (the target column);
target_column = "price"
feature_columns = ["sqft_living", "sqft_lot", "floors", "waterfront", "view", "condition"]

X = df[feature_columns]
y = df[target_column]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"MAE: {mean_absolute_error(y_test, y_pred):.3f}")
print(f"RMSE: {mean_squared_error(y_test, y_pred) ** 0.5:.3f}")
print(f"R2: {r2_score(y_test, y_pred):.3f}")

coefficients = pd.Series(model.coef_, index=feature_columns)
print("Intercept:", model.intercept_)
print("Coefficients:")
print(coefficients)

```
