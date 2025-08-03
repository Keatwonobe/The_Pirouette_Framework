#!/usr/bin/env python3
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

# --- Core Fractal Dimension Functions (from previous script) ---

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
    if len(rates) < 2 or len(distortions) < 2: return 0
    valid_points = np.array(distortions) > 0
    if np.sum(valid_points) < 2: return 0
    log_rates = np.log(np.array(rates)[valid_points])
    log_inv_distortions = np.log(1 / np.array(distortions)[valid_points])
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', np.RankWarning)
            D = np.polyfit(log_inv_distortions, log_rates, 1)[0]
    except (np.linalg.LinAlgError, ValueError): D = 0
    return D if np.isfinite(D) else 0

# --- Main Logic with Batching and Checkpointing ---

def generate_raw_data(data_directory, raw_csv_file, chk_file, batch_size=1000):
    """
    Step 1: Crawls through stock/ETF directories, calculates fractal dimension
    for each, and saves progress with checkpointing.
    Returns True if data was successfully generated, False otherwise.
    """
    print(f"Searching for stock/ETF files in '{data_directory}'...")
    all_files = list(Path(data_directory).glob('**/*.us.txt'))
    print(f"Found {len(all_files):,} total files to process.")

    resume_idx = 0
    if os.path.exists(chk_file):
        try:
            with open(chk_file, 'r') as f:
                resume_idx = int(f.read().strip())
            print(f"Checkpoint found. Resuming from file index {resume_idx:,}.")
        except (ValueError, FileNotFoundError):
            resume_idx = 0
    
    file_exists = os.path.exists(raw_csv_file)
    if resume_idx == 0 and file_exists:
        os.remove(raw_csv_file)
        file_exists = False

    batch_results = []
    # --- ADDED: Counters for tracking skipped files ---
    files_processed_successfully = 0
    files_skipped_short = 0
    files_skipped_novolatility = 0
    files_skipped_badfit = 0
    
    files_to_process = all_files[resume_idx:]
    
    with tqdm(total=len(all_files), initial=resume_idx, desc="Step 1: Generating Raw Data") as pbar:
        for i, filepath in enumerate(files_to_process):
            current_idx = resume_idx + i
            try:
                df = pd.read_csv(filepath)
                
                if 'High' not in df.columns or 'Low' not in df.columns or len(df) < 252:
                    files_skipped_short += 1
                    continue

                volatility_signal = (df['High'] - df['Low']).to_numpy()
                volatility_signal = volatility_signal[np.isfinite(volatility_signal) & (volatility_signal > 0)]
                
                if len(volatility_signal) < 50:
                    files_skipped_novolatility += 1
                    continue

                rates, distortions = get_rate_distortion(volatility_signal)
                dimension = analyze_power_law_fit(rates, distortions)
                
                if dimension > 0:
                    files_processed_successfully += 1
                    batch_results.append({
                        'ticker': filepath.stem,
                        'type': filepath.parent.name,
                        'fractal_dimension': dimension,
                        'data_points': len(df)
                    })
                else:
                    files_skipped_badfit += 1

            except Exception:
                pass
            finally:
                pbar.update(1)

            if len(batch_results) >= batch_size:
                df_batch = pd.DataFrame(batch_results)
                df_batch.to_csv(raw_csv_file, mode='a', header=not file_exists, index=False)
                file_exists = True
                batch_results.clear()
                
                with open(chk_file, 'w') as f:
                    f.write(str(current_idx + 1))

    if batch_results:
        df_batch = pd.DataFrame(batch_results)
        df_batch.to_csv(raw_csv_file, mode='a', header=not file_exists, index=False)

    # --- ADDED: Summary report ---
    print("\n--- Step 1 Summary ---")
    total_scanned = pbar.n - resume_idx
    print(f"Scanned {total_scanned} files in this run.")
    print(f"Successfully processed and included: {files_processed_successfully} files.")
    print(f"Skipped (too short, <252 days): {files_skipped_short} files.")
    print(f"Skipped (insufficient volatility, <50 days): {files_skipped_novolatility} files.")
    print(f"Skipped (bad fractal dimension fit): {files_skipped_badfit} files.")

    if not os.path.exists(raw_csv_file):
        print("\nWarning: No valid data was processed, so no output file was created.")
        return False
    
    return True

def analyze_final_results(raw_csv_file, final_report_file):
    """
    Step 2: Read the complete raw data, perform statistical analysis,
    and save the final report identifying Ki-resonant assets.
    """
    print("\nStarting Step 2: Final Statistical Analysis...")
    if not os.path.exists(raw_csv_file):
        print(f"Error: Raw data file '{raw_csv_file}' not found. Aborting Step 2.")
        return

    df = pd.read_csv(raw_csv_file)
    
    d_mean = df['fractal_dimension'].mean()
    d_std = df['fractal_dimension'].std()

    print(f"\nAnalysis Complete. Analyzed {len(df):,} assets.")
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
    DATASET_DIRECTORY = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/stocks_rightsized/Target"
    
    RAW_CSV = "stock_fractal_dimensions_raw.csv"
    CHECKPOINT_FILE = "stock_ki.chk"
    FINAL_REPORT_CSV = "stock_ki_final_report.csv"

    if DATASET_DIRECTORY == "path/to/your/stock_data":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! PLEASE UPDATE THE 'DATASET_DIRECTORY' VARIABLE   !!!")
        print("!!! in the script to point to your data folder.      !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        try:
            # --- MODIFIED: Check the return value of Step 1 ---
            if generate_raw_data(DATASET_DIRECTORY, RAW_CSV, CHECKPOINT_FILE):
                analyze_final_results(RAW_CSV, FINAL_REPORT_CSV)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
