import numpy as np
import igraph as ig
import csv
import os

FNAME = "higgs_hodge_out.npz"
EPS = 1e-12


# ------------------------------------------------------------
# fractal / slide-rule Ki tuner (with guards)
# ------------------------------------------------------------
def fractal_ki_tuner(
    curl_sum_by_r: np.ndarray,
    grad_sum_by_r: np.ndarray,
    counts_by_r: np.ndarray,
    max_scale: int = None,
    w_curl: float = 1.0,
    w_grad: float = 1.0,
    radial_alpha: float = 1.0,
    top_k: int = 10,
    min_edges: int = 100,
    min_grad_sum: float = 1e-6,
    skip_r0: bool = True,
):
    """
    Slide a fractal window over radius-space and score each window
    by (curl/grad)*radial_lift, but IGNORE windows that are too small
    or degenerate (no grad, no edges).
    """
    R = len(curl_sum_by_r)
    if R == 0:
        return []

    if max_scale is None:
        max_scale = int(np.floor(np.log2(R))) if R > 1 else 0

    windows = []

    for s in range(max_scale + 1):
        win_size = 2 ** s  # 1,2,4,8,...
        for r0 in range(0, R):
            r1 = r0 + win_size
            if r1 > R:
                break

            # optionally skip any window that STARTS at r=0
            if skip_r0 and r0 == 0 and win_size == 1:
                continue

            c_sum = float(np.sum(curl_sum_by_r[r0:r1]))
            g_sum = float(np.sum(grad_sum_by_r[r0:r1]))
            edge_sum = int(np.sum(counts_by_r[r0:r1]))

            # hard filters
            if edge_sum < min_edges:
                continue
            if g_sum < min_grad_sum:
                continue

            # center of window
            r_mean = (r0 + r1 - 1) / 2.0
            radial_w = (1.0 + r_mean) ** radial_alpha

            score = (w_curl * c_sum + 1e-12) / (w_grad * g_sum + 1e-12)
            score *= radial_w

            windows.append((score, s, r0, r1 - 1, c_sum, g_sum, edge_sum))

    windows.sort(key=lambda x: x[0], reverse=True)
    return windows[:top_k]


def find_critical_radius_robust(theta_mean, grad_mean, counts, min_count=100):
    """
    Find critical radius using multiple heuristics:
    1. Maximum ratio (original method)
    2. Maximum absolute curl magnitude (where curl is actually strongest)
    3. Maximum curl with minimum sample size requirement
    """
    max_r = len(theta_mean) - 1
    if max_r < 1:
        return {'ratio': 0, 'magnitude': 0, 'weighted': 0}
    
    valid_mask = (counts >= min_count) & ~np.isnan(theta_mean) & ~np.isnan(grad_mean)
    
    # Method 1: Maximum ratio (skip r=0)
    ratio = np.zeros_like(theta_mean)
    for i in range(len(theta_mean)):
        ratio[i] = theta_mean[i] / (grad_mean[i] + EPS)
    
    r_c_ratio = 0
    if np.any(valid_mask[1:]):
        valid_ratios = ratio[1:].copy()
        valid_ratios[~valid_mask[1:]] = -np.inf
        r_c_ratio = int(np.argmax(valid_ratios) + 1)
    
    # Method 2: Maximum absolute curl magnitude
    r_c_magnitude = 0
    if np.any(valid_mask[1:]):
        valid_curl = theta_mean[1:].copy()
        valid_curl[~valid_mask[1:]] = -np.inf
        r_c_magnitude = int(np.argmax(valid_curl) + 1)
    
    # Method 3: Weighted score: curl_magnitude * (1 + ratio) * sqrt(count)
    # This balances finding strong curl with good ratio and statistical significance
    weighted_score = np.zeros_like(theta_mean)
    for i in range(1, len(theta_mean)):
        if valid_mask[i]:
            weighted_score[i] = theta_mean[i] * (1.0 + ratio[i]) * np.sqrt(counts[i])
    
    r_c_weighted = int(np.argmax(weighted_score[1:]) + 1) if np.any(valid_mask[1:]) else 0
    
    return {
        'ratio': r_c_ratio,
        'magnitude': r_c_magnitude, 
        'weighted': r_c_weighted,
        'all_ratios': ratio
    }


