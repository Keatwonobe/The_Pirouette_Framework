import numpy as np
from scipy import signal, stats
import matplotlib.pyplot as plt
from scipy.stats import kurtosis, skew
import pywt


class TemporalStructureAnalyzer:
    """
    Analyzes time series data for temporal structures related to Ki values.
    
    This module identifies rhythmic patterns, cyclical components, and
    temporal coherence structures that correspond to known Ki-related frequencies
    and patterns.
    """
    
    def __init__(self, analyzer):
        """
        Initialize the analyzer
        
        Parameters:
        -----------
        analyzer : KiResonanceAnalyzer
            The parent analyzer object
        """
        self.analyzer = analyzer
        self.ki_value = analyzer.ki_value
        self.alternate_ki = analyzer.alternate_ki
        self.pi = 3.14159
        self.significance_threshold = analyzer.significance_threshold
    
    def analyze(self, trace, processed_trace=None, **kwargs):
        """
        Analyze a trace for temporal structures related to Ki
        
        Parameters:
        -----------
        trace : obspy.Trace
            The trace to analyze
        processed_trace : obspy.Trace or None
            A preprocessed version of the trace, if available
        
        Returns:
        --------
        list of AnalysisResult
            Analysis results, or empty list if no patterns found
        """
        # Use processed trace if available, otherwise use original
        data = processed_trace.data if processed_trace is not None else trace.data
        sampling_rate = trace.stats.sampling_rate
        
        results = []
        
        # Check if we have enough data points
        if len(data) < 1000:
            return results
        
        # 1. Analyze block entropy structure
        try:
            entropy_result = self._analyze_block_entropy(data, sampling_rate, trace.id, trace)
            if entropy_result:
                results.append(entropy_result)
        except Exception as e:
            print(f"Error in block entropy analysis: {str(e)}")
        
        # 2. Analyze temporal recurrence patterns
        try:
            recurrence_result = self._analyze_recurrence_patterns(data, sampling_rate, trace.id, trace)
            if recurrence_result:
                results.append(recurrence_result)
        except Exception as e:
            print(f"Error in recurrence patterns analysis: {str(e)}")
        
        # 3. Analyze rhythm stability related to Ki values
        try:
            rhythm_result = self._analyze_rhythm_stability(data, sampling_rate, trace.id, trace)
            if rhythm_result:
                results.append(rhythm_result)
        except Exception as e:
            print(f"Error in rhythm stability analysis: {str(e)}")
        
        # 4. Analyze wavelet scalogram for Ki-related structures
        try:
            wavelet_result = self._analyze_wavelet_structures(data, sampling_rate, trace.id, trace)
            if wavelet_result:
                results.append(wavelet_result)
        except Exception as e:
            print(f"Error in wavelet structures analysis: {str(e)}")
        
        return results
    
    def _analyze_block_entropy(self, data, sampling_rate, trace_id, trace):
        """
        Analyze the entropy structure of fixed-size blocks
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
        sampling_rate : float
            Sampling rate in Hz
        trace_id : str
            Identifier for the trace
        trace : obspy.Trace
            The original trace object
            
        Returns:
        --------
        AnalysisResult or None
            Analysis result if significant patterns found, None otherwise
        """
        # Fix the import to specifically get entropy from scipy.stats
        from scipy.stats import entropy as scipy_entropy
        from obspy.core.utcdatetime import UTCDateTime
        
        # Calculate block sizes based on Ki-related timescales
        ki_period = max(10, int(sampling_rate / self.ki_value))
        pi_period = max(10, int(sampling_rate / self.pi))
        
        # Create list of block sizes to test
        block_sizes = [
            ki_period,
            pi_period,
            max(10, int(ki_period * self.pi / 2)),
            max(10, int(ki_period * 2)),
            max(10, int(ki_period / 2))
        ]
        
        # Filter out invalid block sizes
        block_sizes = [size for size in block_sizes if 10 < size < len(data) // 10]
        
        if not block_sizes:
            return None
        
        # Calculate entropy for each block size
        entropy_results = {}
        entropy_significance = {}
        max_significance = 0
        best_block_size = None
        
        for block_size in block_sizes:
            # Split data into blocks
            n_blocks = len(data) // block_size
            blocks = np.array_split(data[:n_blocks * block_size], n_blocks)
            
            # Calculate entropy for each block
            block_entropies = []
            for block in blocks:
                # Create histogram
                hist, _ = np.histogram(block, bins=20, density=True)
                # Add small value to avoid zeros
                hist = hist + 1e-10
                # Normalize
                hist = hist / np.sum(hist)
                # Calculate entropy - using direct method to avoid issues
                ent = -np.sum(hist * np.log2(hist))
                block_entropies.append(ent)
            
            # Calculate entropy rhythm
            if len(block_entropies) <= 1:
                continue
                
            entropy_diff = np.diff(block_entropies)
            
            # Look for pattern: calculate autocorrelation
            acf = np.correlate(entropy_diff, entropy_diff, mode='full')
            acf = acf[len(acf)//2:]
            if acf[0] != 0:
                acf = acf / acf[0]  # Normalize
            else:
                continue  # Skip if autocorrelation is zero
            
            # Find peaks in autocorrelation
            try:
                peaks, _ = signal.find_peaks(acf, height=0.2, distance=3)
            except Exception:
                continue
            
            # Calculate rhythm metrics
            if len(peaks) > 1:
                # Check if peak intervals are related to Ki
                peak_intervals = np.diff(peaks)
                
                # Calculate closeness to Ki-related values
                ki_relatedness = []
                for interval in peak_intervals:
                    ki_rel = min(
                        abs(interval - ki_period/block_size),
                        abs(interval - (self.pi/self.ki_value) * ki_period/block_size),
                        abs(interval - 2 * ki_period/block_size),
                        abs(interval - ki_period/(2 * block_size))
                    ) / (ki_period/block_size)
                    ki_relatedness.append(ki_rel)
                
                # Calculate mean Ki relatedness (lower is better)
                mean_ki_rel = np.mean(ki_relatedness) if ki_relatedness else 1.0
                
                # Calculate significance (1/mean_ki_rel, higher is better)
                significance = 1 / (mean_ki_rel + 0.01)  # Avoid division by zero
                
                # Save results
                entropy_results[block_size] = {
                    'entropies': block_entropies,
                    'acf': acf.tolist(),  # Convert to list for serialization
                    'peaks': peaks.tolist(),  # Convert to list for serialization
                    'ki_relatedness': ki_relatedness,
                    'significance': significance
                }
                
                entropy_significance[block_size] = significance
                
                # Track best result
                if significance > max_significance:
                    max_significance = significance
                    best_block_size = block_size
        
        # If no significant results found
        if not best_block_size or max_significance < self.significance_threshold:
            return None
        
        # Create result object
        result = self.analyzer.AnalysisResult(trace_id=trace_id)
        
        # Add metrics
        result.add_metric('entropy_block_significance', max_significance)
        result.add_metric('entropy_block_size', best_block_size)
        result.add_metric('entropy_block_ki_relation', 1/entropy_significance[best_block_size])
        
        # Add detected pattern
        result.add_pattern('entropy_blocks', entropy_results[best_block_size])
        
        # Add plot data
        result.add_plot_data('entropy_blocks', {
            'block_size': best_block_size,
            'entropies': entropy_results[best_block_size]['entropies'],
            'acf': entropy_results[best_block_size]['acf'],
            'peaks': entropy_results[best_block_size]['peaks']
        })
        
        result.add_metadata('analysis_type', 'entropy_block_structure')
        
        # Set tentative time range if possible
        try:
            start_time = UTCDateTime(trace.stats.starttime)
            end_time = UTCDateTime(trace.stats.endtime)
            result.start_time = start_time
            result.end_time = end_time
        except Exception:
            pass
        
        return result
    
    def _analyze_recurrence_patterns(self, data, sampling_rate, trace_id, trace):
        """
        Analyze recurrence patterns in the time series
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
        sampling_rate : float
            Sampling rate in Hz
        trace_id : str
            Identifier for the trace
        trace : obspy.Trace
            The original trace object
            
        Returns:
        --------
        AnalysisResult or None
            Analysis result if significant patterns found, None otherwise
        """
        from obspy.core.utcdatetime import UTCDateTime
        
        # Downsample if necessary to make computation manageable
        max_points = 2000  # Reduced from 5000 to prevent hanging
        if len(data) > max_points:
            downsample_factor = len(data) // max_points
            data_downsampled = signal.decimate(data, downsample_factor)
        else:
            downsample_factor = 1
            data_downsampled = data
        
        # Normalize data
        data_norm = (data_downsampled - np.mean(data_downsampled)) / (np.std(data_downsampled) + 1e-10)
        
        # Calculate recurrence matrix
        # A recurrence occurs when points in phase space are close
        threshold = 0.1
        N = len(data_norm)
        # Use a simplified recurrence calculation
        recurrence = np.zeros((N, N))
        
        # Instead of full matrix, compute only diagonal bands
        # to save computation time
        max_lag = min(500, N//4)  # Reduced from 1000 to prevent hanging
        
        # Calculate main diagonals
        for lag in range(1, max_lag):
            # Calculate distance between points separated by lag
            distance = np.abs(data_norm[lag:] - data_norm[:-lag])
            # Create recurrence points where distance is below threshold
            recurrence_points = distance < threshold
            # Place in matrix (only store a downsampled version if large)
            if len(recurrence_points) > 1000:
                step = len(recurrence_points) // 1000
                for i in range(0, len(recurrence_points), step):
                    if i < len(recurrence_points) and recurrence_points[i]:
                        j = min(i+lag, N-1)
                        recurrence[i, j] = 1
                        recurrence[j, i] = 1
            else:
                for i in range(len(recurrence_points)):
                    if recurrence_points[i]:
                        recurrence[i, i+lag] = 1
                        recurrence[i+lag, i] = 1
        
        # Calculate diagonal line statistics (simplified)
        min_line_length = 3
        diagonal_lines = []
        
        # Check diagonals parallel to the main diagonal
        for k in range(1, max_lag, max(1, max_lag//20)):  # Skip some diagonals to speed up
            # Extract diagonal
            diag = np.diag(recurrence, k)
            # Find continuous sequences of 1s
            line_lengths = []
            current_length = 0
            for val in diag:
                if val == 1:
                    current_length += 1
                else:
                    if current_length >= min_line_length:
                        line_lengths.append(current_length)
                    current_length = 0
            # Add last line if exists
            if current_length >= min_line_length:
                line_lengths.append(current_length)
            
            diagonal_lines.extend(line_lengths)
        
        # If no diagonal lines found
        if not diagonal_lines:
            return None
        
        # Calculate recurrence time
        recurrence_times = [t * downsample_factor / sampling_rate for t in np.where(np.diag(recurrence, 1) == 1)[0]]
        
        # If no recurrence times found
        if not recurrence_times:
            return None
        
        # Calculate intervals between recurrences
        recurrence_intervals = np.diff(recurrence_times)
        
        # If no intervals found
        if len(recurrence_intervals) < 2:
            return None
        
        # Check if intervals are related to Ki
        ki_time = 1 / (self.ki_value / (2 * np.pi))
        pi_time = 1 / (self.pi / (2 * np.pi))
        
        ki_relatedness = []
        for interval in recurrence_intervals:
            # Calculate how close the interval is to multiples of ki_time
            ki_rel = min(
                abs(interval - ki_time) / ki_time,
                abs(interval - (ki_time * 2)) / (ki_time * 2),
                abs(interval - (ki_time / 2)) / (ki_time / 2),
                abs(interval - (ki_time * self.pi / self.ki_value)) / (ki_time * self.pi / self.ki_value)
            )
            ki_relatedness.append(ki_rel)
        
        # Calculate mean Ki relatedness (lower is better)
        mean_ki_error = np.mean(ki_relatedness)
        
        # Calculate significance (1/mean_ki_error, higher is better)
        significance = 1 / (mean_ki_error + 0.01)  # Avoid division by zero
        
        # If not significant
        if significance < self.significance_threshold:
            return None
        
        # Create result object
        result = self.analyzer.AnalysisResult(trace_id=trace_id)
        
        # Add metrics
        result.add_metric('recurrence_significance', significance)
        result.add_metric('recurrence_mean_error', mean_ki_error)
        result.add_metric('recurrence_line_count', len(diagonal_lines))
        
        # Add patterns
        result.add_pattern('recurrence_intervals', recurrence_intervals.tolist())
        result.add_pattern('recurrence_times', recurrence_times)
        
        # If matrix is large, store a downsampled version
        if recurrence.shape[0] > 500:
            step = recurrence.shape[0] // 500
            recurrence_downsampled = recurrence[::step, ::step]
        else:
            recurrence_downsampled = recurrence
            
        # Add plot data
        result.add_plot_data('recurrence_matrix', {
            'matrix': recurrence_downsampled.tolist(),
            'threshold': threshold,
            'diagonal_lines': diagonal_lines,
            'recurrence_intervals': recurrence_intervals.tolist()
        })
        
        result.add_metadata('analysis_type', 'recurrence_patterns')
        
        # Set tentative time range if possible
        try:
            start_time = UTCDateTime(trace.stats.starttime)
            end_time = UTCDateTime(trace.stats.endtime)
            result.start_time = start_time
            result.end_time = end_time
        except Exception:
            pass
        
        return result
    
    def _analyze_rhythm_stability(self, data, sampling_rate, trace_id, trace):
        """
        Analyze rhythm stability and its relationship to Ki values
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
        sampling_rate : float
            Sampling rate in Hz
        trace_id : str
            Identifier for the trace
        trace : obspy.Trace
            The original trace object
            
        Returns:
        --------
        AnalysisResult or None
            Analysis result if significant patterns found, None otherwise
        """
        from obspy.core.utcdatetime import UTCDateTime
        
        # Calculate expected periods for Ki and related values
        ki_period = sampling_rate / self.ki_value
        pi_period = sampling_rate / self.pi
        alt_ki_period = sampling_rate / self.alternate_ki
        
        # Create a list of periods to search for
        search_periods = [
            ki_period,
            pi_period,
            alt_ki_period,
            ki_period * 2,
            ki_period / 2,
            ki_period * self.pi / self.ki_value
        ]
        
        # Ensure minimum distance is reasonable
        min_distance = max(5, int(min(search_periods) / 4))
        
        # Find local maxima (peaks) in the signal
        try:
            peaks, peak_props = signal.find_peaks(data, distance=min_distance)
        except Exception:
            # Try with normalized data
            data_norm = (data - np.mean(data)) / (np.std(data) + 1e-10)
            try:
                peaks, peak_props = signal.find_peaks(data_norm, distance=min_distance)
            except Exception:
                return None
        
        # If not enough peaks found
        if len(peaks) < 10:
            # Try with the negative of the signal
            try:
                peaks, peak_props = signal.find_peaks(-data, distance=min_distance)
            except Exception:
                return None
                
            if len(peaks) < 10:
                return None
        
        # Calculate intervals between peaks
        peak_intervals = np.diff(peaks)
        
        # If not enough intervals
        if len(peak_intervals) < 5:
            return None
        
        # Calculate statistics of intervals
        mean_interval = np.mean(peak_intervals)
        std_interval = np.std(peak_intervals)
        cv_interval = std_interval / (mean_interval + 1e-10)  # Coefficient of variation
        
        # Check if mean interval is related to Ki periods
        ki_relatedness = []
        for period in search_periods:
            # Calculate distance to integer multiples of period
            multiple = mean_interval / period
            error = abs(multiple - round(multiple))
            ki_relatedness.append((period, error))
        
        # Find closest Ki-related period
        closest_period, min_error = min(ki_relatedness, key=lambda x: x[1])
        
        # Calculate rhythmicity index (0 = perfect rhythm, higher = more irregular)
        rhythm_index = cv_interval * min_error
        
        # Calculate significance (1/rhythm_index, higher is better)
        significance = 1 / (rhythm_index + 0.01)  # Avoid division by zero
        
        # If not significant
        if significance < self.significance_threshold:
            return None
        
        # Create result object
        result = self.analyzer.AnalysisResult(trace_id=trace_id)
        
        # Add metrics
        result.add_metric('rhythm_significance', significance)
        result.add_metric('rhythm_variability', cv_interval)
        result.add_metric('rhythm_ki_error', min_error)
        result.add_metric('rhythm_period', mean_interval)
        result.add_metric('rhythm_closest_ki_period', closest_period)
        
        # Add patterns
        result.add_pattern('rhythm_peaks', peaks.tolist())
        result.add_pattern('rhythm_intervals', peak_intervals.tolist())
        
        # For large signals, downsample for plotting
        if len(data) > 10000:
            data_plot = signal.resample(data, 10000).tolist()
        else:
            data_plot = data.tolist()
            
        # Add plot data
        result.add_plot_data('rhythm_analysis', {
            'data': data_plot,
            'peaks': peaks.tolist(),
            'intervals': peak_intervals.tolist(),
            'mean_interval': mean_interval,
            'ki_periods': search_periods
        })
        
        result.add_metadata('analysis_type', 'rhythm_stability')
        
        # Set tentative time range if possible
        try:
            start_time = UTCDateTime(trace.stats.starttime)
            end_time = UTCDateTime(trace.stats.endtime)
            result.start_time = start_time
            result.end_time = end_time
        except Exception:
            pass
        
        return result
    
    def _analyze_wavelet_structures(self, data, sampling_rate, trace_id, trace):
        """
        Analyze wavelet scalogram for structures related to Ki
        
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data
        sampling_rate : float
            Sampling rate in Hz
        trace_id : str
            Identifier for the trace
        trace : obspy.Trace
            The original trace object
            
        Returns:
        --------
        AnalysisResult or None
            Analysis result if significant patterns found, None otherwise
        """
        from obspy.core.utcdatetime import UTCDateTime
        
        # Downsample if necessary to make computation manageable
        max_points = 4096  # Reduced from 8192 to prevent hanging
        if len(data) > max_points:
            downsample_factor = len(data) // max_points
            data_downsampled = signal.decimate(data, downsample_factor)
            effective_sampling_rate = sampling_rate / downsample_factor
        else:
            data_downsampled = data
            effective_sampling_rate = sampling_rate
            downsample_factor = 1
        
        # Normalize data
        data_norm = (data_downsampled - np.mean(data_downsampled)) / (np.std(data_downsampled) + 1e-10)
        
        try:
            # Use fewer scales for faster computation
            scales = np.arange(1, 64, 2)  # Reduced from 128 to prevent hanging
            
            # Use a simpler wavelet for faster computation
            wavelet = 'morl'  # Use Morlet wavelet which is faster than complex Morlet
            
            # Calculate CWT
            coefficients, frequencies = pywt.cwt(data_norm, scales, wavelet, 1.0 / effective_sampling_rate)
            
            # Calculate wavelet power spectrum
            power = (abs(coefficients)) ** 2
            
            # Calculate global wavelet spectrum (average over time)
            global_spectrum = np.mean(power, axis=1)
            
            # Find peaks in global spectrum
            peaks, _ = signal.find_peaks(global_spectrum, height=np.mean(global_spectrum), distance=3)
            
            if len(peaks) == 0:
                return None
            
            # Convert peak scales to frequencies
            peak_freqs = frequencies[peaks]
            
            # Calculate expected Ki-related frequencies
            ki_freqs = self.analyzer.get_ki_phase_frequencies(effective_sampling_rate)
            
            # Keep only frequencies below Nyquist
            ki_freqs = {k: v for k, v in ki_freqs.items() if v < effective_sampling_rate / 2}
            
            # Check if peaks are close to Ki-related frequencies
            ki_match_scores = []
            
            for name, ki_freq in ki_freqs.items():
                # Find closest peak
                closest_idx = np.argmin(np.abs(peak_freqs - ki_freq))
                closest_freq = peak_freqs[closest_idx]
                
                # Calculate relative error
                rel_error = abs(closest_freq - ki_freq) / ki_freq
                
                # Calculate significance (1/rel_error, higher is better)
                match_score = 1 / (rel_error + 0.01)  # Avoid division by zero
                
                ki_match_scores.append((name, ki_freq, closest_freq, match_score))
            
            # If no good matches
            if not ki_match_scores:
                return None
            
            # Find best match
            best_match = max(ki_match_scores, key=lambda x: x[3])
            
            # If best match is not significant
            if best_match[3] < self.significance_threshold:
                return None
            
            # Create result object
            result = self.analyzer.AnalysisResult(trace_id=trace_id)
            
            # Add metrics
            result.add_metric('wavelet_ki_significance', best_match[3])
            result.add_metric('wavelet_ki_frequency', best_match[1])
            result.add_metric('wavelet_peak_frequency', best_match[2])
            result.add_metric('wavelet_relative_error', 1 / best_match[3])
            
            # Add patterns
            result.add_pattern('wavelet_peaks', peak_freqs.tolist())
            result.add_pattern('wavelet_ki_matches', ki_match_scores)
            
            # Add plot data (store a downsampled version of the power if it's large)
            max_coefs = 500  # Reduced from 1000 to prevent large data storage
            if power.shape[1] > max_coefs:
                time_downsample = power.shape[1] // max_coefs
                power_downsampled = power[:, ::time_downsample]
            else:
                power_downsampled = power
                
            result.add_plot_data('wavelet_scalogram', {
                'power': power_downsampled.tolist(),
                'scales': scales.tolist(),
                'frequencies': frequencies.tolist(),
                'global_spectrum': global_spectrum.tolist(),
                'peaks': peaks.tolist(),
                'best_match': best_match,
                'sampling_rate': effective_sampling_rate
            })
            
            result.add_metadata('analysis_type', 'wavelet_structures')
            result.add_metadata('wavelet_type', wavelet)
            result.add_metadata('ki_match_type', best_match[0])
            
            # Set tentative time range if possible
            try:
                start_time = UTCDateTime(trace.stats.starttime)
                end_time = UTCDateTime(trace.stats.endtime)
                result.start_time = start_time
                result.end_time = end_time
            except Exception:
                pass
            
            return result
            
        except Exception as e:
            print(f"Error in wavelet analysis: {str(e)}")
            return None
    
    def generate_plots(self, result, output_dir_path):
        """
        Generate plots for analysis results
        
        Parameters:
        -----------
        result : AnalysisResult
            The analysis result to plot
        output_dir_path : Path
            Directory to save plots
        """
        import os
        from pathlib import Path
        import matplotlib.pyplot as plt
        
        # Create output directory if it doesn't exist
        output_dir = Path(output_dir_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Get analysis type
        analysis_type = result.metadata.get('analysis_type', 'unknown')
        
        # Generate plots based on analysis type
        if analysis_type == 'entropy_block_structure':
            self._plot_entropy_blocks(result, output_dir)
        elif analysis_type == 'recurrence_patterns':
            self._plot_recurrence_matrix(result, output_dir)
        elif analysis_type == 'rhythm_stability':
            self._plot_rhythm_analysis(result, output_dir)
        elif analysis_type == 'wavelet_structures':
            self._plot_wavelet_scalogram(result, output_dir)
    
    def _plot_entropy_blocks(self, result, output_dir):
        """Plot entropy block structure"""
        plot_data = result.plots.get('entropy_blocks')
        if not plot_data:
            return
        
        block_size = plot_data['block_size']
        entropies = plot_data['entropies']
        acf = plot_data['acf']
        peaks = plot_data['peaks']
        
        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Plot entropy over blocks
        ax1.plot(entropies, '-o', markersize=3)
        ax1.set_title(f'Block Entropy (block size = {block_size})')
        ax1.set_xlabel('Block Number')
        ax1.set_ylabel('Shannon Entropy')
        ax1.grid(True, alpha=0.3)
        
        # Plot autocorrelation
        ax2.plot(acf)
        ax2.plot(peaks, [acf[i] for i in peaks], 'ro')
        ax2.set_title('Entropy Autocorrelation')
        ax2.set_xlabel('Lag')
        ax2.set_ylabel('Autocorrelation')
        ax2.grid(True, alpha=0.3)
        
        # Add Ki-related information to plot
        ki_times = [result.metrics.get('entropy_block_ki_relation', 0)]
        ki_sig = result.metrics.get('entropy_block_significance', 0)
        ax2.text(0.02, 0.95, f'Ki Relation: {ki_times[0]:.2f}\nSignificance: {ki_sig:.2f}',
                transform=ax2.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        # Save the figure
        output_file = output_dir / f"{result.trace_id}_entropy_blocks.png"
        plt.savefig(output_file, dpi=300)
        plt.close(fig)
    
    def _plot_recurrence_matrix(self, result, output_dir):
        """Plot recurrence matrix"""
        plot_data = result.plots.get('recurrence_matrix')
        if not plot_data:
            return
        
        matrix = np.array(plot_data['matrix'])
        threshold = plot_data['threshold']
        recurrence_intervals = plot_data['recurrence_intervals']
        
        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot recurrence matrix
        im = ax1.imshow(matrix, cmap='binary', aspect='auto', origin='lower')
        ax1.set_title(f'Recurrence Matrix (threshold = {threshold:.2f})')
        ax1.set_xlabel('Time Index')
        ax1.set_ylabel('Time Index')
        plt.colorbar(im, ax=ax1)
        
        # Plot histogram of recurrence intervals
        ax2.hist(recurrence_intervals, bins=30, alpha=0.7)
        ax2.set_title('Recurrence Time Intervals')
        ax2.set_xlabel('Interval Length')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        
        # Add Ki-related information to plot
        ki_sig = result.metrics.get('recurrence_significance', 0)
        ki_error = result.metrics.get('recurrence_mean_error', 0)
        ax2.text(0.02, 0.95, f'Ki Significance: {ki_sig:.2f}\nMean Error: {ki_error:.2f}',
                transform=ax2.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        # Save the figure
        output_file = output_dir / f"{result.trace_id}_recurrence_matrix.png"
        plt.savefig(output_file, dpi=300)
        plt.close(fig)
    
    def _plot_rhythm_analysis(self, result, output_dir):
        """Plot rhythm analysis"""
        plot_data = result.plots.get('rhythm_analysis')
        if not plot_data:
            return
        
        data = plot_data['data']
        peaks = plot_data['peaks']
        intervals = plot_data['intervals']
        mean_interval = plot_data['mean_interval']
        ki_periods = plot_data['ki_periods']
        
        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Plot signal with peaks
        time = np.arange(len(data)) / len(data)  # Normalized time
        ax1.plot(time, data)
        
        # Convert peak indices to normalized time
        peak_indices = np.array(peaks)
        if len(data) > 0 and len(peak_indices) > 0:
            peak_times = peak_indices / len(data)
            peak_values = [data[min(p, len(data)-1)] for p in peak_indices]
            ax1.plot(peak_times, peak_values, 'ro', markersize=5)
        
        ax1.set_title('Signal with Detected Peaks')
        ax1.set_xlabel('Normalized Time')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True, alpha=0.3)
        
        # Plot histogram of intervals
        ax2.hist(intervals, bins=20, alpha=0.7)
        
        # Add vertical lines for Ki-related periods
        for period in ki_periods:
            ax2.axvline(x=period, color='r', linestyle='--', alpha=0.5)
        
        # Add vertical line for mean interval
        ax2.axvline(x=mean_interval, color='g', linestyle='-', linewidth=2, label=f'Mean: {mean_interval:.2f}')
        
        ax2.set_title('Peak Interval Distribution')
        ax2.set_xlabel('Interval')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Add Ki-related information to plot
        ki_sig = result.metrics.get('rhythm_significance', 0)
        ki_error = result.metrics.get('rhythm_ki_error', 0)
        closest_period = result.metrics.get('rhythm_closest_ki_period', 0)
        ax2.text(0.02, 0.95, f'Ki Significance: {ki_sig:.2f}\nError: {ki_error:.2f}\nClosest Period: {closest_period:.2f}',
                transform=ax2.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        # Save the figure
        output_file = output_dir / f"{result.trace_id}_rhythm_analysis.png"
        plt.savefig(output_file, dpi=300)
        plt.close(fig)
    
    def _plot_wavelet_scalogram(self, result, output_dir):
        """Plot wavelet scalogram"""
        plot_data = result.plots.get('wavelet_scalogram')
        if not plot_data:
            return
        
        power = np.array(plot_data['power'])
        scales = np.array(plot_data['scales'])
        frequencies = np.array(plot_data['frequencies'])
        global_spectrum = np.array(plot_data['global_spectrum'])
        peaks = np.array(plot_data['peaks'])
        best_match = plot_data['best_match']
        sampling_rate = plot_data['sampling_rate']
        
        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot scalogram
        periods = 1 / frequencies
        times = np.arange(power.shape[1]) / power.shape[1]  # Normalized time
        
        # Use log scale for better visualization
        im = ax1.pcolormesh(times, np.log2(periods), power, cmap='viridis', shading='gouraud')
        
        # Set y-ticks to show actual periods
        yticks = 2**np.arange(np.floor(np.log2(periods.min())), np.ceil(np.log2(periods.max())))
        ax1.set_yticks(np.log2(yticks))
        ax1.set_yticklabels([f"{p:.1f}" for p in yticks])
        
        ax1.set_title('Wavelet Scalogram')
        ax1.set_xlabel('Normalized Time')
        ax1.set_ylabel('Period')
        plt.colorbar(im, ax=ax1, label='Power')
        
        # Plot global wavelet spectrum
        ax2.plot(global_spectrum, np.log2(periods))
        
        # Mark peaks
        peak_periods = periods[peaks]
        ax2.plot(global_spectrum[peaks], np.log2(peak_periods), 'ro')
        
        # Mark best Ki match
        ki_freq = best_match[1]
        ki_period = 1 / ki_freq
        closest_freq = best_match[2]
        closest_period = 1 / closest_freq
        
        ax2.axhline(y=np.log2(ki_period), color='g', linestyle='--', 
                    label=f'Ki Period: {ki_period:.2f}')
        ax2.axhline(y=np.log2(closest_period), color='r', linestyle='-', 
                    label=f'Detected: {closest_period:.2f}')
        
        # Set y-ticks to show actual periods
        ax2.set_yticks(np.log2(yticks))
        ax2.set_yticklabels([f"{p:.1f}" for p in yticks])
        
        ax2.set_title('Global Wavelet Spectrum')
        ax2.set_xlabel('Power')
        ax2.set_ylabel('Period')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Add Ki-related information to plot
        ki_sig = result.metrics.get('wavelet_ki_significance', 0)
        ki_error = result.metrics.get('wavelet_relative_error', 0)
        ki_type = result.metadata.get('ki_match_type', 'unknown')
        ax2.text(0.02, 0.05, f'Ki Type: {ki_type}\nSignificance: {ki_sig:.2f}\nError: {ki_error:.2f}',
                transform=ax2.transAxes, verticalalignment='bottom',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        # Save the figure
        output_file = output_dir / f"{result.trace_id}_wavelet_scalogram.png"
        plt.savefig(output_file, dpi=300)
        plt.close(fig)