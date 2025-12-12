#!/usr/bin/env python
"""
fractal_tda_pipeline.py

Topological Data Analysis on the Pirouette latent point cloud.

- Loads latent_cloud.npz (expects XYZ, anchor_flat, ftle_flat, tension_flat, spin_flat, stiff_flat)
- Optionally selects a "residue" / D+ subset via thresholds
- Clusters points with DBSCAN to isolate islands
- Runs persistent homology (Rips) with ripser (H0/H1/H2)
- Saves persistence diagrams and raw diagrams to disk
"""

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances
import gc

from ripser import ripser
from persim import plot_diagrams


# ----------------------------
# 1. Loading + optional masking
# ----------------------------

def load_latent_cloud(path):
    data = np.load(path)
    XYZ = data["XYZ"].astype(float)

    # Optional fields (used for masking if present)
    fields = {}
    for key in ["anchor_flat", "ftle_flat", "tension_flat", "spin_flat", "stiff_flat"]:
        if key in data:
            fields[key] = data[key].astype(float)

    return XYZ, fields


def make_residue_mask(fields, mode="none"):
    """
    Build a boolean mask selecting the "interesting" asymmetry region.

    You should feel free to EDIT this function once you see which cuts
    actually isolate the D+ island you care about.
    """
    N = len(next(iter(fields.values()))) if fields else 0
    if mode == "none" or not fields:
        return np.ones(N, dtype=bool)

    ftle    = fields.get("ftle_flat")
    tension = fields.get("tension_flat")
    anchor  = fields.get("anchor_flat")
    spin    = fields.get("spin_flat")
    stiff   = fields.get("stiff_flat")

    mask = np.ones(N, dtype=bool)

    if mode == "high_ftle_tail":
        # Example: keep the chaotic tail in FTLE
        if ftle is None:
            raise ValueError("FTLE field not available for masking")
        thr = np.percentile(ftle, 85)
        mask &= ftle >= thr

    elif mode == "D_plus_example":
        # Example asymmetric residue cut: tweak these after you inspect histograms.
        if ftle is not None:
            mask &= ftle >= np.percentile(ftle, 80)
        if tension is not None:
            mask &= tension >= np.percentile(tension, 40)  # not *too* negative
        if anchor is not None:
            mask &= anchor >= np.percentile(anchor, 40)
        if stiff is not None:
            mask &= stiff >= np.percentile(stiff, 60)

    else:
        raise ValueError(f"Unknown residue mask mode: {mode}")

    return mask


# ----------------------------
# 2. Clustering
# ----------------------------

def cluster_cloud(X, eps_scale=0.05, min_samples=15):
    """
    Cluster the point cloud using DBSCAN.

    eps is chosen as eps_scale * (max pairwise distance),
    which you can tweak on the command line.
    """
    # Standardize so DBSCAN is isotropic
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    # crude diameter
    dists = pairwise_distances(X_std, metric="euclidean")
    max_dist = np.max(dists)
    eps = eps_scale * max_dist

    print(f"[DBSCAN] max_dist={max_dist:.3f}, eps={eps:.3f}, min_samples={min_samples}")

    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(X_std)

    unique, counts = np.unique(labels, return_counts=True)
    print("[DBSCAN] cluster sizes (label: count):")
    for u, c in zip(unique, counts):
        print(f"  {u:3d}: {c}")

    return labels, scaler


# ----------------------------
# 3. TDA helpers
# ----------------------------

def guess_rips_thresh(X_std, percentile=95.0):
    """
    Choose a distance threshold for ripser based on a high-distance percentile.
    """
    dists = pairwise_distances(X_std, metric="euclidean")
    thr = np.percentile(dists, percentile)
    print(f"[TDA] Using Rips threshold (percentile {percentile}) = {thr:.3f}")
    return thr


