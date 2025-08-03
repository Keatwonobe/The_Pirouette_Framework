#!/usr/bin/env python3
# HackRF Ki Resonance Analyzer
# This script uses a HackRF One to capture radio signals and analyze them
# for potential Ki-related resonance patterns

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, butter, lfilter, filtfilt, decimate
import argparse
import time
import os
from datetime import datetime
from multiprocessing import Process, Queue
import queue

# Try to import HackRF libraries
try:
    import SoapySDR
    from SoapySDR import SOAPY_SDR_RX, SOAPY_SDR_CF32
    SOAPY_AVAILABLE = True
except ImportError:
    print("SoapySDR not found! Please install: pip install SoapySDR")
    SOAPY_AVAILABLE = False

# --- Constants from Pirouette Framework ---
KI_REST = 4.14159
KI_MOTION = 4.0 * np.pi / 3.0  # Approx 4.18879
DELTA_KI = KI_MOTION - KI_REST

# --- Configuration ---
DEFAULT_FREQ = 97.9e6  # Default center frequency (97.9 MHz - FM radio)
DEFAULT_SAMPLE_RATE = 2e6  # 2 MHz sample rate
DEFAULT_DURATION = 5  # 5 seconds of capture
DEFAULT_GAIN = 40  # RF gain in dB

