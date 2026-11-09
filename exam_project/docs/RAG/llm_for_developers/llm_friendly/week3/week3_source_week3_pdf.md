<!-- studygraph:converted-source:v1 -->
# Week 3 — Week3 (pdf)

Source: [week3/Week3.pdf](../../source/week3/Week3.pdf).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

## Page 1

LLMs for 
Developers E26

Week 3

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 2

Agenda

[20 mins] Recap week 1
[10 mins] Break
[80 mins] Machine Learning
[10 mins] Break
[120 mins] Societal Aspects

11. september 2026
2

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 3

The value of being in a study group CANNOT be overestimated.

How are we doing

on groups?
‘A’, ‘B’, ‘C’, ‘D’, …

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 4

Important dates – again.

Fri 4 September: mandatory assignment 1 is released.

Tue 29 September: workshop & mandatory assignment 2 is released. Guest from ITU!

Thu 8 October: hand-in of mandatory assignment 1 + review one other assignment.

Thu 29 October: hand-in of Mandatory Assignment 2 + review one other assignment.

Fri 6 November: the project period starts.

Mon 14 December - ?: Exam

11. september 2026
4

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 5

Recap – week 1

“All models are wrong, but some are useful”

– George Box

11. september 2026
5

"Be the change that you wish to see in the world.”

– Mahatma Gandhi

Machine Learning

Societal Aspects

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 6

Machine Learning

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 7

11. september 2026
7

Predictive

Diagnostic

Descriptive

Prescriptive

Compactification…
… busy boil-down slide ... ☺

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 8

x = [1, 2, 3, 4]

f(x) = [1, 4, 9, 16]

Generally: A Machine Learning Model is a Function.

8

Function

f

Output
f(x)

Input

x

Remember, LLMs have billions of parameters!
And non-linear functions.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 9

❖In machine learning a model is trained, by minimizing an error function.

❖That trained model is then validated using a test data set.

The model can now be used to predict output values from new data.

❖This goes for all machine learning.

11. september 2026
‹#›

Point being…

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 10

Example embedding map from Nomic.

https://atlas.nomic.ai/map/nomic-text-embed-v1-5m-sample

https://static.nomic.ai/reports/2024_Nom
ic_Embed_Text_Technical_Report.pdf

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 11

Societal Aspects

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 12

We are still also looking at some of these 
societal aspects (SA) of the LLM revolution:

•
Ethics & Moral

•
Human Culture Drifts

•
Language and factuality drift

•
Copyrights & Legal Issues

•
Data physical residence

•
GDPR Considerations

•
Explainability

•
Hallucinations

•
LLM Security – prompt injections

•
LLM Energy Consumption

Small time case – but quite illustrative.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 13

Last week’s topics

Societal Aspects – a few tests of cloud LLMs. In prep for LLMs week 2.

Ambiguity (not so hard…)
In your groups: Construct two significantly different prompts that can provoke ambiguity. Run both against 
various LLMs (even Local ones!). Observe. Report response.
Hint: different tone, or language, but essentially ask the same question.

Hallucination (harder than I thought!)
In your groups: Construct a prompt with unreal content which can provoke hallucination. Run it against 
various LLMs, observe, report response.
Hint: invent something that does not exist. “Explain the principle underlying Relativistic Quantum Blockchains (RQBs).”

11. september 2026
‹#›

How’d it go?

Did you get to this part?

Let’s relate this to Prompt

Engineering!

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 14

Ambiguity, and worse yet, Hallucination of LLMs can inflict – sometimes even severely so – 
unintended societal discourse.

❖Ambiguity: In absence of validation / cross-validation of LLM responses to prompts,

acceptance of the response can lead to a distorting or diffusive effect on the user (or 
agentic system!)

❖Hallucination: can generate a new truth. Which cannot necessarily be corrected in post-

fact validation measures.

This leads us to the topic of misuse – even hacking – by deliberate Prompt Injection 
attempts, this week (Week 3).

11. september 2026
‹#›

Point being… Societal Aspects

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 15

11. september 2026
15

Take a 10 minute break.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 16

Machine Learning – week 3

“All models are wrong, but some are useful”

– George Box

11. september 2026
16

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 17

Paper exercise: 1 iteration.

=> Tolerance high

=> Error high

=> Accuracy low

Python exercise: 10+ iterations.

=> Tolerance = low

=> error low

=> accuracy = high

We trained a linear predictive machine learning model – linear regression.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 18

Our simple model from Week 1 is:

𝑓𝑥= 𝑎∙𝑥+ 𝑏

Two parameters, a and b, must be optimized, to best fit the data. Then our 
model will have predictive power! – remember…?

- BUT! How do we optimize?!  -- a and b can take on infinitely many values. 
- Let’s see what that actually means….

Only one set of a and b is the best one!!

11. september 2026
‹#›

Gradient Descent 1

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 19

‹#›

Gradient Descent 2

a = 0
b <> 0

a = ‘Inf’
b <> 0

a <> 0
b <> 0

Extreme cases of 
values of a and b.

… and a few good guesses…
… but which is the right one…?

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 20

Gradient Descent 3

Our simple model from Week 1 is:

𝑓𝑥= 𝑎∙𝑥+ 𝑏
Our N data points are:

𝑥𝑖, 𝑦𝑖
𝑖= {1, … 𝑁}

Our loss function becomes – remember – the (total) error:

𝐿𝑎, 𝑏= 1

𝑁෍

𝑖=1

𝑁

