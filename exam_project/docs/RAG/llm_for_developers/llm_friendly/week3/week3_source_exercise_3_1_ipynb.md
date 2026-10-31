<!-- studygraph:converted-source:v1 -->
# Uge 3 — Exercise_3.1 (ipynb)

Kilde: [week3/Exercise_3.1.ipynb](../../source/week3/Exercise_3.1.ipynb).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

Kildeceller er bevaret i rækkefølge. Koden er ikke kørt. Gemte outputs, billeder og kørselsnumre er udeladt; der tilføjes ingen forsøgsresultater.

## Celle 1 — markdown

### Simple Linear Regression via Gradient Descent

Fits a one-variable model **f(x) = a·x + b** using batch gradient descent, with an explicit
training / validation split — implemented from scratch rather than calling scikit-learn's
closed-form `LinearRegression` solver.

**Dataset.** scikit-learn's built-in *diabetes* dataset. We use a single feature, Body Mass Index
(BMI), to predict a quantitative measure of disease progression one year after baseline. It ships
with the package, so there is no download and no Kaggle account needed.

**What this notebook produces**

| Output | Where |
|---|---|
| Two-panel animation of the fitting process | inline, **and** `outputs/gradient_descent_fit.mp4` |
| Final fit figure (train/validation split) | inline, **and** `outputs/final_fit.png` |
| Training/validation loss curve | inline, **and** `outputs/loss_curve.png` |
| Final `a`, `b`, MSE and R² | inline, **and** `outputs/metrics.txt` |

> **Differences from the `.py` version.** Three things had to change for a notebook:
> 1. `matplotlib.use("Agg")` is dropped — we want figures inline. The animation is rendered with
>    the JavaScript writer so it plays in the browser.
> 2. `__file__` does not exist in a notebook, so the output directory is resolved from the
>    current working directory instead.
> 3. Figures are *not* closed with `plt.close()` after saving, so they display inline as well.
>
> The numerical results are identical.

## Celle 2 — markdown

#### 0. Setup, reproducibility and output directory

## Celle 3 — code

### Kildelinjer 1–20

```python
# %pip install numpy matplotlib scikit-learn        # uncomment if needed

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML, display

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

%matplotlib inline

RNG_SEED = 42
np.random.seed(RNG_SEED)

# A notebook has no __file__, so anchor the output directory to the working directory.
OUT_DIR = os.path.join(os.getcwd(), "outputs")
os.makedirs(OUT_DIR, exist_ok=True)
print("Outputs will be written to:", OUT_DIR)
```

## Celle 4 — markdown

#### 1. Data collection

## Celle 5 — code

### Kildelinjer 1–9

```python
data = load_diabetes()
feature_index = list(data.feature_names).index("bmi")

x_raw = data.data[:, feature_index]   # independent variable: BMI
y_raw = data.target                   # dependent variable: disease progression

print(f"{x_raw.shape[0]} samples")
print(f"x (BMI)    range: {x_raw.min():.4f} to {x_raw.max():.4f}")
print(f"y (target) range: {y_raw.min():.1f} to {y_raw.max():.1f}")
```

## Celle 6 — markdown

#### 2. Split into training and validation sets (80% / 20%)

The split happens **before** any scaling, so the scaling statistics are computed only from the
training data — no leakage from validation into training.

## Celle 7 — code

### Kildelinjer 1–6

```python
x_train_raw, x_val_raw, y_train_raw, y_val_raw = train_test_split(
    x_raw, y_raw, test_size=0.2, random_state=RNG_SEED
)

print(f"training:   {x_train_raw.shape[0]} samples")
print(f"validation: {x_val_raw.shape[0]} samples")
```

## Celle 8 — markdown

#### 3. Standardization

Gradient descent on raw, unscaled features converges very slowly (or diverges) when `x` and `y`
live on very different numeric scales — here `x ≈ 0.06` while `y ≈ 150`.

We standardize both using **training statistics only**, run gradient descent in standardized
space, and convert the learned `(a, b)` back into original units at the end so that
`f(x) = a·x + b` is directly usable on raw BMI values.

## Celle 9 — code

### Kildelinjer 1–10

```python
x_mean, x_std = x_train_raw.mean(), x_train_raw.std()
y_mean, y_std = y_train_raw.mean(), y_train_raw.std()

x_train = (x_train_raw - x_mean) / x_std
x_val   = (x_val_raw   - x_mean) / x_std
y_train = (y_train_raw - y_mean) / y_std
y_val   = (y_val_raw   - y_mean) / y_std

print(f"x_train mean {x_train.mean():+.3e}   std {x_train.std():.4f}")
print(f"y_train mean {y_train.mean():+.3e}   std {y_train.std():.4f}")
```

