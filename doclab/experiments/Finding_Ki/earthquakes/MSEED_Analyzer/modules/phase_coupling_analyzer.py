import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import hilbert
import pywt
from pathlib import Path

class PhaseCouplingAnalyzer:
    """
    Analyzes phase coupling and cross-frequency interactions in time series,
    specifically looking for resonance patterns related to the Ki constant.
    
    The module uses several approaches:
    1. Phase-amplitude coupling (PAC) analysis
    2. Bicoherence analysis for detecting quadratic phase coupling
    3. Phase synchronization index calculation
    4. Ki-resonant frequency band interactions
    """
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        # Primary Ki value being analyzed
        self.ki_value = analyzer.ki_value
        # Alternative Ki value for comparison
        self.alt_ki = analyzer.alternate_ki
        # Significance threshold
        self.significance = analyzer.significance_threshold
        # Pi constant for reference
        self.pi = 3.14159
    
    def analyze(self, trace, processed_trace=None, **kwargs):
        """
        Analyze a trace for Ki-related phase coupling phenomena
        
        Parameters:
        -----------
        trace : obspy.Trace
            The original trace to analyze
        processed_trace : obspy.Trace or None
            Preprocessed version of the trace (detrended, filtered)
            
        Returns:
        --------
        list of AnalysisResult
            Analysis results with any detected patterns
        """
        # Use processed trace if available, else use original
        if processed_trace is not None:
            working_trace = processed_trace
        else:
            working_trace = trace
        
        results = []
        
        # Extract key information
        data = working_trace.data
        sampling_rate = working_trace.stats.sampling_rate
        
        # Calculate Ki-related frequencies
        ki_freqs = self.analyzer.get_ki_phase_frequencies(sampling_rate)
        
        # Calculate frequency bands of interest based on Ki values
        frequency_bands = self.calculate_ki_frequency_bands(sampling_rate)
        
        # Only proceed if we have enough data points
        min_samples_required = int(sampling_rate * 5)  # At least 5 seconds
        if len(data) < min_samples_required:
            return results
        
        # Try different analysis approaches
        
        # 1. Analyze phase-amplitude coupling
        pac_result = self.analyze_phase_amplitude_coupling(data, sampling_rate, frequency_bands)
        if pac_result:
            results.append(pac_result)
        
        # 2. Analyze bicoherence (quadratic phase coupling)
        bic_result = self.analyze_bicoherence(data, sampling_rate, frequency_bands)
        if bic_result:
            results.append(bic_result)
        
        # 3. Analyze phase synchronization across frequency bands
        sync_result = self.analyze_phase_synchronization(data, sampling_rate, frequency_bands)
        if sync_result:
            results.append(sync_result)
        
        # 4. Analyze Ki wavelet coherence
        wavelet_result = self.analyze_wavelet_coherence(data, sampling_rate, ki_freqs)
        if wavelet_result:
            results.append(wavelet_result)
            
        return results
    
    def calculate_ki_frequency_bands(self, sampling_rate):
        """
        Calculate frequency bands of interest based on Ki value and sampling rate
        
        Returns:
        --------
        dict of frequency bands
        """
        nyquist = sampling_rate / 2
        
        # Create frequency bands centered around Ki-related frequencies
        ki_freqs = self.analyzer.get_ki_phase_frequencies(sampling_rate)
        
        # Filter out frequencies beyond Nyquist
        valid_freqs = {k: v for k, v in ki_freqs.items() if v < nyquist}
        
        # Create bands with 10% bandwidth around each frequency
        bands = {}
        for name, center_freq in valid_freqs.items():
            # Skip if center frequency is too close to 0
            if center_freq < 0.1:
                continue
                
            bandwidth = center_freq * 0.1  # 10% bandwidth
            bands[name] = (max(0.01, center_freq - bandwidth), min(nyquist, center_freq + bandwidth))
        
        # Add some wider bands for slower modulations
        if nyquist > 10:
            bands['delta'] = (0.5, 4)
            bands['theta'] = (4, 8)
            bands['alpha'] = (8, 13)
            bands['beta'] = (13, 30)
            bands['gamma'] = (30, min(100, nyquist))
        
        return bands
    
    def analyze_phase_amplitude_coupling(self, data, sampling_rate, frequency_bands):
        """
        Analyze phase-amplitude coupling between frequency bands
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
        sampling_rate : float
            Sampling rate in Hz
        frequency_bands : dict
            Dictionary of frequency bands
            
        Returns:
        --------
        AnalysisResult or None
            Analysis result if significant coupling found, None otherwise
        """
        from itertools import product
        
        # Initialize result
        result = None
        
        # Extract the standard frequency bands for phase and the potential Ki-bands for amplitude
        phase_bands = {k: v for k, v in frequency_bands.items() if k in ['delta', 'theta', 'alpha', 'beta']}
        amplitude_bands = {k: v for k, v in frequency_bands.items() if k.startswith('ki_')}
        
        # Keep track of the maximum PAC value
        max_pac = 0
        max_phase_band = None
        max_amp_band = None
        
        # Calculate PAC between each phase and amplitude band
        pac_values = {}
        for phase_name, phase_band in phase_bands.items():
            for amp_name, amp_band in amplitude_bands.items():
                # Skip if the amplitude band is lower than the phase band
                if amp_band[0] <= phase_band[1]:
                    continue
                    
                # Calculate phase timeseries
                phase_data = self.filter_data(data, sampling_rate, phase_band[0], phase_band[1])
                phase_angle = np.angle(hilbert(phase_data))
                
                # Calculate amplitude timeseries
                amp_data = self.filter_data(data, sampling_rate, amp_band[0], amp_band[1])
                amp_envelope = np.abs(hilbert(amp_data))
                
                # Calculate Modulation Index
                pac = self.modulation_index(phase_angle, amp_envelope)
                
                # Save result
                pac_values[(phase_name, amp_name)] = pac
                
                # Update maximum if needed
                if pac > max_pac:
                    max_pac = pac
                    max_phase_band = phase_name
                    max_amp_band = amp_name
        
        # Calculate surrogate distribution by phase-shuffling
        n_surrogates = 50
        surrogate_values = []
        
        if max_phase_band and max_amp_band:
            phase_data = self.filter_data(data, sampling_rate, phase_bands[max_phase_band][0], phase_bands[max_phase_band][1])
            phase_angle = np.angle(hilbert(phase_data))
            
            amp_data = self.filter_data(data, sampling_rate, amplitude_bands[max_amp_band][0], amplitude_bands[max_amp_band][1])
            amp_envelope = np.abs(hilbert(amp_data))
            
            for i in range(n_surrogates):
                # Shuffle phase values
                shuffled_phase = np.random.permutation(phase_angle)
                # Calculate PAC
                surrogate_pac = self.modulation_index(shuffled_phase, amp_envelope)
                surrogate_values.append(surrogate_pac)
            
            # Calculate significance
            surrogate_mean = np.mean(surrogate_values)
            surrogate_std = np.std(surrogate_values)
            
            z_score = (max_pac - surrogate_mean) / surrogate_std if surrogate_std > 0 else 0
            
            # Only create a result if the z-score exceeds the threshold
            if z_score >= self.significance:
                # Create result
                from datetime import datetime
                result = self.analyzer.AnalysisResult(
                    trace_id=f"PAC_{max_phase_band}_{max_amp_band}",
                    start_time=datetime.now(),
                    end_time=datetime.now()
                )
                
                # Add metrics
                result.add_metric("max_pac_value", max_pac)
                result.add_metric("pac_significance", z_score)
                result.add_metric("phase_band", max_phase_band)
                result.add_metric("amplitude_band", max_amp_band)
                
                # Add pattern data for plotting
                result.add_pattern("phase_band_range", phase_bands[max_phase_band])
                result.add_pattern("amplitude_band_range", amplitude_bands[max_amp_band])
                result.add_pattern("pac_values", pac_values)
                result.add_pattern("surrogates", surrogate_values)
                
                # Add phase and amplitude data for plotting
                result.add_plot_data("phase_data", phase_data)
                result.add_plot_data("phase_angle", phase_angle)
                result.add_plot_data("amp_data", amp_data)
                result.add_plot_data("amp_envelope", amp_envelope)
        
        return result
    
    def analyze_bicoherence(self, data, sampling_rate, frequency_bands):
        """
        Analyze bicoherence to detect quadratic phase coupling
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
        sampling_rate : float
            Sampling rate in Hz
        frequency_bands : dict
            Dictionary of frequency bands
            
        Returns:
        --------
        AnalysisResult or None
            Analysis result if significant coupling found, None otherwise
        """
        # Initialize result
        result = None
        
        # Only proceed if we have enough data points
        if len(data) < sampling_rate * 10:  # Need at least 10s for good bicoherence
            return None
        
        # Calculate bicoherence
        try:
            # Determine segment size
            segment_size = min(1024, len(data) // 5)
            
            # Calculate frequencies that will be returned
            freq = np.fft.fftfreq(segment_size, 1/sampling_rate)[:segment_size//2+1]
            
            # Get indices for Ki-related frequencies
            ki_freqs = self.analyzer.get_ki_phase_frequencies(sampling_rate)
            ki_indices = {}
            
            for name, ki_freq in ki_freqs.items():
                if ki_freq < sampling_rate/2:  # Check if below Nyquist
                    # Find closest frequency index
                    idx = np.argmin(np.abs(freq - ki_freq))
                    ki_indices[name] = idx
            
            # Calculate bicoherence
            bic, freq_pairs = self.bicoherence(data, segment_size, 50)
            
            # Find the maximum bicoherence value
            max_bic = np.max(bic)
            max_idx = np.unravel_index(np.argmax(bic), bic.shape)
            max_freq_pair = freq_pairs[max_idx]
            max_freq1, max_freq2 = max_freq_pair
            
            # Surrogate analysis for significance testing
            n_surrogates = 20
            surrogate_maxbic = []
            
            for i in range(n_surrogates):
                # Create phase-randomized surrogate
                surrogate = self.phase_randomize(data)
                # Calculate bicoherence
                s_bic, _ = self.bicoherence(surrogate, segment_size, 50)
                # Store maximum value
                surrogate_maxbic.append(np.max(s_bic))
            
            # Calculate significance
            surrogate_mean = np.mean(surrogate_maxbic)
            surrogate_std = np.std(surrogate_maxbic)
            
            z_score = (max_bic - surrogate_mean) / surrogate_std if surrogate_std > 0 else 0
            
            # Check if maximum bicoherence is near Ki-related frequencies
            ki_detected = False
            ki_pair = None
            
            for name1, idx1 in ki_indices.items():
                for name2, idx2 in ki_indices.items():
                    # Check if the sum frequency is within bounds
                    sum_idx = min(idx1 + idx2, len(freq) - 1)
                    
                    # Get bicoherence value at these indices
                    if idx1 < bic.shape[0] and idx2 < bic.shape[1]:
                        bic_value = bic[idx1, idx2]
                        
                        # Check if the value is significant
                        if bic_value > surrogate_mean + self.significance * surrogate_std:
                            ki_detected = True
                            ki_pair = (name1, name2, bic_value)
                            break
                
                if ki_detected:
                    break
            
            # Create result if significant
            if z_score >= self.significance:
                from datetime import datetime
                result = self.analyzer.AnalysisResult(
                    trace_id=f"Bicoherence",
                    start_time=datetime.now(),
                    end_time=datetime.now()
                )
                
                # Add metrics
                result.add_metric("max_bicoherence", max_bic)
                result.add_metric("bic_significance", z_score)
                result.add_metric("freq1", max_freq1)
                result.add_metric("freq2", max_freq2)
                
                # Add Ki-related information if detected
                if ki_detected:
                    result.add_metric("ki_bic_detected", 1)
                    result.add_metric("ki_bic_value", ki_pair[2])
                    result.add_metric("ki_freq1", ki_pair[0])
                    result.add_metric("ki_freq2", ki_pair[1])
                
                # Add pattern data for plotting
                result.add_pattern("bic_matrix", bic)
                result.add_pattern("freq", freq)
                result.add_pattern("ki_indices", ki_indices)
                result.add_pattern("surrogate_maxbic", surrogate_maxbic)
                
        except Exception as e:
            print(f"Error in bicoherence analysis: {e}")
        
        return result
    
    def analyze_phase_synchronization(self, data, sampling_rate, frequency_bands):
        """
        Analyze phase synchronization between frequency bands
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
        sampling_rate : float
            Sampling rate in Hz
        frequency_bands : dict
            Dictionary of frequency bands
            
        Returns:
        --------
        AnalysisResult or None
            Analysis result if significant synchronization found, None otherwise
        """
        # Initialize result
        result = None
        
        # Extract Ki-related frequency bands
        ki_bands = {k: v for k, v in frequency_bands.items() if k.startswith('ki_')}
        
        # Check if we have enough Ki bands to analyze
        if len(ki_bands) < 2:
            return None
        
        # Calculate phase for each band
        phase_series = {}
        for name, band in ki_bands.items():
            # Filter data
            filtered = self.filter_data(data, sampling_rate, band[0], band[1])
            # Calculate phase
            phase = np.angle(hilbert(filtered))
            phase_series[name] = phase
        
        # Calculate pairwise phase synchronization index
        sync_indices = {}
        max_sync = 0
        max_pair = None
        
        for name1 in phase_series:
            for name2 in phase_series:
                if name1 >= name2:  # Skip duplicates
                    continue
                
                # Calculate phase synchronization
                phase1 = phase_series[name1]
                phase2 = phase_series[name2]
                
                # n:m synchronization where n:m are related to Ki numbers
                ratio_n = 1
                ratio_m = 1
                
                # If using primary and alternative Ki
                if (name1 == 'ki_fundamental' and name2 == 'ki_alt_fundamental') or \
                   (name2 == 'ki_fundamental' and name1 == 'ki_alt_fundamental'):
                    # Calculate the ratio
                    ratio_n = round(self.ki_value)
                    ratio_m = round(self.alt_ki)
                
                sync_index = self.phase_synchronization_index(phase1, phase2, ratio_n, ratio_m)
                sync_indices[(name1, name2)] = sync_index
                
                if sync_index > max_sync:
                    max_sync = sync_index
                    max_pair = (name1, name2)
        
        # Calculate surrogate distribution
        if max_pair:
            n_surrogates = 50
            surrogate_values = []
            
            phase1 = phase_series[max_pair[0]]
            phase2 = phase_series[max_pair[1]]
            
            for i in range(n_surrogates):
                # Shuffle second phase
                shuffled_phase = np.random.permutation(phase2)
                # Calculate synchronization
                sync = self.phase_synchronization_index(phase1, shuffled_phase)
                surrogate_values.append(sync)
            
            # Calculate significance
            surrogate_mean = np.mean(surrogate_values)
            surrogate_std = np.std(surrogate_values)
            
            z_score = (max_sync - surrogate_mean) / surrogate_std if surrogate_std > 0 else 0
            
            # Create result if significant
            if z_score >= self.significance:
                from datetime import datetime
                result = self.analyzer.AnalysisResult(
                    trace_id=f"PhaseSynchronization",
                    start_time=datetime.now(),
                    end_time=datetime.now()
                )
                
                # Add metrics
                result.add_metric("max_sync_index", max_sync)
                result.add_metric("sync_significance", z_score)
                result.add_metric("sync_band1", max_pair[0])
                result.add_metric("sync_band2", max_pair[1])
                
                # Add pattern data for plotting
                result.add_pattern("sync_indices", sync_indices)
                result.add_pattern("surrogates", surrogate_values)
                
                # Add phase series for plotting
                result.add_plot_data("phase1", phase_series[max_pair[0]])
                result.add_plot_data("phase2", phase_series[max_pair[1]])
        
        return result
    
    def analyze_wavelet_coherence(self, data, sampling_rate, ki_freqs):
        """
        Analyze wavelet coherence to detect Ki-related phase coupling across time
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
        sampling_rate : float
            Sampling rate in Hz
        ki_freqs : dict
            Dictionary of Ki-related frequencies
            
        Returns:
        --------
        AnalysisResult or None
            Analysis result if significant coherence found, None otherwise
        """
        # Initialize result
        result = None
        
        # Only proceed if we have enough samples and pywt is available
        min_samples = 512
        if len(data) < min_samples:
            return None
        
        try:
            # Create two versions of the data to compare for coherence
            # 1. Original data
            # 2. Data shifted by approximately Ki/2 periods
            
            # Determine an appropriate shift
            ki_fundamental_freq = ki_freqs.get('ki_fundamental', 1/self.ki_value)
            if ki_fundamental_freq < 0.1:  # Very low frequency
                return None
                
            ki_period_samples = int(sampling_rate / ki_fundamental_freq)
            shift_samples = ki_period_samples // 2
            
            # Ensure we don't shift too much
            if shift_samples >= len(data) // 2:
                shift_samples = len(data) // 4
            
            # Create shifted data
            data1 = data[:-shift_samples] if shift_samples > 0 else data
            data2 = data[shift_samples:] if shift_samples > 0 else data
            
            # Make sure they're the same length
            min_len = min(len(data1), len(data2))
            data1 = data1[:min_len]
            data2 = data2[:min_len]
            
            # Calculate wavelet coherence
            try:
                import wavelet_coherence
                wct, aWCT, coi = wavelet_coherence.wct(data1, data2, dt=1/sampling_rate)
                
                # Define scales for the wavelet transform
                scales = wavelet_coherence.get_scales(N=min_len, dt=1/sampling_rate, wavelet='morlet', omega0=6)
                
                # Convert scales to frequencies
                frequencies = wavelet_coherence.scales_to_frequencies(scales, wavelet='morlet', omega0=6)
                
                # Calculate mean coherence in bands near Ki frequencies
                ki_coherence = {}
                max_coherence = 0
                max_ki_band = None
                
                for name, ki_freq in ki_freqs.items():
                    if ki_freq < sampling_rate/2:  # Below Nyquist
                        # Find closest frequency
                        idx = np.argmin(np.abs(frequencies - ki_freq))
                        
                        # Extract coherence around this frequency
                        band_start = max(0, idx - 2)
                        band_end = min(len(frequencies), idx + 3)
                        
                        # Calculate mean coherence in this band
                        band_coherence = np.mean(np.abs(wct[band_start:band_end, :]))
                        ki_coherence[name] = band_coherence
                        
                        if band_coherence > max_coherence:
                            max_coherence = band_coherence
                            max_ki_band = name
                
                # Need surrogate analysis for significance
                n_surrogates = 20
                surrogate_values = []
                
                for i in range(n_surrogates):
                    # Create phase-randomized surrogate
                    surrogate = self.phase_randomize(data2)
                    surrogate = surrogate[:min_len]
                    
                    # Calculate wavelet coherence
                    s_wct, _, _ = wavelet_coherence.wct(data1, surrogate, dt=1/sampling_rate)
                    
                    # Calculate mean coherence for max band
                    if max_ki_band:
                        # Find closest frequency
                        idx = np.argmin(np.abs(frequencies - ki_freqs[max_ki_band]))
                        
                        # Extract coherence around this frequency
                        band_start = max(0, idx - 2)
                        band_end = min(len(frequencies), idx + 3)
                        
                        # Calculate mean coherence in this band
                        band_coherence = np.mean(np.abs(s_wct[band_start:band_end, :]))
                        surrogate_values.append(band_coherence)
                
                # Calculate significance
                if surrogate_values:
                    surrogate_mean = np.mean(surrogate_values)
                    surrogate_std = np.std(surrogate_values)
                    
                    z_score = (max_coherence - surrogate_mean) / surrogate_std if surrogate_std > 0 else 0
                    
                    # Create result if significant
                    if z_score >= self.significance:
                        from datetime import datetime
                        result = self.analyzer.AnalysisResult(
                            trace_id=f"WaveletCoherence",
                            start_time=datetime.now(),
                            end_time=datetime.now()
                        )
                        
                        # Add metrics
                        result.add_metric("max_coherence", max_coherence)
                        result.add_metric("coherence_significance", z_score)
                        result.add_metric("max_coherence_band", max_ki_band)
                        result.add_metric("max_coherence_freq", ki_freqs[max_ki_band])
                        
                        # Add pattern data for plotting
                        result.add_pattern("ki_coherence", ki_coherence)
                        result.add_pattern("frequencies", frequencies)
                        result.add_pattern("surrogates", surrogate_values)
                        
                        # Add wavelet data for plotting
                        result.add_plot_data("wct_magnitude", np.abs(wct))
                        result.add_plot_data("wct_phase", np.angle(wct))
                        result.add_plot_data("coi", coi)
            except ImportError:
                # If wavelet_coherence isn't available, try to do a simplified analysis
                from scipy.signal import coherence
                
                # Calculate coherence
                f, coh = coherence(data1, data2, fs=sampling_rate, nperseg=min(256, min_len//4))
                
                # Find coherence at Ki frequencies
                ki_coherence = {}
                max_coherence = 0
                max_ki_band = None
                
                for name, ki_freq in ki_freqs.items():
                    if ki_freq < sampling_rate/2:  # Below Nyquist
                        # Find closest frequency
                        idx = np.argmin(np.abs(f - ki_freq))
                        
                        # Get coherence at this frequency
                        coherence_value = coh[idx]
                        ki_coherence[name] = coherence_value
                        
                        if coherence_value > max_coherence:
                            max_coherence = coherence_value
                            max_ki_band = name
                
                # Create surrogate distribution
                n_surrogates = 50
                surrogate_values = []
                
                for i in range(n_surrogates):
                    # Create phase-randomized surrogate
                    surrogate = self.phase_randomize(data2)
                    surrogate = surrogate[:min_len]
                    
                    # Calculate coherence
                    _, s_coh = coherence(data1, surrogate, fs=sampling_rate, nperseg=min(256, min_len//4))
                    
                    # Find coherence at max Ki frequency
                    if max_ki_band:
                        idx = np.argmin(np.abs(f - ki_freqs[max_ki_band]))
                        surrogate_values.append(s_coh[idx])
                
                # Calculate significance
                if surrogate_values:
                    surrogate_mean = np.mean(surrogate_values)
                    surrogate_std = np.std(surrogate_values)
                    
                    z_score = (max_coherence - surrogate_mean) / surrogate_std if surrogate_std > 0 else 0
                    
                    # Create result if significant
                    if z_score >= self.significance:
                        from datetime import datetime
                        result = self.analyzer.AnalysisResult(
                            trace_id=f"FrequencyCoherence",
                            start_time=datetime.now(),
                            end_time=datetime.now()
                        )
                        
                        # Add metrics
                        result.add_metric("max_coherence", max_coherence)
                        result.add_metric("coherence_significance", z_score)
                        result.add_metric("max_coherence_band", max_ki_band)
                        result.add_metric("max_coherence_freq", ki_freqs[max_ki_band])
                        
                        # Add pattern data for plotting
                        result.add_pattern("ki_coherence", ki_coherence)
                        result.add_pattern("frequencies", f)
                        result.add_pattern("coherence", coh)
                        result.add_pattern("surrogates", surrogate_values)
        
        except Exception as e:
            print(f"Error in wavelet coherence analysis: {e}")
        
        return result
    
    # Helper methods
    
    def filter_data(self, data, sampling_rate, low, high, order=4):
        """
        Apply bandpass filter to data
    
        Parameters:
        -----------
        data : numpy.ndarray
            Signal to filter
        sampling_rate : float
            Sampling rate in Hz
        low : float
            Low cutoff frequency in Hz
        high : float
            High cutoff frequency in Hz
        order : int
            Filter order (default: 4)
        
        Returns:
        --------
        numpy.ndarray
            Filtered signal
        """
        # Normalize frequencies to Nyquist frequency
        nyquist = 0.5 * sampling_rate
    
        # Bound frequencies to valid range (0 < f < 1)
        low_normalized = max(0.001, min(low / nyquist, 0.999))
        high_normalized = max(low_normalized + 0.001, min(high / nyquist, 0.999))
    
        # Create butterworth filter
        b, a = signal.butter(order, [low_normalized, high_normalized], btype='band')
    
        # Apply forward-backward filter to avoid phase shifts
        filtered_data = signal.filtfilt(b, a, data)
    
        return filtered_data
    
    def modulation_index(self, phase, amplitude):
        """
        Calculate the modulation index for phase-amplitude coupling
        
        Parameters:
        -----------
        phase : numpy.ndarray
            Phase time series
        amplitude : numpy.ndarray
            Amplitude envelope time series
            
        Returns:
        --------
        float
            Modulation index [0-1]
        """
        # Number of bins for the phase
        n_bins = 18  # 20° bins
        
        # Create bins for the phase
        phase_bins = np.linspace(-np.pi, np.pi, n_bins + 1)
        
        # Calculate the mean amplitude for each phase bin
        mean_amp = np.zeros(n_bins)
        for i in range(n_bins):
            # Find indices where phase is in this bin
            idx = np.logical_and(phase >= phase_bins[i], phase < phase_bins[i+1])
            
            # Calculate mean amplitude for these indices
            if np.any(idx):
                mean_amp[i] = np.mean(amplitude[idx])
        
        # Normalize
        if np.sum(mean_amp) > 0:
            mean_amp = mean_amp / np.sum(mean_amp)
        
        # Calculate modulation index (KL divergence from uniform)
        uniform = np.ones(n_bins) / n_bins
        mi = np.sum(mean_amp * np.log(mean_amp / uniform))
        
        return mi
    
    def bicoherence(self, data, segmentLength, overlap, sampling_rate):
        """
        Calculate bicoherence to detect quadratic phase coupling
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
        segmentLength : int
            Length of segments for FFT
        overlap : int
            Overlap between segments
            
        Returns:
        --------
        numpy.ndarray
            Bicoherence matrix
        list
            Frequency pairs
        """
        # Ensure segmentLength is at least 2
        segmentLength = max(segmentLength, 2)
        
        # Ensure overlap is less than segmentLength
        overlap = min(overlap, segmentLength - 1)
        
        # Calculate the number of segments
        step = segmentLength - overlap
        n_segments = (len(data) - overlap) // step
        
        # Truncate the data to fit the segments
        data = data[:n_segments * step + overlap]
        
        # Initialize arrays
        fft_data = np.zeros((n_segments, segmentLength//2+1), dtype=complex)
        
        # Calculate FFT for each segment
        for i in range(n_segments):
            start = i * step
            end = start + segmentLength
            segment = data[start:end] * np.hanning(segmentLength)
            fft_data[i, :] = np.fft.rfft(segment)
        
        # Calculate bicoherence
        n_freq = segmentLength//2+1
        bic = np.zeros((n_freq, n_freq))
        
        # Generate frequency pairs for the bicoherence
        freq_pairs = []
        for i in range(n_freq):
            for j in range(n_freq):
                # Ensure we don't go beyond the Nyquist frequency
                if i + j < n_freq:
                    freq_pairs.append((i, j))
        
        # Calculate bicoherence for each frequency pair
        for i, j in freq_pairs:
            # Skip DC component
            if i == 0 or j == 0:
                continue
                
            # Calculate numerator: <X(f1)X(f2)X*(f1+f2)>
            num = np.mean(fft_data[:, i] * fft_data[:, j] * np.conj(fft_data[:, i+j]))
            
            # Calculate denominator: sqrt(<|X(f1)X(f2)|^2><|X(f1+f2)|^2>)
            den1 = np.mean(np.abs(fft_data[:, i] * fft_data[:, j])**2)
            den2 = np.mean(np.abs(fft_data[:, i+j])**2)
            den = np.sqrt(den1 * den2)
            
            # Calculate bicoherence
            if den > 0:
                bic[i, j] = np.abs(num) / den
        
        # Create a list of frequency pairs with actual frequency values
        freq = np.fft.rfftfreq(segmentLength, 1/sampling_rate)
        freq_pairs = [(freq[i], freq[j]) for i, j in freq_pairs]
        
        return bic, freq_pairs
    
    def phase_randomize(self, data):
        """
        Create a phase-randomized surrogate of the data
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
            
        Returns:
        --------
        numpy.ndarray
            Phase-randomized surrogate
        """
        # Calculate FFT
        fft_data = np.fft.rfft(data)
        
        # Create random phases
        n = len(fft_data)
        random_phases = np.random.uniform(0, 2*np.pi, n)
        
        # Set DC component phase to zero
        random_phases[0] = 0
        
        # Apply random phases
        fft_surrogate = np.abs(fft_data) * np.exp(1j * random_phases)
        
        # Inverse FFT
        surrogate = np.fft.irfft(fft_surrogate, len(data))
        
        return surrogate
    
    def phase_synchronization_index(self, phase1, phase2, n=1, m=1):
        """
        Calculate phase synchronization index between two phase time series
        
        Parameters:
        -----------
        phase1 : numpy.ndarray
            First phase time series
        phase2 : numpy.ndarray
            Second phase time series
        n : int
            First ratio component for n:m synchronization
        m : int
            Second ratio component for n:m synchronization
            
        Returns:
        --------
        float
            Phase synchronization index [0-1]
        """
        # Calculate phase difference for n:m synchronization
        phase_diff = (n * phase1 - m * phase2) % (2*np.pi)
        
        # Calculate synchronization index
        # Using circular variance approach
        complex_exp = np.exp(1j * phase_diff)
        mean_complex = np.mean(complex_exp)
        
        # Return magnitude of mean complex exponential
        return np.abs(mean_complex)
    
    def generate_plots(self, result, output_dir):
        """
        Generate plots for the analysis result
        
        Parameters:
        -----------
        result : AnalysisResult
            Analysis result to plot
        output_dir : Path
            Directory to save plots
        """
        import matplotlib.pyplot as plt
        
        # Make sure output directory exists
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Determine which analysis type this is
        module_name = result.metadata.get('module', '')
        trace_id = result.trace_id or 'unknown'
        
        # Handle PAC results
        if trace_id.startswith('PAC_'):
            self._plot_pac_result(result, output_dir)
        
        # Handle Bicoherence results
        elif trace_id.startswith('Bicoherence'):
            self._plot_bicoherence_result(result, output_dir)
        
        # Handle Phase Synchronization results
        elif trace_id.startswith('PhaseSynchronization'):
            self._plot_phase_sync_result(result, output_dir)
        
        # Handle Wavelet Coherence results
        elif trace_id.startswith('WaveletCoherence') or trace_id.startswith('FrequencyCoherence'):
            self._plot_coherence_result(result, output_dir)
    
    def _plot_pac_result(self, result, output_dir):
        """Plot Phase-Amplitude Coupling results"""
        import matplotlib.pyplot as plt
        
        # Extract data from result
        phase_band = result.metrics.get('phase_band', 'unknown')
        amp_band = result.metrics.get('amplitude_band', 'unknown')
        pac_value = result.metrics.get('max_pac_value', 0)
        significance = result.metrics.get('pac_significance', 0)
        
        phase_data = result.plots.get('phase_data', None)
        phase_angle = result.plots.get('phase_angle', None)
        amp_data = result.plots.get('amp_data', None)
        amp_envelope = result.plots.get('amp_envelope', None)
        
        if phase_data is not None and amp_data is not None:
            # Create figure with 3 subplots
            fig, axes = plt.subplots(3, 1, figsize=(10, 12))
            
            # Plot 1: Filtered signals
            ax = axes[0]
            t = np.arange(len(phase_data)) / len(phase_data)  # Normalized time
            ax.plot(t, phase_data / np.max(np.abs(phase_data)), label=f'Phase band ({phase_band})')
            ax.plot(t, amp_data / np.max(np.abs(amp_data)), label=f'Amplitude band ({amp_band})')
            ax.set_xlabel('Normalized Time')
            ax.set_ylabel('Normalized Amplitude')
            ax.set_title('Filtered Signals')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Plot 2: Phase vs Amplitude Envelope
            ax = axes[1]
            if phase_angle is not None and amp_envelope is not None:
                # Create scatter plot of amplitude vs phase
                ax.scatter(phase_angle, amp_envelope, alpha=0.3, s=1)
                
                # Calculate average amplitude at each phase bin
                phase_bins = np.linspace(-np.pi, np.pi, 36)
                mean_amp = np.zeros(len(phase_bins)-1)
                
                for i in range(len(phase_bins)-1):
                    idx = np.logical_and(phase_angle >= phase_bins[i], phase_angle < phase_bins[i+1])
                    if np.any(idx):
                        mean_amp[i] = np.mean(amp_envelope[idx])
                
                # Plot average amplitude
                bin_centers = (phase_bins[:-1] + phase_bins[1:]) / 2
                ax.plot(bin_centers, mean_amp, 'r-', linewidth=2)
                
                ax.set_xlabel('Phase (radians)')
                ax.set_ylabel('Amplitude Envelope')
                ax.set_title(f'Phase-Amplitude Coupling (MI={pac_value:.3f}, Z={significance:.2f})')
                ax.set_xlim(-np.pi, np.pi)
                ax.grid(True, alpha=0.3)
            
            # Plot 3: Significance
            ax = axes[2]
            surrogates = result.patterns.get('surrogates', [])
            if surrogates:
                ax.hist(surrogates, bins=20, alpha=0.7, label='Surrogate Distribution')
                ax.axvline(pac_value, color='r', linestyle='--', label=f'Observed MI={pac_value:.3f}')
                ax.set_xlabel('Modulation Index')
                ax.set_ylabel('Count')
                ax.set_title(f'Significance Testing (Z-score={significance:.2f})')
                ax.legend()
                ax.grid(True, alpha=0.3)
            
            # Adjust layout and save
            plt.tight_layout()
            plt.savefig(output_dir / f'pac_result_{phase_band}_{amp_band}.png', dpi=150)
            plt.close(fig)
    
    def _plot_bicoherence_result(self, result, output_dir):
        """Plot Bicoherence results"""
        import matplotlib.pyplot as plt
        
        # Extract data from result
        bic_matrix = result.patterns.get('bic_matrix', None)
        freq = result.patterns.get('freq', None)
        
        if bic_matrix is not None and freq is not None:
            # Create figure
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            
            # Plot 1: Bicoherence matrix
            ax = axes[0]
            im = ax.imshow(bic_matrix, cmap='hot', aspect='auto', origin='lower', 
                        extent=[freq[0], freq[-1], freq[0], freq[-1]])
            plt.colorbar(im, ax=ax, label='Bicoherence')
            ax.set_xlabel('Frequency 1 (Hz)')
            ax.set_ylabel('Frequency 2 (Hz)')
            ax.set_title('Bicoherence Matrix')
            
            # Add markers for Ki-related frequencies
            ki_indices = result.patterns.get('ki_indices', {})
            for name, idx in ki_indices.items():
                if idx < len(freq):
                    f_val = freq[idx]
                    ax.axhline(y=f_val, color='cyan', linestyle='--', alpha=0.5)
                    ax.axvline(x=f_val, color='cyan', linestyle='--', alpha=0.5)
                    ax.text(freq[-1]*0.9, f_val, name, color='white', fontsize=8, 
                           bbox=dict(facecolor='blue', alpha=0.5))
            
            # Plot 2: Histogram of maximum bicoherence values
            ax = axes[1]
            max_bic = result.metrics.get('max_bicoherence', 0)
            surrogate_maxbic = result.patterns.get('surrogate_maxbic', [])
            
            if surrogate_maxbic:
                ax.hist(surrogate_maxbic, bins=20, alpha=0.7, label='Surrogate Distribution')
                ax.axvline(max_bic, color='r', linestyle='--', label=f'Observed Max={max_bic:.3f}')
                ax.set_xlabel('Maximum Bicoherence')
                ax.set_ylabel('Count')
                ax.set_title(f'Significance Testing (Z-score={result.metrics.get("bic_significance", 0):.2f})')
                ax.legend()
                ax.grid(True, alpha=0.3)
            
            # Adjust layout and save
            plt.tight_layout()
            plt.savefig(output_dir / 'bicoherence_result.png', dpi=150)
            plt.close(fig)
    
    def _plot_phase_sync_result(self, result, output_dir):
        """Plot Phase Synchronization results"""
        import matplotlib.pyplot as plt
        
        # Extract data from result
        phase1 = result.plots.get('phase1', None)
        phase2 = result.plots.get('phase2', None)
        sync_indices = result.patterns.get('sync_indices', {})
        
        if phase1 is not None and phase2 is not None:
            # Create figure with 2 subplots
            fig, axes = plt.subplots(2, 1, figsize=(10, 8))
            
            # Plot 1: Phase timeseries
            ax = axes[0]
            t = np.arange(len(phase1)) / len(phase1)  # Normalized time
            ax.plot(t, np.cos(phase1), label=f'Band 1 ({result.metrics.get("sync_band1", "unknown")})')
            ax.plot(t, np.cos(phase2), label=f'Band 2 ({result.metrics.get("sync_band2", "unknown")})')
            ax.set_xlabel('Normalized Time')
            ax.set_ylabel('Cos(Phase)')
            ax.set_title('Phase Time Series')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Plot 2: Synchronization Indices and Significance
            ax = axes[1]
            
            # Create bar chart of sync indices
            if sync_indices:
                labels = [f"{k[0]}-{k[1]}" for k in sync_indices.keys()]
                values = list(sync_indices.values())
                x = np.arange(len(labels))
                
                ax.bar(x, values, width=0.6, alpha=0.7)
                ax.set_xlabel('Frequency Band Pairs')
                ax.set_ylabel('Sync Index')
                ax.set_title(f'Phase Synchronization Indices (Max={result.metrics.get("max_sync_index", 0):.3f})')
                ax.set_xticks(x)
                ax.set_xticklabels(labels, rotation=90)
                ax.grid(True, alpha=0.3)
                
                # Add significance information
                surrogates = result.patterns.get('surrogates', [])
                if surrogates:
                    ax2 = ax.twinx()
                    ax2.hist(surrogates, bins=10, alpha=0.3, color='gray')
                    ax2.axvline(result.metrics.get('max_sync_index', 0), color='r', linestyle='--')
                    ax2.set_ylabel('Surrogate Count')
            
            # Adjust layout and save
            plt.tight_layout()
            plt.savefig(output_dir / 'phase_sync_result.png', dpi=150)
            plt.close(fig)
    
    def _plot_coherence_result(self, result, output_dir):
        """Plot Coherence results"""
        import matplotlib.pyplot as plt
        
        # Extract data from result
        if 'WaveletCoherence' in result.trace_id:
            # Handle wavelet coherence result
            wct_magnitude = result.plots.get('wct_magnitude', None)
            wct_phase = result.plots.get('wct_phase', None)
            frequencies = result.patterns.get('frequencies', None)
            
            if wct_magnitude is not None and frequencies is not None:
                # Create figure with 2 subplots
                fig, axes = plt.subplots(2, 1, figsize=(10, 10))
                
                # Plot 1: Wavelet coherence magnitude
                ax = axes[0]
                t = np.arange(wct_magnitude.shape[1])  # Time points
                extent = [t[0], t[-1], frequencies[-1], frequencies[0]]  # Note frequency is flipped for imshow
                
                im = ax.imshow(wct_magnitude, aspect='auto', extent=extent, cmap='jet', vmin=0, vmax=1)
                plt.colorbar(im, ax=ax, label='Coherence Magnitude')
                ax.set_xlabel('Time (samples)')
                ax.set_ylabel('Frequency (Hz)')
                ax.set_title(f'Wavelet Coherence Magnitude (Max={result.metrics.get("max_coherence", 0):.3f})')
                
                # Add markers for Ki-related frequencies
                ki_coherence = result.patterns.get('ki_coherence', {})
                for name, _ in ki_coherence.items():
                    ki_freq = result.metrics.get('max_coherence_freq', 0)
                    if ki_freq > 0:
                        ax.axhline(y=ki_freq, color='white', linestyle='--', alpha=0.7)
                        ax.text(t[-1]*0.9, ki_freq, name, color='white', fontsize=8,
                               bbox=dict(facecolor='black', alpha=0.5))
                
                # Plot 2: Coherence at Ki frequencies
                ax = axes[1]
                if ki_coherence:
                    names = list(ki_coherence.keys())
                    values = list(ki_coherence.values())
                    x = np.arange(len(names))
                    
                    ax.bar(x, values, width=0.6, alpha=0.7)
                    ax.set_xlabel('Ki-related Frequency Bands')
                    ax.set_ylabel('Mean Coherence')
                    ax.set_title(f'Coherence at Ki Frequencies (Z-score={result.metrics.get("coherence_significance", 0):.2f})')
                    ax.set_xticks(x)
                    ax.set_xticklabels(names, rotation=90)
                    ax.grid(True, alpha=0.3)
                    
                    # Add significance threshold
                    surrogates = result.patterns.get('surrogates', [])
                    if surrogates:
                        surrogate_mean = np.mean(surrogates)
                        surrogate_std = np.std(surrogates)
                        threshold = surrogate_mean + self.significance * surrogate_std
                        ax.axhline(y=threshold, color='r', linestyle='--', label=f'Significance Threshold')
                        ax.legend()
                
                # Adjust layout and save
                plt.tight_layout()
                plt.savefig(output_dir / 'wavelet_coherence_result.png', dpi=150)
                plt.close(fig)
                
        else:
            # Handle frequency coherence result
            frequencies = result.patterns.get('frequencies', None)
            coherence = result.patterns.get('coherence', None)
            
            if frequencies is not None and coherence is not None:
                # Create figure with 2 subplots
                fig, axes = plt.subplots(2, 1, figsize=(10, 8))
                
                # Plot 1: Coherence spectrum
                ax = axes[0]
                ax.plot(frequencies, coherence)
                ax.set_xlabel('Frequency (Hz)')
                ax.set_ylabel('Coherence')
                ax.set_title('Frequency Coherence Spectrum')
                ax.grid(True, alpha=0.3)
                
                # Add markers for Ki-related frequencies
                ki_coherence = result.patterns.get('ki_coherence', {})
                for name, value in ki_coherence.items():
                    ki_freq = result.metrics.get('max_coherence_freq', 0)
                    if name == result.metrics.get('max_coherence_band', '') and ki_freq > 0:
                        ax.plot(ki_freq, value, 'ro', markersize=8)
                        ax.annotate(name, xy=(ki_freq, value), xytext=(10, 0), 
                                  textcoords='offset points', fontsize=8)
                
                # Plot 2: Ki coherence values
                ax = axes[1]
                if ki_coherence:
                    names = list(ki_coherence.keys())
                    values = list(ki_coherence.values())
                    x = np.arange(len(names))
                    
                    ax.bar(x, values, width=0.6, alpha=0.7)
                    ax.set_xlabel('Ki-related Frequency Bands')
                    ax.set_ylabel('Coherence')
                    ax.set_title(f'Coherence at Ki Frequencies (Z-score={result.metrics.get("coherence_significance", 0):.2f})')
                    ax.set_xticks(x)
                    ax.set_xticklabels(names, rotation=90)
                    ax.grid(True, alpha=0.3)
                    
                    # Add significance threshold
                    surrogates = result.patterns.get('surrogates', [])
                    if surrogates:
                        surrogate_mean = np.mean(surrogates)
                        surrogate_std = np.std(surrogates)
                        threshold = surrogate_mean + self.significance * surrogate_std
                        ax.axhline(y=threshold, color='r', linestyle='--', label=f'Significance Threshold')
                        ax.legend()
                
                # Adjust layout and save
                plt.tight_layout()
                plt.savefig(output_dir / 'frequency_coherence_result.png', dpi=150)
                plt.close(fig)