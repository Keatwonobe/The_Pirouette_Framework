import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull
import os

def create_convex_hull_plot(df: pd.DataFrame, output_filename='data_polyhedron.png'):
    """
    Computes the convex hull of the data points and visualizes it as a 3D polyhedron.
    """
    print("Generating 3D convex hull plot...")

    # --- 1. Prepare the data points for the hull calculation ---
    points = df[[
        'velcridance_score',
        'kurtosis_score',
        'drift_score'
    ]].values

    # --- 2. Compute the Convex Hull ---
    # The result contains the indices of the points that form the vertices of the hull's faces
    try:
        hull = ConvexHull(points)
    except Exception as e:
        print(f"Could not compute convex hull: {e}")
        print("This can happen if the data points are co-planar (all lie on a flat 2D plane).")
        return

    # --- 3. Create the 3D plot ---
    fig = plt.figure(figsize=(14, 11))
    ax = fig.add_subplot(111, projection='3d')
    plt.style.use('seaborn-v0_8-whitegrid')

    # --- 4. Plot the hull's triangular faces ---
    # `hull.simplices` is a list of the faces, where each face is a list of 3 vertex indices.
    ax.plot_trisurf(
        points[:, 0], points[:, 1], points[:, 2],
        triangles=hull.simplices,
        cmap='viridis',
        edgecolor='k',
        alpha=0.2,
        linewidth=0.5
    )

    # --- 5. Plot the data points as vertices ---
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=150, c=df['category'].map(colors),
               edgecolor='k', alpha=1.0, depthshade=True)

    # --- 6. Add labels to each vertex ---
    for i, row in df.iterrows():
        ax.text(row['velcridance_score'], row['kurtosis_score'], row['drift_score'],
                s=row['file'].split('.')[0][:12], # First 12 chars of filename
                color='black', fontsize=9, ha='center', va='bottom')

    # --- Set labels and title ---
    ax.set_xlabel('Velcridance (μ)', fontsize=12, labelpad=10)
    ax.set_ylabel('Kurtosis (Kᵢ)', fontsize=12, labelpad=10)
    ax.set_zlabel('Drift (E)', fontsize=12, labelpad=10)
    ax.set_title('Convex Hull of Semantic Personas', fontsize=16, pad=20)
    
    # Improve viewing angle
    ax.view_init(elev=20, azim=45)

    plt.savefig(output_filename, dpi=300)
    print(f"✅ Polyhedron plot saved as '{output_filename}'")
    plt.show()

# --- Main Execution Block ---
if __name__ == '__main__':
    RESULTS_CSV = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment/vr_analysis_results_from_tar.csv"

    if not os.path.exists(RESULTS_CSV):
        print(f"Error: Results file '{RESULTS_CSV}' not found.")
    else:
        df = pd.read_csv(RESULTS_CSV)
        if len(df) < 4:
            print("Error: Need at least 4 data points to form a 3D convex hull.")
        else:
            create_convex_hull_plot(df)