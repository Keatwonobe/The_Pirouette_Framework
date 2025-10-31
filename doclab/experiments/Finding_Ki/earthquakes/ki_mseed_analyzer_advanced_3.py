import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from datetime import datetime
from scipy import signal
from scipy.stats import kurtosis, skew
from obspy import read, Stream, Trace
from multiprocessing import Pool, cpu_count
import platform
import tqdm

# Constants
KI_REST = 4.14159      # Ki in rest state
KI_MOTION = 4.18879    # Ki in motion state (approximately 4π/3)
DEFAULT_BAND_WIDTH = 0.05  # Default bandwidth for analysis


class KiAnalyzer:
    """
    Class for analyzing miniseed files for evidence of Ki-related phenomena
    """
    
    def __init__(self, ki_value=KI_MOTION, band_width=DEFAULT_BAND_WIDTH, 
                 output_dir=None, significance_threshold=3.0, p_value_threshold=0.001,
                 q_factor=40):
        """
        Initialize the analyzer
        
        Parameters:
        -----------
        ki_value : float
            The Ki value to search for (default: KI_MOTION)
        band_width : float
            Width of frequency band to analyze around Ki value
        output_dir : str
            Directory for saving results (default: 'ki_analysis_results')
        significance_threshold : float
            Number of standard deviations above mean to consider significant
        p_value_threshold : float
            P-value threshold for significance (default: 0.001)
        q_factor : float
            Q-factor for dynamic bandwidth calculation (default: 40)
        """
        self.ki_value = ki_value
        self.static_band_width = band_width
        self.q_factor = q_factor
        self.band_width = self.calculate_dynamic_bandwidth(ki_value, q_factor)
        
        # Create output directory
        if output_dir is None:
            self.output_dir = Path('ki_analysis_results')
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Create subdirectories
        self.plots_dir = self.output_dir / 'plots'
        self.data_dir = self.output_dir / 'data'
        self.reports_dir = self.output_dir / 'reports'
        
        for directory in [self.plots_dir, self.data_dir, self.reports_dir]:
            directory.mkdir(exist_ok=True)
            
        self.significance_threshold = significance_threshold
        self.p_value_threshold = p_value_threshold
        self.session_start_time = datetime.now()
        self.session_id = self.session_start_time.strftime("%Y%m%d_%H%M%S")
        
        # Initialize results container
        self.results = []
        self.all_energy_ratios = []
        
        # Track processed files
        self.processed_files = []
        self.processed_file_count = 0
        
    def calculate_dynamic_bandwidth(self, ki_value, q_factor=40):
        """
        Calculate a dynamic bandwidth based on a Q-factor
        
        Parameters:
        -----------
        ki_value : float
            The Ki value to analyze
        q_factor : float
            Q-factor for the bandwidth calculation
            
        Returns:
        --------
        float
            Dynamic bandwidth
        """
        # Ensure minimum bandwidth of 0.05 Hz
        return max(0.05, 0.5 * ki_value / q_factor)
    
    def compute_psd(self, data, fs, method='welch', nperseg=None, window='hann', **kwargs):
        """
        Compute power spectral density using various methods
        
        Parameters:
        -----------
        data : array
            Time series data
        fs : float
            Sampling frequency
        method : str
            Method to use: 'fft', 'welch', or 'multitaper'
        nperseg : int or None
            Length of each segment (default: min(4096, len(data)//8))
        window : str or tuple
            Window function to use
        **kwargs : dict
            Additional arguments for the specific method
            
        Returns:
        --------
        freqs : array
            Frequency values
        psd : array
            Power spectral density values
        """
        if nperseg is None:
            nperseg = min(4096, len(data)//8)
        
        if method == 'fft':
            # Apply window before FFT
            if window == 'hann':
                win = np.hanning(len(data))
            elif window == 'hamming':
                win = np.hamming(len(data))
            else:
                win = signal.get_window(window, len(data))
            
            windowed_data = data * win
            fft_vals = np.abs(np.fft.rfft(windowed_data))**2
            freqs = np.fft.rfftfreq(len(data), d=1/fs)
            
            # Normalize for power
            fft_vals = fft_vals / np.sum(win**2) * 2
            
            return freqs, fft_vals
            
        elif method == 'welch':
            freqs, psd = signal.welch(data, fs, window=window, nperseg=nperseg, **kwargs)
            return freqs, psd
            
        elif method == 'multitaper':
            try:
                from scipy.signal import mtspectrum
                freqs, psd = mtspectrum(data, fs, **kwargs)
                return freqs, psd
            except (ImportError, AttributeError):
                try:
                    from spectrum import pmtm
                    psd, freqs = pmtm(data, fs, **kwargs)
                    return freqs, psd
                except ImportError:
                    print("Multitaper method requested but not available. Falling back to Welch.")
                    return self.compute_psd(data, fs, method='welch', nperseg=nperseg, window=window)
        
        else:
            raise ValueError(f"Unknown PSD method: {method}")
    
    def compute_local_baseline(self, freqs, psd_vals, ki_min, ki_max, expansion_factor=1.0):
        """
        Compute a local baseline for significance testing
        
        Parameters:
        -----------
        freqs : array
            Frequency values
        psd_vals : array
            Power spectral density values
        ki_min : float
            Lower bound of Ki frequency band
        ki_max : float
            Upper bound of Ki frequency band
        expansion_factor : float
            Factor to expand the exclusion band (default: 1.0)
            
        Returns:
        --------
        float
            Local baseline value
        """
        # Define the band mask with expanded bounds
        expanded_min = ki_min - expansion_factor * self.band_width
        expanded_max = ki_max + expansion_factor * self.band_width
        
        # Create mask that excludes the expanded Ki band
        band_mask = (freqs >= expanded_min) & (freqs <= expanded_max)
        
        # Get values outside the expanded band
        local_ref = psd_vals[~band_mask]
        
        if len(local_ref) == 0:
            # If all frequencies are in the band, fall back to global
            return np.mean(psd_vals) + self.significance_threshold * np.std(psd_vals)
        
        # Compute local baseline
        local_baseline = np.mean(local_ref) + self.significance_threshold * np.std(local_ref)
        
        return local_baseline
    
    def compute_empirical_p_value(self, energy_ratio, all_ratios):
        """
        Compute empirical p-value for an energy ratio
        
        Parameters:
        -----------
        energy_ratio : float
            Energy ratio to evaluate
        all_ratios : array
            Distribution of all energy ratios observed
            
        Returns:
        --------
        float
            Empirical p-value
        """
        if len(all_ratios) == 0:
            return 1.0
            
        # Count how many ratios are greater than or equal to this one
        count_greater = np.sum(np.array(all_ratios) >= energy_ratio)
        
        # Compute empirical p-value
        p_value = count_greater / len(all_ratios)
        
        return p_value
        
    def process_file(self, file_path, save_plots=True, psd_method='welch', 
                    permutation_test=False, nperseg=None):
        """
        Process a single miniseed file
    
        Parameters:
        -----------
        file_path : str or Path
            Path to the miniseed file
        save_plots : bool
            Whether to save plots for the file
        psd_method : str
            Method to use for PSD estimation
        permutation_test : bool
            Whether to perform permutation test
        nperseg : int or None
            Length of each segment for welch/multitaper methods
        
        Returns:
        --------
        list
            List of detection results from the file
        """
        file_path = Path(file_path)
        file_results = []
    
        try:
            # Read the miniseed file
            st = read(str(file_path), headonly=False)
        
            # Process each trace in the file
            for tr in st:
                # Only pass the expected arguments to analyze_trace
                trace_results = self.analyze_trace(tr, file_path.name, save_plots)
                if trace_results:
                    file_results.extend(trace_results)
        
            # Save summary for this file if we found anything
            if file_results and save_plots:
                self.save_file_summary(file_path, st, file_results)
            
            # Track the processed file
            if file_path not in self.processed_files:
                self.processed_files.append(file_path)
                self.processed_file_count += 1
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
        
        return file_results
    
    def analyze_trace(self, tr, filename, save_plots=True, psd_method='welch', 
                 permutation_test=False, nperseg=None):
        """
        Enhanced analysis of a single trace for complex Ki-related phenomena
    
        Parameters:
        -----------
        tr : obspy.Trace
            The trace to analyze
        filename : str
            Original filename for reference
        save_plots : bool
            Whether to save plots for this trace
        
        Returns:
        --------
        list
            List of detection results from the trace
        """
        trace_results = []
    
        try:
            # Basic preprocessing
            tr_processed = tr.copy()
            tr_processed.detrend("demean")
            tr_processed.detrend("linear")
        
            # Define frequency ranges
            ki_center = self.ki_value
            ki_bandwidth = self.band_width
            ki_min = ki_center - ki_bandwidth
            ki_max = ki_center + ki_bandwidth
        
            # Apply bandpass filter around frequencies of interest
            tr_filtered = tr_processed.copy()
            analysis_min = max(0.01, ki_center - 2 * ki_bandwidth)
            analysis_max = ki_center + 2 * ki_bandwidth
            tr_filtered.filter('bandpass', freqmin=analysis_min, freqmax=analysis_max, corners=4)
        
            # Compute FFT for spectral analysis
            n = len(tr_processed.data)
            dt = tr_processed.stats.delta
            fs = 1/dt  # Sampling frequency
            freqs = np.fft.rfftfreq(n, d=dt)
            fft_vals = np.abs(np.fft.rfft(tr_processed.data))
        
            # Compute phase information
            fft_complex = np.fft.rfft(tr_processed.data)
            phase_vals = np.angle(fft_complex)
        
            # Compute spectrogram
            nperseg = min(256, n // 8)
            f, t, Sxx = signal.spectrogram(tr_processed.data, fs, nperseg=nperseg)
        
            # 1. Amplitude Modulation Detection
            # Apply Hilbert transform to get the analytic signal
            analytic_signal = signal.hilbert(tr_filtered.data)
            amplitude_envelope = np.abs(analytic_signal)
            instantaneous_phase = np.unwrap(np.angle(analytic_signal))
            instantaneous_frequency = np.diff(instantaneous_phase) / (2.0 * np.pi * dt)
        
            # Look for modulation at Ki frequency by analyzing the envelope
            envelope_freqs = np.fft.rfftfreq(len(amplitude_envelope), d=dt)
            envelope_fft = np.abs(np.fft.rfft(amplitude_envelope))
        
            # Check for modulation near Ki frequency
            mod_band = (envelope_freqs >= ki_min) & (envelope_freqs <= ki_max)
            mod_energy = np.mean(envelope_fft[mod_band]) if np.any(mod_band) else 0
            mod_baseline = np.mean(envelope_fft) + self.significance_threshold * np.std(envelope_fft)
            mod_ratio = mod_energy / (np.mean(envelope_fft) + 1e-10)
        
            # 2. Phase Relationship Analysis
            # Compute phase coherence in the Ki band
            ki_band_indices = np.where((freqs >= ki_min) & (freqs <= ki_max))[0]
            if len(ki_band_indices) > 1:
                phase_diff = np.diff(phase_vals[ki_band_indices])
                phase_coherence = np.abs(np.mean(np.exp(1j * phase_diff)))
            else:
                phase_coherence = 0
            
            # 3. Harmonic Structure Detection
            # Search for harmonics and subharmonics of Ki
            harmonics = []
            subharmonics = []
            harmonics_strength = 0
        
            # Check frequency ranges up to 5th harmonic
            for i in range(2, 6):
                harm_center = ki_center * i
                harm_min = harm_center - ki_bandwidth
                harm_max = harm_center + ki_bandwidth
            
                # Only check if within Nyquist frequency
                if harm_max < fs/2:
                    harm_band = (freqs >= harm_min) & (freqs <= harm_max)
                    if np.any(harm_band):
                        harm_peak = np.max(fft_vals[harm_band])
                        harm_peak_freq = freqs[harm_band][np.argmax(fft_vals[harm_band])]
                        harm_ratio = harm_peak / (np.mean(fft_vals) + 1e-10)
                    
                        if harm_ratio > self.significance_threshold:
                            harmonics.append((i, harm_peak_freq, harm_ratio))
                            harmonics_strength += harm_ratio
        
            # Check for subharmonics
            for i in range(2, 6):
                sub_center = ki_center / i
                sub_min = sub_center - ki_bandwidth/2  # Narrower band for subharmonics
                sub_max = sub_center + ki_bandwidth/2
            
                sub_band = (freqs >= sub_min) & (freqs <= sub_max)
                if np.any(sub_band):
                    sub_peak = np.max(fft_vals[sub_band])
                    sub_peak_freq = freqs[sub_band][np.argmax(fft_vals[sub_band])]
                    sub_ratio = sub_peak / (np.mean(fft_vals) + 1e-10)
                
                    if sub_ratio > self.significance_threshold:
                        subharmonics.append((1/i, sub_peak_freq, sub_ratio))
        
            # 4. Frequency Band Correlation Analysis
            # Divide spectrum into bands and analyze correlation between them
            band_correlations = []
            band_width = ki_bandwidth * 2
            num_bands = min(10, int(fs/(2*band_width)))  # Up to 10 bands, but limited by Nyquist
        
            if num_bands > 1:
                # Create band-filtered signals
                band_signals = []
                for i in range(num_bands):
                    band_min = i * band_width
                    band_max = (i + 1) * band_width
                    if band_max > fs/2:  # Ensure we don't exceed Nyquist
                        break
                    if band_min <= 0:
                        band_min = 0.01  # Set minimum frequency to a small positive value


                    band_tr = tr_processed.copy()
                    band_tr.filter('bandpass', freqmin=band_min, freqmax=band_max, corners=4)
                    band_signals.append(band_tr.data)
            
                # Compute correlation matrix between bands
                corr_matrix = np.corrcoef(band_signals)
            
                # Find bands with high correlation
                for i in range(len(corr_matrix)):
                    for j in range(i+1, len(corr_matrix)):
                        if abs(corr_matrix[i, j]) > 0.7:  # Threshold for significant correlation
                            band_correlations.append((i, j, corr_matrix[i, j]))
        
            # 5. Wavelet Analysis for Time-Localized Phenomena
            # Using continuous wavelet transform to detect time-localized resonances
            wavelet_results = self.perform_wavelet_analysis(tr_processed.data, dt, ki_center)
        
            # Combine detection metrics
            detection_score = 0
            detection_metrics = {}
        
            # Original FFT-based detection
            ki_band = (freqs >= ki_min) & (freqs <= ki_max)
            if np.any(ki_band):
                band_energy = np.mean(fft_vals[ki_band])
                baseline = np.mean(fft_vals) + self.significance_threshold * np.std(fft_vals)
                energy_ratio = band_energy / (np.mean(fft_vals) + 1e-10)
                peak_freq = freqs[ki_band][np.argmax(fft_vals[ki_band])]
                peak_value = np.max(fft_vals[ki_band])
            
                detection_metrics['fft_energy_ratio'] = energy_ratio
                detection_score += energy_ratio
            else:
                band_energy = 0
                baseline = 0
                energy_ratio = 0
                peak_freq = 0
                peak_value = 0
                detection_metrics['fft_energy_ratio'] = 0
        
            # Add new detection metrics
            detection_metrics['modulation_ratio'] = mod_ratio
            detection_score += mod_ratio * 1.5  # Giving extra weight to modulation
        
            detection_metrics['phase_coherence'] = phase_coherence
            detection_score += phase_coherence * 1.2
        
            detection_metrics['harmonics_strength'] = harmonics_strength
            detection_score += harmonics_strength * 1.1
        
            detection_metrics['wavelet_score'] = wavelet_results['wavelet_score']
            detection_score += wavelet_results['wavelet_score'] * 1.3
        
            # Additional statistics from original code
            band_kurtosis = kurtosis(fft_vals[ki_band]) if np.any(ki_band) else 0
            band_skew = skew(fft_vals[ki_band]) if np.any(ki_band) else 0
        
            # Calculate temporal Ki signatures
            envelope = np.abs(signal.hilbert(tr_filtered.data))
            envelope_mean = np.mean(envelope)
            envelope_std = np.std(envelope)
            envelope_max = np.max(envelope)
        
            # Check if this exceeds our threshold for significance
            detection_threshold = self.significance_threshold * 1.5  # Adjusted threshold for combined metrics
        
            if detection_score > detection_threshold:
                # Format the results
                detection = {
                    'filename': filename,
                    'trace_id': tr.id,
                    'start_time': tr.stats.starttime,
                    'end_time': tr.stats.endtime,
                    'duration': tr.stats.endtime - tr.stats.starttime,
                    'sampling_rate': tr.stats.sampling_rate,
                    'detection_score': detection_score,
                    'fft_energy_ratio': detection_metrics['fft_energy_ratio'],
                    'modulation_ratio': detection_metrics['modulation_ratio'],
                    'phase_coherence': detection_metrics['phase_coherence'],
                    'harmonics_strength': detection_metrics['harmonics_strength'],
                    'wavelet_score': detection_metrics['wavelet_score'],
                    'band_energy': band_energy,
                    'baseline': baseline,
                    'peak_freq': peak_freq,
                    'peak_value': peak_value,
                    'ki_distance': abs(peak_freq - self.ki_value) if peak_freq else float('inf'),
                    'band_kurtosis': band_kurtosis,
                    'band_skew': band_skew,
                    'envelope_mean': envelope_mean,
                    'envelope_std': envelope_std,
                    'envelope_max': envelope_max,
                    'harmonics': harmonics,
                    'subharmonics': subharmonics,
                    'wavelet_peaks': wavelet_results['peaks'],
                    'mod_freq': wavelet_results['mod_freq']
                }
            
                trace_results.append(detection)
            
                # Save plots if requested
                if save_plots:
                    self.save_enhanced_trace_plots(
                        tr, tr_processed, tr_filtered, 
                        freqs, fft_vals, phase_vals,
                        f, t, Sxx, envelope, amplitude_envelope, instantaneous_frequency,
                        envelope_freqs, envelope_fft, wavelet_results, detection
                    )
    
        except Exception as e:
            print(f"Error analyzing trace {tr.id}: {e}")
            import traceback
            traceback.print_exc()
        
        return trace_results

    def perform_wavelet_analysis(self, data, dt, ki_center):
        """
        Perform wavelet analysis to detect time-localized resonance phenomena
    
        Parameters:
        -----------
        data : array
            The signal data
        dt : float
            Time step
        ki_center : float
            Central Ki frequency to analyze
        
        Returns:
        --------
        dict
            Dictionary with wavelet analysis results
        """
        try:
            # Import PyWavelets if available
            import pywt
        
            # For better frequency resolution, we use complex Morlet wavelet
            widths = np.arange(1, 31)
        
            # Calculate the scales from frequencies of interest
            # We want to focus around Ki frequency
            fs = 1/dt
            central_freq = pywt.central_frequency('cmor1.5-1.0')
            scales = central_freq / (np.linspace(ki_center/2, ki_center*2, 50) * dt)
        
            # Perform continuous wavelet transform
            cwtmatr, freqs = pywt.cwt(data, scales, 'cmor1.5-1.0', dt)
        
            # We're only interested in frequencies around Ki
            ki_band_indices = np.where((freqs >= ki_center-self.band_width) & 
                                    (freqs <= ki_center+self.band_width))[0]
        
            if len(ki_band_indices) == 0:
                return {'wavelet_score': 0, 'peaks': [], 'mod_freq': None, 'cwtmatr': None, 'freqs': None}
            
            # Get wavelet power in the Ki band
            ki_power = np.abs(cwtmatr[ki_band_indices, :])
        
            # Look for oscillatory patterns in the wavelet power
            power_mean = np.mean(ki_power, axis=0)
            power_detrended = power_mean - np.mean(power_mean)
        
            # Look for modulation pattern in the wavelet power
            power_spec = np.abs(np.fft.rfft(power_detrended))
            power_freqs = np.fft.rfftfreq(len(power_detrended), dt)
        
            # Find the dominant modulation frequency
            mod_idx = np.argmax(power_spec)
            mod_freq = power_freqs[mod_idx]
            mod_strength = power_spec[mod_idx] / np.mean(power_spec)
        
            # Detect peaks in the wavelet power
            from scipy.signal import find_peaks
            peaks, _ = find_peaks(power_mean, height=np.mean(power_mean) + np.std(power_mean), 
                                distance=int(fs/ki_center/2))  # Minimum distance between peaks
        
            # Calculate peak times and strengths
            peak_times = peaks * dt
            peak_heights = power_mean[peaks]
        
            # Calculate a score based on modulation strength and regularity of peaks
            if len(peaks) > 1:
                peak_intervals = np.diff(peak_times)
                interval_regularity = 1.0 - np.std(peak_intervals) / np.mean(peak_intervals)
                interval_regularity = max(0, interval_regularity)  # Ensure non-negative
            else:
                interval_regularity = 0
            
            wavelet_score = (mod_strength * interval_regularity) if (mod_freq > 0.1 and mod_freq < 10) else 0
        
            return {
                'wavelet_score': wavelet_score,
                'peaks': list(zip(peak_times, peak_heights)),
                'mod_freq': mod_freq,
                'cwtmatr': cwtmatr,
                'freqs': freqs
            }
        
        except ImportError:
            # Fallback if PyWavelets not available
            print("PyWavelets not installed. Skipping wavelet analysis.")
            return {'wavelet_score': 0, 'peaks': [], 'mod_freq': None}

    def save_enhanced_trace_plots(self, tr_original, tr_processed, tr_filtered, 
                            freqs, fft_vals, phase_vals, f, t, Sxx, envelope, 
                            amplitude_envelope, instantaneous_frequency,
                            envelope_freqs, envelope_fft, wavelet_results, detection):
        """
        Save enhanced plots for a trace with detected Ki phenomena
    
        Parameters:
        -----------
        tr_original, tr_processed, tr_filtered : obspy.Trace
            Different processed versions of the trace
        freqs, fft_vals, phase_vals : arrays
            Frequency, FFT magnitude, and phase data
        f, t, Sxx : arrays
            Spectrogram data
        envelope, amplitude_envelope : arrays
            Different envelope representations
        instantaneous_frequency : array
            Instantaneous frequency from Hilbert transform
        envelope_freqs, envelope_fft : arrays
            Frequency analysis of the envelope
        wavelet_results : dict
            Results from wavelet analysis
        detection : dict
            Detection information
        """
        # Create a unique filename for this detection
        plot_base = self.plots_dir / f"{self.session_id}_{detection['trace_id']}_{detection['start_time'].datetime.strftime('%Y%m%d_%H%M%S')}"
    
        # Plot 1: Time series comparison (similar to original but with amplitude envelope)
        plt.figure(figsize=(12, 12))

        plt.subplot(411)
        plt.plot(tr_original.times(), tr_original.data, 'k', alpha=0.7, label='Original')
        plt.title(f"Original Signal - {detection['trace_id']}")
        plt.ylabel('Amplitude')
        plt.legend()
    
        plt.subplot(412)
        plt.plot(tr_processed.times(), tr_processed.data, 'b', label='Processed')
        plt.title('Detrended Signal')
        plt.ylabel('Amplitude')
        plt.legend()
    
        plt.subplot(413)
        plt.plot(tr_filtered.times(), tr_filtered.data, 'r', label='Ki Band Filtered')
        plt.plot(tr_filtered.times(), amplitude_envelope, 'g', label='Amplitude Envelope')
        plt.title(f'Filtered Signal (around Ki={self.ki_value} Hz)')
        plt.ylabel('Amplitude')
        plt.legend()
    
        plt.subplot(414)
        # Only plot instantaneous frequency where it's meaningful
        valid_indices = np.where((instantaneous_frequency > 0) & 
                                (instantaneous_frequency < tr_filtered.stats.sampling_rate/2))[0]
        if len(valid_indices) > 0:
            plt.plot(tr_filtered.times()[1:][valid_indices], 
                    instantaneous_frequency[valid_indices], 'purple', label='Instantaneous Frequency')
        plt.axhline(y=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
        plt.title('Instantaneous Frequency')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.ylim([0, min(10, tr_filtered.stats.sampling_rate/4)])  # Limit the range for clarity
        plt.legend()
    
        plt.tight_layout()
        plt.savefig(f"{plot_base}_timeseries.png", dpi=300)
        plt.close()
    
        # Plot 2: Enhanced spectral analysis
        plt.figure(figsize=(12, 15))
    
        plt.subplot(411)
        plt.plot(freqs, fft_vals, 'b', alpha=0.7)
        plt.axvline(x=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
    
        # Highlight the Ki band
        ki_min = self.ki_value - self.band_width
        ki_max = self.ki_value + self.band_width
        plt.axvspan(ki_min, ki_max, alpha=0.2, color='yellow', label='Analysis Band')
    
        # Mark harmonics if detected
        for harmonic in detection['harmonics']:
            harm_num, harm_freq, harm_ratio = harmonic
            plt.axvline(x=harm_freq, color='g', linestyle='-.', 
                    label=f'{harm_num}x Ki ({harm_freq:.3f} Hz)')
    
        # Mark subharmonics if detected
        for subharmonic in detection['subharmonics']:
            sub_num, sub_freq, sub_ratio = subharmonic
            plt.axvline(x=sub_freq, color='m', linestyle=':', 
                    label=f'{sub_num}x Ki ({sub_freq:.3f} Hz)')
    
        plt.title(f"FFT Spectrum - {detection['trace_id']}")
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
    
        # Plot phase spectrum
        plt.subplot(412)
        plt.plot(freqs, phase_vals, 'g')
        plt.axvline(x=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
        plt.axvspan(ki_min, ki_max, alpha=0.2, color='yellow', label='Analysis Band')
        plt.title('Phase Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Phase (radians)')
        plt.legend()
    
        # Plot envelope frequency spectrum
        plt.subplot(413)
        plt.plot(envelope_freqs, envelope_fft, 'purple')
        plt.axvline(x=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
        plt.axvspan(ki_min, ki_max, alpha=0.2, color='yellow', label='Analysis Band')
        plt.title('Envelope Frequency Spectrum (Amplitude Modulation)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
    
        # Zoomed view of envelope spectrum around Ki
        plt.subplot(414)
        ki_range_min = max(0, self.ki_value - 5 * self.band_width)
        ki_range_max = self.ki_value + 5 * self.band_width
        ki_range = (envelope_freqs >= ki_range_min) & (envelope_freqs <= ki_range_max)
    
        if np.any(ki_range):
            plt.plot(envelope_freqs[ki_range], envelope_fft[ki_range], 'purple')
            plt.axvline(x=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
            plt.axvline(x=detection['mod_freq'] if detection['mod_freq'] else 0, 
                    color='orange', linestyle='-', 
                    label=f'Mod Freq={detection["mod_freq"]:.3f} Hz' if detection['mod_freq'] else 'No Mod')
            plt.title('Zoomed Envelope Spectrum (around Ki)')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude')
            plt.legend()
    
        plt.tight_layout()
        plt.savefig(f"{plot_base}_spectrum.png", dpi=300)
        plt.close()
    
        # Plot 3: Enhanced spectrogram and wavelet analysis
        plt.figure(figsize=(12, 10))
    
        plt.subplot(211)
        plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')
        plt.axhline(y=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
        plt.colorbar(label='Power/Frequency (dB/Hz)')
        plt.ylabel('Frequency (Hz)')
        plt.title(f"Spectrogram - {detection['trace_id']}")
        plt.ylim([max(0, self.ki_value - 10 * self.band_width), self.ki_value + 10 * self.band_width])
        plt.legend()
    
        # If wavelet analysis was performed, show results
        if wavelet_results.get('cwtmatr') is not None:
            plt.subplot(212)
        
            # Get data from wavelet analysis
            cwtmatr = wavelet_results['cwtmatr']
            freqs = wavelet_results['freqs']
        
            # Plot wavelet scalogram
            plt.pcolormesh(np.arange(len(tr_processed.data)) * tr_processed.stats.delta, 
                        freqs, np.abs(cwtmatr), cmap='jet')
            plt.axhline(y=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
        
            # Mark detected peaks
            for peak_time, peak_height in detection['wavelet_peaks']:
                plt.axvline(x=peak_time, color='g', linestyle=':', alpha=0.5)
            
            plt.colorbar(label='Wavelet Power')
            plt.yscale('log')
            plt.ylabel('Frequency (Hz)')
            plt.xlabel('Time (s)')
            plt.title('Wavelet Transform - Power Scalogram')
            plt.legend()
    
        plt.tight_layout()
        plt.savefig(f"{plot_base}_timefreq.png", dpi=300)
        plt.close()
    
    def perform_permutation_test(self, tr, n_permutations=10):
        """
        Perform permutation test to estimate false alarm rate
        
        Parameters:
        -----------
        tr : obspy.Trace
            The trace to analyze
        n_permutations : int
            Number of permutations to run
            
        Returns:
        --------
        tuple
            (null_detection_counts, p_value)
        """
        # Store original data
        original_data = tr.data.copy()
        
        # Track null detections
        null_detections = []
        
        for i in range(n_permutations):
            # Create a random circular shift
            shift = np.random.randint(0, len(original_data))
            tr.data = np.roll(original_data, shift)
            
            # Analyze the shifted trace
            detections = self.analyze_trace(tr, "permutation_test", save_plots=False)
            null_detections.append(len(detections))
        
        # Restore original data
        tr.data = original_data
        
        # Calculate p-value based on original detection count
        original_detections = len(self.analyze_trace(tr, "original", save_plots=False))
        
        if len(null_detections) == 0:
            return [], 1.0
            
        p_value = sum(count >= original_detections for count in null_detections) / len(null_detections)
        
        return null_detections, p_value
    
    def save_trace_plots(self, tr_original, tr_processed, tr_filtered, 
                         freqs, fft_vals, f, t, Sxx, envelope, detection):
        """
        Save plots for a trace with detected Ki phenomena
        
        Parameters:
        -----------
        tr_original : obspy.Trace
            The original trace
        tr_processed : obspy.Trace
            The processed trace
        tr_filtered : obspy.Trace
            The filtered trace around Ki
        freqs, fft_vals : array
            Frequency and FFT magnitude data
        f, t, Sxx : arrays
            Spectrogram data
        envelope : array
            Hilbert envelope of the filtered signal
        detection : dict
            Detection information
        """
        # Create a unique filename for this detection
        plot_base = self.plots_dir / f"{self.session_id}_{detection['trace_id']}_{detection['start_time'].datetime.strftime('%Y%m%d_%H%M%S')}"
        
        # Plot 1: Time series comparison
        plt.figure(figsize=(12, 10))
        
        plt.subplot(311)
        plt.plot(tr_original.times(), tr_original.data, 'k', alpha=0.7, label='Original')
        plt.title(f"Original Signal - {detection['trace_id']}")
        plt.ylabel('Amplitude')
        plt.legend()
        
        plt.subplot(312)
        plt.plot(tr_processed.times(), tr_processed.data, 'b', label='Processed')
        plt.title('Detrended Signal')
        plt.ylabel('Amplitude')
        plt.legend()
        
        plt.subplot(313)
        plt.plot(tr_filtered.times(), tr_filtered.data, 'r', label='Ki Band Filtered')
        plt.plot(tr_filtered.times(), envelope, 'g', label='Envelope')
        plt.title(f'Filtered Signal (around Ki={self.ki_value} Hz)')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(f"{plot_base}_timeseries.png", dpi=300)
        plt.close()
        
        # Plot 2: Spectral analysis
        plt.figure(figsize=(12, 10))
        
        plt.subplot(211)
        plt.plot(freqs, fft_vals, 'b', alpha=0.7)
        plt.axvline(x=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
        plt.axvline(x=detection['peak_freq'], color='g', linestyle='-', 
                    label=f'Peak={detection["peak_freq"]:.3f}')
        
        # Highlight the Ki band
        ki_min = self.ki_value - self.band_width
        ki_max = self.ki_value + self.band_width
        plt.axvspan(ki_min, ki_max, alpha=0.2, color='yellow', label='Analysis Band')
        
        plt.title(f"FFT Spectrum - {detection['trace_id']}")
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        
        # Zoom in on the Ki region
        plt.subplot(212)
        ki_range_min = max(0, self.ki_value - 5 * self.band_width)
        ki_range_max = self.ki_value + 5 * self.band_width
        ki_range = (freqs >= ki_range_min) & (freqs <= ki_range_max)
        
        plt.plot(freqs[ki_range], fft_vals[ki_range], 'b')
        plt.axvline(x=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
        plt.axvline(x=detection['peak_freq'], color='g', linestyle='-', 
                    label=f'Peak={detection["peak_freq"]:.3f}')
        plt.axvspan(ki_min, ki_max, alpha=0.2, color='yellow', label='Analysis Band')
        
        plt.title('Zoomed FFT Spectrum around Ki')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(f"{plot_base}_spectrum.png", dpi=300)
        plt.close()
        
        # Plot 3: Spectrogram
        plt.figure(figsize=(10, 6))
        
        plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')
        plt.axhline(y=self.ki_value, color='r', linestyle='--', label=f'Ki={self.ki_value}')
        plt.colorbar(label='Power/Frequency (dB/Hz)')
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')
        plt.title(f"Spectrogram - {detection['trace_id']}")
        plt.ylim([max(0, self.ki_value - 10 * self.band_width), self.ki_value + 10 * self.band_width])
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(f"{plot_base}_spectrogram.png", dpi=300)
        plt.close()
    
    def save_file_summary(self, file_path, stream, file_results):
        """
        Save a summary plot for a file with detections
        
        Parameters:
        -----------
        file_path : Path
            Path to the original file
        stream : obspy.Stream
            The stream of traces from the file
        file_results : list
            List of detections from the file
        """
        summary_file = self.plots_dir / f"{self.session_id}_summary_{file_path.stem}.png"
        
        num_traces = len(stream)
        fig, axes = plt.subplots(num_traces, 1, figsize=(12, 3 * num_traces), sharex=True)
        
        # If only one trace, make axes iterable
        if num_traces == 1:
            axes = [axes]
            
        for i, tr in enumerate(stream):
            # Plot the trace
            axes[i].plot(tr.times(), tr.data, 'k', alpha=0.7, label=tr.id)
            
            # Highlight sections with detections for this trace
            for detection in [d for d in file_results if d['trace_id'] == tr.id]:
                start_index = int((detection['start_time'] - tr.stats.starttime) * tr.stats.sampling_rate)
                end_index = int((detection['end_time'] - tr.stats.starttime) * tr.stats.sampling_rate)
                
                # Ensure indices are within valid range
                start_index = max(0, start_index)
                end_index = min(len(tr.data) - 1, end_index)
                
                # Highlight the detection region
                axes[i].axvspan(start_index / tr.stats.sampling_rate, 
                               end_index / tr.stats.sampling_rate,
                               alpha=0.3, color='red')
            
            axes[i].set_ylabel('Amplitude')
            axes[i].set_title(f"Trace: {tr.id}")
            axes[i].legend(loc='upper right')
            
        axes[-1].set_xlabel('Time (s)')
        plt.suptitle(f"Summary for {file_path.name}: {len(file_results)} Ki detections", fontsize=16)
        
        plt.tight_layout()
        plt.savefig(summary_file, dpi=300)
        plt.close()
    
    def process_directory(self, directory_path, pattern="*.mseed", parallel=True, max_workers=None, 
                        psd_method='welch', save_plots=True, permutation_test=False, nperseg=None):
        """
        Process all miniseed files in a directory
    
        Parameters:
        -----------
        directory_path : str or Path
            Path to the directory containing miniseed files
        pattern : str
            Glob pattern to match files (default: "*.mseed")
        parallel : bool
            Whether to process files in parallel
        max_workers : int or None
            Maximum number of parallel workers (None = use CPU count)
        psd_method : str
            Method to use for PSD estimation
        save_plots : bool
            Whether to save plots
        permutation_test : bool
            Whether to perform permutation test
        nperseg : int or None
            Length of each segment for welch/multitaper methods
        
        Returns:
        --------
        list
            Combined results from all files
        """
        # Set appropriate start method for multiprocessing
        if parallel and platform.system() != 'Linux':
            import multiprocessing
            try:
                multiprocessing.set_start_method('forkserver', force=True)
            except RuntimeError:
                # If already set, ignore
                pass
            except ValueError:
                # If method not available, try spawn
                try:
                    multiprocessing.set_start_method('spawn', force=True)
                except:
                    print("Warning: Could not set multiprocessing start method.")
    
        directory_path = Path(directory_path)
        files = list(directory_path.glob(pattern))
    
        if not files:
            print(f"No files matching '{pattern}' found in {directory_path}")
            return []
    
        print(f"Found {len(files)} files to process in {directory_path}")
    
        # Save the parameters as instance variables to be used by process_file_with_args
        self.temp_save_plots = save_plots
        self.temp_psd_method = psd_method
        self.temp_permutation_test = permutation_test
        self.temp_nperseg = nperseg
    
        if parallel and len(files) > 1:
            # Process files in parallel
            if max_workers is None:
                max_workers = cpu_count()
            
            print(f"Processing files in parallel with {max_workers} workers")
        
            with Pool(processes=max_workers) as pool:
                # Use tqdm for progress bar
                all_results = list(tqdm.tqdm(
                    pool.imap(self._process_file_wrapper, files),
                    total=len(files),
                    desc="Processing files"
                ))
            
            # Flatten results list
            flat_results = [item for sublist in all_results for item in sublist]
        
        else:
            # Process files sequentially
            print("Processing files sequentially")
            flat_results = []
            for i, file in enumerate(tqdm.tqdm(files, desc="Processing files")):
                file_results = self.process_file(file, save_plots, psd_method, permutation_test, nperseg)
                flat_results.extend(file_results)
            
        # Store all results
        self.results = flat_results

        # Update the file count explicitly
        self.processed_file_count = len(files)
    
        return flat_results
    
    def save_results(self):
        """
        Save analysis results to files
        
        Returns:
        --------
        Path
            Path to the saved results files
        """
        if not self.results:
            print("No results to save.")
            return None
        
        # Convert results to DataFrame
        df = pd.DataFrame(self.results)
        
        # Save to CSV
        csv_path = self.data_dir / f"{self.session_id}_ki_detections.csv"
        df.to_csv(csv_path, index=False)
        
        # Save to Excel
        excel_path = self.data_dir / f"{self.session_id}_ki_detections.xlsx"
        df.to_excel(excel_path, index=False)
        
        # Generate summary statistics
        stats = {
            'total_detections': len(df),
            'unique_files': df['filename'].nunique(),
            'unique_traces': df['trace_id'].nunique(),
            'mean_energy_ratio': df['energy_ratio'].mean(),
            'max_energy_ratio': df['energy_ratio'].max(),
            'min_ki_distance': df['ki_distance'].min(),
            'mean_ki_distance': df['ki_distance'].mean(),
            'session_start': self.session_start_time,
            'session_end': datetime.now(),
            'ki_value': self.ki_value,
            'band_width': self.band_width,
            'significance_threshold': self.significance_threshold,
            'p_value_threshold': self.p_value_threshold
        }
        
        # Save summary report
        report_path = self.reports_dir / f"{self.session_id}_summary_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write(f"Ki ANALYSIS SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Start Time: {stats['session_start']}\n")
            f.write(f"End Time: {stats['session_end']}\n")
            f.write(f"Duration: {stats['session_end'] - stats['session_start']}\n\n")
            
            f.write(f"Analysis Parameters:\n")
            f.write(f"  Ki Value: {stats['ki_value']}\n")
            f.write(f"  Band Width: {stats['band_width']}\n")
            f.write(f"  Significance Threshold: {stats['significance_threshold']} std\n")
            f.write(f"  P-value Threshold: {stats['p_value_threshold']}\n\n")
            
            f.write(f"Results Summary:\n")
            f.write(f"  Total Detections: {stats['total_detections']}\n")
            f.write(f"  Files with Detections: {stats['unique_files']}\n")
            f.write(f"  Traces with Detections: {stats['unique_traces']}\n\n")
            
            f.write(f"Detection Statistics:\n")
            f.write(f"  Mean Energy Ratio: {stats['mean_energy_ratio']:.4f}\n")
            f.write(f"  Max Energy Ratio: {stats['max_energy_ratio']:.4f}\n")
            f.write(f"  Min Ki Distance: {stats['min_ki_distance']:.6f} Hz\n")
            f.write(f"  Mean Ki Distance: {stats['mean_ki_distance']:.6f} Hz\n\n")
            
            f.write(f"Top 10 Strongest Detections:\n")
            top_detections = df.sort_values('energy_ratio', ascending=False).head(10)
            for i, row in enumerate(top_detections.itertuples(), 1):
                f.write(f"  {i}. {row.trace_id} @ {row.start_time} - Energy Ratio: {row.energy_ratio:.4f}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Report generated at {datetime.now()}\n")
            f.write("=" * 80 + "\n")
        
        print(f"Analysis results saved to {self.output_dir}")
        
        return self.output_dir
    
    def perform_ks_test_on_ki_modes(self, rest_analyzer):
        """
        Perform Kolmogorov-Smirnov test to compare Ki modes
        
        Parameters:
        -----------
        rest_analyzer : KiAnalyzer
            Analyzer configured for Ki rest value
            
        Returns:
        --------
        dict
            KS test results
        """
        from scipy import stats
        
        if not self.results or not rest_analyzer.results:
            return {"error": "Insufficient data for comparison"}
        
        # Extract ki_distance values
        rest_distances = [r['ki_distance'] for r in rest_analyzer.results]
        motion_distances = [r['ki_distance'] for r in self.results]
        
        if not rest_distances or not motion_distances:
            return {"error": "Empty distance arrays"}
        
        # Perform KS test
        ks_statistic, p_value = stats.ks_2samp(rest_distances, motion_distances)
        
        # Calculate means
        rest_mean = np.mean(rest_distances)
        motion_mean = np.mean(motion_distances)
        
        # Determine which mode has closer distances on average
        closer_mode = "Rest" if rest_mean < motion_mean else "Motion"
        
        results = {
            "ks_statistic": ks_statistic,
            "p_value": p_value,
            "rest_mean_distance": rest_mean,
            "motion_mean_distance": motion_mean,
            "significant_difference": p_value < 0.05,
            "closer_mode": closer_mode
        }
        
        return results
    
    def generate_dual_ki_comparison(self):
        """
        Run analysis for both Ki values (rest and motion) and compare results
        
        Returns:
        --------
        tuple
            (rest_analyzer, motion_analyzer) with results from both analyses
        """
        print(f"Running dual Ki comparison analysis...")
        
        # Create a rest Ki analyzer with similar settings
        rest_analyzer = KiAnalyzer(
            ki_value=KI_REST,
            band_width=self.static_band_width,
            output_dir=self.output_dir / 'ki_rest',
            significance_threshold=self.significance_threshold,
            p_value_threshold=self.p_value_threshold,
            q_factor=self.q_factor
        )
        
        # Process the same files with both analyzers
        for file_path in self.processed_files:
            rest_analyzer.process_file(file_path)
            
        # Save results from both analyses
        rest_analyzer.save_results()
        self.save_results()
        
        # Compare the results
        self.compare_ki_modes(rest_analyzer)
        
        return (rest_analyzer, self)
    
    def compare_ki_modes(self, rest_analyzer):
        """
        Compare results from rest and motion Ki analysis
        
        Parameters:
        -----------
        rest_analyzer : KiAnalyzer
            Analyzer configured for Ki rest value
        """
        if not self.results or not rest_analyzer.results:
            print("Insufficient data for comparison.")
            return
                
        rest_df = pd.DataFrame(rest_analyzer.results)
        motion_df = pd.DataFrame(self.results)
        
        # Add mode identifier
        rest_df['ki_mode'] = 'rest'
        motion_df['ki_mode'] = 'motion'
        
        # Combine the results
        combined_df = pd.concat([rest_df, motion_df])
        
        # Save combined results
        combined_csv = self.reports_dir / f"{self.session_id}_ki_mode_comparison.csv"
        combined_df.to_csv(combined_csv, index=False)
        
        # Perform KS test
        ks_test_results = self.perform_ks_test_on_ki_modes(rest_analyzer)
        
        # Create comparison plots
        plt.figure(figsize=(10, 6))
        
        # Group by trace and count detections for each mode
        trace_counts = combined_df.groupby(['trace_id', 'ki_mode']).size().unstack(fill_value=0)
        trace_counts.plot(kind='bar', alpha=0.7)
        
        plt.title('Ki Mode Comparison by Trace')
        plt.xlabel('Trace ID')
        plt.ylabel('Detection Count')
        plt.tight_layout()
        
        plt.savefig(self.reports_dir / f"{self.session_id}_ki_mode_comparison.png", dpi=300)
        plt.close()
        
        # Compare energy ratios
        plt.figure(figsize=(10, 6))
        
        try:
            import seaborn as sns
            sns.boxplot(x='ki_mode', y='energy_ratio', data=combined_df)
        except ImportError:
            # Fallback if seaborn is not available
            combined_df.boxplot(column='energy_ratio', by='ki_mode')
            
        plt.title('Energy Ratio Comparison between Ki Modes')
        plt.xlabel('Ki Mode')
        plt.ylabel('Energy Ratio')
        
        plt.savefig(self.reports_dir / f"{self.session_id}_energy_ratio_comparison.png", dpi=300)
        plt.close()
        
        # Compare Ki distances
        plt.figure(figsize=(10, 6))
        
        try:
            import seaborn as sns
            sns.boxplot(x='ki_mode', y='ki_distance', data=combined_df)
        except ImportError:
            # Fallback if seaborn is not available
            combined_df.boxplot(column='ki_distance', by='ki_mode')
            
        plt.title('Ki Distance Comparison between Modes')
        plt.xlabel('Ki Mode')
        plt.ylabel('Distance from Ki (Hz)')
        
        plt.savefig(self.reports_dir / f"{self.session_id}_ki_distance_comparison.png", dpi=300)
        plt.close()
        
        # Write comparison report
        report_path = self.reports_dir / f"{self.session_id}_ki_mode_comparison_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write(f"Ki MODE COMPARISON REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Rest Mode (Ki = {KI_REST}):\n")
            f.write(f"  Total Detections: {len(rest_df)}\n")
            f.write(f"  Mean Energy Ratio: {rest_df['energy_ratio'].mean():.4f}\n")
            f.write(f"  Mean Ki Distance: {rest_df['ki_distance'].mean():.6f} Hz\n\n")
            
            f.write(f"Motion Mode (Ki = {KI_MOTION}):\n")
            f.write(f"  Total Detections: {len(motion_df)}\n")
            f.write(f"  Mean Energy Ratio: {motion_df['energy_ratio'].mean():.4f}\n")
            f.write(f"  Mean Ki Distance: {motion_df['ki_distance'].mean():.6f} Hz\n\n")
            
            # Add KS test results
            f.write(f"Mode Comparison (Kolmogorov-Smirnov Test):\n")
            f.write(f"  KS Statistic: {ks_test_results.get('ks_statistic', 'N/A'):.4f}\n")
            f.write(f"  p-value: {ks_test_results.get('p_value', 'N/A'):.6f}\n")
            f.write(f"  Significant Difference: {ks_test_results.get('significant_difference', False)}\n")
            f.write(f"  Mode with Closer Ki Match: {ks_test_results.get('closer_mode', 'N/A')}\n\n")
            
            # Compute trace-level statistics
            f.write(f"Trace-level comparison:\n")
            for trace_id in trace_counts.index:
                rest_count = trace_counts.loc[trace_id, 'rest'] if 'rest' in trace_counts.columns else 0
                motion_count = trace_counts.loc[trace_id, 'motion'] if 'motion' in trace_counts.columns else 0
                ratio = motion_count / rest_count if rest_count > 0 else float('inf')
                
                f.write(f"  {trace_id}: Rest: {rest_count}, Motion: {motion_count}, Ratio: {ratio:.2f}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Report generated at {datetime.now()}\n")
            f.write("=" * 80 + "\n")
            
        print(f"Ki mode comparison completed and saved to {report_path}")

    def process_file_with_args(self, file_path, save_plots=True, psd_method='welch', 
                                    permutation_test=False, nperseg=None):
                """Helper method to process a file with fixed arguments"""
                return self.process_file(file_path, save_plots, psd_method, permutation_test, nperseg)
        
    def _process_file_wrapper(self, file_path):
        """Wrapper method for multiprocessing that will be used by pool.imap"""
        return self.process_file(file_path, self.temp_save_plots, self.temp_psd_method, 
                                        self.temp_permutation_test, self.temp_nperseg)



def generate_resonance_report(self, detection):
    """
    Generate a detailed report about detected resonance patterns
    
    Parameters:
    -----------
    detection : dict
        Detection information
        
    Returns:
    --------
    str
        Formatted report text
    """
    report = []
    report.append(f"Ki RESONANCE PATTERN REPORT\n")
    report.append(f"="*80 + "\n")
    report.append(f"Trace ID: {detection['trace_id']}")
    report.append(f"Time: {detection['start_time']} to {detection['end_time']}")
    report.append(f"Duration: {detection['duration']}")
    report.append(f"Total Detection Score: {detection['detection_score']:.4f}")
    report.append("\n")
    
    report.append(f"DETECTION METRICS:")
    report.append(f"-"*80)
    report.append(f"FFT Energy Ratio: {detection['fft_energy_ratio']:.4f}")
    report.append(f"Modulation Ratio: {detection['modulation_ratio']:.4f}")
    report.append(f"Phase Coherence: {detection['phase_coherence']:.4f}")
    report.append(f"Harmonics Strength: {detection['harmonics_strength']:.4f}")
    report.append(f"Wavelet Score: {detection['wavelet_score']:.4f}")
    report.append(f"Peak Frequency: {detection['peak_freq']:.6f} Hz")
    report.append(f"Ki Distance: {detection['ki_distance']:.6f} Hz")
    report.append("\n")
    
    report.append(f"HARMONIC STRUCTURE:")
    report.append(f"-"*80)
    if detection['harmonics']:
        for i, (harm_num, harm_freq, harm_ratio) in enumerate(detection['harmonics']):
            report.append(f"Harmonic {i+1}: {harm_num}x Ki at {harm_freq:.6f} Hz (strength: {harm_ratio:.4f})")
    else:
        report.append("No significant harmonics detected")
        
    if detection['subharmonics']:
        for i, (sub_num, sub_freq, sub_ratio) in enumerate(detection['subharmonics']):
            report.append(f"Subharmonic {i+1}: {sub_num}x Ki at {sub_freq:.6f} Hz (strength: {sub_ratio:.4f})")
    else:
        report.append("No significant subharmonics detected")
    report.append("\n")
    
    report.append(f"MODULATION PATTERNS:")
    report.append(f"-"*80)
    if detection['mod_freq']:
        report.append(f"Dominant Modulation Frequency: {detection['mod_freq']:.6f} Hz")
        if abs(detection['mod_freq'] - self.ki_value) < self.band_width:
            report.append(f"SIGNIFICANT: Modulation occurs at Ki frequency!")
    else:
        report.append("No significant modulation detected")
    report.append("\n")
    
    report.append(f"TIME-LOCALIZED RESONANCE:")
    report.append(f"-"*80)
    if detection['wavelet_peaks']:
        report.append(f"Found {len(detection['wavelet_peaks'])} time-localized resonance peaks:")
        for i, (peak_time, peak_strength) in enumerate(detection['wavelet_peaks'][:5]):  # Show top 5
            report.append(f"Peak {i+1}: Time {peak_time:.2f}s (strength: {peak_strength:.4f})")
        if len(detection['wavelet_peaks']) > 5:
            report.append(f"... and {len(detection['wavelet_peaks']) - 5} more peaks")
    else:
        report.append("No significant time-localized resonance detected")
        
    return "\n".join(report)


def process_args():
    """Process command-line arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze miniseed files for evidence of Ki-related phenomena")
    
    parser.add_argument('input', help="Input file or directory path")
    parser.add_argument('-o', '--output', help="Output directory", default=None)
    parser.add_argument('-k', '--ki-value', type=float, default=KI_MOTION, 
                        help=f"Ki value to analyze (default: {KI_MOTION})")
    parser.add_argument('-b', '--bandwidth', type=float, default=DEFAULT_BAND_WIDTH,
                        help=f"Analysis bandwidth around Ki (default: {DEFAULT_BAND_WIDTH})")
    parser.add_argument('-q', '--q-factor', type=float, default=40,
                        help="Q-factor for dynamic bandwidth calculation (default: 40)")
    parser.add_argument('-t', '--threshold', type=float, default=3.0,
                        help="Significance threshold in standard deviations (default: 3.0)")
    parser.add_argument('-m', '--method', default="welch", choices=['fft', 'welch', 'multitaper'],
                        help="PSD estimation method (default: welch)")
    parser.add_argument('-p', '--pattern', default="*.mseed",
                        help="File pattern to match (default: *.mseed)")
    parser.add_argument('-s', '--sequential', action='store_true',
                        help="Process files sequentially instead of in parallel")
    parser.add_argument('-w', '--workers', type=int, default=None,
                        help="Number of parallel workers (default: CPU count)")
    parser.add_argument('-d', '--dual-ki', action='store_true',
                        help="Analyze both rest and motion Ki values")
    parser.add_argument('--no-plots', action='store_true',
                        help="Disable plot generation")
    parser.add_argument('--nperseg', type=int, default=None,
                        help="Length of each segment for welch/multitaper methods")
    parser.add_argument('--permutation', action='store_true',
                        help="Perform permutation test to estimate false alarm rate")
    parser.add_argument('--p-value', type=float, default=0.001,
                        help="P-value threshold for significance (default: 0.001)")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Enable verbose output")
    
    return parser.parse_args()


def main():
    """Main function"""
    args = process_args()
    
    # Configure the analyzer
    analyzer = KiAnalyzer(
        ki_value=args.ki_value,
        band_width=args.bandwidth,
        output_dir=args.output,
        significance_threshold=args.threshold,
        p_value_threshold=args.p_value,
        q_factor=args.q_factor
    )
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Process a single file
        print(f"Processing file: {input_path}")
        results = analyzer.process_file(
            input_path,
            save_plots=not args.no_plots,
            psd_method=args.method,
            permutation_test=args.permutation,
            nperseg=args.nperseg
        )
        print(f"Found {len(results)} Ki phenomena in file")
        
    elif input_path.is_dir():
        # Process a directory
        print(f"Processing directory: {input_path}")
        results = analyzer.process_directory(
            input_path, 
            pattern=args.pattern,
            parallel=not args.sequential,
            max_workers=args.workers,
            psd_method=args.method,
            save_plots=not args.no_plots,
            permutation_test=args.permutation,
            nperseg=args.nperseg
        )
        print(f"Found {len(results)} Ki phenomena in {analyzer.processed_file_count} files")
        
    else:
        print(f"Error: {input_path} is not a valid file or directory")
        return 1
    
    # Save all results
    output_path = analyzer.save_results()
    
    # If dual Ki analysis is requested, run that too
    if args.dual_ki:
        rest_analyzer, motion_analyzer = analyzer.generate_dual_ki_comparison()
        print(f"Dual Ki comparison completed")
    
    print(f"Analysis complete. Results saved to {output_path}")
    return 0


if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)