# Assuming you have the full pi_scanner_2 functions imported
import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio  # You'll need to install 'imageio'
import os

# MOCKING: This mocks loading a time series of masks
def load_mock_time_series_data():
    """Mocks loading a sequence of masks and times."""
    # In a real scenario, this would load files like 'mask_t1.png', 'mask_t2.png', etc.
    NUM_FRAMES = 10
    M_VALUES = np.linspace(2.8e7, 4.0e7, NUM_FRAMES) # e.g., 'm' values evolving over time
    
    # Simple mock: The basin is a single expanding circle for visualization
    RES = 500 # Smaller resolution for faster mock
    m_vals = np.linspace(-4e7, 4e7, RES)
    lam_vals = np.linspace(-4e7, 4e7, RES)
    M, L = np.meshgrid(m_vals, lam_vals)
    
    masks = []
    
    for i in range(NUM_FRAMES):
        # The radius R grows over time
        R_current = (i + 5) * 4e6 
        R_grid = np.sqrt(M**2 + L**2)
        mock_mask = (R_grid < R_current)
        masks.append(mock_mask)

    return masks, M_VALUES, m_vals, lam_vals

# ---------------------------------------------------------
# New function to generate frames
# ---------------------------------------------------------

def generate_time_series_frames(output_dir="gif_frames"):
    """
    Loads time-series data, analyzes each frame, and saves the overlay plot.
    """
    print("--- Generating GIF Frames ---")
    os.makedirs(output_dir, exist_ok=True)
    
    masks, m_values, m_coords, lam_coords = load_mock_time_series_data()
    frame_filenames = []
    
    for i, (mask, m_val) in enumerate(zip(masks, m_values)):
        time_label = f"m={m_val/1e6:.1f}M"
        frame_label = f"frame_{i:03d}"
        
        print(f"[{time_label}] Analyzing and plotting frame {i+1}/{len(masks)}...")
        
        # 1. Run Analysis (Replace this with the actual analyze_proton_basin call)
        # Note: analyze_proton_basin usually prints output and saves the plot.
        
        # MOCK PLOTTING: Create a plot to save as an image file
        fig, ax = plt.subplots()
        ax.imshow(mask, cmap='viridis', origin='lower', extent=[m_coords.min(), m_coords.max(), lam_coords.min(), lam_coords.max()])
        
        # MOCK: Plot a 'fitted' circle (e.g., for the expanding basin)
        circle = plt.Circle((0, 0), (i + 5) * 4e6, color='red', fill=False, linewidth=2, linestyle='--')
        ax.add_artist(circle)
        
        ax.set_title(f"Proton Basin Analysis: {time_label}")
        ax.set_xlabel("M coordinate")
        ax.set_ylabel("Λ coordinate")
        
        filename = os.path.join(output_dir, f"{frame_label}.png")
        plt.savefig(filename, dpi=100)
        plt.close(fig)
        frame_filenames.append(filename)
        
    return frame_filenames

# ---------------------------------------------------------
# New function to create the GIF
# ---------------------------------------------------------

def create_gif(frame_files, output_filename="basin_evolution.gif", duration_ms=200):
    """Stitches PNG frames into an animated GIF."""
    print(f"--- Creating GIF: {output_filename} ---")
    
    # Read the images
    images = [iio.imread(filename) for filename in frame_files]
    
    # Use imageio to write the GIF
    # 'duration' is in milliseconds (ms) per frame
    iio.imwrite(output_filename, images, duration=duration_ms, loop=0) # loop=0 means infinite loop
    
    print(f"Success! GIF saved as: {output_filename}")


if __name__ == "__main__":
    frame_files = generate_time_series_frames()
    
    if frame_files:
        create_gif(frame_files, duration_ms=300) # 300ms per frame