<!-- studygraph:converted-source:v1 -->
# Uge 3 — PCA_for_FewerDimensions_4d_to_2d (ipynb)

Kilde: [week3/PCA_for_FewerDimensions_4d_to_2d.ipynb](../../source/week3/PCA_for_FewerDimensions_4d_to_2d.ipynb).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

Kildeceller er bevaret i rækkefølge. Koden er ikke kørt. Gemte outputs, billeder og kørselsnumre er udeladt; der tilføjes ingen forsøgsresultater.

## Celle 1 — markdown

### Collapsing four dimensions into two: PCA as an animation

Every point in this dataset has **three spatial coordinates** $(x, y, z)$ and **one extra measurement** $c$, drawn as color.
That makes the data four-dimensional. Principal component analysis (PCA) finds the directions in which the cloud spreads the most, rotates the data so those directions line up with the axes, and then drops the directions that carry the least variance.

The notebook builds one animated Plotly figure that plays through the whole process:

1. **Raw data.** The features are in different units, so the cloud is off-center with uneven spreads.
2. **Standardize.** Each feature is centered and scaled to unit variance.
3. **Find the principal components.** These are the eigenvectors of the $4 \times 4$ covariance matrix.
4. **Rotate in 4D.** A smooth rotation $W(t)$ turns the principal directions onto the drawing axes, with color acting as the 4th axis.
5. **Drop PC4.** The color axis is squashed to zero.
6. **Drop PC3.** The slab flattens onto the PC1–PC2 plane.
7. **Face the plane.** The camera turns to look straight down.
8. **2D result.** The points are recolored by the original $c$ to show that its information survives as position.

Requirements: `pip install numpy plotly`. With `pio.renderers.default = "browser"`, each `fig.show()` opens a new browser tab.

## Celle 2 — code

### Kildelinjer 1–8

```python
import textwrap

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

pio.renderers.default = "browser"   # every fig.show() opens in a new browser tab
```

## Celle 3 — markdown

#### Settings

## Celle 4 — code

### Kildelinjer 1–4

```python
DATASET  = "spiral"   # "spiral", "clusters" or "rings": the 2D pattern hidden inside the 4D data
SEED     = 8          # change for a different random sample
N_POINTS = 1000       # number of points in the cloud
FPS      = 12         # animation frames per second; lower it for a smaller, faster-loading figure
```

## Celle 5 — markdown

#### 1. Build a 4D dataset with a hidden 2D pattern

To make the demo meaningful, the data really is (almost) two-dimensional. A 2D pattern $(u, v)$ is laid on a flat sheet that runs through all four features, including color. A little noise is added in the two remaining directions: a moderate amount (which becomes PC3) and a very small amount (PC4).

The sheet starts from a balanced orthonormal basis, so each feature carries a similar share of the pattern. It is then shuffled and tilted by a small random 4D rotation. Finally each feature gets its own offset and unit, so the raw data needs standardizing.

## Celle 6 — code

### Kildelinjer 1–45

```python
def make_latent(kind, n, rng):
    # The 2D pattern (u, v) that PCA should recover.
    idx = np.arange(n)
    if kind == "spiral":
        arm = idx % 2
        t = rng.random(n) ** 0.7
        theta = arm * np.pi + t * 3.3 * np.pi
        radius = 0.12 + 1.5 * t
        jitter = (0.06 + 0.06 * t)[:, None]
        uv = np.c_[radius * np.cos(theta), radius * np.sin(theta)] + jitter * rng.standard_normal((n, 2))
    elif kind == "clusters":
        centers = np.array([[-1.25, -0.35], [-0.10, -1.15], [0.25, 0.95], [1.35, 0.10]])
        uv = centers[idx % 4] + 0.27 * rng.standard_normal((n, 2))
    elif kind == "rings":
        outer = (idx % 5) < 3
        theta = rng.random(n) * 2 * np.pi
        radius = np.where(outer, 1.45, 0.60) + 0.06 * rng.standard_normal(n)
        uv = np.c_[radius * np.cos(theta), radius * np.sin(theta)]
    else:
        raise ValueError(f"Unknown dataset {kind!r}")
    return uv - uv.mean(axis=0)


def plane_rotation(a, b, angle, dim=4):
    # Rotation by `angle` in the plane spanned by coordinate axes a and b.
    G = np.eye(dim)
    c, s = np.cos(angle), np.sin(angle)
    G[a, a], G[a, b], G[b, a], G[b, b] = c, -s, s, c
    return G


def make_dataset(kind, n, seed):
    rng = np.random.default_rng(seed)
    uv = make_latent(kind, n, rng) * [1.2, 0.8]          # a little anisotropy so PC1 and PC2 differ

    # Balanced orthonormal basis (rows): every feature takes part in every direction equally.
    E = 0.5 * np.array([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]], dtype=float)
    E = E[rng.permutation(4)] * rng.choice([-1, 1], size=4)
    for a in range(4):                                     # small random tilt in 4D
        for b in range(a + 1, 4):
            angle = rng.choice([-1, 1]) * (0.04 + 0.10 * rng.random())
            E = E @ plane_rotation(a, b, angle).T

    noise = rng.standard_normal((n, 2)) * [0.24, 0.08]    # thickness of the sheet in the other two directions
    X = np.c_[uv, noise] @ E                               # rows of E: sheet, sheet, noise, noise
```