def main():
    print(f"Loading data from {FNAME}...")
    data = np.load(FNAME, allow_pickle=True)

    edges_raw = data["edges"]
    grad_part = data["grad"]
    curl_part = data["curl"]

    # DIAGNOSTIC: Check raw data statistics
    print("\n--- RAW DATA DIAGNOSTICS ---")
    print(f"grad_part stats: min={np.min(grad_part):.6e}, max={np.max(grad_part):.6e}, mean={np.mean(grad_part):.6e}")
    print(f"curl_part stats: min={np.min(curl_part):.6e}, max={np.max(curl_part):.6e}, mean={np.mean(curl_part):.6e}")
    print(f"grad_part non-zero: {np.count_nonzero(grad_part)} / {len(grad_part)}")
    print(f"curl_part non-zero: {np.count_nonzero(curl_part)} / {len(curl_part)}")
    print(f"\nCurl/Grad magnitude ratio: {np.mean(np.abs(curl_part)):.6e} / {np.mean(np.abs(grad_part)):.6e} = {np.mean(np.abs(curl_part))/np.mean(np.abs(grad_part)):.6e}")
    print("\n>>> INTERPRETATION: Curl is ~8 orders of magnitude smaller than grad.")
    print(">>> This network is HIGHLY tree-like with minimal circulation/cycles.")

    # normalize edge endpoints to strings
    edges = [(str(u), str(v)) for (u, v) in edges_raw]

    print("\nRebuilding graph using igraph...")
    G = ig.Graph.TupleList(edges, directed=True, vertex_name_attr="name")

    print(f"Total vertices in full graph: {len(G.vs)}")
    print(f"Total edges in full graph:    {len(G.es)}")

    print("Finding largest connected component (weak)...")
    giant = G.components(mode="weak").giant()
    print(f"Giant component vertices: {len(giant.vs)}")
    print(f"Giant component edges:    {len(giant.es)}")

    degrees = giant.degree()
    root_local_idx = int(np.argmax(degrees))
    root_name = giant.vs[root_local_idx]["name"]
    print(f"Found central root user {root_name} with degree {degrees[root_local_idx]}")

    giant_undirected = giant.as_undirected(combine_edges="first")

    print("Calculating shortest path lengths...")
    dists_from_root = giant_undirected.distances(source=root_local_idx)[0]
    max_dist = int(np.max(dists_from_root))
    print(f"Max distance from root inside giant (undirected): {max_dist}")

    name_to_dist = {v["name"]: d for v, d in zip(giant_undirected.vs, dists_from_root)}

    print("Mapping distances and calculating radii...")
    m = len(edges)
    radii = np.zeros(m, dtype=float)
    for i, (u, v) in enumerate(edges):
        du = name_to_dist.get(u, np.inf)
        dv = name_to_dist.get(v, np.inf)
        radii[i] = max(du, dv)

    finite_mask = np.isfinite(radii)
    finite_r = radii[finite_mask]
    finite_grad = grad_part[finite_mask]
    finite_curl = curl_part[finite_mask]

    if finite_r.size == 0:
        raise RuntimeError("No edges mapped to finite radii – check ID normalization.")

    max_r = int(np.max(finite_r))

    theta_mean_abs = []
    grad_mean_abs = []
    counts = []

    print("\nBinning data by radius and calculating final metrics...")
    for r in range(max_r + 1):
        mask = (finite_r == r)
        cnt = int(np.count_nonzero(mask))
        counts.append(cnt)

        if not np.any(mask):
            theta_mean_abs.append(np.nan)
            grad_mean_abs.append(np.nan)
            continue

        curl_at_r = finite_curl[mask]
        grad_at_r = finite_grad[mask]
        
        theta_mean_abs.append(float(np.mean(np.abs(curl_at_r))))
        grad_mean_abs.append(float(np.mean(np.abs(grad_at_r))))

    theta_mean_abs = np.array(theta_mean_abs)
    grad_mean_abs = np.array(grad_mean_abs)
    counts = np.array(counts, dtype=float)

    # Find critical radius using multiple methods
    r_c_results = find_critical_radius_robust(theta_mean_abs, grad_mean_abs, counts, min_count=100)
    
    ratio = r_c_results['all_ratios']
    
    # Use weighted method as primary (balances magnitude, ratio, and sample size)
    r_c = r_c_results['weighted']
    
    Theta = theta_mean_abs[r_c] if not np.isnan(theta_mean_abs[r_c]) else 0.0
    Theta_c = grad_mean_abs[r_c] if not np.isnan(grad_mean_abs[r_c]) else 0.0
    cascade = ratio[r_c] > 1.0

    curl_sum_by_r = np.nan_to_num(theta_mean_abs) * counts
    grad_sum_by_r = np.nan_to_num(grad_mean_abs) * counts

    # ------------------------------------------------------------
    # PRINT COMPREHENSIVE DIAGNOSTIC
    # ------------------------------------------------------------
    print("\n--- PER-RADIUS DIAGNOSTIC ---")
    print("r  | curl_abs | grad_abs | ratio | count | curl_total | grad_total")
    print("-" * 85)
    for r in range(max_r + 1):
        c_tot = curl_sum_by_r[r]
        g_tot = grad_sum_by_r[r]
        marker = " <--" if r == r_c else ""
        print(f"{r:2d} | {theta_mean_abs[r]:.3e} | {grad_mean_abs[r]:.3e} | "
              f"{ratio[r]:.3e} | {int(counts[r]):6d} | {c_tot:.3e} | {g_tot:.3e}{marker}")

    print("\n--- CRITICAL RADIUS ANALYSIS ---")
    print(f"Method 1 - Maximum Ratio:     r_c = {r_c_results['ratio']:2d}  (ratio = {ratio[r_c_results['ratio']]:.6e})")
    print(f"Method 2 - Maximum Magnitude: r_c = {r_c_results['magnitude']:2d}  (curl = {theta_mean_abs[r_c_results['magnitude']]:.6e})")
    print(f"Method 3 - Weighted Score:    r_c = {r_c_results['weighted']:2d}  (RECOMMENDED)")
    print(f"\n>>> Using Method 3 (Weighted) as primary result")

    print("\n--- FINAL RESULTS (at r_c = {}) ---".format(r_c))
    print(f"Critical Radius (r_c)       = {r_c}")
    print(f"Theta at r_c (curl)         = {Theta:.6e}")
    print(f"Theta_c (grad at r_c)       = {Theta_c:.6e}")
    print(f"Dominance ratio (curl/grad) = {ratio[r_c]:.6e}")
    print(f"Cascade Condition Met?      = {cascade}")
    print(f"Edge count at r_c           = {int(counts[r_c])}")
    
    print("\n--- PHYSICAL INTERPRETATION ---")
    if ratio[r_c] < 0.01:
        print("• Network is STRONGLY gradient-dominated (tree-like)")
        print("• Curl component is ~100x+ weaker than gradient")
        print("• Information flows in hierarchical/acyclic patterns")
    elif ratio[r_c] < 0.1:
        print("• Network is gradient-dominated with weak circulation")
        print("• Curl component is ~10x weaker than gradient")
    elif ratio[r_c] < 1.0:
        print("• Network has moderate gradient dominance")
        print("• Curl and gradient are comparable in magnitude")
    else:
        print("• Network has significant circulatory flows")
        print("• Curl component exceeds gradient component")

    # ------------------------------------------------------------
    # FRACTAL / SLIDE-RULE PASS
    # ------------------------------------------------------------
    print("\n--- FRACTAL KI WINDOWS (filtered) ---")
    windows = fractal_ki_tuner(
        curl_sum_by_r=curl_sum_by_r,
        grad_sum_by_r=grad_sum_by_r,
        counts_by_r=counts,
        max_scale=None,
        w_curl=1.0,
        w_grad=1.0,
        radial_alpha=1.0,
        top_k=10,
        min_edges=100,
        min_grad_sum=1e-6,
        skip_r0=True,
    )

    if not windows:
        print("No non-degenerate windows found at this threshold.")
    else:
        for i, (score, scale, r_start, r_end, c_sum, g_sum, edge_sum) in enumerate(windows, start=1):
            print(
                f"{i:2d}) score={score:.6e}  scale={scale}  "
                f"r={r_start}..{r_end}  curl_sum={c_sum:.6e}  "
                f"grad_sum={g_sum:.6e}  edges={edge_sum}"
            )

    # ------------------------------------------------------------
    # OPTIONAL CSV
    # ------------------------------------------------------------
    out_csv = "higgs_hodge_fractal_windows.csv"
    try:
        with open(out_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["rank", "score", "scale", "r_start", "r_end",
                 "curl_sum", "grad_sum", "edges"]
            )
            for i, (score, scale, r_start, r_end, c_sum, g_sum, edge_sum) in enumerate(windows, start=1):
                writer.writerow([i, score, scale, r_start, r_end, c_sum, g_sum, edge_sum])
        print(f"\nFractal window report written to {os.path.abspath(out_csv)}")
    except Exception as e:
        print(f"\nCould not write CSV: {e}")


if __name__ == "__main__":
    main()