(𝑎∙𝑥𝑖+ 𝑏−𝑦𝑖)2

!! We must the a and b to match the data by looking for smallest value of L !!

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 21

Gradient Descent 4

𝐿𝒂, 𝒃= 1

𝑁෍

𝑖=1

𝑁

(𝒂∙𝑥𝑖+ 𝒃−𝑦𝑖)2

i)
We have a (Loss) function which is parabolic in 
two variables, a and b.

ii)
Make an initial guess for a and b.

iii)
Find the direction of steepest descent (the largest
slope).

iv)
Step-by-step we ”roll” downhill.

v)
… until convergence … and …

vi)
…SOLVED!

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 22

Model Training by Minimizing the Loss
Exercise 3.1

Gradient descent in Python, Scikit Learn, diabetes data.

11. september 2026
22

1. Get data: https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset
2. Get the Jupyter Notebook from Its Learning: gradient_descent_linear_regression.ipynb
3. Run the notebook in VS Code, or from Anaconda Navigator -> Jupyter Notebooks
4. Read the Notebook and try to understand the steps. Sections 4 and 5 are central!
5. Play with it, change parameters, especially the LEARNING_RATE.
6. Try to “break” the fitting by severely altering the LEARNING_RATE (btw 0.0 and 1.0).

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 23

11. september 2026
‹#›

Gradient Descent 5

You should see somethings like this

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 24

11. september 2026
‹#›

Gradient Descent 6

We change into K-fold cross validation, where we sample K batches of training data and validation 
data K times, at random, and make the fit(s). This gives K estimate(s) of slope and bias.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 25

Gradient Descent Last

•
For multidimensional parameter space, say, 
3D parameter space the Loss minimum is to 
be found in a volume rather than on a 
surface.

•
For even higher dimensions, say 700 billion 
dimensions, and non-linear functions, there is 
much much more than one minimum. We
now talk of “local” minima, and “global” 
minimum.

•
So in language models, there is by no means
one truth. Not mathematically, nor 
semantically, nor syntatically.

•
But we can get very close to a minimum by 
training for months and months at a time.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 26

Multiple local minima – Global maximum

• Non-linear functions of multiple 
parameters

• Also in extreme dimensionlity (LLMs)

• We may never find the “right” global 
minimum but end up in a local trough

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 27

Example embedding map from Nomic.

https://atlas.nomic.ai/map/nomic-text-embed-v1-5m-sample

https://static.nomic.ai/reports/2024_Nom
ic_Embed_Text_Technical_Report.pdf

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 28

We will begin to look at language modeling next time 
(week 5)

11. september 2026
28

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 29

Text Corpora and Embeddings
Exercise 3.2

Voluntary prep for week 5, you can download ‘corpus.txt’ and play around.

11. september 2026
29

1. Get the data from ItsLearning: ‘corpus.txt’
2. Get the Jupyter Notebook from Its Learning: ’train_embeddings.ipynb’
3. Run the notebook in VS Code, or from Anaconda Navigator -> Jupyter Notebooks
4. Read the Notebook and try to understand the steps. Sections 4 and 5 are central!
5. Play with it, change parameters, especially the LEARNING_RATE.
6. Try to “break” the fitting by severely altering the LEARNING_RATE (btw 0.0 and 1.0).

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 30

11. september 2026
30

Take a 15 minute break.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 31

Societal Aspects – week 3

"Be the change that you wish to see in the world.”

– Mahatma Gandhi

11. september 2026
31

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 32

Ambiguity, and worse yet, Hallucination of LLMs can inflict – sometimes even severely so – 
unintended societal discourse.

❖Ambiguity: In absence of validation / cross-validation of LLM responses to prompts,

acceptance of the response can lead to a distorting or diffusive effect on the user (or 
agentic system!)

❖Hallucination: can generate a new truth. Which cannot necessarily be corrected in post-

fact validation measures.

This leads us to the topic of misuse – even hacking – by deliberate Prompt Injection 
attempts, this week (Week 3).

11. september 2026
‹#›

Point being… Societal Aspects

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 33

Ambiguity, and worse yet, Hallucination of LLMs can inflict – sometimes even severely so – 
unintended societal discourse.

❖Ambiguity: In absence of validation / cross-validation of LLM responses to prompts,

acceptance of the response can lead to a distorting or diffusive effect on the user (or 
agentic system!)

❖Hallucination: can generate a new truth. Which cannot necessarily be corrected in post-

fact validation measures.

❖Prompt Injection: what is that? Is it real, is it dangerous? Added this week (Week 3).

11. september 2026
‹#›

Point being… Societal Aspects

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 34

4 Ts -- Prompt Engineering

(from week 2)

Trait

Task

11. september 2026
‹#›

Tone
 Target

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 35

Prompt Injection I

Developer instructions
Untrusted content

… ONE token stream …

Output / action — may follow either source

No separation survives the concatenation step.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 36

Two Ways to Inject

DIRECT

Typed straight into the chat by the attacker.

INDIRECT

Hidden in content the model reads later — the real user never sees it.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 37

11. september 2026
‹#›

Week 3 SA topical slides

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 38

Exercise 3.3

• We start now. In your groups.

1) Work in classroom, in groups.
2) Continue at home – loadbalance in your group.
3) Email slides + synopsis to jatr@ek.dk

• We finish Friday 25th September 
(week 5).

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 39

11. september 2026
39

LLMs for Developers next: week 5

• Machine Learning
• Societal Aspects

TBD
TBD

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.
