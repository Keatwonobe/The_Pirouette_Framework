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

# Constants
KI_REST = 4.14159      # Ki in rest state
KI_MOTION = 4.18879    # Ki in motion state
DEFAULT_BAND_WIDTH = 0.05  # Default bandwidth for analysis


class KiAnalyzer:
    """
    Class for analyzing miniseed files for evidence of Ki-related phenomena
    """
    
    def __init__(self, ki_value=KI_MOTION, band_width=DEFAULT_BAND_WIDTH, 
                 output_dir=None, significance_threshold=3.0):
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
        """
        self.ki_value = ki_value
        self.band_width = band_width
        
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
        self.session_start_time = datetime.now()
        self.session_id = self.session_start_time.strftime("%Y%m%d_%H%M%S")
        
        # Initialize results container
        self.results = []
            # Add these lines to track processed files
        self.processed_files = []
        self.processed_file_count = 0
        
    def process_file(self, file_path, save_plots=True):
        """
        Process a single miniseed file
        
        Parameters:
        -----------
        file_path : str or Path
            Path to the miniseed file
        save_plots : bool
            Whether to save plots for the file
            
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
                trace_results = self.analyze_trace(tr, file_path.name, save_plots)
                if trace_results:
                    file_results.extend(trace_results)
            
            # Save summary for this file if we found anything
            if file_results and save_plots:
                self.save_file_summary(file_path, st, file_results)
                        # Add these lines to track the processed file
            if file_path not in self.processed_files:
                self.processed_files.append(file_path)
                self.processed_file_count += 1
                
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            
        return file_results
    
    def analyze_trace(self, tr, filename, save_plots=True):
        """
        Analyze a single trace for Ki-related phenomena
        
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
            
            # Apply bandpass filter around frequencies of interest
            tr_filtered = tr_processed.copy()
            min_freq = max(0.01, self.ki_value - 2 * self.band_width)
            max_freq = self.ki_value + 2 * self.band_width
            tr_filtered.filter('bandpass', freqmin=min_freq, freqmax=max_freq, corners=4)
            
            # Compute FFT
            n = len(tr_processed.data)
            dt = tr_processed.stats.delta
            freqs = np.fft.rfftfreq(n, d=dt)
            fft_vals = np.abs(np.fft.rfft(tr_processed.data))
            
            # Compute spectrogram
            nperseg = min(256, n // 8)
            f, t, Sxx = signal.spectrogram(tr_processed.data, 1/dt, nperseg=nperseg)
            
            # Analyze frequency band around Ki
            ki_band = (freqs >= (self.ki_value - self.band_width)) & (freqs <= (self.ki_value + self.band_width))
            
            if not any(ki_band):
                return []  # No frequencies in our band of interest
                
            # Calculate metrics
            band_energy = np.mean(fft_vals[ki_band])
            baseline = np.mean(fft_vals) + self.significance_threshold * np.std(fft_vals)
            energy_ratio = band_energy / (np.mean(fft_vals) + 1e-10)
            
            # Calculate additional statistics
            peak_freq = freqs[np.argmax(fft_vals[ki_band] if np.any(ki_band) else fft_vals)]
            peak_value = np.max(fft_vals[ki_band] if np.any(ki_band) else fft_vals)
            band_kurtosis = kurtosis(fft_vals[ki_band]) if np.any(ki_band) else 0
            band_skew = skew(fft_vals[ki_band]) if np.any(ki_band) else 0
            
            # Calculate temporal Ki signatures
            envelope = np.abs(signal.hilbert(tr_filtered.data))
            envelope_mean = np.mean(envelope)
            envelope_std = np.std(envelope)
            envelope_max = np.max(envelope)
            
            # Check if this exceeds our threshold for significance
            if band_energy > baseline:
                # Format the results
                detection = {
                    'filename': filename,
                    'trace_id': tr.id,
                    'start_time': tr.stats.starttime,
                    'end_time': tr.stats.endtime,
                    'duration': tr.stats.endtime - tr.stats.starttime,
                    'sampling_rate': tr.stats.sampling_rate,
                    'band_energy': band_energy,
                    'baseline': baseline,
                    'energy_ratio': energy_ratio,
                    'peak_freq': peak_freq,
                    'peak_value': peak_value,
                    'ki_distance': abs(peak_freq - self.ki_value),
                    'band_kurtosis': band_kurtosis,
                    'band_skew': band_skew,
                    'envelope_mean': envelope_mean,
                    'envelope_std': envelope_std,
                    'envelope_max': envelope_max
                }
                
                trace_results.append(detection)
                
                # Save plots if requested
                if save_plots:
                    self.save_trace_plots(tr, tr_processed, tr_filtered, freqs, fft_vals, 
                                          f, t, Sxx, envelope, detection)
        
        except Exception as e:
            print(f"Error analyzing trace {tr.id}: {e}")
            
        return trace_results
    
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
    
    def process_directory(self, directory_path, pattern="*.mseed", parallel=True, max_workers=None):
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
            
        Returns:
        --------
        list
            Combined results from all files
        """
        directory_path = Path(directory_path)
        files = list(directory_path.glob(pattern))
        
        if not files:
            print(f"No files matching '{pattern}' found in {directory_path}")
            return []
        
        print(f"Found {len(files)} files to process in {directory_path}")
        
        if parallel and len(files) > 1:
            # Process files in parallel
            if max_workers is None:
                max_workers = cpu_count()
                
            print(f"Processing files in parallel with {max_workers} workers")
            
            with Pool(processes=max_workers) as pool:
                all_results = pool.map(self.process_file, files)
                
            # Flatten results list
            flat_results = [item for sublist in all_results for item in sublist]
            
        else:
            # Process files sequentially
            print("Processing files sequentially")
            flat_results = []
            for i, file in enumerate(files):
                print(f"Processing file {i+1}/{len(files)}: {file.name}")
                file_results = self.process_file(file)
                flat_results.extend(file_results)
                
        # Store all results
        self.results = flat_results

        # At the end, update the file count explicitly
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
            'significance_threshold': self.significance_threshold
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
            f.write(f"  Significance Threshold: {stats['significance_threshold']} std\n\n")
            
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
            band_width=self.band_width,
            output_dir=self.output_dir / 'ki_rest',
            significance_threshold=self.significance_threshold
        )
        
        # This analyzer is already set for motion Ki
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
        
        sns.boxplot(x='ki_mode', y='energy_ratio', data=combined_df)
        plt.title('Energy Ratio Comparison between Ki Modes')
        plt.xlabel('Ki Mode')
        plt.ylabel('Energy Ratio')
        
        plt.savefig(self.reports_dir / f"{self.session_id}_energy_ratio_comparison.png", dpi=300)
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


