```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd

# Replace this with your own data loading step.
df = pd.read_csv("data.csv")

# Define X (feature columns) and y (the target column);
target_column = "Price"
feature_columns = ["sqft_living", "sqft_lot", "floors", "waterfront", "view", "condition"]

X = df[feature_columns]
y = df[target_column]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(mean_absolute_error(y_test, y_pred))
print(r2_score(y_test, y_pred))
```
