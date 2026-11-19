```python
import pandas as pd

# Load the dataset
df = pd.read_csv('regression/datasets/ice_cream_regression.csv')

# Calculate the regression line
df['Temperature'] = df['Temperature'] - df['Temperature'].mean()
df['Revenue'] = df['Revenue'] - df['Revenue'].mean()

# Print the regression line
print(df)
```
