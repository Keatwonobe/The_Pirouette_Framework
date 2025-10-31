# filename: process_all_resonances.py

import os
import shutil
import zlib
import warnings
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Dependency Imports ---
# These libraries provide the core functionalities for analysis and data handling.
# Make sure they are installed in your Python environment.
# pip install numpy pandas matplotlib scikit-learn astropy obspy scipy
try:
    from astropy.io import fits
    from obspy import read as read_mseed
    from sklearn.random_projection import GaussianRandomProjection
    from sklearn.metrics import mean_squared_error, r2_score
    from scipy.stats import skew, kurtosis
except ImportError as e:
    print(f"Error: A required library is missing. {e}")
    print("Please install all required libraries by running: pip install numpy pandas matplotlib scikit-learn astropy obspy scipy")
    exit()

# --- Core Analysis Functions ---

def get_rate_distortion(data, quantization_levels):
    """
    Calculates the rate and distortion for a given dataset over a range of quantization levels.

    Args:
        data (np.ndarray): The input data array (1D).
        quantization_levels (list): A list of integers representing the number of levels to quantize to.

    Returns:
        tuple: A tuple containing lists of rates (compressed sizes) and distortions (MSE).
    """
    rates = []
    distortions = []
    original_data_float = data.astype(np.float32)

    data_min, data_max = original_data_float.min(), original_data_float.max()
    if data_max == data_min:
        # For constant data, distortion is always zero.
        for _ in quantization_levels:
            quantized_data = np.full_like(original_data_float, fill_value=data_min, dtype=np.uint8)
            rates.append(len(zlib.compress(quantized_data.tobytes())))
            distortions.append(0.0)
        return rates, distortions

    for levels in quantization_levels:
        # Quantize the data by scaling to the number of levels
        scaled_data = (original_data_float - data_min) / (data_max - data_min) * (levels - 1)
        quantized_data_int = np.round(scaled_data).astype(np.uint8)

        # De-quantize to calculate distortion
        dequantized_data = data_min + (quantized_data_int.astype(np.float32) / (levels - 1)) * (data_max - data_min)
        distortion = mean_squared_error(original_data_float, dequantized_data)
        distortions.append(distortion)

        # Calculate rate by compressing the quantized data
        compressed_data = zlib.compress(quantized_data_int.tobytes())
        rate = len(compressed_data)
        rates.append(rate)

    return rates, distortions

def get_random_projection_rate_distortion(data, n_components_list):
    """
    Calculates rate and distortion using a random projection as a control.

    Args:
        data (np.ndarray): The input data array (1D).
        n_components_list (list): List of target dimensions for the projection.

    Returns:
        tuple: A tuple containing lists of rates (projected dimensions) and distortions (reconstruction MSE).
    """
    rates = []
    distortions = []
    data_2d = data.reshape(1, -1)  # Reshape for sklearn compatibility

    for n_components in n_components_list:
        if n_components > data.shape[0]:
            continue
        rp = GaussianRandomProjection(n_components=n_components)
        projected_data = rp.fit_transform(data_2d)
        
        # Rate is the number of dimensions in the projection
        rates.append(n_components)

        # Distortion is the reconstruction error
        reconstructed_data = rp.inverse_transform(projected_data)
        distortion = mean_squared_error(data_2d, reconstructed_data)
        distortions.append(distortion)

    return rates, distortions

def get_data_statistics(data):
    """Calculates descriptive statistics for the raw data."""
    if data.size == 0:
        return {
            'mean': 0, 'std_dev': 0, 'skewness': 0,
            'kurtosis': 0, 'min': 0, 'max': 0
        }
    return {
        'mean': np.mean(data),
        'std_dev': np.std(data),
        'skewness': skew(data),
        'kurtosis': kurtosis(data),
        'min': np.min(data),
        'max': np.max(data)
    }

def analyze_power_law_fit(rates, distortions):
    """
    Fits a power law to the R-D curve to find the fractal dimension 'D'.
    This relationship is expected to be R ∝ (1/ε)^D. In log-space, this becomes
    log(R) = D * log(1/ε) + C, a linear relationship.

    Returns:
        tuple: A tuple containing the fractal dimension (D) and the R-squared value of the fit.
    """
    # Inverse distortion represents information fidelity
    inv_distortions = np.array([1/d if d > 0 else np.inf for d in distortions])

    # Filter out non-finite values for a clean log-transform
    finite_mask = np.isfinite(inv_distortions) & (np.array(rates) > 0)
    if np.sum(finite_mask) < 2:
        return 0, 0  # Not enough data points to fit a line

    rates_f = np.array(rates)[finite_mask]
    inv_distortions_f = inv_distortions[finite_mask]

    log_rates = np.log(rates_f)
    log_inv_distortions = np.log(inv_distortions_f)
    
    # Ensure no lingering -inf values from log(0) if any slip through
    valid_fit_mask = np.isfinite(log_rates) & np.isfinite(log_inv_distortions)
    if np.sum(valid_fit_mask) < 2:
        return 0, 0

    x = log_inv_distortions[valid_fit_mask]
    y = log_rates[valid_fit_mask]

    # Perform linear regression to find the slope (D)
    D, _ = np.polyfit(x, y, 1)
    
    # Calculate R-squared for goodness-of-fit
    predicted_y = np.polyval(np.polyfit(x, y, 1), x)
    r_sq = r2_score(y, predicted_y)
    
    return D, r_sq

