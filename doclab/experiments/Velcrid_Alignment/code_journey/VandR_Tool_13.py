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
import math

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

# --- V4 Scorer: Modified for Batch Processing ---
class PirouetteScorerV4:
    def __init__(self, grid_size=128, flips=4096, amplitude=0.1):
        self.flips = flips
        self.engine = SemanticDistillator(grid_size=grid_size, perturbation_amplitude=amplitude)

    @staticmethod
    def _create_seed_from_title(title: str) -> int:
        return int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % (2**32)

    def calculate_stats_from_file(self, temp_file_path):
        n = 0
        mean = 0.0
        M2 = 0.0
        with open(temp_file_path, 'r') as f:
            for line in f:
                x = float(line)
                n += 1
                delta = x - mean
                mean += delta / n
                delta2 = x - mean
                M2 += delta * delta2
        if n < 2: return mean, 0.0
        variance = M2 / n
        std_dev = math.sqrt(variance)
        return mean, std_dev

    def run_simulation_batch(self, pattern_path: str, title: str, temp_file_path: str, completed_flips: int, batch_size: int):
        print(f"[CHECKPOINT] Preparing batch for '{title}' by loading pre-calculated pattern.")

        # --- Load the pre-calculated base pattern ---
        base_pattern = np.load(pattern_path)
        base_power = self.engine.run_simulation(base_pattern)
        flat_pattern_base = base_pattern.flatten()

        # --- This part remains deterministic ---
        seed = self._create_seed_from_title(title)
        rng = np.random.default_rng(seed)
        static_grid = rng.random((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        bit_indices = np.argsort(static_grid.flatten())[-self.flips:]

        # --- Select the correct slice of flips for this batch ---
        flips_to_run = bit_indices[completed_flips : completed_flips + batch_size]
        print(f"[CHECKPOINT] This batch will run {len(flips_to_run)} flips.")

        # --- Open file in APPEND mode 'a' to add to existing work ---
        with open(temp_file_path, 'a') as f:
            for i, bit_index in enumerate(flips_to_run):
                variant = flat_pattern_base.copy()
                variant[bit_index] = 1 - variant[bit_index]
                flipped_power = self.engine.run_simulation(variant.reshape(base_pattern.shape))
                delta = np.abs(flipped_power - base_power)
                f.write(f"{delta}\n")

        print(f"[CHECKPOINT] Batch for '{title}' complete. Progress is saved.")
        return True

# --- File Utilities (with helpers for checkpointing) ---
def get_content_chunks(path: str, chunk_size=8192):
    # This is a generator, so it's memory-efficient.
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            if path.lower().endswith('.html'):
                content = strip_gutenberg_headers(BeautifulSoup(f.read(), "html.parser").get_text())
                for i in range(0, len(content), chunk_size): yield content[i:i+chunk_size]
            else:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk: break
                    yield strip_gutenberg_headers(chunk)
    except Exception as e:
        print(f"  ✗ ERROR during file read for {path}: {e}")
        return

def count_lines(path: str) -> int:
    if not os.path.exists(path): return 0
    with open(path, 'r') as f:
        return sum(1 for _ in f)

def create_pattern_file(text_iterator_factory, grid_size, output_path):
    """Reads a text file via an iterator and saves the composite pattern to a .npy file."""
    print(f"[PRE-CALC] Creating pattern file for {os.path.basename(output_path)}...")
    # This function is temporary and can be removed after the script is updated.
    # Note: The function `text_to_binary_image` is defined within the `SemanticDistillator` class.
    # To make this helper function work, you would need to either pass an instance of
    # `SemanticDistillator` or move the `text_to_binary_image` logic out of the class.
    # For the purpose of this example, we'll assume the logic is accessible.

    # A simplified placeholder for the text_to_binary_image logic:
    def text_to_binary_image(text, grid_size):
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
        target_size = grid_size * grid_size
        if binary_array.size < target_size:
            binary_array = np.pad(binary_array, (0, target_size - binary_array.size), 'constant')
        else:
            binary_array = binary_array[:target_size]
        return binary_array.reshape((grid_size, grid_size))


    composite_pattern = np.zeros((grid_size, grid_size), dtype=np.float32)
    chunk_count = 0
    for text_chunk in text_iterator_factory():
        composite_pattern += text_to_binary_image(text_chunk, grid_size)
        chunk_count += 1

    if chunk_count > 0:
        final_pattern = composite_pattern / chunk_count
        np.save(output_path, final_pattern)
        print(f"[PRE-CALC]  ✓ Saved pattern to {os.path.basename(output_path)}")
        return True
    return False

def load_completed_files(csv_path: str) -> set:
    if not os.path.exists(csv_path): return set()
    df = pd.read_csv(csv_path)
    return set(df['file'].unique())

def strip_gutenberg_headers(raw_text: str) -> str:
    start_pattern = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.IGNORECASE | re.DOTALL)
    end_pattern = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*", re.IGNORECASE | re.DOTALL)
    text = start_pattern.sub('', raw_text); text = end_pattern.sub('', text)
    return text.strip()

def append_to_csv(result_dict: dict, csv_path: str):
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=result_dict.keys())
        if not file_exists: writer.writeheader()
        writer.writerow(result_dict)

