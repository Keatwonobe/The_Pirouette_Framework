
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoS Metabolizer
---------------
Consumes outputs from sos_unified_mseed_analyzer.py and produces summary CSVs and plots.

Inputs discovered under --indir:
  *_sos_windows.csv   (ΔP, |κ*| windows)
  *_sos_states.csv    (per-window archetype labels)
  *_sos_epochs.csv    (sustained segments)
  *_triads_summary.json (optional)

Outputs under --outdir:
  sos_summary_overall.csv        # overall counts & basic stats
  sos_summary_by_band.csv        # per-band counts & stats
  sos_summary_by_trace_band.csv  # per-trace, per-band counts
  plots/                         
    pirouette_plane_band_{lo}-{hi}.png
    state_distribution.png
    state_timeline_band_{lo}-{hi}.png
    triads_peak_vs_bw.png   (if triads present)

Usage:
  python sos_metabolizer.py --indir ./sos_out --outdir ./sos_plots
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def summarize(dfw: pd.DataFrame, dfs: pd.DataFrame, outdir: Path):
    # Overall stats
    out_overall = []
    if not dfw.empty:
        out_overall.append({
            "n_windows": len(dfw),
            "kappa_mag_mean": dfw["kappa_mag"].mean(),
            "kappa_mag_median": dfw["kappa_mag"].median(),
            "deltaP_mean": dfw["deltaP"].mean(),
            "deltaP_median": dfw["deltaP"].median(),
            "n_files": dfw["file"].nunique(),
            "n_traces": dfw["trace"].nunique(),
        })
    else:
        out_overall.append({"n_windows": 0})
    if not dfs.empty:
        counts = dfs["state"].value_counts().to_dict()
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
        # add states distribution per band if available
        if not dfs.empty:
            state_counts = dfs.groupby(["band_lo","band_hi","state"]).size().reset_index(name="count")
            state_pivot = state_counts.pivot_table(index=["band_lo","band_hi"], columns="state", values="count", fill_value=0)
            state_pivot = state_pivot.reset_index()
            band_stats = band_stats.merge(state_pivot, on=["band_lo","band_hi"], how="left")
        band_stats.to_csv(outdir / "sos_summary_by_band.csv", index=False)

    # Per-trace-per-band stats
    if not dfw.empty:
        grp2 = dfw.groupby(["file","trace","band_lo","band_hi"])
        tb = grp2.agg({
            "kappa_mag":["count","mean","median"],
            "deltaP":["mean","median"]
        })
        tb.columns = ["_".join(c).strip("_") for c in tb.columns.to_flat_index()]
        tb = tb.reset_index()
        if not dfs.empty:
            sc = dfs.groupby(["file","trace","band_lo","band_hi","state"]).size().reset_index(name="count")
            sp = sc.pivot_table(index=["file","trace","band_lo","band_hi"], columns="state", values="count", fill_value=0).reset_index()
            tb = tb.merge(sp, on=["file","trace","band_lo","band_hi"], how="left")
        tb.to_csv(outdir / "sos_summary_by_trace_band.csv", index=False)

def plot_pirouette_planes(dfw: pd.DataFrame, dfs: pd.DataFrame, outdir: Path, max_points=100000):
    if dfw.empty:
        return
    ensure_dir(outdir / "plots")
    # If labels are available, join; else we'll plot unlabeled points
    if not dfs.empty:
        df = dfw.merge(dfs[["file","trace","band_lo","band_hi","t0","t1","state"]],
                       on=["file","trace","band_lo","band_hi","t0","t1"],
                       how="left")
    else:
        df = dfw.copy()
        df["state"] = "Unlabeled"
    # Sample for speed if huge
    if len(df) > max_points:
        df = df.sample(max_points, random_state=0)
    # Per band plot
    for (blo,bhi), d in df.groupby(["band_lo","band_hi"]):
        fig = plt.figure(figsize=(6,6))
        # Scatter; default matplotlib color cycle (no explicit colors)
        for s, sub in d.groupby("state"):
            plt.scatter(sub["kappa_mag"], sub["deltaP"], s=6, alpha=0.6, label=str(s))
        plt.axhline(0.0, linewidth=1)
        plt.xlabel("|κ*|")
        plt.ylabel("ΔP (relative)")
        plt.title(f"Pirouette Plane ΔP vs |κ*|  [{blo:.3g}–{bhi:.3g} Hz]")
        plt.legend(markerscale=2, fontsize=8)
        fig.tight_layout()
        fig.savefig(outdir / "plots" / f"pirouette_plane_band_{blo:.6g}-{bhi:.6g}.png", dpi=150)
        plt.close(fig)