### Kildelinjer 46–59

```python

    offset = np.array([4.0, 1.5, 2.5, 50.0])               # each feature gets its own origin ...
    unit = np.array([1.1, 0.55, 0.8, 20.0])                # ... and its own unit
    F = offset + unit * X
    return F, uv


F, uv = make_dataset(DATASET, N_POINTS, SEED)
FEATURES = ["x", "y", "z", "c"]

print(f"{N_POINTS} points, 4 features")
print(f"{'feature':>8} {'mean':>9} {'std':>8}")
for name, m, s in zip(FEATURES, F.mean(axis=0), F.std(axis=0, ddof=1)):
    print(f"{name:>8} {m:9.2f} {s:8.2f}")
```

## Celle 7 — markdown

#### 2. Standardize and compute the principal components

Standardizing gives every feature mean 0 and variance 1:

$$ z_{ij} = \frac{f_{ij} - \bar f_j}{s_j} $$

The principal components are the eigenvectors of the covariance matrix $C = \frac{1}{n-1} Z^\top Z$, sorted by eigenvalue. Each eigenvalue $\lambda_k$ is the variance along its component, and $\lambda_k / \sum \lambda$ is the share of the total variance it explains.

Stacking the eigenvectors as the **rows** of a matrix $W$ gives the PCA rotation: the component scores are $q = W z$. An eigenvector's sign is arbitrary, so the signs are chosen to keep $W$ close to the identity and to make $\det W = +1$. That makes $W$ a proper rotation that can be animated.

## Celle 8 — code

### Kildelinjer 1–28

```python
mean = F.mean(axis=0)
std = F.std(axis=0, ddof=1)
Z = (F - mean) / std

C = np.cov(Z, rowvar=False)
eigvals, eigvecs = np.linalg.eigh(C)          # ascending order for symmetric matrices
order = np.argsort(eigvals)[::-1]
lam = eigvals[order]
W = eigvecs[:, order].T.copy()                # rows = principal directions

for k in range(3):                            # sign choice: keep W near the identity
    if W[k, k] < 0:
        W[k] *= -1
if np.linalg.det(W) < 0:                      # make W a proper rotation (det = +1)
    W[3] *= -1

explained = lam / lam.sum()
scores = Z @ W.T                              # q = W z for every point

# Cross-check against the singular value decomposition of Z
sing = np.linalg.svd(Z, compute_uv=False)
assert np.allclose(sing**2 / (N_POINTS - 1), lam)

np.set_printoptions(precision=3, suppress=True)
print("Covariance matrix of the standardized data:\n", C, "\n")
print(f"{'':>5} {'eigenvalue':>11} {'explained':>10} {'cumulative':>11}   direction (x, y, z, c)")
for i in range(4):
    print(f"PC{i+1:<3} {lam[i]:11.3f} {100*explained[i]:9.1f}% {100*explained[:i+1].sum():10.1f}%   {W[i]}")
```

## Celle 9 — markdown

#### 3. A smooth rotation in four dimensions

