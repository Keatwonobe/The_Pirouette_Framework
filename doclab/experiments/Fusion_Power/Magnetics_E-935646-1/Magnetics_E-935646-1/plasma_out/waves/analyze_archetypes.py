import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import argparse
import sys

def analyze_archetypes(data_directory: Path):
    """
    Scans a directory for *_archetypes.csv files, compiles them,
    and generates a summary report and visualizations.
    """
    print(f"--- Starting Analysis in: {data_directory} ---")

    # 1. Discover and load all archetype files
    # =================================================================
    archetype_files = list(data_directory.glob('*_archetypes.csv'))
    if not archetype_files:
        print(f"Error: No '*_archetypes.csv' files found in '{data_directory}'.", file=sys.stderr)
        print("Please run this script in the directory containing your result files.", file=sys.stderr)
        return

    print(f"Found {len(archetype_files)} archetype files. Loading...")
    df_list = [pd.read_csv(f) for f in archetype_files]
    full_df = pd.concat(df_list, ignore_index=True)
    print("All files loaded and combined into a single dataset.")
    print(f"Total records found: {len(full_df)}")

    # Create an output directory for results
    output_dir = data_directory / "analysis_results"
    output_dir.mkdir(exist_ok=True)
    print(f"Results will be saved in: {output_dir}")

    # 2. Perform Statistical Analysis and Save to Text File
    # =================================================================
    summary_path = output_dir / "analysis_summary.txt"
    with open(summary_path, 'w') as f:
        f.write("--- Archetype Analysis Summary ---\n\n")

        # Overall distribution
        f.write("1. Overall Archetype Distribution (Counts and Percentages)\n")
        f.write("----------------------------------------------------------\n")
        counts = full_df['archetype'].value_counts()
        percentages = full_df['archetype'].value_counts(normalize=True) * 100
        dist_df = pd.DataFrame({'Count': counts, 'Percentage': percentages.round(2)})
        f.write(dist_df.to_string())
        f.write("\n\n")

        # Distribution by frequency band
        f.write("2. Archetype Distribution by Frequency Band\n")
        f.write("-------------------------------------------\n")
        band_crosstab = pd.crosstab(full_df['band'], full_df['archetype'])
        f.write(band_crosstab.to_string())
        f.write("\n\n")

        # Distribution by series (experimental run)
        f.write("3. Archetype Distribution by Series (Experimental Run)\n")
        f.write("------------------------------------------------------\n")
        series_crosstab = pd.crosstab(full_df['series'], full_df['archetype'])
        f.write(series_crosstab.to_string())
        f.write("\n\n")

        # Feature analysis by archetype
        f.write("4. Feature Statistics by Archetype\n")
        f.write("------------------------------------\n")
        feature_stats = full_df.groupby('archetype')[['kappa_abs', 'power', 'delta_power']].describe()
        f.write(feature_stats.to_string())
        f.write("\n")

    print(f"Statistical summary saved to {summary_path}")

    # 3. Generate and Save Visualizations
    # =================================================================
    sns.set_theme(style="whitegrid")

    # Plot 1: Overall distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(y=full_df['archetype'], order=full_df['archetype'].value_counts().index, palette='viridis')
    plt.title('Overall Archetype Distribution')
    plt.xlabel('Count')
    plt.ylabel('Archetype')
    plt.tight_layout()
    plt.savefig(output_dir / "1_overall_distribution.png")
    print("Saved plot: 1_overall_distribution.png")

    # Plot 2: Distribution by frequency band
    band_crosstab.plot(kind='bar', stacked=True, figsize=(12, 7), colormap='plasma')
    plt.title('Archetype Distribution by Frequency Band')
    plt.xlabel('Frequency Band')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.legend(title='Archetype')
    plt.tight_layout()
    plt.savefig(output_dir / "2_distribution_by_band.png")
    print("Saved plot: 2_distribution_by_band.png")

    # Plot 3: Boxplots for feature analysis (Absolute Kappa)
    plt.figure(figsize=(12, 7))
    sns.boxplot(x='archetype', y='kappa_abs', data=full_df, palette='muted', order=counts.index)
    plt.title('Distribution of Absolute Kappa by Archetype')
    plt.xlabel('Archetype')
    plt.ylabel('Absolute Kappa')
    plt.yscale('log')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "3_kappa_abs_by_archetype.png")
    print("Saved plot: 3_kappa_abs_by_archetype.png")
    
    # Plot 4: Boxplots for feature analysis (Delta Power)
    plt.figure(figsize=(12, 7))
    sns.boxplot(x='archetype', y='delta_power', data=full_df, palette='muted', showfliers=False, order=counts.index)
    plt.title('Distribution of Delta Power by Archetype (Outliers Hidden)')
    plt.xlabel('Archetype')
    plt.ylabel('Delta Power (Relative to Baseline)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "4_delta_power_by_archetype.png")
    print("Saved plot: 4_delta_power_by_archetype.png")

    # Plot 5: Scatter plot to see feature relationships
    plt.figure(figsize=(12, 8))
    # Using a subset of data for a cleaner plot, as plotting all points can be slow and messy
    plot_sample = full_df.sample(n=min(5000, len(full_df)), random_state=1)
    sns.scatterplot(data=plot_sample, x='kappa_abs', y='delta_power', hue='archetype', palette='bright', alpha=0.7, s=50)
    plt.title('Kappa vs. Delta Power for different Archetypes')
    plt.xlabel('Absolute Kappa')
    plt.ylabel('Delta Power')
    plt.xscale('log')
    plt.legend(title='Archetype', bbox_to_anchor=(1.05, 1), loc=2)
    plt.tight_layout()
    plt.savefig(output_dir / "5_kappa_vs_delta_power.png")
    print("Saved plot: 5_kappa_vs_delta_power.png")

    plt.close('all')
    print("--- Analysis Complete ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Analyze and compile archetype classification results from CSV files."
    )
    parser.add_argument(
        '--dir',
        type=str,
        default='.',
        help="The directory containing the '*_archetypes.csv' files. Defaults to the current directory."
    )
    args = parser.parse_args()
    
    data_dir = Path(args.dir)
    if not data_dir.is_dir():
        print(f"Error: Directory not found at '{data_dir}'", file=sys.stderr)
        sys.exit(1)
        
    analyze_archetypes(data_dir)