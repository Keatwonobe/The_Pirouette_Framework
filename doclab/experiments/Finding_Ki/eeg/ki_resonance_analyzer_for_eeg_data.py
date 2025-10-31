import zlib
import os
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import warnings

# --- Constants and Core Functions ---

# Ki constants from your research
KI_REST = 4.14159
KI_MOTION = 4.18879

# --- Core Fractal Dimension Functions (from previous analyses) ---

def get_rate_distortion(data):
    """Calculates rate (compressed size) and distortion (error) for a data sequence."""
    rates, distortions = [], []
    original_data_float = data.astype(np.float32)
    data_min, data_max = original_data_float.min(), original_data_float.max()
    if data_max == data_min: return [1], [0]
    quantization_levels = [2, 4, 8, 16, 32, 64, 128, 256]
    for levels in quantization_levels:
        scaled_data = (original_data_float - data_min) / (data_max - data_min) * (levels - 1)
        quantized_data_int = np.round(scaled_data).astype(np.uint8)
        dequantized_data = data_min + (quantized_data_int.astype(np.float32) / (levels - 1)) * (data_max - data_min)
        distortions.append(np.mean((original_data_float - dequantized_data)**2))
        rates.append(len(zlib.compress(quantized_data_int.tobytes())))
    return rates, distortions

def analyze_power_law_fit(rates, distortions):
    """Fits a power law to the Rate-Distortion curve to find the fractal dimension 'D'."""
    if len(rates) < 2 or len(distortions) < 2: return 0.0
    valid_points = np.array(distortions) > 1e-9 # Use a small epsilon to avoid log(0)
    if np.sum(valid_points) < 2: return 0.0
    log_rates = np.log(np.array(rates)[valid_points])
    log_inv_distortions = np.log(1 / np.array(distortions)[valid_points])
    try:
        with warnings.catch_warnings():
            D = np.polyfit(log_inv_distortions, log_rates, 1)[0]
    except (np.linalg.LinAlgError, ValueError): D = 0.0
    return D if np.isfinite(D) else 0.0

# --- Main Logic with Batching and Checkpointing ---

def generate_raw_data(data_directory, raw_csv_file, chk_file, batch_size=5):
    """
    Step 1: Crawls through EEG CSV files, calculates fractal dimension
    for each channel, and saves progress with checkpointing.
    Returns True if data was successfully generated, False otherwise.
    """
    print(f"Searching for EEG data files in '{data_directory}'...")
    all_files = sorted(list(Path(data_directory).glob('s*.csv')))
    print(f"Found {len(all_files):,} total files to process.")

    last_processed_file = None
    if os.path.exists(chk_file):
        with open(chk_file, 'r') as f:
            last_processed_file = f.read().strip()
        if last_processed_file:
            print(f"Checkpoint found. Resuming after file: {last_processed_file}")
            try:
                resume_idx = [str(f) for f in all_files].index(last_processed_file) + 1
                all_files = all_files[resume_idx:]
                print(f"Skipping {resume_idx} files and resuming...")
            except ValueError:
                print("Checkpoint file not found in list. Starting from scratch.")
    
    file_exists = os.path.exists(raw_csv_file)
    if not last_processed_file and file_exists:
        print("Starting a fresh run. Deleting existing raw data file.")
        os.remove(raw_csv_file)
        file_exists = False

    batch_results = []
    
    with tqdm(total=len(all_files), desc="Step 1: Processing EEG Files") as pbar:
        for filepath in all_files:
            try:
                # Load EEG data, assuming no header
                df = pd.read_csv(filepath, header=None)
                
                # Analyze each column (channel)
                for channel_idx, channel_data in df.items():
                    signal = channel_data.dropna().to_numpy()
                    
                    if len(signal) < 256: # Ensure enough data for analysis
                        continue

                    rates, distortions = get_rate_distortion(signal)
                    dimension = analyze_power_law_fit(rates, distortions)
                    
                    if dimension > 0:
                        batch_results.append({
                            'subject_file': filepath.name,
                            'channel': f'ch_{channel_idx}',
                            'fractal_dimension': dimension,
                            'signal_length': len(signal)
                        })

                # Write batch and update checkpoint
                if len(batch_results) >= batch_size:
                    pd.DataFrame(batch_results).to_csv(raw_csv_file, mode='a', header=not file_exists, index=False)
                    file_exists = True
                    batch_results.clear()
                    
                    with open(chk_file, 'w') as f_chk:
                        f_chk.write(str(filepath))

            except Exception as e:
                print(f"\nWarning: Could not process {filepath.name}. Error: {e}")
            finally:
                pbar.update(1)

    if batch_results:
        pd.DataFrame(batch_results).to_csv(raw_csv_file, mode='a', header=not file_exists, index=False)

    if not os.path.exists(raw_csv_file):
        print("\nWarning: No valid data was processed, so no output file was created.")
        return False
    
    return True