class KiAnalyzer:
    def __init__(self, center_freq, sample_rate, duration, gain, output_dir="./ki_analysis_results"):
        self.center_freq = center_freq
        self.sample_rate = sample_rate
        self.duration = duration
        self.gain = gain
        
        # Create output directory if it doesn't exist
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp for file naming
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Log setup
        print(f"Ki Resonance Analyzer initialized:")
        print(f"  Center Frequency: {center_freq/1e6:.3f} MHz")
        print(f"  Sample Rate: {sample_rate/1e6:.1f} MHz")
        print(f"  Duration: {duration} seconds")
        print(f"  Gain: {gain} dB")
        print(f"  Output directory: {output_dir}")
    
    def setup_hackrf(self):
        """Initialize the HackRF device"""
        if not SOAPY_AVAILABLE:
            raise ImportError("SoapySDR library not available. Cannot access HackRF.")
            
        # Find all available SDR devices
        results = SoapySDR.Device.enumerate()
        if len(results) == 0:
            raise RuntimeError("No SDR devices found!")
        
        # Find HackRF
        hackrf_found = False
        for result in results:
            if 'HackRF' in result.get('driver', ''):
                hackrf_found = True
                break
                
        if not hackrf_found:
            raise RuntimeError("HackRF not found! Is it connected?")
        
        # Setup the device
        self.sdr = SoapySDR.Device(dict(driver="hackrf"))
        
        # Configure device settings
        self.sdr.setSampleRate(SOAPY_SDR_RX, 0, self.sample_rate)
        self.sdr.setFrequency(SOAPY_SDR_RX, 0, self.center_freq)
        
        # Set gain (adjust as needed)
        self.sdr.setGain(SOAPY_SDR_RX, 0, "AMP", 1 if self.gain > 0 else 0)  # Enable preamp
        self.sdr.setGain(SOAPY_SDR_RX, 0, "LNA", min(40, max(0, self.gain)))  # LNA gain
        self.sdr.setGain(SOAPY_SDR_RX, 0, "VGA", min(40, max(0, self.gain)))  # VGA gain
        
        # Setup a stream
        self.rxStream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
        
        print("HackRF successfully configured!")
        return True
        
    def capture_signal(self):
        """Capture radio signal data from HackRF"""
        # Start streaming
        self.sdr.activateStream(self.rxStream)
        
        # Calculate buffer size based on sample rate and duration
        buffer_size = int(self.sample_rate * self.duration)
        buffer = np.zeros(buffer_size, np.complex64)
        
        print(f"Starting capture for {self.duration} seconds...")
        samples_read = 0
        
        # Create a receiving buffer
        rx_buffer = np.zeros(1024, np.complex64)
        
        # Read samples in chunks
        while samples_read < buffer_size:
            remaining = buffer_size - samples_read
            this_chunk = min(len(rx_buffer), remaining)
            
            # Read from device
            sr = self.sdr.readStream(self.rxStream, [rx_buffer], this_chunk)
            
            if sr.ret > 0:
                # Copy data to our main buffer
                buffer[samples_read:samples_read + sr.ret] = rx_buffer[:sr.ret]
                samples_read += sr.ret
            else:
                print(f"Error reading from device: {sr.ret}")
                break
        
        # Cleanup
        self.sdr.deactivateStream(self.rxStream)
        self.sdr.closeStream(self.rxStream)
        
        print(f"Captured {samples_read} samples ({samples_read/self.sample_rate:.2f} seconds)")
        
        # Save raw data to file
        raw_file = os.path.join(self.output_dir, f"{self.timestamp}_raw_capture.npy")
        np.save(raw_file, buffer)
        print(f"Raw data saved to {raw_file}")
        
        return buffer
    
    def preprocess_signal(self, raw_signal):
        """Preprocess the captured signal for analysis"""
        # Convert complex data to real by taking magnitude
        # (this simplifies for amplitude analysis - phase will be handled separately)
        magnitude = np.abs(raw_signal)
        
        # Decimate signal to reduce processing load (if needed)
        decimation_factor = max(1, int(self.sample_rate / 200000))  # Target ~200kHz sample rate
        if decimation_factor > 1:
            print(f"Decimating signal by factor of {decimation_factor}")
            preprocessed = decimate(magnitude, decimation_factor)
        else:
            preprocessed = magnitude
            
        # Calculate effective sample rate after decimation
        effective_sample_rate = self.sample_rate / decimation_factor
        
        # Create time array
        time_array = np.arange(len(preprocessed)) / effective_sample_rate
        
        # Return preprocessed signal and metadata
        return {
            'signal': preprocessed,
            'time': time_array,
            'sample_rate': effective_sample_rate,
            'original_signal': raw_signal
        }
    
    def extract_phase(self, signal_data):
        """Extract instantaneous phase using Hilbert transform"""
        # Apply Hilbert transform to get analytic signal
        analytic_signal = hilbert(signal_data)
        
        # Extract instantaneous phase
        instantaneous_phase = np.unwrap(np.angle(analytic_signal))
        
        return instantaneous_phase
    
    def analyze_phase_evolution_rate(self, phase, time, sample_rate):
        """
        Analyze the rate of change of phase (instantaneous frequency deviation)
        Looks for potential relationships with Ki constants
        """
        # Calculate phase rate of change (derivative)
        phase_rate_of_change = np.gradient(phase, time)  # d(phase)/dt
        
        # Check if phase rate is close to Ki values
        tolerance = 0.1
        rest_rate_matches = np.isclose(phase_rate_of_change, KI_REST, atol=tolerance)
        motion_rate_matches = np.isclose(phase_rate_of_change, KI_MOTION, atol=tolerance)
        
        # Calculate percentage of points matching Ki values
        percent_rest = np.sum(rest_rate_matches) / len(phase) * 100
        percent_motion = np.sum(motion_rate_matches) / len(phase) * 100
        
        # Check for segments with consistent Ki-related rates
        # (More reliable than individual point matches)
        segment_length = int(sample_rate * 0.01)  # 10ms segments
        segment_count = len(phase) // segment_length
        
        rest_segments = 0
        motion_segments = 0
        
        for i in range(segment_count):
            start_idx = i * segment_length
            end_idx = start_idx + segment_length
            
            segment_rate = np.mean(phase_rate_of_change[start_idx:end_idx])
            
            if abs(segment_rate - KI_REST) < tolerance:
                rest_segments += 1
                
            if abs(segment_rate - KI_MOTION) < tolerance:
                motion_segments += 1
        
        # Print results  
        print(f"\n--- Phase Evolution Rate Analysis ---")
        print(f"Average phase rate (d(phase)/dt): {np.mean(phase_rate_of_change):.4f} rad/s")
        print(f"Points near Ki_rest ({KI_REST:.4f}): {np.sum(rest_rate_matches)} ({percent_rest:.2f}%)")
        print(f"Points near Ki_motion ({KI_MOTION:.4f}): {np.sum(motion_rate_matches)} ({percent_motion:.2f}%)")
        print(f"Segments near Ki_rest: {rest_segments} ({rest_segments/segment_count*100:.2f}%)")
        print(f"Segments near Ki_motion: {motion_segments} ({motion_segments/segment_count*100:.2f}%)")
        
        # Calculate significance score
        significance_score = max(percent_rest, percent_motion) * (max(rest_segments, motion_segments) / segment_count)
        print(f"Ki Phase Rate Significance Score: {significance_score:.2f}")
        
        # Create and save plot
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 1, 1)
        plt.plot(time, phase, label='Phase (rad)')
        plt.title('Signal Phase and Rate of Change')
        plt.ylabel('Phase (rad)')
        plt.grid(True)
        plt.legend()
        
        plt.subplot(2, 1, 2)
        plt.plot(time, phase_rate_of_change, label='d(Phase)/dt (rad/s)', alpha=0.7)
        plt.axhline(KI_REST, color='r', linestyle='--', label=f'Ki_rest ({KI_REST:.2f})')
        plt.axhline(KI_MOTION, color='g', linestyle='--', label=f'Ki_motion ({KI_MOTION:.2f})')
        
        # Highlight matching regions
        if np.any(rest_rate_matches):
            plt.scatter(time[rest_rate_matches], phase_rate_of_change[rest_rate_matches], 
                        color='r', s=5, alpha=0.3, label=f'Ki_rest matches ({percent_rest:.1f}%)')
        
        if np.any(motion_rate_matches):
            plt.scatter(time[motion_rate_matches], phase_rate_of_change[motion_rate_matches], 
                        color='g', s=5, alpha=0.3, label=f'Ki_motion matches ({percent_motion:.1f}%)')
            
        plt.xlabel('Time (s)')
        plt.ylabel('Phase Rate (rad/s)')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        
        # Save plot
        plot_file = os.path.join(self.output_dir, f"{self.timestamp}_phase_evolution.png")
        plt.savefig(plot_file, dpi=150)
        print(f"Phase evolution plot saved to {plot_file}")
        
        return {
            'phase_rate': phase_rate_of_change,
            'rest_match_percent': percent_rest,
            'motion_match_percent': percent_motion,
            'rest_segments': rest_segments,
            'motion_segments': motion_segments,
            'significance_score': significance_score
        }
    
    def detect_ki_modulation(self, signal_data, time, sample_rate):
        """
        Look for modulation patterns potentially related to Ki resonances.
        This analysis focuses on frequency domain analysis.
        """
        print(f"\n--- Ki Modulation Detection ---")
        
        # Compute FFT
        fft_result = np.fft.fft(signal_data)
        fft_freq = np.fft.fftfreq(len(signal_data), 1/sample_rate)
        
        # Focus on positive frequencies
        positive_freq_indices = fft_freq > 0
        fft_freq_pos = fft_freq[positive_freq_indices]
        fft_magnitude = np.abs(fft_result[positive_freq_indices])
        
        # Normalize magnitude
        fft_magnitude_norm = fft_magnitude / np.max(fft_magnitude)
        
        # Define frequencies of interest related to Ki constants
        # These could manifest as modulation frequencies
        ki_related_freqs = {
            'DELTA_KI': DELTA_KI / (2 * np.pi),  # ~0.0075 Hz (very low)
            'KI_REST_2PI': KI_REST / (2 * np.pi),  # ~0.66 Hz
            'KI_MOTION_2PI': KI_MOTION / (2 * np.pi),  # ~0.67 Hz
            'HARMONIC_1': KI_REST,  # ~4.14 Hz
            'HARMONIC_2': KI_MOTION,  # ~4.19 Hz
            'HARMONIC_3': 3 * KI_REST / (2 * np.pi),  # ~1.98 Hz
            'HARMONIC_4': 3 * KI_MOTION / (2 * np.pi)  # ~2.00 Hz
        }
        
        # Search for peaks near Ki-related frequencies
        tolerance = 0.01  # Hz
        ki_peaks = {}
        
        for name, freq in ki_related_freqs.items():
            # Find closest frequency bin
            closest_idx = np.argmin(np.abs(fft_freq_pos - freq))
            closest_freq = fft_freq_pos[closest_idx]
            
            # Check if within tolerance
            if abs(closest_freq - freq) < tolerance:
                # Check if it's a peak (higher than neighbors)
                if closest_idx > 0 and closest_idx < len(fft_magnitude_norm) - 1:
                    if (fft_magnitude_norm[closest_idx] > fft_magnitude_norm[closest_idx - 1] and
                        fft_magnitude_norm[closest_idx] > fft_magnitude_norm[closest_idx + 1]):
                        
                        # Store peak information
                        ki_peaks[name] = {
                            'expected_freq': freq,
                            'actual_freq': closest_freq,
                            'magnitude': fft_magnitude_norm[closest_idx],
                            'index': closest_idx
                        }
                        
                        print(f"Found peak near {name} frequency: {closest_freq:.6f} Hz (expected {freq:.6f} Hz)")
        
        # Calculate significance score based on number and strength of Ki-related peaks
        if ki_peaks:
            total_magnitude = sum(peak['magnitude'] for peak in ki_peaks.values())
            peak_count_factor = len(ki_peaks) / len(ki_related_freqs)
            
            significance_score = total_magnitude * peak_count_factor * 100
            print(f"Found {len(ki_peaks)} Ki-related frequency peaks")
            print(f"Ki Modulation Significance Score: {significance_score:.2f}")
        else:
            significance_score = 0
            print("No significant Ki-related frequency peaks found")
        
        # Create and save plot
        plt.figure(figsize=(12, 8))
        
        # Plot full spectrum (log scale)
        plt.subplot(2, 1, 1)
        plt.semilogy(fft_freq_pos, fft_magnitude_norm, label='Normalized Magnitude')
        plt.title('Signal Spectrum with Ki-Related Frequencies')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude (log scale)')
        plt.grid(True, which='both', alpha=0.3)
        
        # Add vertical lines for Ki-related frequencies
        for name, freq in ki_related_freqs.items():
            plt.axvline(freq, color='r', linestyle=':', alpha=0.5)
            plt.text(freq, 0.1, name, rotation=90, verticalalignment='bottom')
        
        # Plot zoomed in around the detected peaks
        plt.subplot(2, 1, 2)
        
        # Determine zoom range
        if ki_peaks:
            min_peak_freq = min(peak['actual_freq'] for peak in ki_peaks.values())
            max_peak_freq = max(peak['actual_freq'] for peak in ki_peaks.values())
            
            # Expand range by 20%
            range_width = max_peak_freq - min_peak_freq
            min_freq = max(0, min_peak_freq - range_width * 0.2)
            max_freq = max_peak_freq + range_width * 0.2
            
            # Ensure minimum range size
            if max_freq - min_freq < 1:
                center = (min_freq + max_freq) / 2
                min_freq = center - 0.5
                max_freq = center + 0.5
        else:
            # Default zoom range if no peaks found
            min_freq = 0
            max_freq = 5  # Hz
        
        # Filter data for zoom range
        zoom_mask = (fft_freq_pos >= min_freq) & (fft_freq_pos <= max_freq)
        zoom_freq = fft_freq_pos[zoom_mask]
        zoom_magnitude = fft_magnitude_norm[zoom_mask]
        
        plt.plot(zoom_freq, zoom_magnitude)
        plt.title('Zoomed Signal Spectrum near Ki-Related Frequencies')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Normalized Magnitude')
        plt.grid(True)
        
        # Mark the detected peaks
        for name, peak in ki_peaks.items():
            plt.plot(peak['actual_freq'], peak['magnitude'], 'ro')
            plt.annotate(
                name, 
                xy=(peak['actual_freq'], peak['magnitude']),
                xytext=(5, 10),
                textcoords='offset points',
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2')
            )
        
        plt.tight_layout()
        
        # Save plot
        plot_file = os.path.join(self.output_dir, f"{self.timestamp}_ki_modulation.png")
        plt.savefig(plot_file, dpi=150)
        print(f"Spectrum analysis plot saved to {plot_file}")
        
        return {
            'ki_peaks': ki_peaks,
            'significance_score': significance_score
        }
    
    def check_wound_channel_signature(self, phase, time, sample_rate):
        """
        Check if phase evolution matches potential wound channel signatures.
        Based on Ki * arctan((z - vt)/r0) pattern expected in wound channels.
        """
        print(f"\n--- Wound Channel Signature Analysis ---")
        
        # Define a range of velocities and scales to test
        velocities = np.linspace(0.1, 0.9, 5)
        r0_values = np.linspace(0.1, 2.0, 5)
        
        # Remove linear trend from phase for better comparison
        phase_detrended = phase - np.polyval(np.polyfit(time, phase, 1), time)
        
        # Normalize for correlation calculation
        phase_normalized = (phase_detrended - np.mean(phase_detrended)) / np.std(phase_detrended)
        
        best_corr_rest = -np.inf
        best_params_rest = None
        best_model_rest = None
        
        best_corr_motion = -np.inf
        best_params_motion = None
        best_model_motion = None
        
        # Test different parameter combinations
        for velocity in velocities:
            for r0 in r0_values:
                # Create model phases for both Ki values
                model_rest = KI_REST * np.arctan((time - velocity * time) / r0)
                model_motion = KI_MOTION * np.arctan((time - velocity * time) / r0)
                
                # Normalize models
                model_rest = (model_rest - np.mean(model_rest)) / np.std(model_rest)
                model_motion = (model_motion - np.mean(model_motion)) / np.std(model_motion)
                
                # Calculate correlations
                corr_rest = np.corrcoef(phase_normalized, model_rest)[0, 1]
                corr_motion = np.corrcoef(phase_normalized, model_motion)[0, 1]
                
                # Update best parameters for rest model
                if corr_rest > best_corr_rest:
                    best_corr_rest = corr_rest
                    best_params_rest = (velocity, r0)
                    best_model_rest = model_rest
                
                # Update best parameters for motion model
                if corr_motion > best_corr_motion:
                    best_corr_motion = corr_motion
                    best_params_motion = (velocity, r0)
                    best_model_motion = model_motion
        
        # Determine which model is better
        if best_corr_rest > best_corr_motion:
            best_model = "Ki_rest"
            best_corr = best_corr_rest
            best_params = best_params_rest
            best_matched_model = best_model_rest
        else:
            best_model = "Ki_motion"
            best_corr = best_corr_motion
            best_params = best_params_motion
            best_matched_model = best_model_motion
        
        # Calculate significance based on correlation
        # Correlation of 0.7 or higher is considered significant
        significance_score = max(0, (best_corr - 0.5) * 2) * 100
        
        print(f"Best wound channel match: {best_model}")
        print(f"Correlation: {best_corr:.4f}")
        print(f"Parameters: velocity={best_params[0]:.2f}, r0={best_params[1]:.2f}")
        print(f"Wound Channel Signature Significance Score: {significance_score:.2f}")
        
        # Create and save plot
        plt.figure(figsize=(12, 6))
        
        plt.plot(time, phase_normalized, label='Normalized Phase')
        plt.plot(time, best_matched_model, 
                 label=f'Best {best_model} Model (corr={best_corr:.3f})', 
                 linestyle='--')
        
        plt.title('Wound Channel Signature Analysis')
        plt.xlabel('Time (s)')
        plt.ylabel('Normalized Phase')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        
        # Save plot
        plot_file = os.path.join(self.output_dir, f"{self.timestamp}_wound_channel.png")
        plt.savefig(plot_file, dpi=150)
        print(f"Wound channel analysis plot saved to {plot_file}")
        
        return {
            'best_model': best_model,
            'correlation': best_corr,
            'parameters': best_params,
            'significance_score': significance_score
        }
    
    def run_full_analysis(self):
        """Run complete Ki resonance analysis on captured signal"""
        try:
            print("\n=== Starting HackRF capture and Ki resonance analysis ===")
            
            # Setup HackRF
            self.setup_hackrf()
            
            # Capture signal
            raw_signal = self.capture_signal()
            
            # Preprocess signal
            processed = self.preprocess_signal(raw_signal)
            
            # Extract phase information
            phase = self.extract_phase(processed['signal'])
            
            # Run the three main analyses
            phase_results = self.analyze_phase_evolution_rate(
                phase, processed['time'], processed['sample_rate']
            )
            
            modulation_results = self.detect_ki_modulation(
                processed['signal'], processed['time'], processed['sample_rate']
            )
            
            wound_channel_results = self.check_wound_channel_signature(
                phase, processed['time'], processed['sample_rate']
            )
            
            # Calculate combined significance score
            combined_score = (
                phase_results['significance_score'] +
                modulation_results['significance_score'] +
                wound_channel_results['significance_score']
            ) / 3
            
            print("\n=== Analysis Complete ===")
            print(f"Combined Ki Resonance Significance Score: {combined_score:.2f}/100")
            
            # Interpretation
            if combined_score > 80:
                print("Interpretation: VERY STRONG evidence of Ki-related resonance patterns")
            elif combined_score > 60:
                print("Interpretation: STRONG evidence of Ki-related resonance patterns")
            elif combined_score > 40:
                print("Interpretation: MODERATE evidence of Ki-related resonance patterns")
            elif combined_score > 20:
                print("Interpretation: WEAK evidence of Ki-related resonance patterns")
            else:
                print("Interpretation: NO significant evidence of Ki-related resonance patterns")
            
            # Create summary plot
            plt.figure(figsize=(12, 10))
            
            # Raw signal
            plt.subplot(3, 1, 1)
            plt.plot(processed['time'], processed['signal'])
            plt.title(f'Radio Signal Analysis: {self.center_freq/1e6:.3f} MHz')
            plt.ylabel('Amplitude')
            plt.grid(True)
            
            # Phase evolution
            plt.subplot(3, 1, 2)
            plt.plot(processed['time'], phase, label='Phase')
            plt.title(f'Phase Evolution (Score: {phase_results["significance_score"]:.1f}/100)')
            plt.ylabel('Phase (rad)')
            plt.grid(True)
            
            # Significance scores
            plt.subplot(3, 1, 3)
            scores = [
                phase_results['significance_score'],
                modulation_results['significance_score'],
                wound_channel_results['significance_score'],
                combined_score
            ]
            labels = ['Phase Rate', 'Ki Modulation', 'Wound Channel', 'Combined']
            
            plt.bar(labels, scores)
            plt.axhline(y=40, color='r', linestyle='--', alpha=0.7, label='Significance Threshold')
            plt.ylabel('Significance Score')
            plt.title('Ki Resonance Detection Scores')
            plt.ylim(0, 100)
            
            plt.tight_layout()
            
            # Save summary plot
            summary_file = os.path.join(self.output_dir, f"{self.timestamp}_summary.png")
            plt.savefig(summary_file, dpi=150)
            print(f"Summary plot saved to {summary_file}")
            
            # Save results to a text file
            results_file = os.path.join(self.output_dir, f"{self.timestamp}_results.txt")
            with open(results_file, 'w') as f:
                f.write("=== Ki Resonance Analysis Results ===\n")
                f.write(f"Timestamp: {self.timestamp}\n")
                f.write(f"Center Frequency: {self.center_freq/1e6:.3f} MHz\n")
                f.write(f"Sample Rate: {self.sample_rate/1e6:.1f} MHz\n")
                f.write(f"Duration: {self.duration} seconds\n\n")
                
                f.write("--- Phase Evolution Analysis ---\n")
                f.write(f"Ki_rest Match: {phase_results['rest_match_percent']:.2f}%\n")
                f.write(f"Ki_motion Match: {phase_results['motion_match_percent']:.2f}%\n")
                f.write(f"Significance Score: {phase_results['significance_score']:.2f}\n\n")
                
                f.write("--- Ki Modulation Analysis ---\n")
                f.write(f"Ki-related peaks found: {len(modulation_results['ki_peaks'])}\n")
                for name, peak in modulation_results['ki_peaks'].items():
                    f.write(f"  {name}: {peak['actual_freq']:.6f} Hz (mag: {peak['magnitude']:.4f})\n")
                f.write(f"Significance Score: {modulation_results['significance_score']:.2f}\n\n")
                
                f.write("--- Wound Channel Analysis ---\n")
                f.write(f"Best model: {wound_channel_results['best_model']}\n")
                f.write(f"Correlation: {wound_channel_results['correlation']:.4f}\n")
                f.write(f"Parameters: v={wound_channel_results['parameters'][0]:.2f}, r0={wound_channel_results['parameters'][1]:.2f}\n")
                f.write(f"Significance Score: {wound_channel_results['significance_score']:.2f}\n\n")
                
                f.write("--- Overall Results ---\n")
                f.write(f"Combined Score: {combined_score:.2f}/100\n")
                
                if combined_score > 80:
                    f.write("Interpretation: VERY STRONG evidence of Ki-related resonance patterns\n")
                elif combined_score > 60:
                    f.write("Interpretation: STRONG evidence of Ki-related resonance patterns\n")
                elif combined_score > 40:
                    f.write("Interpretation: MODERATE evidence of Ki-related resonance patterns\n")
                elif combined_score > 20:
                    f.write("Interpretation: WEAK evidence of Ki-related resonance patterns\n")
                else:
                    f.write("Interpretation: NO significant evidence of Ki-related resonance patterns\n")
            
            print(f"Results saved to {results_file}")
            return