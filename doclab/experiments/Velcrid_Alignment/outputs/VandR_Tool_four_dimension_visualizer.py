import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def create_pair_plot(df: pd.DataFrame, output_filename='4d_analysis_pair_plot.png'):
    """
    Generates a pair plot to visualize the relationships between all metrics,
    colored by category.
    """
    print("Generating pair plot... This may take a moment.")
    
    # Select the columns to be plotted
    plot_vars = [
        'velcridance_score',
        'radiance_score',
        'kurtosis_score',
        'drift_score',
        'anisotropy_score'
    ]
    
    # Set the style
    sns.set_style("whitegrid")
    
    # Create the pair plot
    # The 'hue' parameter automatically colors the points by the 'category' column
    g = sns.pairplot(
        df,
        vars=plot_vars,
        hue='category',
        palette={'radiant': 'gold', 'velcrid': 'darkblue'},
        plot_kws={'alpha': 0.7, 's': 60, 'edgecolor': 'w'}, # Style for scatter plots
        diag_kind='kde' # Use Kernel Density Estimate for diagonal plots
    )
    
    # Add a title for the entire plot
    g.fig.suptitle("Pair Plot of Stage 1 & 2 Semantic Metrics", y=1.02, fontsize=16)
    
    # Save the plot
    plt.savefig(output_filename, dpi=300) # Save with high resolution
    print(f"✅ Pair plot saved as '{output_filename}'")
    plt.show()


# --- Main Execution Block ---
if __name__ == '__main__':
    # Use the new results file you provided
    RESULTS_CSV = "vr_analysis_results_4d_2.csv" 

    if not os.path.exists(RESULTS_CSV):
        print(f"Error: Results file not found at '{RESULTS_CSV}'")
    else:
        print(f"Loading results from '{RESULTS_CSV}'...")
        df_raw = pd.read_csv(RESULTS_CSV)

        if not df_raw.empty:
            create_pair_plot(df_raw)
        else:
            print("The results file is empty. Cannot generate a plot.")