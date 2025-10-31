# INSTRUMENT: The Surveyor
# id: INST-WAVEFORM-SURVEYOR-002
# version: 2.0 (replaces 1.0)
# parents: [INST-WAVEFORM-ANALYZER-003, DOMA-206]
#
# ABSTRACT: This is a significant evolution of the Surveyor instrument. Instead
# of projecting a 1D signal (Price) and searching for an optimal kappa, this
# version constructs a true 3D path using Price and Volume over Time. It then
# directly calculates the intrinsic chirality of this path using the mathematical
# concept of Torsion from differential geometry. This provides a more fundamental
# and physically meaningful measure of an asset's dynamic signature, revealing
# the complex interplay between price movement and market energy.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse
import os
from tqdm import tqdm

def load_and_normalize_local_data(filename):
    """
    Loads Price and Volume data. Normalizes both to the [-1, 1] range.
    Returns a tuple (normalized_price, normalized_volume) or None on failure.
    """
    try:
        data = pd.read_csv(filename)
        if 'Close' not in data.columns or 'Volume' not in data.columns:
            return None
        
        price = pd.to_numeric(data['Close'].dropna())
        volume = pd.to_numeric(data['Volume'].dropna())
        
        # Align data by index
        common_index = price.index.intersection(volume.index)
        price = price.loc[common_index]
        volume = volume.loc[common_index]

        if len(price) < 100: # Need more points for stable derivatives
            return None

        # Normalize Price
        price_min, price_max = price.min(), price.max()
        if (price_max - price_min) == 0: return None
        norm_price = 2 * ((price - price_min) / (price_max - price_min)) - 1
        
        # Normalize Volume
        vol_min, vol_max = volume.min(), volume.max()
        if (vol_max - vol_min) == 0: return None
        norm_vol = 2 * ((volume - vol_min) / (vol_max - vol_min)) - 1
        
        return norm_price.values, norm_vol.values
    except Exception:
        return None

def calculate_intrinsic_kappa(price_data, volume_data):
    """
    Calculates the intrinsic kappa by measuring the mean torsion of the
    3D path defined by (price, volume, time).
    """
    # Construct the 3D path vector r(t)
    t = np.linspace(0, 1, len(price_data))
    r = np.vstack([price_data, volume_data, t]).T

    # Calculate first, second, and third derivatives using finite differences
    dr_dt = np.gradient(r, axis=0)
    d2r_dt2 = np.gradient(dr_dt, axis=0)
    d3r_dt3 = np.gradient(d2r_dt2, axis=0)

    # Calculate the cross products needed for the torsion formula
    cross_r_prime_r_double_prime = np.cross(dr_dt, d2r_dt2)
    
    # Numerator of the torsion formula: (r' x r'') . r'''
    numerator = np.einsum('ij,ij->i', cross_r_prime_r_double_prime, d3r_dt3)
    
    # Denominator: ||r' x r''||^2
    denominator = np.sum(cross_r_prime_r_double_prime**2, axis=1)

    # Avoid division by zero for straight-line segments
    torsion = np.zeros_like(denominator)
    valid_indices = denominator > 1e-9 # Epsilon to avoid floating point issues
    torsion[valid_indices] = numerator[valid_indices] / denominator[valid_indices]

    # Kappa is the mean of the absolute torsion, representing average "twistiness"
    intrinsic_kappa = np.mean(np.abs(torsion))
    
    # Scale the result for a more intuitive range
    return intrinsic_kappa * 100

def plot_kappa_distribution(results_df, output_dir):
    """
    Plots a histogram of the calculated intrinsic kappa values.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    kappas = results_df['intrinsic_kappa'].dropna()
    ax.hist(kappas, bins=50, color='deepskyblue', alpha=0.7, edgecolor='white')
    
    mean_kappa = kappas.mean()
    median_kappa = kappas.median()
    
    ax.axvline(mean_kappa, color='red', linestyle='--', linewidth=2, label=f'Mean κ = {mean_kappa:.4f}')
    ax.axvline(median_kappa, color='orange', linestyle=':', linewidth=2, label=f'Median κ = {median_kappa:.4f}')
    
    ax.set_title('Distribution of Intrinsic Chirality (κ) Across a Market', fontsize=16)
    ax.set_xlabel('Intrinsic Chirality Factor (κ) - (Torsion-based)', fontsize=12)
    ax.set_ylabel('Number of Assets', fontsize=12)
    ax.legend()
    
    plot_filename = os.path.join(output_dir, 'intrinsic_kappa_distribution.png')
    plt.savefig(plot_filename)
    print(f"\nDistribution plot saved to '{plot_filename}'")
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Batch Pirouette Analyzer (v2 - Torsion Method) for local directories.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("directory", help="The path to the input directory (e.g., 'Data/Stocks/').")
    parser.add_argument("--output_dir", default='.', help="Directory to save the results CSV and plot (default: current dir).")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found at '{args.directory}'")
        sys.exit(1)
        
    os.makedirs(args.output_dir, exist_ok=True)
    
    results = []
    file_paths = [os.path.join(root, file) for root, _, files in os.walk(args.directory) for file in files if file.endswith('.txt')]

    print(f"Found {len(file_paths)} .txt files. Starting intrinsic analysis...")
    
    for filepath in tqdm(file_paths, desc="Measuring Asset Torsion"):
        data = load_and_normalize_local_data(filepath)
        if data is not None:
            norm_price, norm_vol = data
            intrinsic_kappa = calculate_intrinsic_kappa(norm_price, norm_vol)
            results.append({'asset': os.path.basename(filepath), 'intrinsic_kappa': intrinsic_kappa})

    if not results:
        print("No valid data files could be processed.")
        sys.exit(0)

    results_df = pd.DataFrame(results)
    output_csv = os.path.join(args.output_dir, 'intrinsic_kappa_results.csv')
    results_df.to_csv(output_csv, index=False)
    print(f"\nAnalysis complete. Results for {len(results_df)} assets saved to '{output_csv}'")
    
    plot_kappa_distribution(results_df, args.output_dir)