## Celle 10 — markdown

#### 4. Model, loss and gradients

$$f(x) = a\,x + b \qquad\qquad L(a,b) = \frac{1}{n}\sum_{i=1}^{n}\left(a\,x_i + b - y_i\right)^2$$

with partial derivatives

$$\frac{\partial L}{\partial a} = \frac{2}{n}\sum_i (a x_i + b - y_i)\,x_i
\qquad\qquad
\frac{\partial L}{\partial b} = \frac{2}{n}\sum_i (a x_i + b - y_i)$$

## Celle 11 — code

### Kildelinjer 1–15

```python
def predict(a, b, x):
    return a * x + b


def mse(a, b, x, y):
    err = predict(a, b, x) - y
    return np.mean(err ** 2)


def gradients(a, b, x, y):
    n = x.shape[0]
    err = predict(a, b, x) - y
    da = (2.0 / n) * np.sum(err * x)
    db = (2.0 / n) * np.sum(err)
    return da, db
```

## Celle 12 — markdown

#### 5. Training cycle

Validation is tracked alongside training at every iteration: at each step we also *evaluate*, but
never *fit on*, the validation set.

**A note on step size.** A gradient-descent update `a -= dt * dL/da` plays the same role as a time
step `dt` in the discretization of the continuous gradient-flow ODE `da/dt = -dL/da`. The step used
here is ten times smaller than a "natural" choice, specifically so the early, fast-changing part of
the fit is stretched over many more iterations — and therefore many more animation frames — instead
of being over in a handful of steps. Because the step is 10× smaller, training runs for 500
iterations so the fit still has room to converge.

## Celle 13 — code

### Kildelinjer 1–26

```python
LEARNING_RATE = 0.01   # dt_new = 0.1 * dt_old  (dt_old was 0.1)
N_ITERS = 500          # end after 500 dt_new steps

a, b = 0.0, 0.0        # initial guess (standardized space)

history_a = np.zeros(N_ITERS + 1)
history_b = np.zeros(N_ITERS + 1)
history_train_loss = np.zeros(N_ITERS + 1)
history_val_loss = np.zeros(N_ITERS + 1)

history_a[0], history_b[0] = a, b
history_train_loss[0] = mse(a, b, x_train, y_train)
history_val_loss[0]   = mse(a, b, x_val, y_val)

for i in range(1, N_ITERS + 1):
    da, db = gradients(a, b, x_train, y_train)
    a -= LEARNING_RATE * da
    b -= LEARNING_RATE * db

    history_a[i] = a
    history_b[i] = b
    history_train_loss[i] = mse(a, b, x_train, y_train)
    history_val_loss[i]   = mse(a, b, x_val, y_val)

print(f"Finished training after {N_ITERS} iterations.")
print(f"Final (standardized-space) params: a={a:.4f}, b={b:.4f}")
```

## Celle 14 — markdown

#### 6. Convert back to original units

With $x_{\rm std} = (x - \bar{x})/s_x$ and $y_{\rm std} = (y - \bar{y})/s_y$:

$$y = s_y\left(a\,\frac{x - \bar{x}}{s_x} + b\right) + \bar{y}
    = \underbrace{\frac{s_y\,a}{s_x}}_{a_{\rm final}} x
    + \underbrace{\bar{y} + s_y b - \frac{s_y a \bar{x}}{s_x}}_{b_{\rm final}}$$

## Celle 15 — code

### Kildelinjer 1–8

```python
a_final = a * (y_std / x_std)
b_final = y_mean + y_std * b - a_final * x_mean

print(f"Final model in ORIGINAL units:  f(x) = {a_final:.4f} * x + {b_final:.4f}")

# Per-iteration record of (a, b) in ORIGINAL units, for the animation's left panel.
history_a_orig = history_a * (y_std / x_std)
history_b_orig = y_mean + y_std * history_b - history_a_orig * x_mean
```

## Celle 16 — markdown

#### 7. Final metrics

## Celle 17 — code

### Kildelinjer 1–25

```python
def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    return 1 - ss_res / ss_tot


y_train_pred_final = predict(a_final, b_final, x_train_raw)
y_val_pred_final   = predict(a_final, b_final, x_val_raw)

train_mse_final = np.mean((y_train_pred_final - y_train_raw) ** 2)
val_mse_final   = np.mean((y_val_pred_final   - y_val_raw) ** 2)
train_r2_final  = r2_score(y_train_raw, y_train_pred_final)
val_r2_final    = r2_score(y_val_raw,   y_val_pred_final)

metrics_path = os.path.join(OUT_DIR, "metrics.txt")
with open(metrics_path, "w") as f:
    f.write("Simple Linear Regression via Gradient Descent\n")
    f.write("================================================\n")
    f.write("Feature (x): BMI   Target (y): disease progression\n")
    f.write(f"Learning rate: {LEARNING_RATE}   Iterations: {N_ITERS}\n\n")
    f.write(f"Fitted model:  f(x) = {a_final:.4f} * x + {b_final:.4f}\n\n")
    f.write(f"Training set  -> MSE: {train_mse_final:.3f}   R^2: {train_r2_final:.4f}\n")
    f.write(f"Validation set -> MSE: {val_mse_final:.3f}   R^2: {val_r2_final:.4f}\n")

print(open(metrics_path).read())
```

