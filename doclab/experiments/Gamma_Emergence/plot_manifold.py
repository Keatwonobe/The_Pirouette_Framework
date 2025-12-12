# File: plot_manifold.py
#
# This agent loads the *single, massive* manifold_data.json
# created by `manifold_generator.py` and plots the "rugs."
#
# It will generate 3 plots:
# 1. The "Low Load" Manifold (Standing Wave)
# 2. The "High Load" Manifold (Engaged Wave)
# 3. The "Difference" Manifold (Shifting Wave)

import os, re, json, pathlib, warnings, argparse
import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Error: matplotlib is required for this script.")
    print("Please install it with: pip install matplotlib")
    exit(1)

def plot_manifold(json_path, out_dir):
    """
    Loads the manifold JSON and generates 3 heatmap plots.
    """
    print(f"▶ Plotting Manifold from {json_path.name}...")
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ! Failed to load {json_path.name}: {e}")
        return

    # Extract data
    try:
        time_pts = data['time_points_sec']
        triad_labels = data['triad_labels']
        manifold_low = np.array(data['manifold_low_load'])
        manifold_high = np.array(data['manifold_high_load'])
        manifold_diff = manifold_high - manifold_low
        
        subject = data.get('subject', 'NA')
        task = data.get('task', 'NA')
    except KeyError as e:
        print(f"  ! File is missing required data key: {e}")
        return
    except Exception as e:
        print(f"  ! Error processing data: {e}")
        return
        
    print(f"  ...Manifold dimensions: {len(triad_labels)} triads x {len(time_pts)} time points")
    
    # --- Plotting Function ---
    def create_plot(data_matrix, title, cmap, out_name, vmin=None, vmax=None):
        plt.figure(figsize=(15, 10))
        
        # Use imshow for the heatmap
        # We set aspect='auto' to create the "rug" shape
        plt.imshow(data_matrix, aspect='auto', cmap=cmap, 
                   origin='lower', # Put (0,0) at bottom-left
                   extent=[time_pts[0], time_pts[-1], -0.5, len(triad_labels)-0.5],
                   vmin=vmin, vmax=vmax) # Add color limits
        
        plt.colorbar(label="TPCI Value" if "Difference" not in title else "TPCI Difference (High - Low)")
        
        # We only label every Nth triad so the Y-axis isn't a mess
        step = max(1, len(triad_labels) // 20) # Show ~20 labels max
        plt.yticks(ticks=np.arange(len(triad_labels))[::step], 
                   labels=triad_labels[::step])
        
        plt.xlabel("Time in Trial (seconds)", fontsize=12)
        plt.ylabel("Triad (f1 - f2 - f3)", fontsize=12)
        plt.title(f"{title}\nSubject: {subject}, Task: {task}", fontsize=16, weight='bold')
        
        # Add a vertical line for stimulus onset (t=0)
        plt.axvline(x=0, color='white', linestyle='--', linewidth=2, alpha=0.7)
        
        plt.tight_layout()
        
        # --- Save the Plot ---
        out_path = out_dir / out_name
        plt.savefig(out_path, dpi=150)
        plt.close()
        print(f"  ✓ Saved plot: {out_name}")

    # --- Create the 3 Plots ---
    
    # 1. Low Load (The "Standing Wave")
    create_plot(manifold_low, 
                "Resonant Manifold: LOW Load (Standing Wave)", 
                'viridis', 
                f"manifold_sub-{subject}_task-{task}_01_low_load.png")
                
    # 2. High Load (The "Engaged Wave")
    create_plot(manifold_high, 
                "Resonant Manifold: HIGH Load (Engaged Wave)", 
                'viridis', 
                f"manifold_sub-{subject}_task-{task}_02_high_load.png")

    # 3. Difference (The "Shifting Wave")
    # We use a diverging colormap here and set symmetric color limits
    diff_abs_max = np.max(np.abs(manifold_diff))
    create_plot(manifold_diff, 
                "Resonant Manifold: DIFFERENCE (High - Low) (Shifting Wave)", 
                'RdBu_r', 
                f"manifold_sub-{subject}_task-{task}_03_difference.png",
                vmin=-diff_abs_max, vmax=diff_abs_max)


def main():
    ap = argparse.ArgumentParser(description="Plotter for Resonant Manifold 'X-ray' data")
    
    ap.add_argument("--json-path", required=True,
                    help="Path to the *single* manifold_data.json file from manifold_generator.py")
    
    ap.add_argument("--outdir", required=True, 
                    help="Directory to save the output .png files.")

    args = ap.parse_args()

    # --- Setup Paths ---
    json_path = pathlib.Path(args.json_path)
    if not json_path.exists():
        print(f"Error: JSON file not found: {json_path}")
        return
        
    out_dir_path = pathlib.Path(args.outdir)
    out_dir_path.mkdir(parents=True, exist_ok=True)
    print(f"Saving plots to: {out_dir_path.resolve()}")

    # --- Process the file ---
    plot_manifold(json_path, out_dir_path)
    
    print("✓ Manifold plotting complete.")

if __name__ == "__main__":
    main()