# filename: universal_resonance_rate_analyzer.py

import argparse
import zlib
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from astropy.io import fits
from obspy import read as read_mseed
from sklearn.random_projection import GaussianRandomProjection
from sklearn.metrics import mean_squared_error
import warnings

# --- Core Functions ---

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
    
    # Handle the case where data might be constant
    data_min, data_max = original_data_float.min(), original_data_float.max()
    if data_max == data_min:
        print("Warning: Data is constant. Distortion will be zero.")
        # Create dummy results for constant data
        for levels in quantization_levels:
            quantized_data = np.full_like(original_data_float, fill_value=data_min, dtype=np.uint8)
            rates.append(len(zlib.compress(quantized_data.tobytes())))
            distortions.append(0.0)
        return rates, distortions

    for levels in quantization_levels:
        # 1. Quantize the data
        # Scale data to [0, levels-1]
        scaled_data = (original_data_float - data_min) / (data_max - data_min) * (levels - 1)
        quantized_data_int = np.round(scaled_data).astype(np.uint8)

        # 2. Calculate Distortion (ε)
        # De-quantize to compare with original
        dequantized_data = data_min + (quantized_data_int.astype(np.float32) / (levels - 1)) * (data_max - data_min)
        # MSE between original and de-quantized data
        distortion = mean_squared_error(original_data_float, dequantized_data)
        distortions.append(distortion)

        # 3. Calculate Rate (R)
        # Compress the quantized data and get the length
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
    data_2d = data.reshape(1, -1) # Reshape for sklearn compatibility

    for n_components in n_components_list:
        if n_components > data.shape[0]:
            continue
            
        # 1. Project to a lower dimension (this is our "encoding")
        rp = GaussianRandomProjection(n_components=n_components)
        projected_data = rp.fit_transform(data_2d)
        
        # 2. Calculate Rate (R)
        # The "code length" is the number of dimensions we kept.
        rate = n_components
        rates.append(rate)

        # 3. Calculate Distortion (ε)
        # Reconstruct the data from the projection
        reconstructed_data = rp.inverse_transform(projected_data)
        distortion = mean_squared_error(data_2d, reconstructed_data)
        distortions.append(distortion)
        
    return rates, distortions

# --- Data Loaders ---

def load_text_data(filepath):
    """Loads and preprocesses a text file."""
    print(f"Loading TEXT data from: {filepath}")
    with open(filepath, 'rb') as f:
        # Read as raw bytes for quantization
        raw_data = f.read()
    # Convert bytes to a numpy array of integers (0-255)
    return np.frombuffer(raw_data, dtype=np.uint8).astype(np.float32)

def load_fits_data(filepath):
    """Loads and preprocesses a FITS file."""
    print(f"Loading FITS data from: {filepath}")
    with fits.open(filepath) as hdul:
        # Find the first HDU with image data
        image_hdu = None
        for hdu in hdul:
            if hdu.data is not None and isinstance(hdu.data, np.ndarray) and hdu.data.ndim >= 2:
                image_hdu = hdu
                break
        if image_hdu is None:
            raise ValueError("No image data found in FITS file.")
        
        print(f"Found image data in HDU: {image_hdu.name}")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            # Flatten the image data to a 1D array
            data = image_hdu.data.astype(np.float32).flatten()
            
    # Remove NaN/Inf values if they exist
    data = data[np.isfinite(data)]
    return data

def load_mseed_data(filepath):
    """Loads and preprocesses an MSEED file."""
    print(f"Loading MSEED data from: {filepath}")
    stream = read_mseed(filepath)
    if not stream:
        raise ValueError("No data streams found in MSEED file.")
    # Concatenate all traces into a single array
    data = np.concatenate([tr.data for tr in stream]).astype(np.float32)
    return data

# --- Visualization ---

