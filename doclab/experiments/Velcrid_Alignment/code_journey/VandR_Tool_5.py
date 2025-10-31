import os
import re
import csv
import json
import shutil
import argparse
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from bs4 import BeautifulSoup
import statsmodels.api as sm
from statsmodels.formula.api import ols

# --- Configuration & Suppressions ---
warnings.filterwarnings("ignore", category=FutureWarning)
plt.style.use('seaborn-v0_8-whitegrid')

# --- Core Simulation Engine (Upgraded) ---
class SemanticDistillator:
    """
    The core simulation engine. Upgraded to accept a configurable perturbation amplitude.
    """
    def __init__(self, grid_size=64, num_frames=200, noise_level=0.05, perturbation_amplitude=0.01, seed=0):
        self.grid_size = grid_size
        self.num_frames = num_frames
        self.perturbation_amplitude = perturbation_amplitude
        np.random.seed(seed)
        self.base_static_field = np.random.rand(self.grid_size, self.grid_size) * noise_level
        self.evolution_kernel = np.ones((3, 3)) / 9.0

    def text_to_binary_image(self, text):
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
        target_size = self.grid_size * self.grid_size
        if len(binary_array) > target_size:
            binary_array = binary_array[:target_size]
        else:
            padding = np.zeros(target_size - len(binary_array))
            binary_array = np.concatenate([binary_array, padding])
        return binary_array.reshape((self.grid_size, self.grid_size))

    def run_simulation(self, initial_pattern):
        grid = self.base_static_field + initial_pattern * self.perturbation_amplitude
        total_power = 0
        for _ in range(self.num_frames):
            grid = convolve(grid, self.evolution_kernel, mode='wrap')
            total_power += np.sum(grid**2)
        return total_power / (self.num_frames * self.grid_size * self.grid_size)

# --- V2 Scorer Module (New) ---
class PirouetteScorerV2:
    """
    A flexible scorer that calculates Radiance and Velcridance using configurable metrics.
    """
    def __init__(self, flips=256, amplitude=0.1, metric='mean', seed=42):
        self.flips = flips
        self.metric = metric
        self.rng = np.random.default_rng(seed)
        self.engine = SemanticDistillator(perturbation_amplitude=amplitude, seed=seed)
        print(f"Scorer V2 initialized with: {flips=}, {amplitude=}, {metric=}")

    def get_delta_distribution(self, text: str) -> np.ndarray:
        """Calculates the distribution of energy changes from random bit flips."""
        base_pattern = self.engine.text_to_binary_image(text)
        base_power = self.engine.run_simulation(base_pattern)
        
        bit_indices_to_flip = self.rng.choice(base_pattern.size, self.flips, replace=False)
        
        deltas = []
        for bit_index in bit_indices_to_flip:
            flat_pattern = base_pattern.flatten()
            flat_pattern[bit_index] = 1 - flat_pattern[bit_index]
            flipped_pattern = flat_pattern.reshape(base_pattern.shape)
            flipped_power = self.engine.run_simulation(flipped_pattern)
            deltas.append(np.abs(flipped_power - base_power))
            
        return np.array(deltas)

    def score(self, text: str) -> dict:
        """
        Computes Radiance and Velcridance scores based on the configured metric.
        """
        delta_dist = self.get_delta_distribution(text)
        
        # Calculate the core metric (mean, std, or max)
        if self.metric == 'std':
            radiance_base = np.std(delta_dist)
        elif self.metric == 'max':
            radiance_base = np.max(delta_dist)
        else: # Default to mean
            radiance_base = np.mean(delta_dist)
            
        # Radiance: The direct measure of semantic sensitivity.
        radiance_score = radiance_base
        
        # Velcridance: A measure of rigidity, using log1p for better numeric stability.
        # We use the inverse of radiance here. A high radiance (sensitivity) means low velcridance (rigidity).
        velcridance_score = np.log1p(1 / (radiance_score + 1e-12)) # Add small epsilon to avoid division by zero

        return {
            "radiance_score": float(radiance_score),
            "velcridance_score": float(velcridance_score)
        }


# --- File & System Utilities (Mostly Unchanged) ---
def strip_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    for element in soup(["script", "style"]):
        element.decompose()
    return re.sub(r'\s+', ' ', soup.get_text()).strip()

def get_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    return strip_html(content) if path.lower().endswith('.html') else content

def append_to_csv(result_dict: dict, csv_path: str):
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=result_dict.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(result_dict)

def move_to_processed(source_path: str):
    base_dir = os.path.dirname(source_path)
    filename = os.path.basename(source_path)
    processed_dir = os.path.join(base_dir, "processed")
    os.makedirs(processed_dir, exist_ok=True)
    destination_path = os.path.join(processed_dir, filename)
    shutil.move(source_path, destination_path)
    print(f"  ✓ Moved to: {os.path.relpath(destination_path)}")

# --- Analysis & Visualization (Upgraded) ---
def analyze_and_log(dir_path: str, label: str, scorer: PirouetteScorerV2, csv_path: str):
    """Processes all files in a directory, scoring and logging them."""
    if not os.path.isdir(dir_path): return
    print(f"\n--- Scanning '{label}' directory: {dir_path} ---")
    files = [f for f in os.listdir(dir_path) if f.lower().endswith(('.txt', '.html')) and os.path.isfile(os.path.join(dir_path, f))]
    if not files: print("  No new files to process."); return

    for filename in files:
        file_path = os.path.join(dir_path, filename)
        print(f"\n- Processing: {filename}")
        try:
            content = get_content(file_path)
            if not content or not content.strip():
                print(f"  ✗ Error: No content found."); move_to_processed(file_path); continue
            
            scores = scorer.score(content)
            result = {"file": filename, "category": label, **scores}
            
            append_to_csv(result, csv_path)
            print(f"  ✓ Scores logged: V={scores['velcridance_score']:.4f}, R={scores['radiance_score']:.6f}")
            move_to_processed(file_path)
        except Exception as e:
            print(f"  ✗ An error occurred: {e}")

