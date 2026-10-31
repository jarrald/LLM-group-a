<!-- studygraph:converted-source:v1 -->
# Uge 9 — Week9 (pdf)

Kilde: [week9/Week9.pdf](../../source/week9/Week9.pdf).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Side 1

LLMs for 
Developers E26
Week 9

My own brief reflection at my biketrip before work (traffic 
secure, at the stoplight etc ;-) ): “Is Software development and 
data analysis important?” 
-- Is distributed computing and local services important?

•
SETI@Home – whence. Just for exemplification of distributed computing, nothing else.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 2

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 3

Vigtige datoer – igen.

Fre 4. september: mandatory assignment 1 udleveres.

Tir 29. september: workshop & mandatory assignment 2 udleveres. Gæst fra ITU!

Tor 8. oktober: aflevering mandatory assignment 1 + review one other assignment.

Tor 29. oktober: aflevering Mandatory Assignment 2 + review one other assignment.

Fre 6. november: projektforløb starter.

Man 14. december - ?: Eksamen

23. oktober 2026
3

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 4

Recap

“All models are wrong, but some are useful”

– George Box

23. oktober 2026
4

"Be the change that you wish to see in the world.”

– Mahatma Gandhi

Machine Learning

Societal Aspects

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 5

Societal Aspects

Not for today. But we’re working on that – because it is central.

For now? Let’s tone this down for the course of today.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 6

Machine Learning

• “All models are wrong, but some are useful”

• – George Box

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 7

23. oktober 2026
7

Predictive

Diagnostic

Descriptive

Prescriptive

Compactification…
… busy boil-down slide ... J

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 8

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 9

vIn machine learning a model is trained, by minimizing an error function.

vThat trained model is then validated using a test data set.

The model can now be used to predict output values from new data.

vThis goes for all machine learning.

23. oktober 2026
‹#›

Point being…

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 10

Example embedding map from Nomic.

https://atlas.nomic.ai/map/nomic-text-embed-v1-5m-sample

https://static.nomic.ai/reports/2024_Nom
ic_Embed_Text_Technical_Report.pdf

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 11

15 mins break.

23. oktober 2026
11

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 12

We trained a linear predictive machine learning model – linear regression.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 13

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 14

‹#›

Gradient Descent 2

Extreme cases of 
values of a and b.

… and a few good guesses…
… but which is the right one…?

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 15

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 16

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 17

23. oktober 2026
‹#›

Gradient Descent 5

You should see somethings like this

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 18

23. oktober 2026
‹#›

Gradient Descent 6

We change into K-fold cross validation, where we sample with K==5, batches of training data and 
validation data five times, at random, and make the fit(s). This gives five estimate(s) of slope and bias.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 19

Multiple local minima – Global maximum

• Non-linear functions of multiple 
parameters

• Also in extreme dimensionlity (LLMs)

• We may never find the “right” global 
minimum but end up in a local trough – 
where our LLMs speak dialect tongue.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 20

15 mins break.

23. oktober 2026
20

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 21

Where are we going 
with this?

• Into the unknown, one might state.

• L-LLMs are not just useful – they may be 
future.

23. oktober 2026
‹#›

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 22

15 mins break.

23. oktober 2026
22

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 23

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

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.
