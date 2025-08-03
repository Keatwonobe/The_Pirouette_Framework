#!/usr/bin/env python3
import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import warnings
import zlib
from scipy.stats import kurtosis
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks

# --- Constants ---
KI_REST = 4.14159
KI_MOTION = 4.18879
HARMONIC_RATIOS = {
    "Ki_motion": KI_MOTION,
    "Ki_rest": KI_REST,
    "golden_ratio": 1.618,
    "pi_ratio": np.pi,
}

# --- Analysis Method 1: Fractal Dimension ---
def calculate_fractal_dimension(data):
    """Calculates the fractal dimension 'D' of a time-series."""
    if len(data) < 50: return 0.0
    
    rates, distortions = [], []
    original_data_float = np.array(data, dtype=np.float32)
    data_min, data_max = original_data_float.min(), original_data_float.max()
    if data_max == data_min: return 0.0

    quantization_levels = [2, 4, 8, 16, 32, 64, 128]
    for levels in quantization_levels:
        scaled_data = (original_data_float - data_min) / (data_max - data_min) * (levels - 1)
        quantized_data_int = np.round(scaled_data).astype(np.uint8)
        dequantized_data = data_min + (quantized_data_int.astype(np.float32) / (levels - 1)) * (data_max - data_min)
        distortions.append(np.mean((original_data_float - dequantized_data)**2))
        rates.append(len(zlib.compress(quantized_data_int.tobytes())))

    valid_points = np.array(distortions) > 1e-9
    if np.sum(valid_points) < 2: return 0.0
    
    log_rates = np.log(np.array(rates)[valid_points])
    log_inv_distortions = np.log(1 / np.array(distortions)[valid_points])
    
    try:
        with warnings.catch_warnings():
            D = np.polyfit(log_inv_distortions, log_rates, 1)[0]
    except (np.linalg.LinAlgError, ValueError): D = 0.0
    return D if np.isfinite(D) else 0.0

# --- Analysis Method 2: Statistical Moments ---
def calculate_statistics(data):
    """Calculates key statistical properties of a time-series."""
    if len(data) < 2: return {'std_dev': 0.0, 'kurtosis': 0.0}
    data_array = np.array(data, dtype=np.float64)
    return {
        'std_dev': np.std(data_array),
        'kurtosis': kurtosis(data_array, fisher=False) # Use Pearson's definition
    }

# --- Analysis Method 3: Ki-Harmonic Resonance ---
def calculate_ki_resonance(data):
    """Performs FFT analysis to find a Ki-harmonic resonance score."""
    n = len(data)
    if n < 50: return {'ki_resonance_score': 0.0, 'fundamental_freq': 0.0}
    
    time_series = np.array(data, dtype=np.float64)
    amps = np.abs(rfft(time_series))
    freqs = rfftfreq(n, 1)

    if len(amps) < 2: return {'ki_resonance_score': 0.0, 'fundamental_freq': 0.0}
    
    # Find dominant peaks, ignoring the DC component (index 0)
    peaks, properties = find_peaks(amps[1:], height=np.mean(amps[1:]))
    if len(peaks) < 2: return {'ki_resonance_score': 0.0, 'fundamental_freq': 0.0}
    
    # Sort peaks by amplitude
    sorted_peak_indices = sorted(peaks, key=lambda p: properties['peak_heights'][np.where(peaks == p)[0][0]], reverse=True)
    top_indices = np.array(sorted_peak_indices[:10], dtype=int) + 1 # Get top 10 peaks, correct index
    
    dominant_freqs = freqs[top_indices]
    dominant_amps = amps[top_indices]

    if len(dominant_freqs) < 2: return {'ki_resonance_score': 0.0, 'fundamental_freq': 0.0}

    base_frequency = dominant_freqs[0]
    total_match_strength = 0.0
    
    for i in range(1, len(dominant_freqs)):
        observed_ratio = dominant_freqs[i] / base_frequency
        for name, theo_ratio in HARMONIC_RATIOS.items():
            # Check for match with ratio or its inverse, within a tolerance
            if abs(observed_ratio - theo_ratio) < 0.05 or abs(1/observed_ratio - theo_ratio) < 0.05:
                match_strength = dominant_amps[i] / dominant_amps[0] # Strength relative to fundamental
                total_match_strength += match_strength

    return {
        'ki_resonance_score': total_match_strength,
        'fundamental_freq': base_frequency
    }

