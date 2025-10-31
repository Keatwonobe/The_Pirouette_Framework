# filename: process_all_resonances_final.py

import os
import shutil
import zlib
import warnings
from pathlib import Path
import pandas as pd
import numpy as np

# --- Dependency Imports ---
try:
    from astropy.io import fits
    from obspy import read as read_mseed
    from sklearn.random_projection import GaussianRandomProjection
    from sklearn.metrics import mean_squared_error, r2_score
    from scipy.stats import skew, kurtosis
    from scipy.io import wavfile
except ImportError as e:
    print(f"Error: A required library is missing. {e}")
    print("Please install all required libraries: pip install numpy pandas scikit-learn astropy obspy scipy")
    exit()

# --- Core Analysis Functions ---

def get_rate_distortion(data, quantization_levels):
    """Calculates rate and distortion (MSE) over a range of quantization levels."""
    rates = []
    distortions = []
    original_data_float = data.astype(np.float32)

    data_min, data_max = original_data_float.min(), original_data_float.max()
    if data_max == data_min:
        for _ in quantization_levels:
            quantized_data = np.full_like(original_data_float, fill_value=data_min, dtype=np.uint8)
            rates.append(len(zlib.compress(quantized_data.tobytes())))
            distortions.append(0.0)
        return rates, distortions

    for levels in quantization_levels:
        scaled_data = (original_data_float - data_min) / (data_max - data_min) * (levels - 1)
        quantized_data_int = np.round(scaled_data).astype(np.uint8)
        dequantized_data = data_min + (quantized_data_int.astype(np.float32) / (levels - 1)) * (data_max - data_min)
        distortion = mean_squared_error(original_data_float, dequantized_data)
        distortions.append(distortion)
        compressed_data = zlib.compress(quantized_data_int.tobytes())
        rate = len(compressed_data)
        rates.append(rate)

    return rates, distortions

def get_data_statistics(data):
    """Calculates descriptive statistics for the raw data."""
    if data.size == 0: return { 'mean': 0, 'std_dev': 0, 'skewness': 0, 'kurtosis': 0, 'min': 0, 'max': 0 }
    return {
        'mean': np.mean(data), 'std_dev': np.std(data), 'skewness': skew(data),
        'kurtosis': kurtosis(data), 'min': np.min(data), 'max': np.max(data)
    }

def get_drift_score(data, n_chunks=10):
    """
    Calculates a drift score as the standard deviation of the means of data chunks.
    A simple proxy for non-stationarity.
    """
    if data.size < n_chunks * 2: return 0.0 # Not enough data
    try:
        chunk_means = [np.mean(chunk) for chunk in np.array_split(data, n_chunks)]
        return np.std(chunk_means)
    except Exception:
        return 0.0

def analyze_power_law_fit(rates, distortions):
    """Fits a power law to the R-D curve to find the fractal dimension 'D'."""
    inv_distortions = np.array([1/d if d > 0 else np.inf for d in distortions])
    finite_mask = np.isfinite(inv_distortions) & (np.array(rates) > 0)
    if np.sum(finite_mask) < 2: return 0, 0

    rates_f = np.array(rates)[finite_mask]
    inv_distortions_f = inv_distortions[finite_mask]
    log_rates, log_inv_distortions = np.log(rates_f), np.log(inv_distortions_f)

    valid_fit_mask = np.isfinite(log_rates) & np.isfinite(log_inv_distortions)
    if np.sum(valid_fit_mask) < 2: return 0, 0

    x, y = log_inv_distortions[valid_fit_mask], log_rates[valid_fit_mask]
    D, _ = np.polyfit(x, y, 1)
    predicted_y = np.polyval(np.polyfit(x, y, 1), x)
    r_sq = r2_score(y, predicted_y)
    
    return D, r_sq

# --- Data Loaders ---

