import os
import sys
import re
import csv
import shutil
import hashlib
import numpy as np
import pandas as pd
from scipy.ndimage import convolve
from scipy.stats import kurtosis
from bs4 import BeautifulSoup
import tarfile
import io
import multiprocessing
import gc
import time

# --- Core Simulation Engine (Unchanged) ---
class SemanticDistillator:
    """Runs the core physics simulation on a 2D grid."""
    def __init__(self, grid_size=128, num_frames=200, noise_level=0.05, perturbation_amplitude=0.1):
        self.grid_size = grid_size
        self.num_frames = num_frames
        self.perturbation_amplitude = perturbation_amplitude
        np.random.seed(0)
        self.base_static_field = np.random.rand(self.grid_size, self.grid_size).astype(np.float32) * noise_level
        self.evolution_kernel = np.ones((3, 3), dtype=np.float32) / 9.0
        self.convolve_buffer = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)

    def run_simulation(self, initial_pattern):
        """Runs the simulation for a given pattern and returns the average power."""
        if not isinstance(initial_pattern, np.ndarray):
            return 0.0
        grid = (self.base_static_field + initial_pattern * self.perturbation_amplitude).astype(np.float32)
        total_power = 0.0
        for _ in range(self.num_frames):
            convolve(grid, self.evolution_kernel, output=self.convolve_buffer, mode='wrap')
            grid, self.convolve_buffer = self.convolve_buffer, grid
            if not isinstance(grid, np.ndarray):
                return 0.0
            total_power += np.sum(np.square(grid))
        return total_power / (self.num_frames * self.grid_size * self.grid_size)

