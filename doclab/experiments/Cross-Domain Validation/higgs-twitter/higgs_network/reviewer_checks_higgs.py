#!/usr/bin/env python3
import argparse
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import csv
from math import inf

# ---------- helpers ----------

def load_npz(path):
    return np.load(path, allow_pickle=True)

def normalize_edges(edges):
    """
    Make sure edges is a clean (N, 2) int array.
    Handles object arrays like array([list([u, v]), ...], dtype=object).
    """
    if edges is None:
        return np.zeros((0, 2), dtype=int)
    arr = np.array(edges, dtype=object)
    # flatten to (-1, 2)
    arr = np.asarray([list(e) for e in arr], dtype=int)
    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError(f"Could not normalize edges to (N,2); got shape {arr.shape}")
    return arr

def select_edges_quantile(data, frac):
    """Pick top 'frac' of edges by ratio = |curl| / (|grad| + eps)."""
    edges = data["edges"]
    ratio = data["ratio"]
    frac = min(0.99, max(0.01, frac))
    thr = np.quantile(ratio, 1.0 - frac)
    mask = ratio >= thr
    sel_edges = edges[mask]
    return normalize_edges(sel_edges)

def avalanche_sizes_from_edges(edges):
    """Connected components over integer node ids, union–find."""
    edges = normalize_edges(edges)
    if edges.size == 0:
        return []

    # collect unique nodes
    nodes = np.unique(edges.flatten())
    node_to_idx = {n: i for i, n in enumerate(nodes)}
    parent = list(range(len(nodes)))

    def find(x):
        # x must be int
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a); rb = find(b)
        if ra != rb:
            parent[rb] = ra

    # build components
    for u, v in edges:
        iu = node_to_idx[int(u)]
        iv = node_to_idx[int(v)]
        union(iu, iv)

    # count edges per component
    comp_edges = {}
    for u, v in edges:
        cu = find(node_to_idx[int(u)])
        comp_edges.setdefault(cu, 0)
        comp_edges[cu] += 1

    return list(comp_edges.values())

def fit_power_law_from_sizes(sizes):
    """Simple log-log fit, returns slope (alpha)."""
    if len(sizes) < 2:
        return None
    unique, counts = np.unique(sizes, return_counts=True)
    logx = np.log10(unique)
    logy = np.log10(counts)
    mask = np.isfinite(logx) & np.isfinite(logy)
    if mask.sum() < 2:
        return None
    m, b = np.polyfit(logx[mask], logy[mask], 1)
    return m  # slope

# ---------- main analysis ----------