def plot_state_distribution(dfs: pd.DataFrame, outdir: Path):
    if dfs.empty:
        return
    ensure_dir(outdir / "plots")
    counts = dfs["state"].value_counts().sort_index()
    fig = plt.figure(figsize=(7,4))
    plt.bar(counts.index.astype(str), counts.values)
    plt.ylabel("Count")
    plt.title("State Distribution (All Bands)")
    fig.tight_layout()
    fig.savefig(outdir / "plots" / "state_distribution.png", dpi=150)
    plt.close(fig)

def plot_state_timeline(dfs: pd.DataFrame, outdir: Path, per_band=True):
    if dfs.empty:
        return
    ensure_dir(outdir / "plots")
    # For each band, plot an event timeline of states (simple strip per state)
    key = ["band_lo","band_hi"] if per_band else []
    for keys, d in dfs.groupby(key) if key else [([], dfs)]:
        # Normalize time axis per trace by min(t0) to make plots comparable
        d = d.copy()
        # Build a simple mapping to rows for each state
        states = sorted(d["state"].unique().tolist())
        state_rows = {s:i for i,s in enumerate(states)}
        fig = plt.figure(figsize=(10, max(3, 0.3*len(states))))
        for s, sub in d.groupby("state"):
            y = np.ones(len(sub)) * state_rows[s]
            # use t0; represent window spans as small horizontal ticks via t1-t0, but scatter is simpler
            plt.scatter(sub["t0"].values, y, s=4, alpha=0.6, label=str(s))
        plt.yticks(range(len(states)), states)
        plt.xlabel("Time (s)")
        if key:
            blo, bhi = keys
            plt.title(f"State Timeline  [{blo:.3g}–{bhi:.3g} Hz]")
            fname = f"state_timeline_band_{blo:.6g}-{bhi:.6g}.png"
        else:
            plt.title("State Timeline (All Bands)")
            fname = "state_timeline_all.png"
        fig.tight_layout()
        fig.savefig(outdir / "plots" / fname, dpi=150)
        plt.close(fig)

def plot_triads(dft: pd.DataFrame, outdir: Path):
    if dft.empty or "peak" not in dft.columns:
        return
    ensure_dir(outdir / "plots")
    fig = plt.figure(figsize=(6,5))
    x = dft["half_bw_hz"] if "half_bw_hz" in dft.columns else None
    if x is not None:
        plt.scatter(dft["peak"], x, s=10, alpha=0.7)
        plt.xlabel("TPCI Peak")
        plt.ylabel("Half Bandwidth (Hz)")
        plt.title("Triads: Peak vs Half-Bandwidth")
    else:
        plt.hist(dft["peak"], bins=30)
        plt.xlabel("TPCI Peak")
        plt.ylabel("Count")
        plt.title("Triads: Peak Distribution")
    fig.tight_layout()
    fig.savefig(outdir / "plots" / "triads_peak_vs_bw.png", dpi=150)
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description="Metabolize SoS outputs into plots & summaries")
    ap.add_argument("--indir", type=str, required=True, help="Directory containing SoS output files")
    ap.add_argument("--outdir", type=str, default="./sos_plots", help="Directory for plots & summaries")
    ap.add_argument("--max-points", type=int, default=100000, help="Max points per scatter to keep plots fast")
    args = ap.parse_args()

    indir = Path(args.indir)
    outdir = Path(args.outdir)
    ensure_dir(outdir)

    dfw, dfs, dfe, dft = load_tables(indir)

    # Save merged tables for convenience if present
    if not dfw.empty:
        dfw.to_csv(outdir / "merged_windows.csv", index=False)
    if not dfs.empty:
        dfs.to_csv(outdir / "merged_states.csv", index=False)
    if not dfe.empty:
        dfe.to_csv(outdir / "merged_epochs.csv", index=False)
    if not dft.empty:
        dft.to_csv(outdir / "merged_triads.csv", index=False)

    summarize(dfw, dfs, outdir)
    plot_pirouette_planes(dfw, dfs, outdir, max_points=args.max_points)
    plot_state_distribution(dfs, outdir)
    plot_state_timeline(dfs, outdir, per_band=True)
    plot_triads(dft, outdir)

    print(f"Done. See {outdir} for CSV summaries and plots/.")

if __name__ == "__main__":
    main()
