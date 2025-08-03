import os
import re
import csv
import shutil
import hashlib
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

# --- Core Simulation Engine ---
class SemanticDistillator:
    def __init__(self, grid_size=128, num_frames=200, noise_level=0.05, perturbation_amplitude=0.1):
        self.grid_size = grid_size
        self.num_frames = num_frames
        self.perturbation_amplitude = perturbation_amplitude
        # Note: The base static field is now deterministic for the class instance
        np.random.seed(0) 
        self.base_static_field = np.random.rand(self.grid_size, self.grid_size) * noise_level
        self.evolution_kernel = np.ones((3, 3)) / 9.0

    def text_to_binary_image(self, text):
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
        target_size = self.grid_size * self.grid_size
        binary_array = np.pad(binary_array, (0, max(0, target_size - binary_array.size)), 'constant')[:target_size]
        return binary_array.reshape((self.grid_size, self.grid_size))

    def run_simulation(self, initial_pattern):
        grid = self.base_static_field + initial_pattern * self.perturbation_amplitude
        total_power = sum(np.sum(grid := convolve(grid, self.evolution_kernel, mode='wrap')**2) for _ in range(self.num_frames))
        return total_power / (self.num_frames * self.grid_size * self.grid_size)

# --- V4 Scorer: Static-Seeded Flip Selection ---
class PirouetteScorerV4:
    def __init__(self, grid_size=128, flips=4096, amplitude=0.1):
        self.flips = flips
        self.engine = SemanticDistillator(grid_size=grid_size, perturbation_amplitude=amplitude)
        print(f"Scorer V4 initialized with: grid={grid_size}, flips={flips}, amplitude={amplitude}")

    @staticmethod
    def _create_seed_from_title(title: str) -> int:
        """Creates a deterministic integer seed from a string."""
        return int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % (2**32)

    def get_delta_distribution(self, text: str, title: str, return_map=False):
        """Calculates energy deltas using a title-seeded static grid to select flip locations."""
        # 1. "Static to decide": Generate the static pattern seeded by the title
        seed = self._create_seed_from_title(title)
        rng = np.random.default_rng(seed)
        static_grid = rng.random((self.engine.grid_size, self.engine.grid_size))
        
        # Determine which bits to flip by finding the highest values in the static grid
        bit_indices = np.argsort(static_grid.flatten())[-self.flips:]

        # 2. "Delta to sort" (or analyze): Calculate deltas for these chosen bits
        base_pattern = self.engine.text_to_binary_image(text)
        base_power = self.engine.run_simulation(base_pattern)
        
        deltas = []
        delta_map = np.zeros_like(base_pattern, dtype=float)
        flat_pattern_base = base_pattern.flatten()

        for bit_index in bit_indices:
            variant = flat_pattern_base.copy()
            variant[bit_index] = 1 - variant[bit_index]
            flipped_power = self.engine.run_simulation(variant.reshape(base_pattern.shape))
            delta = np.abs(flipped_power - base_power)
            deltas.append(delta)
            if return_map:
                np.put(delta_map, bit_index, delta)
        
        return (np.array(deltas), delta_map) if return_map else (np.array(deltas), None)

    def score(self, text: str, title: str) -> dict:
        delta_dist, _ = self.get_delta_distribution(text, title)
        return {
            "velcridance_score": float(np.mean(delta_dist)),
            "radiance_score": float(np.std(delta_dist)),
            "text_length": len(text)
        }

# --- File & System Utilities (Unchanged) ---
def strip_gutenberg_headers(raw_text: str) -> str:
    start_pattern = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.IGNORECASE | re.DOTALL)
    end_pattern = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*", re.IGNORECASE | re.DOTALL)
    
    text = start_pattern.sub('', raw_text)
    text = end_pattern.sub('', text)
    return text.strip()

def get_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if path.lower().endswith('.html'):
        content = BeautifulSoup(content, "html.parser").get_text()
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

