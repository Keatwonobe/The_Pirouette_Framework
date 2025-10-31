#!/usr/bin/env python3
import zlib
import os
import numpy as np
import pandas as pd
from tqdm import tqdm

# --- Constants and Core Functions ---

KI_REST = 4.14159
KI_MOTION = 4.18879
AMINO_ACID_ALPHABET = "ACDEFGHIKLMNPQRSTVWYBZXUO"
AMINO_ACID_MAP = {char: i for i, char in enumerate(AMINO_ACID_ALPHABET)}

def get_rate_distortion(data):
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
    if len(rates) < 2 or len(distortions) < 2: return 0
    valid_points = np.array(distortions) > 0
    if np.sum(valid_points) < 2: return 0
    log_rates = np.log(np.array(rates)[valid_points])
    log_inv_distortions = np.log(1 / np.array(distortions)[valid_points])
    try:
        D = np.polyfit(log_inv_distortions, log_rates, 1)[0]
    except (np.linalg.LinAlgError, ValueError): D = 0
    return D if np.isfinite(D) else 0

def parse_protein_fasta(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        header, parts = None, []
        for line in f:
            if line.startswith('>'):
                if header and 'mol:protein' in header: yield header, "".join(parts)
                header, parts = line[1:].strip(), []
            else:
                parts.append(line.strip().upper())
        if header and 'mol:protein' in header: yield header, "".join(parts)

# --- Main Logic with Batching and Checkpointing ---

def generate_raw_data(fasta_file, raw_csv_file, chk_file, batch_size=1000):
    """
    Step 1: Process the FASTA file in batches, calculating fractal dimension
    and saving progress to a checkpoint file.
    """
    resume_idx = 0
    if os.path.exists(chk_file):
        try:
            with open(chk_file, 'r') as f:
                resume_idx = int(f.read().strip())
            print(f"Checkpoint found. Resuming from protein index {resume_idx:,}.")
        except (ValueError, FileNotFoundError):
            resume_idx = 0
    
    # If resuming, we append. Otherwise, we write a new file.
    # The header is only written if the file doesn't exist yet.
    file_exists = os.path.exists(raw_csv_file)
    if resume_idx == 0 and file_exists:
        os.remove(raw_csv_file) # Start fresh if not resuming
        file_exists = False

    batch_results = []
    
    # Use enumerate to track the overall index for checkpointing
    protein_generator = parse_protein_fasta(fasta_file)
    with tqdm(initial=resume_idx, desc="Step 1: Generating Raw Data") as pbar:
        for idx, (header, sequence) in enumerate(protein_generator):
            pbar.update(1)
            if idx < resume_idx:
                continue

            # --- Core calculation per protein ---
            numerical_sequence = np.array([AMINO_ACID_MAP.get(char, -1) for char in sequence], dtype=np.int8)
            if len(numerical_sequence) < 50: continue
            rates, distortions = get_rate_distortion(numerical_sequence)
            dimension = analyze_power_law_fit(rates, distortions)
            if dimension > 0:
                batch_results.append({
                    'header': header.split()[0],
                    'fractal_dimension': dimension,
                    'length': len(sequence)
                })

            # --- Write to CSV and checkpoint when batch is full ---
            if len(batch_results) >= batch_size:
                df_batch = pd.DataFrame(batch_results)
                # Append to CSV, only write header if the file is new
                df_batch.to_csv(raw_csv_file, mode='a', header=not file_exists, index=False)
                file_exists = True # Header has been written
                batch_results.clear() # Free up memory
                
                # Update checkpoint
                with open(chk_file, 'w') as f:
                    f.write(str(idx + 1))

    # --- Save any remaining results from the last batch ---
    if batch_results:
        df_batch = pd.DataFrame(batch_results)
        df_batch.to_csv(raw_csv_file, mode='a', header=not file_exists, index=False)

    print("Step 1 complete. Raw data saved.")


def analyze_final_results(raw_csv_file, final_report_file):
    """
    Step 2: Read the complete raw data file, perform statistical analysis,
    and save the final report.
    """
    print("\nStarting Step 2: Final Statistical Analysis...")
    if not os.path.exists(raw_csv_file):
        print(f"Error: Raw data file '{raw_csv_file}' not found. Cannot perform analysis.")
        return

    df = pd.read_csv(raw_csv_file)
    
    d_mean = df['fractal_dimension'].mean()
    d_std = df['fractal_dimension'].std()

    print(f"Analysis Complete. Found {len(df):,} proteins.")
    print(f"Mean Fractal Dimension (D): {d_mean:.4f}")
    print(f"Std Dev of Fractal Dimension: {d_std:.4f}")

    df['D_z_score'] = (df['fractal_dimension'] - d_mean) / d_std

    tolerance = 0.1
    rest_matches = df[np.abs(df['D_z_score'] - KI_REST) < tolerance]
    motion_matches = df[np.abs(df['D_z_score'] - KI_MOTION) < tolerance]

    print("\n--- Potential Ki Matches Found ---")
    if not rest_matches.empty:
        print(f"\nFound {len(rest_matches)} matches for Ki_Rest (~{KI_REST:.4f}):")
        print(rest_matches[['header', 'D_z_score', 'fractal_dimension', 'length']].to_string(index=False))
    else: print(f"\nNo matches found for Ki_Rest within tolerance {tolerance}.")
        
    if not motion_matches.empty:
        print(f"\nFound {len(motion_matches)} matches for Ki_Motion (~{KI_MOTION:.4f}):")
        print(motion_matches[['header', 'D_z_score', 'fractal_dimension', 'length']].to_string(index=False))
    else: print(f"\nNo matches found for Ki_Motion within tolerance {tolerance}.")
        
    df.to_csv(final_report_file, index=False, float_format='%.6f')
    print(f"\n✅ Final analysis report saved to '{final_report_file}'")

if __name__ == '__main__':
    FASTA_FILENAME = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Finding_Ki/proteins/pdb_seqres.txt"
    RAW_CSV = "protein_fractal_dimensions_raw.csv"
    CHECKPOINT_FILE = "protein_ki.chk"
    FINAL_REPORT_CSV = "protein_ki_final_report.csv"

    try:
        # Run Step 1
        generate_raw_data(FASTA_FILENAME, RAW_CSV, CHECKPOINT_FILE)
        # Run Step 2
        analyze_final_results(RAW_CSV, FINAL_REPORT_CSV)
    except FileNotFoundError:
        print(f"\nERROR: The file '{FASTA_FILENAME}' was not found.")
        print("Please update the FASTA_FILENAME variable in the script.")