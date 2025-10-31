import pandas as pd
import numpy as np
import itertools
import os
import json
from tqdm import tqdm

# -------------------------- Config -------------------------- #
CONFIG = {
    "input_csv": "Magnetics_E-935646-1-1_kappa.csv",
    "output_dir": "triad_results",
    "results_csv": "triad_analysis_results.csv",
    "checkpoint_file": "checkpoint.json",
    "batch_size": 1000,  # Save progress every N combinations
}

# ------------------- Core Functions ------------------- #

def calculate_triad_metrics(p1, p2, p3):
    """
    Calculates metrics for a triad of epochs in the phase space.
    'Detuning' can be thought of as the geometric properties of the
    triangle formed by these three points.
    """
    # Extract kappa (x) and performance (y) for each point
    k1, p_perf1 = p1['kappa_instability'], p1['performance_temp']
    k2, p_perf2 = p2['kappa_instability'], p2['performance_temp']
    k3, p_perf3 = p3['kappa_instability'], p3['performance_temp']

    # --- Geometric Metrics (The "Detuning") ---
    # Side lengths of the triangle in phase space
    side12 = np.sqrt((k1 - k2)**2 + (p_perf1 - p_perf2)**2)
    side23 = np.sqrt((k2 - k3)**2 + (p_perf2 - p_perf3)**2)
    side31 = np.sqrt((k3 - k1)**2 + (p_perf3 - p_perf1)**2)

    # Area of the triangle (a measure of how much phase space the triad covers)
    # Using Heron's formula
    s = (side12 + side23 + side31) / 2
    # Add a small epsilon to prevent sqrt of negative due to float precision
    area = np.sqrt(abs(s * (s - side12) * (s - side23) * (s - side31)))

    # --- Archetype and State Metrics ---
    archetypes = [p1['archetype'], p2['archetype'], p3['archetype']]
    # Count unique archetypes in the triad
    diversity = len(set(archetypes))

    return {
        # Identifiers
        "epoch1_idx": p1.name, "arch1": archetypes[0],
        "epoch2_idx": p2.name, "arch2": archetypes[1],
        "epoch3_idx": p3.name, "arch3": archetypes[2],
        # Geometric "Detuning" Metrics
        "triad_area": area,
        "triad_perimeter": s * 2,
        # State Metrics
        "archetype_diversity": diversity,
        "mean_kappa": np.mean([k1, k2, k3]),
        "mean_performance": np.mean([p_perf1, p_perf2, p_perf3]),
    }

def load_checkpoint(ckpt_path):
    """Loads the last processed combination index from the checkpoint file."""
    if os.path.exists(ckpt_path):
        with open(ckpt_path, 'r') as f:
            return json.load(f).get("last_processed_index", -1)
    return -1

def save_checkpoint(ckpt_path, index):
    """Saves the last processed index to the checkpoint file."""
    with open(ckpt_path, 'w') as f:
        json.dump({"last_processed_index": index}, f)

# ------------------- Main Pipeline ------------------- #

def main():
    print("Starting Plasma Post-Hoc Triadic Analysis...")

    # --- Setup ---
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    results_path = os.path.join(CONFIG["output_dir"], CONFIG["results_csv"])
    checkpoint_path = os.path.join(CONFIG["output_dir"], CONFIG["checkpoint_file"])

    # --- Load Data ---
    try:
        df = pd.read_csv(CONFIG["input_csv"])
        # Ensure an 'archetype' column exists. If not, create it.
        if 'archetype' not in df.columns:
             # Basic quadrant classification if not present
            median_kappa = df['kappa_instability'].median()
            median_perf = df['performance_temp'].median()
            df['archetype'] = 'Default'
            df.loc[(df['kappa_instability'] < median_kappa) & (df['performance_temp'] > median_perf), 'archetype'] = 'Weaver'
            df.loc[(df['kappa_instability'] > median_kappa) & (df['performance_temp'] > median_perf), 'archetype'] = 'Gladiator'
            df.loc[(df['kappa_instability'] < median_kappa) & (df['performance_temp'] < median_perf), 'archetype'] = 'Drifter'
            df.loc[(df['kappa_instability'] > median_kappa) & (df['performance_temp'] < median_perf), 'archetype'] = 'Vortex'

    except FileNotFoundError:
        print(f"FATAL ERROR: Input file not found at '{CONFIG['input_csv']}'")
        return

    # --- Prepare for Processing ---
    epoch_indices = df.index.tolist()
    # Using itertools.combinations to get all unique sets of 3 epochs
    all_combinations = list(itertools.combinations(epoch_indices, 3))
    total_combinations = len(all_combinations)

    print(f"Found {len(df)} epochs to analyze.")
    print(f"This will result in {total_combinations:,} unique triadic combinations.")

    # --- Resume from Checkpoint ---
    start_index = load_checkpoint(checkpoint_path) + 1
    if start_index > 0:
        print(f"Resuming from combination index {start_index}...")
    else:
        print("Starting a new analysis from the beginning.")
        # If starting fresh, create or clear the results file
        pd.DataFrame().to_csv(results_path, index=False)


    # --- Main Processing Loop ---
    results_batch = []
    # Use tqdm for a nice progress bar
    pbar = tqdm(enumerate(all_combinations), total=total_combinations, initial=start_index)

    # This is the critical block where silent crashes happen.
    try:
        for i, (idx1, idx2, idx3) in pbar:
            # Skip already processed combinations if resuming
            if i < start_index:
                continue

            # Get the data for the three points in the triad
            point1 = df.loc[idx1]
            point2 = df.loc[idx2]
            point3 = df.loc[idx3]

            # Calculate the "detuning" and other metrics
            triad_data = calculate_triad_metrics(point1, point2, point3)
            results_batch.append(triad_data)

            # --- Save Batch and Checkpoint ---
            if (i + 1) % CONFIG["batch_size"] == 0 or (i + 1) == total_combinations:
                # Append the batch to the main results CSV
                pd.DataFrame(results_batch).to_csv(results_path, mode='a', header=not os.path.exists(results_path) or os.path.getsize(results_path) == 0, index=False)
                results_batch.clear() # Clear the batch
                save_checkpoint(checkpoint_path, i) # Save progress
                pbar.set_description(f"Saved checkpoint at index {i}")


    except Exception as e:
        # This will now catch any error and prevent silent closing.
        print(f"\n\nFATAL ERROR during processing at combination index {i}:")
        print(f"Indices involved: ({idx1}, {idx2}, {idx3})")
        print(f"Error details: {e}")
        # Save any results we have before exiting
        if results_batch:
            pd.DataFrame(results_batch).to_csv(results_path, mode='a', header=not os.path.exists(results_path) or os.path.getsize(results_path) == 0, index=False)
        save_checkpoint(checkpoint_path, i-1 if i > 0 else -1)
        print("Partial results and latest checkpoint have been saved.")
        return

    print("\nAnalysis complete. All combinations processed.")
    print(f"Results saved to '{results_path}'")

if __name__ == '__main__':
    main()