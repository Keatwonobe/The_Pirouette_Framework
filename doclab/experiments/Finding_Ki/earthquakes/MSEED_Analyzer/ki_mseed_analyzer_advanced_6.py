import os
import sys
import json
import platform
import warnings
import traceback
import importlib.util
from pathlib import Path
from datetime import datetime
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from obspy import read
from scipy import signal
from scipy.stats import kurtosis, skew
import tqdm

# GUI Imports
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# --- Constants ---
KI_REST = 4.14159      # Ki in rest state
KI_MOTION = 4.18879    # Ki in motion (approximately 4π/3)
PI = np.pi             # Pi constant
GOLDEN_RATIO = 1.61803 # Golden ratio

# --- Core Classes (Self-Contained) ---

class AnalysisResult:
    """Container for analysis results."""
    def __init__(self, trace_id=None, start_time=None, end_time=None):
        self.trace_id = trace_id
        self.start_time = start_time
        self.end_time = end_time
        self.metrics = {}
        self.patterns = {}
        self.plots = {}
        self.metadata = {}

    def add_metric(self, name, value):
        """Add a numeric metric to the result."""
        self.metrics[name] = value
        return self

    def add_pattern(self, name, data):
        """Add a detected pattern to the result."""
        self.patterns[name] = data
        return self

    def add_plot_data(self, name, data):
        """Add plot data to the result."""
        self.plots[name] = data
        return self

    def add_metadata(self, name, value):
        """Add metadata to the result."""
        self.metadata[name] = value
        return self

    def to_dict(self):
        """Convert to dictionary for storage/reporting."""
        result = {
            'trace_id': self.trace_id,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'metrics': self.metrics,
            'metadata': self.metadata,
        }
        serializable_patterns = {}
        for name, pattern in self.patterns.items():
            try:
                json.dumps(pattern)
                serializable_patterns[name] = pattern
            except (TypeError, OverflowError):
                if hasattr(pattern, '__len__'):
                    # Convert non-serializable pattern data to a string representation
                    serializable_patterns[name] = f"<{type(pattern).__name__} with {len(pattern)} items>"
                else:
                    serializable_patterns[name] = f"<{type(pattern).__name__}>"
        result['patterns'] = serializable_patterns
        return result

class KiStateTracker():
    """
    Slides a window, estimates Ki(t) from the dominant phase-ratio,
    then classifies each slice as REST, MOTION, or TRANSITION.
    """
    def analyze(self, trace, processed_trace=None, **kw):
        # Use processed_trace if available, otherwise fall back to original trace
        data_to_analyze = processed_trace.data if processed_trace is not None else trace.data

        win_s, step_s = 4.0, 0.5          # tweakable: window size and step in seconds
        sr = trace.stats.sampling_rate
        nwin = int((len(data_to_analyze) / sr - win_s) / step_s)
        ki_series = []

        # print(f"Analyzing trace {trace.id} for Ki states...") # Suppress for cleaner output
        for k in range(nwin):
            s_idx = int(k * step_s * sr)
            e_idx = s_idx + int(win_s * sr)
            seg = data_to_analyze[s_idx:e_idx]

            if seg.std() < 1e-9: # Skip windows with no variance (flat line)
                continue

            try:
                # Use Welch's method for Power Spectral Density (PSD)
                # nperseg should be chosen carefully; 2048 samples at 100 Hz = 20.48 seconds,
                # which is longer than win_s=4.0s. It should be <= win_s * sr.
                nperseg = min(len(seg), 256) # Adjust nperseg to be reasonable for window size
                
                f, pxx = signal.welch(seg, sr, nperseg=nperseg)
                
                # Ensure f and pxx are not empty and contain valid data
                if len(f) == 0 or len(pxx) == 0:
                    continue

                # Crude "carrier" and "harmonic" peak detection
                # Ensure peaks are valid and distinct
                pk_idx = np.argmax(pxx)
                pk = f[pk_idx]

                # Find next prominent peak (harmonic)
                # Ensure we are looking at frequencies higher than pk
                # And there's data to support it
                harmonic_search_indices = np.where(f > pk * 1.1)[0] # Look for peaks slightly higher than carrier
                if len(harmonic_search_indices) == 0:
                    continue # No higher frequencies to find a harmonic

                harm_pxx = pxx[harmonic_search_indices]
                harm_f = f[harmonic_search_indices]

                if len(harm_pxx) == 0:
                    continue

                harm_idx_in_subset = np.argmax(harm_pxx)
                harm = harm_f[harm_idx_in_subset]
                
                if harm == 0: # Avoid division by zero
                    continue

                ratio = pk / harm
                ki_hat = ratio * np.pi # Restore Ki scale
                
                # Get the time for the current window
                window_time = trace.stats.starttime + s_idx / sr
                ki_series.append((window_time.timestamp, ki_hat)) # Store timestamp for easier serialization

            except Exception as e:
                # print(f"Error processing window at time {trace.stats.starttime + s_idx / sr}: {e}")
                continue # Skip problematic windows
        
        # This module should return the ki_series, which the main analyzer loop can aggregate
        # Convert to list of lists or similar for JSON serialization
        return {"ki_series": ki_series}

