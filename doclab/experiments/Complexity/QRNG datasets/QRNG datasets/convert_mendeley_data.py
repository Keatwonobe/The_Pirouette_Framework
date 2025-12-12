import pandas as pd
import numpy as np
import datetime

def convert_mendeley_to_qrng(input_csv, output_txt, n_values=10000, n_bins=69):
    """
    Reads the raw voltage data from the Mendeley dataset (FIG2a.csv),
    normalizes it using quantile binning into 69 bins, and saves
    the first n_values to a text file.
    
    This is a one-time conversion script.
    """
    print(f"Starting conversion of {input_csv}...")
    
    try:
        # 1. Load the raw time series data
        df = pd.read_csv(input_csv)
        
        # 2. Get the voltage column (the raw random data)
        # Verify the column name, e.g., 'CH1 mV'
        if 'CH1 mV' not in df.columns:
            print(f"Error: Column 'CH1 mV' not found in {input_csv}.")
            print(f"Available columns: {df.columns.tolist()}")
            return
            
        voltages = df['CH1 mV']
        print(f"  Loaded {len(voltages)} voltage readings.")

        # 3. Use quantile-based binning to normalize to [1, 69]
        # We use pd.qcut to get 69 bins with (roughly) equal numbers of samples
        # This is the most robust way to normalize this kind of data
        print(f"  Normalizing data into {n_bins} quantile bins...")
        
        # pd.qcut gives us bin labels, we just want the integer codes
        # 'labels=False' gives us bin indices from 0 to 68
        binned_data = pd.qcut(voltages, q=n_bins, labels=False, duplicates='drop')
        
        # Add 1 to get the range [1, 69]
        normalized_data = binned_data + 1
        
        # 4. Take the first n_values
        if len(normalized_data) < n_values:
            print(f"  Warning: Source data only has {len(normalized_data)} points.")
            final_data = normalized_data
        else:
            final_data = normalized_data.iloc[:n_values]

        # 5. Save to output text file, one number per line
        np.savetxt(output_txt, final_data, fmt='%d')
        
        print(f"\nSuccess! Saved {len(final_data)} normalized numbers to {output_txt}")

    except FileNotFoundError:
        print(f"Error: Input file not found: {input_csv}")
        print("Please make sure 'FIG2a.csv' is in the same directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    INPUT_FILE = "FIG2a.csv"
    OUTPUT_FILE = "mendeley_qrng_10000.txt" # The file run_analysis.py will look for
    N_VALUES = 10000
    
    print("--- Mendeley QRNG Data Converter ---")
    print(f"This script will read '{INPUT_FILE}' and create '{OUTPUT_FILE}'.")
    
    convert_mendeley_to_qrng(INPUT_FILE, OUTPUT_FILE, n_values=N_VALUES)
