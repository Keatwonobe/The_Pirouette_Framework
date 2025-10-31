# INSTRUMENT PART 2: The Seer
# id: INST-WAVEFORM-ANALYZER-002
# version: 2.0 (replaces 1.1)
# parents: [DOMA-206]
#
# ABSTRACT: This script performs the core Pirouette Waveform analysis. It loads
# a pre-fetched, one-dimensional time-series from a local file and searches
# for its hidden helical coherence. By operating on local data, it can run
# instantly and repeatedly, allowing for deep, uninterrupted exploration of
# the dataset's latent geometric structure and its Chirality Factor (kappa).

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

def load_local_data(filename):
    """
    Loads normalized time-series data from a local CSV file.
    """
    print(f"Loading data from '{filename}'...")
    try:
        data = pd.read_csv(filename)
        return data['normalized_price'].values
    except FileNotFoundError:
        print(f"\n--- ERROR: DATA FILE NOT FOUND ---")
        print(f"The file '{filename}' was not found.")
        print("Please run the 'data_fetcher.py' script first to download the required data.")
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
    print(f"Scanning for optimal kappa across {num_steps} steps...")
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

def plot_results(data_1d, optimal_kappa, kappas, coherence_scores):
    """
    Visualizes the results of the analysis.
    """
    print(f"Optimal Chirality Factor (κ) found: {optimal_kappa:.6f}")
    
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("Pirouette Waveform Analysis of S&P 500 Data", fontsize=20)
    
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
    # --- PARAMETERS ---
    DATA_FILENAME = 'sp500_data_2007_2010.csv'
    KAPPA_RANGE = (0, 0.1)
    KAPPA_STEPS = 500
    
    # --- EXECUTION ---
    # 1. Load the local data
    market_data_1d = load_local_data(DATA_FILENAME)
    
    # 2. Analyze for hidden geometry
    opt_kappa, kappas, scores = find_optimal_kappa(market_data_1d, KAPPA_RANGE, KAPPA_STEPS)
    
    # 3. Visualize the claim
    plot_results(market_data_1d, opt_kappa, kappas, scores)
