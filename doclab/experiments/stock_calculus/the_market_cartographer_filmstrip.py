"""
Market Migration Filmstrip
--------------------------
Computes rolling intrinsic κ (torsion in (Price, Volume, t)) and rolling
performance for each asset, then renders an animated phase-space
(κ vs log-return) GIF over time.

Input
-----
- A directory tree containing per-asset CSV/TXT files with columns:
  Close, Volume
  (Same expectations as `the_market_cartographer.py`.)

Usage
-----
python market_migration_filmstrip.py --data_dir /path/to/data --window 252 --step 21 \
    --out_gif /path/to/out.gif --out_csv /path/to/panel.csv

Notes
-----
- window is the rolling window size (rows); step is the hop between frames.
- Median κ across assets per frame sets the vertical split; y=0 is the horizontal split.
- The animation uses default matplotlib colors (no explicit palette).
"""

import argparse
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def load_asset_series(path):
    try:
        df = pd.read_csv(path)
    except Exception:
        try:
            df = pd.read_csv(path, sep=None, engine="python")
        except Exception:
            return None
    cols = {c.lower(): c for c in df.columns}
    if "close" not in cols or "volume" not in cols:
        return None
    
    # --- Start of fix ---
    # Select the relevant columns and rename them
    s = df[[cols["close"], cols["volume"]]].copy()
    s.rename(columns={cols["close"]:"Close", cols["volume"]:"Volume"}, inplace=True)
    
    # Explicitly convert columns to numeric, turning errors into NaN
    s["Close"] = pd.to_numeric(s["Close"], errors='coerce')
    s["Volume"] = pd.to_numeric(s["Volume"], errors='coerce')
    
    # Drop any rows that now contain NaN
    s.dropna(inplace=True)
    # --- End of fix ---

    if len(s) < 100:
        return None
    return s.reset_index(drop=True)

def normalize_minmax(x):
    s = pd.to_numeric(pd.Series(x), errors="coerce")
    x = s[pd.notna(s)].values
    xmin, xmax = np.min(x), np.max(x)
    if xmax - xmin == 0:
        return None
    return 2 * ((x - xmin) / (xmax - xmin)) - 1

def intrinsic_kappa_from_series(price, volume):
    t = np.linspace(0, 1, len(price))
    r = np.vstack([price, volume, t]).T
    dr = np.gradient(r, axis=0)
    d2r = np.gradient(dr, axis=0)
    d3r = np.gradient(d2r, axis=0)
    cross = np.cross(dr, d2r)
    num = np.einsum('ij,ij->i', cross, d3r)
    den = np.sum(cross**2, axis=1)
    torsion = np.zeros_like(den)
    valid = den > 1e-9
    torsion[valid] = num[valid] / den[valid]
    return float(np.mean(np.abs(torsion)) * 100.0)

def rolling_panels(data_paths, window=252, step=21):
    # Build aligned windows per asset independently; then assemble panels by frame index.
    per_asset = {}
    for p in data_paths:
        s = load_asset_series(p)
        if s is None: 
            continue
        closes = s["Close"].values
        vols = s["Volume"].values
        n = len(s)
        frames = []
        for start in range(0, n - window + 1, step):
            end = start + window
            # κ on normalized window
            np_norm = normalize_minmax(closes[start:end])
            nv_norm = normalize_minmax(vols[start:end])
            if np_norm is None or nv_norm is None:
                continue
            kappa = intrinsic_kappa_from_series(np_norm, nv_norm)
            # performance on raw window
            c0, c1 = closes[start], closes[end-1]
            if c0 <= 0 or c1 <= 0:
                perf = np.nan
            else:
                perf = float(np.log(c1 / c0))
            frames.append((start, end-1, kappa, perf))
        if frames:
            df = pd.DataFrame(frames, columns=["t_start","t_end","kappa","performance"])
            df["asset"] = Path(p).name
            per_asset[p] = df
    if not per_asset:
        return pd.DataFrame()
    panel = pd.concat(per_asset.values(), ignore_index=True)
    # define a global frame index from (t_end, step) bins for alignment
    panel["frame"] = panel.groupby("asset").cumcount()
    return panel

def make_animation(panel, out_gif, fps=6):
    if panel.empty:
        raise ValueError("Empty panel; no frames to animate.")
    # Prepare figure
    fig, ax = plt.subplots(figsize=(8, 6))
    frames = int(panel["frame"].max()) + 1

    scat = ax.scatter([], [])
    vline = ax.axvline(0)
    hline = ax.axhline(0)
    title = ax.set_title("")
    ax.set_xlabel("Intrinsic Chirality (κ)")
    ax.set_ylabel("Performance (log return)")

    def init():
        scat.set_offsets(np.empty((0,2)))
        return scat, vline, hline, title

    def animate(i):
        sub = panel[panel["frame"] == i]
        x = sub["kappa"].values
        y = sub["performance"].values
        if len(x) == 0:
            offsets = np.empty((0,2))
            k_med = 0.0
        else:
            offsets = np.column_stack([x, y])
            k_med = float(np.nanmedian(x))
        scat.set_offsets(offsets)
        # update lines
        vline.set_xdata(k_med)
        hline.set_ydata(0.0)
        title.set_text(f"Market Phase-Space Migration — Frame {i+1}/{frames}")
        # autoscale softly
        if len(x) > 0:
            ax.set_xlim(float(np.nanmin(x))*0.95, float(np.nanmax(x))*1.05)
            ax.set_ylim(float(np.nanmin(y))*1.05, float(np.nanmax(y))*1.05)
        return scat, vline, hline, title

    anim = FuncAnimation(fig, animate, init_func=init, frames=frames, interval=1000//fps, blit=False)
    writer = PillowWriter(fps=fps)
    anim.save(out_gif, writer=writer)
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True, help="Directory with per-asset files")
    ap.add_argument("--window", type=int, default=252, help="Rolling window length")
    ap.add_argument("--step", type=int, default=21, help="Hop between frames")
    ap.add_argument("--out_gif", default="market_phase_space_migration.gif", help="Output GIF path")
    ap.add_argument("--out_csv", default="market_migration_panel.csv", help="Output CSV (long format)")
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    paths = [str(p) for p in data_dir.rglob("*") if p.suffix.lower() in [".csv", ".txt"]]

    panel = rolling_panels(paths, window=args.window, step=args.step)
    if panel.empty:
        print("No usable time-series found (need Close, Volume, >=100 rows per file).")
        return

    panel.to_csv(args.out_csv, index=False)
    print(f"Panel saved: {args.out_csv}  (rows: {len(panel)})")

    make_animation(panel, args.out_gif, fps=6)
    print(f"GIF saved: {args.out_gif}")

if __name__ == "__main__":
    main()

