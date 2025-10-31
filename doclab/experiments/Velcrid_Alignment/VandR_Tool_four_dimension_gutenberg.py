import os
import sys
import re
import csv
import shutil
import hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from scipy.stats import kurtosis
from bs4 import BeautifulSoup
import statsmodels.api as sm
from statsmodels.formula.api import ols
import tarfile
import io
import zipfile

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
        """Calculates mean, std dev, and kurtosis from the delta file."""
        print(f"[FINALIZE] Calculating full stats from {os.path.basename(temp_file_path)}...")

        # Read all deltas into memory for kurtosis calculation
        with open(temp_file_path, 'r') as f:
            deltas = [float(line) for line in f]

        if not deltas:
            return 0.0, 0.0, 0.0

        # Use numpy for efficient calculation
        delta_array = np.array(deltas, dtype=np.float64)
        mean_val = np.mean(delta_array)
        std_val = np.std(delta_array)
        # Use 'fisher=False' for the standard definition of kurtosis (3.0 is normal)
        kurtosis_val = kurtosis(delta_array, fisher=False)

        print(f"[FINALIZE]  ✓ Stats: μ={mean_val:.4e}, σ={std_val:.4e}, Kᵢ={kurtosis_val:.4f}")
        return mean_val, std_val, kurtosis_val

    # AFTER
    def run_simulation_batch(self, pattern_path: str, title: str, temp_delta_path: str, drift_log_path: str, completed_flips: int, batch_size: int):
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
        batch_deltas = [] # Store deltas for this batch only
        with open(temp_delta_path, 'a') as f:
            for i, bit_index in enumerate(flips_to_run):
                variant = flat_pattern_base.copy()
                variant[bit_index] = 1 - variant[bit_index]
                flipped_power = self.engine.run_simulation(variant.reshape(base_pattern.shape))
                delta = np.abs(flipped_power - base_power)
                f.write(f"{delta}\n")
                batch_deltas.append(delta)
        
            # --- New Drift Calculation Logic ---
            if batch_deltas:
                batch_mean = np.mean(np.array(batch_deltas, dtype=np.float64))
                # Log the number of flips *at the end* of this batch and the batch mean
                flips_at_batch_end = completed_flips + len(batch_deltas)
                with open(drift_log_path, 'a', newline='') as df:
                    writer = csv.writer(df)
                    writer.writerow([flips_at_batch_end, batch_mean])
                print(f"[DRIFT LOG]  ✓ Logged batch mean {batch_mean:.4e} at flip {flips_at_batch_end}.")

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

def get_content_chunks_from_tar(tar_handle, member_name: str, chunk_size=8192):
    """Yields chunks of text for a single file directly from an open tar archive."""
    try:
        # Extract the file into an in-memory bytes buffer
        extracted_file = tar_handle.extractfile(member_name)
        if extracted_file:
            # Wrap the bytes buffer in a text reader
            # Use errors='ignore' for robustness against encoding issues
            with io.TextIOWrapper(extracted_file, encoding='utf-8', errors='ignore') as text_reader:
                content = strip_gutenberg_headers(text_reader.read())
                # Yield the cleaned content in chunks
                for i in range(0, len(content), chunk_size):
                    yield content[i:i+chunk_size]
    except KeyError:
        print(f"  ✗ ERROR: Member '{member_name}' not found in the tar archive.")
    except Exception as e:
        print(f"  ✗ ERROR during tar extraction for {member_name}: {e}")

def text_to_binary_image(text, grid_size):
    """Converts a string of text into a binary image grid."""
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
    target_size = grid_size * grid_size
    if binary_array.size < target_size:
        binary_array = np.pad(binary_array, (0, target_size - binary_array.size), 'constant')
    else:
        binary_array = binary_array[:target_size]
    return binary_array.reshape((grid_size, grid_size))

def count_lines(path: str) -> int:
    if not os.path.exists(path): return 0
    with open(path, 'r') as f:
        return sum(1 for _ in f)

