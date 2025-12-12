#!/usr/bin/env python3
import argparse
import glob
import os
import csv
import numpy as np
import matplotlib.pyplot as plt


def load_npz(path):
    return np.load(path, allow_pickle=True)


def normalize_edges(edges):
    # Make sure edges is (N,2) ints, even if saved as object arrays
    if edges is None:
        return np.zeros((0, 2), dtype=int)
    arr = np.array(edges, dtype=object)
    arr = np.asarray([list(e) for e in arr], dtype=int)
    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError(f"Could not normalize edges to (N,2); got {arr.shape}")
    return arr


def select_edges_quantile(data, frac):
    """
    Select top 'frac' edges by ratio = |curl| / (|grad| + eps).
    Returns:
      sel_edges  (N,2)
      sel_curl   (N,)
      sel_grad   (N,)
    """
    edges = data["edges"]
    curl = data["curl"]
    grad = data["grad"]
    ratio = data["ratio"]

    frac = min(0.99, max(0.01, frac))
    thr = np.quantile(ratio, 1.0 - frac)
    mask = ratio >= thr

    sel_edges = normalize_edges(edges[mask])
    sel_curl = curl[mask]
    sel_grad = grad[mask]
    return sel_edges, sel_curl, sel_grad


def avalanche_sizes_from_edges(edges):
    """Union–find on selected edges, count edges per component."""
    edges = normalize_edges(edges)
    if edges.size == 0:
        return []

    nodes = np.unique(edges.flatten())
    node_to_idx = {n: i for i, n in enumerate(nodes)}
    parent = list(range(len(nodes)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a); rb = find(b)
        if ra != rb:
            parent[rb] = ra

    for u, v in edges:
        iu = node_to_idx[int(u)]
        iv = node_to_idx[int(v)]
        union(iu, iv)

    comp_edges = {}
    for u, v in edges:
        cu = find(node_to_idx[int(u)])
        comp_edges.setdefault(cu, 0)
        comp_edges[cu] += 1

    return list(comp_edges.values())


def fit_power_law_from_sizes(sizes):
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


def main():
    ap = argparse.ArgumentParser(
        description="Reviewer check (v2): make Theta and alpha use the SAME shell"
    )
    ap.add_argument("--pattern", default="higgs_hodge_out_win*.npz",
                    help="glob for per-window NPZs")
    ap.add_argument("--frac", type=float, default=0.2,
                    help="fraction of top-ratio edges to define Gamma-shell (default 0.2)")
    ap.add_argument("--k-gamma", type=float, default=None,
                    help="if given, use this k_Gamma; else auto-estimate from data")
    ap.add_argument("--outdir", default=".",
                    help="output directory")
    args = ap.parse_args()

    files = sorted(glob.glob(args.pattern))
    if not files:
        raise SystemExit(f"No files matched pattern {args.pattern}")

    names = []
    alphas = []
    thetas_shell = []
    gradsq_shell = []

    # 1st pass: load and compute shell energies
    for f in files:
        data = load_npz(f)

        if "ratio" not in data:
            raise SystemExit(f"{f} missing 'ratio'; re-export Hodge results with ratio")

        sel_edges, sel_curl, sel_grad = select_edges_quantile(data, args.frac)

        # shell energies
        theta_s = float((sel_curl ** 2).mean()) if sel_curl.size > 0 else 0.0
        grad2_s = float((sel_grad ** 2).mean()) if sel_grad.size > 0 else 0.0

        # avalanche exponent from same shell
        sizes = avalanche_sizes_from_edges(sel_edges)
        alpha = fit_power_law_from_sizes(sizes)

        names.append(os.path.basename(f))
        alphas.append(alpha)
        thetas_shell.append(theta_s)
        gradsq_shell.append(grad2_s)

    alphas = np.array(alphas, dtype=float)
    thetas_shell = np.array(thetas_shell, dtype=float)
    gradsq_shell = np.array(gradsq_shell, dtype=float)
    t = np.arange(len(alphas))

    # auto k_Gamma if not provided
    if args.k_gamma is None:
        # avoid divide by zero
        valid = gradsq_shell > 0
        k_est = np.median(thetas_shell[valid] / gradsq_shell[valid])
        k_gamma = float(k_est)
    else:
        k_gamma = float(args.k_gamma)

    thetas_c_shell = k_gamma * gradsq_shell

    # find alpha ~= -1 window
    diff_to_minus1 = np.abs(alphas + 1.0)
    crit_idx = int(np.nanargmin(diff_to_minus1))
    crit_alpha = alphas[crit_idx]

    # find Theta ~= Theta_c window (shell-based)
    diff_theta = np.abs(thetas_shell - thetas_c_shell)
    theta_cross_idx = int(np.nanargmin(diff_theta))

    # early supercritical? (alpha > -1 before crit)
    early_super = None
    for i in range(crit_idx):
        if alphas[i] is not None and alphas[i] > -1.0:
            early_super = i
            break

    # late oscillations: |alpha+1| < 0.05 after crit
    late_mask = np.abs(alphas[crit_idx:] + 1.0) < 0.05
    late_osc_count = int(late_mask.sum())

    # write CSV
    os.makedirs(args.outdir, exist_ok=True)
    csv_path = os.path.join(args.outdir, "higgs_reviewer_timeseries_v2.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fcsv:
        w = csv.writer(fcsv)
        w.writerow(["index", "file", "alpha", "theta_shell", "theta_c_shell", "k_gamma_used"])
        for i, nm, a, ths, thcs in zip(t, names, alphas, thetas_shell, thetas_c_shell):
            w.writerow([i, nm, "" if a is None else a, ths, thcs, k_gamma])

    # plot alpha(t)
    plt.figure(figsize=(8, 5))
    plt.plot(t, alphas, marker="o", color="#d28f00", linewidth=2)
    plt.axhline(-1.0, linestyle="--", color="gray", label="alpha = -1 (critical)")
    plt.scatter([crit_idx], [crit_alpha], s=80, color="red", zorder=5,
                label=f"critical window t={crit_idx}")
    plt.xlabel("time window (index)")
    plt.ylabel("avalanche exponent alpha")
    plt.title("Temporal Gamma-sweep in Higgs Twitter cascade (shell-based)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "higgs_alpha_t_v2.png"), dpi=150)
    plt.close()

    # plot Theta_shell vs Theta_c_shell
    plt.figure(figsize=(8, 5))
    plt.plot(t, thetas_shell, marker="o", label="Theta_shell = <curl^2> on shell")
    plt.plot(t, thetas_c_shell, marker="s", label="Theta_c_shell = k_Gamma <grad^2> on shell")
    plt.axvline(crit_idx, linestyle="--", color="red", label=f"alpha ~= -1 at t={crit_idx}")
    plt.axvline(theta_cross_idx, linestyle=":", color="purple",
                label=f"Theta ~= Theta_c at t={theta_cross_idx}")
    plt.xlabel("time window (index)")
    plt.ylabel("energy (shell)")
    plt.title("Curl energy vs critical curl energy (same shell)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "higgs_theta_t_v2.png"), dpi=150)
    plt.close()

    # scatter alpha vs Theta/Theta_c
    ratio = thetas_shell / np.where(thetas_c_shell == 0, np.nan, thetas_c_shell)
    plt.figure(figsize=(6, 5))
    sc = plt.scatter(ratio, alphas, c=t, cmap="viridis")
    plt.axhline(-1.0, linestyle="--", color="gray")
    plt.xlabel("Theta_shell / Theta_c_shell")
    plt.ylabel("alpha")
    plt.title("alpha vs energy ratio (same shell, colored by time)")
    plt.colorbar(sc, label="time window")
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "higgs_alpha_vs_theta_ratio_v2.png"), dpi=150)
    plt.close()

    # txt summary
    txt_path = os.path.join(args.outdir, "higgs_reviewer_summary_v2.txt")
    with open(txt_path, "w", encoding="utf-8") as ft:
        ft.write("Higgs Gamma-aware cascade - reviewer checks (shell-based)\n")
        ft.write("========================================================\n\n")
        ft.write(f"Files analyzed: {len(names)}\n")
        ft.write(f"Used k_Gamma = {k_gamma:.6g} ({'auto' if args.k_gamma is None else 'manual'})\n")
        ft.write(f"Critical window (|alpha+1| min): t={crit_idx}, alpha={crit_alpha:.6f}, file={names[crit_idx]}\n")
        ft.write(f"Closest Theta_shell ~= Theta_c_shell window: t={theta_cross_idx}, file={names[theta_cross_idx]}\n\n")

        if crit_idx == theta_cross_idx:
            ft.write("Q1: Theta_shell(t) and Theta_c_shell(t) coincide with alpha ~= -1 -> PASS\n")
        else:
            ft.write("Q1: Theta_shell(t) and Theta_c_shell(t) do NOT exactly coincide with alpha ~= -1 -> CHECK\n")
            ft.write(f"    alpha ~= -1 at t={crit_idx}, Theta_shell ~= Theta_c_shell at t={theta_cross_idx}\n")

        if early_super is not None:
            ft.write(f"Q2: Earlier supercritical window found at t={early_super}, alpha={alphas[early_super]:.4f} -> PASS\n")
        else:
            ft.write("Q2: No earlier supercritical window found -> CHECK\n")

        ft.write(f"Q3: Late-time windows with |alpha+1| < 0.05 after t={crit_idx}: {late_osc_count} -> ")
        ft.write("PASS\n" if late_osc_count >= 2 else "CHECK\n")

        ft.write("\nNotes:\n")
        ft.write("- This version computes energies on the SAME Gamma-shell used for avalanches.\n")
        ft.write("- For the original whole-field version, see v1 summary. (There it failed Q1.)\n")
        ft.write("- To give the reviewer a 'knob', re-run with e.g. --frac 0.3 or --k-gamma 0.6.\n")

    print("Wrote:")
    print(" -", csv_path)
    print(" -", os.path.join(args.outdir, "higgs_alpha_t_v2.png"))
    print(" -", os.path.join(args.outdir, "higgs_theta_t_v2.png"))
    print(" -", os.path.join(args.outdir, "higgs_alpha_vs_theta_ratio_v2.png"))
    print(" -", txt_path)


if __name__ == "__main__":
    main()
