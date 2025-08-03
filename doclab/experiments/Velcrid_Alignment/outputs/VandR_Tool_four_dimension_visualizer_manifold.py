import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os

def create_depth_map(df: pd.DataFrame, output_filename='manifold_depth_map.png'):
    """
    Generates a 2D depth map (contour plot) of the 3D data manifold.
    X-axis: Velcridance, Y-axis: Kurtosis, Color: Drift
    """
    print("Generating depth map of the semantic manifold...")

    # --- Prepare data points ---
    x = df['velcridance_score']
    y = df['kurtosis_score']
    z = df['drift_score']

    # --- Create a regular grid to interpolate data onto ---
    xi = np.linspace(x.min(), x.max(), 100)
    yi = np.linspace(y.min(), y.max(), 100)
    X, Y = np.meshgrid(xi, yi)

    # --- Interpolate the Z values (Drift) onto the grid ---
    # This creates the smooth surface from the scattered data points
    Z = griddata((x, y), z, (X, Y), method='cubic')

    # --- Create the plot ---
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.style.use('seaborn-v0_8-whitegrid')

    # --- Plot the filled contour (the depth map) ---
    contour = ax.contourf(X, Y, Z, levels=15, cmap='viridis', alpha=0.8)

    # --- Add contour lines for clarity ---
    ax.contour(X, Y, Z, levels=15, colors='white', linewidths=0.5, alpha=0.5)

    # --- Overlay the original data points ---
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}
    for category_name, group in df.groupby('category'):
        ax.scatter(group['velcridance_score'], group['kurtosis_score'], s=100,
                   c=colors.get(category_name, 'gray'), label=category_name.capitalize(),
                   edgecolor='k', alpha=1.0)

    # --- Set labels, title, and color bar ---
    ax.set_xlabel('Velcridance (μ) → Rigidity', fontsize=12)
    ax.set_ylabel('Kurtosis (Kᵢ) → Brittleness', fontsize=12)
    ax.set_title('Depth Map of the Semantic Manifold', fontsize=16, pad=20)
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label('Drift (∂μ/∂flips) → Stability', fontsize=12)
    ax.legend(title='Category', fontsize=12)
    ax.grid(True)

    plt.savefig(output_filename, dpi=300)
    print(f"✅ Depth map saved as '{output_filename}'")
    plt.show()

# --- Main Execution Block ---
if __name__ == '__main__':
    RESULTS_CSV = "vr_analysis_results_4d_2.csv"

    if not os.path.exists(RESULTS_CSV):
        print(f"Error: Results file not found at '{RESULTS_CSV}'")
    else:
        print(f"Loading results from '{RESULTS_CSV}'...")
        df_raw = pd.read_csv(RESULTS_CSV)

        if not df_raw.empty:
            create_depth_map(df_raw)
        else:
            print("The results file is empty. Cannot generate a plot.")