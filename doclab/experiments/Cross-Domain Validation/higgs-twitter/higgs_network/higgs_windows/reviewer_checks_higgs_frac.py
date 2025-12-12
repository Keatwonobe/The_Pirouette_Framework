#!/usr/bin/env python3
"""
Reviewer check: run the Higgs Twitter windows through the
Gamma-shell analysis for multiple shell fractions.

This version is tolerant of older NPZ files that do NOT contain
`curl2` / `grad2` and only have `curl` / `grad`.

It will:
- scan an input directory for window files (default: higgs_hodge_out_win*.npz)
- for each fraction in --frac-list (e.g. 0.1,0.2,0.3,0.5)
  * load every window
  * pick the top `frac` edges by (curl2 / (grad2+eps))
  * compute:
      - Theta_shell = mean(curl2 on shell)
      - Theta_c_shell = k_gamma * mean(grad2 on shell)
      - alpha (avalanche power law) from those edges
  * store time series
  * make plots
  * append to CSV

Author: patched for mixed NPZ layouts (old/new), CP1252-safe output.
"""

import argparse
import glob
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------


def load_window(path):
    """
    Load a single NPZ window and normalize field names.

    We try these possibilities:
      - 'curl2', 'grad2'
      - else: square 'curl', 'grad'
    We also look for 'edges' (needed for avalanche grouping).
    We ALSO try to pick up k_gamma from the file; if missing we set None.
    """
    data = np.load(path, allow_pickle=True)

    # edges are always needed to group avalanches
    if "edges" in data:
        edges = data["edges"]
    elif "edge_list" in data:
        edges = data["edge_list"]
    else:
        raise ValueError(f"{path}: no 'edges' array found")

    # curl2
    if "curl2" in data:
        curl2 = data["curl2"].astype(float)
    elif "curl" in data:
        curl2 = np.square(data["curl"].astype(float))
    elif "curl_energy" in data:
        curl2 = data["curl_energy"].astype(float)
    else:
        raise ValueError(f"{path}: missing curl2/curl")

    # grad2
    if "grad2" in data:
        grad2 = data["grad2"].astype(float)
    elif "grad" in data:
        grad2 = np.square(data["grad"].astype(float))
    elif "grad_energy" in data:
        grad2 = data["grad_energy"].astype(float)
    else:
        raise ValueError(f"{path}: missing grad2/grad")

    # k_gamma (may be absent on old files)
    k_gamma = None
    for k in ("k_gamma", "k_Gamma", "kgamma"):
        if k in data:
            k_gamma = float(data[k])
            break

    return {
        "edges": edges,
        "curl2": curl2,
        "grad2": grad2,
        "k_gamma": k_gamma,
    }


# union-find for avalanche grouping ----------------------------------
def _uf_make(n):
    return list(range(n)), [1] * n


def _uf_find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def _uf_union(parent, size, a, b):
    ra = _uf_find(parent, a)
    rb = _uf_find(parent, b)
    if ra == rb:
        return
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]


def avalanche_sizes_from_edges(edges):
    """
    edges: (m,2) int array
    Return: list of component sizes counted as #edges per component
    """
    if edges.size == 0:
        return []

    # map node id -> 0..n-1
    nodes = np.unique(edges)
    node_to_idx = {int(n): i for i, n in enumerate(nodes)}
    n_nodes = len(nodes)

    parent, size = _uf_make(n_nodes)

    for u, v in edges:
        iu = node_to_idx[int(u)]
        iv = node_to_idx[int(v)]
        _uf_union(parent, size, iu, iv)

    # count edges per root
    root_edge_count = {}
    for u, v in edges:
        ru = _uf_find(parent, node_to_idx[int(u)])
        root_edge_count[ru] = root_edge_count.get(ru, 0) + 1

    return list(root_edge_count.values())


def powerlaw_slope_from_sizes(sizes, min_size=1):
    """
    Very lightweight slope estimator on log-log.
    We only need a relative slope for comparison.
    """
    if not sizes:
        return None

    # histogram
    counts = {}
    for s in sizes:
        if s < min_size:
            continue
        counts[s] = counts.get(s, 0) + 1

    if len(counts) < 2:
        return None

    xs = np.array(sorted(counts.keys()), dtype=float)
    ys = np.array([counts[x] for x in xs], dtype=float)

    logx = np.log10(xs)
    logy = np.log10(ys)

    # fit slope
    A = np.vstack([logx, np.ones_like(logx)]).T
    slope, _ = np.linalg.lstsq(A, logy, rcond=None)[0]
    return slope  # note: this is negative


# --------------------------------------------------------------------
# main analysis per fraction
# --------------------------------------------------------------------


