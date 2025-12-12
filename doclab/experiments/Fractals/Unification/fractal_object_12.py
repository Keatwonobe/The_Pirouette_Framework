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


# --- New/Modified TDA function for memory-saving and streaming ---

def process_cluster_tda_generator(X, label, out_dir, maxdim=2, percentile=95.0, sample_size=5000):
    """
    Runs ripser on a cluster (with optional sampling) and yields the
    numerical persistence diagrams for immediate storage/streaming.
    """
    
    N_full = len(X)
    if N_full == 0:
        print(f"[TDA] Cluster {label}: empty, skipping")
        return # Generator stops
    
    # 1. Memory-Saving Sampling (Bootstrapping)
    if N_full > sample_size:
        # Randomly sample the point cloud to reduce memory usage for ripser
        print(f"[TDA] Cluster {label}: N={N_full} > {sample_size}. Sampling down to N={sample_size}.")
        # Select indices randomly without replacement
        sample_indices = np.random.choice(N_full, size=sample_size, replace=False)
        X_sampled = X[sample_indices]
    else:
        X_sampled = X
        
    N_used = len(X_sampled)

    # 2. Checkpoint Logic (Kept for sequential processing/re-running)
    npz_path = os.path.join(out_dir, f"cluster_{label}_tda.npz")
    
    # --- Checkpoint/Cache Logic ---
    if os.path.exists(npz_path):
        # ... (same loading logic as before) ...
        print(f"[TDA] Cluster {label}: Found checkpoint at {npz_path}. Loading cached results.")
        try:
            cached_data = np.load(npz_path, allow_pickle=True)
            diagrams = [cached_data[f'H{dim}'] for dim in range(maxdim + 1)]
            print(f"[TDA] Cluster {label}: Loaded H0/H1/H2 diagrams successfully.")
        except Exception as e:
            print(f"[TDA] WARNING: Could not load cached file: {e}. Re-running ripser.")
            diagrams = None
    else:
        diagrams = None

    # 3. Run Rips-Filtration (The memory-intensive step)
    if diagrams is None:
        # Standardize inside cluster/sample for stable thresholds
        scaler = StandardScaler()
        X_std = scaler.fit_transform(X_sampled)

        thresh = guess_rips_thresh(X_std, percentile=percentile)

        print(f"[TDA] Cluster {label}: N_used={N_used}, running ripser(maxdim={maxdim}, thresh={thresh:.3f})")
        
        # Explicit garbage collection before and after
        gc.collect() 
        result = ripser(X_std, maxdim=maxdim, thresh=thresh)
        gc.collect() 
        
        diagrams = result["dgms"]

        # Save checkpoint
        np.savez(
            npz_path,
            H0=diagrams[0],
            H1=diagrams[1] if len(diagrams) > 1 else np.zeros((0, 2)),
            H2=diagrams[2] if len(diagrams) > 2 else np.zeros((0, 2)),
        )
        print(f"[TDA] Cluster {label}: Numerical data saved to checkpoint {npz_path}.")


    # 4. Yield/Generate Results (The Streaming/Incremental Part)
    if diagrams is not None:
        fig, ax = plt.subplots(1, maxdim + 1, figsize=(4 * (maxdim + 1), 4))
        if maxdim == 0:
            ax = [ax]

        for dim in range(maxdim + 1):
            if dim < len(diagrams):
                # *** MODIFICATION START ***
                diagram = diagrams[dim]
                
                # Check if the diagram is empty (contains no points)
                if diagram.size > 0:
                    plot_diagrams(diagram, ax=ax[dim])
                else:
                    # Handle the empty case: just set up the axes without data
                    ax[dim].set_xlim(0, 1) # Set a default range
                    ax[dim].set_ylim(0, 1)
                    ax[dim].plot([0, 1], [0, 1], '--', color='gray') # Add the identity line
                    ax[dim].text(0.5, 0.5, "Empty Diagram", 
                                 ha='center', va='center', fontsize=12, color='red')
                
                ax[dim].set_title(f"Cluster {label} – H{dim} (N_used={N_used})")
                # *** MODIFICATION END ***
            else:
                ax[dim].set_title(f"Cluster {label} – H{dim} (Not Computed)")
        
        png_path = os.path.join(out_dir, f"cluster_{label}_tda.png")
        fig.tight_layout()
        fig.savefig(png_path, dpi=200)
        plt.close(fig)
        print(f"[TDA] Cluster {label}: Plot saved to {png_path}.")

        # *** The Generator Yield Step ***
        # Yield the results for immediate consumption/database insertion
        yield {
            'label': label,
            'N_full': N_full,
            'N_used': N_used,
            'diagrams': diagrams, # The list of [H0, H1, H2] arrays
            'png_path': png_path,
            'npz_path': npz_path
        }