To animate the change from the original axes to the principal axes, there needs to be a path of rotations $W(t)$ with $W(0) = I$ and $W(1) = W$.

Any 4D rotation can be split into six **plane rotations**, one for each pair of axes. Each zeroes one entry below the diagonal, like a QR decomposition done with Givens rotations. Scaling all six angles by $t$ gives a smooth path that is a genuine rotation at every step, so distances between points never distort during the animation.

## Celle 10 — code

### Kildelinjer 1–39

```python
def givens_decompose(W):
    # Return plane rotations (j, i, angle) with W = R_1(angle_1) ... R_6(angle_6).
    A = W.copy()
    rotations = []
    for j in range(3):
        for i in range(j + 1, 4):
            angle = np.arctan2(A[i, j], A[j, j])
            c, s = np.cos(angle), np.sin(angle)
            row_j, row_i = A[j].copy(), A[i].copy()
            A[j] = c * row_j + s * row_i
            A[i] = -s * row_j + c * row_i
            rotations.append((j, i, angle))
    assert np.allclose(A, np.eye(4), atol=1e-9), "W must be a proper rotation"
    return rotations


def rotation_at(rotations, t):
    # The rotation after a fraction t of every plane rotation has been applied.
    M = np.eye(4)
    for j, i, angle in rotations:
        c, s = np.cos(t * angle), np.sin(t * angle)
        col_j, col_i = M[:, j].copy(), M[:, i].copy()
        M[:, j] = c * col_j + s * col_i
        M[:, i] = -s * col_j + c * col_i
    return M


rots = givens_decompose(W)

# Checks: correct end points, and a real rotation part-way along the path
assert np.allclose(rotation_at(rots, 0.0), np.eye(4))
assert np.allclose(rotation_at(rots, 1.0), W)
for t in np.linspace(0, 1, 11):
    Wt = rotation_at(rots, t)
    assert np.allclose(Wt @ Wt.T, np.eye(4)) and np.isclose(np.linalg.det(Wt), 1.0)

print("Plane rotation angles (degrees):")
for j, i, angle in rots:
    print(f"  {FEATURES[j]}–{FEATURES[i]} plane: {np.degrees(angle):7.1f}")
```

## Celle 11 — markdown

#### 4. The timeline

Each stage has a duration. `state_at(T)` turns a time in seconds into eased progress values that drive the animation, such as how far the standardization, rotation and collapses have gone.

## Celle 12 — code

### Kildelinjer 1–22

```python
STAGES = [
    dict(id="raw", dur=4.5, short="Raw data", title="Raw data in four dimensions",
         caption="Each point has three coordinates, x, y and z, plus a fourth measurement c shown as color. "
                 "The features come in different units, so the cloud sits off-center with uneven spreads."),
    dict(id="std", dur=3.5, short="Standardize", title="Standardize every feature",
         caption="Subtract each feature's mean and divide by its standard deviation. "
                 "All four features, color included, are now centered at zero with unit variance."),
    dict(id="pcs", dur=4.5, short="Find components", title="Find the principal components",
         caption="The eigenvectors of the 4 × 4 covariance matrix point along the directions of greatest spread. "
                 "The arrows show their x, y, z part; the rest of each vector points along the color axis."),
    dict(id="rot", dur=7.0, short="Rotate in 4D", title="Rotate into the principal axes",
         caption="A smooth rotation in four dimensions turns the principal directions onto the drawing axes. "
                 "The colors drift toward the middle of the scale as that variation moves into the positions."),
    dict(id="c4", dur=3.5, short="Drop PC4", title="Drop the fourth component",
         caption="Color now shows PC4, the direction with the least spread. "
                 "Setting it to zero discards only {p4} of the variance, so the colors barely shift."),
    dict(id="c3", dur=4.0, short="Drop PC3", title="Drop the third component",
         caption="Squash PC3 next. The thin slab flattens onto the plane of PC1 and PC2, "
                 "discarding another {p3} of the variance."),
    dict(id="cam", dur=3.5, short="Face the plane", title="Face the remaining plane",
         caption="Turning the camera square to the plane shows what is left: every point now has exactly two coordinates."),
    dict(id="end", dur=6.5, short="2D result", title="The two-component view",
```

