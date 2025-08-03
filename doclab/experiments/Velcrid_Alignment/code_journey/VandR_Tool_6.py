import os
import re
import csv
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
    def __init__(self, grid_size=128, num_frames=200, noise_level=0.05, perturbation_amplitude=0.1, seed=0):
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

# --- V3 Scorer: Independent Metrics ---
class PirouetteScorerV3:
    def __init__(self, grid_size=128, flips=4096, amplitude=0.1, seed=42):
        self.flips = flips
        self.rng = np.random.default_rng(seed)
        self.engine = SemanticDistillator(grid_size=grid_size, perturbation_amplitude=amplitude, seed=seed)
        print(f"Scorer V3 initialized with: grid={grid_size}, flips={flips}, amplitude={amplitude}")

    def get_delta_distribution(self, text: str, return_map=False):
        base_pattern = self.engine.text_to_binary_image(text)
        base_power = self.engine.run_simulation(base_pattern)
        bit_indices = self.rng.choice(base_pattern.size, self.flips, replace=False)
        
        deltas = []
        delta_map = np.zeros_like(base_pattern, dtype=float)
        
        for bit_index in bit_indices:
            flat_pattern = base_pattern.flatten()
            flat_pattern[bit_index] = 1 - flat_pattern[bit_index]
            flipped_power = self.engine.run_simulation(flat_pattern.reshape(base_pattern.shape))
            delta = np.abs(flipped_power - base_power)
            deltas.append(delta)
            if return_map:
                np.put(delta_map, bit_index, delta)

        return (np.array(deltas), delta_map) if return_map else (np.array(deltas), None)

    def score(self, text: str) -> dict:
        delta_dist, _ = self.get_delta_distribution(text)
        return {
            "velcridance_score": float(np.mean(delta_dist)), # Average sensitivity
            "radiance_score": float(np.std(delta_dist)),     # Variability of sensitivity
            "text_length": len(text)
        }

# --- File & System Utilities (Gutenberg Stripper Added) ---
def strip_gutenberg_headers(raw_text: str) -> str:
    """Removes Project Gutenberg headers and footers."""
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK"
    ]
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK"
    ]
    
    text = raw_text
    
    for marker in start_markers:
        start_pos = text.find(marker)
        if start_pos != -1:
            end_of_line = text.find('\n', start_pos)
            text = text[end_of_line+1:]
            break

    for marker in end_markers:
        end_pos = text.find(marker)
        if end_pos != -1:
            text = text[:end_pos]
            break
            
    return text.strip()

def get_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if path.lower().endswith('.html'):
        content = BeautifulSoup(content, "html.parser").get_text()
    
    # Always run the Gutenberg stripper
    return strip_gutenberg_headers(content)

def append_to_csv(result_dict: dict, csv_path: str):
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=result_dict.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(result_dict)

def move_to_processed(source_path: str):
    processed_dir = os.path.join(os.path.dirname(source_path), "processed")
    os.makedirs(processed_dir, exist_ok=True)
    shutil.move(source_path, os.path.join(processed_dir, os.path.basename(source_path)))
    print(f"  ✓ Moved to: {os.path.relpath(processed_dir)}")

# --- Analysis & Visualization (Upgraded) ---
def analyze_and_log(dir_path: str, label: str, scorer: PirouetteScorerV3, csv_path: str):
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
                print(f"  ✗ Error: No content found after cleaning."); move_to_processed(file_path); continue
            
            scores = scorer.score(content)
            result = {"file": filename, "category": label, **scores}
            
            append_to_csv(result, csv_path)
            print(f"  ✓ Scores logged: V={scores['velcridance_score']:.4e}, R={scores['radiance_score']:.4e}, Len={scores['text_length']}")
            move_to_processed(file_path)
        except Exception as e:
            print(f"  ✗ An error occurred: {e}")

def run_final_analysis(df: pd.DataFrame):
    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS (Full-Length Texts Only)")
    print("="*60)
    
    # 1. Correlation Matrix (including length)
    print("\n--- Pearson Correlation Matrix ---")
    corr_df = df[['velcridance_score', 'radiance_score', 'text_length']]
    print(corr_df.corr())

    # 2. ANOVA
    print("\n--- ANOVA: Does 'category' explain score variance? ---")
    try:
        model_v = ols('velcridance_score ~ C(category)', data=df).fit()
        print(f"\n[Velcridance (mean ΔE)] F-statistic: {model_v.fvalue:.4f}, p-value: {model_v.f_pvalue:.4f}")
        model_r = ols('radiance_score ~ C(category)', data=df).fit()
        print(f"[Radiance (std ΔE)]    F-statistic: {model_r.fvalue:.4f}, p-value: {model_r.f_pvalue:.4f}")
    except Exception as e:
        print(f"Could not run ANOVA: {e}")
    print("\n" + "="*60 + "\n")

