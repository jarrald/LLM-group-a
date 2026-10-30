# LLMs for Developers E26 — Week 3 Overview

**Primary source:** `Week3.pdf` (39 slides; 11 September 2026)  
**Related materials:** ambiguity and semantic-drift papers, hallucination papers, prompt-injection/security papers, `HandInPromptingArtifacts(1).pdf`, `Web Resources.md`, and accompanying Jupyter notebooks.

> This is an organized study guide for retrieval-augmented generation (RAG). It distinguishes concepts explicitly presented in the lecture from summaries of related research papers and from student assignment instructions.

## Week 3 at a glance

The lecture combines two strands:

1. **Machine learning:** gradient descent, loss functions, parameter fitting, learning rate, cross-validation, local and global minima, and a preview of text embeddings.
2. **Societal aspects of LLMs:** ambiguity and semantic drift, hallucinations, prompt injection, and a group literature-review assignment.

The lecture is dated **11 September 2026**. It refers to Week 5 as the next session for further language-modelling topics.

## 1. Machine-learning recap

The slides revisit the idea that a machine-learning model is a function mapping input to output. The lecture gives the example:

```text
x = [1, 2, 3, 4]
f(x) = [1, 4, 9, 16]
```

The example maps each input to its square. It illustrates that models can represent non-linear functions and that LLMs have very large numbers of parameters.

The lecture's general training sequence is:

1. Train a model by minimizing an error or loss function.
2. Validate the trained model using held-out data.
3. Use the model to predict outputs for new data.

The lecture reiterates George Box's quotation: “All models are wrong, but some are useful.”

## 2. Gradient descent

The Week 1 linear model is revisited:

```text
f(x) = a * x + b
```

The two parameters are:

- `a`: slope
- `b`: intercept or bias

Training means finding values of `a` and `b` that fit the data well. Because there are infinitely many possible parameter values, the model needs an optimization procedure.

The lecture defines a mean squared error-style loss for `N` data points:

\[
L(a,b) = \frac{1}{N}\sum_{i=1}^{N}(a x_i + b - y_i)^2
\]

The goal is to find parameters that make `L(a,b)` small.

The slides describe gradient descent as:

1. Choose an initial parameter guess.
2. Find the direction of steepest descent of the loss.
3. Update parameters in small steps downhill.
4. Repeat until the procedure converges or a stopping condition is reached.

The lecture's diagrams describe a loss surface that is parabolic in two parameters for the simple linear-regression example. More complicated models have higher-dimensional and often non-convex loss landscapes.

## 3. Learning rate and practical fitting

The lecture assigns Exercise 3.1 using the scikit-learn diabetes dataset and a supplied notebook, `gradient_descent_linear_regression.ipynb`.

Students are asked to:

- Get the diabetes dataset from scikit-learn.
- Open the notebook in VS Code or Jupyter through Anaconda Navigator.
- Read the notebook, paying particular attention to sections 4 and 5.
- Change parameters, especially `LEARNING_RATE`.
- Try to break fitting by choosing extreme learning-rate values between 0.0 and 1.0.

The learning rate controls the size of each optimization step. If steps are too small, optimization may progress slowly; if too large, updates may overshoot useful regions or fail to converge. The exercise asks students to observe this behavior rather than supplying a fixed result.

## 4. Testing and cross-validation

The lecture introduces K-fold cross-validation. Data is divided into `K` folds, and training/validation is repeated so that each fold can be used for validation in turn. This produces multiple estimates of model performance and, in the simple regression framing, potentially multiple estimates of slope and bias.

Cross-validation helps assess whether results depend too strongly on a particular train/test split. It is distinct from using a final untouched test set for a final estimate of generalization.

## 5. Local minima and large models

The lecture explains that a loss function with multiple parameters has a multi-dimensional optimization landscape. In higher-dimensional, non-linear models, the loss can have many local minima as well as a global minimum.

- **Global minimum:** the lowest loss over the entire parameter space.
- **Local minimum:** a point whose loss is lower than nearby points, but not necessarily the lowest possible overall.

The slides use LLMs as an example of models with extremely high-dimensional parameter spaces. The lecture's conceptual point is that optimization does not imply a single mathematically, semantically, or syntactically perfect “truth.” The exact training behavior of any particular LLM depends on its architecture, objective, data, and optimization process.

## 6. Embeddings and upcoming language modelling