## Celle 18 — markdown

#### 8. Final fit

Training and validation points are drawn with a different colour **and** a different marker.

## Celle 19 — code

### Kildelinjer 1–19

```python
fig_final, ax_final = plt.subplots(figsize=(7, 5))
ax_final.scatter(x_train_raw, y_train_raw, color="lightcoral", marker="o",
                 label="Training data", alpha=0.8, edgecolor="white", linewidth=0.5)
ax_final.scatter(x_val_raw, y_val_raw, color="steelblue", marker="^",
                 label="Validation data", alpha=0.9, edgecolor="white", linewidth=0.5)

x_line = np.linspace(x_raw.min(), x_raw.max(), 100)
ax_final.plot(x_line, predict(a_final, b_final, x_line), color="firebrick",
              linewidth=2, label=f"Fit: f(x) = {a_final:.1f}x + {b_final:.1f}")

ax_final.set_title("Disease Progression vs BMI - Gradient Descent Fit")
ax_final.set_xlabel("BMI (standardized input feature)")
ax_final.set_ylabel("Disease progression (target)")
ax_final.legend(loc="best", facecolor="white")
ax_final.spines["top"].set_visible(False)
ax_final.spines["right"].set_visible(False)
fig_final.tight_layout()
fig_final.savefig(os.path.join(OUT_DIR, "final_fit.png"), dpi=150)
plt.show()
```

## Celle 20 — markdown

#### 9. Loss curve

## Celle 21 — code

### Kildelinjer 1–12

```python
fig_loss, ax_loss = plt.subplots(figsize=(7, 5))
ax_loss.plot(history_train_loss, color="firebrick", label="Training loss")
ax_loss.plot(history_val_loss, color="steelblue", label="Validation loss")
ax_loss.set_title("Loss (MSE, standardized space) vs. Iteration")
ax_loss.set_xlabel("Iteration")
ax_loss.set_ylabel("MSE")
ax_loss.legend(loc="best", facecolor="white")
ax_loss.spines["top"].set_visible(False)
ax_loss.spines["right"].set_visible(False)
fig_loss.tight_layout()
fig_loss.savefig(os.path.join(OUT_DIR, "loss_curve.png"), dpi=150)
plt.show()
```

## Celle 22 — markdown

#### 10. Animation

Two panels:

* **left** — the data plus the current regression line, evolving over iterations
* **right** — training and validation loss curves, drawn live

The validation points are deliberately withheld from the left panel until iteration 250, then
revealed — like a held-out check — rather than shown from frame one.

The figure is built with `plt.ioff()` so the static first frame is not also displayed above the
animation.

## Celle 23 — code

### Kildelinjer 1–45

```python
N_FRAMES = 150
frame_iters = np.unique(
    np.linspace(0, N_ITERS, N_FRAMES).astype(int)
)  # sample iterations evenly (gradient descent moves fastest early on)

REVEAL_VAL_ITER = 250   # validation points appear from this iteration onwards

plt.ioff()   # don't display the bare figure; we only want the animation below
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# --- left panel setup ---
ax1.scatter(x_train_raw, y_train_raw, color="lightcoral", marker="o",
            label="Training data", alpha=0.8, edgecolor="white", linewidth=0.5, zorder=2)
val_scatter = ax1.scatter(x_val_raw, y_val_raw, color="steelblue", marker="^",
                          label="Validation data", alpha=0.9, edgecolor="white",
                          linewidth=0.5, zorder=2)
val_scatter.set_visible(False)  # hidden until REVEAL_VAL_ITER
line_plot, = ax1.plot([], [], color="firebrick", linewidth=2, zorder=3, label="Current fit")
ax1.set_xlim(x_raw.min() - 0.02, x_raw.max() + 0.02)
ax1.set_ylim(y_raw.min() - 20, y_raw.max() + 20)
ax1.set_title("Fitting f(x) = a*x + b")
ax1.set_xlabel("BMI (standardized input feature)")
ax1.set_ylabel("Disease progression (target)")
ax1.legend(loc="upper left", facecolor="white", fontsize=9)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
iter_text = ax1.text(0.98, 0.03, "", transform=ax1.transAxes, ha="right", va="bottom",
                     fontsize=10, family="monospace")

# --- right panel setup ---
train_loss_plot, = ax2.plot([], [], color="firebrick", label="Training loss")
val_loss_plot,   = ax2.plot([], [], color="steelblue", label="Validation loss")
ax2.set_xlim(0, N_ITERS)
ax2.set_ylim(0, max(history_train_loss.max(), history_val_loss.max()) * 1.05)
ax2.set_title("Loss vs. Iteration")
ax2.set_xlabel("Iteration")
ax2.set_ylabel("MSE (standardized space)")
ax2.legend(loc="upper right", facecolor="white")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

fig.tight_layout()


def init():
```

