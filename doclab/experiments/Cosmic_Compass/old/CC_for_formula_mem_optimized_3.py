import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import time
import os
import numba

# --- Default Parameters ---
DEFAULT_PARAMS = {"a": -1.9, "b": 1.6, "c": 0.7, "d": -1.8}

@numba.jit(nopython=True, fastmath=True)
def generate_points(canvas, value_canvas, mode, points, params, x_start, y_start):
    """
    Numba-JIT function, now with different modes for data collection.
    """
    a, b, c, d = params
    height, width = canvas.shape
    scale_x, scale_y = width / 6.0, height / 6.0
    offset_x, offset_y = width / 2, height / 2
    x, y = x_start, y_start

    for i in range(points):
        x_new = np.sin(a * y) + c * np.cos(a * x)
        y_new = np.sin(b * x) + d * np.cos(b * y)
        
        pixel_x = int(x_new * scale_x + offset_x)
        pixel_y = int(y_new * scale_y + offset_y)
        
        if 0 <= pixel_x < width and 0 <= pixel_y < height:
            canvas[pixel_y, pixel_x] += 1
            
            # --- NEW: Record different data based on the mode ---
            if mode == 1: # Time Mode
                # Only record the first time a pixel is hit
                if value_canvas[pixel_y, pixel_x] == 0:
                    value_canvas[pixel_y, pixel_x] = i + 1 # Use i+1 to avoid 0
            
            elif mode == 2: # Flow Mode
                # Calculate angle of movement (vector)
                angle = np.arctan2(y_new - y, x_new - x)
                value_canvas[pixel_y, pixel_x] = angle

        x, y = x_new, y_new
            
    return x, y

def run_compass_simulation(
    params, 
    mode='density', # <--- NEW: 'density', 'time', or 'flow'
    total_points=20_000_000, 
    width=2048, 
    height=2048, 
    checkpoint_interval=2_000_000,
    filename="cosmic_compass.png"
):
    """
    Main function with selectable visualization modes.
    """
    mode_map = {'density': 0, 'time': 1, 'flow': 2}
    if mode not in mode_map:
        raise ValueError("Mode must be 'density', 'time', or 'flow'")
    mode_int = mode_map[mode]

    param_tuple = (params['a'], params['b'], params['c'], params['d'])
    print(f"--- Running simulation for {filename} (Mode: {mode}) ---")
    
    # --- Checkpointing Setup ---
    # Note: Checkpoints are mode-specific now
    base_name = os.path.splitext(filename)[0]
    checkpoint_file = f"{base_name}_checkpoint.npy"
    value_checkpoint_file = f"{base_name}_values.npy" # For time/flow data
    meta_file = f"{base_name}.meta.txt"
    
    points_done, x, y = 0, 0.0, 0.0
    try:
        canvas = np.load(checkpoint_file)
        value_canvas = np.load(value_checkpoint_file)
        with open(meta_file, "r") as f:
            points_done, x, y = [float(val) for val in f.read().split(',')]
            points_done = int(points_done)
        print(f"Resuming from checkpoint...")
    except FileNotFoundError:
        print("No checkpoint found. Starting new simulation.")
        canvas = np.zeros((width, height), dtype=np.uint32)
        # Use float32 for value canvas to store angles or large iteration counts
        value_canvas = np.zeros((width, height), dtype=np.float32)

    # --- Main Calculation Loop ---
    if points_done < total_points:
        # Pass the integer representation of the mode to Numba
        x, y = generate_points(canvas, value_canvas, mode_int, total_points - points_done, param_tuple, x, y)
        np.save(checkpoint_file, canvas)
        np.save(value_checkpoint_file, value_canvas)
        with open(meta_file, "w") as f:
            f.write(f"{total_points},{x},{y}")
    
    # --- Visualization ---
    print("Generation complete. Plotting image...")
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Replace 0s with NaN (Not a Number) to make them transparent
    value_canvas[value_canvas == 0] = np.nan
    
    if mode == 'density':
        ax.imshow(canvas, cmap='hot', norm=LogNorm(vmin=1, vmax=canvas.max()))
    elif mode == 'time':
        ax.imshow(value_canvas, cmap='viridis')
    elif mode == 'flow':
        ax.imshow(value_canvas, cmap='hsv') # HSV is a cyclical colormap perfect for angles
    
    ax.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

# --- How to Use ---
if __name__ == "__main__":
    # Generate the standard density plot
    run_compass_simulation(DEFAULT_PARAMS, mode='density', filename="compass_default_density.png")
    
    # NOW, reveal the temporal skeleton
    run_compass_simulation(DEFAULT_PARAMS, mode='time', filename="compass_default_time.png")
    
    # AND, reveal the underlying flow
    run_compass_simulation(DEFAULT_PARAMS, mode='flow', filename="compass_default_flow.png")