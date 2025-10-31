#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZIP‑Bench v0.2 — Cross‑modal Collapse‑as‑Learning Runner
========================================================

id: INST-ZIP-002
title: ZIP‑Bench Runner (Images, Text, Timeseries)
version: 0.2
status: experimental-validated
parents: [INST-DIM-001, CORE-DIM-002]
children: [EXP-LEARN-002]
module_type: instrument-protocol
summary: Batch runner for Pirouette's collapse‑as‑learning experiments with adaptive gates, hysteresis corridor, utilities (A1/B1/C1), and cross‑dataset transfer analysis.
keywords: [collapse, entropy, coherence, corridor, transfer, benchmark]

What it does
------------
• Recursively ingests three roots: images (PNG/JPG), text (.txt/.md), and timeseries (.csv).
• Runs the adaptive gate learner with hysteresis (g* and two‑step hold).
• Utilities:
  - A1 (Images): PNG byte‑size reduction at proxy‑SSIM ≥ 0.90.
  - B1 (Text): gzip size reduction of collapsed‑field bytes at unigram KL ≤ 0.05.
  - C1 (Timeseries): spectral entropy reduction; simple 1‑step forecast MSE delta.
• Outputs per‑item logs, per‑domain results, and cross‑dataset transfer stats (are collapses in one set predictive of utility in another?).

CLI examples (Windows paths)
----------------------------
python zip_bench_runner.py \
  --images-root "C:\\Users\\keatw\\OneDrive\\Documents\\Expressions" \
  --txt-root    "C:\\Users\\keatw\\OneDrive\\Documents\\Doclab\\Big_Datasets\\target\\paper\\Pirouette_Volume_6\\doclab\\experiments\\Semantics\\radiant" \
  --csv-root    "C:\\Users\\keatw\\OneDrive\\Documents\\Doclab\\Big_Datasets\\stocks_rightsized\\Data\\Stocks" \
  --csv-col Close --iters 8 --out "C:\\Users\\keatw\\zip_bench_out"