### Kildelinjer 23–67

```python
         caption="PC1 and PC2 keep {kept} of the total variance. Recoloring by the original feature c shows "
                 "that its information survived, now encoded as position across the plane."),
]

t0 = 0.0
for s in STAGES:
    s["start"] = t0
    t0 += s["dur"]
TOTAL = t0
S = {s["id"]: s for s in STAGES}


def ease(t):
    t = float(np.clip(t, 0.0, 1.0))
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def lerp(a, b, t):
    return a + (b - a) * t


def progress(stage_id, T):
    s = S[stage_id]
    return float(np.clip((T - s["start"]) / s["dur"], 0.0, 1.0))


def state_at(T):
    p_pcs, p4, p3 = progress("pcs", T), progress("c4", T), progress("c3", T)
    return dict(
        std=ease(progress("std", T)),               # raw -> standardized
        grow=ease(p_pcs),                           # arrows grow
        arrow=ease(p_pcs) * (1 - ease(p4 * 1.6)),   # arrow visibility
        bars=ease(p_pcs * 1.5),                     # variance bars grow
        rot=ease(progress("rot", T)),               # t in W(t)
        s4=ease(p4), s3=ease(p3), p3=p3,            # collapse of PC4 and PC3
        cam=ease(progress("cam", T)),               # camera turns to face the plane
        plane=ease(p4),                             # PC1–PC2 grid fades in
        recolor=ease((T - S["end"]["start"] - 0.8) / 2.2),
    )


def stage_index(T):
    return max(i for i, s in enumerate(STAGES) if T >= s["start"] - 1e-9)
```

### Kildelinjer 68–68

```python
print(f"{len(STAGES)} stages, {TOTAL:.1f} s in total")
```

## Celle 13 — markdown

#### 5. Draw one frame

`frame_at(T)` computes everything on screen at time $T$:

* **Points:** $q = W(t)\,z$, with $q_4$ scaled by $(1 - s_4)$ and $q_3$ by $(1 - s_3)$. Positions are the first three coordinates. Color is the fourth coordinate, blended back to the original $c$ at the very end.
* **Arrows:** the principal directions carried along by the same rotation, so they end up lying on the axes.
* **Axes, grid and residual lines:** the $z$ axis shrinks as PC3 collapses, and faint lines show how far each point moves onto the plane.
* **Camera:** a slow orbit that settles into a view straight down on the PC1–PC2 plane.
* **Bar chart:** explained variance, with bars fading as their components are dropped.

## Celle 14 — code

### Kildelinjer 1–45

```python
COLORSCALE = [[0.00, "rgb(72,80,216)"], [0.25, "rgb(28,159,214)"], [0.50, "rgb(47,179,109)"],
              [0.75, "rgb(232,163,23)"], [1.00, "rgb(224,67,90)"]]
C_RANGE = 2.2                  # color scale covers -2.2 to +2.2 standard deviations
INK = "21,34,46"
ACCENT = "61,67,200"
FONT = "Georgia, 'Times New Roman', serif"

L = 1.75                       # axis half-length (scene units)
GRID, GSTEP = 1.75, 0.35       # PC1–PC2 grid extent and spacing
BOX = 2.1                      # fixed scene range, so nothing rescales between frames
AZ0, OMEGA = 0.75, 0.16        # camera start azimuth (rad) and orbit speed (rad/s)
R_ORBIT, R_TOP = 1.3, 1.28    # camera distance while orbiting and when facing the plane
CAM_END = S["cam"]["start"] + S["cam"]["dur"]

# Raw coordinates are shown with one common scale factor, so their uneven spreads stay visible.
raw_scale = 1.7 / np.max(np.abs(mean[:3]) + 2.2 * std[:3])
raw_pos = F[:, :3] * raw_scale
k_scale = 1.55 / (2.3 * np.sqrt(lam[0]))       # standardized units -> scene units
residual_idx = np.arange(0, N_POINTS, 2)       # residual lines for every other point

pct = lambda share: f"{100 * share:.1f}%"
fill = lambda text: text.format(p4=pct(explained[3]), p3=pct(explained[2]), kept=pct(explained[:2].sum()))


def ink(alpha):
    # Ink blended onto the white background. Opaque colors avoid WebGL transparency-sorting artifacts.
    r, g, b = (int(v) for v in INK.split(","))
    mix = lambda v: round(255 + (v - 255) * float(np.clip(alpha, 0, 1)))
    return f"rgb({mix(r)},{mix(g)},{mix(b)})"


def f32(a):
    return np.asarray(a, dtype=np.float32)


def segments(pairs):
    # Line segments [(p, q), ...] -> x, y, z lists with None gaps between segments.
    xs, ys, zs = [], [], []
    for p, q in pairs:
        xs += [p[0], q[0], None]
        ys += [p[1], q[1], None]
        zs += [p[2], q[2], None]
    return xs, ys, zs
```

