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
                    serializable_patterns[name] = f"<{type(pattern).__name__} with {len(pattern)} items>"
                else:
                    serializable_patterns[name] = f"<{type(pattern).__name__}>"
        result['patterns'] = serializable_patterns
        return result

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
            
            for module_name, module_class in module_classes.items():
                try:
                    module = module_class(self)
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
                flat_results.append(flat_r)
            
            df = pd.DataFrame(flat_results)
            csv_path = self.data_dir / f"{self.session_id}_results.csv"
            df.to_csv(csv_path, index=False)
            print(f"Results saved to {csv_path}")
        except Exception as e:
            print(f"Warning: Could not create CSV report. {e}")

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
        self.geometry("500x350")

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

        try:
            self.withdraw() # Hide the main window during analysis
            
            analyzer = KiResonanceAnalyzer(output_dir=final_output_dir)
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