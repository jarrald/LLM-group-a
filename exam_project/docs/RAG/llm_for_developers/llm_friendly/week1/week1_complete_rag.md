# LLMs for Developers E26 — Week 1 Complete Notes

> Combined RAG source: lecture slides plus the accompanying linear-regression exercise materials.

# LLMs for Developers E26 — Week 1: Welcome

**Source:** `Week1.pdf`  
**Course:** LLMs for Developers E26  
**Session:** Week 1 — Welcome  
**Presentation date shown in slides:** 28 August 2026

> This Markdown file is a text-first transcription and organization of the lecture slides for retrieval-augmented generation (RAG). It preserves the slide topics, terminology, examples, questions, and activities. Visual diagrams are described in words where their meaning is reasonably clear. Details that are not legible or not stated in the slides are not inferred.

## Contents

1. Course overview and schedule
2. Study groups and AI in study
3. Machine learning foundations
4. Model fitting, overfitting, and outliers
5. Training, validation, and prediction
6. Introductory LLM topics and embeddings
7. Societal aspects of LLMs
8. Ambiguity, hallucinations, and prompt injection
9. Exercises and further resources
10. Key takeaways

---

## 1. Course overview and schedule

### Course timeline

The opening slides place the LLM course in a broader educational timeline:

- **Pre-E2026:** related DAT topics include Machine Learning and AI-Driven Applications (AIDA).
- **E2026:** SOFT course covering L-LLMs, machine learning (ML), and societal aspects.
- **F2027:** planned SOFT courses include Machine Learning & Data Analytics and a bachelor project.

The course's topical flow is organized around three broad strands:

1. Machine learning — technical.
2. Large Language Models (LLMs) — technical.
3. Societal, economic, and environmental aspects.

The slide depicts numbered sessions across these strands and a main-project-work period later in the course. It also marks an exam period. The graphic does not provide enough readable detail to reconstruct every individual session's topic.

### Important dates listed in the presentation

The slide lists these dates for autumn 2026:

- **Friday, 4 September:** Mandatory Assignment 1 is released.
- **Tuesday, 29 September:** Workshop; Mandatory Assignment 2 is released. A guest from ITU is mentioned.
- **Thursday, 8 October:** Mandatory Assignment 1 is due, and students review one other assignment.
- **Thursday, 29 October:** Mandatory Assignment 2 is due, and students review one other assignment.
- **Friday, 6 November:** Project period starts.
- **Monday, 14 December onward:** Exam period; the end date is unspecified.

### Project groups

The presentation strongly recommends project groups of **five people**, with the suggested composition **3 + 2 students from first and second semester**.

The slide encourages students to take an inviting, proactive approach to forming groups: more “Would you like to join us?” and less “May I join you?”

Another slide emphasizes that the value of being in a study group cannot be overestimated. Its illustration contrasts students with different backgrounds and experiences before working together with students organized into collaborative groups afterward.

### Reflection: AI in study

A 15-minute group reflection asks students to discuss:

- How do you use AI/LLMs in your daily study work?
- How have you used AI/LLMs in connection with exams?
- How does AI affect collaboration and the division of roles in group work?
- What dilemmas and concerns do you experience when using AI?
- What teaching or skills development on this topic do you feel is missing?

These are discussion prompts, not questions with prescribed answers in the slides.

---

## 2. Machine learning foundations

### General perspective

The machine-learning section opens with the quotation:

> “All models are wrong, but some are useful.” — George Box

The point is that a model is a simplified representation of a problem. Its usefulness depends on whether it serves the intended purpose, not on whether it perfectly captures reality.

### Relationship between AI, ML, and LLMs

The presentation describes AI, machine learning, and large language models as nested sets or classes:

- **Artificial Intelligence (AI):** the broad field of building machines that can perceive, reason, and act. The diagram gives examples such as rule-based systems, search/optimization, planning, expert systems, robotics, NLP, and computer vision.
- **Machine Learning (ML):** a subset of AI in which systems learn patterns from data to make predictions or decisions. The diagram mentions supervised learning, unsupervised learning, and reinforcement learning.
- **Large Language Models (LLMs):** a subset of ML focused on learning language patterns and generating human-like text. The diagram names GPT, Claude, Llama, and PaLM as examples.

