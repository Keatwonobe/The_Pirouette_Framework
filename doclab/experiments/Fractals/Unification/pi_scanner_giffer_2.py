import numpy as np
import imageio.v3 as iio
import os
import matplotlib.pyplot as plt
# You will likely need to import more from pi_scanner_3.py here (e.g., the force laws)

# ------------------------------------------------------------------------
# 🎯 STEP 1: Replace this function with the actual logic from pi_scanner_3.py
# ------------------------------------------------------------------------

def compute_and_save_frame(dynamic_param, filename):
    """
    MOCK: This function MUST be replaced by your real function from pi_scanner_3.py.
    
    Your real function needs to:
    1. Update the global or class-level dynamic parameter (e.g., TWIST = dynamic_param).
    2. Run the simulation/computation to generate the helicity map array.
    3. Use matplotlib to plot the map.
    4. Call plt.savefig(filename) to save the frame.
    5. Call plt.close('all') to free up memory before the next loop.
    """
    
    # --- MOCK IMPLEMENTATION (shows how the function should behave) ---
    RES = 512
    m_vals = np.linspace(-4, 4, RES)
    M, L = np.meshgrid(m_vals, m_vals)
    
    # Example: A spiral structure evolving with the parameter
    R = np.sqrt(M**2 + L**2)
    Angle = np.arctan2(L, M)
    
    helicity_map = np.sin(R * 5 + Angle * dynamic_param / 4.0) * np.exp(-R/4) 
    
    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(helicity_map, origin='lower', cmap='hsv', 
                   extent=[m_vals.min(), m_vals.max(), m_vals.min(), m_vals.max()])
    
    ax.set_title(f"Helicity Map: Parameter = {dynamic_param:.2f}")
    plt.colorbar(im, ax=ax, label="Helicity Field Value")
    fig.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"Generated frame: {filename}")
# ------------------------------------------------------------------------


def create_animated_helicity_gif(output_dir="helicity_frames"):
    """
    Generates time-series frames by varying a simulation parameter 
    and creates the final GIF.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the parameter evolution for the animation
    # (e.g., varying the TWIST parameter from 3.0 to 5.0 over 20 frames)
    DYNAMIC_PARAMETERS = np.linspace(3.0, 5.0, 20)
    
    frame_filenames = []
    print(f"--- Generating {len(DYNAMIC_PARAMETERS)} Helicity Map Frames ---")

    for i, param_val in enumerate(DYNAMIC_PARAMETERS):
        frame_label = f"frame_{i:03d}"
        filename = os.path.join(output_dir, f"{frame_label}.png")
        
        # Call the core function (which is the real pi_scanner_3.py logic)
        compute_and_save_frame(param_val, filename)
        frame_filenames.append(filename)
        
    # Stitch frames into a GIF
    print(f"\n--- Stitching {len(frame_filenames)} Frames into GIF ---")
    output_gif = "helicity_field_evolution.gif"
    
    images = [iio.imread(filename) for filename in frame_filenames]
    
    # Duration is in milliseconds (ms) per frame (150ms = about 6.7 fps)
    iio.imwrite(output_gif, images, duration=150, loop=0) 
    
    print(f"Success! Animated GIF saved as: {output_gif}")


if __name__ == "__main__":
    create_animated_helicity_gif()