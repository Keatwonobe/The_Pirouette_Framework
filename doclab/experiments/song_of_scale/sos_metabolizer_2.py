
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoS Metabolizer (v2.1, hardened)
- Drops NaN/Inf rows, coerces numeric types
- Skips empty bands safely
- Uses percentile-based axis ranges with small padding
- Four-projection per band + allocation bars + triads plot
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ARCS = ["Weaver","Gladiator","Vortex","Drifter"]

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def find_first(patterns, root: Path):
    files = []
    for pat in patterns:
        files.extend(root.glob(pat))
    return sorted(set(files))

def load_tables(indir: Path):
    windows = find_first(["*_sos_windows.csv"], indir)
    states  = find_first(["*_sos_states.csv"], indir)
    epochs  = find_first(["*_sos_epochs.csv"], indir)
    triadsj = find_first(["*_triads_summary.json"], indir)
    dfw = pd.concat((pd.read_csv(f) for f in windows), ignore_index=True) if windows else pd.DataFrame()
    dfs = pd.concat((pd.read_csv(f) for f in states), ignore_index=True)  if states  else pd.DataFrame()
    dfe = pd.concat((pd.read_csv(f) for f in epochs), ignore_index=True)  if epochs  else pd.DataFrame()
    triads = []
    for tj in triadsj:
        with open(tj, 'r') as f:
            triads.extend(json.load(f))
    dft = pd.DataFrame(triads) if triads else pd.DataFrame()
    return dfw, dfs, dfe, dft