### Kildelinjer 46–83

```python
    line_plot.set_data([], [])
    train_loss_plot.set_data([], [])
    val_loss_plot.set_data([], [])
    iter_text.set_text("")
    val_scatter.set_visible(False)
    return line_plot, train_loss_plot, val_loss_plot, iter_text, val_scatter


def animate(frame_idx):
    it = frame_iters[frame_idx]
    a_i, b_i = history_a_orig[it], history_b_orig[it]

    line_plot.set_data(x_line, predict(a_i, b_i, x_line))

    xs = np.arange(0, it + 1)
    train_loss_plot.set_data(xs, history_train_loss[: it + 1])
    val_loss_plot.set_data(xs, history_val_loss[: it + 1])

    revealed = it >= REVEAL_VAL_ITER
    val_scatter.set_visible(revealed)

    status = f"val revealed (iter>={REVEAL_VAL_ITER})" if revealed else "val hidden"
    iter_text.set_text(
        f"iter {it:3d}/{N_ITERS}\n"
        f"a={a_i:6.2f}  b={b_i:6.2f}\n"
        f"train MSE={history_train_loss[it]:.4f}\n"
        f"val   MSE={history_val_loss[it]:.4f}\n"
        f"{status}"
    )
    return line_plot, train_loss_plot, val_loss_plot, iter_text, val_scatter


ani = animation.FuncAnimation(
    fig, animate, frames=len(frame_iters), init_func=init,
    interval=80, blit=True
)

print(f"Built animation with {len(frame_iters)} frames.")
```

## Celle 24 — markdown

##### 10a. Save to MP4

Requires `ffmpeg`. If it is not installed, this cell falls back to an animated GIF via
`PillowWriter` so the notebook still produces a file.

## Celle 25 — code

### Kildelinjer 1–12

```python
mp4_path = os.path.join(OUT_DIR, "gradient_descent_fit.mp4")

if animation.FFMpegWriter.isAvailable():
    ani.save(mp4_path, writer=animation.FFMpegWriter(fps=15, bitrate=1800), dpi=130)
    saved_path = mp4_path
    print("Saved:", saved_path)
else:
    gif_path = os.path.join(OUT_DIR, "gradient_descent_fit.gif")
    ani.save(gif_path, writer=animation.PillowWriter(fps=15), dpi=100)
    saved_path = gif_path
    print("ffmpeg not found - saved a GIF instead:", saved_path)
    print("To get the MP4, install ffmpeg, e.g.  conda install -c conda-forge ffmpeg")
```

## Celle 26 — markdown

##### 10b. Play it inline

`to_jshtml()` embeds the frames plus a JavaScript player, so it works in any browser without
needing an HTML5 video codec. (Use `ani.to_html5_video()` instead if you prefer a real video
element and have ffmpeg.)

## Celle 27 — code

### Kildelinjer 1–3

```python
display(HTML(ani.to_jshtml(fps=15)))
plt.close(fig)   # tidy up the figure now that the animation is rendered
plt.ion()        # restore interactive plotting for any later cells
```

## Celle 28 — markdown

#### 11. Summary

Everything above has also been written to disk:

```
outputs/
├── gradient_descent_fit.mp4   (or .gif without ffmpeg)
├── final_fit.png
├── loss_curve.png
└── metrics.txt
```

## Celle 29 — code

### Kildelinjer 1–9

```python
print("Files in", OUT_DIR)
for fn in sorted(os.listdir(OUT_DIR)):
    size = os.path.getsize(os.path.join(OUT_DIR, fn))
    print(f"  {fn:<32} {size/1024:8.1f} KB")

print()
print(f"f(x) = {a_final:.4f} * x + {b_final:.4f}")
print(f"train  MSE {train_mse_final:8.1f}   R^2 {train_r2_final:.4f}")
print(f"val    MSE {val_mse_final:8.1f}   R^2 {val_r2_final:.4f}")
```
