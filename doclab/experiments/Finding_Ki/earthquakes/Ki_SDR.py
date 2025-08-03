#!/usr/bin/env python3
"""
Ki Resonance Detector - HackRF One Implementation
Uses pyHackRF to detect Ki-related resonance patterns in radio signals
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, find_peaks
import time
from datetime import datetime
import os
import argparse
import hackrf

# Constants from Pirouette Framework
KI_REST = 4.14159      # Ki in rest state
KI_MOTION = 4.0 * np.pi / 3.0  # Approx 4.18879
DELTA_KI = KI_MOTION - KI_REST

# Create output directory for results
output_dir = "ki_detection_results"
os.makedirs(output_dir, exist_ok=True)

def setup_hackrf(center_freq, sample_rate, gain=40):
    """Initialize the HackRF One with the specified parameters"""
    # Create HackRF device instance
    device = hackrf.HackRF()
    
    # Set parameters
    device.sample_rate = sample_rate
    device.center_freq = center_freq
    device.lna_gain = min(gain, 40)  # LNA gain (0-40 dB)
    device.vga_gain = min(gain, 62)  # VGA gain (0-62 dB)
    
    print(f"HackRF initialized with:")
    print(f"  Center frequency: {center_freq/1e6:.2f} MHz")
    print(f"  Sample rate: {sample_rate/1e6:.2f} Msps")
    print(f"  LNA gain: {device.lna_gain} dB")
    print(f"  VGA gain: {device.vga_gain} dB")
    
    return device

def capture_samples(device, duration_sec, chunk_size=131072):
    """Capture samples from the HackRF for the specified duration"""
    num_samples = int(duration_sec * device.sample_rate)
    samples = np.zeros(num_samples, dtype=np.complex64)
    
    # Calculate number of chunks needed
    num_chunks = int(np.ceil(num_samples / chunk_size))
    
    print(f"Capturing {duration_sec:.1f} seconds of data ({num_samples} samples)...")
    
    # Start RX
    device.start_rx_mode()
    
    samples_collected = 0
    for i in range(num_chunks):
        if samples_collected >= num_samples:
            break
            
        # Read a chunk of samples
        iq_data = device.read_samples(chunk_size)
        
        # Convert to complex
        complex_data = iq_data[::2] + 1j * iq_data[1::2]
        
        # Add to our samples array
        samples_to_copy = min(len(complex_data), num_samples - samples_collected)
        samples[samples_collected:samples_collected+samples_to_copy] = complex_data[:samples_to_copy]
        samples_collected += samples_to_copy
        
        # Show progress
        progress = samples_collected / num_samples * 100
        print(f"\rProgress: {progress:.1f}%", end="")
    
    print("\nCapture complete!")
    device.stop_rx_mode()
    
    return samples

def analyze_ki_resonance(samples, sample_rate):
    """Analyze samples for Ki-related resonance patterns"""
    results = {}
    
    # Extract amplitude and phase
    analytic_signal = hilbert(np.real(samples))
    amplitude = np.abs(analytic_signal)
    phase = np.unwrap(np.angle(analytic_signal))
    
    # Calculate instantaneous frequency
    time = np.arange(len(samples)) / sample_rate
    phase_derivative = np.gradient(phase, time)
    inst_freq = phase_derivative / (2 * np.pi)
    
    # Analyze phase evolution rates
    results['mean_phase_rate'] = np.mean(phase_derivative)
    
    # Tolerance for Ki matches (can be adjusted)
    tolerance = 0.05
    
    # Check for Ki-related phase rates
    ki_rest_matches = np.abs(phase_derivative - KI_REST) < (KI_REST * tolerance)
    ki_motion_matches = np.abs(phase_derivative - KI_MOTION) < (KI_MOTION * tolerance)
    
    results['ki_rest_match_percentage'] = np.sum(ki_rest_matches) / len(phase_derivative) * 100
    results['ki_motion_match_percentage'] = np.sum(ki_motion_matches) / len(phase_derivative) * 100
    
    # Analyze frequency spectrum for Ki-related modulations
    spectrum = np.abs(np.fft.fft(np.real(samples)))
    freqs = np.fft.fftfreq(len(samples), 1/sample_rate)
    
    # Check for spectral components at Ki-related frequencies
    # Looking for Ki/(2π) frequencies which would appear as modulation or oscillation rates
    ki_rest_freq = KI_REST / (2 * np.pi)  # ~0.66 Hz
    ki_motion_freq = KI_MOTION / (2 * np.pi)  # ~0.67 Hz
    
    # Find peaks in the frequency domain
    peak_indices, _ = find_peaks(spectrum[:len(spectrum)//2], height=np.mean(spectrum) + np.std(spectrum))
    peak_freqs = freqs[peak_indices]
    peak_powers = spectrum[peak_indices]
    
    # Check if any peaks are near Ki-related frequencies
    ki_matches = []
    for freq_to_check in [ki_rest_freq, ki_motion_freq, DELTA_KI]:
        matches = []
        for i, peak_freq in enumerate(peak_freqs):
            # Check for peaks at the frequency, harmonics, and as modulation sidebands
            if any(np.abs(peak_freq - freq * freq_to_check) < (freq_to_check * tolerance) for freq in [1, 2, 3]):
                matches.append((peak_freq, peak_powers[i]))
        
        if matches:
            ki_matches.append({
                'base_frequency': freq_to_check,
                'matches': matches
            })
    
    results['ki_spectral_matches'] = ki_matches
    
    # Check for wound channel signature
    # A wound channel should show Ki-modulated arctan patterns in the phase
    def wound_channel_model(t, ki_value, velocity=0.1, r0=1.0):
        return ki_value * np.arctan((t - velocity * t) / r0)
    
    # Try multiple parameter combinations
    best_corr = 0
    best_params = None
    
    for ki in [KI_REST, KI_MOTION]:
        for v in [0.01, 0.05, 0.1, 0.5]:
            for r0 in [0.1, 0.5, 1.0, 5.0]:
                model = wound_channel_model(time, ki, v, r0)
                
                # Normalize and detrend for comparison
                phase_normalized = phase - np.mean(phase)
                phase_normalized = phase_normalized - np.polyval(np.polyfit(time, phase_normalized, 1), time)
                model_normalized = model - np.mean(model)
                
                # Calculate correlation
                corr = np.abs(np.corrcoef(phase_normalized, model_normalized)[0, 1])
                if corr > best_corr:
                    best_corr = corr
                    best_params = {'ki': ki, 'velocity': v, 'r0': r0}
    
    results['wound_channel_correlation'] = best_corr
    results['wound_channel_params'] = best_params
    
    # Calculate overall Ki resonance score
    # This is a heuristic combining different indicators
    resonance_score = (
        results['ki_rest_match_percentage'] * 0.3 +
        results['ki_motion_match_percentage'] * 0.3 +
        (len(ki_matches) * 10) * 0.2 +
        (best_corr * 100) * 0.2
    )
    
    results['resonance_score'] = resonance_score
    
    return results, amplitude, phase, time, spectrum, freqs

def plot_results(results, amplitude, phase, time, spectrum, freqs, center_freq, sample_rate, output_file=None):
    """Create visualization of the Ki resonance analysis"""
    fig = plt.figure(figsize=(12, 12))
    
    # Plot 1: Time domain signal
    ax1 = fig.add_subplot(3, 1, 1)
    ax1.plot(time, amplitude)
    ax1.set_title(f"Signal Amplitude (Center Freq: {center_freq/1e6:.2f} MHz)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True)
    
    # Plot 2: Phase evolution
    ax2 = fig.add_subplot(3, 1, 2)
    # Plot phase derivative to see rate of change
    phase_derivative = np.gradient(phase, time)
    ax2.plot(time, phase_derivative)
    # Add horizontal lines at Ki values
    ax2.axhline(y=KI_REST, color='r', linestyle='--', 
                label=f'Ki_rest = {KI_REST:.5f}')
    ax2.axhline(y=KI_MOTION, color='g', linestyle='--', 
                label=f'Ki_motion = {KI_MOTION:.5f}')
    ax2.set_title("Phase Rate of Change")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("dφ/dt (rad/s)")
    ax2.legend()
    ax2.grid(True)
    
    # Calculate limits for better visualization
    ylim_mean = np.mean(phase_derivative)
    ylim_std = np.std(phase_derivative)
    ax2.set_ylim([ylim_mean - 3*ylim_std, ylim_mean + 3*ylim_std])
    
    # Plot 3: Frequency spectrum with Ki markers
    ax3 = fig.add_subplot(3, 1, 3)
    
    # Only plot positive frequencies up to 1/4 of Nyquist to zoom in on interesting region
    nyquist = sample_rate / 2
    mask = (freqs > 0) & (freqs < nyquist / 4)
    
    ax3.plot(freqs[mask], spectrum[mask])
    ax3.set_title("Frequency Spectrum with Ki-Related Frequencies")
    ax3.set_xlabel("Frequency (Hz)")
    ax3.set_ylabel("Magnitude")
    ax3.grid(True)
    
    # Add Ki-related frequencies to the spectrum
    ki_rest_freq = KI_REST / (2 * np.pi)
    ki_motion_freq = KI_MOTION / (2 * np.pi)
    
    # Mark Ki-related frequencies and harmonics
    for i, (freq, color, name) in enumerate([
            (ki_rest_freq, 'r', 'Ki_rest/(2π)'),
            (ki_motion_freq, 'g', 'Ki_motion/(2π)'),
            (DELTA_KI, 'b', 'ΔKi')
        ]):
        for j, harmonic in enumerate([1, 2, 3]):
            freq_val = harmonic * freq
            if freq_val < nyquist / 4:
                ax3.axvline(x=freq_val, color=color, 
                           linestyle='--' if j == 0 else ':',
                           label=f'{name} x{harmonic}' if j == 0 else None)
    
    ax3.legend()
    
    # Add a text box with the analysis results
    info_text = (
        f"Ki Resonance Analysis Results:\n"
        f"Mean Phase Rate: {results['mean_phase_rate']:.4f} rad/s\n"
        f"Ki_rest Matches: {results['ki_rest_match_percentage']:.2f}%\n"
        f"Ki_motion Matches: {results['ki_motion_match_percentage']:.2f}%\n"
        f"Wound Channel Correlation: {results['wound_channel_correlation']:.4f}\n"
        f"Resonance Score: {results['resonance_score']:.2f} / 100"
    )
    
    # Add spectral match information
    if results['ki_spectral_matches']:
        match_text = "\nKi-Related Spectral Components:"
        for match in results['ki_spectral_matches']:
            match_text += f"\n  {match['base_frequency']:.4f} Hz: {len(match['matches'])} matches"
        info_text += match_text
    
    plt.figtext(0.5, 0.01, info_text, ha='center', va='bottom', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout(rect=[0, 0.08, 1, 0.98])
    
    # Save plot if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300)
        print(f"Plot saved to {output_file}")
    
    return fig

def save_results_to_file(results, center_freq, sample_rate, duration, output_file):
    """Save analysis results to a text file"""
    with open(output_file, 'w') as f:
        f.write("Ki Resonance Detection Results\n")
        f.write("==============================\n\n")
        f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Center Frequency: {center_freq/1e6:.2f} MHz\n")
        f.write(f"Sample Rate: {sample_rate/1e6:.2f} Msps\n")
        f.write(f"Duration: {duration:.1f} seconds\n\n")
        
        f.write("Ki Reference Values:\n")
        f.write(f"  Ki_rest: {KI_REST:.5f}\n")
        f.write(f"  Ki_motion: {KI_MOTION:.5f}\n")
        f.write(f"  ΔKi: {DELTA_KI:.5f}\n\n")
        
        f.write("Analysis Results:\n")
        f.write(f"  Mean Phase Rate: {results['mean_phase_rate']:.4f} rad/s\n")
        f.write(f"  Ki_rest Match Percentage: {results['ki_rest_match_percentage']:.2f}%\n")
        f.write(f"  Ki_motion Match Percentage: {results['ki_motion_match_percentage']:.2f}%\n")
        
        if results['ki_spectral_matches']:
            f.write("\nKi-Related Spectral Components:\n")
            for match in results['ki_spectral_matches']:
                f.write(f"  Base Frequency: {match['base_frequency']:.4f} Hz\n")
                f.write(f"  Matches Found: {len(match['matches'])}\n")
                for freq, power in match['matches']:
                    f.write(f"    {freq:.4f} Hz (Power: {power:.2e})\n")
        
        f.write("\nWound Channel Analysis:\n")
        f.write(f"  Correlation: {results['wound_channel_correlation']:.4f}\n")
        
        if results['wound_channel_params']:
            f.write("  Best Model Parameters:\n")
            f.write(f"    Ki Value: {results['wound_channel_params']['ki']:.5f}\n")
            f.write(f"    Velocity: {results['wound_channel_params']['velocity']:.4f}\n")
            f.write(f"    r0: {results['wound_channel_params']['r0']:.4f}\n")
        
        f.write(f"\nOverall Resonance Score: {results['resonance_score']:.2f} / 100\n")
        
        # Interpretation
        f.write("\nInterpretation:\n")
        if results['resonance_score'] >= 70:
            f.write("  STRONG Ki resonance detected! High confidence in Ki-related phenomena.\n")
        elif results['resonance_score'] >= 40:
            f.write("  MODERATE Ki resonance detected. Some evidence of Ki-related patterns.\n")
        elif results['resonance_score'] >= 20:
            f.write("  WEAK Ki resonance detected. Limited evidence of Ki-related patterns.\n")
        else:
            f.write("  NO significant Ki resonance detected in this signal.\n")
    
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ki Resonance Detector for HackRF One")
    
    parser.add_argument("--freq", type=float, default=100e6,
                      help="Center frequency in Hz (default: 100 MHz)")
    parser.add_argument("--samplerate", type=float, default=2e6,
                      help="Sample rate in Hz (default: 2 MHz)")
    parser.add_argument("--gain", type=int, default=40,
                      help="RX gain in dB (default: 40)")
    parser.add_argument("--duration", type=float, default=5.0,
                      help="Capture duration in seconds (default: 5.0)")
    parser.add_argument("--sessions", type=int, default=1,
                      help="Number of capture sessions (default: 1)")
    parser.add_argument("--interval", type=float, default=0,
                      help="Interval between sessions in seconds (default: 0)")
    
    args = parser.parse_args()
    
    try:
        # Initialize HackRF
        center_freq = args.freq
        sample_rate = args.samplerate
        gain = args.gain
        duration = args.duration
        
        device = setup_hackrf(center_freq, sample_rate, gain)
        
        # Run multiple capture sessions if requested
        for session in range(1, args.sessions + 1):
            print(f"\nSession {session}/{args.sessions}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create filenames for this session
            results_file = os.path.join(output_dir, f"ki_results_{timestamp}.txt")
            plot_file = os.path.join(output_dir, f"ki_plot_{timestamp}.png")
            
            try:
                # Capture samples
                samples = capture_samples(device, duration)
                
                # Analyze for Ki resonance
                results, amplitude, phase, time, spectrum, freqs = analyze_ki_resonance(samples, sample_rate)
                
                # Generate visualizations
                plot_results(results, amplitude, phase, time, spectrum, freqs, center_freq, sample_rate, plot_file)
                
                # Save results to file
                save_results_to_file(results, center_freq, sample_rate, duration, results_file)
                
                # Simple command-line output
                print(f"\nKi Resonance Score: {results['resonance_score']:.2f} / 100")
                
                # Interpretation
                if results['resonance_score'] >= 70:
                    print("STRONG Ki resonance detected! High confidence in Ki-related phenomena.")
                elif results['resonance_score'] >= 40:
                    print("MODERATE Ki resonance detected. Some evidence of Ki-related patterns.")
                elif results['resonance_score'] >= 20:
                    print("WEAK Ki resonance detected. Limited evidence of Ki-related patterns.")
                else:
                    print("NO significant Ki resonance detected in this signal.")
                
                # Wait between sessions if needed
                if session < args.sessions and args.interval > 0:
                    print(f"Waiting {args.interval} seconds until next session...")
                    time.sleep(args.interval)
            
            except Exception as e:
                print(f"Error in capture session {session}: {str(e)}")
                continue
        
    except KeyboardInterrupt:
        print("\nCapture interrupted by user.")
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Make sure the device is properly closed
        try:
            if 'device' in locals():
                device.close()
                print("HackRF device closed.")
        except:
            pass

    print("\nKi detection complete!")