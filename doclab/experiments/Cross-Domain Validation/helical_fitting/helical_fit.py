# helical_fit.py
# Reusable κ-Hamiltonian fitting utilities with AIC/BIC scoring.
# Usage:
#   python helical_fit.py --csv your_timeseries.csv --tcol t --ycol y --out outdir
# CSV must have columns for time (t) and observed signal (y).

import argparse, math, os
import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple
from scipy.optimize import curve_fit

@dataclass
class FitResult:
    params: Dict[str, float]
    rss: float
    aic: float
    bic: float
    cov: np.ndarray

def sine_model(t, A, w, phi, C):
    # Standard sinusoid: A * sin(w t + phi) + C
    return A * np.sin(w * t + phi) + C

def helical_model(t, A, w, phi, C, kappa):
    # Helical phase-drag model: phase = w t + phi + kappa * (w t)^2 / 2  (toy; replace with κ-Hamiltonian)
    # NOTE: Replace with your exact helical derivative integration per MATH-028/029/030.
    phase = w * t + phi + 0.5 * kappa * (w * t)**2
    return A * np.sin(phase) + C

def aic_bic(y_true, y_pred, k_params):
    n = len(y_true)
    rss = float(np.sum((y_true - y_pred)**2))
    aic = n * math.log(rss / n + 1e-30) + 2 * k_params
    bic = n * math.log(rss / n + 1e-30) + k_params * math.log(n + 1e-30)
    return rss, aic, bic

def fit_model(model, t, y, p0):
    popt, pcov = curve_fit(model, t, y, p0=p0, maxfev=100000)
    yhat = model(t, *popt)
    rss, aic, bic = aic_bic(y, yhat, len(popt))
    names = ["A","w","phi","C"] + (["kappa"] if model is helical_model else [])
    params = {n: float(v) for n, v in zip(names, popt)}
    return FitResult(params=params, rss=rss, aic=aic, bic=bic, cov=pcov)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--tcol", default="t")
    ap.add_argument("--ycol", default="y")
    ap.add_argument("--out", default="./out")
    args = ap.parse_args()

    import pandas as pd
    df = pd.read_csv(args.csv)
    t = df[args.tcol].to_numpy(dtype=float)
    y = df[args.ycol].to_numpy(dtype=float)

    os.makedirs(args.out, exist_ok=True)

    # Initial guesses (tune as needed or make automatic from data moments)
    A0 = 0.5 * (np.percentile(y, 95) - np.percentile(y, 5))
    w0 = 2*np.pi / (t[-1] - t[0] + 1e-9)
    phi0 = 0.0
    C0 = float(np.mean(y))
    kappa0 = 0.0

    sin_res = fit_model(sine_model, t, y, p0=[A0, w0, phi0, C0])
    hel_res = fit_model(helical_model, t, y, p0=[A0, w0, phi0, C0, kappa0])

    # Report
    import json
    with open(os.path.join(args.out, "fit_report.json"), "w") as f:
        json.dump({
            "sine": sin_res.__dict__,
            "helical": hel_res.__dict__,
            "delta": {
                "AIC": hel_res.aic - sin_res.aic,
                "BIC": hel_res.bic - sin_res.bic
            }
        }, f, indent=2)

    # Quick plots
    import matplotlib.pyplot as plt
    plt.figure()
    plt.scatter(t, y, s=8)
    t_f = np.linspace(t.min(), t.max(), 1000)
    plt.plot(t_f, sine_model(t_f, **sin_res.params))
    plt.title("Sine fit")
    plt.savefig(os.path.join(args.out, "sine_fit.png"), dpi=150)

    plt.figure()
    plt.scatter(t, y, s=8)
    plt.plot(t_f, helical_model(t_f, **hel_res.params))
    plt.title("Helical fit (κ)")
    plt.savefig(os.path.join(args.out, "helical_fit.png"), dpi=150)

if __name__ == "__main__":
    main()
