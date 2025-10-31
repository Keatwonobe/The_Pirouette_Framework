import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import time

# --- Default Parameters (An interesting set from your simulations) ---
# This set produces a complex, filamentous structure.
DEFAULT_PARAMS = {
    "a": -1.9, 
    "b": 1.6, 
    "c": 0.7, 
    "d": -1.8
}

def run_compass_simulation(params, points=20_000_000, width=2048, height=2048, filename="cosmic_compass.png"):
    """
    Generates and saves a Cosmic Compass visualization based on a given set of parameters.

    Args:
        params (dict): A dictionary with keys 'a', 'b', 'c', 'd'.
        points (int): Number of points to calculate for detail.
        width (int): Output image width in pixels.
        height (int): Output image height in pixels.
        filename (str): The name of the output image file.
    """
    a, b, c, d = params['a'], params['b'], params['c'], params['d']
    print(f"--- Running simulation for {filename} with params {params} ---")
    start_time = time.time()

    # Create a 2D array (canvas) to store the density of points
    canvas = np.zeros((width, height))
    
    # Initialize coordinates
    x, y = 0.0, 0.0
    
    # Pre-calculate scaling factors to map coordinates to pixels
    scale_x = width / 6.0
    scale_y = height / 6.0
    
    # --- The Core Simulation Loop ---
    for i in range(points):
        # Print a simple progress indicator every million points
        if i % 1_000_000 == 0 and i > 0:
            print(f"...processed {i // 1_000_000}M points")

        # Clifford Attractor equations
        x_new = np.sin(a * y) + c * np.cos(a * x)
        y_new = np.sin(b * x) + d * np.cos(b * y)
        x, y = x_new, y_new
        
        # Map the continuous coordinates to discrete pixel locations
        pixel_x = int(x * scale_x + width / 2)
        pixel_y = int(y * scale_y + height / 2)
        
        # Increment the density count if the point is on the canvas
        if 0 <= pixel_x < width and 0 <= pixel_y < height:
            canvas[pixel_y, pixel_x] += 1
    
    # --- Visualization ---
    print("Generation complete. Plotting image...")
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Using LogNorm brings out the faint, intricate details of the "wake"
    ax.imshow(canvas, cmap='hot', norm=LogNorm(vmin=1, vmax=canvas.max()))
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig) # Close the figure to free up memory
    
    end_time = time.time()
    print(f"--- Finished. Image saved as '{filename}'. Total time: {end_time - start_time:.2f} seconds ---\n")


# --- How to Use: Define and Run Your Tests ---
if __name__ == "__main__":
    
    # Test 1: The default, complex parameter set
    #run_compass_simulation(DEFAULT_PARAMS, filename="compass_default.png")
    
    # Test 2: A more symmetrical, crystalline structure from another of your files
    crystalline_params = {"a": 1.7, "b": 1.7, "c": 0.6, "d": 1.2}
    run_compass_simulation(crystalline_params, filename="compass_crystalline.png")
    
    # Test 3: An example of a chaotic, gaseous-looking structure
    gaseous_params = {"a": -1.2, "b": -1.7, "c": -1.8, "d": -0.7}
    run_compass_simulation(gaseous_params, filename="compass_gaseous.png")