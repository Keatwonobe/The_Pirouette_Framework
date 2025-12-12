#!/usr/bin/env python3
import argparse
import gzip
import json
import os
from datetime import datetime

import pandas as pd
import networkx as nx
import numpy as np

from scipy import sparse
from scipy.sparse.linalg import spsolve, cg, LinearOperator


# ------------------------------------------------------------
# util: safe CG for weird scipy builds
# ------------------------------------------------------------
def safe_cg(A, b, tol=1e-5, maxiter=5000):
    """
    Try cg(..., tol=...), if that scipy doesn't support it, try rtol.
    Return (x, info).
    """
    try:
        x, info = cg(A, b, tol=tol, maxiter=maxiter)
        return x, info
    except TypeError:
        # older / different signature
        x, info = cg(A, b, rtol=tol, maxiter=maxiter)
        return x, info


# ------------------------------------------------------------
# 1. load SNAP file
# ------------------------------------------------------------
def load_activity(path, t_min=None, t_max=None):
    rows = []
    with gzip.open(path, "rt") as f:
        for line in f:
            a, b, ts, itype = line.strip().split()
            ts = int(ts)
            if (t_min is not None and ts < t_min) or (t_max is not None and ts > t_max):
                continue
            rows.append((int(a), int(b), ts, itype))
    return pd.DataFrame(rows, columns=["src", "dst", "ts", "itype"])


# ------------------------------------------------------------
# 2. core runner
# ------------------------------------------------------------
def run_hodge_on_df(df, outpath, reg=1e-6, use_cg=True, cg_tol=1e-5):
    # 2a. build graph with SNAP direction fix
    G = nx.DiGraph()
    for _, row in df.iterrows():
        u = row["dst"]  # original author
        v = row["src"]  # retweeter / replier
        w = 1.0
        if G.has_edge(u, v):
            G[u][v]["weight"] += w
        else:
            G.add_edge(u, v, weight=w)

    print(f"[run] nodes={G.number_of_nodes()} edges={G.number_of_edges()}")
    edges = list(G.edges())
    m = len(edges)
    n = G.number_of_nodes()
    node_index = {node: i for i, node in enumerate(G.nodes())}

    # 2b. incidence
    rows_i, cols_j, data = [], [], []
    for e_idx, (i, j) in enumerate(edges):
        rows_i.append(node_index[i]); cols_j.append(e_idx); data.append(-1.0)
        rows_i.append(node_index[j]); cols_j.append(e_idx); data.append(+1.0)
    B = sparse.coo_matrix((data, (rows_i, cols_j)), shape=(n, m)).tocsr()

    # 2c. observed flow
    J_obs = np.array([G[u][v]["weight"] for (u, v) in edges], dtype=float)

    # 2d. solve for J_opt without forming B.T@B
    Gamma = np.ones(m)

    def L_edge_matvec(v):
        # (I/Gamma) v + B^T B v
        part1 = (1.0 / Gamma) * v
        part2 = B.T @ (B @ v)
        return part1 + part2

    L_edge_op = LinearOperator((m, m), matvec=L_edge_matvec)

    if use_cg:
        print("[run] solving for J_opt (CG, version-tolerant)…")
        J_opt, info = safe_cg(L_edge_op, J_obs, tol=cg_tol, maxiter=5000)
        if info != 0:
            print(f"[warn] CG for J_opt did not fully converge (info={info}), trying simple smoothing fallback")
            # very simple fallback: one Jacobi-like step
            J_opt = J_obs.copy()
            # one step of projected smoothing
            J_opt = J_opt - 0.1 * (L_edge_op @ J_opt - J_obs)
    else:
        print("[run] solving for J_opt (direct)… (might be slow / large)")
        L_edge = sparse.diags(1.0 / Gamma) + B.T @ B
        J_opt = spsolve(L_edge.tocsr(), J_obs)

    # 2e. residual
    r = J_obs - J_opt

    # 2f. regularized node Laplacian for grad component
    BBt = B @ B.T
    max_diag = BBt.diagonal().max() if BBt.diagonal().size else 1.0
    eps = reg * max_diag
    BBt_reg = BBt + sparse.eye(n) * eps

    print(f"[run] solving (BB^T + {eps:g}I) phi = B r …")
    # version-tolerant solve again
    def BBt_op_vec(v):
        return BBt @ v + eps * v

    BBt_op = LinearOperator((n, n), matvec=BBt_op_vec)
    phi, info2 = safe_cg(BBt_op, B @ r, tol=1e-5, maxiter=5000)
    if info2 != 0:
        print(f"[warn] node solve did not fully converge (info={info2}), using direct solve")
        phi = spsolve(BBt_reg.tocsr(), B @ r)

    grad_part = B.T @ phi
    curl_part = r - grad_part

    # 2g. RENORMALIZE per edge
    energy = grad_part**2 + curl_part**2
    denom = np.sqrt(energy + 1e-12)
    grad_norm = grad_part / denom
    curl_norm = curl_part / denom
    ratio = np.abs(curl_part) / (np.abs(grad_part) + 1e-12)

    ratio_stats = {
        "min": float(np.min(ratio)),
        "max": float(np.max(ratio)),
        "mean": float(np.mean(ratio)),
        "p50": float(np.percentile(ratio, 50)),
        "p75": float(np.percentile(ratio, 75)),
        "p90": float(np.percentile(ratio, 90)),
        "p95": float(np.percentile(ratio, 95)),
        "p99": float(np.percentile(ratio, 99)),
    }

    # 2h. simple radius from main CC
    G_und = G.to_undirected()
    largest_cc_nodes = max(nx.connected_components(G_und), key=len)
    G_main = G.subgraph(largest_cc_nodes)
    degrees = dict(G_main.degree())
    root_user = max(degrees, key=degrees.get)
    lengths = nx.single_source_shortest_path_length(G_main, root_user)

    radii = np.zeros(m)
    for e_idx, (u, v) in enumerate(edges):
        du = lengths.get(u, np.inf)
        dv = lengths.get(v, np.inf)
        radii[e_idx] = max(du, dv)

    # 2i. write out
    np.savez(
        outpath,
        edges=np.array(edges, dtype=object),
        J_obs=J_obs,
        J_opt=J_opt,
        r=r,
        grad=grad_part,
        curl=curl_part,
        grad_norm=grad_norm,
        curl_norm=curl_norm,
        ratio=ratio,
        radii=radii,
        ratio_stats=np.array([ratio_stats], dtype=object),
    )

    with open(os.path.splitext(outpath)[0] + "_stats.json", "w") as f:
        json.dump(
            {
                "n_nodes": int(n),
                "n_edges": int(m),
                "reg": reg,
                "ratio_stats": ratio_stats,
            },
            f,
            indent=2,
        )

    print(f"[run] wrote {outpath}")
    print("[run] ratio stats:", ratio_stats)