**Key relationship:** all LLMs are ML models, and all ML models are AI systems, but not all AI systems are ML models, and not all ML models are LLMs.

### Data science taxonomy

The slide presents four levels of data-oriented questions:

- **Descriptive:** What has happened?
- **Diagnostic:** How did it happen?
- **Predictive:** What will happen?
- **Prescriptive:** How can we make use of a prediction?

The diagram visually places these questions in an ascending progression from describing past events to recommending action based on predictions.

### The machine-learning process is cyclic

A diagram titled “Fundamental Machine Learning — a cyclic process!” shows these stages in a loop:

1. Business case
2. Data acquisition
3. Feature engineering
4. Develop model
5. Train model
6. Validate model
7. Deploy model
8. Return to the business case and iterate

The cyclic presentation implies that deployment is not necessarily the end of the process: the model and its use can be revisited as the business case or evidence changes.

### Machine-learning landscape

A landscape diagram groups machine-learning approaches around different problem types. The readable categories include:

- **Classification**
- **Clustering**
- **Regression**
- **Dimensionality reduction**

The diagram also names a variety of methods and algorithms, including decision-tree and ensemble approaches, Naive Bayes, k-nearest neighbours, linear support vector classification, k-means, mean shift, DBSCAN, random forests, Lasso, Elastic Net, ridge regression, kernel methods, and locally linear embedding (LLE). The image is a broad landscape rather than a complete or fully legible taxonomy; it should not be treated as a definitive mapping of every method to every data condition.

### A machine-learning model as a function

The presentation states:

> Generally, a Machine Learning Model is a Function.

The basic diagram represents a model as a function **f** that takes an input **x** and produces an output **f(x)**.

The example used in the slides is a one-variable linear function:

\[
f(x) = ax + b
\]

It is also written as:

\[
y = ax + b
\]

Here, the model's output is determined by the input and the parameters represented by `a` and `b`.

### What does “training” mean?

The slides note that “training” can be an unfortunate word because it may make a model sound alive or sentient. The presentation suggests **“model parameter fitting”** might be a better term.

In the simple linear-function example, fitting a model means finding parameter values that make the function fit the observed data according to a chosen criterion.

---

## 3. Model fitting, overfitting, and outliers

### In-class exercise 1.1 — fit a model by hand

**Task:** Train an extremely simple machine-learning model by hand.

The slide uses a scatter plot of points as the context for the exercise. It does not provide a fully transcribed dataset or a numerical answer in the slide text.

### In-class exercise 1.2 — fit a model using a spreadsheet

**Task:** Train the same kind of extremely simple model using a spreadsheet tool such as:

- Microsoft Excel
- Google Sheets
- LibreOffice
- Another spreadsheet application

The slide repeats the point that “training” is parameter fitting rather than a process that makes a model alive or sentient.

### Overfitting

The presentation defines overfitting informally as making a model **too sensitive and wrong**.

The illustration compares two fits:

- A first-degree linear model with a good fit and acceptable error.
- An eighth-degree model that fits the training points much more closely and has much smaller error on those points, but follows the data too closely.

The intended lesson is that a smaller error on the observed training data does not automatically mean a better model. A highly complex model may fit peculiarities or noise in the training examples rather than patterns that generalize.

The slide title explicitly connects overfitting with “hallucinations too!” This is presented as a conceptual comparison, not as a formal claim that overfitting and LLM hallucination are identical mechanisms.

### Outliers

The slides explain that outliers can make it easy to fool ourselves into believing a model fits well, even when the model may be wrong.

Questions raised in the presentation:

- Is the model wrong?
- Is the data wrong?
- Is a better model needed?
- Would more dimensions help?
- Is this a different type of problem?

The accompanying plot shows a group of points following a general trend and a separate group of outliers. The lesson is to inspect the data and the model assumptions instead of trusting a visually plausible fit without question.

### ML Demo 1 — from a one-dimensional example to a new model

