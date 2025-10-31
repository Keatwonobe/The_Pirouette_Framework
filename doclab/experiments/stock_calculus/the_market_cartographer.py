# INSTRUMENT: The Market Cartographer
# id: INST-WAVEFORM-CARTOGRAPHER-001
# version: 1.0
# parents: [INST-WAVEFORM-SURVEYOR-002]
#
# ABSTRACT: This instrument creates a "phase-space" map of a market by plotting
# each asset's intrinsic dynamic character (kappa) against its long-term
# performance. This 2D visualization intrinsically separates assets into four
# distinct archetypes: Weavers (constructive, stable growth), Gladiators (high-
# risk, high-return), Drifters (stagnant), and Vortices (parasitic, value-
# destructive). It provides a powerful diagnostic tool for assessing the health
# and identifying the role of any asset within the market ecosystem.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse
import os
from tqdm import tqdm

def load_and_process_data(filename):
    """
    Loads Price and Volume, normalizes them, and returns both the
    normalized data for kappa calculation and raw price for performance.
    """
    try:
        data = pd.read_csv(filename)
        if 'Close' not in data.columns or 'Volume' not in data.columns:
            return None
        
        price = pd.to_numeric(data['Close'].dropna())
        volume = pd.to_numeric(data['Volume'].dropna())
        common_index = price.index.intersection(volume.index)
        price = price.loc[common_index]
        volume = volume.loc[common_index]

        if len(price) < 100: return None

        # --- Normalization for Kappa Calculation ---
        price_min, price_max = price.min(), price.max()
        if (price_max - price_min) == 0: return None
        norm_price = 2 * ((price - price_min) / (price_max - price_min)) - 1
        
        vol_min, vol_max = volume.min(), volume.max()
        if (vol_max - vol_min) == 0: return None
        norm_vol = 2 * ((volume - vol_min) / (vol_max - vol_min)) - 1
        
        return norm_price.values, norm_vol.values, price.values
    except Exception:
        return None

def calculate_intrinsic_kappa(price_data, volume_data):
    """Calculates the intrinsic kappa (mean torsion) of the 3D path."""
    t = np.linspace(0, 1, len(price_data))
    r = np.vstack([price_data, volume_data, t]).T
    dr_dt = np.gradient(r, axis=0)
    d2r_dt2 = np.gradient(dr_dt, axis=0)
    d3r_dt3 = np.gradient(d2r_dt2, axis=0)
    cross_r_prime_r_double_prime = np.cross(dr_dt, d2r_dt2)
    numerator = np.einsum('ij,ij->i', cross_r_prime_r_double_prime, d3r_dt3)
    denominator = np.sum(cross_r_prime_r_double_prime**2, axis=1)
    torsion = np.zeros_like(denominator)
    valid_indices = denominator > 1e-9
    torsion[valid_indices] = numerator[valid_indices] / denominator[valid_indices]
    return np.mean(np.abs(torsion)) * 100

def calculate_performance_score(raw_price):
    """Calculates the log return over the entire period."""
    if raw_price[0] <= 0 or raw_price[-1] <= 0:
        return 0.0
    return np.log(raw_price[-1] / raw_price[0])

def plot_phase_space_map(results_df, output_dir):
    """Plots the 2D scatter plot of kappa vs. performance."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(15, 12))

    kappa = results_df['intrinsic_kappa']
    performance = results_df['performance_score']
    
    # Define quadrant boundaries
    median_kappa = kappa.median()
    
    # Assign assets to quadrants
    is_weaver = (kappa < median_kappa) & (performance > 0)
    is_vortex = (kappa > median_kappa) & (performance < 0)
    is_gladiator = (kappa > median_kappa) & (performance > 0)
    is_drifter = (kappa < median_kappa) & (performance < 0)

    # Plot each quadrant with a different color
    ax.scatter(kappa[is_weaver], performance[is_weaver], color='blue', alpha=0.6, label='Weavers (Constructive)')
    ax.scatter(kappa[is_vortex], performance[is_vortex], color='red', alpha=0.6, label='Vortices (Parasitic)')
    ax.scatter(kappa[is_gladiator], performance[is_gladiator], color='purple', alpha=0.6, label='Gladiators (High-Beta)')
    ax.scatter(kappa[is_drifter], performance[is_drifter], color='gray', alpha=0.6, label='Drifters (Stagnant)')

    # Draw quadrant lines and add labels
    ax.axvline(median_kappa, color='black', linestyle='--', alpha=0.5)
    ax.axhline(0, color='black', linestyle='--', alpha=0.5)

    ax.set_title('Market Phase-Space Map', fontsize=20, pad=20)
    ax.set_xlabel('Intrinsic Chirality (κ) → Complexity/Stress', fontsize=14)
    ax.set_ylabel('Performance Score (Log Return) → Value Creation', fontsize=14)
    
    # Annotate quadrants
    ax.text(kappa.min(), performance.max(), 'I. The Weavers\n(Low κ, High Perf)', ha='left', va='top', fontsize=12, color='blue', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    ax.text(kappa.max(), performance.max(), 'II. The Gladiators\n(High κ, High Perf)', ha='right', va='top', fontsize=12, color='purple', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    ax.text(kappa.min(), performance.min(), 'III. The Drifters\n(Low κ, Low Perf)', ha='left', va='bottom', fontsize=12, color='gray', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    ax.text(kappa.max(), performance.min(), 'IV. The Vortices\n(High κ, Low Perf)', ha='right', va='bottom', fontsize=12, color='red', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax.legend()
    plot_filename = os.path.join(output_dir, 'market_phase_space.png')
    plt.savefig(plot_filename)
    print(f"\nMarket Phase-Space Map saved to '{plot_filename}'")
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Market Phase-Space Cartographer.")
    parser.add_argument("directory", help="The path to the input directory.")
    parser.add_argument("--output_dir", default='.', help="Directory to save the results.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    
    results = []
    file_paths = [os.path.join(root, file) for root, _, files in os.walk(args.directory) for file in files if file.endswith('.txt')]

    print(f"Found {len(file_paths)} files. Mapping the market phase-space...")
    
    for filepath in tqdm(file_paths, desc="Mapping Asset Archetypes"):
        data = load_and_process_data(filepath)
        if data is not None:
            norm_price, norm_vol, raw_price = data
            intrinsic_kappa = calculate_intrinsic_kappa(norm_price, norm_vol)
            performance_score = calculate_performance_score(raw_price)
            results.append({
                'asset': os.path.basename(filepath),
                'intrinsic_kappa': intrinsic_kappa,
                'performance_score': performance_score
            })

    if not results:
        print("No valid data files could be processed.")
        sys.exit(0)

    results_df = pd.DataFrame(results)
    output_csv = os.path.join(args.output_dir, 'market_archetypes.csv')
    results_df.to_csv(output_csv, index=False)
    print(f"\nAnalysis complete. Results for {len(results_df)} assets saved to '{output_csv}'")
    
    plot_phase_space_map(results_df, args.output_dir)