### Kildelinjer 46–90

```python
GRID_SEGMENTS = segments(
    [((g, -GRID, 0), (g, GRID, 0)) for g in np.arange(-GRID, GRID + 1e-6, GSTEP)]
    + [((-GRID, g, 0), (GRID, g, 0)) for g in np.arange(-GRID, GRID + 1e-6, GSTEP)]
)


def camera_at(T, cam):
    target = -np.pi / 2 + 2 * np.pi * np.round((AZ0 + OMEGA * CAM_END + np.pi / 2) / (2 * np.pi))
    az = lerp(AZ0 + OMEGA * T, target, cam)
    el = lerp(0.36 + 0.07 * np.sin(0.45 * T), np.pi / 2, cam)
    r = lerp(R_ORBIT, R_TOP, cam)
    ca, sa, ce, se = np.cos(az), np.sin(az), np.cos(el), np.sin(el)
    return dict(
        eye=dict(x=r * ce * ca, y=r * ce * sa, z=r * se),
        up=dict(x=-ca * se, y=-sa * se, z=ce),       # keeps the view upright, ends with PC2 pointing up
        center=dict(x=0, y=0, z=lerp(0.1, 0.0, cam)),
        projection=dict(type="perspective"),
    )


def scene_layout(T, cam, labels=()):
    hidden = dict(visible=False, range=[-BOX, BOX], autorange=False)
    return dict(domain=dict(x=[0.0, 0.74], y=[0.0, 0.94]), xaxis=hidden, yaxis=hidden, zaxis=hidden,
                aspectmode="manual", aspectratio=dict(x=1, y=1, z=1), camera=camera_at(T, cam),
                dragmode="orbit", annotations=list(labels))


def label3d(text, xyz, size=15, color=None, opacity=1.0, italic=False):
    # A text label pinned to a 3D point (drawn in screen space, so it stays crisp).
    if italic:
        text = f"<i>{text}</i>"
    return dict(x=float(xyz[0]), y=float(xyz[1]), z=float(xyz[2]), text=text, showarrow=False,
                opacity=float(np.clip(opacity, 0, 1)), bgcolor="rgba(255,255,255,0.75)",
                font=dict(size=size, family=FONT, color=color or f"rgb({INK})"))


def frame_at(T):
    st = state_at(T)
    Wt = rotation_at(rots, st["rot"])

    # --- points ---------------------------------------------------------------
    q = Z @ Wt.T
    q[:, 3] *= 1 - st["s4"]
    q[:, 2] *= 1 - st["s3"]
    pos = lerp(raw_pos, k_scale * q[:, :3], st["std"])
```

### Kildelinjer 91–127