def process_args():
    """Process command-line arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze miniseed files for Ki-related phenomena")
    
    parser.add_argument('input', help="Input file or directory path")
    parser.add_argument('-o', '--output', help="Output directory", default=None)
    parser.add_argument('-k', '--ki-value', type=float, default=KI_MOTION, 
                        help=f"Ki value to analyze (default: {KI_MOTION})")
    parser.add_argument('-b', '--bandwidth', type=float, default=DEFAULT_BAND_WIDTH,
                        help=f"Analysis bandwidth around Ki (default: {DEFAULT_BAND_WIDTH})")
    parser.add_argument('-t', '--threshold', type=float, default=3.0,
                        help="Significance threshold in standard deviations (default: 3.0)")
    parser.add_argument('-p', '--pattern', default="*.mseed",
                        help="File pattern to match (default: *.mseed)")
    parser.add_argument('-s', '--sequential', action='store_true',
                        help="Process files sequentially instead of in parallel")
    parser.add_argument('-w', '--workers', type=int, default=None,
                        help="Number of parallel workers (default: CPU count)")
    parser.add_argument('-d', '--dual-ki', action='store_true',
                        help="Analyze both rest and motion Ki values")
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
        significance_threshold=args.threshold
    )
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Process a single file
        print(f"Processing file: {input_path}")
        results = analyzer.process_file(input_path)
        print(f"Found {len(results)} Ki phenomena in file")
        
    elif input_path.is_dir():
        # Process a directory
        print(f"Processing directory: {input_path}")
        results = analyzer.process_directory(
            input_path, 
            pattern=args.pattern,
            parallel=not args.sequential,
            max_workers=args.workers
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
        import seaborn as sns
        sys.exit(main())
    except ImportError:
        print("Warning: seaborn not installed - some visualizations will be limited.")
        try:
            sys.exit(main())
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)