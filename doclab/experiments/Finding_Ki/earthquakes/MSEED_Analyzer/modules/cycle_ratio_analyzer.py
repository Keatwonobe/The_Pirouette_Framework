import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from pathlib import Path
from base_analysis_module import BaseAnalysisModule
from analysis_result import AnalysisResult

class CycleRatioAnalyzer(BaseAnalysisModule):
    """
    Analyzes time series data for cycle ratios related to the Ki constant.
    
    This module identifies periodic components in the signal and compares their
    ratios to the Ki constant (both rest and motion values) to detect
    resonance patterns.
    """
    
    def __init__(self, analyzer):
        super().__init__(analyzer)
        self.ki_value = analyzer.ki_value
        self.alternate_ki = analyzer.alternate_ki
        self.pi = 3.14159
        self.significance_threshold = analyzer.significance_threshold
    
    def analyze(self, trace, processed_trace=None, **kwargs):
        """
        Analyze the trace for cycle ratio patterns related to Ki
        
        Parameters:
        -----------
        trace : obspy.Trace
            Original trace
        processed_trace : obspy.Trace
            Preprocessed trace (detrended, filtered)
            
        Returns:
        --------
        list of AnalysisResult
            Results of the analysis
        """
        # Use processed trace if available, otherwise use original
        data = processed_trace.data if processed_trace else trace.data
        sampling_rate = trace.stats.sampling_rate
        
        # Check if we have enough data
        if len(data) < 3 * sampling_rate:  # At least 3 seconds of data
            return []
        
        # Calculate the power spectrum
        f, pxx = signal.periodogram(data, fs=sampling_rate)
        
        # Normalize the power spectrum
        pxx_norm = pxx / np.sum(pxx)
        
        # Find peaks in the power spectrum
        peaks, properties = signal.find_peaks(
            pxx_norm, 
            height=np.mean(pxx_norm) + 0.5 * np.std(pxx_norm),
            distance=3  # Minimum distance between peaks
        )
        
        if len(peaks) < 2:
            return []  # Not enough peaks for analysis
        
        # Extract peak frequencies and their power
        peak_freqs = f[peaks]
        peak_powers = pxx_norm[peaks]
        
        # Sort peaks by power (descending)
        sorted_indices = np.argsort(-peak_powers)
        sorted_peak_freqs = peak_freqs[sorted_indices]
        sorted_peak_powers = peak_powers[sorted_indices]
        
        # Consider only the top N peaks to reduce noise influence
        top_n = min(10, len(sorted_peak_freqs))
        top_freqs = sorted_peak_freqs[:top_n]
        top_powers = sorted_peak_powers[:top_n]
        
        # Calculate ratios between all pairs of top frequencies
        ratios = []
        ratio_pairs = []
        
        for i in range(top_n):
            for j in range(i+1, top_n):
                # Calculate both possible ratios (higher/lower and lower/higher)
                if top_freqs[i] > top_freqs[j]:
                    ratio = top_freqs[i] / top_freqs[j]
                    ratio_pairs.append((top_freqs[i], top_freqs[j]))
                else:
                    ratio = top_freqs[j] / top_freqs[i]
                    ratio_pairs.append((top_freqs[j], top_freqs[i]))
                ratios.append(ratio)
        
        # If no ratios were calculated, return empty result
        if not ratios:
            return []
        
        # Calculate the closeness of each ratio to Ki values
        ki_rest_diff = [abs(ratio - self.analyzer.alternate_ki) / self.analyzer.alternate_ki for ratio in ratios]
        ki_motion_diff = [abs(ratio - self.analyzer.ki_value) / self.analyzer.ki_value for ratio in ratios]
        pi_diff = [abs(ratio - self.pi) / self.pi for ratio in ratios]
        
        # Find the closest ratio to each constant
        closest_ki_rest_idx = np.argmin(ki_rest_diff)
        closest_ki_motion_idx = np.argmin(ki_motion_diff)
        closest_pi_idx = np.argmin(pi_diff)
        
        # Calculate significance based on the closeness of the match
        # (lower difference = higher significance)
        ki_rest_significance = 5.0 * (1.0 - ki_rest_diff[closest_ki_rest_idx])
        ki_motion_significance = 5.0 * (1.0 - ki_motion_diff[closest_ki_motion_idx])
        pi_significance = 5.0 * (1.0 - pi_diff[closest_pi_idx])
        
        # Create a result if we have significant findings
        results = []
        
        # Check if any significance exceeds threshold
        if (ki_rest_significance > self.significance_threshold or 
            ki_motion_significance > self.significance_threshold or
            pi_significance > self.significance_threshold):
            
            result = AnalysisResult(
                trace_id=trace.id,
                start_time=trace.stats.starttime,
                end_time=trace.stats.endtime
            )
            
            # Add metrics to the result
            result.add_metric("ki_rest_ratio", ratios[closest_ki_rest_idx])
            result.add_metric("ki_rest_expected", self.analyzer.alternate_ki)
            result.add_metric("ki_rest_difference", ki_rest_diff[closest_ki_rest_idx])
            result.add_metric("ki_rest_significance", ki_rest_significance)
            
            result.add_metric("ki_motion_ratio", ratios[closest_ki_motion_idx])
            result.add_metric("ki_motion_expected", self.analyzer.ki_value)
            result.add_metric("ki_motion_difference", ki_motion_diff[closest_ki_motion_idx])
            result.add_metric("ki_motion_significance", ki_motion_significance)
            
            result.add_metric("pi_ratio", ratios[closest_pi_idx])
            result.add_metric("pi_expected", self.pi)
            result.add_metric("pi_difference", pi_diff[closest_pi_idx])
            result.add_metric("pi_significance", pi_significance)
            
            # Add pattern data
            result.add_pattern("peak_frequencies", top_freqs.tolist())
            result.add_pattern("peak_powers", top_powers.tolist())
            result.add_pattern("frequency_ratios", ratios)
            result.add_pattern("ratio_pairs", ratio_pairs)
            
            # Add plot data
            result.add_plot_data("frequencies", f.tolist())
            result.add_plot_data("power_spectrum", pxx_norm.tolist())
            result.add_plot_data("peak_indices", peaks.tolist())
            
            results.append(result)
        
        return results
    
    def generate_plots(self, result, base_output_dir):
        """
        Generate plots for the analysis result
        
        Parameters:
        -----------
        result : AnalysisResult
            The analysis result to plot
        base_output_dir : Path
            Base directory for saving plots
        """
        base_output_dir = Path(base_output_dir)
        base_output_dir.mkdir(exist_ok=True, parents=True)
        
        # Create frequency spectrum plot
        self._plot_frequency_spectrum(result, base_output_dir)
        
        # Create ratio comparison plot
        self._plot_ratio_comparison(result, base_output_dir)
    
    def _plot_frequency_spectrum(self, result, output_dir):
        """Generate frequency spectrum plot with peak highlighting"""
        frequencies = result.plots["frequencies"]
        power_spectrum = result.plots["power_spectrum"]
        peak_indices = result.plots["peak_indices"]
        peak_frequencies = result.patterns["peak_frequencies"]
        peak_powers = result.patterns["peak_powers"]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot power spectrum
        ax.plot(frequencies, power_spectrum, 'b-', alpha=0.7)
        
        # Highlight peaks
        ax.plot(peak_frequencies, peak_powers, 'ro', markersize=6, label='Peaks')
        
        # Annotations for the most significant peaks
        top_n = min(5, len(peak_frequencies))
        for i in range(top_n):
            ax.annotate(
                f"{peak_frequencies[i]:.2f} Hz",
                xy=(peak_frequencies[i], peak_powers[i]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8
            )
        
        # Set labels and title
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Normalized Power')
        ax.set_title(f'Frequency Spectrum - {result.trace_id}')
        
        # Use log scale for better visibility
        ax.set_yscale('log')
        
        # Add grid and legend
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Save plot
        plot_path = output_dir / f"frequency_spectrum.png"
        plt.savefig(plot_path, dpi=300)
        plt.close(fig)
    
    def _plot_ratio_comparison(self, result, output_dir):
        """Generate plot comparing observed ratios to Ki constants"""
        ratios = result.patterns["frequency_ratios"]
        ratio_pairs = result.patterns["ratio_pairs"]
        
        # Calculate differences from constants
        ki_rest_diffs = [abs(ratio - self.analyzer.alternate_ki) / self.analyzer.alternate_ki for ratio in ratios]
        ki_motion_diffs = [abs(ratio - self.analyzer.ki_value) / self.analyzer.ki_value for ratio in ratios]
        pi_diffs = [abs(ratio - self.pi) / self.pi for ratio in ratios]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data for plotting
        x = np.arange(len(ratios))
        width = 0.25
        
        # Plot bars for each constant
        rects1 = ax.bar(x - width, ki_rest_diffs, width, label=f'Ki Rest ({self.analyzer.alternate_ki:.5f})')
        rects2 = ax.bar(x, ki_motion_diffs, width, label=f'Ki Motion ({self.analyzer.ki_value:.5f})')
        rects3 = ax.bar(x + width, pi_diffs, width, label=f'Pi ({self.pi:.5f})')
        
        # Add ratio values above bars
        for i, ratio in enumerate(ratios):
            ax.annotate(
                f"{ratio:.3f}",
                xy=(i, 0.01),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8
            )
            
            # Display the frequency pair
            pair = ratio_pairs[i]
            ax.annotate(
                f"{pair[0]:.2f}/{pair[1]:.2f} Hz",
                xy=(i, 0.005),
                xytext=(0, -15),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=7,
                rotation=45
            )
        
        # Add threshold line
        inverse_threshold = 1 - (self.significance_threshold / 5.0)
        ax.axhline(y=inverse_threshold, color='r', linestyle='--', alpha=0.7, 
                   label=f'Significance Threshold ({self.significance_threshold})')
        
        # Set labels and title
        ax.set_xlabel('Frequency Ratio Index')
        ax.set_ylabel('Relative Difference from Constants')
        ax.set_title(f'Frequency Ratio Analysis - {result.trace_id}')
        
        # Set y-axis limits
        ax.set_ylim(0, min(1.0, max(max(ki_rest_diffs), max(ki_motion_diffs), max(pi_diffs)) * 1.2))
        
        # X-axis ticks
        ax.set_xticks(x)
        ax.set_xticklabels([f"{i+1}" for i in range(len(ratios))])
        
        # Add grid and legend
        ax.grid(True, axis='y', alpha=0.3)
        ax.legend()
        
        # Tight layout
        plt.tight_layout()
        
        # Save plot
        plot_path = output_dir / f"ratio_comparison.png"
        plt.savefig(plot_path, dpi=300)
        plt.close(fig)