def visualize_results(data_type, rates, distortions, rp_rates, rp_distortions):
    """
    Plots the rate-distortion curves for both methods.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))

    # We plot Rate vs. 1/Distortion on a log-log scale to test the power law
    inv_distortions = [1/d if d > 0 else np.inf for d in distortions]
    rp_inv_distortions = [1/d if d > 0 else np.inf for d in rp_distortions]

    # Filter out infinite values for plotting
    finite_mask = np.isfinite(inv_distortions)
    rp_finite_mask = np.isfinite(rp_inv_distortions)

    if np.any(finite_mask):
        ax.plot(np.array(inv_distortions)[finite_mask], np.array(rates)[finite_mask], 'o-', label='Pirouette (Quantization + Compression)', color='crimson')
        # Fit a line in log-log space to find the fractal dimension D
        log_x = np.log(np.array(inv_distortions)[finite_mask])
        log_y = np.log(np.array(rates)[finite_mask])
        # Filter out any remaining -inf from log(0)
        valid_fit_mask = np.isfinite(log_x) & np.isfinite(log_y)
        if np.sum(valid_fit_mask) > 1:
            m, c = np.polyfit(log_x[valid_fit_mask], log_y[valid_fit_mask], 1)
            ax.plot(np.array(inv_distortions)[finite_mask], np.exp(c) * np.array(inv_distortions)[finite_mask]**m, '--', color='red', label=f'Fit (Fractal Dim D ≈ {m:.2f})')
        else:
            print("Not enough data to fit a line to the Pirouette results.")

    if np.any(rp_finite_mask):
        ax.plot(np.array(rp_inv_distortions)[rp_finite_mask], np.array(rp_rates)[rp_finite_mask], 's-', label='Control (Random Projection)', color='navy', alpha=0.7)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Information Fidelity (1 / Distortion ε)')
    ax.set_ylabel('Information Rate (Code Length in bytes or dimensions)')
    ax.set_title(f'Rate-Distortion Analysis for {data_type.upper()} Data')
    ax.legend()
    ax.grid(True, which="both", ls="--")
    
    output_filename = f"rate_distortion_{data_type}.png"
    plt.savefig(output_filename, dpi=150)
    print(f"\n✓ Plot saved to {output_filename}")
    plt.show()

# --- Main Execution Logic ---

def main():
    parser = argparse.ArgumentParser(
        description="Universal Resonance-Rate Analyzer based on the Pirouette Dimension-Collapse Lemma.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("filepath", type=str, help="Path to the input data file.")
    parser.add_argument("filetype", type=str, choices=['text', 'fits', 'mseed'], help="Type of the input file.")

    args = parser.parse_args()
    
    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"Error: File not found at {filepath}")
        return

    # Load data based on file type
    loader_map = {
        'text': load_text_data,
        'fits': load_fits_data,
        'mseed': load_mseed_data,
    }
    try:
        data = loader_map[args.filetype](filepath)
        if data.size == 0:
            print("Error: No data loaded from file.")
            return
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # --- Run Experiment ---
    print("\n--- Running Pirouette Analysis (Quantization + Compression) ---")
    # Define quantization levels (powers of 2 are common)
    quant_levels = [2, 4, 8, 16, 32, 64, 128, 256]
    rates, distortions = get_rate_distortion(data, quant_levels)
    print("Results (Rate, Distortion):")
    for r, d in zip(rates, distortions):
        print(f"  {r} bytes, {d:.4e}")

    # --- Run Control Experiment ---
    print("\n--- Running Control Analysis (Random Projection) ---")
    # Define target dimensions for random projection
    n_dims = np.linspace(10, min(1000, data.size // 2), 10, dtype=int)
    rp_rates, rp_distortions = get_random_projection_rate_distortion(data, n_dims)
    print("Results (Rate, Distortion):")
    for r, d in zip(rp_rates, rp_distortions):
        print(f"  {r} dimensions, {d:.4e}")

    # --- Visualize ---
    visualize_results(args.filetype, rates, distortions, rp_rates, rp_distortions)

if __name__ == "__main__":
    main()