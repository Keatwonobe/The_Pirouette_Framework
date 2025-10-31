# Analyze structure of the local manifold we just found: PCA, bounding box, and a simple linear model p,q vs log(mu).
import numpy as np, pandas as pd
from math import log
import matplotlib.pyplot as plt

# Load the dataframe created previously (exists in memory as sol_local); be defensive:
try:
    df = sol_local.copy()
except NameError:
    df = pd.read_csv("/mnt/data/pirouette_manifold_local_grid.csv")

# Bounding box
bbox = {
    "mu_min": float(df["mu_meV"].min()),
    "mu_max": float(df["mu_meV"].max()),
    "p_min":  float(df["p"].min()),
    "p_max":  float(df["p"].max()),
    "q_min":  float(df["q"].min()),
    "q_max":  float(df["q"].max()),
}

# PCA
X = df[["mu_meV","p","q"]].to_numpy()
Xc = X - X.mean(axis=0, keepdims=True)
C = (Xc.T @ Xc) / (len(Xc)-1)
w, V = np.linalg.eigh(C)          # ascending
order = np.argsort(w)[::-1]
w = w[order]; V = V[:,order]
var_exp = w / w.sum()

# Simple relationship: fit p and q as affine functions of log(mu)
Z = np.column_stack([np.log(df["mu_meV"].to_numpy()), np.ones(len(df))])
p_coef, _, _, _ = np.linalg.lstsq(Z, df["p"].to_numpy(), rcond=None)
q_coef, _, _, _ = np.linalg.lstsq(Z, df["q"].to_numpy(), rcond=None)

# Predict and compute R^2
def r2(y, yhat):
    yb = y - y.mean()
    return 1 - np.sum((y-yhat)**2) / np.sum(yb**2)

p_hat = Z @ p_coef
q_hat = Z @ q_coef
r2_p = r2(df["p"].to_numpy(), p_hat)
r2_q = r2(df["q"].to_numpy(), q_hat)

# Save a compact JSON-like text report
report_text = f"""
Local-manifold structure:
- Bounding box:
  mu in [{bbox['mu_min']:.3f}, {bbox['mu_max']:.3f}] meV
  p  in [{bbox['p_min']:.4f}, {bbox['p_max']:.4f}]
  q  in [{bbox['q_min']:.4f}, {bbox['q_max']:.4f}]

- PCA (variance explained): {var_exp.tolist()}
  First PC direction (columns [mu,p,q]): {V[:,0].tolist()}

- Affine laws vs log(mu):
  p ≈ {p_coef[0]:+.4f}·log(μ) {p_coef[1]:+.4f}   (R²={r2_p:.3f})
  q ≈ {q_coef[0]:+.4f}·log(μ) {q_coef[1]:+.4f}   (R²={r2_q:.3f})
"""

# Make two single plots: p vs log(mu) and q vs log(mu)
fig1 = plt.figure(figsize=(6,4))
plt.scatter(np.log(df["mu_meV"]), df["p"], s=8)
plt.plot(np.log(df["mu_meV"]), p_hat, linewidth=2)
plt.xlabel("log(μν [meV])"); plt.ylabel("p")
plt.title("p vs log(μν) with affine fit")
plt.tight_layout()
plt.show()

fig2 = plt.figure(figsize=(6,4))
plt.scatter(np.log(df["mu_meV"]), df["q"], s=8)
plt.plot(np.log(df["mu_meV"]), q_hat, linewidth=2)
plt.xlabel("log(μν [meV])"); plt.ylabel("q")
plt.title("q vs log(μν) with affine fit")
plt.tight_layout()
plt.show()

report_text
