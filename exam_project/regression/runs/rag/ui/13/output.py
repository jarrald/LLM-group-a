import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('/datasets/icecream.csv')

# Calculate the linear regression model
model = pd.LinearRegression()

# Train the model
model.fit(df.iloc[0], df.iloc[1])

# Print the model
print(model.coef_)