# ------------------------------------------------------------
# 3. CLI
# ------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Rebuild Higgs Hodge NPZ (version-tolerant CG, normalized channels, ratio stats)."
    )
    ap.add_argument("--activity", default="higgs-activity_time.txt.gz",
                    help="SNAP Higgs activity file (gz).")
    ap.add_argument("--t-min", type=int, default=1341360000,
                    help="min timestamp (default = 2012-07-04 00:00)")
    ap.add_argument("--t-max", type=int, default=1341446400,
                    help="max timestamp (default = 2012-07-05 00:00)")
    ap.add_argument("--outdir", default=".",
                    help="where to write the npz files")
    ap.add_argument("--out", default="higgs_hodge_out.npz",
                    help="output npz filename (in outdir)")
    ap.add_argument("--reg", type=float, default=1e-6,
                    help="regularization strength for BB^T")
    ap.add_argument("--windows", type=int, default=1,
                    help="if >1, split [t_min, t_max] into this many equal windows and run each")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    df_all = load_activity(args.activity, t_min=args.t_min, t_max=args.t_max)
    print(f"[main] loaded {len(df_all)} rows in window "
          f"{args.t_min}–{args.t_max} ({datetime.utcfromtimestamp(args.t_min)} to {datetime.utcfromtimestamp(args.t_max)})")

    if args.windows == 1:
        outpath = os.path.join(args.outdir, args.out)
        run_hodge_on_df(df_all, outpath, reg=args.reg)
    else:
        span = args.t_max - args.t_min
        step = span // args.windows
        for i in range(args.windows):
            w_min = args.t_min + i * step
            w_max = w_min + step if i < args.windows - 1 else args.t_max
            df_w = df_all[(df_all["ts"] >= w_min) & (df_all["ts"] < w_max)]
            outname = f"higgs_hodge_out_win{i:02d}.npz"
            outpath = os.path.join(args.outdir, outname)
            print(f"[main] window {i}: {w_min}–{w_max} ({len(df_w)} rows)")
            if len(df_w) == 0:
                np.savez(outpath, edges=np.array([], dtype=object))
                print(f"[main] wrote empty {outpath}")
            else:
                run_hodge_on_df(df_w, outpath, reg=args.reg)


if __name__ == "__main__":
    main()
