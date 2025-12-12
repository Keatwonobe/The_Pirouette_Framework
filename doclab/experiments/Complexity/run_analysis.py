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

# --- 1. Data Loading Functions ---

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
    """
    Loads the Powerball CSV and extracts a 1D time series of white balls.
    """
    print(f"Loading and processing {filename}...")
    try:
        df = pd.read_csv(filename)
        
        all_white_balls = []
        # The column name from your file is 'Winning Numbers'
        for num_str in df['Winning Numbers']:
            # '08 12 45 46 63 24' -> split -> ['08', '12', '45', '46', '63', '24']
            parts = num_str.split()
            # Take the first 5 (white balls) and convert to int
            white_balls = [int(p) for p in parts[:5]]
            all_white_balls.extend(white_balls)
            
        # Your experiment design implies a 1D time series, so we flatten all
        # white balls from all draws into one long sequence.
        return np.array(all_white_balls)
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return np.array([])

def normalize_anu_data(data):
    """Normalizes ANU uint16 data to the [1, 69] Powerball space."""
    if data.size == 0:
        return data
    print("Normalizing ANU data (uint16) to [1, 69] range...")
    # (data % 69) gives [0, 68]. Add 1 to get [1, 69].
    return (data % 69) + 1

# --- 2. Main Analysis ---

