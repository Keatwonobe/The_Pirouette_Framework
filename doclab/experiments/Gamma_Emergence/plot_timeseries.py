# File: plot_timeseries.py
#
# This script loads the JSON output from `triad_timeseries.py`
# and uses matplotlib to plot the time-series ("the moving shape")
# for High vs. Low load, saving the result as a PNG.

import os, re, json, pathlib, warnings, argparse
import glob

# We'll try to import matplotlib, but if it's not installed,
# we'll give a helpful error message.
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Error: matplotlib is required for this script.")
    print("Please install it with: pip install matplotlib")
    exit(1)

def plot_single_file(json_path, out_dir, out_num): # Add out_num here
    """
    Loads a single time-series JSON and generates a plot.
    """
    print(f"▶ Plotting {json_path.name}...")
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ! Failed to load {json_path.name}: {e}")
        return

    # Extract data
    t = data.get('time_points_sec')
    low_series = data.get('tpci_low_load_series')
    high_series = data.get('tpci_high_load_series')
    
    if not t or not low_series or not high_series:
        print(f"  ! File {json_path.name} is missing required data.")
        return

    # Extract metadata for the plot
    triad = data.get('triad', ['?','?','?'])
    subject = data.get('subject', 'NA')
    task = data.get('task', 'NA')
    n_low = data.get('n_epochs_low', '?')
    n_high = data.get('n_epochs_high', '?')
    
    triad_str = f"{triad[0]}-{triad[1]}-{triad[2]}"
    
    # --- Create the Plot ---
    plt.figure(figsize=(12, 7))
    
    # Plot the two lines
    plt.plot(t, low_series, label=f"Low Load (n={n_low})", color='#007ACC', linewidth=2.5, alpha=0.8)
    plt.plot(t, high_series, label=f"High Load (n={n_high})", color='#D62728', linewidth=2.5, alpha=0.8)
    
    # Fill the area between them
    plt.fill_between(t, low_series, high_series, 
                     where=[h > l for h, l in zip(high_series, low_series)], 
                     color='#D62728', alpha=0.2, interpolate=True, label='High > Low')
    
    plt.fill_between(t, low_series, high_series, 
                     where=[h <= l for h, l in zip(high_series, low_series)], 
                     color='#007ACC', alpha=0.2, interpolate=True, label='Low > High')

    # --- Style the Plot ---
    plt.xlabel("Time in Trial (seconds)", fontsize=12)
    plt.ylabel("Triadic Phase Coupling (TPCI)", fontsize=12)
    
    title = f"Transient TPCI for Triad {triad_str}\nSubject: {subject}, Task: {task}"
    plt.title(title, fontsize=16, weight='bold')
    
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Add a vertical line for stimulus onset (t=0)
    plt.axvline(x=0, color='black', linestyle='--', linewidth=1.5, label='Stimulus Onset')
    
    # Set reasonable y-limits
    all_vals = low_series + high_series
    min_val = min(all_vals) - 0.02
    max_val = max(all_vals) + 0.02
    plt.ylim(min_val, max_val)
    
    plt.xlim(min(t), max(t))
    plt.tight_layout()

    # --- Save the Plot ---
    out_name = out_name = f"{json_path.stem}_{out_num}.png"
    out_path = out_dir / out_name
    
    plt.savefig(out_path, dpi=150)
    plt.close()
    
    print(f"  ✓ Plot saved to {out_path.name}")


def main():
    ap = argparse.ArgumentParser(description="Plotter for Triadic Time-Series (triad_timeseries.py) results")
    
    # --- Input Args ---
    ap.add_argument("--json-path", default=None,
                    help="Path to a *single* timeseries_...json file.")
    ap.add_argument("--json-dir", default=None,
                   help="Path to a *directory* containing timeseries_...json files.")
    
    # --- Output Arg ---
    ap.add_argument("--outdir", required=True, 
                    help="Directory to save the output .png files.")

    args = ap.parse_args()

    # --- Find files ---
    json_files = []
    if args.json_path:
        json_files.append(pathlib.Path(args.json_path))
    elif args.json_dir:
        json_dir = pathlib.Path(args.json_dir)
        if not json_dir.is_dir():
            print(f"Error: --json-dir path is not a valid directory: {json_dir}")
            return
        json_files = sorted(list(json_dir.rglob("timeseries_*.json")))
    
    if not json_files:
        print("No JSON files found to plot.")
        return

    # --- Setup Output Directory ---
    out_dir_path = pathlib.Path(args.outdir)
    out_dir_path.mkdir(parents=True, exist_ok=True)
    print(f"Saving plots to: {out_dir_path.resolve()}")

    # --- Process each file ---
    for out_num, f_path in enumerate(json_files):
        plot_single_file(f_path, out_dir_path, out_num) # Pass the number in
        
    print("✓ Plotting complete.")

if __name__ == "__main__":
    main()