# You must replace the existing run_ripser_on_cluster with this modified version.


# ----------------------------
# 4. Main pipeline
# ----------------------------

# --- Replacement of the original main function ---

# Placeholder for your database insertion logic
def stream_to_database(tda_result):
    """
    This function simulates inserting the TDA result of one cluster
    (one row) into a database. Replace with actual DB logic (e.g., SQLAlchemy,
    Pandas, or a NoSQL insert).
    """
    label = tda_result['label']
    n_full = tda_result['N_full']
    n_used = tda_result['N_used']
    h0_size = len(tda_result['diagrams'][0])
    h1_size = len(tda_result['diagrams'][1])
    
    print(f"\n[STREAM] --- INSERTING RESULTS FOR CLUSTER '{label}' ---")
    print(f"[STREAM] Full size: {n_full}, Analyzed size (N_used): {n_used}")
    print(f"[STREAM] Persistent Homology Counts: H0={h0_size}, H1={h1_size}")
    # In a real app, you would serialize and insert tda_result['diagrams']

# The main function logic remains similar, but it now iterates over the
# cluster processing, calling stream_to_database for each result.

def main():
    parser = argparse.ArgumentParser(description="TDA on Pirouette latent cloud")
    parser.add_argument(
        "--cloud",
        default="latent_cloud.npz",
        help="Path to latent_cloud.npz (default: latent_cloud.npz)",
    )
    # ... (other arguments unchanged) ...
    parser.add_argument(
        "--sample-size",
        type=int,
        default=7000,
        help="Max number of points to use for ripser on any cluster (default: 5000). Set to 0 to disable.",
    )
    parser.add_argument(
        "--out-dir",
        default="tda_output",
        help="Directory to store TDA results (default: tda_output)",
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

    # ------ List to hold all generators ------
    # We will compute the results one by one but use a list to manage them for simplicity
    # This structure ensures only ONE cluster is being analyzed at a time.
    tda_generators = [] 

    # ------ 1. Global TDA on entire (masked) cloud ------
    print("\n===== GLOBAL TDA ON CLOUD (Start Generator) =====")
    global_gen = process_cluster_tda_generator(
        XYZ,
        label="global",
        out_dir=args.out_dir,
        maxdim=args.maxdim,
        percentile=args.percentile,
        sample_size=args.sample_size
    )
    tda_generators.append(global_gen)


    # ------ 2. Clustering ------
    print("\n===== CLUSTERING + PER-CLUSTER TDA (Start Generator) =====")
    labels, _ = cluster_cloud(
        XYZ, eps_scale=args.eps_scale, min_samples=args.min_samples
    )

    cluster_ids = sorted(set(labels))
    for cid in cluster_ids:
        # ... (same subset filtering logic as before) ...
        if cid == -1:
            subset = XYZ[labels == cid]
            if len(subset) < 50:
                continue
            label_str = "noise"
        else:
            subset = XYZ[labels == cid]
            if len(subset) < 30:
                continue
            label_str = f"{cid}"

        # Create a generator for this cluster
        cluster_gen = process_cluster_tda_generator(
            subset,
            label=label_str,
            out_dir=args.out_dir,
            maxdim=args.maxdim,
            percentile=args.percentile,
            sample_size=args.sample_size
        )
        tda_generators.append(cluster_gen)

    # ------ 3. Consumer Loop: Iteratively run and stream the generators ------
    print("\n===== STREAMING RESULTS TO DATABASE/SINK =====")
    for gen in tda_generators:
        # Calling next() on the generator runs the full TDA for that one cluster/subset
        try:
            result = next(gen)
            stream_to_database(result)
        except StopIteration:
            # The generator was empty (e.g., subset size was 0), which is handled
            # gracefully inside process_cluster_tda_generator
            pass
        # Explicitly delete the result and run GC after each streaming operation
        del result
        gc.collect() 
        print(f"| Memory check: Freed resources after cluster.")
        

if __name__ == "__main__":
    main()