The presentation calls this “The weight of model training” and illustrates a transition from a pen-and-paper example to working with Anaconda and the Iris dataset. The slide does not provide enough text to reproduce the demonstration's detailed steps.

---

## 4. Training, validation, and prediction

The presentation's summary slide states three core points:

1. In machine learning, a model is trained by minimizing a **cost/error function**.
2. The trained model is then **validated using a test dataset**.
3. The model can then be used to **predict output values from new data**.

The slide emphasizes that this general pattern applies to all machine learning.

### Exercise 1.3 — automated training in Python

**Task:** Perform linear regression using Python.

Suggested environments:

- Jupyter Notebook
- Visual Studio Code
- Spyder

The presentation says that Kaggle salary data can be found in the course's ItsLearning Week 1 resources.

### Exercise 1.4 — automated training with a chatbot

**Task:** Repeat the linear-regression exercise, but use a chatbot or LLM assistant. The examples named in the slides are Mistral, Qwen, Ollama, ChatGPT, Claude, and Gemini, followed by “UNameIt.”

Students are asked to go through the same machine-learning steps as in the Jupyter Notebook if the chatbot does not do everything automatically.

This exercise compares using a notebook-based workflow with asking an LLM tool to help perform the workflow. The slide does not report comparative results.

### Open-ended linear-regression exercise

For students who have extra time:

1. Go to Kaggle and retrieve a suitable dataset of your choice.
2. Use an accompanying notebook if one exists, write your own, or find a generic notebook such as one using scikit-learn.
3. Try to understand how the machine learning is performed. The slides particularly emphasize validation using test data.
4. Consider:
   - What are the results?
   - Are the results meaningful — is there a linear dependence in the data?
   - Could a curve other than a straight line fit the data better?

The presentation links to Kaggle's linear-regression dataset search:
https://www.kaggle.com/datasets?search=linear+regression

---

## 5. Introductory LLM topics and embeddings

The presentation says the following week's tentative direction is to continue exploring LLMs in depth. The listed topics are:

- Optimization
- Word2vec
- Clustering
- Pre-training set
- Training

A video resource is listed:
https://www.youtube.com/watch?v=LPZh9BOjkQs

### Embedding map

The slides show an embedding map from Nomic and link to:

- Interactive sample map: https://atlas.nomic.ai/map/nomic-text-embed-v1-5m-sample
- Technical report: https://static.nomic.ai/reports/2024_Nomic_Embed_Text_Technical_Report.pdf

The slide includes a visual map and a technical-report excerpt about unsupervised contrastive pretraining. The presentation does not explain the full embedding-training method in the slide text. The map serves as a visual reference for text embeddings.

---

## 6. Societal aspects of LLMs

The societal-aspects section proposes researching human and societal dimensions of the ongoing LLM revolution. Possible topics listed on the slide are:

- Ethics and morals
- Human culture drift
- Linguistic and factuality drift
- Copyright and legal issues
- Physical residence of data
- GDPR considerations
- Explainability
- Hallucinations
- LLM security, including injections
- LLM energy consumption

The slide also includes a short case related to an AI chatbot providing inaccurate information, illustrating that hallucinations can have real-world consequences. The visible slide text does not provide enough detail to fully reconstruct the case.

These topics are framed as possible areas for study; the slide does not provide conclusions or definitive answers for each one.

---

## 7. Ambiguity, hallucinations, and prompt injection

### In-class exercise 1.5 — tests of cloud LLMs

The exercise is described as a set of simple tests of the “global LLM machinery,” preparing students for the L-LLMs topic in Week 2.

#### Test A: Ambiguity

In groups:

1. Construct two significantly different prompts that can expose ambiguity, if possible.
2. Run the prompts against several LLMs.
3. Observe the responses.
4. Reflect on the differences and report the results.

The slide's hint is to vary tone, language, or setting while essentially asking the same question.

#### Test B: Hallucination

In groups:

1. Construct a prompt containing unreal content that may provoke a hallucination.
2. Run it against several LLMs.
3. Observe and report the responses.