def analyze_once(window_paths, frac, default_k_gamma=3.36516e-07, eps=1e-12):
    """
    Run through all windows with this fraction.
    Return structured results.
    """
    alphas = []
    theta_shell = []
    theta_c_shell = []
    valid_names = []

    for path in window_paths:
        try:
            w = load_window(path)
        except ValueError as e:
            print(f"[warn] {e}", file=sys.stderr)
            continue

        edges = w["edges"]
        curl2 = w["curl2"]
        grad2 = w["grad2"]
        k_gamma = w["k_gamma"] if w["k_gamma"] is not None else default_k_gamma

        # select shell
        ratio = curl2 / (grad2 + eps)
        m = len(ratio)
        k = max(1, int(frac * m))
        idx = np.argpartition(-ratio, k - 1)[:k]  # top-k

        sel_edges = edges[idx]
        sel_curl2 = curl2[idx]
        sel_grad2 = grad2[idx]

        # energies
        Theta_shell = float(sel_curl2.mean()) if sel_curl2.size else 0.0
        Theta_c_shell = float(k_gamma * sel_grad2.mean()) if sel_grad2.size else 0.0

        # avalanches
        sizes = avalanche_sizes_from_edges(sel_edges)
        alpha = powerlaw_slope_from_sizes(sizes, min_size=1)

        alphas.append(alpha)
        theta_shell.append(Theta_shell)
        theta_c_shell.append(Theta_c_shell)
        valid_names.append(os.path.basename(path))

    return {
        "frac": frac,
        "names": valid_names,
        "alpha": np.array(alphas, dtype=float),
        "theta_shell": np.array(theta_shell, dtype=float),
        "theta_c_shell": np.array(theta_c_shell, dtype=float),
    }


def plot_results(all_results, outprefix="higgs_frac"):
    """
    all_results: list of dicts from analyze_once
    Produce:
      - outprefix + "_alpha_t.png"
      - outprefix + "_theta_t.png"
    """
    # alpha(t) per fraction
    plt.figure(figsize=(9, 4.8))
    for res in all_results:
        t = np.arange(len(res["alpha"]))
        plt.plot(t, res["alpha"], marker="o", label=f"frac={res['frac']}")
    plt.axhline(-1.0, color="gray", linestyle="--", alpha=0.6)
    plt.xlabel("time window (index)")
    plt.ylabel("avalanche exponent (slope)")
    plt.title("Higgs Twitter cascade: alpha(t) for multiple shell fractions")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outprefix + "_alpha_t.png", dpi=150)

    # theta vs theta_c per fraction
    plt.figure(figsize=(9, 4.8))
    for res in all_results:
        t = np.arange(len(res["theta_shell"]))
        plt.plot(t, res["theta_shell"], marker="o", label=f"Theta shell, f={res['frac']}")
        plt.plot(t, res["theta_c_shell"], marker="s", linestyle="--", alpha=0.5)
    plt.xlabel("time window (index)")
    plt.ylabel("energy (shell units)")
    plt.title("Higgs Twitter cascade: Theta_shell vs Theta_c_shell for multiple fractions")
    plt.tight_layout()
    plt.savefig(outprefix + "_theta_t.png", dpi=150)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--indir", default=".", help="directory with window NPZs")
    ap.add_argument(
        "--pattern",
        default="higgs_hodge_out_win*.npz",
        help="glob pattern inside --indir",
    )
    ap.add_argument(
        "--frac-list",
        default="0.2",
        help="comma list of shell fractions, e.g. 0.1,0.2,0.3,0.5",
    )
    ap.add_argument(
        "--outfile",
        default="higgs_frac_summary.csv",
        help="CSV to write combined results",
    )
    ap.add_argument(
        "--default-k-gamma",
        type=float,
        default=3.36516e-07,
        help="fallback k_gamma when window doesn't have one",
    )
    args = ap.parse_args()

    pattern = os.path.join(args.indir, args.pattern)
    window_paths = sorted(glob.glob(pattern))
    if not window_paths:
        print(f"no files matching {pattern}", file=sys.stderr)
        sys.exit(1)

    frac_list = [float(x.strip()) for x in args.frac_list.split(",") if x.strip()]

    all_results = []
    for frac in frac_list:
        print(f"[info] analyzing fraction {frac} …")
        res = analyze_once(
            window_paths,
            frac=frac,
            default_k_gamma=args.default_k_gamma,
        )
        all_results.append(res)

    # write CSV (UTF-8 to avoid Windows cp1252 crash)
    with open(args.outfile, "w", encoding="utf-8") as f:
        f.write("frac,idx,filename,alpha,theta_shell,theta_c_shell\n")
        for res in all_results:
            frac = res["frac"]
            for i, name in enumerate(res["names"]):
                a = res["alpha"][i]
                ts = res["theta_shell"][i]
                tc = res["theta_c_shell"][i]
                f.write(f"{frac},{i},{name},{a},{ts},{tc}\n")

    # plots
    plot_results(all_results, outprefix="higgs_frac")

    print("[done] wrote:", args.outfile)
    print("[done] wrote: higgs_frac_alpha_t.png, higgs_frac_theta_t.png")


if __name__ == "__main__":
    main()
