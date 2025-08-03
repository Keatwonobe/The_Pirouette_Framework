import os, sys

# 1) make sure the directory containing this script is on Python's path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# 2) also add the modules/ folder if you haven't already
MODULES_DIR = os.path.join(SCRIPT_DIR, 'modules')
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from datetime import datetime
from scipy import signal, stats
from scipy.stats import kurtosis, skew
from obspy import read, Stream, Trace
from multiprocessing import Pool, cpu_count
import platform
import tqdm
import warnings
import json
import importlib.util

# IMPORTANT: Try to import AnalysisResult first, and if not found, use our own definition
try:
    from analysis_result import AnalysisResult
    print("Successfully imported AnalysisResult from analysis_result.py")
except ImportError:
    print("Using internal AnalysisResult definition")
    # Define AnalysisResult class here (unchanged from your original code)
    class AnalysisResult:
        """Container for analysis results"""
        
        def __init__(self, trace_id=None, start_time=None, end_time=None):
            self.trace_id = trace_id
            self.start_time = start_time
            self.end_time = end_time
            self.metrics = {}
            self.patterns = {}
            self.plots = {}
            self.metadata = {}
        
        def add_metric(self, name, value):
            """Add a numeric metric to the result"""
            self.metrics[name] = value
            return self
        
        def add_pattern(self, name, data):
            """Add a detected pattern to the result"""
            self.patterns[name] = data
            return self
        
        def add_plot_data(self, name, data):
            """Add plot data to the result"""
            self.plots[name] = data
            return self
        
        def add_metadata(self, name, value):
            """Add metadata to the result"""
            self.metadata[name] = value
            return self
        
        def to_dict(self):
            """Convert to dictionary for storage/reporting"""
            result = {
                'trace_id': self.trace_id,
                'start_time': str(self.start_time) if self.start_time else None,
                'end_time': str(self.end_time) if self.end_time else None,
                'metrics': self.metrics,
                'metadata': self.metadata,
            }
            
            # Only include patterns that are serializable
            serializable_patterns = {}
            for name, pattern in self.patterns.items():
                try:
                    # Test if it can be serialized
                    json.dumps(pattern)
                    serializable_patterns[name] = pattern
                except (TypeError, OverflowError):
                    # If not serializable, store a description instead
                    if hasattr(pattern, '__len__'):
                        serializable_patterns[name] = f"<{type(pattern).__name__} with {len(pattern)} items>"
                    else:
                        serializable_patterns[name] = f"<{type(pattern).__name__}>"
            
            result['patterns'] = serializable_patterns
            return result

# Constants
KI_REST = 4.14159      # Ki in rest state
KI_MOTION = 4.18879    # Ki in motion (approximately 4π/3)
PI = 3.14159           # Pi constant
GOLDEN_RATIO = 1.61803 # Golden ratio

# Module system for easy extension
class ModuleRegistry:
    """Registry for analysis modules"""
    
    def __init__(self):
        self.modules = {}
        self.module_order = []
    
    def register(self, name, module_class):
        """Register a new analysis module"""
        if name in self.modules:
            print(f"Warning: Module {name} already registered, overwriting")
        self.modules[name] = module_class
        if name not in self.module_order:
            self.module_order.append(name)
    
    def get_module(self, name):
        """Get a module by name"""
        return self.modules.get(name)
    
    def get_all_modules(self):
        """Get all registered modules in registration order"""
        return [(name, self.modules[name]) for name in self.module_order]
    
    def load_module_file(self, filepath):
        """Load a module from a Python file"""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Module file {filepath} not found")
        
        module_name = filepath.stem
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        # Module should call register_module() to register itself
        return module_name