The slide suggests inventing something that does not exist. Its example prompt is:

> “Explain the principle underlying Relativistic Quantum Blockchains (RQBs).”

The point is to see whether a model invents an explanation for a nonexistent concept rather than acknowledging uncertainty or the premise's lack of grounding.

### Reflection and debate

The follow-up slides ask:

**Ambiguity**
- Did you learn something useful about ambiguity?
- Could you have been pushed in the wrong direction if you had listened to only one LLM?

**Hallucination**
- Did you learn something useful about LLM hallucination?
- Could you have been fooled into an alternate reality by asking the “wrong question” and listening to only one LLM?

The slides invite students to compare observations and discuss risks. They do not supply a fixed answer.

### Prompt injection

A later slide introduces **prompt injection** and asks:

> From Week 2, do we face the same challenges when using “cloud” and “local” LLMs?

The slide provides this introductory resource:
https://www.promptfoo.dev/blog/prompt-injection/

The accompanying visual distinguishes direct and indirect prompt-injection examples and shows a conversation/tool-output scenario with different privilege levels. Its central subject is that instructions can appear in user messages, model outputs, or retrieved/tool-provided content, and those sources do not necessarily have equal authority.

The slide poses the cloud-versus-local question but does not answer it. It should be treated as an open discussion question, not as evidence that the two deployment types have identical risks.

---

## 8. Study questions and key takeaways

These questions summarize the concepts and discussion prompts present in the lecture. They are intended for review, not as additional claims beyond the slides.

1. How are AI, machine learning, and LLMs related?
2. What is the difference between descriptive, diagnostic, predictive, and prescriptive questions?
3. Why can a machine-learning model be described as a function?
4. What does model parameter fitting mean in the linear-function example \(f(x)=ax+b\)?
5. Why is a cyclic machine-learning workflow useful?
6. What is overfitting, and why can a model with lower training error still be worse?
7. How can outliers mislead the evaluation of a model?
8. What roles do a cost/error function, training, validation, and a test dataset play?
9. What questions should be asked before deciding that a linear-regression result is meaningful?
10. How can changing a prompt's tone, language, or setting reveal ambiguity?
11. How can a prompt about a fictional concept help investigate hallucination?
12. What societal issues should be considered when developing or using LLMs?
13. What is prompt injection, and what question does the presentation raise about cloud versus local LLMs?

### Key takeaways stated or directly illustrated in the presentation

- AI is the broad category; machine learning is a subset of AI; LLMs are a subset of machine learning.
- A model maps inputs to outputs and is useful insofar as it serves its purpose.
- Machine-learning development is iterative and includes business framing, data acquisition, feature engineering, development, training, validation, and deployment.
- Training involves minimizing a cost/error function; validation and test data matter when judging a model's usefulness on new data.
- A very close fit to training data is not necessarily evidence of good generalization.
- Outliers and flawed assumptions can make a model appear more convincing than it deserves.
- Prompt ambiguity and hallucination can be investigated by testing variations and comparing responses across multiple LLMs.
- LLM use raises societal questions involving ethics, culture, factuality, copyright, data residence, GDPR, explainability, security, and energy consumption.
- The presentation raises prompt injection as a security topic and leaves the cloud-versus-local comparison open for discussion.

---

## 9. Resources mentioned in the slides

- **Large Language Models for the Curious Beginner** (YouTube): https://www.youtube.com/watch?v=LPZh9BOjkQs
- **Nomic text-embedding map:** https://atlas.nomic.ai/map/nomic-text-embed-v1-5m-sample
- **Nomic text-embedding technical report:** https://static.nomic.ai/reports/2024_Nomic_Embed_Text_Technical_Report.pdf
- **Prompt injection introduction:** https://www.promptfoo.dev/blog/prompt-injection/
- **Kaggle linear-regression datasets:** https://www.kaggle.com/datasets?search=linear+regression

## 10. Scope and source notes

