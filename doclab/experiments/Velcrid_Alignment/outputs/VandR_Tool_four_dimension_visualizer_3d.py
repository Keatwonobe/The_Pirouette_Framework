import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Necessary for 3D projection
import os

def create_3d_scatter_plot(df: pd.DataFrame, output_filename='3d_persona_plot.png'):
    """
    Generates a 3D scatter plot to visualize the text personas.
    """
    print("Generating 3D scatter plot...")

    # --- Prepare the figure and 3D axis ---
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    plt.style.use('seaborn-v0_8-whitegrid')

    # --- Define colors ---
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}
    
    # --- Plot each category separately to apply colors and labels ---
    for category_name, group in df.groupby('category'):
        ax.scatter(
            group['velcridance_score'],
            group['kurtosis_score'],
            group['drift_score'],
            s=80, # Size of the markers
            c=colors.get(category_name, 'gray'),
            label=category_name.capitalize(),
            edgecolor='w',
            alpha=0.8,
            depthshade=True
        )

    # --- Set labels and title ---
    ax.set_xlabel('Velcridance (μ)', fontsize=12, labelpad=10)
    ax.set_ylabel('Kurtosis (Kᵢ)', fontsize=12, labelpad=10)
    ax.set_zlabel('Drift (∂μ/∂flips)', fontsize=12, labelpad=10)
    ax.set_title('3D Pirouette Persona Analysis', fontsize=16, pad=20)
    ax.legend(title='Category', fontsize=12)

    # --- Save and show the plot ---
    plt.savefig(output_filename, dpi=300)
    print(f"✅ 3D scatter plot saved as '{output_filename}'")
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
            create_3d_scatter_plot(df_raw)
        else:
            print("The results file is empty. Cannot generate a plot.")