def run_all_analysis():
    """
    Loads all data, runs analysis, prints mode counts, and generates plots.
    """
    
    # --- Define our data sources and processing steps ---
    # This structure finds your files automatically.
    
    # Note: Using os.path.join for better cross-platform compatibility
    sources = {
        'Numpy PRNG': {
            'file': find_file(os.path.join('.', 'numpy_prng_*.txt')),
            'loader': load_txt_data,
            'normalizer': None
        },
        'Random.org': {
            'file': find_file(os.path.join('.', 'random_org_*.txt')),
            'loader': load_txt_data,
            'normalizer': None
        },
        'Powerball': {
            'file': find_file(os.path.join('.', 'Lottery_Powerball_Winning_Numbers*.csv')),
            'loader': load_powerball_data,
            'normalizer': None
        },
        'Mendeley QRNG': {
            'file': find_file(os.path.join('.', 'mendeley_qrng_*.txt')),
            'loader': load_txt_data,
            'normalizer': normalize_anu_data
        }
    }

    all_results = {}
    print("\n--- Starting Data Processing ---")

    for source_name, config in sources.items():
        if config['file'] is None:
            print(f"Skipping '{source_name}' (no data file found).")
            continue
        
        # 1. Load data
        seq_data = config['loader'](config['file'])
        
        # 2. Normalize (if needed)
        if config['normalizer']:
            seq_data = config['normalizer'](seq_data)
            
        if seq_data.size == 0:
            print(f"Skipping '{source_name}' (no data loaded).")
            continue

        print(f"Analyzing '{source_name}' ({len(seq_data)} data points)...")
        
        # 3. Run your experiment's windowing function
        # Using default window=128, hop=64
        rows = sos_window(seq_data)
        
        # 4. Run your experiment's labeling function
        labeled_rows = sos_label(rows)
        
        # --- FIX: Handle nested list structure ---
        # The DEBUG log shows sos_label is returning [ [(k,d,l), ...] ]
        # We need to extract the *inner* list.
        if labeled_rows and isinstance(labeled_rows[0], (list, tuple)):
            print(f"  (Note: Un-nesting results list. Found {len(labeled_rows[0])} items inside.)")
            all_results[source_name] = labeled_rows[0]
        else:
            all_results[source_name] = labeled_rows
        # --- END FIX ---
        
        print(f"Finished analyzing '{source_name}'.\n")

    if not all_results:
        print("No analysis could be run. Please check file paths and data.")
        return

    # --- 3. Mode Analysis (Text Output) ---
    print("\n--- Analysis of Modes ---")
    for source_name, results in all_results.items():
        print(f"\nSource: {source_name}")
        
        labels = []
        if not results:
            print("  No results to analyze.")
            continue

        # EAFP Pattern: Try dict-style access first, then fall back to tuple-style.
        # This is more robust than `isinstance` checks.
        try:
            # Try accessing data by key (for dicts, pandas.Series, etc.)
            labels = [item['label'] for item in results]
            print("  (Parsing results as dict-like objects)")
        except (TypeError, KeyError):
            # If that fails, try accessing by index (for tuples, lists)
            print("  (Dict-style access failed, trying tuple-style...)")
            try:
                labels = [item[2] for item in results]
                print("  (Parsing results as tuple-like objects)")
            except (TypeError, IndexError, KeyError) as e:
                # The KeyError check is for the pandas.Series[2] case
                print(f"  Error: Could not parse results structure. Skipping source. ({type(e).__name__}: {e})")
                continue
        
        total = len(labels)
        if total == 0:
            print("  No results to analyze.")
            continue
            
        counts = Counter(labels)
        print(f"  Total windows: {total}")
        for label_name, count in counts.most_common():
            percentage = (count / total) * 100
            print(f"  - {label_name}: {count} ({percentage:.1f}%)")

    # --- 4. Visualization (Pirouette Plane Plot) ---
    print("\n--- Generating Pirouette Plane Plot ---")
    
    # Define colors for each mode
    color_map = {
        "Weaver": "#1f77b4",     # Blue
        "Gladiator": "#ff7f0e",  # Orange
        "Vortex": "#d62728",     # Red
        "Drifter": "#9467bd",    # Purple
    }
    
    # Get the list of sources we actually have data for
    source_keys = list(all_results.keys())
    
    # Create a 2x2 subplot grid
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 15))
    fig.suptitle('Pirouette Plane Analysis: $\Delta P$ vs $|\kappa*|$ by Source', fontsize=20)
    
    # Flatten axes array for easy iteration
    axes_flat = axes.flatten()

    for i, source_name in enumerate(source_keys):
        ax = axes_flat[i]
        results = all_results[source_name]
        
        plot_data = []
        if not results:
            print(f"  No plot data to render for '{source_name}'.")
            ax.set_title(f"{source_name}\n(No data to plot)", fontsize=14)
            continue # Skip to the next subplot

        # --- DEBUGGING - Let's inspect the first item from sos_label ---
        print(f"  > DEBUG: First item from results for '{source_name}': {results[0]}")
        # --- END DEBUGGING ---

        # EAFP Pattern: Try dict-style access first, then fall back to tuple-style.
        try:
            # Try accessing data by key (for dicts, pandas.Series, etc.)
            plot_data = [(item['kappa'], item['dP'], item['label']) for item in results]
            print(f"  (Building plot data for '{source_name}' from dicts)")
        except (TypeError, KeyError):
            # If that fails, try accessing by index (for tuples, lists)
            print(f"  (Building plot data for '{source_name}' from tuples)")
            try:
                plot_data = [(item[0], item[1], item[2]) for item in results]
            except (TypeError, IndexError, KeyError) as e:
                # The KeyError check is for the pandas.Series[2] case
                print(f"    Error: Could not parse plot data for '{source_name}'. ({type(e).__name__}: {e})")
                print(f"    > This *strongly* implies 'sos_label' is not returning 3-element tuples (k, dP, label).")
                continue
            
        df = pd.DataFrame(plot_data, columns=['kappa', 'dP', 'label'])
        
        # Plot each mode separately to control color and legend
        for label_name, color in color_map.items():
            subset = df[df['label'] == label_name]
            if not subset.empty:
                ax.scatter(subset['kappa'], subset['dP'], 
                           c=color, label=label_name, 
                           alpha=0.6, s=10, edgecolors='none')
        
        ax.set_title(source_name, fontsize=14)
        ax.set_xlabel('$|\kappa*|$ (Curvature)', fontsize=10)
        ax.set_ylabel('$\Delta P$ (Power Change)', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # Set reasonable limits if data is clustered
        if not df.empty:
            k_med = df['kappa'].median()
            dp_med = df['dP'].median()
            ax.set_xlim(left=0, right=max(1.0, k_med * 4)) # kappa is abs()
            ax.set_ylim(bottom=min(-1.0, dp_med * 3), top=max(1.0, dp_med * 3))

    # Hide any unused subplots
    for i in range(len(source_keys), len(axes_flat)):
        axes_flat[i].set_visible(False)
        
    # Create a single shared legend
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', title="Modes", fontsize=12)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the figure
    output_filename = 'pirouette_plane_analysis.png'
    plt.savefig(output_filename)
    print(f"Plot saved as '{output_filename}'")
    
    # Optionally, display the plot
    # plt.show()


# --- Run the script ---
if __name__ == "__main__":
    run_all_analysis()





