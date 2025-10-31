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
import gc # Import garbage collection module

# --- Configuration & Suppressions ---
warnings.filterwarnings("ignore", category=FutureWarning)
plt.style.use('seaborn-v0_8-whitegrid')

# --- Core Simulation Engine ---
class SemanticDistillator:
    def __init__(self, grid_size=64, num_frames=200, noise_level=0.05, perturbation_amplitude=0.1):
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
        # Ensure grid is float32 to manage memory
        grid = (self.base_static_field + initial_pattern * self.perturbation_amplitude).astype(np.float32)
        total_power = 0.0
        for _ in range(self.num_frames):
            grid = convolve(grid, self.evolution_kernel, mode='wrap')
            total_power += np.sum(np.square(grid))
        return total_power / (self.num_frames * self.grid_size * self.grid_size)

# --- V4 Scorer: Static-Seeded Flip Selection ---
class PirouetteScorerV4:
    def __init__(self, grid_size=64, flips=4096, amplitude=0.1):
        self.flips = flips
        self.engine = SemanticDistillator(grid_size=grid_size, perturbation_amplitude=amplitude)
        print(f"Scorer V4 initialized with: grid={grid_size}, flips={flips}, amplitude={amplitude}")

    @staticmethod
    def _create_seed_from_title(title: str) -> int:
        return int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % (2**32)

    def get_delta_distribution(self, text_iterator, title: str, return_map=False):
        seed = self._create_seed_from_title(title)
        rng = np.random.default_rng(seed)
        static_grid = rng.random((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        
        bit_indices = np.argsort(static_grid.flatten())[-self.flips:]

        all_deltas = []
        delta_map = np.zeros((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        
        # Process text chunk by chunk
        for text_chunk in text_iterator:
            if not text_chunk: continue

            base_pattern = self.engine.text_to_binary_image(text_chunk)
            base_power = self.engine.run_simulation(base_pattern)
            
            flat_pattern_base = base_pattern.flatten()
            
            chunk_deltas = []
            for bit_index in bit_indices:
                variant = flat_pattern_base.copy()
                variant[bit_index] = 1 - variant[bit_index]
                flipped_power = self.engine.run_simulation(variant.reshape(base_pattern.shape))
                delta = np.abs(flipped_power - base_power)
                chunk_deltas.append(delta)
                if return_map:
                    # Accumulate deltas in the map; you might average or sum them
                    np.put(delta_map, bit_index, delta_map.flat[bit_index] + delta)

            all_deltas.extend(chunk_deltas)
            # Clean up memory explicitly
            del base_pattern, flat_pattern_base, chunk_deltas
            gc.collect()

        final_deltas = np.array(all_deltas, dtype=np.float32)
        return (final_deltas, delta_map) if return_map else (final_deltas, None)

    def score(self, text_iterator, title: str) -> dict:
        """Processes text from an iterator to manage memory."""
        # Calculate total text length by iterating through chunks
        # This is memory-inefficient if not handled carefully, but necessary for your output
        # A more memory-friendly approach would be to estimate or handle length differently
        total_len = sum(len(chunk) for chunk in text_iterator()) # text_iterator needs to be a callable that returns a new iterator

        delta_dist, _ = self.get_delta_distribution(text_iterator(), title)
        
        if len(delta_dist) == 0:
            return {"velcridance_score": 0.0, "radiance_score": 0.0, "text_length": total_len}

        return {
            "velcridance_score": float(np.mean(delta_dist)),
            "radiance_score": float(np.std(delta_dist)),
            "text_length": total_len
        }

# --- File & System Utilities ---
def strip_gutenberg_headers(raw_text: str) -> str:
    start_pattern = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.IGNORECASE | re.DOTALL)
    end_pattern = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*", re.IGNORECASE | re.DOTALL)
    
    text = start_pattern.sub('', raw_text)
    text = end_pattern.sub('', text)
    return text.strip()

def get_content_chunks(path: str, chunk_size=8192):
    """Yields chunks of text from a file, processing HTML content."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            if path.lower().endswith('.html'):
                # For HTML, we still need to parse it, which can be memory intensive.
                # A truly robust solution for massive HTML would involve stream-parsing.
                soup = BeautifulSoup(f.read(), "html.parser")
                content = strip_gutenberg_headers(soup.get_text())
                # Yield the parsed content in chunks
                for i in range(0, len(content), chunk_size):
                    yield content[i:i+chunk_size]
            else:
                # For text files, we can read and yield chunk by chunk
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield strip_gutenberg_headers(chunk)
    except Exception as e:
        print(f"Error reading or parsing {path}: {e}")
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

# --- Analysis & Visualization (Largely Unchanged) ---
def analyze_and_log(dir_path: str, label: str, scorer: PirouetteScorerV4, csv_path: str, chunk_size: int):
    if not os.path.isdir(dir_path): return
    print(f"\n--- Scanning '{label}' directory: {dir_path} ---")
    files = [f for f in os.listdir(dir_path) if f.lower().endswith(('.txt', '.html')) and os.path.isfile(os.path.join(dir_path, f))]
    if not files: print("  No new files to process."); return

    for filename in files:
        file_path = os.path.join(dir_path, filename)
        print(f"\n- Processing: {filename}")
        try:
            # Create a callable that returns a new generator each time it's called
            content_iterator_factory = lambda: get_content_chunks(file_path, chunk_size)
            
            # Check if content is empty without loading it all
            first_chunk = next(content_iterator_factory(), None)
            if first_chunk is None or not first_chunk.strip():
                 print(f"  ✗ Error: No content found after cleaning."); move_to_processed(file_path); continue

            # The score function now needs a way to get the iterator factory
            scores = scorer.score(content_iterator_factory, filename)
            
            result = {"file": filename, "category": label, **scores}
            
            append_to_csv(result, csv_path)
            print(f"  ✓ Scores logged: V={scores['velcridance_score']:.4e}, R={scores['radiance_score']:.4e}, Len={scores['text_length']}")
            move_to_processed(file_path)
            
            # Force garbage collection after processing each file
            gc.collect()

        except Exception as e:
            print(f"  ✗ An error occurred while processing {filename}: {e}")
            
# --- Main Execution Block ---
if __name__ == '__main__':
    # --- ⚙️ CONFIGURATION ---
    GRID_SIZE = 64
    NUM_FLIPS = 4096
    AMPLITUDE = 0.1
    CHUNK_SIZE = 16384 # Process files in 16KB chunks. Adjust based on your RAM.
    
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
            # The rest of the analysis assumes the dataframe fits in memory, which is usually fine.
            df_filtered = df_raw[~df_raw['file'].str.contains("example", case=False)]
            if not df_filtered.empty:
                # The analysis functions (plot, stats) should be okay as they operate on the results CSV, not the raw text files.
                # run_final_analysis(df_filtered)
                # plot_results(df_filtered)
                pass # Placeholder for your analysis functions
            else:
                print("No full-length texts found in results to analyze.")
        else:
            print("No results file found.")
            
    elif GENERATE_HEATMAP_MODE:
        if os.path.exists(HEATMAP_FILE_PATH):
            # Heatmap generation might still be memory intensive.
            # You can adapt it to process chunks if needed.
            # generate_heatmap(HEATMAP_FILE_PATH, scorer)
            pass
        else:
            print(f"Error: File not found for heatmap generation: {HEATMAP_FILE_PATH}")