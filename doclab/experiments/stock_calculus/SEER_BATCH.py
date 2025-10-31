# SEER-BATCH — Pirouette Helical Indexer for Local Stock Files
# id: INST-WAVEFORM-ANALYZER-004
# version: 1.0
# parents: [DOMA-206, MATH-028, INST-WAVEFORM-ANALYZER-003]
#
# Purpose:
# - Batch over a folder of local CSV/TXT OHLC files (with 'Close' column)
# - For each file, compute:
#     * optimal κ (chirality) by coherence-minimizing helical projection
#     * coherence score at κ=0 and at κ*
#     * Δcoherence = score(κ=0) - score(κ*)
#     * Frenet–Serret mean torsion |τ_fs| on the κ*-projected 3D curve
#     * Winding rate via unwrapped azimuth θ(t)
#     * Baseline sine-vs-helix residuals (RMSE, AIC, BIC) on a central segment
# - Save a master index CSV for ranking and downstream mining.
#
# Notes:
# - Uses only local files; no internet/API.
# - One plot per figure rule is easy to honor if plotting is requested; here we compute only.
# - Designed to align with your "The Seer" local-file instrument.
#
# Output:
# - /mnt/data/seer_batch_index.csv (per-file metrics)
# - /mnt/data/seer_batch_diagnostics/<TICKER>/*.csv (optional traces if desired)

import os, csv, math, glob, json
import numpy as np
import pandas as pd

# ------------------------ core math ------------------------

def normalize(series):
    x = np.asarray(series, dtype=float)
    x = x - np.nanmean(x)
    denom = np.nanmax(np.abs(x)) + 1e-12
    return x / denom

def helical_projection(sig, kappa):
    n = len(sig)
    t = np.arange(n, dtype=float)
    x = sig * np.cos(kappa * t)
    y = sig * np.sin(kappa * t)
    z = t / max(1, (n-1))
    return np.vstack([x, y, z]).T

def coherence_score(curve3d):
    v = np.diff(curve3d, axis=0)
    a = np.diff(v, axis=0)
    return float(np.sum(np.linalg.norm(a, axis=1)**2))

def frenet_serret(curve):
    r = curve
    r1 = np.diff(r, axis=0)
    r2 = np.diff(r1, axis=0)
    r3 = np.diff(r2, axis=0)
    r1c = r1[:-1]
    cross12 = np.cross(r1c, r2)
    kappa_fs = np.linalg.norm(cross12, axis=1) / (np.linalg.norm(r1c, axis=1)**3 + 1e-12)
    r1t = r1[1:-1]; r2t = r2[:-1]
    cross = np.cross(r1t, r2t)
    num_t = np.einsum('ij,ij->i', cross, r3)
    den_t = (np.linalg.norm(cross, axis=1)**2 + 1e-12)
    tau_fs = num_t / den_t
    return kappa_fs, tau_fs

def winding_rate(curve):
    x, y = curve[:,0], curve[:,1]
    theta = np.unwrap(np.arctan2(y, x))
    dtheta = np.diff(theta)
    return float(np.mean(dtheta))

def best_sine_fit_stats(signal):
    n = len(signal)
    t = np.arange(n)
    freq = np.fft.rfftfreq(n, d=1.0)
    mag = np.abs(np.fft.rfft(signal))
    idx = int(np.argmax(mag[1:]) + 1) if len(mag) > 1 else 0
    w0 = 2*np.pi*freq[idx] if idx < len(freq) else 0.0
    S = np.sin(w0*t); C = np.cos(w0*t)
    X = np.column_stack([S, C, np.ones(n)])
    coeff, *_ = np.linalg.lstsq(X, signal, rcond=None)
    a, b, c = coeff
    pred = a*S + b*C + c
    rss = float(np.sum((signal - pred)**2))
    rmse = float(np.sqrt(rss / max(1, n)))
    k = 3
    aic = n * np.log(rss / max(1, n) + 1e-12) + 2*k
    bic = n * np.log(rss / max(1, n) + 1e-12) + k*np.log(max(1, n))
    return {"w": w0, "pred": pred, "rmse": rmse, "aic": aic, "bic": bic}

