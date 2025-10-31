# INSTRUMENT: The Seer (Local File Version)
# id: INST-WAVEFORM-ANALYZER-003
# version: 3.0 (replaces 2.0)
# parents: [DOMA-206]
#
# ABSTRACT: This script is a self-contained instrument for Pirouette Waveform
# analysis of local time-series data. It takes a file path from the command
# line, loads the specified stock or ETF data, and searches for its hidden
# helical coherence. This version removes the dependency on APIs, allowing for
# robust, repeatable analysis of large, local datasets.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import argparse
import os

def load_and_normalize_local_data(filename):
    """
    Loads time-series data from a local .txt file, extracts the 'Close'
    price, and normalizes it to oscillate between -1 and 1.
    """
    print(f"Loading and processing data from '{filename}'...")
    try:
        # The provided files are standard CSV format with a header.
        data = pd.read_csv(filename)
        
        # Ensure the required 'Close' column exists.
        if 'Close' not in data.columns:
            print(f"\n--- ERROR: 'Close' column not found in {filename} ---")
            sys.exit(1)
            
        price = pd.to_numeric(data['Close'])
        
        # Normalize the data.
        price_min = price.min()
        price_max = price.max()
        normalized_price = 2 * ((price - price_min) / (price_max - price_min)) - 1
        
        return normalized_price.values
        
    except FileNotFoundError:
        print(f"\n--- ERROR: DATA FILE NOT FOUND ---")
        print(f"The file '{filename}' was not found at the specified path.")
        sys.exit(1)
    except Exception as e:
        print(f"\n--- AN ERROR OCCURRED ---")
        print(f"Could not process the file. Error: {e}")
        sys.exit(1)

def calculate_coherence(data_3d):
    """
    Calculates the coherence of a 3D path by measuring its "smoothness."
    A lower score indicates a more coherent, less jagged path.
    """
    velocities = np.diff(data_3d, axis=0)
    accelerations = np.diff(velocities, axis=0)
    coherence_metric = np.sum(np.linalg.norm(accelerations, axis=1)**2)
    return coherence_metric

def find_optimal_kappa(data_1d, kappa_range, num_steps):
    """
    Scans a range of Chirality Factors (kappa) to find the one that
    produces the most coherent (smoothest) 3D waveform.
    """
    print(f"Scanning for optimal kappa across {num_steps} steps from {kappa_range[0]} to {kappa_range[1]}...")
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
    return optimal_kappa, kappas, coherence_scores

def plot_results(data_1d, optimal_kappa, kappas, coherence_scores, filename):
    """
    Visualizes the results of the analysis.
    """
    print(f"Optimal Chirality Factor (κ) for {os.path.basename(filename)} found: {optimal_kappa:.6f}")
    
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle(f"Pirouette Waveform Analysis of: {os.path.basename(filename)}", fontsize=20)
    
    # Plotting code remains largely the same as the previous version...
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(data_1d, color='gray')
    ax1.set_title("1. Original 1D Time Series (The 'Shadow')", fontsize=14)
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(kappas, coherence_scores, color='purple')
    ax2.axvline(optimal_kappa, color='red', linestyle='--', label=f'Optimal κ = {optimal_kappa:.6f}')
    ax2.set_title("2. Coherence Scan (Finding the Hidden Geometry)", fontsize=14)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)

    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    t = np.arange(len(data_1d))
    ax3.plot(data_1d, np.zeros_like(data_1d), t / len(t), color='black', alpha=0.7)
    ax3.set_title("3. Projection with κ = 0 (The Flat 'Noise')", fontsize=14)

    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    x_opt = data_1d * np.cos(optimal_kappa * t)
    y_opt = data_1d * np.sin(optimal_kappa * t)
    z_opt = t / len(t)
    ax4.plot(x_opt, y_opt, z_opt, color='red', alpha=0.9)
    ax4.set_title(f"4. Projection with Optimal κ = {optimal_kappa:.6f} (The 'Form')", fontsize=14)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == '__main__':
    # --- COMMAND-LINE INTERFACE SETUP ---
    # Use argparse to create a flexible and user-friendly command-line tool.
    parser = argparse.ArgumentParser(
        description="Pirouette Waveform Analyzer for local stock/ETF data.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "filepath", 
        help="The path to the input data file (e.g., 'Data/Stocks/a.us.txt')."
    )
    parser.add_argument(
        "--k_max", 
        type=float, 
        default=0.1, 
        help="The maximum kappa value to scan (default: 0.1)."
    )
    parser.add_argument(
        "--k_steps", 
        type=int, 
        default=500, 
        help="The number of steps to use in the kappa scan (default: 500)."
    )
    args = parser.parse_args()

    # --- EXECUTION ---
    # 1. Load data from the user-specified file
    market_data_1d = load_and_normalize_local_data(args.filepath)
    
    # 2. Analyze for hidden geometry using command-line parameters
    kappa_range = (0, args.k_max)
    opt_kappa, kappas, scores = find_optimal_kappa(market_data_1d, kappa_range, args.k_steps)
    
    # 3. Visualize the claim
    plot_results(market_data_1d, opt_kappa, kappas, scores, args.filepath)

