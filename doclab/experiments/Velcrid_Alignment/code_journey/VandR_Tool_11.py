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
import gc
import sys
import math # [TURTLE MODE] Need for sqrt

# --- Core Simulation Engine (Unchanged) ---
class SemanticDistillator:
    def __init__(self, grid_size=128, num_frames=200, noise_level=0.05, perturbation_amplitude=0.1):
        self.grid_size = grid_size
        self.num_frames = num_frames
        self.perturbation_amplitude = perturbation_amplitude
        np.random.seed(0) 
        self.base_static_field = np.random.rand(self.grid_size, self.grid_size).astype(np.float32) * noise_level
        self.evolution_kernel = np.ones((3, 3), dtype=np.float32) / 9.0
        self.convolve_buffer = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)

    def text_to_binary_image(self, text):
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
        target_size = self.grid_size * self.grid_size
        if binary_array.size < target_size:
            binary_array = np.pad(binary_array, (0, target_size - binary_array.size), 'constant')
        else:
            binary_array = binary_array[:target_size]
        return binary_array.reshape((self.grid_size, self.grid_size))

    def run_simulation(self, initial_pattern):
        grid = (self.base_static_field + initial_pattern * self.perturbation_amplitude).astype(np.float32)
        total_power = 0.0
        for _ in range(self.num_frames):
            convolve(grid, self.evolution_kernel, output=self.convolve_buffer, mode='wrap')
            grid, self.convolve_buffer = self.convolve_buffer, grid
            total_power += np.sum(np.square(grid))
        return total_power / (self.num_frames * self.grid_size * self.grid_size)