def load_data(filepath):
    """Factory function to load data from a file based on its extension."""
    suffix = filepath.suffix.lower()
    data = np.array([])
    filetype = suffix.replace('.', '')
    
    if filetype == 'txt':
        with open(filepath, 'rb') as f: data = np.frombuffer(f.read(), dtype=np.uint8)
    elif filetype == 'fits':
        with fits.open(filepath) as hdul:
            image_hdu = next((h for h in hdul if h.data is not None and isinstance(h.data, np.ndarray)), None)
            if image_hdu: data = image_hdu.data.astype(np.float32).flatten()
    elif filetype == 'mseed':
        stream = read_mseed(filepath,_format='MSEED')
        if stream: data = np.concatenate([tr.data for tr in stream])
    elif filetype == 'wav':
        samplerate, data = wavfile.read(filepath)
        if data.ndim > 1: data = data.mean(axis=1) # Convert stereo to mono
    elif filetype in ['fasta', 'fa', 'fna']:
        # Map nucleotides to integers
        mapping = { 'A': 0, 'C': 1, 'G': 2, 'T': 3, 'N': 4 }
        char_list = []
        with open(filepath, 'r') as f:
            for line in f:
                if not line.startswith('>'):
                    char_list.extend(list(line.strip().upper()))
        data = np.array([mapping.get(c, 4) for c in char_list], dtype=np.uint8)

    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    
    return data[np.isfinite(data)].astype(np.float32), filetype

# --- Main Execution Logic ---

def main():
    """Main function to run the batch analysis."""
    print("--- Universal Resonance-Rate Batch Analyzer (Final) ---")
    source_dir, processed_dir = Path.cwd(), Path.cwd() / "processed"
    processed_dir.mkdir(exist_ok=True)
    
    # Expanded file patterns
    patterns = ['*.txt', '*.fits', '*.mseed', '*.wav', '*.fasta', '*.fa', '*.fna']
    files = [p for pattern in patterns for p in source_dir.glob(pattern)]
    
    if not files:
        print("No data files found to process.")
        return

    all_results = []
    for filepath in files:
        print(f"\nProcessing: {filepath.name}...")
        try:
            data, file_type = load_data(filepath)
            if data.size == 0: continue

            stats = get_data_statistics(data)
            quant_levels = [2, 4, 8, 16, 32, 64, 128, 256]
            rates, distortions = get_rate_distortion(data, quant_levels)
            fractal_dim, r_squared = analyze_power_law_fit(rates, distortions)
            
            # **B. Residual-error check**: Use RMSE from highest fidelity distortion
            final_rmse_check = np.sqrt(distortions[-1]) if distortions else 0
            
            # **D. Calculate Drift Score**
            drift_score = get_drift_score(data)
            
            result = {
                'filename': filepath.name, 'file_type': file_type,
                'file_size_kb': round(filepath.stat().st_size / 1024, 2),
                'fractal_dimension_D': fractal_dim, 'r_squared_fit': r_squared,
                'final_rmse_check': final_rmse_check, 'drift_score': drift_score,
                **stats
            }
            all_results.append(result)
            shutil.move(str(filepath), str(processed_dir / filepath.name))

        except Exception as e:
            print(f"✗ ERROR processing {filepath.name}: {e}")

    if not all_results:
        print("\nNo files successfully processed.")
        return
        
    df = pd.DataFrame(all_results)
    d_mean, d_std = df['fractal_dimension_D'].mean(), df['fractal_dimension_D'].std()
    df['D_z_score'] = (df['fractal_dimension_D'] - d_mean) / d_std if d_std > 0 else 0
    
    # Reorder columns to include new metrics
    cols = [
        'filename', 'file_type', 'file_size_kb', 'fractal_dimension_D', 'D_z_score',
        'r_squared_fit', 'final_rmse_check', 'drift_score', 'mean', 'std_dev', 
        'skewness', 'kurtosis', 'min', 'max'
    ]
    output_filename = "resonance_analysis_results_final.csv"
    df[cols].to_csv(output_filename, index=False, float_format='%.6f')
    print(f"\n✅ Batch processing complete. Results saved to '{output_filename}'.")
    
    # **D. Perform correlation check**
    if 'drift_score' in df.columns and 'final_rmse_check' in df.columns:
        correlation = df[['drift_score', 'final_rmse_check']].corr().iloc[0, 1]
        print(f"\n--- Correlation Check ---")
        print(f"Pearson correlation between 'drift_score' and 'final_rmse_check': {correlation:.4f}")

if __name__ == "__main__":
    main()