def move_to_processed(source_path: str):
    processed_dir = os.path.join(os.path.dirname(source_path), "processed")
    os.makedirs(processed_dir, exist_ok=True)
    shutil.move(source_path, os.path.join(processed_dir, os.path.basename(source_path)))
    print(f"  ✓ Moved '{os.path.basename(source_path)}' to processed folder.")

# --- Main Execution Block with Checkpointing Logic ---
if __name__ == '__main__':
    # --- ⚙️ CONFIGURATION ---
    GRID_SIZE = 64
    TOTAL_FLIPS = 4096
    AMPLITUDE = 0.1
    CHUNK_SIZE = 16384
    BATCH_SIZE = 200 # Lowered for stability

    # --- 📂 FOLDER & FILE SETUP ---
    BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
    RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
    VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")
    RESULTS_CSV = "vr_analysis_results_v4.csv"

    # --- Initialize scorer ---
    scorer = PirouetteScorerV4(grid_size=GRID_SIZE, flips=TOTAL_FLIPS, amplitude=AMPLITUDE)

    # --- 🔁 AUTO-RUNNER LOOP ---
    while True:
        manifest = []
        for dir_path, category in [(RADIANT_DIR, "radiant"), (VELCRID_DIR, "velcrid")]:
            if not os.path.isdir(dir_path): continue
            for f in os.listdir(dir_path):
                if f.lower().endswith(('.txt', '.html')) and os.path.isfile(os.path.join(dir_path, f)):
                    manifest.append({'path': os.path.join(dir_path, f), 'category': category})

        completed_files = load_completed_files(RESULTS_CSV)

        if len(manifest) == len(completed_files) and len(manifest) > 0:
            print("\n--- ✅ All files have been processed and finalized! Shutting down. ---")
            break

        work_done_this_pass = False
        for item in manifest:
            file_path = item['path']
            category = item['category']
            filename = os.path.basename(file_path)

            if filename in completed_files: continue

            print(f"\n--- Checking work for: {filename} ---")
            
            # --- Define paths for our two types of temp files ---
            file_hash = hashlib.md5(filename.encode()).hexdigest()
            temp_delta_path = f"temp_deltas_{file_hash}.tmp"
            temp_pattern_path = f"temp_pattern_{file_hash}.npy"

            # --- STAGE 1: Ensure the .npy pattern file exists ---
            if not os.path.exists(temp_pattern_path):
                print(f"[PREP] Pattern file not found. Creating it now...")
                content_iterator_factory = lambda: get_content_chunks(file_path, CHUNK_SIZE)
                create_pattern_file(content_iterator_factory, GRID_SIZE, temp_pattern_path)
                work_done_this_pass = True
                break # Break to restart the loop, ensuring we handle one file at a time.

            # --- STAGE 2: Process a batch or finalize ---
            completed_flips = count_lines(temp_delta_path)

            if completed_flips >= TOTAL_FLIPS:
                # --- Finalization Phase ---
                print(f"[FINALIZE] All {TOTAL_FLIPS} flips are complete. Finalizing score...")
                vel, rad = scorer.calculate_stats_from_file(temp_delta_path)
                text_len = sum(len(chunk) for chunk in get_content_chunks(file_path, CHUNK_SIZE))
                result = {"file": filename, "category": category, "velcridance_score": vel, "radiance_score": rad, "text_length": text_len}
                
                append_to_csv(result, RESULTS_CSV)
                os.remove(temp_delta_path)
                os.remove(temp_pattern_path) # Clean up the pattern file too
                move_to_processed(file_path)
                print(f"[FINALIZE]  ✓ Work for '{filename}' is fully complete.")
                work_done_this_pass = True
                break
            else:
                # --- Work Phase (now much simpler) ---
                scorer.run_simulation_batch(temp_pattern_path, filename, temp_delta_path, completed_flips, BATCH_SIZE)
                work_done_this_pass = True
                break

        if not work_done_this_pass:
            print("\n--- No new work found in a full pass. Shutting down. ---")
            break