def coerce_clean(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    cols = list(df.columns)
    # force numeric on the critical columns if present
    for c in ["kappa_mag","deltaP","band_lo","band_hi","t0","t1"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # drop NaN/Inf in key columns
    key = [c for c in ["kappa_mag","deltaP","band_lo","band_hi"] if c in df.columns]
    if key:
        df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=key)
    return df

# ---------- Bandwise labeling ----------
def label_band(df_band: pd.DataFrame):
    df = df_band.copy()
    df = coerce_clean(df)
    if df.empty:
        df["state"] = []
        return df, None
    km = df["kappa_mag"].to_numpy()
    dp = df["deltaP"].to_numpy()
    if len(km) < 5:  # not enough to compute quantiles robustly
        df["state"] = "Drifter"
        return df, {"th_k_low": float(np.nan), "th_k_high": float(np.nan), "th_dP": float(np.nan)}
    th_l = float(np.quantile(km, 0.65))
    th_h = float(np.quantile(km, 0.85))
    th_P = float(np.quantile(dp, 0.60))
    state = []
    for k, d in zip(km, dp):
        if d >= th_P and th_l <= k < th_h:
            s = "Weaver"
        elif d >= th_P and k >= th_h:
            s = "Gladiator"
        elif d < 0 and k >= th_h:
            s = "Vortex"
        else:
            s = "Drifter"
        state.append(s)
    df["state"] = state
    return df, {"th_k_low": th_l, "th_k_high": th_h, "th_dP": th_P}

def relabel_all(dfw: pd.DataFrame):
    dfw = coerce_clean(dfw)
    if dfw.empty:
        return dfw, {}
    out = []
    thresholds = {}
    for (blo, bhi), sub in dfw.groupby(["band_lo","band_hi"]):
        labeled, th = label_band(sub)
        if not labeled.empty:
            out.append(labeled)
            thresholds[(blo, bhi)] = th
    if not out:
        return pd.DataFrame(columns=dfw.columns.tolist()+["state"]), thresholds
    return pd.concat(out, ignore_index=True), thresholds

# ---------- Summaries ----------
def summarize(dfw: pd.DataFrame, base_df: pd.DataFrame, outdir: Path):
    out_overall = []
    if not dfw.empty:
        out_overall.append({
            "n_windows": int(len(dfw)),
            "kappa_mag_mean": dfw["kappa_mag"].mean(),
            "kappa_mag_median": dfw["kappa_mag"].median(),
            "deltaP_mean": dfw["deltaP"].mean(),
            "deltaP_median": dfw["deltaP"].median(),
            "n_files": int(dfw["file"].nunique() if "file" in dfw.columns else 0),
            "n_traces": int(dfw["trace"].nunique() if "trace" in dfw.columns else 0),
        })
    else:
        out_overall.append({"n_windows": 0})
    if not base_df.empty and "state" in base_df.columns:
        counts = base_df["state"].value_counts().to_dict()
        out_overall[0].update({f"state_{k}": int(v) for k,v in counts.items()})
    pd.DataFrame(out_overall).to_csv(outdir / "sos_summary_overall.csv", index=False)

    # Per-band stats
    if not dfw.empty:
        grp = dfw.groupby(["band_lo","band_hi"])
        band_stats = grp.agg({
            "kappa_mag":["count","mean","median","std"],
            "deltaP":["mean","median","std"]
        })
        band_stats.columns = ["_".join(c).strip("_") for c in band_stats.columns.to_flat_index()]
        band_stats = band_stats.reset_index()
        if not base_df.empty and "state" in base_df.columns:
            sc = base_df.groupby(["band_lo","band_hi","state"]).size().reset_index(name="count")
            sp = sc.pivot_table(index=["band_lo","band_hi"], columns="state",
                                values="count", fill_value=0).reset_index()
            band_stats = band_stats.merge(sp, on=["band_lo","band_hi"], how="left")
        band_stats.to_csv(outdir / "sos_summary_by_band.csv", index=False)

    # Per-trace-per-band stats
    if not dfw.empty and "file" in dfw.columns and "trace" in dfw.columns:
        grp2 = dfw.groupby(["file","trace","band_lo","band_hi"])
        tb = grp2.agg({
            "kappa_mag":["count","mean","median"],
            "deltaP":["mean","median"]
        })
        tb.columns = ["_".join(c).strip("_") for c in tb.columns.to_flat_index()]
        tb = tb.reset_index()
        if not base_df.empty and "state" in base_df.columns:
            sc2 = base_df.groupby(["file","trace","band_lo","band_hi","state"]).size().reset_index(name="count")
            sp2 = sc2.pivot_table(index=["file","trace","band_lo","band_hi"],
                                  columns="state", values="count", fill_value=0).reset_index()
            tb = tb.merge(sp2, on=["file","trace","band_lo","band_hi"], how="left")
        tb.to_csv(outdir / "sos_summary_by_trace_band.csv", index=False)

# ---------- Plots ----------
def _axis_limits(d: pd.DataFrame):
    """Percentile-based limits with small padding; returns (x_min,x_max,y_min,y_max) or None if invalid."""
    if d.empty: 
        return None
    x = d["kappa_mag"].to_numpy()
    y = d["deltaP"].to_numpy()
    if not np.isfinite(x).any() or not np.isfinite(y).any():
        return None
    x = x[np.isfinite(x)]; y = y[np.isfinite(y)]
    if x.size == 0 or y.size == 0:
        return None
    x_lo, x_hi = np.percentile(x, [1, 99])
    y_lo, y_hi = np.percentile(y, [1, 99])
    # If collapsed, expand a hair
    if not np.isfinite(x_lo) or not np.isfinite(x_hi) or x_lo == x_hi:
        m = np.nanmean(x) if np.isfinite(np.nanmean(x)) else 0.0
        span = max(1e-6, 0.1*abs(m)+1e-6)
        x_lo, x_hi = m - span, m + span
    if not np.isfinite(y_lo) or not np.isfinite(y_hi) or y_lo == y_hi:
        m = np.nanmean(y) if np.isfinite(np.nanmean(y)) else 0.0
        span = max(1e-6, 0.1*abs(m)+1e-6)
        y_lo, y_hi = m - span, m + span
    # small padding
    pad_x = 0.05*(x_hi - x_lo)
    pad_y = 0.05*(y_hi - y_lo)
    return x_lo - pad_x, x_hi + pad_x, y_lo - pad_y, y_hi + pad_y

def plot_plane_by_band(dfw_lab: pd.DataFrame, thresholds: dict, outdir: Path, max_points=100000):
    if dfw_lab.empty:
        return
    ensure_dir(outdir / "plots")
    for (blo,bhi), sub in dfw_lab.groupby(["band_lo","band_hi"]):
        d = coerce_clean(sub.copy())
        if d.empty:
            continue
        if len(d) > max_points:
            d = d.sample(max_points, random_state=0)
        limits = _axis_limits(d)
        if limits is None:
            # nothing plottable
            continue
        x_min, x_max, y_min, y_max = limits
        th = thresholds.get((blo,bhi), None)

        # All points
        fig = plt.figure(figsize=(6,6))
        for s, chunk in d.groupby("state"):
            plt.scatter(chunk["kappa_mag"], chunk["deltaP"], s=6, alpha=0.6, label=str(s))
        if th:
            if np.isfinite(th.get("th_k_low", np.nan)):  plt.axvline(th["th_k_low"], linewidth=1)
            if np.isfinite(th.get("th_k_high", np.nan)): plt.axvline(th["th_k_high"], linewidth=1)
            if np.isfinite(th.get("th_dP", np.nan)):     plt.axhline(th["th_dP"], linewidth=1)
        plt.axhline(0.0, linewidth=1)
        plt.xlim(x_min, x_max); plt.ylim(y_min, y_max)
        plt.xlabel("|κ*|"); plt.ylabel("ΔP (relative)")
        plt.title(f"Pirouette Plane (all)  [{blo:.3g}–{bhi:.3g} Hz]")
        fig.tight_layout()
        fig.savefig(outdir / "plots" / f"pirouette_plane_band_{blo:.6g}-{bhi:.6g}_all.png", dpi=150)
        plt.close(fig)

        # Four projections
        for arc in ARCS:
            subarc = d[d["state"] == arc]
            if subarc.empty:
                # still write an empty canvas to keep UX consistent
                fig = plt.figure(figsize=(6,6))
                if th:
                    if np.isfinite(th.get("th_k_low", np.nan)):  plt.axvline(th["th_k_low"], linewidth=1)
                    if np.isfinite(th.get("th_k_high", np.nan)): plt.axvline(th["th_k_high"], linewidth=1)
                    if np.isfinite(th.get("th_dP", np.nan)):     plt.axhline(th["th_dP"], linewidth=1)
                plt.axhline(0.0, linewidth=1)
                plt.xlim(x_min, x_max); plt.ylim(y_min, y_max)
                plt.xlabel("|κ*|"); plt.ylabel("ΔP (relative)")
                plt.title(f"Pirouette Plane ({arc})  [{blo:.3g}–{bhi:.3g} Hz]")
                fig.tight_layout()
                fig.savefig(outdir / "plots" / f"pirouette_plane_band_{blo:.6g}-{bhi:.6g}_{arc.lower()}.png", dpi=150)
                plt.close(fig)
                continue
            fig = plt.figure(figsize=(6,6))
            plt.scatter(subarc["kappa_mag"], subarc["deltaP"], s=6, alpha=0.6, label=str(arc))
            if th:
                if np.isfinite(th.get("th_k_low", np.nan)):  plt.axvline(th["th_k_low"], linewidth=1)
                if np.isfinite(th.get("th_k_high", np.nan)): plt.axvline(th["th_k_high"], linewidth=1)
                if np.isfinite(th.get("th_dP", np.nan)):     plt.axhline(th["th_dP"], linewidth=1)
            plt.axhline(0.0, linewidth=1)
            plt.xlim(x_min, x_max); plt.ylim(y_min, y_max)
            plt.xlabel("|κ*|"); plt.ylabel("ΔP (relative)")
            plt.title(f"Pirouette Plane ({arc})  [{blo:.3g}–{bhi:.3g} Hz]")
            plt.legend(markerscale=2, fontsize=8)
            fig.tight_layout()
            fig.savefig(outdir / "plots" / f"pirouette_plane_band_{blo:.6g}-{bhi:.6g}_{arc.lower()}.png", dpi=150)
            plt.close(fig)

def plot_allocation_bars(dfw_lab: pd.DataFrame, outdir: Path):
    if dfw_lab.empty:
        return
    ensure_dir(outdir / "plots")
    alloc = (dfw_lab.groupby(["band_lo","band_hi","state"]).size()
             .reset_index(name="count"))
    for (blo,bhi), sub in alloc.groupby(["band_lo","band_hi"]):
        order = [s for s in ARCS if s in sub["state"].unique()]
        counts = [int(sub[sub["state"]==s]["count"].sum()) for s in order]
        if not counts:
            continue
        fig = plt.figure(figsize=(7,4))
        plt.bar(order, counts)
        plt.ylabel("Count")
        plt.title(f"Quadrant Allocation  [{blo:.3g}–{bhi:.3g} Hz]")
        fig.tight_layout()
        fig.savefig(outdir / "plots" / f"allocation_band_{blo:.6g}-{bhi:.6g}.png", dpi=150)
        plt.close(fig)

def plot_triads(dft: pd.DataFrame, outdir: Path):
    if dft.empty or "peak" not in dft.columns:
        return
    ensure_dir(outdir / "plots")
    fig = plt.figure(figsize=(6,5))
    if "half_bw_hz" in dft.columns:
        plt.scatter(dft["peak"], dft["half_bw_hz"], s=10, alpha=0.7)
        plt.xlabel("TPCI Peak"); plt.ylabel("Half Bandwidth (Hz)")
        plt.title("Triads: Peak vs Half-Bandwidth")
    else:
        plt.hist(dft["peak"], bins=30)
        plt.xlabel("TPCI Peak"); plt.ylabel("Count")
        plt.title("Triads: Peak Distribution")
    fig.tight_layout()
    fig.savefig(outdir / "plots" / "triads_peak_vs_bw.png", dpi=150)
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description="Metabolize SoS outputs into plots & summaries (v2.1 hardened)")
    ap.add_argument("--indir", type=str, required=True, help="Directory containing SoS output files")
    ap.add_argument("--outdir", type=str, default="./sos_plots", help="Directory for plots & summaries")
    ap.add_argument("--max-points", type=int, default=100000, help="Max points per scatter to keep plots fast")
    args = ap.parse_args()

    indir = Path(args.indir); outdir = Path(args.outdir)
    ensure_dir(outdir)

    dfw, dfs, dfe, dft = load_tables(indir)
    dfw_lab, thresholds = relabel_all(dfw)

    if not dfw_lab.empty:
        dfw_lab.to_csv(outdir / "merged_windows_labeled.csv", index=False)
    if not dfs.empty:
        dfs.to_csv(outdir / "merged_states_raw.csv", index=False)
    if not dfe.empty:
        dfe.to_csv(outdir / "merged_epochs.csv", index=False)
    if not dft.empty:
        dft.to_csv(outdir / "merged_triads.csv", index=False)

    # prefer relabeled windows as base_df for summaries
    summarize(dfw_lab if not dfw_lab.empty else dfw, dfw_lab if not dfw_lab.empty else dfs, outdir)

    plot_plane_by_band(dfw_lab, thresholds, outdir, max_points=args.max_points)
    plot_allocation_bars(dfw_lab, outdir)
    plot_triads(dft, outdir)

    print(f"Done. See {outdir} for summaries and plots/.")

if __name__ == "__main__":
    main()
