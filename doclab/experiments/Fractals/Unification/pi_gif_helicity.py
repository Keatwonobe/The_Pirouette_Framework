import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time
from PIL import Image

# =========================================================
#  HOLOGRAPHIC PROJECTION GIF GENERATOR
#  (Based on Method 3 from pi_scanner_3.py)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_holography.gif"
FRAMES = 60               # Number of frames for one full rotation
RES = 800                 # Resolution (Square)
DURATION = 80             # ms per frame

# Viewport (Matches the HOLO section of pi_scanner_3)
# We expand it slightly to -1.0 to 1.0 to see the full "Triangle" formation
M_MIN, M_MAX = -0.00000005, 0.00000005
L_MIN, L_MAX = -0.00000005, 0.00000005

# External Quark "Sources" (Initial Positions from scanner_3)
# These will be rotated during the animation
SRC_M = np.array([-10.0, 10.0, 0.0])
SRC_L = np.array([5.0, 5.0, -10.0])


# --- PHYSICS KERNEL (METHOD 3 BACKBONE) ---

@njit(parallel=True)
def compute_holographic_frame(m_vals, l_vals, src_m, src_l):
    """
    Computes the interference intensity |Psi|^2 for a specific 
    configuration of external quarks.
    """
    h = len(l_vals)
    w = len(m_vals)
    intensity_map = np.zeros((h, w), dtype=np.float64)
    
    # Pre-compute wavevectors (k) for the sources based on their distance
    # k_i = 2 * pi / L_i
    # Note: In the scanner_3 logic, k changes as the source moves further out.
    # Since we are just rotating here, distance stays same, so k stays same.
    k_vec = np.zeros(3)
    for i in range(3):
        dist = np.sqrt(src_m[i]**2 + src_l[i]**2)
        if dist == 0:
            k_vec[i] = 0
        else:
            k_vec[i] = (2 * np.pi) / dist

    # Parallel loop over the grid
    for i in prange(h):
        y = l_vals[i]
        for j in range(w):
            x = m_vals[j]
            
            # Sum complex waves
            psi_real = 0.0
            psi_imag = 0.0
            
            for q in range(3):
                # Distance from pixel (x,y) to source (xm, yl)
                dx = x - src_m[q]
                dy = y - src_l[q]
                r = np.sqrt(dx*dx + dy*dy)
                
                # Avoid singularity
                if r < 1e-9: r = 1e-9
                
                # Wave: (e^(i k r)) / r
                # Real: cos(kr)/r, Imag: sin(kr)/r
                phase = k_vec[q] * r
                inv_r = 1.0 / r
                
                psi_real += np.cos(phase) * inv_r
                psi_imag += np.sin(phase) * inv_r
            
            # |Psi|^2 = Real^2 + Imag^2
            intensity_map[i, j] = psi_real**2 + psi_imag**2
            
    return intensity_map

# --- HELPER: ROTATION ---

def rotate_sources(m_arr, l_arr, theta_rad):
    """Rotates the external source coordinates around (0,0)."""
    cos_t = np.cos(theta_rad)
    sin_t = np.sin(theta_rad)
    
    m_new = m_arr * cos_t - l_arr * sin_t
    l_new = m_arr * sin_t + l_arr * cos_t
    return m_new, l_new

# --- MAIN GENERATOR ---

def generate_hologram_gif():
    print(f"--- ⚛️ HOLOGRAPHIC PROJECTION GIF GENERATOR ---")
    print(f"Resolution: {RES}x{RES}")
    print(f"Frames: {FRAMES}")
    
    # Generate Grid
    m_vals = np.linspace(M_MIN, M_MAX, RES)
    l_vals = np.linspace(L_MIN, L_MAX, RES)
    
    # Pre-compile JIT
    print("Compiling Interference Engine...")
    compute_holographic_frame(m_vals[0:10], l_vals[0:10], SRC_M, SRC_L)
    
    frames_buffer = []
    start_time = time.time()
    
    # Setup Colormap (Magma or Inferno looks very 'energy field')
    cmap = plt.get_cmap('inferno')
    
    print("rendering frames...")
    
    for f in range(FRAMES):
        # Calculate rotation angle for this frame (0 to 2pi)
        angle = 2 * np.pi * f / FRAMES
        
        # Rotate the external quarks
        curr_m, curr_l = rotate_sources(SRC_M, SRC_L, angle)
        
        # Compute the field
        # Note: We compute the RAW intensity
        raw_intensity = compute_holographic_frame(m_vals, l_vals, curr_m, curr_l)
        
        # --- Normalization for Visuals ---
        # Holographic patterns have high dynamic range. 
        # We take a power (e.g., 0.4) to compress the peaks so we can see the faint fringes.
        # Then we normalize 0-1.
        
        vis_data = np.power(raw_intensity, 0.4) 
        v_min, v_max = vis_data.min(), vis_data.max()
        if v_max > v_min:
            vis_data = (vis_data - v_min) / (v_max - v_min)
        else:
            vis_data = np.zeros_like(vis_data)
            
        # Apply Colormap
        rgba_img = cmap(vis_data)
        
        # Convert to uint8 (0-255)
        final_img = (rgba_img[:, :, :3] * 255).astype(np.uint8)
        
        # Flip vertically (origin lower)
        final_img = np.flipud(final_img)
        
        # Convert to Pillow
        pil_img = Image.fromarray(final_img)
        frames_buffer.append(pil_img)
        
        if (f+1) % 10 == 0:
            print(f"  Frame {f+1}/{FRAMES} done.")

    print(f"Saving GIF to {OUTPUT_FILENAME}...")
    
    frames_buffer[0].save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        optimize=False, # Optimization sometimes kills subtle gradients in GIFs
        duration=DURATION,
        loop=0
    )
    
    print(f"✅ DONE! Total time: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    generate_hologram_gif()