def create_pattern_file(text_iterator_factory, grid_size, output_path):
    """
    Reads text chunks and saves a composite pattern to a .npy file.
    Returns True on success, False on failure, and None if the source is empty.
    """
    print(f"[PREP] Creating pattern file for {os.path.basename(output_path)}...")
    composite_pattern = np.zeros((grid_size, grid_size), dtype=np.float32)
    chunk_count = 0
    try:
        for text_chunk in text_iterator_factory():
            composite_pattern += text_to_binary_image(text_chunk, grid_size)
            chunk_count += 1
    except Exception as e:
        print(f"[PREP]  ✗ Error during text_to_binary_image conversion: {e}")
        return False # Indicates a processing failure

    if chunk_count > 0:
        final_pattern = composite_pattern / chunk_count
        np.save(output_path, final_pattern)
        print(f"[PREP]  ✓ Saved pattern to {os.path.basename(output_path)}")
        return True # Indicates success
    else:
        # This is the crucial new part: handle empty files.
        print(f"[PREP]  ✗ No content found after processing. The file is likely empty.")
        return None # Indicates the source file was empty

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

def calculate_drift_score(drift_log_path):
    """Calculates the slope of the running mean from the drift log file."""
    if not os.path.exists(drift_log_path): return 0.0
    
    # Read the CSV log of batch means
    data = pd.read_csv(drift_log_path, header=None, names=['flip_count', 'batch_mean'])
    if len(data) < 2: return 0.0 # Need at least two points to define a slope
    
    # Perform linear regression to find the slope
    slope = np.polyfit(data['flip_count'], data['batch_mean'], 1)[0]
    print(f"[FINALIZE]  ✓ Drift Score (∂μ/∂flips): {slope:.4e}")
    return slope

def calculate_anisotropy_score(pattern_path):
    """Calculates the average anisotropy from the potential field defined by the pattern."""
    if not os.path.exists(pattern_path): return 0.0

    pattern = np.load(pattern_path)
    
    # Calculate the gradient (first derivative)
    gy, gx = np.gradient(pattern)
    
    # Calculate the components of the Hessian matrix (second derivatives)
    gxy, gxx = np.gradient(gx)
    gyy, gyx = np.gradient(gy)
    
    # Average the mixed derivatives for a symmetric Hessian
    H_xy = (gxy + gyx) / 2.0
    
    # Vectorized calculation of eigenvalue differences across the entire grid
    trace = gxx + gyy
    determinant = gxx * gyy - H_xy**2
    
    # The difference between eigenvalues is sqrt(trace^2 - 4*determinant)
    # Use np.maximum to prevent taking the square root of a small negative number from float error
    eigenvalue_diff = np.sqrt(np.maximum(0, trace**2 - 4 * determinant))
    
    # Summarize anisotropy across the grid by taking the mean
    anisotropy_score = np.mean(eigenvalue_diff)
    print(f"[FINALIZE]  ✓ Anisotropy Score: {anisotropy_score:.4e}")
    return anisotropy_score