# --- Data Loaders ---

def load_data(filepath):
    """Factory function to load data from a file based on its extension."""
    suffix = filepath.suffix.lower()
    if suffix == '.txt':
        filetype = 'text'
        with open(filepath, 'rb') as f:
            raw_data = f.read()
        data = np.frombuffer(raw_data, dtype=np.uint8).astype(np.float32)
    elif suffix == '.fits':
        filetype = 'fits'
        with fits.open(filepath) as hdul:
            image_hdu = next((hdu for hdu in hdul if hdu.data is not None and isinstance(hdu.data, np.ndarray)), None)
            if image_hdu is None: raise ValueError("No image data found in FITS file.")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                data = image_hdu.data.astype(np.float32).flatten()
    elif suffix == '.mseed':
        filetype = 'mseed'
        stream = read_mseed(filepath)
        if not stream: raise ValueError("No data streams found in MSEED file.")
        data = np.concatenate([tr.data for tr in stream]).astype(np.float32)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    
    # Clean data and return
    return data[np.isfinite(data)], filetype

# --- Main Execution Logic ---

def main():
    """
    Main function to run the batch analysis.
    1. Finds all .txt, .fits, and .mseed files in the current directory.
    2. For each file, it computes statistical properties and the rate-distortion curve.
    3. Calculates the 'Fractal Dimension (D)' from the curve.
    4. Moves the processed file to a 'processed' sub-directory.
    5. Aggregates all results, calculates a Z-score for D, and saves to a CSV file.
    """
    print("--- Universal Resonance-Rate Batch Analyzer ---")
    
    # Setup directories and file matching
    source_dir = Path.cwd()
    processed_dir = source_dir / "processed"
    processed_dir.mkdir(exist_ok=True)
    
    file_patterns = ['*.txt', '*.fits', '*.mseed', '*.TXT', '*.FITS', '*.MSEED']
    files_to_process = []
    for pattern in file_patterns:
        files_to_process.extend(source_dir.glob(pattern))
        
    if not files_to_process:
        print("No data files found to process in the current directory.")
        return

    print(f"Found {len(files_to_process)} files to analyze.")
    all_results = []

    # Process each file
    for filepath in files_to_process:
        print(f"\nProcessing: {filepath.name}...")
        try:
            # 1. Load Data
            data, file_type = load_data(filepath)
            if data.size == 0:
                print(f"Warning: No valid data loaded from {filepath.name}. Skipping.")
                continue

            # 2. Get Statistics
            stats = get_data_statistics(data)
            
            # 3. Run Pirouette Analysis
            quant_levels = [2, 4, 8, 16, 32, 64, 128, 256]
            rates, distortions = get_rate_distortion(data, quant_levels)

            # 4. Calculate Fractal Dimension
            fractal_dim, r_squared = analyze_power_law_fit(rates, distortions)
            
            # 5. Store Results
            result = {
                'filename': filepath.name,
                'file_type': file_type,
                'file_size_kb': round(filepath.stat().st_size / 1024, 2),
                'fractal_dimension_D': fractal_dim,
                'r_squared_fit': r_squared,
                **stats  # Unpack the statistics dictionary
            }
            all_results.append(result)
            print(f"✓ Analysis complete. Fractal Dimension (D) = {fractal_dim:.4f}")

            # 6. Move File
            shutil.move(str(filepath), str(processed_dir / filepath.name))
            print(f"→ Moved '{filepath.name}' to '{processed_dir.name}/' folder.")

        except Exception as e:
            print(f"✗ ERROR: Could not process {filepath.name}. Reason: {e}")
            # Optionally move failed files to a 'failed' directory
            # failed_dir = source_dir / "failed"
            # failed_dir.mkdir(exist_ok=True)
            # shutil.move(str(filepath), str(failed_dir / filepath.name))

    # After processing all files, compile results and save
    if not all_results:
        print("\nNo files were successfully processed. No output file generated.")
        return
        
    results_df = pd.DataFrame(all_results)
    
    # Calculate Z-score for the fractal dimension across the batch
    d_mean = results_df['fractal_dimension_D'].mean()
    d_std = results_df['fractal_dimension_D'].std()
    if d_std > 0:
        results_df['D_z_score'] = (results_df['fractal_dimension_D'] - d_mean) / d_std
    else:
        results_df['D_z_score'] = 0.0 # Avoid division by zero if all D values are the same

    # Define column order for clarity in the CSV
    column_order = [
        'filename', 'file_type', 'file_size_kb', 'fractal_dimension_D', 'D_z_score',
        'r_squared_fit', 'mean', 'std_dev', 'skewness', 'kurtosis', 'min', 'max'
    ]
    results_df = results_df[column_order]

    # Save to CSV
    output_filename = "resonance_analysis_results.csv"
    results_df.to_csv(output_filename, index=False, float_format='%.6f')
    
    print(f"\n✅ Batch processing complete. All results saved to '{output_filename}'.")


if __name__ == "__main__":
    main()