```python
    color = lerp(q[:, 3], Z[:, 3], st["recolor"])

    ticks = [-2, -1, 0, 1, 2]
    if st["recolor"] > 0.5:
        cb_title, ticktext = "original c (σ)", [f"{v:+d}" if v else "0" for v in ticks]
    elif st["rot"] > 0.5:
        cb_title, ticktext = "PC4 score", [f"{v:+d}" if v else "0" for v in ticks]
    elif st["std"] > 0.5:
        cb_title, ticktext = "c, standardized (σ)", [f"{v:+d}" if v else "0" for v in ticks]
    else:
        cb_title, ticktext = "c, raw units", [f"{mean[3] + v * std[3]:.0f}" for v in ticks]

    points = go.Scatter3d(
        x=f32(pos[:, 0]), y=f32(pos[:, 1]), z=f32(pos[:, 2]), mode="markers", hoverinfo="skip",
        marker=dict(size=3.5, color=f32(color), colorscale=COLORSCALE, cmin=-C_RANGE, cmax=C_RANGE,
                    line=dict(width=0),
                    colorbar=dict(title=dict(text=cb_title, side="right"), tickvals=ticks, ticktext=ticktext,
                                  x=0.76, xanchor="left", y=0.22, len=0.4, thickness=14, outlinewidth=0)),
        name="points", showlegend=False)

    # --- axes and labels -----------------------------------------------------
    zlen = L * (1 - st["s3"])
    px_, py_, pz_ = segments([((0, 0, 0), (L, 0, 0)), ((0, 0, 0), (0, L, 0)), ((0, 0, 0), (0, 0, zlen))])
    nx_, ny_, nz_ = segments([((0, 0, 0), (-L, 0, 0)), ((0, 0, 0), (0, -L, 0)), ((0, 0, 0), (0, 0, -zlen))])
    axes_pos = go.Scatter3d(x=px_, y=py_, z=pz_, mode="lines", hoverinfo="skip", showlegend=False,
                            line=dict(color=ink(0.75), width=4))
    axes_neg = go.Scatter3d(x=nx_, y=ny_, z=nz_, mode="lines", hoverinfo="skip", showlegend=False,
                            line=dict(color=ink(0.3), width=2, dash="dash"))

    lab = L * 1.13
    label_pos = [(lab, 0, 0), (0, lab, 0), (0, 0, lab * (1 - st["s3"]))]
    labels = []
    for i in range(3):
        if i == 2 and st["s3"] > 0.6:
            continue
        if st["rot"] < 0.5:
            labels.append(label3d("xyz"[i], label_pos[i], size=18, italic=True))
```

### Kildelinjer 128–159

```python
        elif st["cam"] < 0.5 or i == 2:
            labels.append(label3d(f"<b>PC{i + 1}</b>", label_pos[i]))
        else:
            labels.append(label3d(f"<b>PC{i + 1}</b> ({pct(explained[i])})", label_pos[i]))

    # --- PC1–PC2 grid -----------------------------------------------------------
    grid_on = st["plane"] > 0.01
    grid = go.Scatter3d(x=GRID_SEGMENTS[0] if grid_on else [], y=GRID_SEGMENTS[1] if grid_on else [],
                        z=GRID_SEGMENTS[2] if grid_on else [], mode="lines", hoverinfo="skip", showlegend=False,
                        line=dict(color=ink(0.2 * st["plane"]), width=1.5))

    # --- residual lines while PC3 collapses --------------------------------------
    res_alpha = 0.45 * np.sin(np.pi * st["p3"])
    if res_alpha > 0.01:
        n_res = len(residual_idx)
        rx = np.full(3 * n_res, np.nan); ry = rx.copy(); rz = rx.copy()
        p = pos[residual_idx]
        rx[0::3], ry[0::3], rz[0::3] = p[:, 0], p[:, 1], p[:, 2]
        rx[1::3], ry[1::3], rz[1::3] = p[:, 0], p[:, 1], 0.0
        residual = go.Scatter3d(x=f32(rx), y=f32(ry), z=f32(rz), mode="lines", hoverinfo="skip", showlegend=False,
                                connectgaps=False, line=dict(color=ink(res_alpha), width=2))
    else:
        residual = go.Scatter3d(x=[], y=[], z=[], mode="lines", hoverinfo="skip", showlegend=False)

    # --- principal direction arrows -------------------------------------------------
    if st["arrow"] > 0.01:
        tips = np.array([k_scale * 2.8 * np.sqrt(lam[a]) * st["grow"] * (Wt @ W[a])[:3] for a in range(3)])
        ax_, ay_, az_ = segments([((0, 0, 0), tuple(tip)) for tip in tips])
        arrows = go.Scatter3d(x=ax_, y=ay_, z=az_, mode="lines", hoverinfo="skip", showlegend=False,
                              line=dict(color=ink(st["arrow"]), width=9))
        heads = go.Scatter3d(x=tips[:, 0], y=tips[:, 1], z=tips[:, 2], mode="markers", hoverinfo="skip",
                             showlegend=False, marker=dict(size=6, symbol="diamond", color=ink(st["arrow"])))
```

