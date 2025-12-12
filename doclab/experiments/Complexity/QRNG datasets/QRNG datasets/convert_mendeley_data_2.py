import pandas as pd
import numpy as np
import datetime

def generate_ablation_files(input_csv, n_values=10000, n_bins=69):
    """
    Reads the raw voltage data from the Mendeley dataset (FIG2a.csv)
    and generates four different normalized versions for ablation analysis.
    
    This is a one-time conversion script.
    """
    print(f"--- Starting Ablation Analysis Data Generation ---")
    print(f"Reading {input_csv}...")
    
    try:
        # 1. Load the raw time series data
        df = pd.read_csv(input_csv)
        
        # 2. Get the voltage column (the raw random data)
        if 'CH1 mV' not in df.columns:
            print(f"Error: Column 'CH1 mV' not found in {input_csv}.")
            print(f"Available columns: {df.columns.tolist()}")
            return
            
        voltages_series = df['CH1 mV']
        voltages_np = voltages_series.to_numpy()
        print(f"  Loaded {len(voltages_series)} voltage readings.")

        # --- Baseline (Quantile Binning) ---
        print("  Generating 1: Baseline (Quantile Binning)...")
        binned_data = pd.qcut(voltages_series, q=n_bins, labels=False, duplicates='drop')
        x_quantile = (binned_data + 1).iloc[:n_values]
        output_file_1 = "mendeley_qrng_quantile.txt"
        np.savetxt(output_file_1, x_quantile, fmt='%d')
        print(f"    > Saved {output_file_1}")

        # --- Ablation 1 (Uniform Binning) ---
        print("  Generating 2: Ablation (Uniform Binning)...")
        v_norm = (voltages_np - voltages_np.min()) / (voltages_np.max() - voltages_np.min() + 1e-12)
        x_uniform = (v_norm * n_bins).astype(int).clip(0, n_bins - 1) + 1
        x_uniform_final = x_uniform[:n_values]
        output_file_2 = "mendeley_qrng_uniform.txt"
        np.savetxt(output_file_2, x_uniform_final, fmt='%d')
        print(f"    > Saved {output_file_2}")

        # --- Ablation 2 (Shuffle) ---
        print("  Generating 3: Ablation (Shuffled Baseline)...")
        x_shuffled = np.random.permutation(x_quantile.to_numpy())
        output_file_3 = "mendeley_qrng_shuffled.txt"
        np.savetxt(output_file_3, x_shuffled, fmt='%d')
        print(f"    > Saved {output_file_3}")

        # --- Ablation 3 (High-Pass Filter then Quantile) ---
        print("  Generating 4: Ablation (High-Pass Filter)...")
        v_hp = voltages_np - pd.Series(voltages_np).rolling(256, min_periods=1).mean().to_numpy()
        # Now quantize the high-passed signal
        binned_hp = pd.qcut(pd.Series(v_hp), q=n_bins, labels=False, duplicates='drop')
        x_highpass = (binned_hp + 1).iloc[:n_values]
        output_file_4 = "mendeley_qrng_highpass.txt"
        np.savetxt(output_file_4, x_highpass, fmt='%d')
        print(f"    > Saved {output_file_4}")

        print("\nSuccess! All 4 ablation files generated.")

    except FileNotFoundError:
        print(f"Error: Input file not found: {input_csv}")
        print("Please make sure 'FIG2a.csv' is in the same directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    INPUT_FILE = "FIG2a.csv"
    N_VALUES = 10000
    
    print("--- Mendeley QRNG Ablation Data Generator ---")
    print(f"This script will read '{INPUT_FILE}' and create 4 analysis files.")
    
    generate_ablation_files(INPUT_FILE, n_values=N_VALUES)

