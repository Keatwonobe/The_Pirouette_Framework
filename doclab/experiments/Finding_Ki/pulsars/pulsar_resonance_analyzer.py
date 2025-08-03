import os
import pandas as pd
import numpy as np
from scipy.signal import welch, find_peaks
import matplotlib.pyplot as plt
from tqdm import tqdm
from loguru import logger as log

# Constants from your framework
KI_REST = 4.14159
KI_MOTION = 4.18879

def analyze_pulsar_residuals(pulsar_df, pulsar_name):
    """
    Analyzes the timing residuals for a single pulsar for Ki-signatures.
    """
    residuals = pulsar_df['residual_us'].values
    mjds = pulsar_df['mjd'].values
    
    # We need a consistent time step for frequency analysis (FFT/Welch)
    # So we'll analyze the signal in the frequency domain of "cycles per MJD"
    sampling_interval_days = np.mean(np.diff(mjds))
    if np.isnan(sampling_interval_days) or sampling_interval_days == 0:
        return None

    fs = 1.0 / sampling_interval_days # Sampling frequency in days^-1

    # Use Welch's method to get a Power Spectral Density (PSD)
    freqs, psd = welch(residuals, fs=fs, nperseg=min(256, len(residuals)))

    # Find dominant frequency peaks
    peaks, _ = find_peaks(psd, height=np.mean(psd))
    if len(peaks) < 2:
        return None

    dominant_peak_indices = sorted(peaks, key=lambda p: psd[p], reverse=True)[:5]
    dominant_freqs = freqs[dominant_peak_indices]

    # Look for Ki-harmonic ratios between dominant frequencies
    base_freq = dominant_freqs[0]
    matches = {}
    for f in dominant_freqs[1:]:
        ratio = f / base_freq
        if abs(ratio - KI_REST) < 0.1 or abs(1/ratio - KI_REST) < 0.1:
            matches['Ki_Rest_Ratio'] = ratio
        if abs(ratio - KI_MOTION) < 0.1 or abs(1/ratio - KI_MOTION) < 0.1:
            matches['Ki_Motion_Ratio'] = ratio
            
    if not matches:
        return None

    # --- Visualization ---
    plt.figure(figsize=(12, 6))
    plt.semilogy(freqs, psd)
    plt.plot(dominant_freqs, psd[dominant_peak_indices], "x", color='red', markersize=10)
    plt.title(f'Residual Power Spectrum for {pulsar_name}')
    plt.xlabel('Frequency (cycles/day)')
    plt.ylabel('Power Spectral Density')
    plt.grid(True, which="both", ls="--")
    plt.savefig(f"{pulsar_name}_resonance_spectrum.png")
    plt.close()

    return {
        'pulsar': pulsar_name,
        'fundamental_freq_cpd': base_freq,
        'harmonic_matches': matches
    }

def run_broad_analysis(input_csv):
    """
    Runs the resonance analysis on the aggregated residuals CSV.
    """
    log.info(f"Reading aggregated residuals from {input_csv}...")
    df = pd.read_csv(input_csv)
    pulsar_names = df['pulsar'].unique()
    
    all_results = []
    
    for pulsar_name in tqdm(pulsar_names, desc="Analyzing Pulsars for Resonance"):
        pulsar_df = df[df['pulsar'] == pulsar_name]
        result = analyze_pulsar_residuals(pulsar_df, pulsar_name)
        if result:
            all_results.append(result)

    if all_results:
        results_df = pd.DataFrame(all_results)
        output_file = 'pulsar_ki_resonance_findings.csv'
        results_df.to_csv(output_file, index=False)
        log.success(f"Found {len(results_df)} pulsars with potential Ki-signatures. Results saved to {output_file}")
    else:
        log.warning("No significant Ki-signatures found in the dataset.")

if __name__ == '__main__':
    INPUT_CSV = 'all_pulsar_residuals.csv'
    if not os.path.exists(INPUT_CSV):
        print(f"Error: Input file '{INPUT_CSV}' not found. Please run 'batch_residual_extractor.py' first.")
    else:
        run_broad_analysis(INPUT_CSV)