class BaseAnalysisModule:
    """Base class for analysis modules."""
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self, trace, processed_trace=None, **kwargs):
        """Analyze a trace. Subclasses must implement this."""
        raise NotImplementedError("Subclasses must implement analyze()")

    def get_name(self):
        """Get the name of the module."""
        return self.__class__.__name__

    def get_description(self):
        """Get a description of the module."""
        return self.__doc__ or "No description available"

# --- Analysis Modules (Self-Contained & Fixed) ---

class KiTransitionAnalyzer(BaseAnalysisModule):
    """
    Analyzes the Ki time series for transition patterns (e.g., sigmoid, hysteresis).
    Generates a CSV file for ki_series.
    """
    def analyze(self, trace, processed_trace=None, ki_series_data=None, **kwargs):
        results = []
        if not ki_series_data:
            return results

        trace_id = trace.id
        
        # Convert ki_series_data to pandas DataFrame for easier manipulation
        df_ki = pd.DataFrame(ki_series_data, columns=['timestamp', 'ki_hat'])
        df_ki['datetime'] = pd.to_datetime(df_ki['timestamp'], unit='s')
        df_ki = df_ki.set_index('datetime')

        # Save ki_series to a separate CSV file
        ki_series_csv_path = self.analyzer.data_dir / f"{trace_id.replace('/', '_')}_ki_series.csv"
        df_ki.to_csv(ki_series_csv_path)
        print(f"Ki series for trace {trace_id} saved to {ki_series_csv_path}")

        # --- Transition Analysis ---
        # A simple approach to detect significant changes in Ki_hat
        # This is a placeholder for more sophisticated analysis (sigmoid fitting, hysteresis detection)

        # Example: Look for large changes in Ki_hat
        df_ki['ki_diff'] = df_ki['ki_hat'].diff().abs()
        significant_changes = df_ki[df_ki['ki_diff'] > 0.1 * df_ki['ki_hat'].mean()] # Threshold can be tuned

        if not significant_changes.empty:
            result = self.analyzer.AnalysisResult(
                trace_id=trace_id,
                start_time=trace.stats.starttime,
                end_time=trace.stats.endtime
            )
            result.add_metric('num_significant_ki_changes', len(significant_changes))
            result.add_metric('max_ki_change', significant_changes['ki_diff'].max())
            result.add_pattern('ki_change_times', significant_changes['timestamp'].tolist())
            
            # Placeholder for actual sigmoid/hysteresis detection
            # For a real implementation, you'd use curve fitting, state-space models, etc.
            # Example: Check if it looks like a transition from KI_REST to KI_MOTION
            first_ki = df_ki['ki_hat'].iloc[0]
            last_ki = df_ki['ki_hat'].iloc[-1]
            
            transition_type = "None"
            if abs(first_ki - KI_REST) < 0.1 and abs(last_ki - KI_MOTION) < 0.1 and len(significant_changes) > 1:
                transition_type = "Rest_to_Motion_like_transition"
            elif abs(first_ki - KI_MOTION) < 0.1 and abs(last_ki - KI_REST) < 0.1 and len(significant_changes) > 1:
                transition_type = "Motion_to_Rest_like_transition"

            result.add_pattern('ki_transition_type', transition_type)
            results.append(result)

        # You might also want to plot the Ki series
        try:
            plt.figure(figsize=(10, 4))
            plt.plot(df_ki.index, df_ki['ki_hat'])
            plt.axhline(y=KI_REST, color='g', linestyle='--', label='KI_REST')
            plt.axhline(y=KI_MOTION, color='r', linestyle='--', label='KI_MOTION')
            plt.title(f'Ki_hat Series for {trace_id}')
            plt.xlabel('Time')
            plt.ylabel('Ki_hat')
            plt.legend()
            plt.grid(True)
            plot_path = self.analyzer.plots_dir / f"{trace_id.replace('/', '_')}_ki_series.png"
            plt.savefig(plot_path)
            plt.close()
            result_plot = self.analyzer.AnalysisResult(
                trace_id=trace_id,
                start_time=trace.stats.starttime,
                end_time=trace.stats.endtime
            )
            result_plot.add_plot_data('ki_series_plot', str(plot_path))
            results.append(result_plot)

        except Exception as e:
            print(f"Error generating Ki series plot for {trace_id}: {e}")
            traceback.print_exc()

        return results

