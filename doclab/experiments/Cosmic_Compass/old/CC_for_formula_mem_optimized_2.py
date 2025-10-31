import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import time
import os
import numba # Import the Numba library

# --- Default Parameters ---
DEFAULT_PARAMS = {
    "a": -1.9, 
    "b": 1.6, 
    "c": 0.7, 
    "d": -1.8
}

@numba.jit(nopython=True, fastmath=True)
def generate_points(canvas, points, params, x_start, y_start):
    """
    A Numba-JIT compiled function to generate points with extreme speed.
    This function operates directly on the canvas array.
    """
    # <--- FIX: Unpack the 'params' tuple directly. ---
    # Numba can't use string keys, so we unpack the tuple we passed in.
    a, b, c, d = params
    
    # Get canvas dimensions and pre-calculate scaling factors
    height, width = canvas.shape
    scale_x = width / 6.0
    scale_y = height / 6.0
    offset_x = width / 2
    offset_y = height / 2
    
    # Initialize coordinates
    x, y = x_start, y_start

    # This loop will be converted to lightning-fast machine code by Numba
    for i in range(points):
        x_new = np.sin(a * y) + c * np.cos(a * x)
        y_new = np.sin(b * x) + d * np.cos(b * y)
        x, y = x_new, y_new
        
        pixel_x = int(x * scale_x + offset_x)
        pixel_y = int(y * scale_y + offset_y)
        
        if 0 <= pixel_x < width and 0 <= pixel_y < height:
            canvas[pixel_y, pixel_x] += 1
            
    # Return the final coordinates to use as a starting point for the next run
    return x, y


def run_compass_simulation(
    params, 
    total_points=20_000_000, 
    width=2048, 
    height=2048, 
    checkpoint_interval=2_000_000,
    filename="cosmic_compass.png"
):
    """
    Main function to manage the simulation, now using Numba for the core calculation.
    """
    # Numba works with simple data types, so we pass params as a tuple
    param_tuple = (params['a'], params['b'], params['c'], params['d'])
    
    print(f"--- Running simulation for {filename} with params {params} ---")
    start_time = time.time()
    
    # --- Checkpointing Logic (Improved) ---
    checkpoint_file = f"{os.path.splitext(filename)[0]}_checkpoint.npy"
    meta_file = f"{checkpoint_file}.meta.txt" # For storing points_done and last coords
    points_done = 0
    x, y = 0.0, 0.0

    try:
        canvas = np.load(checkpoint_file)
        with open(meta_file, "r") as f:
            points_done, x, y = [float(val) for val in f.read().split(',')]
            points_done = int(points_done)
        print(f"Resuming from checkpoint. {points_done // 1_000_000}M points already processed.")
    except FileNotFoundError:
        print("No checkpoint found. Starting a new simulation.")
        canvas = np.zeros((width, height), dtype=np.uint32)
        
    # --- Main Calculation Loop ---
    points_remaining = total_points - points_done
    if points_remaining <= 0:
        print("Simulation already complete.")
    else:
        # Loop in chunks to allow for checkpointing
        while points_done < total_points:
            points_to_run = min(checkpoint_interval, total_points - points_done)
            
            print(f"Running calculation for {points_to_run / 1_000_000:.1f}M points...")
            
            # Call the super-fast Numba function
            x, y = generate_points(canvas, points_to_run, param_tuple, x, y)
            
            points_done += points_to_run
            print(f"...processed {points_done // 1_000_000}M / {total_points // 1_000_000}M total points. Saving checkpoint...")
            
            # Save progress
            np.save(checkpoint_file, canvas)
            with open(meta_file, "w") as f:
                f.write(f"{points_done},{x},{y}")
    
    # --- Visualization ---
    print("Generation complete. Plotting image...")
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 12))
    
    ax.imshow(canvas, cmap='hot', norm=LogNorm(vmin=1, vmax=canvas.max()))
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    
    # --- Clean up checkpoint files on successful completion ---
    if os.path.exists(checkpoint_file): os.remove(checkpoint_file)
    if os.path.exists(meta_file): os.remove(meta_file)
        
    end_time = time.time()
    print(f"--- Finished. Image saved as '{filename}'. Total time: {end_time - start_time:.2f} seconds ---\n")

# --- Main Execution Block ---
if __name__ == "__main__":
    # Test 1
    #run_compass_simulation(DEFAULT_PARAMS, filename="compass_default.png")
    
    # Test 2
    crystalline_params = {"a": 1.7, "b": 1.7, "c": 0.6, "d": 1.2}
    run_compass_simulation(crystalline_params, filename="compass_crystalline.png")
    
    # Test 3
    gaseous_params = {"a": -1.2, "b": -1.7, "c": -1.8, "d": -0.7}
    run_compass_simulation(gaseous_params, filename="compass_gaseous.png")