# --- V4 Scorer (Unchanged) ---
class PirouetteScorerV4:
    """Handles the scoring logic, including batch processing and statistical analysis."""
    def __init__(self, grid_size=128, flips=4096, amplitude=0.1):
        self.flips = flips
        self.engine = SemanticDistillator(grid_size=grid_size, perturbation_amplitude=amplitude)

    @staticmethod
    def _create_seed_from_title(title: str) -> int:
        return int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % (2**32)

    def calculate_stats_from_file(self, temp_file_path):
        with open(temp_file_path, 'r') as f:
            deltas = [float(line) for line in f]
        if not deltas: return 0.0, 0.0, 0.0
        delta_array = np.array(deltas, dtype=np.float64)
        return np.mean(delta_array), np.std(delta_array), kurtosis(delta_array, fisher=False)

    def run_simulation_batch(self, pattern_path: str, title: str, temp_delta_path: str, drift_log_path: str, completed_flips: int, batch_size: int):
        base_pattern = np.load(pattern_path)
        base_power = self.engine.run_simulation(base_pattern)
        flat_pattern_base = base_pattern.flatten()
        seed = self._create_seed_from_title(title)
        rng = np.random.default_rng(seed)
        static_grid = rng.random((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        bit_indices = np.argsort(static_grid.flatten())[-self.flips:]
        flips_to_run = bit_indices[completed_flips : completed_flips + batch_size]
        batch_deltas = []
        with open(temp_delta_path, 'a') as f:
            for bit_index in flips_to_run:
                variant = flat_pattern_base.copy()
                variant[bit_index] = 1 - variant[bit_index]
                flipped_power = self.engine.run_simulation(variant.reshape(base_pattern.shape))
                delta = np.abs(flipped_power - base_power)
                f.write(f"{delta}\n")
                batch_deltas.append(delta)
        if batch_deltas:
            batch_mean = np.mean(np.array(batch_deltas, dtype=np.float64))
            flips_at_batch_end = completed_flips + len(batch_deltas)
            with open(drift_log_path, 'a', newline='') as df:
                writer = csv.writer(df)
                writer.writerow([flips_at_batch_end, batch_mean])

# --- File & Text Utilities (Functions must be self-contained for multiprocessing) ---
def strip_gutenberg_headers(raw_text: str) -> str:
    start_pattern = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.IGNORECASE | re.DOTALL)
    end_pattern = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*", re.IGNORECASE | re.DOTALL)
    text = start_pattern.sub('', raw_text)
    return end_pattern.sub('', text).strip()

def get_content_chunks_from_tar(archive_path, member_name, chunk_size):
    with tarfile.open(archive_path, 'r') as tar_handle:
        extracted_file = tar_handle.extractfile(member_name)
        if not extracted_file: return
        with io.TextIOWrapper(extracted_file, encoding='utf-8', errors='ignore') as text_reader:
            content = strip_gutenberg_headers(text_reader.read())
            if not content: return
            for i in range(0, len(content), chunk_size):
                yield content[i:i+chunk_size]

def text_to_binary_image(text, grid_size):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
    target_size = grid_size * grid_size
    binary_array = np.pad(binary_array, (0, max(0, target_size - binary_array.size)), 'constant')
    return binary_array[:target_size].reshape((grid_size, grid_size))

def create_pattern_file(archive_path, member_name, grid_size, chunk_size, output_path):
    composite_pattern = np.zeros((grid_size, grid_size), dtype=np.float32)
    chunk_count = 0
    text_iterator = get_content_chunks_from_tar(archive_path, member_name, chunk_size)
    for text_chunk in text_iterator:
        composite_pattern += text_to_binary_image(text_chunk, grid_size)
        chunk_count += 1
    if chunk_count > 0:
        np.save(output_path, composite_pattern / chunk_count)
        return True
    return None

def calculate_drift_score(drift_log_path):
    if not os.path.exists(drift_log_path): return 0.0
    data = pd.read_csv(drift_log_path, header=None, names=['flip_count', 'batch_mean'])
    if len(data) < 2: return 0.0
    return np.polyfit(data['flip_count'], data['batch_mean'], 1)[0]

def calculate_anisotropy_score(pattern_path):
    if not os.path.exists(pattern_path): return 0.0
    pattern = np.load(pattern_path)
    gy, gx = np.gradient(pattern)
    gxy, gxx = np.gradient(gx)
    gyy, gyx = np.gradient(gy)
    H_xy = (gxy + gyx) / 2.0
    trace = gxx + gyy
    determinant = gxx * gyy - H_xy**2
    eigenvalue_diff = np.sqrt(np.maximum(0, trace**2 - 4 * determinant))
    return np.mean(eigenvalue_diff)

# --- WORKER PROCESS FUNCTION ---
def process_file(item, config, result_queue):
    """This function runs in a separate process to process one file."""
    filename = os.path.basename(item['member_name'])
    print(f"--- [Worker] Starting work for: {filename} ---")
    
    # Unpack config
    archive_path = config['archive_path']
    grid_size = config['grid_size']
    total_flips = config['total_flips']
    amplitude = config['amplitude']
    chunk_size = config['chunk_size']
    batch_size = config['batch_size']

    file_hash = hashlib.md5(filename.encode()).hexdigest()
    temp_delta_path = f"temp_deltas_{file_hash}.tmp"
    temp_pattern_path = f"temp_pattern_{file_hash}.npy"
    drift_log_path = f"temp_drift_{file_hash}.csv"
    
    result = None
    try:
        scorer = PirouetteScorerV4(grid_size=grid_size, flips=total_flips, amplitude=amplitude)

        if not os.path.exists(temp_pattern_path):
            print(f"[Worker] Pattern file not found. Creating for {filename}...")
            status = create_pattern_file(archive_path, item['member_name'], grid_size, chunk_size, temp_pattern_path)
            if status is None:
                result = {"file": filename, "category": "empty", "status": "complete"}

        if result is None:
            completed_flips = sum(1 for _ in open(temp_delta_path)) if os.path.exists(temp_delta_path) else 0
            if completed_flips >= total_flips:
                print(f"[Worker] Finalizing score for {filename}...")
                vel, rad, kurtosis_val = scorer.calculate_stats_from_file(temp_delta_path)
                drift = calculate_drift_score(drift_log_path)
                anisotropy = calculate_anisotropy_score(temp_pattern_path)
                result = {"file": filename, "category": item['category'], "velcridance_score": vel, "radiance_score": rad, "kurtosis_score": kurtosis_val, "drift_score": drift, "anisotropy_score": anisotropy, "text_length": 0, "status": "complete"}
            else:
                print(f"[Worker] Running batch for {filename}. Progress: {completed_flips}/{total_flips}")
                scorer.run_simulation_batch(temp_pattern_path, filename, temp_delta_path, drift_log_path, completed_flips, batch_size)
                result = {"file": filename, "status": "in_progress"}

    except Exception as e:
        print(f"--- ✗ [Worker] UNHANDLED EXCEPTION for file: {filename} ---")
        print(f"    Error Type: {type(e).__name__}, Message: {e}")
        result = {"file": filename, "category": "error", "status": "complete"}
    finally:
        if result:
            result_queue.put(result)
        # Clean up memory
        del scorer
        gc.collect()
        print(f"--- [Worker] Finished work for: {filename} ---")

# --- Main Execution Block ---
def main():
    # --- ⚙️ CONFIGURATION ---
    config = {
        'grid_size': 64,
        'total_flips': 4096,
        'amplitude': 0.1,
        'chunk_size': 16384,
        'batch_size': 200,
        'archive_path': "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment/txt-files.tar/txt-files.tar", # <--- CHANGE THIS
        'results_csv': "vr_analysis_results_from_tar.csv"
    }

    # --- Load manifest ---
    manifest = []
    if os.path.exists(config['archive_path']):
        print(f"--- Tar archive found. Building manifest... ---")
        with tarfile.open(config['archive_path'], 'r') as tar_handle:
            for member in tar_handle.getmembers():
                if member.isfile() and member.name.lower().endswith('.txt'):
                    manifest.append({'member_name': member.name, 'category': 'gutenberg_tar'})
        print(f"[PREP] ✓ Manifest created with {len(manifest)} text files.")
    else:
        print(f"--- Tar archive not found at '{config['archive_path']}'. Exiting. ---")
        return

    # --- Main Loop ---
    result_queue = multiprocessing.Queue()
    
    try:
        while True:
            completed_files = set(pd.read_csv(config['results_csv'])['file'].unique()) if os.path.exists(config['results_csv']) else set()
            print(f"\n--- Main Loop --- Completed: {len(completed_files)}/{len(manifest)}")

            if len(completed_files) >= len(manifest):
                print("\n--- ✅ All files have been processed or attempted! ---")
                break

            found_work = False
            for item in manifest:
                filename = os.path.basename(item['member_name'])
                if filename in completed_files:
                    continue
                
                # Found a file to process
                found_work = True
                p = multiprocessing.Process(target=process_file, args=(item, config, result_queue))
                p.start()
                p.join() # Wait for the current file to finish before starting the next

                # Process results from the queue
                while not result_queue.empty():
                    res = result_queue.get()
                    if res['status'] == 'complete':
                        # Clean up temp files for completed/errored files
                        file_hash = hashlib.md5(res['file'].encode()).hexdigest()
                        for temp_file in [f"temp_deltas_{file_hash}.tmp", f"temp_pattern_{file_hash}.npy", f"temp_drift_{file_hash}.csv"]:
                            if os.path.exists(temp_file):
                                os.remove(temp_file)
                        
                        # Log final result
                        res.pop('status', None) # Remove status before logging
                        file_exists = os.path.isfile(config['results_csv'])
                        with open(config['results_csv'], 'a', newline='', encoding='utf-8') as f:
                            writer = csv.DictWriter(f, fieldnames=res.keys())
                            if not file_exists: writer.writeheader()
                            writer.writerow(res)
                break # Break to re-evaluate completed files list

            if not found_work:
                print("\n--- No new work found in a full pass. Shutting down. ---")
                break
            
            # Brief pause to prevent runaway loops on error
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n--- 🛑 User interrupted process. Shutting down. ---")
    finally:
        print("--- Script finished. ---")


if __name__ == '__main__':
    multiprocessing.freeze_support() # For Windows compatibility
    main()