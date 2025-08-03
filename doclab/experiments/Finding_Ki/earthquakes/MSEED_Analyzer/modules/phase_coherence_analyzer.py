from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class PhaseCoherenceAnalyzer:
    """
    Analyzes phase coherence in signals to detect Ki-related relationships
    """
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.ki_value = analyzer.ki_value
        self.alternate_ki = analyzer.alternate_ki
    
    def analyze(self, trace, processed_trace=None, **kwargs):
        """
        Analyze phase coherence in the signal
        
        Parameters:
        -----------
        trace : obspy.Trace
            Original trace
        processed_trace : obspy.Trace or None
            Preprocessed trace if available
        
        Returns:
        --------
        list of AnalysisResult objects
        """
        # Use processed trace if available
        data = processed_trace.data if processed_trace else trace.data
        sampling_rate = trace.stats.sampling_rate
        
        # Need enough data points for analysis
        if len(data) < 1024:
            return []
        
        # Compute the analytic signal (using Hilbert transform)
        analytic_signal = signal.hilbert(data)
        
        # Instantaneous phase
        instantaneous_phase = np.unwrap(np.angle(analytic_signal))
        
        # Phase derivative (instantaneous frequency)
        phase_derivative = np.diff(instantaneous_phase) * sampling_rate / (2.0 * np.pi)
        
        # Look for phase coherence at Ki-related values
        ki_phase_coherence = self._measure_phase_coherence(phase_derivative, self.ki_value)
        alt_ki_phase_coherence = self._measure_phase_coherence(phase_derivative, self.alternate_ki)
        pi_phase_coherence = self._measure_phase_coherence(phase_derivative, np.pi)
        
        # Compute significance
        mean_coherence = np.mean([self._measure_phase_coherence(phase_derivative, random_val) 
                                 for random_val in np.random.uniform(1, 6, 10)])
        std_coherence = np.std([self._measure_phase_coherence(phase_derivative, random_val) 
                               for random_val in np.random.uniform(1, 6, 10)])
        
        ki_significance = (ki_phase_coherence - mean_coherence) / std_coherence if std_coherence > 0 else 0
        alt_ki_significance = (alt_ki_phase_coherence - mean_coherence) / std_coherence if std_coherence > 0 else 0
        
        # Only return results if we have significant coherence
        if (ki_significance > self.analyzer.significance_threshold or 
            alt_ki_significance > self.analyzer.significance_threshold):
            
            # Create result
            result = self.analyzer.AnalysisResult(
                trace_id=trace.id,
                start_time=trace.stats.starttime,
                end_time=trace.stats.endtime
            )
            
            # Add metrics
            result.add_metric('ki_phase_coherence', ki_phase_coherence)
            result.add_metric('alt_ki_phase_coherence', alt_ki_phase_coherence)
            result.add_metric('pi_phase_coherence', pi_phase_coherence)
            result.add_metric('ki_significance', ki_significance)
            result.add_metric('alt_ki_significance', alt_ki_significance)
            
            # Add patterns
            result.add_pattern('instantaneous_phase', instantaneous_phase)
            result.add_pattern('phase_derivative', phase_derivative)
            
            # Add plot data for visualization
            result.add_plot_data('phases', {
                'time': np.arange(len(instantaneous_phase)) / sampling_rate,
                'phase': instantaneous_phase,
                'derivative': np.pad(phase_derivative, (0, 1), 'edge')
            })
            
            return [result]
        
        return []
    
    def _measure_phase_coherence(self, phase_derivative, target_value):
        """
        Measure how coherently the phase derivative aligns with a target value
        
        Parameters:
        -----------
        phase_derivative : numpy.ndarray
            The phase derivative (instantaneous frequency)
        target_value : float
            The target value to check for coherence
            
        Returns:
        --------
        float
            Coherence measure [0-1]
        """
        # Discard extreme outliers
        valid_indices = np.abs(phase_derivative) < 100
        
        if np.sum(valid_indices) < 10:
            return 0.0
            
        valid_derivative = phase_derivative[valid_indices]
        
        # Calculate residuals from target
        residuals = valid_derivative - target_value
        
        # Normalize by data range to get comparable scores
        data_range = np.max(valid_derivative) - np.min(valid_derivative)
        if data_range < 1e-10:
            return 0.0
            
        normalized_residuals = residuals / data_range
        
        # Calculate coherence as inverse of normalized residual variance
        variance = np.var(normalized_residuals)
        
        # Avoid division by zero
        if variance < 1e-10:
            return 0.0
            
        coherence = 1.0 / (1.0 + variance * 10)  # Scale factor for reasonable range
        
        return coherence
    
    def generate_plots(self, result, output_prefix):
        """
        Generate plots for the analysis result
        
        Parameters:
        -----------
        result : AnalysisResult
            The analysis result
        output_prefix : str or Path
            Prefix for output files
        
        Returns:
        --------
        list of Path
            Paths to the generated plot files
        """
        output_paths = []
        
        # Ensure output directory exists
        output_prefix = Path(output_prefix)
        output_prefix.parent.mkdir(parents=True, exist_ok=True)
        
        # Get phases data
        if 'phases' in result.plots:
            phases_data = result.plots['phases']
            time = phases_data['time']
            phase = phases_data['phase']
            derivative = phases_data['derivative']
            # Plot phase and derivative
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
            
            # Phase plot
            ax1.plot(time, phase, 'b-', label='Instantaneous Phase')
            ax1.set_ylabel('Phase (rad)')
            ax1.set_title(f'Phase Coherence Analysis - {result.trace_id}')
            ax1.grid(True, linestyle='--', alpha=0.3)
            ax1.legend(loc='upper right')
            
            # Add reference lines for Ki and Pi
            max_phase = np.max(phase)
            min_phase = np.min(phase)
            phase_range = max_phase - min_phase
            
            # Draw Ki and Pi reference lines
            for i in range(int(min_phase / self.ki_value), int(max_phase / self.ki_value) + 1):
                ki_phase = i * self.ki_value
                ax1.axhline(y=ki_phase, color='r', linestyle='--', alpha=0.3)
                ax1.text(time[-1] * 0.95, ki_phase, f'{i}×Ki', 
                        color='red', fontsize=8, ha='right', va='bottom')
            
            for i in range(int(min_phase / np.pi), int(max_phase / np.pi) + 1):
                pi_phase = i * np.pi
                ax1.axhline(y=pi_phase, color='g', linestyle=':', alpha=0.3)
                ax1.text(time[-1] * 0.95, pi_phase, f'{i}×π', 
                        color='green', fontsize=8, ha='right', va='top')
            
            # Derivative plot
            ax2.plot(time, derivative, 'r-', label='Phase Derivative')
            ax2.set_xlabel('Time (s)')
            ax2.set_ylabel('Phase Derivative (rad/s)')
            ax2.grid(True, linestyle='--', alpha=0.3)
            ax2.legend(loc='upper right')
            
            # Add horizontal lines at Ki and Pi
            ax2.axhline(y=self.ki_value, color='r', linestyle='--', 
                      label=f'Ki = {self.ki_value:.5f}', alpha=0.7)
            ax2.axhline(y=self.alternate_ki, color='m', linestyle='--', 
                      label=f'Alt Ki = {self.alternate_ki:.5f}', alpha=0.7)
            ax2.axhline(y=np.pi, color='g', linestyle=':', 
                      label=f'π = {np.pi:.5f}', alpha=0.7)
            
            # Add coherence values to legend
            ki_coherence = result.metrics.get('ki_phase_coherence', 0)
            alt_ki_coherence = result.metrics.get('alt_ki_phase_coherence', 0)
            pi_coherence = result.metrics.get('pi_phase_coherence', 0)
            
            ki_sig = result.metrics.get('ki_significance', 0)
            alt_ki_sig = result.metrics.get('alt_ki_significance', 0)
            
            # Add to legend
            handles, labels = ax2.get_legend_handles_labels()
            handles.append(plt.Line2D([0], [0], color='none'))
            labels.append(f'Ki Coherence: {ki_coherence:.3f} (sig: {ki_sig:.2f})')
            
            handles.append(plt.Line2D([0], [0], color='none'))
            labels.append(f'Alt Ki Coherence: {alt_ki_coherence:.3f} (sig: {alt_ki_sig:.2f})')
            
            handles.append(plt.Line2D([0], [0], color='none'))
            labels.append(f'π Coherence: {pi_coherence:.3f}')
            
            ax2.legend(handles, labels, loc='upper right')
            
            # Tight layout
            plt.tight_layout()
            
            # Save the figure
            output_path = output_prefix.with_name(f"{output_prefix.name}_phase_coherence.png")
            plt.savefig(output_path, dpi=300)
            plt.close(fig)
            
            output_paths.append(output_path)
        
        # Create power spectrum plot if patterns are available
        if 'phase_derivative' in result.patterns:
            derivative = result.patterns['phase_derivative']
            
            # Compute power spectrum
            f, pxx = signal.welch(derivative, fs=1.0, nperseg=min(len(derivative)//4, 1024))
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot power spectrum
            ax.semilogy(f, pxx, 'b-', alpha=0.7)
            
            # Add vertical lines at key frequencies
            ax.axvline(x=1.0/self.ki_value, color='r', linestyle='--', 
                     label=f'1/Ki = {1.0/self.ki_value:.5f}', alpha=0.7)
            ax.axvline(x=1.0/self.alternate_ki, color='m', linestyle='--', 
                     label=f'1/Alt Ki = {1.0/self.alternate_ki:.5f}', alpha=0.7)
            ax.axvline(x=1.0/np.pi, color='g', linestyle=':', 
                     label=f'1/π = {1.0/np.pi:.5f}', alpha=0.7)
            
            # Add labels
            ax.set_xlabel('Frequency (cycles/sample)')
            ax.set_ylabel('Power Spectrum')
            ax.set_title(f'Phase Derivative Power Spectrum - {result.trace_id}')
            
            # Add grid
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Add legend
            ax.legend(loc='upper right')
            
            # Tight layout
            plt.tight_layout()
            
            # Save the figure
            output_path = output_prefix.with_name(f"{output_prefix.name}_phase_spectrum.png")
            plt.savefig(output_path, dpi=300)
            plt.close(fig)
            
            output_paths.append(output_path)
        
        return output_paths