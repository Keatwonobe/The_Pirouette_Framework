import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import os

# --- Analysis & Visualization Functions (from your original script) ---

def run_final_analysis(df: pd.DataFrame):
    """Performs and prints statistical analysis on the results."""
    print("\n" + "="*60 + "\nSTATISTICAL ANALYSIS\n" + "="*60)

    # Ensure columns are numeric for correlation
    df['velcridance_score'] = pd.to_numeric(df['velcridance_score'])
    df['radiance_score'] = pd.to_numeric(df['radiance_score'])
    df['text_length'] = pd.to_numeric(df['text_length'])

    print("\n--- Pearson Correlation Matrix ---\n")
    print(df[['velcridance_score', 'radiance_score', 'text_length']].corr())

    print("\n--- ANOVA: Does 'category' explain score variance? ---")
    try:
        # Velcridance Score
        model_v = ols('velcridance_score ~ C(category)', data=df).fit()
        print(f"\n[Velcridance (mean ΔE)]")
        print(f"  - F-statistic: {model_v.fvalue:.4f}")
        print(f"  - p-value: {model_v.f_pvalue:.4f} {'(Significant!)' if model_v.f_pvalue < 0.05 else ''}")

        # Radiance Score
        model_r = ols('radiance_score ~ C(category)', data=df).fit()
        print(f"\n[Radiance (std ΔE)]")
        print(f"  - F-statistic: {model_r.fvalue:.4f}")
        print(f"  - p-value: {model_r.f_pvalue:.4f} {'(Significant!)' if model_r.f_pvalue < 0.05 else ''}")

    except Exception as e:
        print(f"Could not run ANOVA: {e}")
    print("\n" + "="*60 + "\n")

def plot_results(df: pd.DataFrame, output_filename='vr_analysis_plot.png'):
    """Generates and saves a scatter plot of the normalized results."""
    plt.style.use('seaborn-v0_8-whitegrid')

    # Calculate Z-scores for normalization
    df['velcridance_z'] = (df['velcridance_score'] - df['velcridance_score'].mean()) / df['velcridance_score'].std()
    df['radiance_z'] = (df['radiance_score'] - df['radiance_score'].mean()) / df['radiance_score'].std()

    fig, ax = plt.subplots(figsize=(12, 10))
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}

    for category, group in df.groupby('category'):
        ax.scatter(group['velcridance_z'], group['radiance_z'], s=120, alpha=0.8,
                   ec='w', c=colors.get(category, 'gray'), label=category.capitalize())

    # Annotate points with file names
    for i, row in df.iterrows():
        ax.text(row['velcridance_z'] + 0.05, row['radiance_z'],
                row['file'].split('.')[0][:20], fontsize=9, alpha=0.7) # Show first 20 chars of filename

    ax.set_title('Normalized Velcridance vs. Radiance by Category', fontsize=16, pad=20)
    ax.set_xlabel('Normalized Velcridance Score (Z-score)', fontsize=12)
    ax.set_ylabel('Normalized Radiance Score (Z-score)', fontsize=12)
    ax.axhline(0, color='grey', linestyle='--', lw=1)
    ax.axvline(0, color='grey', linestyle='--', lw=1)
    ax.legend(title='Category', fontsize=12)
    ax.grid(True)

    plt.savefig(output_filename)
    print(f"✅ Results plot saved as '{output_filename}'")
    plt.show()


# --- Main Execution Block ---
if __name__ == '__main__':
    RESULTS_CSV = "vr_analysis_results_v4.csv"

    if not os.path.exists(RESULTS_CSV):
        print(f"Error: Results file not found at '{RESULTS_CSV}'")
        print("Please ensure the script is in the same directory as your results.")
    else:
        print(f"Loading results from '{RESULTS_CSV}'...")
        df_raw = pd.read_csv(RESULTS_CSV)

        # Filter out any example files if they exist
        df_filtered = df_raw[~df_raw['file'].str.contains("example", case=False, na=False)]

        if not df_filtered.empty:
            # Run the statistical analysis
            run_final_analysis(df_filtered)
            # Generate and display the plot
            plot_results(df_filtered)
        else:
            print("No data left after filtering. Cannot generate analysis or plots.")