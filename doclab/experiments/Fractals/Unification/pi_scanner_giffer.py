import numpy as np
import imageio.v3 as iio
import os
import matplotlib.pyplot as plt

# --- 0. PASTE PI_SCANNER_3.PY CONTENT HERE ---
# Paste the ENTIRE content of your pi_scanner_3.py file here.
# Make sure the plotting logic in that file saves the image (plt.savefig) 
# instead of just displaying it (plt.show()).

# For the sake of demonstration, we'll mock the required function:
def compute_and_save_frame(twist_value, filename):
    """MOCK: This replaces the full simulation from pi_scanner_3.py"""
    RES = 512
    m_vals = np.linspace(-4, 4, RES)
    M, L = np.meshgrid(m_vals, m_vals)
    
    # Create a dynamic helicity-like map that changes with twist_value
    # Example: A spiral structure rotating and shrinking slightly
    R = np.sqrt(M**2 + L**2)
    Angle = np.arctan2(L, M)
    
    # The 'helicity' field depends on the twist value
    helicity_map = np.sin(R * 5 + Angle * twist_value / 4.0) * np.exp(-R/4) 
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Use the color map (e.g., 'twilight' or 'hsv') appropriate for helicity/phase
    im = ax.imshow(helicity_map, origin='lower', cmap='hsv', 
                   extent=[m_vals.min(), m_vals.max(), m_vals.min(), m_vals.max()])
    
    ax.set_title(f"Helicity Map: Twist = {twist_value:.2f}")
    plt.colorbar(im, ax=ax, label="Helicity Field Value")
    fig.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"Generated frame: {filename}")
# --- END MOCK ---


def create_animated_helicity_gif(output_dir="helicity_frames"):
    """
    Generates time-series frames by varying a simulation parameter 
    (like TWIST) and creates a GIF.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the time steps / parameter evolution
    # This simulates a changing dynamic over 20 frames
    TWIST_VALUES = np.linspace(3.0, 5.0, 20)
    frame_filenames = []
    
    print(f"--- Generating {len(TWIST_VALUES)} Helicity Map Frames ---")

    for i, twist_val in enumerate(TWIST_VALUES):
        frame_label = f"frame_{i:03d}"
        filename = os.path.join(output_dir, f"{frame_label}.png")
        
        # 1. Compute and save the map for this 'time step'
        compute_and_save_frame(twist_val, filename)
        frame_filenames.append(filename)
        
    # 2. Stitch frames into a GIF
    print(f"\n--- Stitching {len(frame_filenames)} Frames into GIF ---")
    output_gif = "helicity_evolution.gif"
    
    images = [iio.imread(filename) for filename in frame_filenames]
    
    # Duration is in milliseconds (ms) per frame (40ms = 25fps)
    iio.imwrite(output_gif, images, duration=150, loop=0) 
    
    print(f"Success! Animated GIF saved as: {output_gif}")
    print("Don't forget to delete the 'helicity_frames' directory when done!")


if __name__ == "__main__":
    # Ensure you have the 'imageio' library installed: pip install imageio
    create_animated_helicity_gif()