# --- Analysis & Visualization (Unchanged) ---
def analyze_and_log(dir_path: str, label: str, scorer: PirouetteScorerV4, csv_path: str):
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
            
            scores = scorer.score(content, filename)
            result = {"file": filename, "category": label, **scores}
            
            append_to_csv(result, csv_path)
            print(f"  ✓ Scores logged: V={scores['velcridance_score']:.4e}, R={scores['radiance_score']:.4e}, Len={scores['text_length']}")
            move_to_processed(file_path)
        except Exception as e:
            print(f"  ✗ An error occurred: {e}")

def run_final_analysis(df: pd.DataFrame):
    print("\n" + "="*60 + "\nSTATISTICAL ANALYSIS (Full-Length Texts Only)\n" + "="*60)
    print("\n--- Pearson Correlation Matrix ---\n", df[['velcridance_score', 'radiance_score', 'text_length']].corr())
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
    
    plt.savefig('vr_analysis_plot_v4.png')
    print("✅ Results plot updated and saved as 'vr_analysis_plot_v4.png'")
    plt.show()

def generate_heatmap(file_path: str, scorer: PirouetteScorerV4):
    print(f"\n--- Generating Heatmap for: {os.path.basename(file_path)} ---")
    content = get_content(file_path)
    if not content: print("Cannot generate heatmap, no content found."); return
    
    _, delta_map = scorer.get_delta_distribution(content, os.path.basename(file_path), return_map=True)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(delta_map, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='|ΔE| Magnitude')
    plt.title(f'Semantic Sensitivity Heatmap\n{os.path.basename(file_path)}')
    plt.xlabel('Bit Position (X)'); plt.ylabel('Bit Position (Y)')
    plt.savefig(f"heatmap_{os.path.basename(file_path)}.png")
    print(f"✅ Heatmap saved as 'heatmap_{os.path.basename(file_path)}.png'")
    plt.show()

# --- Main Execution Block ---
if __name__ == '__main__':
    # --- ⚙️ CONFIGURATION ---
    # Set the main parameters for the analysis here.
    GRID_SIZE = 128
    NUM_FLIPS = 4096
    AMPLITUDE = 0.1
    
    # --- 📂 FOLDER & FILE SETUP ---
    BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
    RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
    VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")
    RESULTS_CSV = "vr_analysis_results_v4.csv"

    # --- 🚀 EXECUTION MODE ---
    # Set one of the following modes to True to run it.
    
    # Mode 1: Run the full batch analysis
    RUN_BATCH_ANALYSIS = True
    
    # Mode 2: Generate a heatmap for a single specific file
    GENERATE_HEATMAP_MODE = False
    HEATMAP_FILE_PATH = "velcrid/TheArtOfWar.txt" # File to analyze for the heatmap
    
    # Mode 3: Clear previous results to start fresh
    CLEAR_PREVIOUS_RESULTS = False
    
    # --- Script Logic ---
    if CLEAR_PREVIOUS_RESULTS and os.path.exists(RESULTS_CSV):
        os.remove(RESULTS_CSV)
        print("Cleared previous results CSV.")

    scorer = PirouetteScorerV4(grid_size=GRID_SIZE, flips=NUM_FLIPS, amplitude=AMPLITUDE)

    if RUN_BATCH_ANALYSIS:
        os.makedirs(RADIANT_DIR, exist_ok=True)
        os.makedirs(VELCRID_DIR, exist_ok=True)
        analyze_and_log(RADIANT_DIR, "radiant", scorer, RESULTS_CSV)
        analyze_and_log(VELCRID_DIR, "velcrid", scorer, RESULTS_CSV)

        print("\n--- Analysis Run Complete ---")
        
        if os.path.exists(RESULTS_CSV):
            df_raw = pd.read_csv(RESULTS_CSV)
            df_filtered = df_raw[~df_raw['file'].str.contains("example", case=False)]
            if not df_filtered.empty:
                run_final_analysis(df_filtered)
                plot_results(df_filtered)
            else:
                print("No full-length texts found in results to analyze.")
        else:
            print("No results file found.")
            
    elif GENERATE_HEATMAP_MODE:
        if os.path.exists(HEATMAP_FILE_PATH):
            generate_heatmap(HEATMAP_FILE_PATH, scorer)
        else:
            print(f"Error: File not found for heatmap generation: {HEATMAP_FILE_PATH}")