def plot_results(df: pd.DataFrame):
    # Z-Score Normalization
    df['velcridance_z'] = (df['velcridance_score'] - df['velcridance_score'].mean()) / df['velcridance_score'].std()
    df['radiance_z'] = (df['radiance_score'] - df['radiance_score'].mean()) / df['radiance_score'].std()

    fig, ax = plt.subplots(figsize=(12, 10))
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}
    
    for category, group in df.groupby('category'):
        ax.scatter(group['velcridance_z'], group['radiance_z'], s=120, alpha=0.8, ec='w', c=colors.get(category, 'gray'), label=category.capitalize())
    for i, row in df.iterrows():
        ax.text(row['velcridance_z'] + 0.05, row['radiance_z'], row['file'].split('.')[0], fontsize=9, alpha=0.7)

    ax.set_title('Normalized Velcridance (mean ΔE) vs. Radiance (std ΔE)', fontsize=16)
    ax.set_xlabel('Normalized Velcridance Score (Z-score)', fontsize=12)
    ax.set_ylabel('Normalized Radiance Score (Z-score)', fontsize=12)
    ax.axhline(0, color='grey', linestyle='--', lw=1); ax.axvline(0, color='grey', linestyle='--', lw=1)
    ax.legend(title='Category'); ax.grid(True)
    
    plt.savefig('vr_analysis_plot_v3.png')
    print("✅ Results plot updated and saved as 'vr_analysis_plot_v3.png'")
    plt.show()
    
def generate_heatmap(file_path: str, scorer: PirouetteScorerV3):
    print(f"\n--- Generating Heatmap for: {os.path.basename(file_path)} ---")
    content = get_content(file_path)
    if not content: print("Cannot generate heatmap, no content found."); return
    
    _, delta_map = scorer.get_delta_distribution(content, return_map=True)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(delta_map, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='|ΔE| Magnitude')
    plt.title(f'Semantic Sensitivity Heatmap\n{os.path.basename(file_path)}')
    plt.xlabel('Bit Position (X)')
    plt.ylabel('Bit Position (Y)')
    heatmap_filename = f"heatmap_{os.path.basename(file_path)}.png"
    plt.savefig(heatmap_filename)
    print(f"✅ Heatmap saved as '{heatmap_filename}'")
    plt.show()

# --- Main Execution Block ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pirouette Framework Analyzer v3")
    parser.add_argument('--grid-size', type=int, default=128)
    parser.add_argument('--flips', type=int, default=4096)
    parser.add_argument('--amplitude', type=float, default=0.1)
    parser.add_argument('--clear-results', action='store_true', help="Delete the existing results CSV to start fresh.")
    parser.add_argument('--generate-heatmap', type=str, metavar='FILE', help="Generate a sensitivity heatmap for a single file instead of batch processing.")
    args = parser.parse_args()

    scorer = PirouetteScorerV3(grid_size=args.grid_size, flips=args.flips, amplitude=args.amplitude)

    if args.generate_heatmap:
        if os.path.exists(args.generate_heatmap):
            generate_heatmap(args.generate_heatmap, scorer)
        else:
            print(f"Error: File not found for heatmap generation: {args.generate_heatmap}")
    else:
        # Standard batch processing workflow
        BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
        RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
        VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")
        RESULTS_CSV = "vr_analysis_results_v3.csv"
        
        if args.clear_results and os.path.exists(RESULTS_CSV):
            os.remove(RESULTS_CSV); print("Cleared previous results CSV.")

        os.makedirs(RADIANT_DIR, exist_ok=True); os.makedirs(VELCRID_DIR, exist_ok=True)
        
        analyze_and_log(RADIANT_DIR, "radiant", scorer, RESULTS_CSV)
        analyze_and_log(VELCRID_DIR, "velcrid", scorer, RESULTS_CSV)

        print("\n--- Analysis Run Complete ---")
        
        if os.path.exists(RESULTS_CSV):
            df_raw = pd.read_csv(RESULTS_CSV)
            # Filter out example files for final analysis and plotting
            df_filtered = df_raw[~df_raw['file'].str.contains("example", case=False)]
            
            if not df_filtered.empty:
                run_final_analysis(df_filtered)
                plot_results(df_filtered)
            else:
                print("No full-length texts found in results to analyze.")
        else:
            print("No results file found.")