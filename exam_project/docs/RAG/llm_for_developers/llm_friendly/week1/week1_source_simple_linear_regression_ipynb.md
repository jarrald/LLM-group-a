<!-- studygraph:converted-source:v1 -->
# Uge 1 — simple_linear_regression (ipynb)

Kilde: [week1/simple_linear_regression.ipynb](../../source/week1/simple_linear_regression.ipynb).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

Kildeceller er bevaret i rækkefølge. Koden er ikke kørt. Gemte outputs, billeder og kørselsnumre er udeladt; der tilføjes ingen forsøgsresultater.

## Celle 1 — markdown

### Simple Linear Regression

## Celle 2 — markdown

### Data Collection

## Celle 3 — markdown

We need Pandas for data manipulation, NumPy for mathematical calculations, and Matplotlib, and Seaborn for visualizations. Sklearn libraries are used for machine learning operations

## Celle 4 — code

### Kildelinjer 1–8

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

## Celle 5 — markdown

### Load and Explore the Dataset

## Celle 6 — markdown

We will load the dataset, check its structure, and read it into the panda's data frame.

## Celle 7 — code

### Kildelinjer 1–3

```python
# Get dataset
df_sal = pd.read_csv('Salary_Data.csv')
df_sal.head()
```

## Celle 8 — markdown

#### Data Analysis

## Celle 9 — markdown

Descriptive Statistics
Now lets analyze the dataset to understand its structure.

## Celle 10 — code

### Kildelinjer 1–2

```python
# Describe data
df_sal.describe()
```

## Celle 11 — markdown

#### Visualize Data Distribution

## Celle 12 — markdown

We can also find how the data is distributed visually using the Seaborn displot.

## Celle 13 — code

### Kildelinjer 1–4

```python
# Data distribution
plt.title('Salary Distribution Plot')
sns.distplot(df_sal['Salary'])
plt.show()
```

## Celle 14 — markdown

#### Relationship between variables

## Celle 15 — markdown

Visualize the relationship between "Years of Experience" and "Salary."
A distplot shows how data is spread out. It uses a line and a histogram to display the data.
Later, we check the relationship between Salary and Experience.

## Celle 16 — code

### Kildelinjer 1–7

```python
# Relationship between Salary and Experience
plt.scatter(df_sal['YearsExperience'], df_sal['Salary'], color = 'lightcoral')
plt.title('Salary vs Experience')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.box(False)
plt.show()
```

## Celle 17 — markdown

### Split the dataset into dependent/independent variables

## Celle 18 — markdown

Experience (X) is the independent variable
Salary (y) is dependent on experience

## Celle 19 — code

### Kildelinjer 1–3

```python
# Splitting variables
X = df_sal.iloc[:, :1]  # independent
y = df_sal.iloc[:, 1:]  # dependent
```

## Celle 20 — markdown

#### Split the dataset into Training and Testing Sets

## Celle 21 — markdown

Separate independent (X) and dependent (y) variables, then split into training (80%) and testing (20%) sets.

## Celle 22 — code

### Kildelinjer 1–2

```python
# Splitting dataset into test/train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
```

## Celle 23 — markdown

### Fitting the Model

## Celle 24 — markdown

Pass the X_train and y_train data into the regressor model by regressor fit to train the model using training data.

## Celle 25 — code

### Kildelinjer 1–3

```python
# Regressor model
regressor = LinearRegression()
regressor.fit(X_train, y_train)
```

## Celle 26 — markdown

### Make predictions

## Celle 27 — markdown

Once the model is trained, we can use it to predict the test data.

## Celle 28 — code

### Kildelinjer 1–3

```python
# Prediction result
y_pred_test = regressor.predict(X_test)     # predicted value of y_test
y_pred_train = regressor.predict(X_train)   # predicted value of y_train
```

## Celle 29 — markdown

### Visualize the Results

## Celle 30 — markdown

Now that we have our predictions, let's visualize the results through plotting graphs.

## Celle 31 — markdown

#### Training set results

## Celle 32 — markdown

Firstly, we plot the results of training sets (X_train, y_train) with X_train and the expected value of y_train (regressor.predict(X_train))

## Celle 33 — code

### Kildelinjer 1–9

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

## Celle 34 — markdown

#### Test Set results

## Celle 35 — markdown

Secondly, we plot the results of test sets (X_test, y_test) with X_train and the expected value of y_train (regressor.predict(X_train))

## Celle 36 — code

### Kildelinjer 1–9

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

## Celle 37 — markdown

### Coefficient and Intercept

## Celle 38 — code

### Kildelinjer 1–3

```python
# Regressor coefficients and intercept
print(f'Coefficient: {regressor.coef_}')
print(f'Intercept: {regressor.intercept_}')
```