def run_ripser_on_cluster(X, label, out_dir, maxdim=2, percentile=95.0):
    """
    Run ripser on one subset X and save diagrams + data.
    Implements a checkpoint/caching mechanism and explicit GC.
    """
    # 1. Define the checkpoint file path
    npz_path = os.path.join(out_dir, f"cluster_{label}_tda.npz")

    if len(X) == 0:
        print(f"[TDA] Cluster {label}: empty, skipping")
        return

    # --- Checkpoint/Cache Logic ---
    if os.path.exists(npz_path):
        print(f"[TDA] Cluster {label}: Found checkpoint at {npz_path}. Loading cached results.")
        # Load the cached diagrams for plotting/verification (optional)
        try:
            cached_data = np.load(npz_path, allow_pickle=True)
            diagrams = [cached_data[f'H{dim}'] for dim in range(maxdim + 1)]
            print(f"[TDA] Cluster {label}: Loaded H0/H1/H2 diagrams successfully.")
        except Exception as e:
            print(f"[TDA] WARNING: Could not load cached file: {e}. Re-running ripser.")
            diagrams = None # Force a re-run if loading fails
    else:
        diagrams = None

    # Only run ripser if diagrams couldn't be loaded from the cache
    if diagrams is None:
        # Standardize inside cluster for more stable thresholds
        scaler = StandardScaler()
        X_std = scaler.fit_transform(X)

        thresh = guess_rips_thresh(X_std, percentile=percentile)

        print(f"[TDA] Cluster {label}: N={len(X)}, running ripser(maxdim={maxdim}, thresh={thresh:.3f})")
        
        # --- THE TIME-CONSUMING STEP ---
        # 1. Explicit garbage collection before the memory-intensive step
        gc.collect() 
        result = ripser(X_std, maxdim=maxdim, thresh=thresh)
        # 2. Explicit garbage collection after processing the result
        gc.collect() 
        
        diagrams = result["dgms"]

        # --- Save diagrams numerically (Creating the checkpoint)
        # Note: Added check for list length before saving H1/H2 in case maxdim < 2
        np.savez(
            npz_path,
            H0=diagrams[0],
            H1=diagrams[1] if len(diagrams) > 1 else np.zeros((0, 2)),
            H2=diagrams[2] if len(diagrams) > 2 else np.zeros((0, 2)),
        )
        print(f"[TDA] Cluster {label}: Numerical data saved to checkpoint {npz_path}.")


    # --- Always Plot persistence diagrams (even from cache)
    # ... (plotting logic is unchanged) ...
    if diagrams is not None:
        fig, ax = plt.subplots(1, maxdim + 1, figsize=(4 * (maxdim + 1), 4))
        if maxdim == 0:
            ax = [ax]

        for dim in range(maxdim + 1):
            if dim < len(diagrams): # Check if the dimension exists in the loaded data
                plot_diagrams(diagrams[dim], ax=ax[dim])
                ax[dim].set_title(f"Cluster {label} – H{dim}")
            else:
                ax[dim].set_title(f"Cluster {label} – H{dim} (Not Computed)")
        
        png_path = os.path.join(out_dir, f"cluster_{label}_tda.png")
        fig.tight_layout()
        fig.savefig(png_path, dpi=200)
        plt.close(fig)
        print(f"[TDA] Cluster {label}: Plot saved to {png_path}.")
    else:
        print(f"[TDA] Cluster {label}: Plotting skipped due to error or missing diagrams.")

# You must replace the existing run_ripser_on_cluster with this modified version.


# ----------------------------
# 4. Main pipeline
# ----------------------------

def main():
    parser = argparse.ArgumentParser(description="TDA on Pirouette latent cloud")
    parser.add_argument(
        "--cloud",
        default="latent_cloud.npz",
        help="Path to latent_cloud.npz (default: latent_cloud.npz)",
    )
    parser.add_argument(
        "--mask-mode",
        default="none",
        choices=["none", "high_ftle_tail", "D_plus_example"],
        help="Residue mask to apply before clustering",
    )
    parser.add_argument(
        "--eps-scale",
        type=float,
        default=0.05,
        help="DBSCAN eps as fraction of diameter (default: 0.05)",
    )
    parser.add_argument(
        "--min-samples",
        type=int,
        default=15,
        help="DBSCAN min_samples (default: 15)",
    )
    parser.add_argument(
        "--maxdim",
        type=int,
        default=2,
        help="Max homology dimension for ripser (default: 2)",
    )
    parser.add_argument(
        "--percentile",
        type=float,
        default=95.0,
        help="Percentile of pairwise distances to use as Rips threshold (default: 95)",
    )
    parser.add_argument(
        "--out-dir",
        default="tda_output",
        help="Directory to store TDA results (default: tda_output)",
    )

    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    print(f"[LOAD] {args.cloud}")
    XYZ, fields = load_latent_cloud(args.cloud)
    N = XYZ.shape[0]
    print(f"[LOAD] N={N} points")

    # ------ Mask ------
    if args.mask_mode != "none":
        mask = make_residue_mask(fields, mode=args.mask_mode)
        XYZ = XYZ[mask]
        print(f"[MASK] Mode={args.mask_mode}, kept {XYZ.shape[0]} points")

    # ------ Global TDA on entire (masked) cloud ------
    print("\n===== GLOBAL TDA ON CLOUD =====")
    run_ripser_on_cluster(
        XYZ,
        label="global",
        out_dir=args.out_dir,
        maxdim=args.maxdim,
        percentile=args.percentile,
    )

    # ------ Clustering ------
    print("\n===== CLUSTERING + PER-CLUSTER TDA =====")
    labels, _ = cluster_cloud(
        XYZ, eps_scale=args.eps_scale, min_samples=args.min_samples
    )

    cluster_ids = sorted(set(labels))
    for cid in cluster_ids:
        if cid == -1:
            # DBSCAN noise – still interesting, so we *can* analyze it if big enough
            subset = XYZ[labels == cid]
            if len(subset) < 50:
                print(f"[TDA] Noise cluster (-1) too small (N={len(subset)}), skipping.")
                continue
            label_str = "noise"
        else:
            subset = XYZ[labels == cid]
            if len(subset) < 30:
                print(f"[TDA] Cluster {cid} too small (N={len(subset)}), skipping.")
                continue
            label_str = f"{cid}"

        print(f"\n--- Cluster {label_str}: N={len(subset)} ---")
        run_ripser_on_cluster(
            subset,
            label=label_str,
            out_dir=args.out_dir,
            maxdim=args.maxdim,
            percentile=args.percentile,
        )


if __name__ == "__main__":
    main()