def run_statistical_analysis(df: pd.DataFrame):
    """Performs and prints correlation and ANOVA tests."""
    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS")
    print("="*60)

    if len(df) < 3 or df['category'].nunique() < 2:
        print("Insufficient data for statistical analysis (need at least 3 data points and 2 categories).")
        return

    # 1. Correlation Matrix
    print("\n--- Pearson Correlation Matrix ---")
    corr_matrix = df[['radiance_score', 'velcridance_score']].corr()
    print(corr_matrix)
    
    # 2. ANOVA (Analysis of Variance)
    print("\n--- ANOVA: Does 'category' explain score variance? ---")
    try:
        # Radiance
        model_r = ols('radiance_score ~ C(category)', data=df).fit()
        print("\n[Analysis for Radiance Score]")
        print(f"F-statistic: {model_r.fvalue:.4f}, p-value: {model_r.f_pvalue:.4f}")
        if model_r.f_pvalue < 0.05:
            print("Conclusion: The difference between categories is statistically significant for Radiance.")
        else:
            print("Conclusion: Category does not significantly explain the variance in Radiance scores.")

        # Velcridance
        model_v = ols('velcridance_score ~ C(category)', data=df).fit()
        print("\n[Analysis for Velcridance Score]")
        print(f"F-statistic: {model_v.fvalue:.4f}, p-value: {model_v.f_pvalue:.4f}")
        if model_v.f_pvalue < 0.05:
            print("Conclusion: The difference between categories is statistically significant for Velcridance.")
        else:
            print("Conclusion: Category does not significantly explain the variance in Velcridance scores.")
    except Exception as e:
        print(f"Could not run ANOVA analysis: {e}")

    print("\n" + "="*60 + "\n")

def plot_results(df: pd.DataFrame):
    """Generates a scatter plot using z-score normalized values."""
    print("Generating new plot...")
    if df.empty: return

    # Z-Score Normalization for better visualization
    df['radiance_z'] = (df['radiance_score'] - df['radiance_score'].mean()) / df['radiance_score'].std()
    df['velcridance_z'] = (df['velcridance_score'] - df['velcridance_score'].mean()) / df['velcridance_score'].std()

    fig, ax = plt.subplots(figsize=(12, 10))
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}
    
    for category, group in df.groupby('category'):
        ax.scatter(group['velcridance_z'], group['radiance_z'], s=100, alpha=0.8, ec='w', c=colors.get(category, 'gray'), label=category.capitalize())

    # Add labels for each point
    for i, row in df.iterrows():
        ax.text(row['velcridance_z'] + 0.05, row['radiance_z'], row['file'].split('.')[0], fontsize=9, alpha=0.7)

    ax.set_title('Normalized Velcridance vs. Radiance (Z-Scores)', fontsize=16)
    ax.set_xlabel('Normalized Velcridance Score (Rigidity)', fontsize=12)
    ax.set_ylabel('Normalized Radiance Score (Sensitivity)', fontsize=12)
    ax.axhline(0, color='grey', linestyle='--', lw=1)
    ax.axvline(0, color='grey', linestyle='--', lw=1)
    ax.legend(title='Category')
    ax.grid(True)
    
    output_filename = 'vr_analysis_plot_v2.png'
    plt.savefig(output_filename)
    print(f"✅ Results plot updated and saved as '{output_filename}'")
    plt.show()

# --- Main Execution Block ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pirouette Framework Analyzer v2")
    parser.add_argument('--flips', type=int, default=256, help="Number of random bit-flips per document.")
    parser.add_argument('--amplitude', type=float, default=0.1, help="Perturbation amplitude for the simulation.")
    parser.add_argument('--metric', type=str, default='mean', choices=['mean', 'std', 'max'], help="Metric to calculate scores (mean, std, max of deltas).")
    parser.add_argument('--clear_results', action='store_true', help="Delete the existing results CSV to start fresh.")
    args = parser.parse_args()

    BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
    RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
    VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")
    RESULTS_CSV = "vr_analysis_results_v2.csv"
    
    if args.clear_results and os.path.exists(RESULTS_CSV):
        os.remove(RESULTS_CSV)
        print("Cleared previous results CSV.")

    os.makedirs(RADIANT_DIR, exist_ok=True)
    os.makedirs(VELCRID_DIR, exist_ok=True)

    # Initialize the new scorer with CLI arguments
    scorer = PirouetteScorerV2(flips=args.flips, amplitude=args.amplitude, metric=args.metric)
    
    # Process directories
    analyze_and_log(RADIANT_DIR, "radiant", scorer, RESULTS_CSV)
    analyze_and_log(VELCRID_DIR, "velcrid", scorer, RESULTS_CSV)

    print("\n--- Analysis Run Complete ---")
    
    # Final analysis and plotting
    if os.path.exists(RESULTS_CSV):
        results_df = pd.read_csv(RESULTS_CSV)
        run_statistical_analysis(results_df)
        plot_results(results_df)
    else:
        print("No results file found to analyze or plot.")