# --- Main Execution Block with Checkpointing Logic ---
if __name__ == '__main__':
    # --- ⚙️ CONFIGURATION ---
    GRID_SIZE = 64
    TOTAL_FLIPS = 4096
    AMPLITUDE = 0.1
    CHUNK_SIZE = 16384
    BATCH_SIZE = 200

    # --- 📂 FOLDER & FILE SETUP ---
    BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
    RESULTS_CSV = "vr_analysis_results_from_tar.csv"
    ZIP_ARCHIVE_PATH = os.path.join(BASE_DIR, "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment/txt-files.tar.zip")

    # --- Initialize scorer ---
    scorer = PirouetteScorerV4(grid_size=GRID_SIZE, flips=TOTAL_FLIPS, amplitude=AMPLITUDE)

    # --- 🔁 MASTER LOGIC: Prioritize Tarball ---
    manifest = []
    use_tar_mode = False

    if os.path.exists(ZIP_ARCHIVE_PATH):
        print("--- Nested tar.zip archive found. Operating in streaming mode. ---")
        try:
            # Open the outer .zip file
            zip_handle = zipfile.ZipFile(ZIP_ARCHIVE_PATH, 'r')
            
            # Find the .tar file member within the zip archive
            tar_member_name = next((name for name in zip_handle.namelist() if name.endswith('.tar')), None)

            if not tar_member_name:
                raise FileNotFoundError("No .tar file found inside the zip archive.")
            
            print(f"[STREAM] Opening '{tar_member_name}' from within the zip file...")
            
            # Open the inner tar file as an in-memory stream
            tar_stream = zip_handle.open(tar_member_name, 'r')
            
            # Pass the in-memory stream to tarfile.open()
            tar_handle = tarfile.open(fileobj=tar_stream, mode='r')
            
            # Build the manifest directly from the open tar handle
            for member in tar_handle.getmembers():
                if member.isfile() and member.name.endswith('.txt'):
                    manifest.append({'member_name': member.name, 'category': 'gutenberg_tar'})
            
            print(f"[STREAM]  ✓ Manifest created with {len(manifest)} text files.")
        except Exception as e:
            print(f"FATAL ERROR: Could not process the archive: {e}")
            if 'tar_handle' in locals() and tar_handle: tar_handle.close()
            if 'zip_handle' in locals() and zip_handle: zip_handle.close()
            sys.exit(1) # Exit if we can't build the manifest

    else:
        print("--- No tarball found. Operating in FOLDER mode. ---")
        # Fallback to the old directory scanning method
        for dir_path, category in [(os.path.join(BASE_DIR, "radiant"), "radiant"), (os.path.join(BASE_DIR, "velcrid"), "velcrid")]:
            if not os.path.isdir(dir_path): continue
            for f in os.listdir(dir_path):
                if f.lower().endswith(('.txt', '.html')):
                    manifest.append({'path': os.path.join(dir_path, f), 'category': category})

    # --- AUTO-RUNNER LOOP ---
    tar_handle = None
    if use_tar_mode:
        # Keep the tar file open for the duration of the script
        tar_handle = tarfile.open(ZIP_ARCHIVE_PATH, 'r')

    while True:
        completed_files = load_completed_files(RESULTS_CSV)

        if len(manifest) == len(completed_files):
            print("\n--- ✅ All files have been processed and finalized! Shutting down. ---")
            break

        work_done_this_pass = False
        for item in manifest:
            # Adapt variables based on mode
            filename = os.path.basename(item['member_name'] if use_tar_mode else item['path'])
            category = item['category']

            if filename in completed_files:
                continue

            print(f"\n--- Checking work for: {filename} ---")
            file_hash = hashlib.md5(filename.encode()).hexdigest()
            temp_delta_path = f"temp_deltas_{file_hash}.tmp"
            temp_pattern_path = f"temp_pattern_{file_hash}.npy"
            drift_log_path = f"temp_drift_{file_hash}.csv"

            if not os.path.exists(temp_pattern_path):
                print(f"[PREP] Pattern file not found. Creating it now...")
                if use_tar_mode:
                    member_name = item['member_name']
                    content_iterator_factory = lambda: get_content_chunks_from_tar(tar_handle, member_name, CHUNK_SIZE)
                else:
                    file_path = item['path']
                    content_iterator_factory = lambda: get_content_chunks(file_path, CHUNK_SIZE)
                
                status = create_pattern_file(content_iterator_factory, GRID_SIZE, temp_pattern_path)
                if status is None:
                    print(f"[CLEANUP] Skipping empty or invalid file '{filename}'.")
                    # For tar mode, we can't move the file, so we just log it as "complete" to skip it
                    append_to_csv({"file": filename, "category": "empty"}, RESULTS_CSV)

                work_done_this_pass = True
                break

            completed_flips = count_lines(temp_delta_path)

            if completed_flips >= TOTAL_FLIPS:
                print(f"[FINALIZE] All {TOTAL_FLIPS} flips are complete. Finalizing score...")
                vel, rad, kurtosis = scorer.calculate_stats_from_file(temp_delta_path)
                drift = calculate_drift_score(drift_log_path)
                anisotropy = calculate_anisotropy_score(temp_pattern_path)
                
                # We don't calculate text_len in tar mode to save time, can be set to 0
                result = {
                    "file": filename, "category": category, "velcridance_score": vel, 
                    "radiance_score": rad, "kurtosis_score": kurtosis, "drift_score": drift,
                    "anisotropy_score": anisotropy, "text_length": 0
                }
                
                append_to_csv(result, RESULTS_CSV)
                print(f"[FINALIZE]  ✓ All scores logged.")
                
                for temp_file in [temp_delta_path, temp_pattern_path, drift_log_path]:
                    if os.path.exists(temp_file): os.remove(temp_file)
                print(f"[FINALIZE]  ✓ All temporary files removed.")
                
                if not use_tar_mode: move_to_processed(item['path'])
                work_done_this_pass = True
                break
            else:
                print(f"[WORK] Progress: {completed_flips}/{TOTAL_FLIPS}. Starting new batch.")
                scorer.run_simulation_batch(temp_pattern_path, filename, temp_delta_path, drift_log_path, completed_flips, BATCH_SIZE)
                work_done_this_pass = True
                break

        if not work_done_this_pass:
            print("\n--- No new work found in a full pass. Shutting down. ---")
            break
    
    if tar_handle:
        tar_handle.close()