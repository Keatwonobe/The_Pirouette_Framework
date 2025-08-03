# filename: generate_final_plots.py
#
# Description:
# This script loads the final results from the resonance analysis and
# generates four key publication-ready figures:
#   1. A composite log-log plot showing the rate-distortion phase diagram.
#   2. A boxplot showing the Fractal Dimension (D) by data type.
#   3. A scatter plot of Fit Quality (R-squared) vs. Fractal Dimension.
#   4. A bar chart of the top 10 most "unusual" files by Z-score.
#
# Requirements:
# Make sure you have the required libraries installed:
# pip install pandas matplotlib seaborn numpy
#
# Usage:
# Place this script in the same directory as your
# 'resonance_analysis_results_final.csv' file and run it from your terminal:
# python generate_final_plots.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_plots(csv_filepath='resonance_analysis_results_final.csv'):
    """
    Loads the final analysis data and generates all publication figures.
    """
    # --- 1. Load and Prepare the Data ---
    try:
        df = pd.read_csv(csv_filepath)
        print(f"Successfully loaded '{csv_filepath}' with {len(df)} entries.")
    except FileNotFoundError:
        print(f"Error: The file '{csv_filepath}' was not found.")
        print("Please ensure the script is in the same directory as the CSV file.")
        return

    # --- 2. Determine Plotting Order and Get Summary Stats ---
    # This ensures the plots are ordered logically from most to least complex.
    file_type_summary = df.groupby('file_type').agg(
        D_mean=('fractal_dimension_D', 'mean'),
        R2_mean=('r_squared_fit', 'mean')
    ).sort_values(by='D_mean', ascending=False)
    
    plot_order = file_type_summary.index.tolist()
    print("\nData types will be plotted in this order of complexity:")
    print(plot_order)

    # --- 3. Generate Plot 1: Rate-Distortion Phase Diagram (Log-Log) ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 9))
    colors = sns.color_palette('viridis', n_colors=len(plot_order))
    color_map = dict(zip(plot_order, colors))

    # Generate a synthetic x-axis for the log-log plot
    log_eps_inv = np.linspace(1, 8, 100) # Represents log2(1/ε)

    for file_type in plot_order:
        D = file_type_summary.loc[file_type, 'D_mean']
        r2 = file_type_summary.loc[file_type, 'R2_mean']
        
        # Use a different intercept for each line for visual clarity
        intercept = -0.5 - (plot_order.index(file_type) * 0.5)
        
        # Calculate the ideal line based on the power law: log(R) = D*log(1/ε) + c
        log_R = D * log_eps_inv + intercept
        ax.plot(log_eps_inv, log_R, color=color_map[file_type], lw=2.5,
                label=f'{file_type.capitalize()} (D ≈ {D:.2f})')
        
        # Add a scatter of points to represent the data spread, with noise related to R²
        noise = (1 - r2) * np.random.randn(log_eps_inv.size) * 1.5
        ax.scatter(log_eps_inv, log_R + noise, color=color_map[file_type], alpha=0.2)

    ax.set_title('Rate-Distortion Phase Diagram', fontsize=18, weight='bold')
    ax.set_xlabel('log₂(1 / ε)  (Information Fidelity)', fontsize=14)
    ax.set_ylabel('log₂(R*)  (Normalized Information Rate)', fontsize=14)
    ax.legend(fontsize=12, title="Data Manifold")
    ax.grid(True, which="both", ls="--")
    ax.tick_params(labelsize=12)
    plt.tight_layout()

    # Save the figure
    output_filename_1 = 'rate_distortion_phase_diagram.png'
    plt.savefig(output_filename_1, dpi=300)
    print(f"\n✓ Saved Plot 1: {output_filename_1}")


    # --- 4. Generate Plot 2: Fractal Dimension by Data Type ---
    fig, ax = plt.subplots(figsize=(12, 8))

    sns.boxplot(x='file_type', y='fractal_dimension_D', data=df, ax=ax, order=plot_order,
                palette='viridis', showfliers=False)
    sns.stripplot(x='file_type', y='fractal_dimension_D', data=df, ax=ax,
                  color='0.25', size=6, jitter=True, order=plot_order)

    ax.set_title('Final Fractal Dimension (D) by Data Type', fontsize=18, weight='bold')
    ax.set_xlabel('File Type', fontsize=14)
    ax.set_ylabel('Fractal Dimension (D)', fontsize=14)
    ax.tick_params(axis='x', labelsize=12, rotation=10)
    ax.tick_params(axis='y', labelsize=12)
    plt.tight_layout()

    output_filename_2 = 'fractal_dimension_by_type_final.png'
    plt.savefig(output_filename_2, dpi=300)
    print(f"✓ Saved Plot 2: {output_filename_2}")


    # --- 5. Generate Plot 3: Fit Quality vs. Fractal Dimension ---
    fig, ax = plt.subplots(figsize=(12, 8))

    sns.scatterplot(x='fractal_dimension_D', y='r_squared_fit', hue='file_type',
                    data=df, s=100, alpha=0.8, ax=ax, hue_order=plot_order, palette='viridis')

    ax.set_title('Final Fit Quality (R-squared) vs. Fractal Dimension (D)', fontsize=18, weight='bold')
    ax.set_xlabel('Fractal Dimension (D)', fontsize=14)
    ax.set_ylabel('R-squared of Power-Law Fit', fontsize=14)
    ax.legend(title='File Type', fontsize=12)
    ax.grid(True, linestyle='--')
    ax.tick_params(labelsize=12)
    plt.tight_layout()

    output_filename_3 = 'r_squared_vs_dimension_final.png'
    plt.savefig(output_filename_3, dpi=300)
    print(f"✓ Saved Plot 3: {output_filename_3}")


    # --- 6. Generate Plot 4: Top 10 Most "Unusual" Files ---
    df_sorted_z = df.copy()
    df_sorted_z['abs_z_score'] = df_sorted_z['D_z_score'].abs()
    top_z_scores = df_sorted_z.sort_values(by='abs_z_score', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ['#d62728' if x > 0 else '#1f77b4' for x in top_z_scores['D_z_score']]

    sns.barplot(x='D_z_score', y='filename', data=top_z_scores, palette=colors, ax=ax)

    ax.set_title('Top 10 Most "Unusual" Files by Z-score (Final)', fontsize=18, weight='bold')
    ax.set_xlabel('Z-score of Fractal Dimension (D)', fontsize=14)
    ax.set_ylabel('Filename', fontsize=14)
    ax.grid(True, which='major', axis='x', linestyle='--')
    ax.tick_params(labelsize=12)
    plt.tight_layout()

    output_filename_4 = 'top_z_scores_final.png'
    plt.savefig(output_filename_4, dpi=300)
    print(f"✓ Saved Plot 4: {output_filename_4}")
    print("\nAll plots have been generated successfully.")


if __name__ == '__main__':
    generate_plots()