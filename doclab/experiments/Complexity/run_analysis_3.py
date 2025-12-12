import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from collections import Counter
import os
from scipy import signal  # <-- NEW IMPORT NEEDED FOR TEST 1

# --- Import your custom analysis functions ---
# This requires 'closure_testbed.py' to be in the same directory
try:
    from closure_testbed import sos_window, sos_label
except ImportError:
    print("Error: 'closure_testbed.py' not found.")
    print("Please make sure 'closure_testbed.py' is in the same directory as this script.")
    # We don't exit() here, as some stubs might still work
    # Define placeholder functions if the import fails
    def sos_window(data):
        print("Warning: Using placeholder 'sos_window'.")
        return [data[i:i+10] for i in range(0, len(data), 10) if len(data[i:i+10]) == 10]
    
    def sos_label(rows):
        print("Warning: Using placeholder 'sos_label'.")
        # Return dummy (kappa, dP, label)
        labels = ["Weaver", "Gladiator", "Vortex", "Drifter"]
        return [(np.random.rand() * 0.5, np.random.rand() - 0.5, labels[i % 4]) for i in range(len(rows))]

# --- 1. Data Loading & Helper Functions ---

def find_file(pattern):
    """Finds the first file matching a glob pattern."""
    files = glob.glob(pattern)
    if not files:
        print(f"Warning: No file found matching '{pattern}'.")
        return None
    if len(files) > 1:
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

# --- 2. NEW: Ablation & Test Functions ---

# --- Test 4: Adversarial Sequence Generators ---
def generate_arithmetic(size=10000):
    """Generates a simple arithmetic progression."""
    print("Generating 'Synth: Arithmetic' data...")
    return np.arange(1, size + 1)

def generate_sawtooth(size=10000, period=50):
    """Generates a sawtooth wave."""
    print("Generating 'Synth: Sawtooth' data...")
    return np.array([i % period for i in range(size)])

def generate_repeating(size=10000, pattern=(1, 2, 3, 4)):
    """Generates a repeating sequence."""
    print("Generating 'Synth: Repeating' data...")
    return np.array([pattern[i % len(pattern)] for i in range(size)])

# --- Test 3: Distribution-Preserving Shuffle (Implemented) ---
def sos_window_shuffled(data):
    """
    Runs the original sos_window, then shuffles the data *inside* each window.
    This tests if temporal order *within* the window matters.
    """
    print("  (Applying Test 3: Intra-Window Shuffle)")
    # 1. Get original windows
    original_windows = sos_window(data)
    
    # 2. Shuffle inside each window
    shuffled_windows = []
    rng = np.random.default_rng()
    for window_tuple in original_windows:
        # Assuming sos_window returns (kappa, dP) and we need to re-run
        # NOTE: This implementation was wrong. We must shuffle *before* labeling.
        # This function needs to re-implement sos_window logic.
        print("  (Applying Test 3: Intra-Window Shuffle)")
        
        # --- Copying sos_window logic ---
        seq = np.asarray(data, float)
        win=128
        hop=64
        fs=1.0
        f_center=1.0
        
        z = signal.hilbert(seq - seq.mean())
        dz = np.gradient(z) * fs
        P = np.abs(z)**2
        
        wins = [(s, s+win) for s in range(0, len(seq)-win+1, hop)]
        k0 = max(1, int(0.05*len(wins)))
        P0 = np.median([P[s:e].mean() for (s, e) in wins[:k0]]) + 1e-12
        # --- End sos_window setup ---
        
        rows = []
        rng = np.random.default_rng()
        for (s, e) in wins:
            # Get original windowed data
            z_w, dz_w = z[s:e], dz[s:e]
            
            # --- SHUFFLE ---
            # Shuffle the indices and apply to both z and dz
            # to break temporal order but keep (z, dz) pairs intact
            indices = np.arange(len(z_w))
            rng.shuffle(indices)
            z_w_shuffled = z_w[indices]
            dz_w_shuffled = dz_w[indices]
            # --- END SHUFFLE ---
            
            # Run transform on *shuffled* data
            re = np.real(np.vdot(z_w_shuffled, z_w_shuffled))
            im = np.imag(np.vdot(dz_w_shuffled, z_w_shuffled))
            kappa = abs(-im / (2*np.pi*f_center*(re+1e-12) + 1e-12))
            
            # dP is non-temporal, so shuffle doesn't matter, but we recalculate
            P_w_shuffled = np.abs(z_w_shuffled)**2
            dP = (P_w_shuffled.mean() - P0) / P0
            
            rows.append((kappa, dP))
        return rows
        
    return shuffled_windows

# --- Test 1: Window Ablation (IMPLEMENTED) ---

