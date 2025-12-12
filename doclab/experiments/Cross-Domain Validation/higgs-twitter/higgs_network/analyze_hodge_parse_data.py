#!/usr/bin/env python3
"""
Minimal-memory cascade analyzer.

What it does, in order:

1. From a single NPZ (default: higgs_hodge_out.npz)
   - builds the avalanche distribution for a default k_Gamma
   - writes: higgs_avalanche_distribution.png

2. From the *same* NPZ
   - sweeps a small list of k_Gamma values
   - writes: alpha_vs_kgamma.png

3. Optionally, from a glob pattern of NPZs (e.g. higgs_hodge_day*.npz)
   - processes them ONE AT A TIME
   - writes: daily_avalanche_comparison.png
   - writes: daily_avalanche_slopes.csv

At every stage, large objects are deleted and GC’d.
"""

import argparse
import glob
import os
import gc
import collections
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# core helpers
# ------------------------------------------------------------
def load_hodge_npz(fname):
    # mmap_mode keeps big arrays off RAM until actually touched
    data = np.load(fname, allow_pickle=True, mmap_mode="r")
    edges = data["edges"]
    grad_part = data["grad"]
    curl_part = data["curl"]
    return edges, grad_part, curl_part


def avalanches_for_k(edges, grad_part, curl_part, k_gamma):
    """
    Given Hodge pieces and a threshold k_gamma,
    return avalanche sizes (edge counts of connected comps)
    and number of cascade edges.
    """
    curl_energy = curl_part ** 2
    grad_energy = grad_part ** 2

    cascade_mask = curl_energy > (k_gamma * grad_energy)
    if not np.any(cascade_mask):
        return [], 0

    # pull only the edges that fired
    cascade_edges = edges[cascade_mask]

    # build a graph just for them
    G_cascade = ig.Graph.TupleList(cascade_edges, directed=False)
    comps = G_cascade.components(mode="strong").subgraphs()

    av_sizes = [c.ecount() for c in comps if c.ecount() > 0]
    return av_sizes, len(cascade_edges)


def powerlaw_from_sizes(av_sizes):
    """Return (sizes, counts, slope) with a quick log-log fit."""
    counter = collections.Counter(av_sizes)
    sizes = np.array(sorted(counter.keys()))
    counts = np.array([counter[s] for s in sizes])

    if len(sizes) < 2:
        return sizes, counts, None

    log_s = np.log10(sizes)
    log_c = np.log10(counts)
    mask = np.isfinite(log_c)
    if mask.sum() < 2:
        return sizes, counts, None

    m, b = np.polyfit(log_s[mask], log_c[mask], 1)
    return sizes, counts, m


# ------------------------------------------------------------
# plotting helpers (each one uses & drops memory)
# ------------------------------------------------------------
def plot_avalanche_dist(sizes, counts, slope, outname):
    plt.figure(figsize=(12, 6))

    # left
    plt.subplot(1, 2, 1)
    plt.bar(sizes, counts, width=0.8, align="center")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Avalanche Size (number of edges)")
    plt.ylabel("Frequency (count)")
    plt.title("Avalanche Size Distribution")

    # right
    plt.subplot(1, 2, 2)
    plt.scatter(sizes, counts)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Avalanche Size (log)")
    plt.ylabel("Frequency (log)")
    plt.title("Log-Log Plot")

    if slope is not None:
        # reconstruct simple line through first point
        x0 = sizes[0]
        y0 = counts[0]
        # y = 10^(slope*log10(x) + c)
        c = np.log10(y0) - slope * np.log10(x0)
        xs = np.linspace(sizes.min(), sizes.max(), 50)
        ys = 10 ** (slope * np.log10(xs) + c)
        plt.plot(xs, ys, "r--", label=f"Power law (α={slope:.2f})")
        plt.legend()

    plt.tight_layout()
    plt.savefig(outname)
    plt.close()
    gc.collect()


def plot_alpha_vs_k(k_vals, alphas, outname):
    plt.figure(figsize=(6, 4))
    plt.plot(k_vals, alphas, marker="o")
    plt.xlabel("k_Γ")
    plt.ylabel("Power-law slope α")
    plt.title("Cascade Exponent vs k_Γ")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outname)
    plt.close()
    gc.collect()