# --- V4 Scorer: TURTLE MODE IMPLEMENTATION ---
class PirouetteScorerV4:
    def __init__(self, grid_size=128, flips=4096, amplitude=0.1):
        self.flips = flips
        self.engine = SemanticDistillator(grid_size=grid_size, perturbation_amplitude=amplitude)

    @staticmethod
    def _create_seed_from_title(title: str) -> int:
        return int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % (2**32)

    # [TURTLE MODE] New function to calculate stats from the temp file with minimal memory.
    def _calculate_stats_from_file(self, temp_file_path):
        print(f"[TURTLE DEBUG] Calculating stats by reading from {os.path.basename(temp_file_path)}...")
        n = 0
        mean = 0.0
        M2 = 0.0 # Sum of squares of differences from the current mean

        with open(temp_file_path, 'r') as f:
            for line in f:
                x = float(line)
                n += 1
                delta = x - mean
                mean += delta / n
                delta2 = x - mean
                M2 += delta * delta2
        
        if n < 2:
            return mean, 0.0

        variance = M2 / n
        std_dev = math.sqrt(variance)
        print(f"[TURTLE DEBUG] ...Stats calculated: mean={mean:.4e}, std={std_dev:.4e}")
        return mean, std_dev

    def get_and_write_deltas(self, text_iterator, title: str):
        print(f"\n[TURTLE DEBUG] Starting delta calculation for '{title}'. Will write results to disk.")
        
        # [TURTLE MODE] Define a temporary file path.
        temp_file_path = f"temp_deltas_{hashlib.md5(title.encode()).hexdigest()}.tmp"
        
        # ... (composite pattern creation is the same and memory-safe)
        composite_pattern = np.zeros((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        chunk_count = 0
        for text_chunk in text_iterator:
            if not text_chunk: continue
            chunk_image = self.engine.text_to_binary_image(text_chunk)
            composite_pattern += chunk_image
            chunk_count += 1
        
        if chunk_count == 0: return None
        
        base_pattern = composite_pattern / chunk_count
        base_power = self.engine.run_simulation(base_pattern)
        flat_pattern_base = base_pattern.flatten()

        seed = self._create_seed_from_title(title)
        rng = np.random.default_rng(seed)
        static_grid = rng.random((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        bit_indices = np.argsort(static_grid.flatten())[-self.flips:]

        print(f"[TURTLE DEBUG] Starting {self.flips} simulations. Writing deltas to {os.path.basename(temp_file_path)}...")
        
        # [TURTLE MODE] Open the temp file and write results one by one.
        with open(temp_file_path, 'w') as f:
            for i, bit_index in enumerate(bit_indices):
                if i > 0 and i % 100 == 0:
                     print(f"[TURTLE DEBUG]   ...completed {i} / {self.flips} flips.")
                
                variant = flat_pattern_base.copy()
                variant[bit_index] = 1 - variant[bit_index]
                
                # This is the most intensive part.
                flipped_power = self.engine.run_simulation(variant.reshape(base_pattern.shape))
                delta = np.abs(flipped_power - base_power)
                
                # Write to disk and forget. No memory is held long-term.
                f.write(f"{delta}\n")
        
        print(f"[TURTLE DEBUG] ...Finished writing all deltas to disk.")
        del base_pattern, composite_pattern, flat_pattern_base
        gc.collect()

        return temp_file_path

    def score(self, text_iterator_factory, title: str) -> dict:
        total_len = sum(len(chunk) for chunk in text_iterator_factory())

        # [TURTLE MODE] Step 1: Run simulations and get the path to the results file.
        temp_file_path = self.get_and_write_deltas(text_iterator_factory(), title)
        
        if temp_file_path is None:
            return {"velcridance_score": 0.0, "radiance_score": 0.0, "text_length": total_len}

        # [TURTLE MODE] Step 2: Calculate scores by reading the results file.
        velcridance, radiance = self._calculate_stats_from_file(temp_file_path)

        # [TURTLE MODE] Step 3: Clean up the temporary file.
        print(f"[TURTLE DEBUG] Cleaning up temporary file: {os.path.basename(temp_file_path)}")
        os.remove(temp_file_path)

        return {
            "velcridance_score": float(velcridance),
            "radiance_score": float(radiance),
            "text_length": total_len
        }

# --- The rest of the script is unchanged ---
# (File utilities, analysis, plotting, and main execution block are the same)
def strip_gutenberg_headers(raw_text: str) -> str:
    start_pattern = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.IGNORECASE | re.DOTALL)
    end_pattern = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*", re.IGNORECASE | re.DOTALL)
    text = start_pattern.sub('', raw_text)
    text = end_pattern.sub('', text)
    return text.strip()

def get_content_chunks(path: str, chunk_size=8192):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            if path.lower().endswith('.html'):
                content = strip_gutenberg_headers(BeautifulSoup(f.read(), "html.parser").get_text())
                for i in range(0, len(content), chunk_size):
                    yield content[i:i+chunk_size]
            else:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk: break
                    yield strip_gutenberg_headers(chunk)
    except Exception as e:
        print(f"  ✗ ERROR during file read for {path}: {e}")
        return

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

def analyze_and_log(dir_path: str, label: str, scorer: PirouetteScorerV4, csv_path: str, chunk_size: int):
    if not os.path.isdir(dir_path): return
    print(f"\n--- Scanning '{label}' directory: {dir_path} ---")
    files = [f for f in os.listdir(dir_path) if f.lower().endswith(('.txt', '.html')) and os.path.isfile(os.path.join(dir_path, f))]
    if not files: print("  No new files to process."); return

    for filename in files:
        file_path = os.path.join(dir_path, filename)
        print(f"\n- Processing: {filename}")
        try:
            content_iterator_factory = lambda: get_content_chunks(file_path, chunk_size)
            
            first_chunk = next(content_iterator_factory(), None)
            if first_chunk is None or not first_chunk.strip():
                 print(f"  ✗ Error: No content found after cleaning."); move_to_processed(file_path); continue

            scores = scorer.score(content_iterator_factory, filename)
            
            result = {"file": filename, "category": label, **scores}
            
            append_to_csv(result, csv_path)
            print(f"  ✓ Scores logged: V={scores['velcridance_score']:.4e}, R={scores['radiance_score']:.4e}, Len={scores['text_length']}")
            move_to_processed(file_path)
            
            gc.collect()

        except Exception as e:
            print(f"  ✗ An unexpected error occurred while processing {filename}: {e}")
            import traceback
            traceback.print_exc()

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
    content = get_content_chunks(file_path)
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

if __name__ == '__main__':
    # --- ⚙️ CONFIGURATION ---
    GRID_SIZE = 64
    NUM_FLIPS = 4096
    AMPLITUDE = 0.1
    CHUNK_SIZE = 16384 
    
    # --- 📂 FOLDER & FILE SETUP ---
    BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
    RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
    VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")
    RESULTS_CSV = "vr_analysis_results_v4.csv"

    # --- 🚀 EXECUTION MODE ---
    RUN_BATCH_ANALYSIS = True
    GENERATE_HEATMAP_MODE = False
    HEATMAP_FILE_PATH = "velcrid/TheArtOfWar.txt"
    CLEAR_PREVIOUS_RESULTS = False
    
    # --- Script Logic ---
    if CLEAR_PREVIOUS_RESULTS and os.path.exists(RESULTS_CSV):
        os.remove(RESULTS_CSV)
        print("Cleared previous results CSV.")

    scorer = PirouetteScorerV4(grid_size=GRID_SIZE, flips=NUM_FLIPS, amplitude=AMPLITUDE)

    if RUN_BATCH_ANALYSIS:
        os.makedirs(RADIANT_DIR, exist_ok=True)
        os.makedirs(VELCRID_DIR, exist_ok=True)
        analyze_and_log(RADIANT_DIR, "radiant", scorer, RESULTS_CSV, CHUNK_SIZE)
        analyze_and_log(VELCRID_DIR, "velcrid", scorer, RESULTS_CSV, CHUNK_SIZE)

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