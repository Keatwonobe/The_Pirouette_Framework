#!/usr/bin/env python3
"""
analyze_archetypes_2_chunked_v2.py — chunked analyzer with robust NaN/Inf handling and dtype fixes.
"""
import argparse, sys, math, random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.stats import gaussian_kde

def coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors='coerce')

def detect_columns(first_chunk: pd.DataFrame, kappa_arg: Optional[str], power_arg: Optional[str]) -> Tuple[str, str]:
    if kappa_arg and power_arg:
        return kappa_arg, power_arg
    cols = {c.lower(): c for c in first_chunk.columns}
    for kcand in ['kappa_abs','intrinsic_kappa','kappa','kappa_val']:
        if kcand in cols:
            k = cols[kcand]
            break
    else:
        raise ValueError("Could not find a kappa-like column. Use --kappa-col.")
    for pcand in ['delta_power','performance_score','power','score','delta']:
        if pcand in cols:
            p = cols[pcand]
            break
    else:
        raise ValueError("Could not find a power-like column. Use --power-col.")
    return k, p

def reservoir_append(res: List[Tuple[float, float]], incoming: pd.DataFrame, kcol: str, pcol: str, kmax: int, rng: random.Random, counter: List[int]):
    for _, row in incoming.iterrows():
        k = row[kcol]
        p = row[pcol]
        if k is None or p is None or math.isnan(k) or math.isnan(p):
            counter[0] += 1
            continue
        if len(res) < kmax:
            res.append((k, p))
        else:
            j = rng.randint(0, counter[0])
            if j < kmax:
                res[j] = (k, p)
        counter[0] += 1

def compute_quantiles(sample: List[Tuple[float, float]]) -> Tuple[float, Tuple[float, float]]:
    ks = np.array([t[0] for t in sample], dtype=float)
    ps = np.array([t[1] for t in sample], dtype=float)
    k_median = float(np.nanmedian(ks))
    y_q = (float(np.nanquantile(ps, 0.01)), float(np.nanquantile(ps, 0.99)))
    return k_median, y_q

def archetype_from_row(k: float, p: float, k_boundary: float) -> str:
    if p > 0 and k > k_boundary:
        return 'Gladiator'
    if p > 0 and k <= k_boundary:
        return 'Weaver'
    if p <= 0 and k > k_boundary:
        return 'Vortex'
    return 'Drifter'