Notes
-----
• Use doubled backslashes or raw strings on Windows. Quotes are recommended.
• The script is self‑contained (no project imports) and uses only PIL, numpy, pandas, matplotlib (optional for plots).
• You can toggle per‑radius learning with --per-radius.
"""

from __future__ import annotations
import os, io, math, gzip, glob, argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Optional

import numpy as np
import pandas as pd
from PIL import Image

# ------------------------------
# Small utils
# ------------------------------

def ensure_dir(p: str):
    if p and not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

def slugify(s: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in s)

# ------------------------------
# Geometry & collapse core
# ------------------------------

def polar_grid(n: int = 192, r_max: float = 1.0):
    lin = np.linspace(-r_max, r_max, n)
    x, y = np.meshgrid(lin, lin)
    r = np.sqrt(x*x + y*y) + 1e-12
    theta = np.arctan2(y, x)
    return x, y, r, theta

def helical_time_evolve(field: np.ndarray, kappa: float, t: float = 6.0, omega: float = 2*math.pi*1.0) -> np.ndarray:
    gx, _ = np.gradient(field)
    return np.cos(kappa*omega*t)*field + np.sin(kappa*omega*t)*gx

def signed_angular_gradient(field: np.ndarray, theta: np.ndarray) -> np.ndarray:
    gx, gy = np.gradient(field)
    tx, ty = -np.sin(theta), np.cos(theta)
    return gx*tx + gy*ty

def dominant_mode_signed(field: np.ndarray, theta: np.ndarray, max_m: int = 8, r_mask_inner: int = 4) -> Tuple[int, np.ndarray]:
    s = signed_angular_gradient(field, theta)
    s = s - s.mean()
    n = s.shape[0]; c = n//2
    rr = np.sqrt((np.indices(s.shape)[0]-c)**2 + (np.indices(s.shape)[1]-c)**2)
    mask = rr > r_mask_inner
    amps = []
    for m in range(1, max_m+1):
        c0 = np.sum(s[mask]*np.cos(m*theta[mask]))
        s0 = np.sum(s[mask]*np.sin(m*theta[mask]))
        amps.append((m, float(np.hypot(c0, s0))))
    amps.sort(key=lambda t: t[1], reverse=True)
    return int(amps[0][0]), s

def proj_mode(field: np.ndarray, theta: np.ndarray, m: int) -> Tuple[float, np.ndarray]:
    b = np.cos(m*theta)
    coef = np.sum(field*b) / (np.sum(b*b) + 1e-12)
    return float(coef), b

def energy_L2(field: np.ndarray) -> float:
    return float(np.sqrt(np.mean(field**2) + 1e-12))

def gate_from_params(Ta: float, Gamma: float) -> float:
    g_lin = np.clip((1.0 - Ta)*Gamma, 0.0, 1.0)
    return float(1.0 - math.exp(-3.0 * g_lin))

def Ta_from_gate(g: float, Gamma: float) -> float:
    if g <= 0.0: return 1.0
    if g >= 1.0: return 0.0
    one_minus_Ta = - math.log(1.0 - g) / (3.0*Gamma + 1e-12)
    return float(np.clip(1.0 - one_minus_Ta, 0.0, 1.0))

# ------------------------------
# Entropy & utilities
# ------------------------------

def entropy_image_field(field: np.ndarray, bins: int = 64) -> float:
    f = np.clip(field, -1.0, 1.0)
    hist, _ = np.histogram(f, bins=bins, range=(-1,1), density=True)
    p = hist / (hist.sum() + 1e-12); p = p[p>0]
    return float(-(p*np.log2(p)).sum())

def entropy_text_bytes(data: bytes, bins: int = 256) -> float:
    if len(data)==0: return 0.0
    arr = np.frombuffer(data, dtype=np.uint8)
    hist, _ = np.histogram(arr, bins=bins, range=(0,256), density=False)
    p = hist / (hist.sum() + 1e-12); p = p[p>0]
    return float(-(p*np.log2(p)).sum())

# PNG byte size at proxy‑SSIM ≥ thresh (Pearson corr proxy)
from PIL import Image

def to_png_bytes_from_field(field: np.ndarray) -> int:
    f = np.clip((field + 1.0) * 127.5, 0, 255).astype(np.uint8)
    im = Image.fromarray(f, mode="L")
    bio = io.BytesIO(); im.save(bio, format="PNG", optimize=True)
    return len(bio.getvalue())

def pearson_corr(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float64); b = b.astype(np.float64)
    a = (a - a.mean())/(a.std()+1e-12)
    b = (b - b.mean())/(b.std()+1e-12)
    return float(np.clip(np.mean(a*b), -1.0, 1.0))

# gzip helper & KL

def gzip_size(b: bytes, level: int = 6) -> int:
    bio = io.BytesIO()
    with gzip.GzipFile(fileobj=bio, mode="wb", compresslevel=level) as gz:
        gz.write(b)
    return len(bio.getvalue())

def unigram_kl(p_counts: np.ndarray, q_counts: np.ndarray) -> float:
    p = p_counts / (p_counts.sum() + 1e-12)
    q = q_counts / (q_counts.sum() + 1e-12)
    eps = 1e-12
    return float(np.sum(p * np.log((p + eps)/(q + eps))))

# ------------------------------
# Feature mappers
# ------------------------------

def image_to_field(path: str, size: int = 192) -> np.ndarray:
    img = Image.open(path).convert("L").resize((size, size))
    arr = np.array(img).astype(np.float32)
    arr = (arr - arr.mean())/(arr.std()+1e-12)
    return np.tanh(arr/2.5)

def text_to_field_and_bytes(path: str, size: int = 192) -> Tuple[np.ndarray, bytes]:
    data = Path(path).read_bytes()
    N = size*size
    buf = data[:N].ljust(N, b"\0")
    arr = np.frombuffer(buf, dtype=np.uint8).astype(np.float32).reshape(size, size)
    arr = (arr - arr.mean())/(arr.std()+1e-12)
    return np.tanh(arr/3.0), data

def csv_to_series(path: str, value_col: Optional[str] = None) -> np.ndarray:
    import csv
    # try pandas if available for convenience; fall back to csv
    try:
        df = pd.read_csv(path)
        if value_col and value_col in df.columns:
            s = df[value_col].to_numpy()
        else:
            # last numeric column
            nums = [c for c in df.columns if np.issubdtype(df[c].dtype, np.number)]
            if not nums: raise ValueError("No numeric column")
            s = df[nums[-1]].to_numpy()
    except Exception:
        vals = []
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            cols = reader.fieldnames or []
            pick = value_col or (cols[-1] if cols else None)
            for row in reader:
                try:
                    vals.append(float(row[pick]))
                except Exception:
                    continue
        s = np.array(vals, dtype=np.float32)
    s = s.astype(np.float32)
    s = (s - np.mean(s))/(np.std(s)+1e-12)
    return s

# Map 1D series into polar field

def timeseries_to_field(series: np.ndarray, size: int = 192) -> np.ndarray:
    x,y,r,theta = polar_grid(size, 1.0)
    env = np.exp(-(r**2)/(0.6**2))
    steps = max(1, series.shape[0])
    idx = ((theta + math.pi)/(2*math.pi) * steps).astype(int) % steps
    arr = series[idx] * env
    return np.tanh(arr)

# ------------------------------
# Collapse variants
# ------------------------------

def collapse_global(field: np.ndarray, theta: np.ndarray, g: float) -> Tuple[np.ndarray, int, float]:
    m_pre, _ = dominant_mode_signed(field, theta)
    c_dom, b_dom = proj_mode(field, theta, m_pre)
    removed = g * c_dom * b_dom
    remainder = field - removed
    c2, b2 = proj_mode(remainder, theta, 2)
    E_removed = energy_L2(removed)
    b2u = b2 / (energy_L2(b2)+1e-12)
    refill = E_removed * b2u * np.sign(c2 if abs(c2)>1e-8 else 1.0)
    out = remainder + refill
    m_post, _ = dominant_mode_signed(out, theta)
    Eb = abs(energy_L2(field) - energy_L2(out))
    return out, m_post, Eb

# Optional per‑radius fold

def collapse_per_radius(field: np.ndarray, theta: np.ndarray, g: float, r_bins: int = 6) -> Tuple[np.ndarray, int, float]:
    n = field.shape[0]; c = n//2
    rr = np.sqrt((np.indices(field.shape)[0]-c)**2 + (np.indices(field.shape)[1]-c)**2)
    r_norm = rr/(rr.max()+1e-12)
    edges = np.linspace(0.0, 1.0, r_bins+1)
    out = field.copy()
    for i in range(r_bins):
        mask = (r_norm >= edges[i]) & (r_norm < edges[i+1])
        if not np.any(mask):
            continue
        m_loc, _ = dominant_mode_signed(out*mask, theta)
        c_dom, b_dom = proj_mode(out, theta, m_loc)
        removed = g * c_dom * b_dom * mask
        remainder = out - removed
        c2, b2 = proj_mode(remainder, theta, 2)
        E_removed = energy_L2(removed)
        b2u = b2 / (energy_L2(b2)+1e-12)
        refill = E_removed * b2u * np.sign(c2 if abs(c2)>1e-8 else 1.0)
        out = remainder + refill*mask
    m_post, _ = dominant_mode_signed(out, theta)
    Eb = abs(energy_L2(field) - energy_L2(out))
    return out, m_post, Eb

# ------------------------------
# Learner with hysteresis & optional per‑radius
# ------------------------------

def learn_sequence(field0: np.ndarray, size: int = 192, kappa: float = 0.9, Gamma: float = 0.88, g0: float = 0.45,
                   alpha: float = 0.15, iters: int = 8, g_star: float = 0.6, per_radius: bool = False, r_bins: int = 6,
                   entropy_kind: str = "image") -> Tuple[pd.DataFrame, np.ndarray]:
    x,y,r,theta = polar_grid(size, 1.0)
    field = field0.copy()
    g = float(np.clip(g0, 0.0, 1.0))
    hold = 0; t_to_corr = -1
    logs: List[Dict[str, float]] = []

    for t in range(iters):
        Ta = Ta_from_gate(g, Gamma)
        # evolve
        evolved = helical_time_evolve(field, kappa, t=6.0)
        # entropy pre (proxy: field entropy)
        H_pre = entropy_image_field(evolved) if entropy_kind != "text_bytes" else entropy_image_field(evolved)
        # gate for this step
        g_eff = gate_from_params(Ta, Gamma)
        # collapse step
        if per_radius:
            collapsed, m_post, Eb = collapse_per_radius(evolved, theta, g_eff, r_bins=r_bins)
        else:
            collapsed, m_post, Eb = collapse_global(evolved, theta, g_eff)
        # entropy post (proxy on collapsed field)
        H_post = entropy_image_field(collapsed)
        dI = H_pre - H_post
        # observer gradient & coherence dividend
        Psi_o = (dI / (g_eff + 1e-12))
        C = (dI / (Eb + 1e-3)) * g_eff
        # hysteresis
        if (g_eff >= g_star) and (m_post <= 2):
            hold += 1
            if hold == 2 and t_to_corr < 0:
                t_to_corr = t
        else:
            hold = 0
        # update gate
        g = float(np.clip(g + alpha * Psi_o, 0.0, 1.0))
        field = collapsed
        logs.append({
            "iter": t, "g": g_eff, "Ta": Ta, "Gamma": Gamma, "kappa": kappa,
            "H_pre": H_pre, "H_post": H_post, "dI": dI,
            "m_post": int(m_post), "Eb": Eb, "Psi_o": Psi_o, "C": C,
            "t_to_corr": int(t_to_corr)
        })
    return pd.DataFrame(logs), field

# ------------------------------
# Utilities per domain
# ------------------------------

def util_image_A1(pre_field: np.ndarray, post_field: np.ndarray, corr_thresh: float = 0.90) -> Tuple[float, float, bool]:
    corr = pearson_corr(pre_field, post_field)
    pre_sz = to_png_bytes_from_field(pre_field)
    post_sz = to_png_bytes_from_field(post_field)
    bpp_red = (pre_sz - post_sz) / max(pre_sz, 1)
    ok = (corr >= corr_thresh)
    return float(bpp_red), float(corr), bool(ok)

def util_text_B1(orig_bytes: bytes, post_field: np.ndarray, kl_thresh: float = 0.05) -> Tuple[float, float, bool]:
    fb = np.clip((post_field + 1.0) * 127.5, 0, 255).astype(np.uint8).tobytes()
    gz_orig = gzip_size(orig_bytes)
    gz_post = gzip_size(fb)
    delta_gz = (gz_orig - gz_post) / max(gz_orig, 1)
    arr_o = np.frombuffer(orig_bytes, dtype=np.uint8)
    arr_p = np.frombuffer(fb, dtype=np.uint8)
    hist_o, _ = np.histogram(arr_o, bins=256, range=(0,256), density=False)
    hist_p, _ = np.histogram(arr_p, bins=256, range=(0,256), density=False)
    kl = unigram_kl(hist_o, hist_p)
    ok = (kl <= kl_thresh)
    return float(delta_gz), float(kl), bool(ok)

# Timeseries: spectral entropy & naive forecast MSE delta

def spectral_entropy(series: np.ndarray, bins: int = 64) -> float:
    s = series - series.mean()
    # power spectrum via rfft magnitude
    yf = np.abs(np.fft.rfft(s))
    yf[0] = 0.0
    p = yf / (yf.sum() + 1e-12)
    p = p[p>0]
    return float(-(p*np.log2(p)).sum())


def util_timeseries_C1(series: np.ndarray, post_field: np.ndarray) -> Tuple[float, float]:
    # build a collapsed series proxy: read one ring of the post_field
    n = post_field.shape[0]; c = n//2
    ring = post_field[c, :]  # one diameter as proxy signal
    ring = (ring - ring.mean())/(ring.std()+1e-12)
    # spectral entropy delta (lower is better)
    H_spec_pre = spectral_entropy(series)
    H_spec_post = spectral_entropy(ring)
    d_specH = H_spec_pre - H_spec_post
    # simple 1‑step forecast (AR(1) by OLS)
    def ar1_mse(x: np.ndarray) -> float:
        x = x.astype(np.float64)
        if x.size < 3: return np.inf
        X = x[:-1]; Y = x[1:]
        a = (X@Y) / (X@X + 1e-12)
        pred = a*X
        return float(np.mean((Y - pred)**2))
    mse_pre = ar1_mse(series)
    mse_post = ar1_mse(ring)
    d_mse = mse_pre - mse_post
    return float(d_specH), float(d_mse)

# ------------------------------
# Dataset discovery
# ------------------------------

def discover_files(root: Optional[str], patterns: List[str]) -> List[str]:
    if not root: return []
    found: List[str] = []
    for pat in patterns:
        found += glob.glob(str(Path(root)/"**"/pat), recursive=True)
    # de‑duplicate preserving order
    seen = set(); uniq = []
    for p in found:
        if p not in seen:
            uniq.append(p); seen.add(p)
    return uniq

# ------------------------------
# Runner
# ------------------------------

def run_zip_bench(images_root: Optional[str], txt_root: Optional[str], csv_root: Optional[str], value_col: Optional[str],
                  out_dir: str, size: int = 192, iters: int = 8, per_radius: bool = False, r_bins: int = 6,
                  kappa: float = 0.9, Gamma: float = 0.88, g0: float = 0.45, alpha: float = 0.15, g_star: float = 0.6) -> Dict[str, str]:
    ensure_dir(out_dir)
    plots_dir = str(Path(out_dir)/"plots")
    ensure_dir(plots_dir)

    images = discover_files(images_root, ["*.png", "*.jpg", "*.jpeg"])
    texts  = discover_files(txt_root,    ["*.txt", "*.md"])    
    csvs   = discover_files(csv_root,    ["*.csv"])            

    all_logs: List[pd.DataFrame] = []
    results_rows: List[Dict[str, object]] = []

    # Images
    for p in images:
        try:
            pre_field = image_to_field(p, size=size)
            df, post_field = learn_sequence(pre_field, size=size, kappa=kappa, Gamma=Gamma, g0=g0, alpha=alpha,
                                            iters=iters, g_star=g_star, per_radius=per_radius, r_bins=r_bins,
                                            entropy_kind="image")
            bpp_red, corr, ok = util_image_A1(pre_field, post_field)
            C_sum, Eb_sum = float(df["C"].sum()), float(df["Eb"].sum())
            t_to_corr = int(df.loc[df["t_to_corr"]>=0, "t_to_corr"].min()) if (df["t_to_corr"]>=0).any() else iters+1
            lambda_U, lambda_E, lambda_S = 1.0, 0.1, 0.05
            U = bpp_red if ok else 0.0
            J = C_sum + lambda_U*U - lambda_E*Eb_sum - lambda_S*t_to_corr
            results_rows.append({"item": os.path.basename(p), "kind":"image", "bpp_red": bpp_red, "corr": corr, "ok": ok,
                                 "C_sum": C_sum, "Eb_sum": Eb_sum, "t_to_corr": t_to_corr, "J": J, "path": p})
            df = df.copy(); df["item"] = os.path.basename(p); df["kind"] = "image"; df["path"] = p
            all_logs.append(df)
        except Exception as e:
            print("[image fail]", p, e)

    # Texts
    for p in texts:
        try:
            pre_field, bytes_data = text_to_field_and_bytes(p, size=size)
            df, post_field = learn_sequence(pre_field, size=size, kappa=kappa, Gamma=Gamma, g0=g0, alpha=alpha,
                                            iters=iters, g_star=g_star, per_radius=per_radius, r_bins=r_bins,
                                            entropy_kind="text_bytes")
            delta_gz, kl, ok = util_text_B1(bytes_data, post_field)
            C_sum, Eb_sum = float(df["C"].sum()), float(df["Eb"].sum())
            t_to_corr = int(df.loc[df["t_to_corr"]>=0, "t_to_corr"].min()) if (df["t_to_corr"]>=0).any() else iters+1
            lambda_U, lambda_E, lambda_S = 1.0, 0.1, 0.05
            U = delta_gz if ok else 0.0
            J = C_sum + lambda_U*U - lambda_E*Eb_sum - lambda_S*t_to_corr
            results_rows.append({"item": os.path.basename(p), "kind":"text", "delta_gz": delta_gz, "kl": kl, "ok": ok,
                                 "C_sum": C_sum, "Eb_sum": Eb_sum, "t_to_corr": t_to_corr, "J": J, "path": p})
            df = df.copy(); df["item"] = os.path.basename(p); df["kind"] = "text"; df["path"] = p
            all_logs.append(df)
        except Exception as e:
            print("[text fail]", p, e)

    # Timeseries
    for p in csvs:
        try:
            series = csv_to_series(p, value_col=value_col)
            pre_field = timeseries_to_field(series, size=size)
            df, post_field = learn_sequence(pre_field, size=size, kappa=kappa, Gamma=Gamma, g0=g0, alpha=alpha,
                                            iters=iters, g_star=g_star, per_radius=per_radius, r_bins=r_bins,
                                            entropy_kind="image")
            d_specH, d_mse = util_timeseries_C1(series, post_field)
            C_sum, Eb_sum = float(df["C"].sum()), float(df["Eb"].sum())
            t_to_corr = int(df.loc[df["t_to_corr"]>=0, "t_to_corr"].min()) if (df["t_to_corr"]>=0).any() else iters+1
            # fold into J (utility = normalized sum of positive deltas)
            lambda_U, lambda_E, lambda_S = 1.0, 0.1, 0.05
            U = max(0.0, d_specH) + 0.1*max(0.0, d_mse)
            J = C_sum + lambda_U*U - lambda_E*Eb_sum - lambda_S*t_to_corr
            results_rows.append({"item": os.path.basename(p), "kind":"timeseries", "d_specH": d_specH, "d_mse": d_mse,
                                 "C_sum": C_sum, "Eb_sum": Eb_sum, "t_to_corr": t_to_corr, "J": J, "path": p})
            df = df.copy(); df["item"] = os.path.basename(p); df["kind"] = "timeseries"; df["path"] = p
            all_logs.append(df)
        except Exception as e:
            print("[csv fail]", p, e)

    # Write outputs
    logs_df = pd.concat(all_logs, ignore_index=True) if all_logs else pd.DataFrame()
    results_df = pd.DataFrame(results_rows)
    logs_csv = str(Path(out_dir)/"zip_bench_logs.csv")
    results_csv = str(Path(out_dir)/"zip_bench_results.csv")
    logs_df.to_csv(logs_csv, index=False)
    results_df.to_csv(results_csv, index=False)

    # Cross‑dataset transfer: does C_sum (images) predict utility in text/timeseries?
    xfer_rows = []
    def corr_pair(dfA, xcol, dfB, ycol, label):
        try:
            xa = dfA[xcol].to_numpy().astype(np.float64)
            yb = dfB[ycol].to_numpy().astype(np.float64)
            n = min(xa.size, yb.size)
            if n < 3: return None
            xa, yb = xa[:n], yb[:n]
            x = (xa - xa.mean())/(xa.std()+1e-12)
            y = (yb - yb.mean())/(yb.std()+1e-12)
            r = float(np.mean(x*y))
            xfer_rows.append({"from": xcol+"@images", "to": ycol+f"@{label}", "pearson_r": r, "n": n})
        except Exception:
            return None
    try:
        img = results_df[results_df["kind"]=="image"]
        txt = results_df[results_df["kind"]=="text"]
        ts  = results_df[results_df["kind"]=="timeseries"]
        if not img.empty and not txt.empty:
            corr_pair(img, "C_sum", txt, "delta_gz", "text")
            corr_pair(img, "J",     txt, "delta_gz", "text")
        if not img.empty and not ts.empty:
            corr_pair(img, "C_sum", ts,  "d_specH",  "timeseries")
            corr_pair(img, "J",     ts,  "d_specH",  "timeseries")
        if not txt.empty and not ts.empty:
            corr_pair(txt, "C_sum", ts,  "d_specH",  "timeseries")
            corr_pair(txt, "J",     ts,  "d_specH",  "timeseries")
    except Exception:
        pass
    xfer_df = pd.DataFrame(xfer_rows)
    xfer_csv = str(Path(out_dir)/"zip_bench_transfer.csv")
    xfer_df.to_csv(xfer_csv, index=False)

    return {"logs_csv": logs_csv, "results_csv": results_csv, "transfer_csv": xfer_csv}

# ------------------------------
# CLI
# ------------------------------

def main():
    ap = argparse.ArgumentParser(description="ZIP‑Bench v0.2 Runner — Pirouette collapse‑as‑learning")
    ap.add_argument("--images-root", type=str, default=None, help="root folder of images (PNG/JPG)")
    ap.add_argument("--txt-root",    type=str, default=None, help="root folder of text files (.txt, .md)")
    ap.add_argument("--csv-root",    type=str, default=None, help="root folder of CSV time series")
    ap.add_argument("--csv-col",     type=str, default=None, help="value column for CSV (e.g., Close)")
    ap.add_argument("--out",         type=str, default="zip_bench_out")
    ap.add_argument("--size",        type=int, default=192)
    ap.add_argument("--iters",       type=int, default=8)
    ap.add_argument("--per-radius",  action="store_true", help="enable per‑radius folding")
    ap.add_argument("--r-bins",      type=int, default=6)
    ap.add_argument("--kappa",       type=float, default=0.9)
    ap.add_argument("--Gamma",       type=float, default=0.88)
    ap.add_argument("--g0",          type=float, default=0.45)
    ap.add_argument("--alpha",       type=float, default=0.15)
    ap.add_argument("--g-star",      type=float, default=0.6)
    args = ap.parse_args()

    outs = run_zip_bench(images_root=args.images_root, txt_root=args.txt_root, csv_root=args.csv_root,
                         value_col=args.csv_col, out_dir=args.out, size=args.size, iters=args.iters,
                         per_radius=args.per_radius, r_bins=args.r_bins, kappa=args.kappa, Gamma=args.Gamma,
                         g0=args.g0, alpha=args.alpha, g_star=args.g_star)
    print("Wrote:")
    for k,v in outs.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
