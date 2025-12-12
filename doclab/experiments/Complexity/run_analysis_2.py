import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from collections import Counter
import os

# --- Import your custom analysis functions ---
# This requires 'closure_testbed.py' to be in the same directory
try:
    from closure_testbed import sos_window, sos_label
except ImportError:
    print("Error: 'closure_testbed.py' not found.")
    print("Please make sure 'closure_testbed.py' is in the same directory as this script.")
    exit()

# --- 1. Data Loading & Helper Functions ---

def find_file(pattern):
    """Finds the first file matching a glob pattern."""
    files = glob.glob(pattern)
    if not files:
        print(f"Warning: No file found matching '{pattern}'.")
        return None
    
    # Check for multiple files and return the most recent one if they have timestamps
    if len(files) > 1:
        # Simple string sort on timestamp should get the latest
        files.sort()
        print(f"Multiple files found for '{pattern}', using '{files[-1]}'")
        return files[-1]
        
    return files[0]

def load_txt_data(filename):
    """Loads a .txt file with one number per line."""
    print(f"Loading {filename}...")
    try:
        data = np.loadtxt(filename, dtype=int)
        return data
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return np.array([])

def load_powerball_data(filename):
    """Loads and processes the Powerball CSV file."""
    print(f"Loading and processing {filename}...")
    try:
        df = pd.read_csv(filename)
        
        # Extract the first 5 numbers from "Winning Numbers"
        # Assumes format "08 12 45 46 63 24"
        all_numbers = []
        for row in df['Winning Numbers']:
            numbers = row.split(' ')[:5] # Get first 5
            all_numbers.extend([int(n) for n in numbers])
            
        print(f"  Extracted {len(all_numbers)} white balls.")
        return np.array(all_numbers)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return np.array([])
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return np.array([])

# --- Reviewer's Cycle Counting Function ---
def count_wgvd_cycles(labels, order=("Weaver", "Gladiator", "Vortex", "Drifter")):
    """Counts the number of completed W->G->V->D cycles in a label sequence."""
    idx = 0
    cycles = 0
    for label in labels:
        if label == order[idx]:
            idx += 1
            if idx == len(order):
                cycles += 1
                idx = 0
    return cycles

# --- 2. Main Analysis ---

