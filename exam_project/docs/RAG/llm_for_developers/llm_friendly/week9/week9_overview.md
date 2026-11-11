# Week 9 — Parameter fitting, gradient descent and validation

Sources: `source/week9/Week9.pdf`, 23 pages, and three short animations. See the [PDF text](week9_source_week9_pdf.md) and the separate video descriptions named `week9_source_*_mp4.md`. The slides are dated 23 October 2026; dates and plans in them are historical source information.

## A model as a function

The slides repeat that a model turns input into output. The example `x = [1, 2, 3, 4]` and `f(x) = [1, 4, 9, 16]` illustrates a non-linear function. A model is trained by minimising an error function, evaluated on data outside the training set and then used for predictions.

## Linear model and loss

The simple model is `f(x) = a*x + b`, where `a` is the slope and `b` is the bias/intercept. Visual inspection of PDF page 15 confirms this formula and the following mean squared loss:

\[
L(a,b) = \frac{1}{N}\sum_{i=1}^{N}(a x_i + b - y_i)^2
\]

The formulas are written readably here because automatic PDF extraction mixes some mathematical symbols and their positions. The remaining PDF formulas have not all been checked manually.

## Gradient descent and initialisation

The slides describe an initial parameter guess, the direction of the greatest decrease in the loss, and small updates until convergence. The animation `gradient_descent_fit.mp4` shows the changing regression line together with the training and validation loss. The validation points are only shown later in the animation, which separates fitting from evaluation on held-out data.

## K-fold cross-validation

The material uses five folds and compares estimates of slope and bias. The animation `kfold_fit_evolution_dual_init.mp4` shows five coloured folds with two initialisations: solid and dashed lines. Loss across folds is shown on a logarithmic scale. The description of the animation is visual observation, not a newly reproduced training experiment.

## Non-linear models and neural networks

The slides discuss local and global minima in functions with many parameters. The planned continuation towards neural networks is described as a possibility, not as something the whole course has already covered. The CNN animation does, however, show an example with three input characters, convolutional feature maps and three softmax output heads. It is explained separately in the media notes.

## Review questions

1. What is optimised in the linear model?
2. What is the difference between training loss and validation loss?
3. What do the two initialisations in the fold animation show?
4. Why can per-character accuracy and per-character-triple accuracy differ?
5. Why is a local minimum not a guarantee of truth in an LLM answer?