def main():
    ap = argparse.ArgumentParser(description="Chunked archetype analyzer for very large CSVs (memory-safe).")
    ap.add_argument('--data', required=True, help="Path to combined CSV")
    ap.add_argument('--outdir', default='fractal_analysis', help="Output directory")
    ap.add_argument('--chunksize', type=int, default=200_000, help="Rows per chunk to stream")
    ap.add_argument('--sample-size', type=int, default=50_000, help="Max reservoir sample size for boundaries & viz")
    ap.add_argument('--kappa-col', default=None, help="Column name for kappa (if auto-detect fails)")
    ap.add_argument('--power-col', default=None, help="Column name for power/performance (if auto-detect fails)")
    ap.add_argument('--random-seed', type=int, default=42, help="Reservoir RNG seed")
    ap.add_argument('--kappa-eps', type=float, default=1e-12, help="Minimum positive kappa before log10")
    args = ap.parse_args()

    data_path = Path(args.data)
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    if not data_path.exists():
        print(f"Error: Data file not found at '{data_path}'", file=sys.stderr); sys.exit(1)

    rng = random.Random(args.random_seed)

    print(f"Loading (stream) from {data_path} ...")
    it = pd.read_csv(data_path, chunksize=args.chunksize, dtype=str, on_bad_lines='skip', low_memory=True)
    try:
        first_chunk = next(it)
    except StopIteration:
        print("Error: CSV appears empty.", file=sys.stderr); sys.exit(1)

    kcol, pcol = detect_columns(first_chunk, args.kappa_col, args.power_col)
    print(f"Using columns: kappa='{kcol}', power='{pcol}'")

    # PASS 1: Global reservoir
    res_counter = [0]
    global_sample: List[Tuple[float, float]] = []
    for df in [first_chunk] + list(it):
        need = [c for c in [kcol, pcol, 'archetype'] if c in df.columns]
        sub = df[need].copy()
        sub[kcol] = coerce_numeric(sub[kcol])
        sub[pcol] = coerce_numeric(sub[pcol])
        reservoir_append(global_sample, sub, kcol, pcol, args.sample_size, rng, res_counter)
    print(f"Reservoir size (global): {len(global_sample)} out of ~{res_counter[0]} rows seen.")
    if len(global_sample) < 100:
        print("Warning: very small sample; results may be unstable.", file=sys.stderr)

    k_median, y_quant = compute_quantiles(global_sample)
    print(f"Estimated kappa median: {k_median:.6g}; y-quantiles (1%,99%): {y_quant}")

    # PASS 2: per-archetype samples
    per_type_samples: Dict[str, List[Tuple[float, float]]] = {
        'Gladiator': [], 'Weaver': [], 'Vortex': [], 'Drifter': []
    }
    per_type_cap = max(8_000, args.sample_size // 4)

    it2 = pd.read_csv(data_path, chunksize=args.chunksize, dtype=str, on_bad_lines='skip', low_memory=True)
    for df in it2:
        need = [c for c in [kcol, pcol, 'archetype'] if c in df.columns]
        sub = df[need].copy()
        sub[kcol] = coerce_numeric(sub[kcol])
        sub[pcol] = coerce_numeric(sub[pcol])

        # Ensure 'archetype' is object dtype to avoid FutureWarnings/incompatible dtype sets
        if 'archetype' in sub.columns:
            sub['archetype'] = sub['archetype'].astype('object')
            mapping = {
                "Stable Order": "Weaver",
                "Chaotic Order": "Gladiator",
                "Stable Decay": "Drifter",
                "Chaotic Decay": "Vortex"
            }
            sub['archetype'] = sub['archetype'].replace(mapping)
            mask_bad = ~sub['archetype'].isin(['Gladiator','Weaver','Vortex','Drifter'])
            if mask_bad.any():
                sub.loc[mask_bad, 'archetype'] = sub.loc[mask_bad].apply(
                    lambda r: archetype_from_row(r[kcol], r[pcol], k_median), axis=1
                ).astype('object')
        else:
            sub['archetype'] = sub.apply(lambda r: archetype_from_row(r[kcol], r[pcol], k_median), axis=1).astype('object')

        # Append to per-type reservoirs
        local_count = 0
        for name, grp in sub.groupby('archetype'):
            if name not in per_type_samples:
                continue
            for _, row in grp.iterrows():
                k = row[kcol]; p = row[pcol]
                if k is None or p is None or math.isnan(k) or math.isnan(p):
                    continue
                arr = per_type_samples[name]
                if len(arr) < per_type_cap:
                    arr.append((k, p))
                else:
                    j = rng.randint(0, local_count + 1)
                    if j < per_type_cap:
                        arr[j] = (k, p)
                local_count += 1

    work_rows = []
    for name, pts in per_type_samples.items():
        for (k, p) in pts:
            work_rows.append({'kappa_abs': float(k), 'delta_power': float(p), 'archetype': name})
    if not work_rows:
        print("Error: no valid data points collected for plotting.", file=sys.stderr); sys.exit(2)
    work_df = pd.DataFrame(work_rows)

    # PLOT 1: 2D convex hulls
    print("Generating 2D Convex Hull plot (sampled)...")
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(16, 12))
    for name, grp in work_df.groupby('archetype'):
        ax.scatter(grp['kappa_abs'], grp['delta_power'], s=10, alpha=0.3, label=name)
    for name, grp in work_df.groupby('archetype'):
        if len(grp) < 3: continue
        try:
            pts = grp[['kappa_abs','delta_power']].to_numpy()
            hull = ConvexHull(pts)
            for simplex in hull.simplices:
                ax.plot(pts[simplex,0], pts[simplex,1], lw=2, alpha=0.9)
        except Exception as e:
            print(f"[WARN] Hull failed for {name}: {e}")
    ax.set_xlabel('Kappa (κ) Axis → Torsion / Shear', fontsize=14, color='white')
    ax.set_ylabel('Performance Axis → Tension / Compression', fontsize=14, color='white')
    ax.set_title('The Fourfold Fractal: Archetype Boundaries in Phase Space (Sampled)', fontsize=18, color='white')
    ax.axhline(0, color='gray', linestyle='--', lw=1)
    ax.axvline(k_median, color='gray', linestyle='--', lw=1)
    ax.set_xscale('log')
    ax.set_ylim(y_quant[0], y_quant[1])
    ax.grid(True, which="both", ls="--", color='gray', alpha=0.3)
    ax.legend(loc='upper right', fontsize=12)
    fig.tight_layout()
    out2d = outdir / "fractal_edges_2D.png"
    plt.savefig(out2d, dpi=150)
    print(f"[OK] Saved 2D hull plot: {out2d}")

    # PLOT 2: 3D KDE landscape (robust sanitization)
    print("Generating 3D Probability Landscape plot (sampled)...")
    kde_n = min(25_000, len(work_df))
    kde_sample = work_df.sample(n=kde_n, random_state=42) if len(work_df) > kde_n else work_df.copy()

    kappa = kde_sample['kappa_abs'].to_numpy(dtype=float)
    power = kde_sample['delta_power'].to_numpy(dtype=float)

    # Positivity guard for log10: clamp tiny/zero values to epsilon and drop non-finite
    eps = max(args.kappa_eps, 1e-15)
    mask_pos = np.isfinite(kappa) & (kappa > 0.0) & np.isfinite(power)
    kappa = kappa[mask_pos]
    power = power[mask_pos]
    if kappa.size == 0:
        print("[WARN] No finite positive kappa values for 3D plot; skipping KDE and saving only 2D plot.")
        return

    x = np.log10(np.clip(kappa, eps, None))
    y = power.copy()

    # Drop any remaining non-finite values
    finite_mask = np.isfinite(x) & np.isfinite(y)
    x = x[finite_mask]; y = y[finite_mask]
    if x.size < 50:
        print("[WARN] Too few finite points for KDE; falling back to coarse 2D histogram.")
        use_kde = False
    else:
        use_kde = True

    xmin, xmax = np.nanquantile(x, 0.01), np.nanquantile(x, 0.99)
    ymin, ymax = np.nanquantile(y, 0.01), np.nanquantile(y, 0.99)
    # Guard against identical limits
    if not np.isfinite(xmin) or not np.isfinite(xmax) or xmin == xmax:
        xmin, xmax = float(np.nanmin(x)), float(np.nanmax(x))
    if not np.isfinite(ymin) or not np.isfinite(ymax) or ymin == ymax:
        ymin, ymax = float(np.nanmin(y)), float(np.nanmax(y))

    if not (np.isfinite(xmin) and np.isfinite(xmax) and np.isfinite(ymin) and np.isfinite(ymax)):
        print("[WARN] Non-finite plot ranges; skipping 3D plot.")
        return

    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    if use_kde:
        values = np.vstack([x, y])
        try:
            kernel = gaussian_kde(values)
            Z = np.reshape(kernel(np.vstack([X.ravel(), Y.ravel()])).T, X.shape)
        except Exception as e:
            print(f"[WARN] KDE failed ({e}); using 2D histogram density instead.")
            use_kde = False

    if not use_kde:
        Z, xedges, yedges = np.histogram2d(x, y, bins=100, density=True,
                                           range=[[xmin, xmax],[ymin, ymax]])
        X, Y = np.meshgrid(0.5*(xedges[:-1]+xedges[1:]), 0.5*(yedges[:-1]+yedges[1:]))

    fig = plt.figure(figsize=(18, 14))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(10**X, Y, Z, cmap='plasma', rstride=1, cstride=1, alpha=0.9, edgecolor='none')
    ax.set_xlabel('Kappa (Torsion/Shear)', fontsize=12, labelpad=15)
    ax.set_ylabel('Performance (Tension/Compression)', fontsize=12, labelpad=15)
    ax.set_zlabel('Probability Density (Likelihood of State)', fontsize=12, labelpad=10)
    ax.set_title("The Collapsed Dimension: A 3D View of Reality's Landscape (Sampled)", fontsize=20, pad=20)
    ax.set_xscale('log')
    ax.view_init(elev=35, azim=-65)
    ax.dist = 11
    out3d = outdir / "fractal_landscape_3D.png"
    plt.savefig(out3d, dpi=150)
    plt.close('all')
    print(f"[OK] Saved 3D landscape plot: {out3d}")
    print("--- Analysis Complete (chunked v2) ---")

if __name__ == "__main__":
    main()
