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
import sys # [DEBUG] Import sys to check object sizes

# --- Configuration & Suppressions ---
warnings.filterwarnings("ignore", category=FutureWarning)
plt.style.use('seaborn-v0_8-whitegrid')

# --- Core Simulation Engine ---
class SemanticDistillator:
    def __init__(self, grid_size=128, num_frames=200, noise_level=0.05, perturbation_amplitude=0.1):
        self.grid_size = grid_size
        self.num_frames = num_frames
        self.perturbation_amplitude = perturbation_amplitude
        np.random.seed(0) 
        self.base_static_field = np.random.rand(self.grid_size, self.grid_size).astype(np.float32) * noise_level
        self.evolution_kernel = np.ones((3, 3), dtype=np.float32) / 9.0

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
            grid = convolve(grid, self.evolution_kernel, mode='wrap')
            total_power += np.sum(np.square(grid))
        return total_power / (self.num_frames * self.grid_size * self.grid_size)

# --- V4 Scorer: Static-Seeded Flip Selection ---
class PirouetteScorerV4:
    def __init__(self, grid_size=128, flips=4096, amplitude=0.1):
        self.flips = flips
        self.engine = SemanticDistillator(grid_size=grid_size, perturbation_amplitude=amplitude)
        print(f"[DEBUG] Scorer V4 initialized with: grid={grid_size}, flips={flips}, amplitude={amplitude}")

    @staticmethod
    def _create_seed_from_title(title: str) -> int:
        return int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % (2**32)

    def get_delta_distribution(self, text_iterator, title: str, return_map=False):
        print(f"\n[DEBUG] Starting delta distribution for '{title}'...")
        seed = self._create_seed_from_title(title)
        rng = np.random.default_rng(seed)
        static_grid = rng.random((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        
        bit_indices = np.argsort(static_grid.flatten())[-self.flips:]
        
        # [FIX] Create a single composite pattern from all chunks instead of re-running for each.
        composite_pattern = np.zeros((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        chunk_count = 0
        for i, text_chunk in enumerate(text_iterator):
            if not text_chunk: continue
            print(f"[DEBUG]   - Processing chunk {i}...")
            chunk_image = self.engine.text_to_binary_image(text_chunk)
            composite_pattern += chunk_image
            chunk_count += 1
        
        if chunk_count == 0:
            print("[DEBUG] No valid chunks found. Returning empty deltas.")
            return (np.array([], dtype=np.float32), None)
            
        # [FIX] Average the composite pattern to get the final base pattern for the whole text.
        base_pattern = composite_pattern / chunk_count
        print(f"[DEBUG] ...Finished processing {chunk_count} chunks.")
        print(f"[DEBUG] Final base_pattern shape: {base_pattern.shape}, dtype: {base_pattern.dtype}")
        
        print("[DEBUG] Calculating base power...")
        base_power = self.engine.run_simulation(base_pattern)
        print(f"[DEBUG] Base power calculated: {base_power:.4e}")
        
        deltas = []
        delta_map = np.zeros_like(base_pattern, dtype=np.float32)
        flat_pattern_base = base_pattern.flatten()

        print(f"[DEBUG] Starting simulation for {self.flips} bit flips...")
        for i, bit_index in enumerate(bit_indices):
            if i > 0 and i % 500 == 0:
                 print(f"[DEBUG]   ...completed {i} / {self.flips} flips.")
            variant = flat_pattern_base.copy()
            variant[bit_index] = 1 - variant[bit_index]
            flipped_power = self.engine.run_simulation(variant.reshape(base_pattern.shape))
            delta = np.abs(flipped_power - base_power)
            deltas.append(delta)
            if return_map:
                np.put(delta_map, bit_index, delta)
        
        final_deltas = np.array(deltas, dtype=np.float32)
        print(f"[DEBUG] ...Finished bit flips.")
        print(f"[DEBUG] Final 'deltas' array shape: {final_deltas.shape}, size: {sys.getsizeof(final_deltas) / 1024:.2f} KB")
        
        # [FIX] Explicitly clean up large arrays
        del base_pattern, composite_pattern, flat_pattern_base
        gc.collect()

        return (final_deltas, delta_map) if return_map else (final_deltas, None)

    def score(self, text_iterator_factory, title: str) -> dict:
        print(f"[DEBUG] Scoring process started for '{title}'.")
        # To get length, we must iterate. The factory ensures we can do it again for the real run.
        total_len = sum(len(chunk) for chunk in text_iterator_factory())

        # The main calculation now uses a fresh iterator
        delta_dist, _ = self.get_delta_distribution(text_iterator_factory(), title)
        
        if len(delta_dist) == 0:
            return {"velcridance_score": 0.0, "radiance_score": 0.0, "text_length": total_len}

        return {
            "velcridance_score": float(np.mean(delta_dist)),
            "radiance_score": float(np.std(delta_dist)),
            "text_length": total_len
        }

# --- File & System Utilities (Unchanged from previous optimization) ---
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

# --- Analysis & Visualization (Unchanged) ---
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
            
            print("[DEBUG] Forcing garbage collection after file processing.")
            gc.collect()

        except Exception as e:
            print(f"  ✗ An unexpected error occurred while processing {filename}: {e}")
            import traceback
            traceback.print_exc()

# ... (plot_results and run_final_analysis functions remain the same) ...

# --- Main Execution Block ---
if __name__ == '__main__':
    # --- ⚙️ CONFIGURATION ---
    GRID_SIZE = 64 # Let's keep it at 64 for faster testing
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
    # ... other modes
    
    # --- Script Logic ---
    scorer = PirouetteScorerV4(grid_size=GRID_SIZE, flips=NUM_FLIPS, amplitude=AMPLITUDE)

    if RUN_BATCH_ANALYSIS:
        os.makedirs(RADIANT_DIR, exist_ok=True)
        os.makedirs(VELCRID_DIR, exist_ok=True)
        analyze_and_log(RADIANT_DIR, "radiant", scorer, RESULTS_CSV, CHUNK_SIZE)
        analyze_and_log(VELCRID_DIR, "velcrid", scorer, RESULTS_CSV, CHUNK_SIZE)
        # ... rest of analysis