class AnalysisResult:
    """Container for analysis results"""
    
    def __init__(self, trace_id=None, start_time=None, end_time=None):
        self.trace_id = trace_id
        self.start_time = start_time
        self.end_time = end_time
        self.metrics = {}
        self.patterns = {}
        self.plots = {}
        self.metadata = {}
    
    def add_metric(self, name, value):
        """Add a numeric metric to the result"""
        self.metrics[name] = value
        return self
    
    def add_pattern(self, name, data):
        """Add a detected pattern to the result"""
        self.patterns[name] = data
        return self
    
    def add_plot_data(self, name, data):
        """Add plot data to the result"""
        self.plots[name] = data
        return self
    
    def add_metadata(self, name, value):
        """Add metadata to the result"""
        self.metadata[name] = value
        return self
    
    def to_dict(self):
        """Convert to dictionary for storage/reporting"""
        result = {
            'trace_id': self.trace_id,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'metrics': self.metrics,
            'metadata': self.metadata,
        }
        
        # Only include patterns that are serializable
        serializable_patterns = {}
        for name, pattern in self.patterns.items():
            try:
                # Test if it can be serialized
                json.dumps(pattern)
                serializable_patterns[name] = pattern
            except (TypeError, OverflowError):
                # If not serializable, store a description instead
                if hasattr(pattern, '__len__'):
                    serializable_patterns[name] = f"<{type(pattern).__name__} with {len(pattern)} items>"
                else:
                    serializable_patterns[name] = f"<{type(pattern).__name__}>"
        
        result['patterns'] = serializable_patterns
        return result


class BaseAnalysisModule:
    """Base class for analysis modules"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def analyze(self, trace, processed_trace=None, **kwargs):
        """
        Analyze a trace for Ki-related phenomena
        
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
        raise NotImplementedError("Subclasses must implement analyze()")
    
    def get_name(self):
        """Get the name of the module"""
        return self.__class__.__name__
    
    def get_description(self):
        """Get a description of the module"""
        return self.__doc__ or "No description available"