The lecture references a Nomic text-embedding map and its technical report:

- Interactive map: https://atlas.nomic.ai/map/nomic-text-embed-v1-5m-sample
- Technical report: https://static.nomic.ai/reports/2024_Nomic_Embed_Text_Technical_Report.pdf

Exercise 3.2 is optional preparation for Week 5. Students are asked to use `corpus.txt` and `train_embeddings.ipynb`, inspect the notebook, change parameters—especially the learning rate—and observe how extreme values affect fitting.

An embedding maps text (such as tokens or passages) into numerical vectors. An embedding map can visualize relationships among vectors, but the plotted geometry is a representation produced by a model and visualization process, not a literal map of meaning.

## 7. Societal aspects: ambiguity, hallucination, prompt injection

The lecture warns that ambiguous prompts and hallucinated answers can distort a user's understanding or an agentic system's decisions when responses are accepted without validation or cross-validation. It describes hallucination as potentially creating a “new truth” that may persist even after later correction.

The lecture then introduces deliberate prompt injection as a form of misuse or attack.

### Ambiguity and semantic drift

Ambiguity occurs when a prompt or answer can reasonably be interpreted in more than one way. Semantic drift refers to meaning or the direction of a conversation changing over successive turns. The related literature explores how multi-turn interactions can fail when models make assumptions early and then fail to recover.

### Hallucination

A hallucination is an output that presents fabricated, unsupported, or unverifiable information as though it were factual. Fluent writing is not proof of factual correctness. Verification, source checking, and calibrated uncertainty are important.

### Prompt injection

The Week 3 slides explain that developer instructions and untrusted content can be concatenated into a single token stream. The model may not reliably preserve the intended trust boundary merely because the application developer intended one.

Two broad forms are identified:

- **Direct prompt injection:** an attacker puts malicious instructions directly into the chat.
- **Indirect prompt injection:** malicious instructions are hidden in content the model later reads, such as a document or web page; the user may not see those instructions.

This is particularly relevant to retrieval-augmented generation: retrieved documents are evidence to use for answering, not trusted instructions that should override system or developer policy.

## 8. Group literature-review assignment — Exercise 3.3

The handout is titled **“Literature Review on LLM Prompting and Societal Implications.”** It asks groups to search and evaluate existing literature, rather than conduct new experiments.

The project investigates how prompting can affect the quality, reliability, and societal impact of AI-generated information through three challenges:

1. Ambiguity and semantic drift.
2. Response hallucination.
3. Prompt injection.

The assignment asks students to explain the concepts, synthesize evidence from literature in the context of LLM training and inference/prompting, discuss societal implications, and communicate findings as if reporting from an IT department to company leadership (CEO, CSO, and CHRO).

### Deliverables

- One PowerPoint presentation per group: maximum 6 slides and maximum 10 minutes.
- One synopsis per group: maximum 6 pages plus cover page.
- The handout lists the per-group hand-in as Thursday evening of Week 5, **24 September**, by email to `jatr@ek.dk`.
- The handout says the group should finish on Friday 25 September (Week 5).
- Groups of 4–6 students are suggested. The handout estimates approximately 0.5 FTE week per group, around 23 hours for a group of five.
- AI may be used cautiously, but students must be able to account for and discuss their deliberations.

**Date note:** the handout's stated weekday/date combination and the lecture's course dates should be confirmed with the instructor if the deadline is operationally important.

## 9. Week 3 review questions

1. What does it mean to train a model by minimizing a loss function?
2. What are slope and intercept in `f(x) = a*x + b`?
3. Why does gradient descent need an initial guess?
4. What role does the learning rate play?
5. What can happen if the learning rate is too high or too low?
6. What is the difference between a local minimum and a global minimum?
7. How does K-fold cross-validation differ from a single train/test split?
8. What are embeddings, and what does an embedding map visualize?
9. How can ambiguous instructions lead to incorrect user conclusions?
10. What is the difference between a hallucination and an ambiguous response?
11. What is the difference between direct and indirect prompt injection?
12. Why should retrieved documents be treated as untrusted data rather than instructions?
13. What are the three topics in the Week 3 literature-review assignment?

## Source scope

This overview combines the Week 3 lecture and the assignment handout. Related papers are summarized in separate files to keep RAG chunks focused. The notebook files are described at the workflow level; numerical outputs should be taken from actually running the supplied notebooks, not inferred from the lecture slides.