### Kildelinjer 160–190

```python
        if st["rot"] < 0.5:
            labels += [label3d(f"<b>PC{a + 1}</b>", tips[a] * 1.12, size=13, opacity=st["arrow"] * (1 - 2 * st["rot"]))
                       for a in range(3)]
    else:
        arrows = go.Scatter3d(x=[], y=[], z=[], mode="lines", hoverinfo="skip", showlegend=False)
        heads = go.Scatter3d(x=[], y=[], z=[], mode="markers", hoverinfo="skip", showlegend=False)

    # --- explained variance bars ------------------------------------------------------
    dim = [0.0, 0.0, st["s3"], st["s4"]]
    bars = go.Bar(x=["PC1", "PC2", "PC3", "PC4"], y=100 * explained * st["bars"], xaxis="x", yaxis="y",
                  marker=dict(color=[f"rgba({ACCENT},{1 - 0.78 * d:.3f})" for d in dim]),
                  text=[pct(e) if st["bars"] > 0.02 else "" for e in explained], textposition="outside",
                  cliponaxis=False, hoverinfo="skip", showlegend=False)

    # --- captions -------------------------------------------------------------------
    si = stage_index(T)
    stage = STAGES[si]
    kept = 1 - st["s4"] * explained[3] - st["s3"] * explained[2]
    caption = "<br>".join(textwrap.wrap(fill(stage["caption"]), 105))
    layout = dict(
        title=dict(text=f"<b>Step {si + 1} of {len(STAGES)}: {stage['title']}</b>"),
        annotations=[
            dict(text=caption, x=0, y=1.0, xref="paper", yref="paper", xanchor="left", yanchor="bottom",
                 align="left", showarrow=False, font=dict(size=14, family=FONT, color=f"rgb({INK})")),
            dict(text=f"Variance kept: <b>{pct(kept)}</b>", x=0.9, y=0.5, xref="paper", yref="paper",
                 xanchor="center", yanchor="top", showarrow=False, font=dict(size=14, family=FONT)),
        ],
        scene=scene_layout(T, st["cam"], labels),
    )
    data = [points, grid, axes_neg, axes_pos, residual, arrows, heads, bars]
    return data, layout
```

## Celle 15 — markdown

#### 6. Assemble the animation and open it in the browser

The figure has one Plotly frame every `1 / FPS` seconds. **Play** and **Pause** control playback, the slider scrubs through time, and the dropdown jumps to the start of any step. You can drag to orbit while paused, but the camera follows the script again once the animation plays.

## Celle 16 — code

### Kildelinjer 1–40

```python
times = np.append(np.arange(0.0, TOTAL, 1.0 / FPS), TOTAL - 1e-3)
frame_ms = 1000 / FPS

frames = []
for T in times:
    data, layout = frame_at(T)
    frames.append(go.Frame(name=f"{T:.3f}", data=data, layout=layout, traces=list(range(len(data)))))

data0, layout0 = frame_at(0.0)
play_args = dict(frame=dict(duration=frame_ms, redraw=True), transition=dict(duration=0),
                 fromcurrent=True, mode="immediate")
jump_args = dict(frame=dict(duration=0, redraw=True), transition=dict(duration=0), mode="immediate")

def frame_name_at(t):
    return frames[int(np.argmin(np.abs(times - t)))].name

fig = go.Figure(data=data0, frames=frames)
fig.update_layout(
    **layout0,
    template="plotly_white",
    height=860,
    margin=dict(l=30, r=30, t=135, b=100),
    font=dict(family=FONT, size=13, color=f"rgb({INK})"),
    xaxis=dict(domain=[0.8, 1.0], anchor="y", fixedrange=True, tickfont=dict(size=13)),
    yaxis=dict(domain=[0.58, 0.93], anchor="x", range=[0, 100], fixedrange=True,
               title=dict(text="% of variance"), gridcolor="rgba(0,0,0,0.08)"),
    updatemenus=[
        dict(type="buttons", direction="left", x=0.0, y=-0.02, xanchor="left", yanchor="top",
             pad=dict(t=0, r=10), showactive=False,
             buttons=[dict(label="▶ Play", method="animate", args=[None, play_args]),
                      dict(label="❚❚ Pause", method="animate", args=[[None], jump_args])]),
        dict(type="dropdown", direction="down", x=1.0, y=0.38, xanchor="right", yanchor="top",
             showactive=True, active=0,
             buttons=[dict(label=f"{i + 1}. {s['short']}", method="animate",
                           args=[[frame_name_at(s["start"])], jump_args]) for i, s in enumerate(STAGES)]),
    ],
    sliders=[dict(
        active=0, x=0.16, y=-0.01, len=0.58, xanchor="left", yanchor="top", pad=dict(t=0),
        currentvalue=dict(prefix="t = ", suffix=" s", visible=True, xanchor="right", font=dict(size=13, color=f"rgb({INK})")),
        font=dict(color="rgba(0,0,0,0)"), ticklen=0, tickcolor="rgba(0,0,0,0)",
```