def analyze_final_results(raw_csv_file, final_report_file):
    """
    Step 2: Read the complete raw data, perform statistical analysis,
    and save the final report identifying Ki-resonant EEG channels.
    """
    print("\nStarting Step 2: Final Statistical Analysis...")
    if not os.path.exists(raw_csv_file):
        print(f"Error: Raw data file '{raw_csv_file}' not found.")
        return

    df = pd.read_csv(raw_csv_file)
    
    # Calculate mean and std dev across ALL channels and subjects
    d_mean = df['fractal_dimension'].mean()
    d_std = df['fractal_dimension'].std()

    print(f"\nAnalysis Complete. Analyzed {len(df):,} total channels.")
    print(f"Mean Fractal Dimension (D): {d_mean:.4f}")
    print(f"Std Dev of Fractal Dimension: {d_std:.4f}")

    df['D_z_score'] = (df['fractal_dimension'] - d_mean) / d_std

    tolerance = 0.1
    rest_matches = df[np.abs(df['D_z_score'] - KI_REST) < tolerance].sort_values('D_z_score', ascending=False)
    motion_matches = df[np.abs(df['D_z_score'] - KI_MOTION) < tolerance].sort_values('D_z_score', ascending=False)

    print("\n--- Potential Ki Matches Found ---")
    if not rest_matches.empty:
        print(f"\nFound {len(rest_matches)} matches for Ki_Rest (~{KI_REST:.4f}):")
        print(rest_matches.to_string(index=False))
    else:
        print(f"\nNo matches found for Ki_Rest within tolerance {tolerance}.")
        
    if not motion_matches.empty:
        print(f"\nFound {len(motion_matches)} matches for Ki_Motion (~{KI_MOTION:.4f}):")
        print(motion_matches.to_string(index=False))
    else:
        print(f"\nNo matches found for Ki_Motion within tolerance {tolerance}.")
        
    df.sort_values('D_z_score', ascending=False).to_csv(final_report_file, index=False, float_format='%.6f')
    print(f"\n✅ Final analysis report saved to '{final_report_file}'")

if __name__ == '__main__':
    # --- Configuration ---
    # IMPORTANT: Set this to the path of your directory containing the s00.csv, s01.csv, etc. files.
    DATASET_DIRECTORY = "C:/Users/keatw/.cache/kagglehub/datasets/amananandrai/complete-eeg-dataset/versions/1"
    
    RAW_CSV = "eeg_fractal_dimensions_raw.csv"
    CHECKPOINT_FILE = "eeg_ki.chk"
    FINAL_REPORT_CSV = "eeg_ki_final_report.csv"

    if DATASET_DIRECTORY == "path/to/your/eeg_data":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! PLEASE UPDATE THE 'DATASET_DIRECTORY' VARIABLE   !!!")
        print("!!! in the script to point to your data folder.      !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        try:
            if generate_raw_data(DATASET_DIRECTORY, RAW_CSV, CHECKPOINT_FILE):
                analyze_final_results(RAW_CSV, FINAL_REPORT_CSV)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
