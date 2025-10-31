import os
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from pint import models, toa
from pint.residuals import Residuals
import pint.logging
from loguru import logger as log
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks

# --- Constants from your framework ---
KI_REST = 4.14159
KI_MOTION = 4.18879

# Setup logging
pint.logging.setup(level="INFO")

def analyze_pulsar_for_ki(base_dir, pulsar_name):
    """
    Analyzes a pulsar's residuals for Ki-resonant frequencies.
    """
    log.info(f"Starting Ki-resonance analysis for pulsar: {pulsar_name}")

    par_file_path = os.path.join(base_dir, 'narrowband', 'par', f'{pulsar_name}_PINT_20220302.nb.par')
    tim_file_path = os.path.join(base_dir, 'narrowband', 'tim', f'{pulsar_name}_PINT_20220302.nb.tim')

    if not os.path.exists(par_file_path) or not os.path.exists(tim_file_path):
        log.error(f"Data files for {pulsar_name} not found.")
        return

    # --- Step 1: Calculate Residuals (same as before) ---
    try:
        model = models.get_model(par_file_path)
        t = toa.get_TOAs(tim_file_path, ephem="DE440", planets=True)
        residuals_us = Residuals(t, model).time_resids.to_value(u.us)
        times_mjd = t.get_mjds().value
    except Exception as e:
        log.error(f"Error calculating residuals for {pulsar_name}: {e}")
        return

    # --- Step 2: Frequency Analysis (FFT) ---
    # We need to work with evenly spaced data for a simple FFT.
    # We'll analyze the signal in "cycles per MJD".
    avg_sampling_interval = np.mean(np.diff(times_mjd))
    if avg_sampling_interval == 0:
        log.error("Cannot perform FFT on data with zero time intervals.")
        return
        
    sampling_freq = 1.0 / avg_sampling_interval # cycles per MJD

    # Perform the FFT on the residuals
    fft_amps = rfft(residuals_us)
    fft_freqs = rfftfreq(len(residuals_us), d=avg_sampling_interval)
    
    power_spectrum = np.abs(fft_amps)**2

    # --- Step 3: Search for Ki-Harmonics ---
    peaks, _ = find_peaks(power_spectrum, height=np.mean(power_spectrum) * 5) # Find significant peaks
    if len(peaks) < 2:
        log.warning("Not enough significant frequency peaks found for harmonic analysis.")
        return

    dominant_freqs = fft_freqs[peaks]
    dominant_powers = power_spectrum[peaks]
    
    # Sort by power to find the fundamental frequency
    sorted_indices = np.argsort(dominant_powers)[::-1]
    fundamental_freq = dominant_freqs[sorted_indices[0]]

    ki_matches = {}
    for freq in dominant_freqs:
        ratio_motion = freq / fundamental_freq
        ratio_rest = freq / fundamental_freq
        
        # Check for matches with a 5% tolerance
        if abs(ratio_motion - KI_MOTION) < KI_MOTION * 0.05:
            ki_matches[freq] = 'Ki_Motion'
        if abs(ratio_rest - KI_REST) < KI_REST * 0.05:
            ki_matches[freq] = 'Ki_Rest'

    # --- Step 4: Visualize Results ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    
    # Plot 1: Standard Residuals Plot
    ax1.plot(times_mjd, residuals_us, 'x', alpha=0.5, label='Residuals')
    ax1.set_title(f'Timing Residuals for Pulsar {pulsar_name}')
    ax1.set_xlabel('Time (MJD)')
    ax1.set_ylabel('Residuals (µs)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()

    # Plot 2: Power Spectrum with Ki-Harmonics
    ax2.plot(fft_freqs, power_spectrum, label='Power Spectrum', color='slateblue')
    ax2.plot(dominant_freqs, dominant_powers, "x", color='crimson', markersize=8, label='Dominant Frequencies')
    
    for freq, label in ki_matches.items():
        ax2.axvline(x=freq, color='limegreen', linestyle='--', lw=2, label=f'Ki Match: {label} at {freq:.4f} cpd')

    ax2.set_title(f'Residual Power Spectrum & Ki-Resonance Analysis for {pulsar_name}')
    ax2.set_xlabel('Frequency (cycles per day)')
    ax2.set_ylabel('Power')
    ax2.set_yscale('log')
    ax2.grid(True, which="both", ls="--", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    output_filename = f'{pulsar_name}_ki_spectrum_analysis.png'
    plt.savefig(output_filename)
    log.success(f"Ki Spectrum Analysis plot saved to {output_filename}")
    plt.close()


if __name__ == '__main__':
    # --- Configuration ---
    NANOGRAV_BASE_DIR = r'C:/Users/keatw/Downloads/NANOGrav15yr_PulsarTiming_v2.1.0/NANOGrav15yr_PulsarTiming_v2.1.0'
    PULSAR_TO_ANALYZE = 'J0030+0451' 
    
    # --- Run Analysis ---
    if not os.path.exists(os.path.join(NANOGRAV_BASE_DIR, 'narrowband')):
        print("Please update the 'NANOGRAV_BASE_DIR' variable to the correct path.")
    else:
        analyze_pulsar_for_ki(NANOGRAV_BASE_DIR, PULSAR_TO_ANALYZE)