# --- Main Processing Pipeline ---
def analyze_preprocessed_data(input_file, output_csv, chk_file):
    """
    Streams a .jsonl file, applies multiple analyses to each entry, and saves results.
    """
    print(f"Starting analysis of preprocessed data from '{input_file}'...")
    
    last_processed_ticker = None
    start_from_scratch = True
    if os.path.exists(chk_file):
        with open(chk_file, 'r') as f:
            last_processed_ticker = f.read().strip()
        if last_processed_ticker:
            start_from_scratch = False
            print(f"Checkpoint found. Resuming after ticker: {last_processed_ticker}")

    if start_from_scratch and os.path.exists(output_csv):
        print("Starting a fresh run. Deleting existing results file.")
        os.remove(output_csv)

    output_file_exists = os.path.exists(output_csv)
    
    with open(input_file, 'r') as f_in, open(output_csv, 'a', newline='') as f_out:
        # Define the header for our comprehensive CSV file
        fieldnames = ['ticker', 'type', 'data_points']
        signals = ['daily_return', 'volatility', 'normalized_volume']
        analyses = ['fractal_dimension', 'std_dev', 'kurtosis', 'ki_resonance_score', 'fundamental_freq']
        for s in signals:
            for a in analyses:
                fieldnames.append(f"{s}_{a}")
        
        writer = pd.DataFrame(columns=fieldnames).to_csv(f_out, header=not output_file_exists, index=False)
        
        # Fast-forward to the last processed ticker if resuming
        if not start_from_scratch:
            print("Scanning to resume point...")
            for line in f_in:
                if json.loads(line)['ticker'] == last_processed_ticker:
                    print("Resume point found. Starting analysis.")
                    break
        
        # Use tqdm to show progress on the rest of the file
        for line in tqdm(f_in, desc="Analyzing Assets"):
            try:
                asset_data = json.loads(line)
                results_row = {
                    'ticker': asset_data['ticker'],
                    'type': asset_data['type'],
                    'data_points': asset_data['data_points']
                }

                for signal_name, signal_data in asset_data['signals'].items():
                    # Run all analyses on this signal
                    fd_result = calculate_fractal_dimension(signal_data)
                    stats_result = calculate_statistics(signal_data)
                    ki_result = calculate_ki_resonance(signal_data)
                    
                    # Add results to the row
                    results_row[f'{signal_name}_fractal_dimension'] = fd_result
                    results_row[f'{signal_name}_std_dev'] = stats_result['std_dev']
                    results_row[f'{signal_name}_kurtosis'] = stats_result['kurtosis']
                    results_row[f'{signal_name}_ki_resonance_score'] = ki_result['ki_resonance_score']
                    results_row[f'{signal_name}_fundamental_freq'] = ki_result['fundamental_freq']

                # Write the single row to the CSV
                pd.DataFrame([results_row]).to_csv(f_out, header=False, index=False)

                # Update checkpoint file
                with open(chk_file, 'w') as f_chk:
                    f_chk.write(asset_data['ticker'])
            
            except (json.JSONDecodeError, KeyError) as e:
                # Handle potential issues with malformed lines in the jsonl
                continue

    print(f"\n✅ Comprehensive analysis complete. Results saved to '{output_csv}'")

if __name__ == '__main__':
    # --- Configuration ---
    PREPROCESSED_FILE = "preprocessed_stock_data.jsonl"
    ANALYSIS_RESULTS_CSV = "stock_analysis_results.csv"
    CHECKPOINT_FILE = "stock_analyzer.chk"

    try:
        analyze_preprocessed_data(PREPROCESSED_FILE, ANALYSIS_RESULTS_CSV, CHECKPOINT_FILE)
    except FileNotFoundError:
        print(f"ERROR: The preprocessed data file '{PREPROCESSED_FILE}' was not found.")
        print("Please run the 'stock_data_preprocessor.py' script first.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