def helical_fit_stats(signal, kappa):
    curve = helical_projection(signal, kappa)
    recon = curve[:,0]
    n = len(signal)
    rss = float(np.sum((signal - recon)**2))
    rmse = float(np.sqrt(rss / max(1, n)))
    k = 1  # only κ as parameter (amplitude baked by normalization)
    aic = n * np.log(rss / max(1, n) + 1e-12) + 2*k
    bic = n * np.log(rss / max(1, n) + 1e-12) + k*np.log(max(1, n))
    return {"pred": recon, "rmse": rmse, "aic": aic, "bic": bic}

def scan_kappa(signal, kmin=0.0, kmax=0.5, steps=300):
    kappas = np.linspace(kmin, kmax, steps)
    scores = np.empty_like(kappas)
    for i, k in enumerate(kappas):
        curve = helical_projection(signal, k)
        scores[i] = coherence_score(curve)
    idx = int(np.argmin(scores))
    return float(kappas[idx]), kappas, scores

# ------------------------ IO helpers ------------------------

def read_close_series(path):
    df = pd.read_csv(path)
    if 'Close' not in df.columns:
        raise ValueError(f"'Close' column not found in {path}")
    series = pd.to_numeric(df['Close'], errors='coerce')
    series = series.dropna().values
    return series

def analyze_file(path, segment_len=1024):
    # load and normalize
    close = read_close_series(path)
    signal = normalize(close)
    n = len(signal)
    if n < 100:
        raise ValueError("Too few samples")

    # κ scan full series
    k_opt, kappas, scores = scan_kappa(signal, 0.0, 0.5, 300)
    # coherence at 0 and optimal
    score0 = float(scores[0])
    score_opt = float(np.min(scores))
    delta_score = score0 - score_opt

    # geometry at κ*
    curve_opt = helical_projection(signal, k_opt)
    _, tau_fs = frenet_serret(curve_opt)
    mean_tau = float(np.mean(np.abs(tau_fs))) if len(tau_fs) > 0 else 0.0
    wind = winding_rate(curve_opt)

    # residuals on central segment
    seg_len = min(segment_len, n)
    start = (n - seg_len) // 2
    seg = signal[start:start+seg_len]
    sine = best_sine_fit_stats(seg)
    helx = helical_fit_stats(seg, k_opt)

    # pack
    ticker = os.path.splitext(os.path.basename(path))[0]
    return {
        "ticker": ticker,
        "n": n,
        "kappa_opt": k_opt,
        "coherence0": score0,
        "coherence_opt": score_opt,
        "delta_coherence": delta_score,
        "mean_abs_torsion": mean_tau,
        "mean_winding_rate": wind,
        "sine_rmse": sine["rmse"],
        "helix_rmse": helx["rmse"],
        "delta_rmse": sine["rmse"] - helx["rmse"],
        "sine_aic": sine["aic"],
        "helix_aic": helx["aic"],
        "delta_aic": sine["aic"] - helx["aic"],
        "sine_bic": sine["bic"],
        "helix_bic": helx["bic"],
        "delta_bic": sine["bic"] - helx["bic"],
        "path": path
    }

# ------------------------ batch run ------------------------

folder = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/stock_calculus/stock_results"
patterns = ["*.us.txt"]
files = []
for pat in patterns:
    files.extend(glob.glob(os.path.join(folder, pat)))

results = []
errors = []
for f in sorted(files)[:200]:  # safety cap
    try:
        res = analyze_file(f)
        results.append(res)
    except Exception as e:
        errors.append({"file": f, "error": str(e)})

index_df = pd.DataFrame(results)
index_path = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/stock_calculus/stock_results/seer_batch_index.csv"
index_df.to_csv(index_path, index=False)