class PhaseCouplingAnalyzer(BaseAnalysisModule):
    """
    Analyzes phase coupling, bicoherence, and modulation index.
    This module contains fixes for the previously reported bugs.
    """
    def modulation_index(self, phase, amp):
        """
        Calculates the modulation index (MI) for phase-amplitude coupling.
        FIX: Handles potential log(0) errors by adding a small epsilon.
        """
        bins = np.linspace(-np.pi, np.pi, 18 + 1)
        mean_amp = np.zeros(len(bins) - 1)
        
        for i in range(len(bins) - 1):
            indices = np.where((phase >= bins[i]) & (phase < bins[i+1]))[0]
            if len(indices) > 0:
                mean_amp[i] = np.mean(amp[indices])
        
        # BUG FIX: Add a small epsilon to avoid log(0) and division by zero.
        epsilon = 1e-15
        mean_amp_norm = (mean_amp + epsilon) / (np.sum(mean_amp) + epsilon)
        
        uniform = np.ones_like(mean_amp_norm) / len(mean_amp_norm)
        
        # Calculate Modulation Index (Kullback-Leibler divergence)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            mi = np.sum(mean_amp_norm * np.log(mean_amp_norm / uniform))
        
        return mi / np.log(len(mean_amp_norm)) if mi > 0 else 0

    def bicoherence(self, data, sampling_rate, nperseg=256):
        """
        Calculates bicoherence.
        FIX: This function now correctly accepts the 'sampling_rate' argument.
        """
        nperseg = min(len(data), nperseg)
        if nperseg < 1:
            return np.array([[]]), np.array([]), np.array([])

        freqs, t, stft = signal.stft(data, fs=sampling_rate, nperseg=nperseg)
        
        # Bicoherence calculation
        bic = np.zeros((len(freqs), len(freqs)), dtype=np.complex128)
        for f1_idx, f1 in enumerate(freqs):
            for f2_idx, f2 in enumerate(freqs):
                f_sum = f1 + f2
                f_sum_idx = np.argmin(np.abs(freqs - f_sum))
                
                if f_sum_idx < len(freqs):
                    x_f1 = stft[f1_idx, :]
                    x_f2 = stft[f2_idx, :]
                    x_f_sum = stft[f_sum_idx, :]
                    
                    numerator = np.mean(x_f1 * x_f2 * np.conj(x_f_sum))
                    denominator = np.sqrt(np.mean(np.abs(x_f1 * x_f2)**2) * np.mean(np.abs(x_f_sum)**2))
                    
                    if denominator > 1e-10:
                        bic[f1_idx, f2_idx] = numerator / denominator
        
        return freqs, freqs, np.abs(bic)

    def analyze(self, trace, processed_trace=None, **kwargs):
        results = []
        data = processed_trace.data
        sr = trace.stats.sampling_rate
        
        # --- Bicoherence Analysis ---
        try:
            # BUG FIX: Pass the sampling rate to the bicoherence function.
            f1, f2, bic = self.bicoherence(data, sr)
            if bic.size > 0:
                # Look for significant peaks in bicoherence
                threshold = np.mean(bic) + 3 * np.std(bic)
                peaks = np.where(bic > threshold)
                
                if len(peaks[0]) > 0:
                    result = self.analyzer.AnalysisResult(
                        trace_id=trace.id,
                        start_time=trace.stats.starttime,
                        end_time=trace.stats.endtime
                    )
                    result.add_metric('bicoherence_max', np.max(bic))
                    result.add_metric('bicoherence_mean', np.mean(bic))
                    result.add_metric('bicoherence_peaks', len(peaks[0]))
                    result.add_metric('bicoherence_significance', (np.max(bic) - np.mean(bic)) / np.std(bic))
                    result.add_pattern('bicoherence_hotspots', list(zip(f1[peaks[0]], f2[peaks[1]])))
                    results.append(result)
        except Exception as e:
            print(f"Error in bicoherence analysis: {e}")
            traceback.print_exc()

        # --- Phase-Amplitude Coupling (PAC) Analysis ---
        try:
            # Define frequency bands for phase and amplitude
            low_freq_band = [1, 4]   # Theta-like band for phase
            high_freq_band = [30, 80] # Gamma-like band for amplitude

            # Filter for phase
            sos_phase = signal.butter(2, low_freq_band, 'bandpass', fs=sr, output='sos')
            phase_data = signal.sosfilt(sos_phase, data)
            phase_angle = np.angle(signal.hilbert(phase_data))

            # Filter for amplitude
            sos_amp = signal.butter(2, high_freq_band, 'bandpass', fs=sr, output='sos')
            amp_data = signal.sosfilt(sos_amp, data)
            amp_envelope = np.abs(signal.hilbert(amp_data))
            
            mi = self.modulation_index(phase_angle, amp_envelope)
            
            if mi > 0.01: # Threshold for interesting MI
                result = self.analyzer.AnalysisResult(
                    trace_id=trace.id,
                    start_time=trace.stats.starttime,
                    end_time=trace.stats.endtime
                )
                result.add_metric('modulation_index', mi)
                # Significance can be estimated with surrogate data, but for now, we use the value itself
                result.add_metric('pac_significance', mi * 100) 
                results.append(result)
        except Exception as e:
            print(f"Error in PAC analysis: {e}")
            traceback.print_exc()
            
        return results