- This document is based on the 34-slide PDF titled `Week1.pdf`.
- Course dates and schedule items are reproduced as presented in the slides and may be subject to change.
- Some diagrams contain small labels that are not fully legible in extracted text. Their descriptions above are limited to clearly readable concepts.
- Exercises are preserved as tasks and questions; no student answers or experimental results were included in the source slides.
- The presentation announces some later topics as tentative. Those topics should not be interpreted as a guaranteed schedule.

---

# Week 1 — Machine Learning 0.0.1: Linear Regression Training Data

## Purpose

This document covers the remaining Week 1 material supplied alongside the lecture: a small hand-held linear-regression dataset, its coordinate plot, and a notebook demonstrating simple linear regression on salary data.

The content below is based on the supplied files. It describes the exercise and notebook workflow; it does not claim that a model has been fitted or evaluated unless that result is explicitly shown in the supplied materials.

## 1. Machine Learning 0.0.1 — Hand-held training data

The files identify the dataset as **“Machine learning 0.0.1, training data.”** The data consists of 20 `(x, y)` coordinate pairs.

### Coordinate pairs

```text
10.5, 12.73
0.5, -2.50
-1.5, -1.12
-3.5, -2.50
-1.5, 1.65
-5.5, -2.50
-3.5, -1.12
2.5, 3.04
0.5, 0.27
6.5, 7.19
4.5, 3.04
6.5, 8.58
10.5, 15.50
4.5, 8.58
6.5, 3.04
4.5, 0.27
4.5, 7.19
2.5, 8.58
10.5, 5.81
0.5, 5.81
```

### Vector representation

The same dataset is supplied as two vectors, where each `x` value corresponds by position to the `y` value at the same index:

```python
x = [10.5, 0.5, -1.5, -3.5, -1.5, -5.5, -3.5, 2.5, 0.5, 6.5, 4.5, 6.5, 10.5, 4.5, 6.5, 4.5, 4.5, 2.5, 10.5, 0.5]
y = [12.73, -2.50, -1.12, -2.50, 1.65, -2.50, -1.12, 3.04, 0.27, 7.19, 3.04, 8.58, 15.50, 8.58, 3.04, 0.27, 7.19, 8.58, 5.81, 5.81]
```

### Reading the plotted data

The accompanying image, titled **“Machine Learning Chapter 0.0.1,”** plots the supplied coordinate points on an x-y grid. The horizontal axis is labelled `x`; the vertical axis is labelled `f(x)`. The plot visualizes the sample points rather than a fitted regression line.

The points do not all lie on a single straight line. The dataset can be used to explore how a simple model approximates observed data, how parameters affect a fitted line, and why residual error remains when a linear function does not match every point.

These are possible learning uses of the plotted data, not results reported by the supplied files.

## 2. Salary dataset for simple linear regression

The file `Salary_Data.csv` contains two columns:

- `YearsExperience`: the independent/input variable, labelled `X` in the notebook.
- `Salary`: the dependent/target variable, labelled `y` in the notebook.

The supplied CSV contains **30 rows**. Its first records are:

| YearsExperience | Salary |
|---:|---:|
| 1.1 | 39343.00 |
| 1.3 | 46205.00 |
| 1.5 | 37731.00 |
| 2.0 | 43525.00 |
| 2.2 | 39891.00 |

The notebook uses this dataset to examine the relationship between years of experience and salary, then fit a simple linear regression model.

## 3. Notebook workflow: `simple_linear_regression.ipynb`

### Libraries used

The notebook imports:

- **Pandas** for tabular data manipulation.
- **NumPy** for numerical calculations.
- **Matplotlib** and **Seaborn** for visualizations.
- `train_test_split` from `sklearn.model_selection` to split data into training and testing sets.
- `LinearRegression` from `sklearn.linear_model` to create the regression model.

### Step 1 — Load and explore the data

The notebook loads the CSV into a Pandas DataFrame:

```python
df_sal = pd.read_csv('Salary_Data.csv')
df_sal.head()
```

It then calls `df_sal.describe()` to produce descriptive statistics for the columns.

### Step 2 — Visualize the data

The notebook first creates a salary distribution plot. It then creates a scatter plot of `YearsExperience` against `Salary` to visualize their relationship.