class KiResonanceAnalyzer:
    """
    Core analyzer for Ki-related patterns in time series data
    """
    
    def __init__(self, output_dir=None, ki_value=KI_MOTION, significance_threshold=2.0):
        """
        Initialize the analyzer
        
        Parameters:
        -----------
        output_dir : str or Path
            Directory for saving results (default: 'ki_resonance_results')
        ki_value : float
            Primary Ki value to consider (default: KI_MOTION)
        significance_threshold : float
            Threshold for significance in standard deviations (default: 2.0)
        """
        self.ki_value = ki_value
        self.alternate_ki = KI_REST if ki_value == KI_MOTION else KI_MOTION
        self.significance_threshold = significance_threshold
        self.AnalysisResult = AnalysisResult
        
        # Create output directory
        if output_dir is None:
            self.output_dir = Path('ki_resonance_results')
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Create subdirectories
        self.plots_dir = self.output_dir / 'plots'
        self.data_dir = self.output_dir / 'data'
        self.reports_dir = self.output_dir / 'reports'
        
        for directory in [self.plots_dir, self.data_dir, self.reports_dir]:
            directory.mkdir(exist_ok=True)
        
        # Initialize session
        self.session_start_time = datetime.now()
        self.session_id = self.session_start_time.strftime("%Y%m%d_%H%M%S")
        
        # Initialize results container
        self.results = []
        
        # Track processed files
        self.processed_files = []
        self.processed_file_count = 0
        
        # Initialize module registry
        self.module_registry = ModuleRegistry()
        
        # Register built-in modules
        self.register_built_in_modules()
    
    def register_built_in_modules(self):
        """Register built-in analysis modules"""
        # Import and register built-in modules
        from modules.cycle_ratio_analyzer import CycleRatioAnalyzer
        from modules.harmonic_pattern_analyzer import HarmonicPatternAnalyzer
        from modules.phase_coupling_analyzer import PhaseCouplingAnalyzer
        from modules.temporal_structure_analyzer import TemporalStructureAnalyzer
        #from modules.wavelet_resonance_analyzer import WaveletResonanceAnalyzer
        #from modules.phase_coherence_analyzer import PhaseCoherenceAnalyzer
        
        # Register modules
        self.module_registry.register("cycle_ratio", CycleRatioAnalyzer)
        self.module_registry.register("harmonic_pattern", HarmonicPatternAnalyzer)
        self.module_registry.register("phase_coupling", PhaseCouplingAnalyzer)
        self.module_registry.register("temporal_structure", TemporalStructureAnalyzer)
        #self.module_registry.register("wavelet_resonance", WaveletResonanceAnalyzer)
        #self.module_registry.register("phase_coherence", PhaseCoherenceAnalyzer)
    
    def register_module(self, name, module_class):
        """Register a new analysis module"""
        self.module_registry.register(name, module_class)
    
    def load_module_file(self, filepath):
        """Load a module from a Python file"""
        return self.module_registry.load_module_file(filepath)
    
    def preprocess_trace(self, trace):
        """
        Perform basic preprocessing on a trace
        
        Parameters:
        -----------
        trace : obspy.Trace
            The trace to preprocess
        
        Returns:
        --------
        obspy.Trace
            Preprocessed trace
        """
        # Make a copy to avoid modifying the original
        processed = trace.copy()
        
        # Remove mean and linear trend
        processed.detrend("demean")
        processed.detrend("linear")
        
        # Apply a very mild bandpass filter to remove extreme outliers
        nyquist = processed.stats.sampling_rate / 2
        processed.filter('bandpass', freqmin=0.01, freqmax=nyquist * 0.9, corners=2)
        
        return processed
    
    def analyze_trace(self, trace, filename=None, save_plots=True, modules=None):
        """
        Analyze a trace with all registered modules (or specified ones)
        
        Parameters:
        -----------
        trace : obspy.Trace
            The trace to analyze
        filename : str
            Original filename for reference
        save_plots : bool
            Whether to save plots
        modules : list
            List of module names to use (if None, use all)
            
        Returns:
        --------
        list
            List of AnalysisResult objects from all modules
        """
        try:
            # Preprocess the trace
            processed_trace = self.preprocess_trace(trace)
            
            # Prepare common result properties
            trace_results = []
            
            # Get module list
            if modules is None:
                module_classes = self.module_registry.get_all_modules()
            else:
                module_classes = [(name, self.module_registry.get_module(name)) 
                                  for name in modules if self.module_registry.get_module(name)]
            
            # Run each module
            for module_name, module_class in module_classes:
                try:
                    module = module_class(self)
                    module_results = module.analyze(trace, processed_trace)
                    
                    # Add module identifier to results
                    for result in module_results:
                        result.add_metadata('module', module_name)
                        result.add_metadata('filename', filename)
                        
                    trace_results.extend(module_results)
                    
                    # If the module found results and save_plots is True, generate plots
                    if module_results and save_plots and hasattr(module, 'generate_plots'):
                        for result in module_results:
                            module.generate_plots(result, self.plots_dir / f"{self.session_id}_{trace.id}")
                            
                except Exception as e:
                    print(f"Error in module {module_name}: {e}")
                    import traceback
                    traceback.print_exc()
            
            return trace_results
            
        except Exception as e:
            print(f"Error analyzing trace {trace.id}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def process_file(self, file_path, save_plots=True, modules=None):
        """
        Process a single miniseed file
        
        Parameters:
        -----------
        file_path : str or Path
            Path to the miniseed file
        save_plots : bool
            Whether to save plots for the file
        modules : list
            List of module names to use (if None, use all)
        
        Returns:
        --------
        list
            List of AnalysisResult objects from the file
        """
        file_path = Path(file_path)
        file_results = []
        
        try:
            # Read the miniseed file
            st = read(str(file_path), headonly=False)
            
            # Process each trace in the file
            for tr in st:
                # Analyze the trace
                trace_results = self.analyze_trace(tr, file_path.name, save_plots, modules)
                if trace_results:
                    file_results.extend(trace_results)
            
            # Track the processed file
            if file_path not in self.processed_files:
                self.processed_files.append(file_path)
                self.processed_file_count += 1
            
            # Add results to the main results list
            self.results.extend(file_results)
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            import traceback
            traceback.print_exc()
        
        return file_results
    
    def process_directory(self, directory_path, pattern="*.mseed", parallel=True, 
                         max_workers=None, save_plots=True, modules=None):
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
        save_plots : bool
            Whether to save plots
        modules : list
            List of module names to use (if None, use all)
        
        Returns:
        --------
        list
            List of AnalysisResult objects from all files
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
        
        # Save parameters as instance variables for wrapper
        self.temp_save_plots = save_plots
        self.temp_modules = modules
        
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
            
            # Flatten results list and add to main results
            flat_results = [item for sublist in all_results for item in sublist]
            self.results.extend(flat_results)
            
        else:
            # Process files sequentially
            print("Processing files sequentially")
            all_results = []
            for i, file in enumerate(tqdm.tqdm(files, desc="Processing files")):
                file_results = self.process_file(file, save_plots, modules)
                all_results.extend(file_results)
            
            # Results already added in process_file
            flat_results = all_results
        
        return flat_results
    
    def _process_file_wrapper(self, file_path):
        """Wrapper for multiprocessing"""
        return self.process_file(file_path, self.temp_save_plots, self.temp_modules)
    
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
        
        # Convert results to list of dictionaries
        results_dicts = [result.to_dict() for result in self.results]
        
        # Save as JSON
        json_path = self.data_dir / f"{self.session_id}_ki_resonance_results.json"
        with open(json_path, 'w') as f:
            json.dump(results_dicts, f, indent=2)
        
        # Try to convert to DataFrame for CSV/Excel export
        try:
            # Flatten the nested structures
            flat_results = []
            for r in results_dicts:
                flat_r = {
                    'trace_id': r['trace_id'],
                    'start_time': r['start_time'],
                    'end_time': r['end_time'],
                }
                
                # Include module name
                if 'metadata' in r and 'module' in r['metadata']:
                    flat_r['module'] = r['metadata']['module']
                
                # Include filename
                if 'metadata' in r and 'filename' in r['metadata']:
                    flat_r['filename'] = r['metadata']['filename']
                
                # Add all metrics
                for k, v in r.get('metrics', {}).items():
                    flat_r[f'metric_{k}'] = v
                
                flat_results.append(flat_r)
            
            # Create DataFrame
            df = pd.DataFrame(flat_results)
            
            # Save to CSV
            csv_path = self.data_dir / f"{self.session_id}_ki_resonance_results.csv"
            df.to_csv(csv_path, index=False)
            
            # Save to Excel
            excel_path = self.data_dir / f"{self.session_id}_ki_resonance_results.xlsx"
            df.to_excel(excel_path, index=False)
            
        except Exception as e:
            print(f"Warning: Could not create CSV/Excel")

    def generate_report(self, output_format='html'):
        """
        Generate a summary report of all analysis results
    
        Parameters:
        -----------
        output_format : str
            Format for the report ('html' or 'text')
    
        Returns:
        --------
        Path
            Path to the generated report
        """
        if not self.results:
            print("No results to generate report from.")
            return None
    
        # Count results by module
        module_counts = {}
        significant_counts = {}
    
        for result in self.results:
            module = result.metadata.get('module', 'unknown')
            if module not in module_counts:
                module_counts[module] = 0
                significant_counts[module] = 0
        
            module_counts[module] += 1
        
            # Check if any metric exceeds significance threshold
            for metric_name, value in result.metrics.items():
                if isinstance(value, (int, float)) and 'significance' in metric_name.lower() and value >= self.significance_threshold:
                    significant_counts[module] += 1
                    break
    
        # Generate report based on format
        if output_format.lower() == 'html':
            return self._generate_html_report(module_counts, significant_counts)
        else:
            return self._generate_text_report(module_counts, significant_counts)
    
    def _generate_html_report(self, module_counts, significant_counts):
        """Generate HTML report"""
        # Create report filename
        report_path = self.reports_dir / f"{self.session_id}_report.html"
    
        # Basic HTML template
        html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Ki Resonance Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1, h2, h3 {{ color: #333; }}
            .summary {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .highlight {{ background-color: #ffffcc; }}
            .significant {{ color: #d9534f; font-weight: bold; }}
            .image-gallery {{ display: flex; flex-wrap: wrap; gap: 10px; }}
            .image-container {{ width: 300px; margin-bottom: 20px; }}
            .image-container img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <h1>Ki Resonance Analysis Report</h1>
    
        <div class="summary">
            <h2>Summary</h2>
            <p>Session ID: {self.session_id}</p>
            <p>Analysis date: {self.session_start_time.strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>Files processed: {self.processed_file_count}</p>
            <p>Ki values analyzed: Primary = {self.ki_value}, Alternative = {self.alternate_ki}</p>
            <p>Significance threshold: {self.significance_threshold}</p>
            <p>Total results: {len(self.results)}</p>
        </div>
    
        <h2>Results by Module</h2>
        <table>
            <tr>
                <th>Module</th>
                <th>Total Results</th>
                <th>Significant Results</th>
                <th>Significance Rate</th>
            </tr>
    """
    
        # Add rows for each module
        for module, count in module_counts.items():
            sig_count = significant_counts.get(module, 0)
            sig_rate = f"{sig_count / count * 100:.1f}%" if count > 0 else "0%"
        
            html += f"""
            <tr>
                <td>{module}</td>
                <td>{count}</td>
                <td>{sig_count}</td>
                <td>{sig_rate}</td>
            </tr>"""
    
        # Calculate totals
        total_count = sum(module_counts.values())
        total_sig = sum(significant_counts.values())
        total_sig_rate = f"{total_sig / total_count * 100:.1f}%" if total_count > 0 else "0%"
    
        # Add totals row
        html += f"""
            <tr class="highlight">
                <td><strong>Total</strong></td>
                <td><strong>{total_count}</strong></td>
                <td><strong>{total_sig}</strong></td>
                <td><strong>{total_sig_rate}</strong></td>
            </tr>
        </table>
        """
    
        # Add Top Findings section if there are significant results
        if total_sig > 0:
            # Sort results by significance
            significant_results = []
            for result in self.results:
                for metric_name, value in result.metrics.items():
                    if isinstance(value, (int, float)) and 'significance' in metric_name.lower() and value >= self.significance_threshold:
                        significant_results.append((result, metric_name, value))
                        break
        
            # Sort by significance value (descending)
            significant_results.sort(key=lambda x: x[2], reverse=True)
        
            # Take top 10 or fewer
            top_n = min(10, len(significant_results))
        
            html += f"""
        <h2>Top {top_n} Significant Findings</h2>
        <table>
            <tr>
                <th>Trace ID</th>
                <th>Module</th>
                <th>Metric</th>
                <th>Value</th>
                <th>Time Range</th>
            </tr>
            """
        
            for result, metric_name, value in significant_results[:top_n]:
                html += f"""
            <tr>
                <td>{result.trace_id}</td>
                <td>{result.metadata.get('module', 'unknown')}</td>
                <td>{metric_name}</td>
                <td class="significant">{value:.3f}</td>
                <td>{result.start_time} to {result.end_time}</td>
            </tr>"""
        
            html += """
        </table>
            """
    
        # Add image gallery of plots if available
        plot_files = list(self.plots_dir.glob(f"{self.session_id}_*.png"))
        if plot_files:
            # Group by trace_id
            plots_by_trace = {}
            for plot_file in plot_files:
                parts = plot_file.stem.split('_')
                if len(parts) > 2:
                    trace_id = '_'.join(parts[1:-1])  # Assume format is session_id_trace_id_plot_name
                    if trace_id not in plots_by_trace:
                        plots_by_trace[trace_id] = []
                    plots_by_trace[trace_id].append(plot_file)
        
            html += """
        <h2>Visualization Gallery</h2>
        <p>Click on images to enlarge</p>
        <div class="image-gallery">
            """
        
            # Add each plot
            for trace_id, plots in plots_by_trace.items():
                for plot_file in plots:
                    plot_rel_path = plot_file.relative_to(self.output_dir)
                    plot_name = plot_file.stem.split('_')[-1]
                
                    html += f"""
            <div class="image-container">
                <h4>{trace_id}: {plot_name}</h4>
                <a href="../{plot_rel_path}" target="_blank">
                    <img src="../{plot_rel_path}" alt="{plot_name}">
                </a>
            </div>"""
        
            html += """
        </div>
            """
    
        # Close HTML
        html += """
    </body>
    </html>
        """
    
        # Write to file
        with open(report_path, 'w') as f:
            f.write(html)
    
        print(f"HTML report generated: {report_path}")
        return report_path

    def _generate_text_report(self, module_counts, significant_counts):
        """Generate text report"""
        # Create report filename
        report_path = self.reports_dir / f"{self.session_id}_report.txt"
    
        # Build text report
        lines = [
            "===== Ki Resonance Analysis Report =====",
            "",
            f"Session ID: {self.session_id}",
            f"Analysis date: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Files processed: {self.processed_file_count}",
            f"Ki values analyzed: Primary = {self.ki_value}, Alternative = {self.alternate_ki}",
            f"Significance threshold: {self.significance_threshold}",
            f"Total results: {len(self.results)}",
            "",
            "--- Results by Module ---",
            ""
        ]
    
        # Format as table
        lines.append(f"{'Module':<20} {'Total':<10} {'Significant':<15} {'Sig. Rate':<10}")
        lines.append("-" * 60)
    
        # Add rows for each module
        for module, count in module_counts.items():
            sig_count = significant_counts.get(module, 0)
            sig_rate = f"{sig_count / count * 100:.1f}%" if count > 0 else "0%"
            lines.append(f"{module:<20} {count:<10} {sig_count:<15} {sig_rate:<10}")
    
        # Calculate totals
        total_count = sum(module_counts.values())
        total_sig = sum(significant_counts.values())
        total_sig_rate = f"{total_sig / total_count * 100:.1f}%" if total_count > 0 else "0%"
    
        # Add totals row
        lines.append("-" * 60)
        lines.append(f"{'Total':<20} {total_count:<10} {total_sig:<15} {total_sig_rate:<10}")
    
        # Add Top Findings section if there are significant results
        if total_sig > 0:
            # Sort results by significance
            significant_results = []
            for result in self.results:
                for metric_name, value in result.metrics.items():
                    if isinstance(value, (int, float)) and 'significance' in metric_name.lower() and value >= self.significance_threshold:
                        significant_results.append((result, metric_name, value))
                        break
        
            # Sort by significance value (descending)
            significant_results.sort(key=lambda x: x[2], reverse=True)
        
            # Take top 10 or fewer
            top_n = min(10, len(significant_results))
        
            lines.extend([
                "",
                f"--- Top {top_n} Significant Findings ---",
                "",
                f"{'Trace ID':<20} {'Module':<15} {'Metric':<25} {'Value':<10} {'Time Range':<30}"
            ])
            lines.append("-" * 100)
        
            for result, metric_name, value in significant_results[:top_n]:
                time_range = f"{result.start_time} to {result.end_time}"
                lines.append(f"{result.trace_id:<20} {result.metadata.get('module', 'unknown'):<15} {metric_name:<25} {value:<10.3f} {time_range:<30}")
    
        # Write to file
        with open(report_path, 'w') as f:
            f.write('\n'.join(lines))
    
        print(f"Text report generated: {report_path}")
        return report_path

    def get_ki_phase_frequencies(self, sampling_rate):
        """
        Calculate expected frequencies related to Ki values
    
        Parameters:
        -----------
        sampling_rate : float
            Sampling rate in Hz
    
        Returns:
        --------
        dict
            Dictionary of Ki-related frequencies
        """
        nyquist = sampling_rate / 2
    
        # Calculate base frequencies
        ki_to_pi_ratio = self.ki_value / PI
        ki_rest_to_pi = KI_REST / PI
        ki_motion_to_pi = KI_MOTION / PI
    
        return {
            'ki_fundamental': sampling_rate / self.ki_value,
            'ki_half': sampling_rate / (self.ki_value / 2),
            'ki_double': sampling_rate / (self.ki_value * 2),
            'ki_pi_ratio': sampling_rate / ki_to_pi_ratio,
            'ki_golden_ratio': sampling_rate / (self.ki_value * GOLDEN_RATIO),
            'ki_rest_freq': sampling_rate / KI_REST,
            'ki_motion_freq': sampling_rate / KI_MOTION,
            'ki_alt_fundamental': sampling_rate / self.alternate_ki,
            'pi_fundamental': sampling_rate / PI
        }

    def estimate_resonance_probability(self, signal, sampling_rate):
        """
        Estimate the probability that a signal contains Ki-related resonances
    
        Parameters:
        -----------
        signal : numpy.ndarray
            The signal data
        sampling_rate : float
            Sampling rate in Hz
    
        Returns:
        --------
        float
            Probability estimate [0-1]
        dict
            Details of the estimate
        """
        # Get expected Ki frequencies
        ki_freqs = self.get_ki_phase_frequencies(sampling_rate)
    
        # Calculate the power spectrum
        f, pxx = signal.periodogram(signal, fs=sampling_rate)
    
        # Normalize power
        pxx_norm = pxx / np.sum(pxx)
    
        # Find peaks
        peak_indices = signal.find_peaks(pxx_norm, height=np.mean(pxx_norm) + np.std(pxx_norm))[0]
        peak_freqs = f[peak_indices]
        peak_powers = pxx_norm[peak_indices]
    
        # Check if peaks are near Ki-related frequencies
        tolerance = 0.05  # 5% tolerance
    
        ki_resonances = {}
        total_ki_power = 0
    
        for name, expected_freq in ki_freqs.items():
            # Skip frequencies beyond Nyquist
            if expected_freq >= sampling_rate / 2:
                continue
            
            # Find closest peak
            closest_idx = None
            min_diff = float('inf')
        
            for i, peak_freq in enumerate(peak_freqs):
                rel_diff = abs(peak_freq - expected_freq) / expected_freq
                if rel_diff < tolerance and rel_diff < min_diff:
                    min_diff = rel_diff
                    closest_idx = i
        
            if closest_idx is not None:
                ki_resonances[name] = {
                    'expected_freq': expected_freq,
                    'actual_freq': peak_freqs[closest_idx],
                    'relative_error': min_diff,
                    'power': peak_powers[closest_idx]
                }
                total_ki_power += peak_powers[closest_idx]
    
        # Calculate overall probability
        total_peak_power = np.sum(peak_powers)
        ki_probability = total_ki_power / total_peak_power if total_peak_power > 0 else 0
    
        # Adjust by number of matches
        match_ratio = len(ki_resonances) / len(ki_freqs)
    
        # Final probability estimate
        final_probability = ki_probability * match_ratio
    
        return final_probability, {
            'ki_resonances': ki_resonances,
            'total_ki_power': total_ki_power,
            'total_power': total_peak_power,
            'match_ratio': match_ratio
        }
    
    # Additional utility methods for the analyzer class

    def plot_ki_spectrogram(self, trace, processed_trace=None, output_path=None):
        """
        Generate a spectrogram highlighting Ki-related frequencies
    
        Parameters:
        -----------
        trace : obspy.Trace
            The trace to analyze
        processed_trace : obspy.Trace or None
            Preprocessed trace if available
        output_path : str or Path or None
            Path to save the plot (if None, display instead)
    
        Returns:
        --------
        matplotlib.figure.Figure
            The generated figure
        """
        import matplotlib.pyplot as plt
        from matplotlib.colors import LogNorm
    
        # Use processed trace if available
        data = processed_trace.data if processed_trace else trace.data
        sampling_rate = trace.stats.sampling_rate
    
        # Calculate spectrogram
        nperseg = min(1024, len(data) // 8)
        noverlap = nperseg // 2
    
        f, t, Sxx = signal.spectrogram(
            data, 
            fs=sampling_rate,
            nperseg=nperseg,
            noverlap=noverlap,
            scaling='spectrum'
        )
    
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # Plot spectrogram
        pcm = ax.pcolormesh(t, f, 10 * np.log10(Sxx), cmap='viridis', shading='gouraud')
    
        # Calculate Ki-related frequencies
        ki_freqs = self.get_ki_phase_frequencies(sampling_rate)
    
        # Filter to frequencies within range
        visible_freqs = {name: freq for name, freq in ki_freqs.items() if freq < sampling_rate/2}
    
        # Plot horizontal lines at Ki frequencies
        for name, freq in visible_freqs.items():
            if 0 < freq < f.max():
                ax.axhline(y=freq, color='r', linestyle='--', alpha=0.7, linewidth=1)
                ax.text(t.max() * 0.95, freq, name, color='white', 
                        backgroundcolor='red', alpha=0.7, fontsize=8)
    
        # Add colorbar and labels
        plt.colorbar(pcm, ax=ax, label='Power (dB)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_xlabel('Time (s)')
        ax.set_title(f'Spectrogram with Ki Frequencies - {trace.id}')
    
        # Set y-axis to log scale for better visualization
        ax.set_yscale('log')
    
        # Add grid
        ax.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.3)
    
        # Tight layout
        plt.tight_layout()
    
        # Save or show
        if output_path:
            plt.savefig(output_path, dpi=300)
            plt.close(fig)
    
        return fig

    def plot_resonance_significance(self, freqs, power, ki_resonances, output_path=None):
        """
        Plot spectrum with highlighted Ki resonances
    
        Parameters:
        -----------
        freqs : numpy.ndarray
            Frequency values
        power : numpy.ndarray
            Power spectrum values
        ki_resonances : dict
            Dictionary of identified Ki resonances
        output_path : str or Path or None
            Path to save the plot (if None, display instead)
    
        Returns:
        --------
        matplotlib.figure.Figure
            The generated figure
        """
        import matplotlib.pyplot as plt
    
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # Plot power spectrum
        ax.plot(freqs, power, 'b-', alpha=0.7, linewidth=1)
    
        # Highlight Ki resonances
        for name, info in ki_resonances.items():
            ax.axvline(x=info['expected_freq'], color='r', linestyle='--', alpha=0.5, linewidth=1)
        
            # Mark the actual peak
            if 'actual_freq' in info and 'power' in info:
                ax.plot(info['actual_freq'], info['power'], 'ro', markersize=5)
            
                # Add annotation
                ax.annotate(
                    name, 
                    xy=(info['actual_freq'], info['power']),
                    xytext=(10, 10),
                    textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2')
                )
    
        # Add labels
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Normalized Power')
        ax.set_title('Frequency Spectrum with Ki Resonances')
    
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.3)
    
        # Set y-axis to log scale for better visualization
        ax.set_yscale('log')
    
        # Tight layout
        plt.tight_layout()
    
        # Save or show
        if output_path:
            plt.savefig(output_path, dpi=300)
            plt.close(fig)
    
        return fig



# Command-line interface
def main():
    """Command-line interface for the Ki Resonance Analyzer"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze MSeed files for Ki-related resonance patterns')
    
    # Input options
    parser.add_argument('input', help='Input file or directory path')
    parser.add_argument('--pattern', default='*.mseed', help='File pattern to match (default: *.mseed)')
    
    # Analysis options
    parser.add_argument('--ki-value', type=float, default=KI_MOTION, 
                        help=f'Primary Ki value to analyze (default: {KI_MOTION})')
    parser.add_argument('--significance', type=float, default=2.0,
                        help='Significance threshold in standard deviations (default: 2.0)')
    parser.add_argument('--modules', nargs='+', default=None,
                        help='Specific analysis modules to run (default: all)')
    
    # Output options
    parser.add_argument('--output-dir', default=None, 
                        help='Directory for output files (default: ki_resonance_results)')
    parser.add_argument('--no-plots', action='store_true', 
                        help='Disable plot generation')
    parser.add_argument('--report-format', choices=['html', 'text'], default='html',
                        help='Report format (default: html)')
    
    # Parallel processing options
    parser.add_argument('--no-parallel', action='store_true',
                        help='Disable parallel processing')
    parser.add_argument('--max-workers', type=int, default=None,
                        help='Maximum number of parallel workers (default: CPU count)')
    
    # Additional modules
    parser.add_argument('--module-file', nargs='+', default=None,
                        help='Additional module files to load')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = KiResonanceAnalyzer(
        output_dir=args.output_dir,
        ki_value=args.ki_value,
        significance_threshold=args.significance
    )
    
    # Load additional modules if specified
    if args.module_file:
        for module_file in args.module_file:
            analyzer.load_module_file(module_file)
    
    # Run analysis
    input_path = Path(args.input)
    
    if input_path.is_file():
        print(f"Processing single file: {input_path}")
        analyzer.process_file(input_path, not args.no_plots, args.modules)
    elif input_path.is_dir():
        print(f"Processing directory: {input_path}")
        analyzer.process_directory(
            input_path,
            pattern=args.pattern,
            parallel=not args.no_parallel,
            max_workers=args.max_workers,
            save_plots=not args.no_plots,
            modules=args.modules
        )
    else:
        print(f"Error: Input path {input_path} does not exist")
        return 1
    
    # Save results
    analyzer.save_results()
    
    # Generate report
    analyzer.generate_report(output_format=args.report_format)
    
    print(f"Analysis complete. Processed {analyzer.processed_file_count} files with {len(analyzer.results)} results.")
    return 0

if __name__ == '__main__':
    sys.exit(main())