class CycleRatioAnalyzer(BaseAnalysisModule):
    """Analyzes ratios between dominant cycle periods against Ki values."""
    def analyze(self, trace, processed_trace=None, **kwargs):
        results = []
        data = processed_trace.data
        sr = trace.stats.sampling_rate
        
        f, pxx = signal.welch(data, sr, nperseg=min(2048, len(data)))
        peaks, _ = signal.find_peaks(pxx, height=np.mean(pxx), distance=5)
        
        if len(peaks) < 2:
            return []
            
        # Get the top 5 frequencies by prominence
        peak_prominences = signal.peak_prominences(pxx, peaks)[0]
        top_peak_indices = peaks[np.argsort(peak_prominences)[-5:]]
        top_freqs = f[top_peak_indices]
        
        # Check ratios
        for i in range(len(top_freqs)):
            for j in range(i + 1, len(top_freqs)):
                ratio = top_freqs[i] / top_freqs[j]
                
                # Check against Ki/pi and Golden Ratio
                targets = {
                    'ki_motion_ratio': KI_MOTION / PI,
                    'ki_rest_ratio': KI_REST / PI,
                    'golden_ratio': GOLDEN_RATIO
                }
                
                for name, target_ratio in targets.items():
                    if abs(ratio - target_ratio) < 0.05 or abs(1/ratio - target_ratio) < 0.05:
                        result = self.analyzer.AnalysisResult(
                            trace_id=trace.id,
                            start_time=trace.stats.starttime,
                            end_time=trace.stats.endtime
                        )
                        result.add_metric(f'ratio_found_{name}', ratio)
                        result.add_metric(f'ratio_significance', 5.0) # High significance for a match
                        result.add_pattern('frequencies', (top_freqs[i], top_freqs[j]))
                        results.append(result)
        return results

