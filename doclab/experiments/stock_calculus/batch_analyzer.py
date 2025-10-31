# INSTRUMENT: The Surveyor
# id: INST-WAVEFORM-SURVEYOR-001
# version: 1.0
# parents: [INST-WAVEFORM-ANALYZER-003, DOMA-206]
#
# ABSTRACT: This script extends the single-file analyzer into a high-throughput
# research instrument. It traverses a directory of time-series data, calculates
# the optimal Chirality Factor (kappa) for each file, and aggregates the
# results. The final output is both a data file (CSV) containing the kappa
# for each asset and a histogram visualizing the distribution of these values.
# This allows for the discovery of systemic "laws" and the identification of
# anomalies within a large dataset, revealing the collective geometry of a market.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse
import os
from tqdm import tqdm

def load_and_normalize_local_data(filename):
    """
    Loads and normalizes a single data file. Returns None on failure.
    """
    try:
        data = pd.read_csv(filename)
        if 'Close' not in data.columns or data['Close'].isnull().all():
            return None
        price = pd.to_numeric(data['Close'].dropna())
        if len(price) < 50: # Skip very short time-series
            return None
        price_min = price.min()
        price_max = price.max()
        if (price_max - price_min) == 0:
            return None # Skip flat-lined data
        normalized_price = 2 * ((price - price_min) / (price_max - price_min)) - 1
        return normalized_price.values
    except Exception:
        return None

def calculate_coherence(data_3d):
    """
    Calculates the coherence of a 3D path.
    """
    velocities = np.diff(data_3d, axis=0)
    accelerations = np.diff(velocities, axis=0)
    coherence_metric = np.sum(np.linalg.norm(accelerations, axis=1)**2)
    return coherence_metric

def find_optimal_kappa(data_1d, kappa_range, num_steps):
    """
    Scans a range of Chirality Factors (kappa) to find the optimal value.
    """
    kappas = np.linspace(kappa_range[0], kappa_range[1], num_steps)
    coherence_scores = []
    t = np.arange(len(data_1d))

    for kappa in kappas:
        x = data_1d * np.cos(kappa * t)
        y = data_1d * np.sin(kappa * t)
        z = t / len(t)
        data_3d = np.vstack([x, y, z]).T
        score = calculate_coherence(data_3d)
        coherence_scores.append(score)

    min_score_index = np.argmin(coherence_scores)
    optimal_kappa = kappas[min_score_index]
    return optimal_kappa

def plot_kappa_distribution(results_df, output_dir):
    """
    Plots a histogram of the calculated optimal kappa values.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    kappas = results_df['optimal_kappa']
    ax.hist(kappas, bins=50, color='purple', alpha=0.7, edgecolor='white')
    
    mean_kappa = kappas.mean()
    median_kappa = kappas.median()
    
    ax.axvline(mean_kappa, color='red', linestyle='--', linewidth=2, label=f'Mean κ = {mean_kappa:.4f}')
    ax.axvline(median_kappa, color='cyan', linestyle=':', linewidth=2, label=f'Median κ = {median_kappa:.4f}')
    
    ax.set_title('Distribution of Optimal Chirality (κ) Across a Market', fontsize=16)
    ax.set_xlabel('Optimal Chirality Factor (κ)', fontsize=12)
    ax.set_ylabel('Number of Assets', fontsize=12)
    ax.legend()
    
    # Save the plot
    plot_filename = os.path.join(output_dir, 'kappa_distribution.png')
    plt.savefig(plot_filename)
    print(f"\nDistribution plot saved to '{plot_filename}'")
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Batch Pirouette Waveform Analyzer for local directories.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("directory", help="The path to the input directory (e.g., 'Data/Stocks/').")
    parser.add_argument("--output_dir", default='.', help="Directory to save the results CSV and plot (default: current dir).")
    parser.add_argument("--k_max", type=float, default=0.1, help="Maximum kappa value to scan (default: 0.1).")
    parser.add_argument("--k_steps", type=int, default=100, help="Number of steps in the kappa scan (default: 100).")
    args = parser.parse_args()

    # --- EXECUTION ---
    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found at '{args.directory}'")
        sys.exit(1)
        
    os.makedirs(args.output_dir, exist_ok=True)
    
    results = []
    file_paths = [os.path.join(root, file) for root, _, files in os.walk(args.directory) for file in files if file.endswith('.txt')]

    print(f"Found {len(file_paths)} .txt files. Starting analysis...")
    
    for filepath in tqdm(file_paths, desc="Analyzing Assets"):
        data_1d = load_and_normalize_local_data(filepath)
        if data_1d is not None:
            kappa_range = (0, args.k_max)
            opt_kappa = find_optimal_kappa(data_1d, kappa_range, args.k_steps)
            results.append({'asset': os.path.basename(filepath), 'optimal_kappa': opt_kappa})

    if not results:
        print("No valid data files could be processed.")
        sys.exit(0)

    # Save results to CSV
    results_df = pd.DataFrame(results)
    output_csv = os.path.join(args.output_dir, 'kappa_results.csv')
    results_df.to_csv(output_csv, index=False)
    print(f"\nAnalysis complete. Results for {len(results_df)} assets saved to '{output_csv}'")
    
    # Plot the distribution
    plot_kappa_distribution(results_df, args.output_dir)