def plot_daily_comparison(day_data, outname):
    """
    day_data: list of (label, sizes, counts, slope)
    We draw each day on its own row.
    """
    n = len(day_data)
    plt.figure(figsize=(10, 3 * max(1, n)))
    for i, (label, sizes, counts, slope) in enumerate(day_data, start=1):
        plt.subplot(n, 1, i)
        if len(sizes):
            plt.scatter(sizes, counts)
            plt.xscale("log"); plt.yscale("log")
        plt.title(f"{label} (α={slope if slope is not None else float('nan'):.2f})")
        plt.xlabel("avalanche size"); plt.ylabel("freq")

    plt.tight_layout()
    plt.savefig(outname)
    plt.close()
    gc.collect()


# ------------------------------------------------------------
# main
# ------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Low-memory cascade postprocessor (Pirouette SOCIO companion)."
    )
    ap.add_argument("--input", "-i", default="higgs_hodge_out.npz",
                    help="NPZ file with edges, grad, curl.")
    ap.add_argument("--pattern", "-p", default=None,
                    help="Optional glob for daily/multi NPZs, e.g. 'higgs_hodge_day*.npz'")
    ap.add_argument("--kgammas", "-k", default="0.5,1.0,2.0",
                    help="Comma-separated k_Gamma values to sweep.")
    ap.add_argument("--default-k", default=1.0, type=float,
                    help="k_Gamma to use for the main avalanche plot.")
    args = ap.parse_args()

    # ---- 1. MAIN FILE: avalanche distribution (one shot) ----
    print("[1/3] main avalanche distribution …")
    edges, grad_part, curl_part = load_hodge_npz(args.input)
    av_sizes, n_edges = avalanches_for_k(
        edges, grad_part, curl_part, k_gamma=args.default_k
    )
    if not av_sizes:
        print(f"no cascades at k_Γ={args.default_k}, skipping plot")
    else:
        sizes, counts, slope = powerlaw_from_sizes(av_sizes)
        plot_avalanche_dist(sizes, counts, slope,
                            outname="higgs_avalanche_distribution.png")
        print(" -> wrote higgs_avalanche_distribution.png")
    # free biggest arrays (we’ll reload for safety later)
    del edges, grad_part, curl_part
    gc.collect()

    # ---- 2. MAIN FILE: k_Γ sweep (one at a time) ----
    print("[2/3] k_Γ sweep …")
    edges, grad_part, curl_part = load_hodge_npz(args.input)
    k_vals = [float(x) for x in args.kgammas.split(",")]
    alphas = []
    for k in k_vals:
        av_sizes, _ = avalanches_for_k(edges, grad_part, curl_part, k_gamma=k)
        if not av_sizes:
            print(f"  k_Γ={k}: no cascades")
            alphas.append(np.nan)
            continue
        sizes, counts, slope = powerlaw_from_sizes(av_sizes)
        print(f"  k_Γ={k}: α={slope}")
        alphas.append(slope)
    plot_alpha_vs_k(k_vals, alphas, outname="alpha_vs_kgamma.png")
    print(" -> wrote alpha_vs_kgamma.png")
    del edges, grad_part, curl_part
    gc.collect()

    # ---- 3. DAILY / MULTI-FILE: process each NPZ separately ----
    if args.pattern:
        print("[3/3] daily / multi-file comparison …")
        files = sorted(glob.glob(args.pattern))
        if not files:
            print(f"  no files matched {args.pattern}")
        else:
            day_results = []
            with open("daily_avalanche_slopes.csv", "w") as fw:
                fw.write("file,alpha\n")
                for f in files:
                    print(f"  processing {f} …")
                    e2, g2, c2 = load_hodge_npz(f)
                    av_sizes, _ = avalanches_for_k(
                        e2, g2, c2, k_gamma=k_vals[0]
                    )
                    if av_sizes:
                        sizes, counts, slope = powerlaw_from_sizes(av_sizes)
                    else:
                        sizes, counts, slope = [], [], np.nan
                    lbl = os.path.basename(f)
                    day_results.append((lbl, sizes, counts, slope))
                    fw.write(f"{lbl},{'' if slope is None else slope}\n")
                    # drop per-file arrays asap
                    del e2, g2, c2
                    gc.collect()

            plot_daily_comparison(day_results,
                                  outname="daily_avalanche_comparison.png")
            print(" -> wrote daily_avalanche_comparison.png")
            print(" -> wrote daily_avalanche_slopes.csv")

    print("done.")


if __name__ == "__main__":
    main()