def sos_window_fixed(data, win=128, fs=1.0, f_center=1.0):
    """
    Test 1a: Replaces sos_window with fixed-length, *non-overlapping* windows.
    (This copies logic from closure_testbed.sos_window)
    """
    print(f"  (Applying Test 1a: Fixed Windows, win={win})")
    
    # --- sos_window logic ---
    seq = np.asarray(data, float)
    hop = win  # <--- The ONLY change: hop size == window size
    
    z = signal.hilbert(seq - seq.mean())
    dz = np.gradient(z) * fs
    P = np.abs(z)**2

    wins = [(s, s+win) for s in range(0, len(seq)-win+1, hop)] # <-- hop=win
    if not wins:
        print("    Warning: No full windows generated for fixed window test.")
        return []
        
    k0 = max(1, int(0.05*len(wins)))
    P0 = np.median([P[s:e].mean() for (s, e) in wins[:k0]]) + 1e-12

    rows = []
    for (s, e) in wins:
        z_w, dz_w = z[s:e], dz[s:e]
        re = np.real(np.vdot(z_w, z_w))
        im = np.imag(np.vdot(dz_w, z_w))
        kappa = abs(-im / (2*np.pi*f_center*(re+1e-12) + 1e-12))
        dP = (P[s:e].mean() - P0) / P0
        rows.append((kappa, dP))
    return rows

def sos_window_random(data, min_win=50, max_win=200, fs=1.0, f_center=1.0):
    """
    Test 1c: Replaces sos_window with non-overlapping windows of random size.
    (This copies logic from closure_testbed.sos_window)
    """
    print(f"  (Applying Test 1c: Random Windows, min={min_win}, max={max_win})")
    
    # --- sos_window logic ---
    seq = np.asarray(data, float)
    z = signal.hilbert(seq - seq.mean())
    dz = np.gradient(z) * fs
    P = np.abs(z)**2
    
    # --- Generate random, non-overlapping windows ---
    wins = []
    s = 0
    while s < len(seq):
        win_size = np.random.randint(min_win, max_win + 1)
        e = s + win_size
        if e >= len(seq):
            break
        wins.append((s, e))
        s = e # Move to end of last window
        
    if not wins:
        print("    Warning: No full windows generated for random window test.")
        return []
    
    k0 = max(1, int(0.05*len(wins)))
    P0 = np.median([P[s:e].mean() for (s, e) in wins[:k0]]) + 1e-12

    rows = []
    for (s, e) in wins:
        z_w, dz_w = z[s:e], dz[s:e]
        re = np.real(np.vdot(z_w, z_w))
        im = np.imag(np.vdot(dz_w, z_w))
        kappa = abs(-im / (2*np.pi*f_center*(re+1e-12) + 1e-12))
        dP = (P[s:e].mean() - P0) / P0
        rows.append((kappa, dP))
    return rows

# --- Test 2: Labeler Permutation (IMPLEMENTED) ---
def sos_label_permuted_5bin(rows):
    """
    Test 2: Re-runs the (kappa, dP) calculation but uses new
    thresholds to create 5 bins instead of 4.
    (This copies logic from closure_testbed.sos_label)
    """
    print("  (Applying Test 2: 5-Bin Labeler)")
    if not rows:
        return [], {}

    # --- sos_label logic ---
    km = np.array([r[0] for r in rows])
    dp = np.array([r[1] for r in rows])
    
    # --- NEW 5-BIN THRESHOLDS ---
    th_k_low = np.quantile(km, 0.60)
    th_k_high = np.quantile(km, 0.85)
    th_P_low = np.quantile(dp, 0.35)
    th_P_high = np.quantile(dp, 0.65)
    
    labels = []
    for k, d in rows:
        # --- NEW 5-BIN LOGIC ---
        if d >= th_P_high and th_k_low <= k < th_k_high:
            lab = "Weaver"      # High Power, Mid Curvature
        elif d >= th_P_high and k >= th_k_high:
            lab = "Gladiator"   # High Power, High Curvature
        elif d < th_P_low and k >= th_k_high:
            lab = "Vortex"      # Low/Neg Power, High Curvature
        elif th_P_low <= d < th_P_high:
            lab = "Nomad"       # Mid Power (new category)
        else:
            lab = "Drifter"     # Catch-all (mostly Low Curvature)
            
        labels.append((k, d, lab))
        
    thresholds = dict(
        th_k_low=th_k_low, th_k_high=th_k_high, 
        th_P_low=th_P_low, th_P_high=th_P_high
    )
    return labels, thresholds


# --- 3. Main Analysis ---

