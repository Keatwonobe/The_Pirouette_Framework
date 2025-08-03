#!/usr/bin/env python3
import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import warnings

def preprocess_financial_data(data_directory, output_file, chk_file):
    """
    Crawls stock/ETF data directories, extracts multiple time-series signals from each file,
    and saves them into a single JSON Lines (.jsonl) file.
    
    This script SEPARATES data extraction from analysis. Its only job is to
    create a clean dataset for future analysis scripts to use.
    """
    print(f"Searching for stock/ETF files in '{data_directory}'...")
    all_files = sorted(list(Path(data_directory).glob('**/*.us.txt')))
    print(f"Found {len(all_files):,} total files to process.")

    last_processed_file = None
    if os.path.exists(chk_file):
        with open(chk_file, 'r') as f:
            last_processed_file = f.read().strip()
        if last_processed_file:
            print(f"Checkpoint found. Resuming after file: {last_processed_file}")
            # Find the index to resume from
            try:
                resume_idx = [str(f) for f in all_files].index(last_processed_file) + 1
                all_files = all_files[resume_idx:]
                print(f"Skipping {resume_idx} files and resuming...")
            except ValueError:
                print("Checkpoint file not found in file list. Starting from scratch.")
                last_processed_file = None # Reset if file not found
    
    # If not resuming, we overwrite the output file. Otherwise, we append.
    mode = 'a' if last_processed_file else 'w'

    # --- Counters for tracking skipped files ---
    files_processed = 0
    files_skipped = 0
    
    with open(output_file, mode) as f_out, tqdm(total=len(all_files), desc="Preprocessing financial data") as pbar:
        for filepath in all_files:
            try:
                df = pd.read_csv(filepath)
                
                # Basic validation: must have enough data and the right columns
                if len(df) < 252 or not {'Date', 'Close', 'High', 'Low', 'Volume'}.issubset(df.columns):
                    files_skipped += 1
                    continue

                # --- Signal Extraction ---
                
                # 1. Daily Return (Percentage Change)
                daily_return = df['Close'].pct_change().dropna().tolist()

                # 2. Volatility (High - Low Range)
                volatility = (df['High'] - df['Low']).dropna().tolist()

                # 3. Normalized Volume (Volume / 90-day Moving Average)
                # This highlights unusual trading activity relative to recent history.
                volume_ma = df['Volume'].rolling(window=90, min_periods=1).mean()
                # Replace 0s in moving average to avoid division by zero, then calculate ratio
                normalized_volume = (df['Volume'] / volume_ma.replace(0, 1)).dropna().tolist()

                # --- Construct the JSON object for this asset ---
                asset_data = {
                    'ticker': filepath.stem,
                    'type': filepath.parent.name,
                    'data_points': len(df),
                    'signals': {
                        'daily_return': daily_return,
                        'volatility': volatility,
                        'normalized_volume': normalized_volume
                    }
                }
                
                # Write the JSON object as a single line in the output file
                f_out.write(json.dumps(asset_data) + '\n')
                files_processed += 1

            except Exception as e:
                # Catch errors from corrupted files, etc.
                files_skipped += 1
            finally:
                pbar.update(1)
                # Update checkpoint with the name of the last file attempted
                with open(chk_file, 'w') as f_chk:
                    f_chk.write(str(filepath))

    print("\n--- Preprocessing Summary ---")
    print(f"Successfully processed and saved: {files_processed} files.")
    print(f"Skipped (due to insufficient data or errors): {files_skipped} files.")
    print(f"✅ Preprocessed dataset saved to '{output_file}'")


if __name__ == '__main__':
    # --- Configuration ---
    DATASET_DIRECTORY = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/stocks_rightsized/Target"
    
    # The output is a .jsonl file, where each line is a complete JSON object.
    PREPROCESSED_OUTPUT_FILE = "preprocessed_stock_data.jsonl"
    CHECKPOINT_FILE = "stock_preprocessor.chk"

    if DATASET_DIRECTORY == "path/to/your/stock_data":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! PLEASE UPDATE THE 'DATASET_DIRECTORY' VARIABLE   !!!")
        print("!!! in the script to point to your data folder.      !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        try:
            preprocess_financial_data(DATASET_DIRECTORY, PREPROCESSED_OUTPUT_FILE, CHECKPOINT_FILE)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
