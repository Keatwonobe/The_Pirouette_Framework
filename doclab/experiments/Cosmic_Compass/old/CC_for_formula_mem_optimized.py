import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import time
import os # <--- NEW: Needed for checking if a file exists

# --- Default Parameters ---
DEFAULT_PARAMS = {
    "a": -1.9, 
    "b": 1.6, 
    "c": 0.7, 
    "d": -1.8
}

def run_compass_simulation(
    params, 
    total_points=20_000_000, 
    width=2048, 
    height=2048, 
    batch_size=100_000, # <--- NEW: Process points in chunks for efficiency
    checkpoint_interval=2_000_000, # <--- NEW: Save progress every 2M points
    filename="cosmic_compass.png"
):
    """
    Generates and saves a Cosmic Compass visualization with improved memory management,
    performance, and checkpointing.
    """
    a, b, c, d = params['a'], params['b'], params['c'], params['d']
    print(f"--- Running simulation for {filename} with params {params} ---")
    start_time = time.time()
    
    # --- NEW: Checkpointing and Canvas Initialization ---
    checkpoint_file = f"{os.path.splitext(filename)[0]}_checkpoint.npy"
    start_point = 0
    
    try:
        # Try to load a previous checkpoint
        print(f"Attempting to load checkpoint from '{checkpoint_file}'...")
        canvas = np.load(checkpoint_file)
        # Assuming each checkpoint is a multiple of the interval
        start_point = (canvas.sum() // checkpoint_interval) * checkpoint_interval
        # We need to refine the start point based on actual points calculated
        # A simple way is to just resume from a known interval, but for this case
        # we'll just track iterations. Let's adjust the logic slightly.
        # We will track points processed in a separate variable.
        with open(f"{checkpoint_file}.meta", "r") as f:
             start_point = int(f.read())
        print(f"Resuming from {start_point / 1_000_000:.1f}M points.")
    except FileNotFoundError:
        # If no checkpoint, start from scratch
        print("No checkpoint found. Starting a new simulation.")
        # <--- KEY MEMORY IMPROVEMENT ---
        # Use unsigned 32-bit integers instead of 64-bit floats.
        # This cuts the memory usage of this array by 50%!
        canvas = np.zeros((width, height), dtype=np.uint32) 
        
    # Initialize coordinates
    x, y = 0.0, 0.0

    # Pre-calculate scaling factors
    scale_x = width / 6.0
    scale_y = height / 6.0
    offset_x = width / 2
    offset_y = height / 2

    # --- The Core Simulation Loop (Now Batch-Processed) ---
    print(f"Starting calculation from point {start_point} to {total_points}.")
    for i in range(start_point, total_points, batch_size):
        
        # Create arrays for the batch
        x_batch = np.zeros(batch_size)
        y_batch = np.zeros(batch_size)
        x_batch[0], y_batch[0] = x, y # Start batch with last point from previous batch
        
        # Generate the points for this batch
        for j in range(batch_size - 1):
            x_batch[j+1] = np.sin(a * y_batch[j]) + c * np.cos(a * x_batch[j])
            y_batch[j+1] = np.sin(b * x_batch[j]) + d * np.cos(b * y_batch[j])
        
        # Keep the last point for the next batch
        x, y = x_batch[-1], y_batch[-1]

        # --- Vectorized Mapping to Pixels ---
        # Perform calculations on the entire batch at once. This is MUCH faster.
        pixel_x = (x_batch * scale_x + offset_x).astype(np.int32)
        pixel_y = (y_batch * scale_y + offset_y).astype(np.int32)
        
        # Create a mask for points that are within the canvas bounds
        valid_mask = (0 <= pixel_x) & (pixel_x < width) & (0 <= pixel_y) & (pixel_y < height)
        
        # Use the mask to select only valid coordinates
        valid_x = pixel_x[valid_mask]
        valid_y = pixel_y[valid_mask]
        
        # Use np.add.at to efficiently increment the counts for valid pixels.
        # This is a safe way to handle cases where multiple points map to the same pixel.
        np.add.at(canvas, (valid_y, valid_x), 1)
        
        # --- NEW: Checkpointing Logic ---
        points_processed = i + batch_size
        if points_processed % checkpoint_interval == 0 and points_processed > 0:
            print(f"...processed {points_processed // 1_000_000}M points. Saving checkpoint...")
            np.save(checkpoint_file, canvas)
            with open(f"{checkpoint_file}.meta", "w") as f:
                f.write(str(points_processed))
    
    # --- Visualization ---
    print("Generation complete. Plotting image...")
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 12))
    
    ax.imshow(canvas, cmap='hot', norm=LogNorm(vmin=1, vmax=canvas.max()))
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    
    # --- NEW: Clean up checkpoint files on successful completion ---
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)
    if os.path.exists(f"{checkpoint_file}.meta"):
        os.remove(f"{checkpoint_file}.meta")
        
    end_time = time.time()
    print(f"--- Finished. Image saved as '{filename}'. Total time: {end_time - start_time:.2f} seconds ---\n")


# --- How to Use ---
if __name__ == "__main__":
    
    # Test 1: The default, complex parameter set
    #run_compass_simulation(DEFAULT_PARAMS, filename="compass_default.png")
    
    # Test 2: A more symmetrical, crystalline structure
    crystalline_params = {"a": 1.7, "b": 1.7, "c": 0.6, "d": 1.2}
    run_compass_simulation(crystalline_params, filename="compass_crystalline.png")
    
    # Test 3: An example of a chaotic, gaseous-looking structure
    gaseous_params = {"a": -1.2, "b": -1.7, "c": -1.8, "d": -0.7}
    run_compass_simulation(gaseous_params, filename="compass_gaseous.png")