def run_all_analysis():
    """
    Main function to load all data, run analysis, 
    print stats, and generate plots.
    """
    all_data_raw = {}
    all_results = {} # This will now be: all_results[source_name][strategy_name]
    
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
        
    # 4. QRNG Ablation Files
    qrng_sources = {
        'QRNG (Quantile)': r'.\mendeley_qrng_quantile.txt',
        'QRNG (Uniform)': r'.\mendeley_qrng_uniform.txt',
        'QRNG (Shuffled)': r'.\mendeley_qrng_shuffled.txt',
        'QRNG (High-Pass)': r'.\mendeley_qrng_highpass.txt',
        'Closure-Sig': r'.\closure_rng_10000.txt'
    }
    for name, pattern in qrng_sources.items():
        qrng_file = find_file(pattern)
        if qrng_file:
            all_data_raw[name] = load_txt_data(qrng_file)

    # 5. NEW: Test 4 - Adversarial/Synthetic Data
    all_data_raw['Synth: Arithmetic'] = generate_arithmetic(20000)
    all_data_raw['Synth: Sawtooth p=50'] = generate_sawtooth(20000, period=50)
    all_data_raw['Synth: Repeating 1-4'] = generate_repeating(20000, pattern=(1, 2, 3, 4))
    
    # --- NEW: Define Analysis Strategies ---
    # This dictionary maps a test name to the (window_func, label_func) pair.
    # NOTE: "Test 1b (Overlap)" was removed, as "Original" already is overlapping.
    analysis_strategies = {
        "Original": (sos_window, sos_label),
        "Test 1a (Fixed)": (sos_window_fixed, sos_label),
        "Test 1c (Random)": (sos_window_random, sos_label),
        "Test 2 (5-Bin)": (sos_window, sos_label_permuted_5bin),
        "Test 3 (Shuffled)": (sos_window_shuffled, sos_label)
    }

    # --- Run Analysis on Loaded Data ---
    for source_name, data in all_data_raw.items():
        if data.size == 0:
            print(f"Skipping '{source_name}' (no data loaded).")
            continue
        
        print(f"\n--- Processing Source: {source_name} ({data.size} data points) ---")
        all_results[source_name] = {} # Create sub-dict for this source
        
        for strategy_name, (window_func, label_func) in analysis_strategies.items():
            print(f"  Running Strategy: {strategy_name}...")
            
            try:
                # 1. Run windowing
                windowed_rows = window_func(data)
                
                # 2. Run labeling
                labeled_rows = label_func(windowed_rows)
                
                # 3. Fix for nested list results
                if (isinstance(labeled_rows, (list, tuple)) and 
                    len(labeled_rows) > 0 and 
                    isinstance(labeled_rows[0], (list, tuple))):
                    print("    (Fixing nested list result from sos_label)")
                    all_results[source_name][strategy_name] = labeled_rows[0]
                else:
                    all_results[source_name][strategy_name] = labeled_rows
                
                print(f"    Finished '{strategy_name}'.")
            
            except NotImplementedError as e:
                print(f"    SKIPPED: {e}")
            except Exception as e:
                print(f"    ERROR running '{strategy_name}' on '{source_name}': {type(e).__name__}: {e}")
                all_results[source_name][strategy_name] = [] # Store empty result on error

        
    if not all_results:
        print("No analysis could be run. Please check file paths and data.")
        return

    # --- 3. Mode Analysis (Text Output) ---
    print("\n--- Analysis of Modes & Statistics ---")
    for source_name, strategies in all_results.items():
        for strategy_name, results in strategies.items():
            
            print(f"\nSource: {source_name}  |  Strategy: {strategy_name}")
            
            labels = []
            if not results:
                print("  No results to analyze.")
                continue

            # EAFP Pattern: Try dict-style access first, then fall back to tuple-style.
            try:
                labels = [item['label'] for item in results]
            except (TypeError, KeyError):
                try:
                    labels = [item[2] for item in results]
                except (TypeError, IndexError, KeyError) as e:
                    print(f"  Error: Could not parse results structure. Skipping. ({type(e).__name__}: {e})")
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
            # TODO: Update cycle counter for 5-bin test
            if strategy_name == "Test 2 (5-Bin)":
                print("  Cycles:        (Cycle counting not implemented for 5-bin test)")
            else:
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
    print("\n--- Generating Pirouette Plane Plots (One per Source) ---")
    
    # Define a consistent color map for modes
    color_map = {
        "Weaver": "#1f77b4",    # blue
        "Gladiator": "#ff7f0e", # orange
        "Vortex": "#d62728",    # red
        "Drifter": "#9467bd",   # purple
        "Nomad": "#2ca02c",     # green (NEW for Test 2)
        "Other": "#8c564b"      # brown
    }

    
    # --- NEW: Loop and create ONE PLOT PER DATA SOURCE ---
    for source_name, strategies in all_results.items():
        
        # Filter out strategies that weren't successfully run
        strategy_keys = sorted([k for k, v in strategies.items() if v])
        
        if not strategy_keys:
            print(f"No results to plot for '{source_name}'.")
            continue

        # --- Create a dynamic subplot grid ---
        n_strategies = len(strategy_keys)
        n_cols = 3  # Set to 3 columns
        n_rows = int(np.ceil(n_strategies / float(n_cols)))
        
        fig, axes = plt.subplots(n_rows, n_cols, 
                                 figsize=(n_cols * 5.5, n_rows * 4.5), 
                                 squeeze=False, # Always return 2D array for axes
                                 constrained_layout=True) 
        axes_flat = axes.flatten()
        
        fig.suptitle(f"Pirouette Plane Analysis for: {source_name}", fontsize=20, fontweight='bold')
        
        # Keep track of legend items
        legend_handles = {}
        
        for i, strategy_name in enumerate(strategy_keys):
            ax = axes_flat[i]
            results = strategies[strategy_name]
            
            # Build DataFrame for plotting, using robust access
            plot_data = []
            try: # dict-style
                plot_data = [(item['kappa'], item['dP'], item['label']) for item in results]
            except (TypeError, KeyError): # tuple-style
                try:
                    plot_data = [(item[0], item[1], item[2]) for item in results]
                except (TypeError, IndexError, KeyError) as e:
                    print(f"  (Building plot data for '{strategy_name}'... from tuples)")
                    print(f"    Error: Could not parse plot data. ({type(e).__name__}: {e})")
                    continue
            
            if not plot_data:
                # This check is now redundant given the filter, but good to keep
                print(f"  No plot data for '{strategy_name}'. Skipping subplot.")
                ax.set_title(strategy_name, fontsize=14, fontweight='bold')
                ax.text(0.5, 0.5, "No data or Test not implemented", ha='center', va='center', fontsize=12, alpha=0.5)
                ax.set_xlabel('$|\\kappa*|$ (Curvature)', fontsize=10)
                ax.set_ylabel('$\Delta P$ (Power Change)', fontsize=10)
                ax.grid(True, linestyle='--', alpha=0.5)
                continue

            df = pd.DataFrame(plot_data, columns=['kappa', 'dP', 'label'])
            
            # --- Plot mean dP line ---
            if not df.empty:
                mean_dp = df['dP'].mean()
                ax.axhline(mean_dp, color='black', linestyle='--', linewidth=1.0, alpha=0.7,
                           label=f'Mean ΔP ({mean_dp:+.3f})')
            
            # Plot each mode separately to control color and legend
            all_labels_in_plot = df['label'].unique()
            for label_name in all_labels_in_plot:
                color = color_map.get(label_name, "#7f7f7f") # Default to grey
                subset = df[df['label'] == label_name]
                if not subset.empty:
                    h = ax.scatter(subset['kappa'], subset['dP'], 
                                  c=color, label=label_name, 
                                  alpha=0.6, s=10, edgecolors='none')
                    if label_name not in legend_handles:
                        legend_handles[label_name] = h
            
            ax.set_title(strategy_name, fontsize=14, fontweight='bold')
            ax.set_xlabel('$|\\kappa*|$ (Curvature)', fontsize=10)
            ax.set_ylabel('$\Delta P$ (Power Change)', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(loc='upper right', fontsize='small') # Per-plot legend for mean line
            
            # Set reasonable, robust limits
            if not df.empty:
                # Use 99th quantile for more robust outlier handling
                k_right = max(0.5, np.quantile(df[df['kappa'] < np.inf]['kappa'], 0.99) * 1.2)
                dp_abs_max = max(0.5, np.quantile(np.abs(df['dP']), 0.99) * 1.2)
                
                ax.set_xlim(left=-0.02, right=k_right) # Start just before 0
                ax.set_ylim(bottom=-dp_abs_max, top=dp_abs_max)

        # Hide any unused subplots
        for i in range(len(strategy_keys), len(axes_flat)):
            axes_flat[i].set_visible(False)
            
        # Create a single shared legend for modes
        fig.legend(legend_handles.values(), legend_handles.keys(), 
                   loc='outside upper right', title="Modes", fontsize=12)
        
        # Save the final plot
        # --- CRASH FIX APPLIED HERE ---
        safe_source_name = source_name.replace(":", "").replace(" ", "_").replace("=", "_")
        output_plot_file = f'pirouette_plane_{safe_source_name}.png'
        plt.savefig(output_plot_file, dpi=150)
        print(f"\nPlot for '{source_name}' saved as '{output_plot_file}'")
        plt.close(fig) # Close the figure to save memory

if __name__ == "__main__":
    run_all_analysis()