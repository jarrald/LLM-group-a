<!-- studygraph:converted-source:v1 -->
# Week 1 — simple_linear_regression (ipynb)

Source: [week1/simple_linear_regression.ipynb](../../source/week1/simple_linear_regression.ipynb).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

Notebook cells are preserved in order. The code was not executed. Stored outputs, images and execution counts are omitted; no experimental results are added.

## Cell 1 — markdown

### Simple Linear Regression

## Cell 2 — markdown

### Data Collection

## Cell 3 — markdown

We need Pandas for data manipulation, NumPy for mathematical calculations, and Matplotlib, and Seaborn for visualizations. Sklearn libraries are used for machine learning operations

## Cell 4 — code

### Source lines 1-8

```python
# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from pandas.core.common import random_state
from sklearn.linear_model import LinearRegression
```

## Cell 5 — markdown

### Load and Explore the Dataset

## Cell 6 — markdown

We will load the dataset, check its structure, and read it into the panda's data frame.

## Cell 7 — code

### Source lines 1-3

```python
# Get dataset
df_sal = pd.read_csv('Salary_Data.csv')
df_sal.head()
```

## Cell 8 — markdown

#### Data Analysis

## Cell 9 — markdown

Descriptive Statistics
Now lets analyze the dataset to understand its structure.

## Cell 10 — code

### Source lines 1-2

```python
# Describe data
df_sal.describe()
```

## Cell 11 — markdown

#### Visualize Data Distribution

## Cell 12 — markdown

We can also find how the data is distributed visually using the Seaborn displot.

## Cell 13 — code

### Source lines 1-4

```python
# Data distribution
plt.title('Salary Distribution Plot')
sns.distplot(df_sal['Salary'])
plt.show()
```

## Cell 14 — markdown

#### Relationship between variables

## Cell 15 — markdown

Visualize the relationship between "Years of Experience" and "Salary."
A distplot shows how data is spread out. It uses a line and a histogram to display the data.
Later, we check the relationship between Salary and Experience.

## Cell 16 — code

### Source lines 1-7

```python
# Relationship between Salary and Experience
plt.scatter(df_sal['YearsExperience'], df_sal['Salary'], color = 'lightcoral')
plt.title('Salary vs Experience')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.box(False)
plt.show()
```

## Cell 17 — markdown

### Split the dataset into dependent/independent variables

## Cell 18 — markdown

Experience (X) is the independent variable
Salary (y) is dependent on experience

## Cell 19 — code

### Source lines 1-3

```python
# Splitting variables
X = df_sal.iloc[:, :1]  # independent
y = df_sal.iloc[:, 1:]  # dependent
```

## Cell 20 — markdown

#### Split the dataset into Training and Testing Sets

## Cell 21 — markdown

Separate independent (X) and dependent (y) variables, then split into training (80%) and testing (20%) sets.

## Cell 22 — code

### Source lines 1-2

```python
# Splitting dataset into test/train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
```

## Cell 23 — markdown

### Fitting the Model

## Cell 24 — markdown

Pass the X_train and y_train data into the regressor model by regressor fit to train the model using training data.

## Cell 25 — code

### Source lines 1-3

```python
# Regressor model
regressor = LinearRegression()
regressor.fit(X_train, y_train)
```

## Cell 26 — markdown

### Make predictions

## Cell 27 — markdown

Once the model is trained, we can use it to predict the test data.

## Cell 28 — code

### Source lines 1-3

```python
# Prediction result
y_pred_test = regressor.predict(X_test)     # predicted value of y_test
y_pred_train = regressor.predict(X_train)   # predicted value of y_train
```

## Cell 29 — markdown

### Visualize the Results

## Cell 30 — markdown

Now that we have our predictions, let's visualize the results through plotting graphs.

## Cell 31 — markdown

#### Training set results

## Cell 32 — markdown

Firstly, we plot the results of training sets (X_train, y_train) with X_train and the expected value of y_train (regressor.predict(X_train))

## Cell 33 — code

### Source lines 1-9

```python
# Prediction on training set
plt.scatter(X_train, y_train, color = 'lightcoral')
plt.plot(X_train, y_pred_train, color = 'firebrick')
plt.title('Salary vs Experience (Training Set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.legend(['X_train/Pred(y_test)', 'X_train/y_train'], title = 'Sal/Exp', loc='best', facecolor='white')
plt.box(False)
plt.show()
```

## Cell 34 — markdown

#### Test Set results

## Cell 35 — markdown

Secondly, we plot the results of test sets (X_test, y_test) with X_train and the expected value of y_train (regressor.predict(X_train))

## Cell 36 — code

### Source lines 1-9

```python
# Prediction on test set
plt.scatter(X_test, y_test, color = 'lightcoral')
plt.plot(X_train, y_pred_train, color = 'firebrick')
plt.title('Salary vs Experience (Test Set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.legend(['X_train/Pred(y_test)', 'X_train/y_train'], title = 'Sal/Exp', loc='best', facecolor='white')
plt.box(False)
plt.show()
```

## Cell 37 — markdown

### Coefficient and Intercept

## Cell 38 — code

### Source lines 1-3

```python
# Regressor coefficients and intercept
print(f'Coefficient: {regressor.coef_}')
print(f'Intercept: {regressor.intercept_}')
```
