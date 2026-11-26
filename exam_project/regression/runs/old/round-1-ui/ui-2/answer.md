```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Replace this with your own data loading step.
df = pd.read_csv("data.csv")

# Define X (feature columns) and y (target column)
X = df[numeric_features + categorical_features]
y = df[target_column]

# X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model = Pipeline([
#     ("preprocess", preprocess),
#     ("regression", LinearRegression()),
# ])

# Model.fit(X_train, y_train)
# predictions = model.predict(X_test)

# Print MAE and R2
MAE = mean_absolute_error(y_test, predictions)
RMSE = mean_squared_error(y_test, predictions)
R2 = r2_score(y_test, predictions)

print("MAE:", MAE)
print("RMSE:", RMSE)
print("R2:", R2)
```