### Kildelinjer 41–48

```python
        steps=[dict(method="animate", label=f"{T:.1f}", args=[[fr.name], jump_args]) for T, fr in zip(times, frames)],
    )],
)
fig.add_annotation(text="Jump to step", x=1.0, y=0.39, xref="paper", yref="paper", xanchor="right",
                   yanchor="bottom", showarrow=False, font=dict(size=13))

print(f"{len(frames)} frames at {FPS} fps")
fig.show()
```

## Celle 17 — markdown

##### Save a standalone copy (optional)

This writes a self-contained HTML file that plays offline and can be shared.

## Celle 18 — code

### Kildelinjer 1–2

```python
fig.write_html("pca_4d_to_2d.html", include_plotlyjs=True, auto_play=False)
print("Saved pca_4d_to_2d.html")
```

## Celle 19 — markdown

#### 7. Check the result against the hidden pattern

The left panel is the final PCA view: the scores on PC1 and PC2. The right panel is the 2D pattern that was hidden inside the 4D data. PCA can't know how that pattern was originally oriented, so its version may be rotated or mirrored, but the shape should match.

Both panels are colored by the original feature $c$. The smooth color gradient across the plane is the information from the fourth feature, now carried by position.

The printed $R^2$ values measure how well a linear map from (PC1, PC2) reproduces the hidden $(u, v)$; values near 1 mean PCA recovered the sheet.

## Celle 20 — code

### Kildelinjer 1–21

```python
A = np.c_[scores[:, :2], np.ones(N_POINTS)]
coef, *_ = np.linalg.lstsq(A, uv, rcond=None)
r2 = 1 - ((uv - A @ coef) ** 2).sum(axis=0) / ((uv - uv.mean(axis=0)) ** 2).sum(axis=0)
print(f"R² for recovering u: {r2[0]:.3f}, v: {r2[1]:.3f}")

check = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                      subplot_titles=(f"What PCA found: PC1 vs PC2 ({pct(explained[:2].sum())} of variance)",
                                      "The hidden 2D pattern used to build the data"))
marker = dict(size=5, color=Z[:, 3], colorscale=COLORSCALE, cmin=-C_RANGE, cmax=C_RANGE,
              colorbar=dict(title=dict(text="original c (σ)"), thickness=14, outlinewidth=0))
check.add_trace(go.Scattergl(x=scores[:, 0], y=scores[:, 1], mode="markers", marker=marker,
                             hovertemplate="PC1 %{x:.2f}<br>PC2 %{y:.2f}<extra></extra>"), 1, 1)
check.add_trace(go.Scattergl(x=uv[:, 0], y=uv[:, 1], mode="markers", marker={**marker, "showscale": False},
                             hovertemplate="u %{x:.2f}<br>v %{y:.2f}<extra></extra>"), 1, 2)
check.update_xaxes(title_text="PC1", row=1, col=1)
check.update_yaxes(title_text="PC2", scaleanchor="x", scaleratio=1, row=1, col=1)
check.update_xaxes(title_text="u", row=1, col=2)
check.update_yaxes(title_text="v", scaleanchor="x2", scaleratio=1, row=1, col=2)
check.update_layout(template="plotly_white", height=560, showlegend=False,
                    font=dict(family=FONT, size=13, color=f"rgb({INK})"))
check.show()
```
