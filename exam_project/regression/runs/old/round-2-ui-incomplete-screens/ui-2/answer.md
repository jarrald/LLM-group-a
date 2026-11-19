```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Replace this with your own data loading step.
df = pd.read_csv("data.csv")

# Define X (feature columns) and y (target column)
X = df[feature_columns]
y = df[target_column]

# X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model = LinearRegression()
# Model.fit(X_train, y_train)

# Predict Revenue from Temperature. Use pandas and scikit-learn. Split the rows with train_test_split(random_state=42), fit LinearRegression on the training rows only, predict the test rows, and print MAE and R2. Use exactly the path and columns above; do not use data.

# Reply with one fenced ```python block.
```
