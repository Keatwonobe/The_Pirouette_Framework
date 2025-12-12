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

    We need counts to reject r=0 .. r=0 cases with count=1.
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


def main():
    print(f"Loading data from {FNAME}...")
    data = np.load(FNAME, allow_pickle=True)

    edges_raw = data["edges"]
    grad_part = data["grad"]
    curl_part = data["curl"]

    # normalize edge endpoints to strings
    edges = [(str(u), str(v)) for (u, v) in edges_raw]

    print("Rebuilding graph using igraph...")
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

    theta_mean = []
    grad_mean = []
    counts = []

    print("Binning data by radius and calculating final metrics...")
    for r in range(max_r + 1):
        mask = (finite_r == r)
        cnt = int(np.count_nonzero(mask))
        counts.append(cnt)

        if not np.any(mask):
            theta_mean.append(np.nan)
            grad_mean.append(np.nan)
            continue

        curl_energy = (finite_curl[mask] ** 2)
        grad_energy = (finite_grad[mask] ** 2)

        th_m = float(np.mean(curl_energy))
        gr_m = float(np.mean(grad_energy))

        theta_mean.append(th_m)
        grad_mean.append(gr_m)

    theta_mean = np.array(theta_mean)
    grad_mean = np.array(grad_mean)
    counts = np.array(counts, dtype=float)

    curl_sum_by_r = np.nan_to_num(theta_mean) * counts
    grad_sum_by_r = np.nan_to_num(grad_mean) * counts

    # classical ratio
    ratio = np.zeros_like(theta_mean)
    for i in range(len(theta_mean)):
        num = curl_sum_by_r[i]
        den = grad_sum_by_r[i] + EPS
        ratio[i] = num / den

    # classical r_c
    if max_r >= 1:
        r_candidates = np.arange(1, max_r + 1)
        r_c_idx = np.nanargmax(ratio[1:])
        r_c = int(r_candidates[r_c_idx])
    else:
        r_c = 0

    Theta = theta_mean[r_c] if not np.isnan(theta_mean[r_c]) else 0.0
    Theta_c = grad_mean[r_c] if not np.isnan(grad_mean[r_c]) else 0.0
    cascade = ratio[r_c] > 1.0

    # ------------------------------------------------------------
    # PRINT classical diag
    # ------------------------------------------------------------
    print("\n--- PER-RADIUS DIAGNOSTIC (r, mean_curl, mean_grad, ratio, count) ---")
    for r in range(max_r + 1):
        th = theta_mean[r]
        gr = grad_mean[r]
        rt = ratio[r]
        cnt = counts[r]
        print(f"{r:3d}: {th:.6e}  {gr:.6e}  ratio={rt:.6e}  count={int(cnt)}")

    print("\n--- FINAL (CLASSICAL) RESULTS ---")
    print(f"Critical Radius (r_c) = {r_c}")
    print(f"Theta at r_c          = {Theta:.6f}")
    print(f"Theta_c (critical)    = {Theta_c:.6f}")
    print(f"Dominance ratio       = {ratio[r_c]:.6f}")
    print(f"Cascade Condition Met?  {cascade}")

    # ------------------------------------------------------------
    # FRACTAL / SLIDE-RULE PASS (with guards)
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
        min_edges=100,     # THIS kills r=0
        min_grad_sum=1e-6, # THIS kills grad≈0 windows
        skip_r0=True,
    )

    if not windows:
        print("No non-degenerate windows found at this threshold. "
              "Try lowering min_edges or min_grad_sum.")
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