class HarmonicPatternAnalyzer(BaseAnalysisModule):
    """Searches for harmonic series related to Ki-derived fundamental frequencies."""
    def analyze(self, trace, processed_trace=None, **kwargs):
        results = []
        data = processed_trace.data
        sr = trace.stats.sampling_rate
        
        ki_freqs = self.analyzer.get_ki_phase_frequencies(sr)
        f_fund = ki_freqs.get('ki_fundamental')
        
        if not f_fund or f_fund > sr / 2:
            return []

        f, pxx = signal.welch(data, sr, nperseg=min(4096, len(data)))
        
        # Look for harmonics of the fundamental Ki frequency
        harmonics_found = 0
        total_power = 0
        for n in range(2, 6): # Check up to the 5th harmonic
            harmonic_freq = f_fund * n
            if harmonic_freq > sr / 2:
                break
            
            # Find the closest frequency peak in the spectrum
            peak_indices, _ = signal.find_peaks(pxx, height=np.mean(pxx))
            if len(peak_indices) == 0: continue

            closest_peak_idx = peak_indices[np.argmin(np.abs(f[peak_indices] - harmonic_freq))]
            
            # Check if the closest peak is within a tolerance
            if abs(f[closest_peak_idx] - harmonic_freq) < (f_fund * 0.1): # 10% tolerance
                harmonics_found += 1
                total_power += pxx[closest_peak_idx]

        if harmonics_found >= 2: # Found at least 2 harmonics
            result = self.analyzer.AnalysisResult(
                trace_id=trace.id,
                start_time=trace.stats.starttime,
                end_time=trace.stats.endtime
            )
            result.add_metric('harmonics_found', harmonics_found)
            result.add_metric('harmonic_power', total_power)
            result.add_metric('harmonic_significance', harmonics_found * 2.0)
            results.append(result)
            
        return results

# --- Main Analyzer Class ---

