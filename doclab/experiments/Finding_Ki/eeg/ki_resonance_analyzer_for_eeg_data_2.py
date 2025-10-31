#!/usr/bin/env python3
import zlib
import os
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import warnings
from scipy.stats import kurtosis

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
    Step 1: Crawls through EEG CSV files, calculates multiple metrics
    for each channel, and saves progress with checkpointing.
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
                df = pd.read_csv(filepath, header=None)
                
                for channel_idx, channel_data in df.items():
                    signal = channel_data.dropna().to_numpy()
                    
                    if len(signal) < 256:
                        continue

                    # Metric 1: Fractal Dimension of the raw signal
                    rates, distortions = get_rate_distortion(signal)
                    dimension = analyze_power_law_fit(rates, distortions)
                    
                    # Metric 2 & 3: Deltas (Volatility) and Kurtosis of Deltas
                    if len(signal) > 1:
                        deltas = np.diff(signal)
                        delta_std_dev = np.std(deltas)
                        # Use fisher=False for standard kurtosis (3.0 is normal)
                        delta_kurtosis = kurtosis(deltas, fisher=False) 
                    else:
                        delta_std_dev = 0.0
                        delta_kurtosis = 0.0

                    if dimension > 0:
                        batch_results.append({
                            'subject_file': filepath.name,
                            'channel': f'ch_{channel_idx}',
                            'fractal_dimension': dimension,
                            'delta_std_dev': delta_std_dev,
                            'delta_kurtosis': delta_kurtosis,
                            'signal_length': len(signal)
                        })

                if len(batch_results) >= (batch_size * len(df.columns)): # Write after a few full files
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
    Step 2: Read the complete raw data, calculate z-scores for all metrics,
    and save the final report identifying Ki-resonant EEG channels.
    """
    print("\nStarting Step 2: Final Statistical Analysis...")
    if not os.path.exists(raw_csv_file):
        print(f"Error: Raw data file '{raw_csv_file}' not found.")
        return

    df = pd.read_csv(raw_csv_file)
    
    metrics_to_analyze = ['fractal_dimension', 'delta_std_dev', 'delta_kurtosis']
    
    print(f"\nAnalysis Complete. Analyzed {len(df):,} total channels.")
    
    for metric in metrics_to_analyze:
        d_mean = df[metric].mean()
        d_std = df[metric].std()
        print(f"  - Metric '{metric}': Mean={d_mean:.4f}, StdDev={d_std:.4f}")
        df[f'zscore_{metric}'] = (df[metric] - d_mean) / d_std

    print("\n--- Potential Ki Matches Found ---")
    
    for metric in metrics_to_analyze:
        zscore_col = f'zscore_{metric}'
        
        rest_matches = df[np.abs(df[zscore_col] - KI_REST) < 0.1].sort_values(zscore_col, ascending=False)
        motion_matches = df[np.abs(df[zscore_col] - KI_MOTION) < 0.1].sort_values(zscore_col, ascending=False)

        if not rest_matches.empty:
            print(f"\nFound {len(rest_matches)} matches for Ki_Rest (~{KI_REST:.4f}) in METRIC: '{metric}'")
            print(rest_matches[['subject_file', 'channel', metric, zscore_col]].to_string(index=False))
        
        if not motion_matches.empty:
            print(f"\nFound {len(motion_matches)} matches for Ki_Motion (~{KI_MOTION:.4f}) in METRIC: '{metric}'")
            print(motion_matches[['subject_file', 'channel', metric, zscore_col]].to_string(index=False))

    df.to_csv(final_report_file, index=False, float_format='%.6f')
    print(f"\n✅ Final analysis report with all z-scores saved to '{final_report_file}'")

if __name__ == '__main__':
    # --- Configuration ---
    DATASET_DIRECTORY = "C:/Users/keatw/.cache/kagglehub/datasets/amananandrai/complete-eeg-dataset/versions/1"
    
    RAW_CSV = "eeg_multi_metric_raw.csv"
    CHECKPOINT_FILE = "eeg_multi_ki.chk"
    FINAL_REPORT_CSV = "eeg_multi_ki_final_report.csv"

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
