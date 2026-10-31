# Week 3 — Gradient Descent, Loss Functions, Cross-Validation, and Embeddings

**Primary source:** `Week3.pdf`, especially slides 8–10 and 16–29.  
**Related notebooks:** `gradient_descent_linear_regression.ipynb`, `train_embeddings.ipynb`, `Exercise_3.1.ipynb`, `PCA_for_FewerDimensions_4d_to_2d.ipynb`, and `curriculum_embeddings.ipynb`.

## 1. A machine-learning model is a function

A model maps input to output. The lecture gives:

```text
x = [1, 2, 3, 4]
f(x) = [1, 4, 9, 16]
```

This example squares each input. It shows that a model can be a non-linear function. A model's parameters determine which function is represented.

## 2. Linear regression and its parameters

The Week 1 example is:

\[
f(x) = ax + b
\]

- `a` is the slope.
- `b` is the intercept (also commonly called the bias term in this simple model).

Given training pairs `(x_i, y_i)`, the model predicts `a*x_i + b`. The prediction error for one point is the difference between the prediction and its observed target.

## 3. Loss function

The Week 3 slides use the average squared error:

\[
L(a,b) = \frac{1}{N}\sum_{i=1}^{N}(a x_i + b - y_i)^2
\]

where:

- `N` is the number of training points.
- `x_i` is the input for point `i`.
- `y_i` is the observed target.
- `a*x_i + b` is the model prediction.
- `L(a,b)` is the loss for the selected parameters.

Squaring makes negative and positive residuals contribute non-negative values and penalizes larger residuals more heavily. The training objective is to find parameters that minimize this loss. The lecture's formula uses a factor of `1/N`; other formulations may use `1/(2N)` or a sum rather than an average.

## 4. Gradient descent

Gradient descent is an iterative optimization algorithm. In broad terms:

1. Initialize model parameters.
2. Evaluate the loss.
3. Calculate the gradient—the direction and rate of steepest increase in the loss.
4. Move the parameters in the opposite direction to reduce the loss.
5. Repeat until a stopping criterion is met.

For parameters `θ`, the standard update is:

\[
\theta_{t+1} = \theta_t - \eta \nabla_\theta L(\theta_t)
\]

where `η` is the learning rate.

For the lecture's two-parameter model, `θ` consists of `a` and `b`. The loss surface can be visualized over this two-dimensional parameter space.

## 5. Learning rate

The learning rate controls the size of each parameter update.

- **Too small:** training can make very slow progress.
- **Appropriate:** updates may converge efficiently toward a low-loss region.
- **Too large:** updates may overshoot, oscillate, or diverge rather than converge.

The lecture's Exercise 3.1 explicitly asks students to change `LEARNING_RATE` and try extreme values between 0.0 and 1.0 to observe how fitting behaves. The exact useful range depends on the data scaling, model, optimizer, and implementation; 0.0–1.0 is the exercise's exploration range, not a universal recommended range.

## 6. Local and global minima

A **global minimum** is the lowest value of a loss function over the entire parameter space. A **local minimum** is lower than nearby points but may not be globally lowest.

The lecture contrasts simple linear regression with high-dimensional, non-linear models such as LLMs. Their optimization landscapes can be complex and may contain many low-loss regions. A training process finding a low loss does not establish that the model's output is universally true or semantically perfect.

## 7. Train/test evaluation and K-fold cross-validation

A train/test split holds out data from fitting so performance can be evaluated on examples not used for parameter estimation.

In K-fold cross-validation:

1. Divide the dataset into `K` folds.
2. Train on `K-1` folds and validate on the remaining fold.
3. Repeat so each fold serves as validation once.
4. Aggregate the `K` validation results.

Cross-validation estimates how results vary across splits. If hyperparameters are tuned using cross-validation, a separate final test set is still useful for an unbiased final evaluation.

## 8. Exercise 3.1 — gradient descent with the diabetes dataset

The lecture instructions are:

1. Obtain the scikit-learn diabetes dataset: https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset
2. Open `gradient_descent_linear_regression.ipynb` from the course materials.
3. Run it in VS Code or Jupyter via Anaconda Navigator.
4. Read the notebook; the lecture says sections 4 and 5 are central.
5. Change parameters, especially `LEARNING_RATE`.
6. Try extreme learning-rate values and observe when fitting becomes poor.

The purpose is to understand how parameter updates affect optimization. Do not assume a specific score or coefficient without running the supplied notebook.

## 9. Exercise 3.2 — text corpora and embeddings

This is voluntary preparation for Week 5. Students are asked to:

1. Obtain `corpus.txt` from the course materials.
2. Open `train_embeddings.ipynb`.
3. Read the notebook, focusing on sections 4 and 5.
4. Experiment with parameters, especially the learning rate.
5. Observe the effect of extreme learning-rate values.

An **embedding** is a numerical vector representation of a token, sentence, or document. Embedding models are trained so that vector relationships capture useful patterns in text, according to their training objective. An embedding map visualizes vectors in a lower-dimensional display; it does not show meaning directly and may involve dimensionality-reduction distortions.

Lecture references:

- Nomic sample map: https://atlas.nomic.ai/map/nomic-text-embed-v1-5m-sample
- Nomic embedding technical report: https://static.nomic.ai/reports/2024_Nomic_Embed_Text_Technical_Report.pdf

## 10. Review questions

1. What does the loss function measure?
2. Why does gradient descent move opposite the gradient?
3. What is the learning rate?
4. What behavior might occur when the learning rate is too large?
5. Why is a low training loss not sufficient to establish good generalization?
6. How do local and global minima differ?
7. Why might K-fold cross-validation be useful?
8. What does an embedding represent?
9. What are the limitations of interpreting a two-dimensional embedding map?