class KiResonanceAnalyzer:
    """Core analyzer for Ki-related patterns in time series data."""
    def __init__(self, output_dir=None, ki_value=KI_MOTION, significance_threshold=2.0):
        self.ki_value = ki_value
        self.alternate_ki = KI_REST if ki_value == KI_MOTION else KI_MOTION
        self.significance_threshold = significance_threshold
        self.AnalysisResult = AnalysisResult
        
        self.output_dir = Path(output_dir) if output_dir else Path('ki_resonance_results')
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        self.plots_dir = self.output_dir / 'plots'
        self.data_dir = self.output_dir / 'data'
        self.reports_dir = self.output_dir / 'reports'
        for directory in [self.plots_dir, self.data_dir, self.reports_dir]:
            directory.mkdir(exist_ok=True)
            
        self.session_start_time = datetime.now()
        self.session_id = self.session_start_time.strftime("%Y%m%d_%H%M%S")
        self.results = []
        self.processed_file_count = 0
        
        # Register built-in modules
        self.modules = {
            "ki_state_tracker": KiStateTracker, # Added KiStateTracker
            "ki_transition_analyzer": KiTransitionAnalyzer, # Added KiTransitionAnalyzer
            "cycle_ratio": CycleRatioAnalyzer,
            "harmonic_pattern": HarmonicPatternAnalyzer,
            "phase_coupling": PhaseCouplingAnalyzer,
        }

    def preprocess_trace(self, trace):
        """Perform basic preprocessing on a trace."""
        processed = trace.copy()
        processed.detrend("demean")
        processed.detrend("linear")
        nyquist = processed.stats.sampling_rate / 2
        if nyquist > 0.01:
            processed.filter('bandpass', freqmin=0.01, freqmax=nyquist * 0.95, corners=2, zerophase=True)
        return processed

    def analyze_trace(self, trace, filename=None, modules=None):
        """Analyze a trace with all registered modules."""
        try:
            processed_trace = self.preprocess_trace(trace)
            trace_results = []
            
            module_classes = self.modules
            
            # Special handling for KiStateTracker to pass its output to KiTransitionAnalyzer
            ki_series_data = None
            if "ki_state_tracker" in module_classes:
                try:
                    ki_tracker_module = module_classes["ki_state_tracker"](self)
                    tracker_output = ki_tracker_module.analyze(trace, processed_trace)
                    if "ki_series" in tracker_output:
                        ki_series_data = tracker_output["ki_series"]
                        # You can optionally add a result for KiStateTracker itself
                        # result_tracker = self.AnalysisResult(
                        #     trace_id=trace.id,
                        #     start_time=trace.stats.starttime,
                        #     end_time=trace.stats.endtime
                        # )
                        # result_tracker.add_pattern('ki_series_raw', ki_series_data)
                        # result_tracker.add_metadata('module', "ki_state_tracker")
                        # result_tracker.add_metadata('filename', filename)
                        # trace_results.append(result_tracker)
                except Exception as e:
                    print(f"Error in KiStateTracker module: {e}")
                    traceback.print_exc()

            for module_name, module_class in module_classes.items():
                if module_name == "ki_state_tracker": # Already handled above
                    continue

                try:
                    module = module_class(self)
                    # Pass ki_series_data to KiTransitionAnalyzer
                    if module_name == "ki_transition_analyzer":
                        module_results = module.analyze(trace, processed_trace, ki_series_data=ki_series_data)
                    else:
                        module_results = module.analyze(trace, processed_trace)
                    
                    for result in module_results:
                        result.add_metadata('module', module_name)
                        result.add_metadata('filename', filename)
                    trace_results.extend(module_results)
                            
                except Exception as e:
                    print(f"Error in module {module_name}: {e}")
                    traceback.print_exc()
            
            return trace_results
            
        except Exception as e:
            print(f"Error analyzing trace {trace.id}: {e}")
            traceback.print_exc()
            return []

    def process_files(self, file_paths):
        """Process a list of miniseed files."""
        all_results = []
        print(f"Processing {len(file_paths)} files...")
        for file_path in tqdm.tqdm(file_paths, desc="Processing files"):
            file_path = Path(file_path)
            try:
                st = read(str(file_path), headonly=False)
                for tr in st:
                    trace_results = self.analyze_trace(tr, file_path.name)
                    if trace_results:
                        all_results.extend(trace_results)
                self.processed_file_count += 1
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
        
        self.results.extend(all_results)
        return all_results

    def save_results(self):
        """Save analysis results to JSON and CSV files."""
        if not self.results:
            print("No results to save.")
            return
        
        results_dicts = [result.to_dict() for result in self.results]
        
        json_path = self.data_dir / f"{self.session_id}_results.json"
        with open(json_path, 'w') as f:
            json.dump(results_dicts, f, indent=2)
        print(f"Results saved to {json_path}")

        try:
            flat_results = []
            for r in results_dicts:
                flat_r = {
                    'trace_id': r.get('trace_id'),
                    'start_time': r.get('start_time'),
                    'end_time': r.get('end_time'),
                    'module': r.get('metadata', {}).get('module'),
                    'filename': r.get('metadata', {}).get('filename'),
                }
                flat_r.update({f'metric_{k}': v for k, v in r.get('metrics', {}).items()})
                flat_r.update({f'pattern_{k}': str(v) for k, v in r.get('patterns', {}).items()}) # Include patterns as string
                flat_results.append(flat_r)
            
            df = pd.DataFrame(flat_results)
            csv_path = self.data_dir / f"{self.session_id}_results.csv"
            df.to_csv(csv_path, index=False)
            print(f"Results saved to {csv_path}")
        except Exception as e:
            print(f"Warning: Could not create CSV report. {e}")
            traceback.print_exc()


    def generate_report(self):
        """Generate a summary HTML report."""
        if not self.results:
            print("No results to generate report from.")
            return

        report_path = self.reports_dir / f"{self.session_id}_report.html"
        
        # Simple HTML report generation
        html = f"""
        <!DOCTYPE html>
        <html><head><title>Ki Analysis Report</title>
        <style>
            body {{ font-family: sans-serif; margin: 2em; background-color: #f9f9f9; }}
            h1, h2 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background-color: #e9e9e9; }}
            .summary {{ background-color: #eee; padding: 1em; border-radius: 5px; }}
            .plot-container {{ margin-top: 20px; border: 1px solid #ddd; padding: 10px; background-color: #fff; }}
        </style>
        </head><body>
        <h1>Ki Resonance Analysis Report</h1>
        <div class="summary">
            <p>Session ID: {self.session_id}</p>
            <p>Files Processed: {self.processed_file_count}</p>
            <p>Total Results Found: {len(self.results)}</p>
        </div>
        <h2>Results Summary</h2>
        """
        
        try:
            df = pd.read_csv(self.data_dir / f"{self.session_id}_results.csv")
            html += df.to_html(index=False, border=0)
        except Exception as e:
            html += f"<p>Could not load CSV data for report: {e}</p>"

        html += "<h2>Generated Plots</h2>"
        plot_files = list(self.plots_dir.glob("*.png"))
        if plot_files:
            for plot_file in plot_files:
                html += f"""
                <div class="plot-container">
                    <h3>{plot_file.name}</h3>
                    <img src="./plots/{plot_file.name}" alt="{plot_file.name}" style="max-width:100%;">
                </div>
                """
        else:
            html += "<p>No plots generated.</p>"

        html += "</body></html>"
        
        with open(report_path, 'w') as f:
            f.write(html)
        print(f"HTML report generated: {report_path}")
        return report_path

    def get_ki_phase_frequencies(self, sampling_rate):
        """Calculate expected frequencies related to Ki values."""
        if sampling_rate == 0: return {}
        return {
            'ki_fundamental': sampling_rate / self.ki_value,
            'ki_rest_freq': sampling_rate / KI_REST,
            'ki_motion_freq': sampling_rate / KI_MOTION,
            'pi_fundamental': sampling_rate / PI
        }

