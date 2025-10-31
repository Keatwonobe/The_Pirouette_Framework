import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import zscore



class HarmonicPatternAnalyzer:
    """
    Analyzes time series data for harmonic patterns that may be related to the Ki constant.
    Identifies resonance structures that follow harmonic series based on ratios related to Ki.
    """
    
    def __init__(self, analyzer):
        """
        Initialize the harmonic pattern analyzer
        
        Parameters:
        -----------
        analyzer : KiResonanceAnalyzer
            The main analyzer instance
        """
        self.analyzer = analyzer
        self.ki_value = analyzer.ki_value
        self.alternate_ki = analyzer.alternate_ki
        self.significance_threshold = analyzer.significance_threshold
        self.pi = 3.14159
        
        # Define the key ratios to look for
        self.key_ratios = {
            'ki_fundamental': 1.0,
            'ki_half': 0.5,
            'ki_double': 2.0,
            'ki_pi_ratio': self.ki_value / self.pi,
            'ki_third': 1/3,
            'ki_two_thirds': 2/3,
            'ki_three_halves': 1.5,
            'golden_ki': 1.61803 * self.ki_value / self.pi
        }

    def analyze(self, trace, processed_trace=None, **kwargs):
        """
        Analyze a trace for harmonic patterns related to Ki
        
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
        # Use processed trace if available
        data = processed_trace.data if processed_trace else trace.data
        sampling_rate = trace.stats.sampling_rate
        
        # Ensure we have enough data points
        if len(data) < 512:
            return []
        
        # Calculate power spectrum
        freqs, power = self._compute_power_spectrum(data, sampling_rate)
        
        # Identify potential harmonic patterns
        harmonic_patterns = self._identify_harmonic_patterns(freqs, power, sampling_rate)
        
        # Return empty list if no significant patterns found
        if not harmonic_patterns['patterns']:
            return []
        
        # Create result object
        result = self.analyzer.AnalysisResult(
            trace_id=trace.id,
            start_time=trace.stats.starttime,
            end_time=trace.stats.endtime
        )
        
        # Add metrics
        result.add_metric('harmonic_pattern_count', len(harmonic_patterns['patterns']))
        result.add_metric('harmonic_pattern_significance', harmonic_patterns['max_significance'])
        result.add_metric('harmonic_pattern_ki_ratio', harmonic_patterns['best_ki_ratio'])
        result.add_metric('harmonic_coherence', harmonic_patterns['coherence'])
        
        # Add patterns
        result.add_pattern('harmonic_patterns', harmonic_patterns['patterns'])
        
        # Add plot data
        result.add_plot_data('frequencies', freqs)
        result.add_plot_data('power', power)
        result.add_plot_data('harmonic_peaks', harmonic_patterns['peak_freqs'])
        result.add_plot_data('harmonic_powers', harmonic_patterns['peak_powers'])
        
        # Return as list since we only produce one result per trace
        return [result]
    
    def _compute_power_spectrum(self, data, sampling_rate):
        """
        Compute the power spectrum of the data using Welch's method
        
        Parameters:
        -----------
        data : numpy.ndarray
            The time series data
        sampling_rate : float
            The sampling rate in Hz
            
        Returns:
        --------
        numpy.ndarray, numpy.ndarray
            Frequencies and corresponding power values
        """
        # Apply Hann window to reduce spectral leakage
        window = signal.windows.hann(len(data))
        data_windowed = data * window
        
        # Compute power spectral density using Welch's method
        nperseg = min(8192, len(data))
        freqs, power = signal.welch(
            data_windowed, 
            fs=sampling_rate, 
            nperseg=nperseg,
            scaling='spectrum'
        )
        
        # Normalize power
        power = power / np.max(power)
        
        return freqs, power
    
    def _identify_harmonic_patterns(self, freqs, power, sampling_rate):
        """
        Identify harmonic patterns in the power spectrum
        
        Parameters:
        -----------
        freqs : numpy.ndarray
            Frequency values
        power : numpy.ndarray
            Power spectrum values
        sampling_rate : float
            The sampling rate in Hz
            
        Returns:
        --------
        dict
            Dictionary containing identified harmonic patterns and metrics
        """
        # Find peaks in the power spectrum
        peak_indices, _ = signal.find_peaks(power, height=np.mean(power) + 0.5 * np.std(power))
        
        # Filter out insignificant peaks
        significant_peaks = []
        for idx in peak_indices:
            # Check if peak is significant compared to local background
            local_start = max(0, idx - 20)
            local_end = min(len(power), idx + 20)
            local_background = np.concatenate([power[local_start:idx], power[idx+1:local_end]])
            
            if power[idx] > np.mean(local_background) + 2 * np.std(local_background):
                significant_peaks.append(idx)
        
        peak_indices = np.array(significant_peaks)
        
        # If no significant peaks found, return empty result
        if len(peak_indices) < 3:  # Need at least 3 peaks to form a harmonic pattern
            return {
                'patterns': [],
                'max_significance': 0,
                'best_ki_ratio': 0,
                'coherence': 0,
                'peak_freqs': [],
                'peak_powers': []
            }
        
        peak_freqs = freqs[peak_indices]
        peak_powers = power[peak_indices]
        
        # Sort peaks by power
        sorted_indices = np.argsort(peak_powers)[::-1]
        peak_freqs = peak_freqs[sorted_indices]
        peak_powers = peak_powers[sorted_indices]
        
        # Look for harmonic patterns related to Ki
        patterns = []
        max_significance = 0
        best_ki_ratio = 0
        
        # Compute expected frequencies based on Ki
        ki_fundamental_freq = sampling_rate / self.ki_value
        expected_freqs = {}
        
        for ratio_name, ratio in self.key_ratios.items():
            expected_freqs[ratio_name] = ki_fundamental_freq * ratio
        
        # For each of the top peaks, check if it could be a fundamental frequency
        for i, fundamental in enumerate(peak_freqs[:min(10, len(peak_freqs))]):
            # Only consider peaks with reasonable power
            if peak_powers[i] < 0.2 * np.max(peak_powers):
                continue
                
            # Check for harmonics
            harmonic_indices = []
            harmonic_ratios = []
            
            for j, freq in enumerate(peak_freqs):
                # Skip the peak itself
                if j == i:
                    continue
                
                # Calculate ratio to potential fundamental
                ratio = freq / fundamental
                
                # Check if the ratio is close to any of our key ratios
                for ratio_name, expected_ratio in self.key_ratios.items():
                    if abs(ratio - expected_ratio) < 0.05:  # 5% tolerance
                        harmonic_indices.append(j)
                        harmonic_ratios.append((ratio_name, expected_ratio, ratio))
                        break
            
            # If we have enough harmonics, consider it a pattern
            if len(harmonic_indices) >= 2:
                # Calculate significance based on number of harmonics and power
                significance = (len(harmonic_indices) * np.mean(peak_powers[harmonic_indices]) / 
                               np.mean(power))
                
                # Calculate coherence (how well ratios match expected values)
                ratio_errors = [abs(actual - expected)/expected 
                               for _, expected, actual in harmonic_ratios]
                coherence = 1 - np.mean(ratio_errors)
                
                # Check which Ki-related ratio this might be
                best_match = None
                best_error = float('inf')
                
                for ratio_name, expected_freq in expected_freqs.items():
                    error = abs(fundamental - expected_freq) / expected_freq
                    if error < best_error and error < 0.1:  # 10% tolerance
                        best_error = error
                        best_match = ratio_name
                
                # Store the pattern
                pattern = {
                    'fundamental_freq': fundamental,
                    'fundamental_power': peak_powers[i],
                    'harmonic_freqs': peak_freqs[harmonic_indices].tolist(),
                    'harmonic_powers': peak_powers[harmonic_indices].tolist(),
                    'harmonic_ratios': harmonic_ratios,
                    'significance': significance,
                    'coherence': coherence,
                    'ki_relation': best_match,
                    'ki_relation_error': best_error
                }
                
                patterns.append(pattern)
                
                # Update max significance
                if significance > max_significance:
                    max_significance = significance
                    best_ki_ratio = 1.0 if best_match is None else self.key_ratios.get(best_match, 1.0)
        
        # Calculate overall coherence of all patterns
        if patterns:
            overall_coherence = np.mean([p['coherence'] for p in patterns])
        else:
            overall_coherence = 0
        
        return {
            'patterns': patterns,
            'max_significance': max_significance,
            'best_ki_ratio': best_ki_ratio,
            'coherence': overall_coherence,
            'peak_freqs': peak_freqs.tolist(),
            'peak_powers': peak_powers.tolist()
        }
    
    def generate_plots(self, result, output_dir):
        """
        Generate plots for the harmonic pattern analysis
        
        Parameters:
        -----------
        result : AnalysisResult
            The analysis result with plot data
        output_dir : Path
            Directory to save the plots
            
        Returns:
        --------
        list
            List of generated plot file paths
        """
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Extract data from result
        freqs = result.plots['frequencies']
        power = result.plots['power']
        peak_freqs = result.plots['harmonic_peaks']
        peak_powers = result.plots['harmonic_powers']
        patterns = result.patterns['harmonic_patterns']
        
        # Generate spectrum plot
        spectrum_plot_path = output_dir / f"{result.trace_id}_harmonic_spectrum.png"
        self._plot_harmonic_spectrum(freqs, power, peak_freqs, peak_powers, 
                                    patterns, result.trace_id, spectrum_plot_path)
        
        # Generate ratio plot for the most significant pattern (if any)
        ratio_plot_paths = []
        if patterns:
            # Sort by significance
            sorted_patterns = sorted(patterns, key=lambda p: p['significance'], reverse=True)
            top_pattern = sorted_patterns[0]
            
            ratio_plot_path = output_dir / f"{result.trace_id}_harmonic_ratios.png"
            self._plot_harmonic_ratios(top_pattern, result.trace_id, ratio_plot_path)
            ratio_plot_paths.append(ratio_plot_path)
        
        return [spectrum_plot_path] + ratio_plot_paths
    
    def _plot_harmonic_spectrum(self, freqs, power, peak_freqs, peak_powers, 
                              patterns, trace_id, output_path):
        """
        Plot the power spectrum with identified harmonic patterns
        
        Parameters:
        -----------
        freqs : list
            Frequency values
        power : list
            Power spectrum values
        peak_freqs : list
            Frequencies of identified peaks
        peak_powers : list
            Power values of identified peaks
        patterns : list
            List of identified harmonic patterns
        trace_id : str
            Trace identifier
        output_path : Path
            Output file path
            
        Returns:
        --------
        None
        """
        # Create plot
        plt.figure(figsize=(12, 8))
        
        # Plot power spectrum
        plt.plot(freqs, power, 'b-', alpha=0.6, label='Power Spectrum')
        
        # Plot all peaks
        plt.plot(peak_freqs, peak_powers, 'ro', markersize=4, alpha=0.5, label='Detected Peaks')
        
        # Plot patterns
        colors = plt.cm.tab10.colors
        for i, pattern in enumerate(patterns[:5]):  # Limit to top 5 patterns
            # Get pattern data
            fund_freq = pattern['fundamental_freq']
            fund_power = pattern['fundamental_power']
            harm_freqs = pattern['harmonic_freqs']
            harm_powers = pattern['harmonic_powers']
            
            # Plot fundamental
            plt.plot(fund_freq, fund_power, 'o', color=colors[i % len(colors)], 
                     markersize=8, alpha=0.8,
                     label=f"Pattern {i+1} (Significance: {pattern['significance']:.2f})")
            
            # Plot harmonics
            plt.plot(harm_freqs, harm_powers, 's', color=colors[i % len(colors)], 
                     markersize=6, alpha=0.8)
            
            # Connect with lines
            all_freqs = np.append(fund_freq, harm_freqs)
            all_powers = np.append(fund_power, harm_powers)
            sort_idx = np.argsort(all_freqs)
            plt.plot(all_freqs[sort_idx], all_powers[sort_idx], '--', 
                     color=colors[i % len(colors)], alpha=0.5)
        
        # Annotate with Ki-related frequencies
        sampling_rate = freqs[-1] * 2  # Rough estimate of sampling rate
        ki_freq = sampling_rate / self.ki_value
        alt_ki_freq = sampling_rate / self.alternate_ki
        pi_freq = sampling_rate / self.pi
        
        if ki_freq < freqs[-1]:
            plt.axvline(ki_freq, color='g', linestyle='--', alpha=0.5, 
                        label=f'Ki Frequency ({ki_freq:.2f} Hz)')
        
        if alt_ki_freq < freqs[-1]:
            plt.axvline(alt_ki_freq, color='m', linestyle='--', alpha=0.5,
                       label=f'Alt Ki Frequency ({alt_ki_freq:.2f} Hz)')
        
        if pi_freq < freqs[-1]:
            plt.axvline(pi_freq, color='k', linestyle='--', alpha=0.5,
                       label=f'Pi Frequency ({pi_freq:.2f} Hz)')
        
        # Set layout
        plt.title(f'Harmonic Patterns - {trace_id}')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Normalized Power')
        plt.yscale('log')
        plt.grid(True, alpha=0.3)
        plt.legend(loc='upper right', fontsize=8)
        plt.tight_layout()
        
        # Save
        plt.savefig(output_path, dpi=300)
        plt.close()
    
    def _plot_harmonic_ratios(self, pattern, trace_id, output_path):
        """
        Plot the harmonic ratios for a specific pattern
        
        Parameters:
        -----------
        pattern : dict
            The harmonic pattern data
        trace_id : str
            Trace identifier
        output_path : Path
            Output file path
            
        Returns:
        --------
        None
        """
        # Extract ratios
        ratio_names = []
        expected_ratios = []
        actual_ratios = []
        
        fundamental = pattern['fundamental_freq']
        
        # Add fundamental (ratio 1.0)
        ratio_names.append('fundamental')
        expected_ratios.append(1.0)
        actual_ratios.append(1.0)
        
        # Add harmonics
        for ratio_name, expected, actual in pattern['harmonic_ratios']:
            ratio_names.append(ratio_name)
            expected_ratios.append(expected)
            actual_ratios.append(actual)
        
        # Create plot
        plt.figure(figsize=(10, 6))
        
        # Plot expected vs actual ratios
        x = np.arange(len(ratio_names))
        width = 0.35
        
        plt.bar(x - width/2, expected_ratios, width, label='Expected Ratio', alpha=0.7)
        plt.bar(x + width/2, actual_ratios, width, label='Actual Ratio', alpha=0.7)
        
        # Add labels
        plt.xlabel('Ratio Type')
        plt.ylabel('Ratio to Fundamental')
        plt.title(f'Harmonic Ratios - {trace_id}\nFundamental: {fundamental:.2f} Hz')
        plt.xticks(x, ratio_names, rotation=45, ha='right')
        plt.legend()
        
        # Add relationship to Ki
        ki_relation = pattern.get('ki_relation')
        if ki_relation:
            ki_error = pattern.get('ki_relation_error', 0)
            plt.figtext(0.5, 0.01, 
                      f"Ki Relation: {ki_relation} (Error: {ki_error:.2%})",
                      ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        
        # Save
        plt.savefig(output_path, dpi=300)
        plt.close()


# Function to register this module with the KiResonanceAnalyzer
def register_module(analyzer):
    """
    Register this module with the KiResonanceAnalyzer
    
    Parameters:
    -----------
    analyzer : KiResonanceAnalyzer
        The analyzer instance
    """
    analyzer.register_module("harmonic_pattern", HarmonicPatternAnalyzer)