The scatter plot is intended to help the learner inspect whether a roughly linear relationship is plausible.

### Step 3 — Define the input and target variables

The notebook defines:

```python
X = df_sal.iloc[:, :1]  # independent variable: YearsExperience
y = df_sal.iloc[:, 1:]  # dependent variable: Salary
```

`X` contains the experience column; `y` contains the salary column.

### Step 4 — Split into training and testing sets

The notebook uses an 80% training / 20% testing split:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)
```

The fixed `random_state=0` makes the split repeatable for the same data and library behavior.

The purpose of keeping a test set separate is to evaluate predictions on examples that were not used to fit the model.

### Step 5 — Fit the linear regression model

The notebook creates and fits a scikit-learn linear regression estimator:

```python
regressor = LinearRegression()
regressor.fit(X_train, y_train)
```

This step estimates the linear model's parameters from the training data.

### Step 6 — Predict values

After fitting, the notebook predicts salary values for both the training and testing inputs:

```python
y_pred_test = regressor.predict(X_test)
y_pred_train = regressor.predict(X_train)
```

- `y_pred_train` contains predictions for the training inputs.
- `y_pred_test` contains predictions for the held-out testing inputs.

Predictions for the test set can be compared with `y_test` to assess how well the model generalizes to those examples.

### Step 7 — Visualize the results

The notebook plots:

- The training-set observations and the regression line.
- The test-set observations and the regression line fitted from the training data.

These visualizations provide a qualitative way to compare observed salaries with the fitted linear trend.

### Step 8 — Inspect the coefficient and intercept

The notebook prints:

```python
print(f'Coefficient: {{regressor.coef_}}')
print(f'Intercept: {{regressor.intercept_}}')
```

For a simple linear model, the prediction can be written as:

```text
predicted_salary = coefficient * YearsExperience + intercept
```

- **Coefficient (slope):** how much the predicted salary changes for a one-unit increase in years of experience.
- **Intercept:** the model's predicted salary when years of experience is zero.

The notebook source contains the code to print these values, but the supplied notebook does not include the resulting numeric output in its saved cells. Therefore, this document does not state specific fitted coefficient or intercept values.

## 4. Connection to the Week 1 lecture

The lecture introduces a machine-learning model as a function that maps an input to an output and gives the linear-function form:

```text
f(x) = ax + b
```

The salary notebook applies this idea to a real-valued prediction task:

- Input `X`: years of experience.
- Output `y`: salary.
- Model: a fitted linear relationship.
- Training: estimate the coefficient and intercept from the training examples.
- Testing: compare predictions with salary values withheld from fitting.

The lecture also emphasizes that a model is trained by minimizing a cost/error function and that validation or testing is important before using a model to predict new values. The salary notebook's train/test split is an example of holding data back for evaluation.

## 5. Review questions

1. In the hand-held dataset, what does each `(x, y)` pair represent?
2. Why are the `x` and `y` vectors kept in the same order?
3. What does a scatter plot reveal before fitting a model?
4. In the salary dataset, which variable is the input and which is the target?
5. Why does the notebook split the data into training and testing sets?
6. What does `test_size=0.2` specify?
7. What does `random_state=0` do in the data-splitting call?
8. What does `LinearRegression().fit(X_train, y_train)` do?
9. What is the difference between `y_pred_train` and `y_pred_test`?
10. What do the coefficient and intercept mean in a simple linear model?
11. Why should test-set performance matter in addition to how closely the model fits its training data?
12. What evidence would you need before concluding that a straight line is an appropriate model for a dataset?

## 6. Source and scope notes

- `ml_0.0.1_training_data_list.txt` supplies the 20 coordinate pairs.
- `ml_0.0.1_training_data_vectors.txt` supplies the same values as `x` and `y` vectors.
- `Handheld linear regression data.png` visualizes the coordinate data and labels the axes `x` and `f(x)`.
- `Salary_Data.csv` supplies the experience/salary dataset.
- `simple_linear_regression.ipynb` supplies the notebook's code and explanatory Markdown cells.
- No external sources or extra model results have been added.