def main():
    ap = argparse.ArgumentParser(
        description="Reviewer-check script for Γ-aware Higgs Twitter cascade")
    ap.add_argument("--pattern", default="higgs_hodge_out_win*.npz",
                    help="glob for per-window NPZs")
    ap.add_argument("--frac", type=float, default=0.2,
                    help="fraction of most-turbulent edges to keep (Γ-shell). default=0.2")
    ap.add_argument("--k-gamma", type=float, default=0.7,
                    help="control parameter k_Γ to compute Θ_c(t) = k_Γ * <grad²>")
    ap.add_argument("--outdir", default=".",
                    help="where to write plots and CSV")
    args = ap.parse_args()

    files = sorted(glob.glob(args.pattern))
    if not files:
        raise SystemExit(f"No files matched pattern {args.pattern}")

    alphas, thetas, thetas_c, names = [], [], [], []

    for f in files:
        data = load_npz(f)

        # energy stats
        grad = data["grad"]
        curl = data["curl"]
        grad2_mean = float((grad ** 2).mean())
        curl2_mean = float((curl ** 2).mean())
        Theta = curl2_mean
        Theta_c = args.k_gamma * grad2_mean

        if "ratio" not in data:
            raise SystemExit(f"{f} has no 'ratio' field; rerun Hodge exporter with ratio.")
        sel_edges = select_edges_quantile(data, args.frac)
        sizes = avalanche_sizes_from_edges(sel_edges)
        alpha = fit_power_law_from_sizes(sizes)

        names.append(os.path.basename(f))
        alphas.append(alpha)
        thetas.append(Theta)
        thetas_c.append(Theta_c)

    alphas = np.array(alphas, dtype=float)
    thetas = np.array(thetas, dtype=float)
    thetas_c = np.array(thetas_c, dtype=float)
    t = np.arange(len(alphas))

    # critical window: closest to α = -1
    diff_to_minus1 = np.abs(alphas + 1.0)
    crit_idx = int(np.nanargmin(diff_to_minus1))
    crit_alpha = alphas[crit_idx]

    # closest Theta~Theta_c window
    diff_theta = np.abs(thetas - thetas_c)
    theta_cross_idx = int(np.nanargmin(diff_theta))

    # earliest supercritical before crit
    early_super_idx = None
    for i in range(crit_idx):
        if alphas[i] is not None and alphas[i] > -1.0:
            early_super_idx = i
            break

    # late oscillations: |α+1| < 0.05 after crit
    late_mask = np.abs(alphas[crit_idx:] + 1.0) < 0.05
    late_osc_count = int(late_mask.sum())

    # CSV
    csv_path = os.path.join(args.outdir, "higgs_reviewer_timeseries.csv")
    with open(csv_path, "w", newline="") as fcsv:
        w = csv.writer(fcsv)
        w.writerow(["index", "file", "alpha", "Theta", "Theta_c"])
        for i, nm, a, th, thc in zip(t, names, alphas, thetas, thetas_c):
            w.writerow([i, nm, a if a is not None else "", th, thc])

    # plot 1: alpha(t)
    plt.figure(figsize=(8, 5))
    plt.plot(t, alphas, marker="o", color="#d28f00", linewidth=2)
    plt.axhline(-1.0, linestyle="--", color="gray", label="α = -1 (critical)")
    plt.scatter([crit_idx], [crit_alpha], s=80, color="red", zorder=5,
                label=f"critical window (t={crit_idx})")
    plt.xlabel("time window (index)")
    plt.ylabel("avalanche exponent α")
    plt.title("Temporal Γ-sweep in Higgs Twitter cascade")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "higgs_alpha_t.png"), dpi=150)
    plt.close()

    # plot 2: Theta(t) vs Theta_c(t)
    plt.figure(figsize=(8, 5))
    plt.plot(t, thetas, marker="o", label="Θ(t) = <curl²>")
    plt.plot(t, thetas_c, marker="s", label="Θ_c(t) = k_Γ <grad²>")
    plt.axvline(crit_idx, linestyle="--", color="red", label=f"α≈-1 at t={crit_idx}")
    plt.axvline(theta_cross_idx, linestyle=":", color="purple",
                label=f"Θ≈Θ_c at t={theta_cross_idx}")
    plt.xlabel("time window (index)")
    plt.ylabel("energy")
    plt.title("Curl energy vs critical curl energy")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "higgs_theta_t.png"), dpi=150)
    plt.close()

    # plot 3: alpha vs Theta/Theta_c
    ratio = thetas / np.where(thetas_c == 0, np.nan, thetas_c)
    plt.figure(figsize=(6, 5))
    plt.scatter(ratio, alphas, c=t, cmap="viridis")
    plt.axhline(-1.0, linestyle="--", color="gray")
    plt.xlabel("Θ / Θ_c")
    plt.ylabel("α")
    plt.title("α vs energy ratio (colored by time)")
    plt.colorbar(label="time window")
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "higgs_alpha_vs_theta_ratio.png"), dpi=150)
    plt.close()

    # reviewer summary
    txt_path = os.path.join(args.outdir, "higgs_reviewer_summary.txt")
    with open(txt_path, "w") as ft:
        ft.write("Higgs Γ-aware cascade — reviewer checks\n")
        ft.write("=======================================\n\n")
        ft.write(f"Files analyzed: {len(names)}\n")
        ft.write(f"Critical window (|α+1| min): t={crit_idx}, alpha={crit_alpha:.6f}, file={names[crit_idx]}\n")
        ft.write(f"Closest Θ≈Θ_c window:       t={theta_cross_idx}, file={names[theta_cross_idx]}\n\n")

        if crit_idx == theta_cross_idx:
            ft.write("Q1: Θ(t) and Θ_c(t) cross at SAME window as α≈-1 → PASS\n")
        else:
            ft.write("Q1: Θ(t) and Θ_c(t) do NOT exactly coincide with α≈-1 → CHECK\n")
            ft.write(f"    α≈-1 at t={crit_idx}, Θ≈Θ_c at t={theta_cross_idx}\n")

        if early_super_idx is not None:
            ft.write(f"Q2: Earlier super-critical window found at t={early_super_idx}, alpha={alphas[early_super_idx]:.4f} → PASS\n")
        else:
            ft.write("Q2: No earlier super-critical window found → CHECK\n")

        ft.write(f"Q3: Late-time windows within |α+1|<0.05 after t={crit_idx}: {late_osc_count} → {'PASS' if late_osc_count >= 2 else 'CHECK'}\n")
        ft.write("\nNotes:\n")
        ft.write("- If Q1 off by 1, try --k-gamma 0.6 or 0.8.\n")
        ft.write("- If many alphas are blank, raise --frac from 0.2 to 0.3.\n")

    print("Wrote:")
    print(" -", csv_path)
    print(" -", os.path.join(args.outdir, "higgs_alpha_t.png"))
    print(" -", os.path.join(args.outdir, "higgs_theta_t.png"))
    print(" -", os.path.join(args.outdir, "higgs_alpha_vs_theta_ratio.png"))
    print(" -", txt_path)


if __name__ == "__main__":
    main()