# --- GUI Class ---

class AnalysisGUI(tk.Tk):
    """A simple Tkinter GUI for running the analysis."""
    def __init__(self):
        super().__init__()
        self.title("Ki Resonance Analyzer")
        self.geometry("500x400") # Increased height for more elements

        self.file_paths = []
        self.output_dir = str(Path.home() / "Ki_Analysis_Results")

        # --- Widgets ---
        tk.Label(self, text="MSEED File Analysis for Ki Resonance", font=("Helvetica", 16)).pack(pady=10)

        # File selection
        self.files_label = tk.Label(self, text="No files selected.", wraplength=480)
        self.files_label.pack(pady=5)
        tk.Button(self, text="Select MSEED Files", command=self.select_files).pack(pady=5)

        # Output folder
        self.output_label = tk.Label(self, text=f"Output: {self.output_dir}", wraplength=480)
        self.output_label.pack(pady=5)
        tk.Button(self, text="Select Output Folder", command=self.select_output_dir).pack(pady=5)

        # Session name
        tk.Label(self, text="Output Subfolder Name (Optional):").pack(pady=(10, 0))
        self.session_name_entry = tk.Entry(self, width=50)
        self.session_name_entry.pack()

        # Ki Value selection
        tk.Label(self, text="Select Primary Ki Value:").pack(pady=(10, 0))
        self.ki_value_var = tk.StringVar(self)
        self.ki_value_var.set("KI_MOTION") # default value
        self.ki_value_optionmenu = tk.OptionMenu(self, self.ki_value_var, "KI_MOTION", "KI_REST")
        self.ki_value_optionmenu.pack()

        # Run button
        tk.Button(self, text="Run Analysis", command=self.run_analysis, bg="green", fg="white", font=("Helvetica", 12)).pack(pady=20)

    def select_files(self):
        self.file_paths = filedialog.askopenfilenames(
            title="Select MSEED files",
            filetypes=(("MSEED files", "*.mseed *.msd"), ("All files", "*.*"))
        )
        if self.file_paths:
            self.files_label.config(text=f"{len(self.file_paths)} file(s) selected.")
        else:
            self.files_label.config(text="No files selected.")

    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="Select Output Folder")
        if dir_path:
            self.output_dir = dir_path
            self.output_label.config(text=f"Output: {self.output_dir}")

    def run_analysis(self):
        if not self.file_paths:
            messagebox.showerror("Error", "Please select at least one MSEED file.")
            return
        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        session_name = self.session_name_entry.get().strip()
        if session_name:
            final_output_dir = Path(self.output_dir) / session_name
        else:
            final_output_dir = Path(self.output_dir)
        
        selected_ki_value_str = self.ki_value_var.get()
        ki_value_for_analyzer = KI_MOTION if selected_ki_value_str == "KI_MOTION" else KI_REST

        try:
            self.withdraw() # Hide the main window during analysis
            
            analyzer = KiResonanceAnalyzer(output_dir=final_output_dir, ki_value=ki_value_for_analyzer)
            analyzer.process_files(self.file_paths)
            analyzer.save_results()
            report_path = analyzer.generate_report()
            
            messagebox.showinfo("Success", f"Analysis complete!\n\nProcessed {analyzer.processed_file_count} files.\nFound {len(analyzer.results)} results.\n\nReport saved to:\n{report_path}")

        except Exception as e:
            messagebox.showerror("Analysis Failed", f"An error occurred:\n\n{e}")
            traceback.print_exc()
        finally:
            self.deiconify() # Show the main window again


if __name__ == '__main__':
    # This will run the GUI by default.
    # The old command-line interface can be added back here if needed.
    app = AnalysisGUI()
    app.mainloop()