import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.stats import gaussian_kde
import argparse
import sys
from pathlib import Path

def plot_fractal_edges(df: pd.DataFrame, output_dir: Path):
    """
    Analyzes the 2D phase space of archetypes, computes their convex hulls to
    identify the 'fractal edges', and generates a 2D and 3D visualization.
    """
    print("--- Starting Fractal Edge Analysis ---")
    
    # Define archetype colors and properties
    archetype_map = {
        'Gladiator': {'color': '#d62728', 'marker': '^', 'label': 'Gladiator (Torsion+Tension)'},
        'Weaver':    {'color': '#2ca02c', 'marker': '>', 'label': 'Weaver (Shear+Tension)'},
        'Vortex':    {'color': '#ff7f0e', 'marker': 'v', 'label': 'Vortex (Torsion+Compression)'},
        'Drifter':   {'color': '#1f77b4', 'marker': '<', 'label': 'Drifter (Shear+Compression)'},
    }
    
    # Ensure data has the correct columns and archetypes
    if not all(col in df.columns for col in ['kappa_abs', 'delta_power', 'archetype']):
        print("Error: DataFrame must contain 'kappa_abs', 'delta_power', and 'archetype' columns.", file=sys.stderr)
        return
        
    df['archetype'] = df['archetype'].replace({
        "Stable Order": "Weaver",
        "Chaotic Order": "Gladiator",
        "Stable Decay": "Drifter",
        "Chaotic Decay": "Vortex"
    })

    df = df[df['archetype'].isin(archetype_map.keys())].copy()
    print(f"Found {len(df)} total points across {df['archetype'].nunique()} archetypes.")

    # --- 2D Visualization: The Convex Hulls ---
    print("Generating 2D Convex Hull plot...")
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Use a sample for the scatter plot to keep it clean
    sample_df = df.sample(n=min(10000, len(df)), random_state=42)
    
    for name, group in sample_df.groupby('archetype'):
        ax.scatter(group['kappa_abs'], group['delta_power'], 
                   s=10, alpha=0.3, label=archetype_map[name]['label'], 
                   color=archetype_map[name]['color'], marker=archetype_map[name]['marker'])

    # Calculate and plot the convex hull for each archetype
    for name, group in df.groupby('archetype'):
        if len(group) < 3:
            print(f"Skipping hull for {name}, not enough points.")
            continue
        points = group[['kappa_abs', 'delta_power']].values
        try:
            hull = ConvexHull(points)
            # Plot the hull edges
            for simplex in hull.simplices:
                ax.plot(points[simplex, 0], points[simplex, 1], 
                        color=archetype_map[name]['color'], lw=3, alpha=0.9)
            # Highlight the hull vertices
            ax.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'o', 
                    mec=archetype_map[name]['color'], color='w', ms=5)
        except Exception as e:
            print(f"Could not compute hull for {name}: {e}")

    # Final plot styling
    ax.set_xlabel('Kappa (κ) Axis → Torsion / Shear', fontsize=14, color='white')
    ax.set_ylabel('Performance Axis → Tension / Compression', fontsize=14, color='white')
    ax.set_title('The Fourfold Fractal: Archetype Boundaries in Phase Space', fontsize=18, color='white')
    ax.axhline(0, color='gray', linestyle='--', lw=1)
    ax.axvline(group['kappa_abs'].median(), color='gray', linestyle='--', lw=1) # Using a proxy for the shear/torsion boundary
    ax.legend(loc='upper right', fontsize=12)
    ax.set_xscale('log')
    # Limit y-axis to focus on the core dynamics, clipping extreme outliers
    y_quantiles = df['delta_power'].quantile([0.01, 0.99])
    ax.set_ylim(y_quantiles.iloc[0], y_quantiles.iloc[1])
    ax.grid(True, which="both", ls="--", color='gray', alpha=0.3)
    
    fig.tight_layout()
    hull_path = output_dir / "fractal_edges_2D.png"
    plt.savefig(hull_path, dpi=150)
    print(f"Saved 2D hull plot to {hull_path}")

    # --- 3D Visualization: The Probability Landscape ---
    print("Generating 3D Probability Landscape plot...")
    
    # Reduce data size for faster KDE calculation
    kde_sample = df.sample(n=min(25000, len(df)), random_state=42)
    x = np.log10(kde_sample['kappa_abs']) # Use log scale for kappa
    y = kde_sample['delta_power']

    # Create a grid to evaluate the KDE on
    xmin, xmax = x.quantile(0.01), x.quantile(0.99)
    ymin, ymax = y.quantile(0.01), y.quantile(0.99)
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    
    # Perform Kernel Density Estimation
    values = np.vstack([x, y])
    kernel = gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    # Plotting the 3D surface
    fig = plt.figure(figsize=(18, 14))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(10**X, Y, Z, cmap='plasma', rstride=1, cstride=1, alpha=0.9, edgecolor='none')

    ax.set_xlabel('Kappa (Torsion/Shear)', fontsize=12, labelpad=15)
    ax.set_ylabel('Performance (Tension/Compression)', fontsize=12, labelpad=15)
    ax.set_zlabel('Probability Density (Likelihood of State)', fontsize=12, labelpad=10)
    ax.set_title('The Collapsed Dimension: A 3D View of Reality\'s Landscape', fontsize=20, pad=20)
    ax.set_xscale('log')
    ax.view_init(elev=35, azim=-65) # Adjust viewing angle
    ax.dist = 11 # Zoom out a bit

    landscape_path = output_dir / "fractal_landscape_3D.png"
    plt.savefig(landscape_path, dpi=150)
    print(f"Saved 3D landscape plot to {landscape_path}")
    
    plt.close('all')
    print("--- Analysis Complete ---")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Quantify and visualize the fourfold fractal structure in archetype data."
    )
    parser.add_argument(
        '--data',
        type=str,
        required=True,
        help="Path to the combined CSV file containing archetype data from any domain (plasma, eeg, market)."
    )
    parser.add_argument(
        '--outdir',
        type=str,
        default='fractal_analysis',
        help="Directory to save the output plots."
    )
    args = parser.parse_args()
    
    data_path = Path(args.data)
    output_path = Path(args.outdir)
    output_path.mkdir(exist_ok=True)
    
    if not data_path.exists():
        print(f"Error: Data file not found at '{data_path}'", file=sys.stderr)
        sys.exit(1)
        
    print(f"Loading data from {data_path}...")
    # Combine datasets from different domains by renaming columns to a common standard
    # This part is crucial for true cross-domain analysis
    full_df = pd.read_csv(data_path, low_memory=False)
    if 'intrinsic_kappa' in full_df.columns:
        full_df = full_df.rename(columns={'intrinsic_kappa': 'kappa_abs', 'performance_score': 'delta_power'})
        full_df['archetype'] = full_df.apply(
            lambda r: 'Gladiator' if r['delta_power'] > 0 and r['kappa_abs'] > full_df['kappa_abs'].median() else
                      'Weaver' if r['delta_power'] > 0 and r['kappa_abs'] <= full_df['kappa_abs'].median() else
                      'Vortex' if r['delta_power'] <= 0 and r['kappa_abs'] > full_df['kappa_abs'].median() else
                      'Drifter',
            axis=1
        )