<!-- studygraph:converted-source:v1 -->
# Week 9 — Week9 (pdf)

Source: [week9/Week9.pdf](../../source/week9/Week9.pdf).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

## Page 1

LLMs for 
Developers E26
Week 9

My own brief reflection at my biketrip before work (traffic 
secure, at the stoplight etc ;-) ): “Is Software development and 
data analysis important?” 
-- Is distributed computing and local services important?

•
SETI@Home – whence. Just for exemplification of distributed computing, nothing else.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 2

Machine
Learning Cp
ter
0.0.1
22
7
r
8
4,2) = (x2—1)?2 + (y2-1)2 + (22—1)2 + ax + ay + a_zz+ 0:
i
x:
-0.5390244
y: 1.202439
ler
rile?
value: 0.01390263
7
VA
bila
|
s
mi
|
4
s?
"
;
~Ls
z
9
“1
A
ie
70.5
É
f
1
;
é
0
6
y
>
%
0.5
q

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 3

Important dates – again.

Fri 4 September: mandatory assignment 1 is released.

Tue 29 September: workshop & mandatory assignment 2 is released. Guest from ITU!

Thu 8 October: hand-in of mandatory assignment 1 + review one other assignment.

Thu 29 October: hand-in of Mandatory Assignment 2 + review one other assignment.

Fri 6 November: the project period starts.

Mon 14 December - ?: Exam

23. oktober 2026
3

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 4

Recap

“All models are wrong, but some are useful”

– George Box

23. oktober 2026
4

"Be the change that you wish to see in the world.”

– Mahatma Gandhi

Machine Learning

Societal Aspects

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 5

Societal Aspects

Not for today. But we’re working on that – because it is central.

For now? Let’s tone this down for the course of today.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 6

Machine Learning

• “All models are wrong, but some are useful”

• – George Box

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 7

23. oktober 2026
7

Predictive

Diagnostic

Descriptive

Prescriptive

Compactification…
… busy boil-down slide ... J

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

vIn machine learning a model is trained, by minimizing an error function.

vThat trained model is then validated using a test data set.

The model can now be used to predict output values from new data.

vThis goes for all machine learning.

23. oktober 2026
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

15 mins break.

23. oktober 2026
11

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 12

We trained a linear predictive machine learning model – linear regression.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 13

Our simple model from Week 1 is:

𝑓𝑥= 𝑎% 𝑥+ 𝑏

Two parameters, a and b, must be optimized, to best fit the data. Then our 
model may have predictive power. – remember…?

- BUT! How do we optimize?!  -- a and b can take on infinitely many values. 
- Let’s see what that actually means….

Only one set of a and b is the best one!!

23. oktober 2026
‹#›

Gradient Descent 1

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 14

‹#›

Gradient Descent 2

Extreme cases of 
values of a and b.

… and a few good guesses…
… but which is the right one…?

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 15

Gradient Descent 3

Our simple model from Week 1 is:

𝑓𝑥= 𝑎% 𝑥+ 𝑏
Our N data points are:

𝑥!, 𝑦!
𝑖= {1, … 𝑁}

Our loss function becomes – remember – the (total) error:

𝐿𝑎, 𝑏= 1

𝑁1

!"#

$

(𝑎% 𝑥! + 𝑏−𝑦!)%

!! We make a and b match the data best possible by looking for smallest value of L !!

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 16

Gradient Descent 4

𝐿(𝒂, 𝒃) = 1

𝑁1

!"#

$

(𝒂% 𝑥! + 𝒃−𝑦!)%

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

## Page 17

23. oktober 2026
‹#›

Gradient Descent 5

You should see somethings like this

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 18

23. oktober 2026
‹#›

Gradient Descent 6

We change into K-fold cross validation, where we sample with K==5, batches of training data and 
validation data five times, at random, and make the fit(s). This gives five estimate(s) of slope and bias.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 19

Multiple local minima – Global maximum

• Non-linear functions of multiple 
parameters

• Also in extreme dimensionlity (LLMs)

• We may never find the “right” global 
minimum but end up in a local trough – 
where our LLMs speak dialect tongue.

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 20

15 mins break.

23. oktober 2026
20

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 21

Where are we going 
with this?

• Into the unknown, one might state.

• L-LLMs are not just useful – they may be 
future.

23. oktober 2026
‹#›

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 22

15 mins break.

23. oktober 2026
22

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.

## Page 23

Where do we 
want to go?

Look to any ML course on the EK, or the widely spread 
internet… 
We would have liked to continue into Neural networks.

We may look into neural networks, and why they learn so 
efficiently, perhaps in the last LLM workshop of this semester. 
If time serves.

Now, more importantly, the exam project approaches.

:-)

> Visual content: this page contains images or graphics. The meaning of the diagrams and formulas has not been verified automatically.