def run_all_analysis():
    """
    Main function to load all data, run analysis, 
    print stats, and generate plots.
    """
    all_data_raw = {}
    all_results = {}
    
    print("\n--- Starting Data Processing ---")
    
    # --- Load Data Sources ---
    
    # 1. Numpy PRNG
    numpy_file = find_file(r'.\numpy_prng_*.txt')
    if numpy_file:
        all_data_raw['Numpy PRNG'] = load_txt_data(numpy_file)
        
    # 2. Random.org
    random_org_file = find_file(r'.\random_org_*.txt')
    if random_org_file:
        all_data_raw['Random.org'] = load_txt_data(random_org_file)
        
    # 3. Powerball
    powerball_file = find_file(r'.\Lottery_Powerball*.csv')
    if powerball_file:
        all_data_raw['Powerball'] = load_powerball_data(powerball_file)
        
    # 4. QRNG Ablation Files (NEW)
    qrng_sources = {
        'QRNG (Quantile)': r'.\mendeley_qrng_quantile.txt',
        'QRNG (Uniform)': r'.\mendeley_qrng_uniform.txt',
        'QRNG (Shuffled)': r'.\mendeley_qrng_shuffled.txt',
        'QRNG (High-Pass)': r'.\mendeley_qrng_highpass.txt',
        'Closure-Sig': r'.\closure_rng_10000.txt'
    }

    found_ablation_files = False
    for name, pattern in qrng_sources.items():
        qrng_file = find_file(pattern)
        if qrng_file:
            all_data_raw[name] = load_txt_data(qrng_file)
            found_ablation_files = True
    
    if not found_ablation_files:
        print("Warning: No Mendeley QRNG ablation files found.")
        print("  > Run 'convert_mendeley_data.py' to generate them.")


    # --- Run Analysis on Loaded Data ---
    for source_name, data in all_data_raw.items():
        if data.size == 0:
            print(f"Skipping '{source_name}' (no data loaded).")
            continue
            
        print(f"Analyzing '{source_name}' ({data.size} data points)...")
        # 1. Run windowing
        windowed_rows = sos_window(data)
        
        # 2. Run labeling
        labeled_rows = sos_label(windowed_rows)
        
        # 3. Fix for nested list results
        if (isinstance(labeled_rows, (list, tuple)) and 
            len(labeled_rows) > 0 and 
            isinstance(labeled_rows[0], (list, tuple))):
            print("  (Fixing nested list result from sos_label)")
            all_results[source_name] = labeled_rows[0]
        else:
            all_results[source_name] = labeled_rows
            
        print(f"Finished analyzing '{source_name}'.")
        
    if not all_results:
        print("No analysis could be run. Please check file paths and data.")
        return

    # --- 3. Mode Analysis (Text Output) ---
    print("\n--- Analysis of Modes & Statistics ---")
    for source_name, results in all_results.items():
        print(f"\nSource: {source_name}")
        
        labels = []
        if not results:
            print("  No results to analyze.")
            continue

        # EAFP Pattern: Try dict-style access first, then fall back to tuple-style.
        try:
            # Try accessing data by key (for dicts, pandas.Series, etc.)
            labels = [item['label'] for item in results]
        except (TypeError, KeyError):
            # If that fails, try accessing by index (for tuples, lists)
            try:
                labels = [item[2] for item in results]
            except (TypeError, IndexError, KeyError) as e:
                print(f"  Error: Could not parse results structure. Skipping source. ({type(e).__name__}: {e})")
                continue
        
        total = len(labels)
        if total == 0:
            print("  No results to analyze.")
            continue
            
        # --- Mode Percentages ---
        counts = Counter(labels)
        print(f"  Mode Counts:   Total windows: {total}")
        for label_name, count in counts.most_common():
            percentage = (count / total) * 100
            print(f"                 - {label_name}: {count} ({percentage:.1f}%)")
            
        # --- Cycle Counting ---
        cycles = count_wgvd_cycles(labels)
        print(f"  Cycles:        (W→G→V→D): {cycles}")
        
        # --- Quantitative Stats ---
        plot_data = []
        try: # dict-style
            plot_data = [(item['kappa'], item['dP']) for item in results]
        except (TypeError, KeyError): # tuple-style
            try:
                plot_data = [(item[0], item[1]) for item in results]
            except (TypeError, IndexError, KeyError):
                pass 
        
        if plot_data:
            df_stats = pd.DataFrame(plot_data, columns=['kappa', 'dP'])
            print(f"  Stats:         ΔP̄={df_stats.dP.mean():+.3f}  |κ*|̄={df_stats.kappa.mean():.3f}  σΔP={df_stats.dP.std():.3f}")


    # --- 4. Visualization (Pirouette Plane Plot) ---
    print("\n--- Generating Pirouette Plane Plot ---")
    
    source_keys = sorted(list(all_results.keys())) # Sort keys for consistent plot order
    if not source_keys:
        print("No results to plot.")
        return

    # --- Create a dynamic subplot grid ---
    n_sources = len(source_keys)
    n_cols = 3  # Set to 3 columns
    n_rows = int(np.ceil(n_sources / float(n_cols)))
    
    fig, axes = plt.subplots(n_rows, n_cols, 
                             figsize=(n_cols * 5.5, n_rows * 4.5), 
                             squeeze=False, # Always return 2D array for axes
                             constrained_layout=True) 
    axes_flat = axes.flatten()
    
    # Define a consistent color map for modes
    color_map = {
        "Weaver": "#1f77b4",    # blue
        "Gladiator": "#ff7f0e", # orange
        "Vortex": "#d62728",    # red
        "Drifter": "#9467bd",   # purple
        "Other": "#8c564b"      # brown
    }
    
    # Keep track of legend items
    legend_handles = {}
    
    for i, source_name in enumerate(source_keys):
        ax = axes_flat[i]
        results = all_results[source_name]
        
        # Build DataFrame for plotting, using robust access
        plot_data = []
        try: # dict-style
            plot_data = [(item['kappa'], item['dP'], item['label']) for item in results]
        except (TypeError, KeyError): # tuple-style
            try:
                plot_data = [(item[0], item[1], item[2]) for item in results]
            except (TypeError, IndexError, KeyError) as e:
                print(f"  (Building plot data for '{source_name}'... from tuples)")
                print(f"    Error: Could not parse plot data for '{source_name}'. ({type(e).__name__}: {e})")
                continue
        
        if not plot_data:
            print(f"  No plot data for '{source_name}'. Skipping subplot.")
            ax.set_title(source_name, fontsize=14, fontweight='bold')
            ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=18, alpha=0.5)
            continue

        df = pd.DataFrame(plot_data, columns=['kappa', 'dP', 'label'])
        
        # --- Plot mean dP line ---
        if not df.empty:
            mean_dp = df['dP'].mean()
            ax.axhline(mean_dp, color='black', linestyle='--', linewidth=1.0, alpha=0.7,
                       label=f'Mean ΔP ({mean_dp:+.3f})')
        
        # Plot each mode separately to control color and legend
        for label_name, color in color_map.items():
            subset = df[df['label'] == label_name]
            if not subset.empty:
                h = ax.scatter(subset['kappa'], subset['dP'], 
                              c=color, label=label_name, 
                              alpha=0.6, s=10, edgecolors='none')
                if label_name not in legend_handles:
                    legend_handles[label_name] = h
        
        ax.set_title(source_name, fontsize=14, fontweight='bold')
        ax.set_xlabel('$|\\kappa*|$ (Curvature)', fontsize=10)
        ax.set_ylabel('$\Delta P$ (Power Change)', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc='upper right', fontsize='small') # Per-plot legend for mean line
        
        # Set reasonable, robust limits
        if not df.empty:
            k_right = max(0.5, np.quantile(df['kappa'], 0.98) * 1.5)
            dp_abs_max = max(0.5, np.quantile(np.abs(df['dP']), 0.98) * 1.5)
            
            ax.set_xlim(left=-0.02, right=k_right) # Start just before 0
            ax.set_ylim(bottom=-dp_abs_max, top=dp_abs_max)

    # Hide any unused subplots
    for i in range(len(source_keys), len(axes_flat)):
        axes_flat[i].set_visible(False)
        
    # Create a single shared legend for modes
    fig.legend(legend_handles.values(), legend_handles.keys(), 
               loc='outside upper right', title="Modes", fontsize=12)
    
    # Save the final plot
    output_plot_file = 'pirouette_plane_analysis.png'
    plt.savefig(output_plot_file, dpi=150)
    print(f"\nPlot saved as '{output_plot_file}'")

if __name__ == "__main__":
    run_all_analysis()

