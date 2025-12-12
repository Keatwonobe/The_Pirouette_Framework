import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time
from PIL import Image

# =========================================================
#  HOLOGRAPHIC ORBITAL LOCK (Targeting Substructure)
# =========================================================

# --- CINEMATOGRAPHY ---
OUTPUT_FILENAME = "proton_orbital_lock.gif"
FRAMES = 80               # Smooth loop
RES = 600                 # Resolution of the Zoom Window
ZOOM_RADIUS = 12        # How tight the zoom is (0.35 covers the "Airy Disk" and first ring)
DURATION = 50             # ms per frame

# --- PHYSICS PARAMETERS ---
# The External Source Triangle
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

# Pulsing Parameters (To create the "Flash")
BREATHING_AMP = 0.15      # How much the source intensity fluctuates
BREATHING_FREQ = 4.0      # How fast they pulse during the rotation

# --- KERNEL: HOLOGRAPHIC INTERFERENCE ---

@njit(parallel=True)
def render_window(center_m, center_l, radius, res, src_m, src_l, src_amp):
    """
    Renders a specific window of the holographic universe.
    """
    # Create the coordinate grid for the camera window
    m_vals = np.linspace(center_m - radius, center_m + radius, res)
    l_vals = np.linspace(center_l - radius, center_l + radius, res)
    
    intensity_map = np.zeros((res, res), dtype=np.float64)
    
    # Pre-compute source wave numbers
    k_vec = np.zeros(3)
    for i in range(3):
        dist = np.sqrt(src_m[i]**2 + src_l[i]**2)
        k_vec[i] = (2 * np.pi) / (dist + 1e-9)

    for i in prange(res):
        y = l_vals[i]
        for j in range(res):
            x = m_vals[j]
            
            psi_real = 0.0
            psi_imag = 0.0
            
            for q in range(3):
                dx = x - src_m[q]
                dy = y - src_l[q]
                r = np.sqrt(dx*dx + dy*dy)
                
                # Standard Wave Propagation
                if r < 1e-9: r = 1e-9
                phase = k_vec[q] * r
                
                # Amplitude falls off with 1/r, modulated by the "Breathing" source amp
                amp = (src_amp / r)
                
                psi_real += amp * np.cos(phase)
                psi_imag += amp * np.sin(phase)
            
            # Intensity = |Psi|^2
            intensity_map[i, j] = psi_real**2 + psi_imag**2
            
    return intensity_map

# --- NAVIGATION MATH ---

def rotate_coords(m, l, theta):
    """Rotates a point (m, l) around the origin (0,0)."""
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    m_new = m * cos_t - l * sin_t
    l_new = m * sin_t + l * cos_t
    return m_new, l_new

def acquire_lock(src_m, src_l):
    """
    Scans the center at t=0 to find the precise coordinates 
    of the primary internal quark to track.
    """
    print("[SYSTEM] Scanning for High-Energy Target...")
    
    # Coarse scan range [-1, 1]
    scan_res = 500
    m_s = np.linspace(-0.8, 0.8, scan_res)
    l_s = np.linspace(-0.8, 0.8, scan_res)
    
    # We pass amplitude 1.0 for the scan
    intensity = render_window(0, 0, 0.8, scan_res, src_m, src_l, 1.0)
    
    # Mask center singularity
    mid = scan_res // 2
    intensity[mid-20:mid+20, mid-20:mid+20] = 0
    
    # Find max
    idx = np.unravel_index(np.argmax(intensity), intensity.shape)
    
    # Map index back to coordinates
    # Note: render_window uses linspace, so we reconstruct
    target_l = -0.8 + idx[0] * (1.6 / (scan_res - 1))
    target_m = -0.8 + idx[1] * (1.6 / (scan_res - 1))
    
    print(f"[SYSTEM] Target Acquired at: M={target_m:.4f}, L={target_l:.4f}")
    
    # Calculate Polar Coordinates of the Target
    r_target = np.sqrt(target_m**2 + target_l**2)
    theta_target = np.arctan2(target_l, target_m)
    
    return r_target, theta_target

# --- MAIN ENGINE ---

def generate_orbital_gif():
    print(f"--- 🛰️ PROTON ORBITAL CAM ACTIVATED ---")
    
    # 1. JIT Warmup
    print("warming up numba...")
    render_window(0,0,1, 10, SRC_M_BASE, SRC_L_BASE, 1.0)
    
    # 2. Acquire Lock Data
    # We find the quark at rotation=0. 
    # Since the system rotates rigidly, we just rotate this coordinate for future frames.
    lock_r, lock_theta_initial = acquire_lock(SRC_M_BASE, SRC_L_BASE)
    
    frames_buffer = []
    
    # Colormap setup: Magma for that "burning energy" look
    cmap = plt.get_cmap('magma')
    
    start_time = time.time()
    
    for f in range(FRAMES):
        # Time / Rotation variables
        prog = f / FRAMES
        theta_system = 2 * np.pi * prog
        
        # A. Rotate External Sources (The Universe Moves)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, theta_system)
        
        # B. Calculate Camera Position (The Orbit Lock)
        # The quark moves with the system, so its angle is Initial + System Rotation
        cam_theta = lock_theta_initial + theta_system
        cam_m = lock_r * np.cos(cam_theta)
        cam_l = lock_r * np.sin(cam_theta)
        
        # C. Calculate "Breathing" Pulse
        # Sine wave modulation of source strength
        pulse_val = 1.0 + BREATHING_AMP * np.sin(2 * np.pi * prog * BREATHING_FREQ)
        
        # D. Render the Window
        raw_intensity = render_window(cam_m, cam_l, ZOOM_RADIUS, RES, curr_src_m, curr_src_l, pulse_val)
        
        # E. Post-Process (The "Glow")
        # Gamma correction is key here. Power < 1.0 boosts the faint rings/halos.
        vis_data = np.power(raw_intensity, 0.45)
        
        # Normalize frame-by-frame or globally? 
        # Frame-by-frame maximizes the "flash" effect.
        v_min, v_max = vis_data.min(), vis_data.max()
        vis_data = (vis_data - v_min) / (v_max - v_min + 1e-9)
        
        # Apply Color
        rgba = cmap(vis_data)
        final_img = (rgba[:, :, :3] * 255).astype(np.uint8)
        
        # Orientation (Origin Lower)
        final_img = np.flipud(final_img)
        
        frames_buffer.append(Image.fromarray(final_img))
        
        if (f+1) % 10 == 0:
            print(f"  Frame {f+1}/{FRAMES} rendered. Cam: ({cam_m:.2f}, {cam_l:.2f})")

    print(f"Saving locked footage to {OUTPUT_FILENAME}...")
    
    frames_buffer[0].save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        optimize=False,
        duration=DURATION,
        loop=0
    )
    
    print(f"✅ MISSION COMPLETE. Time: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    generate_orbital_gif()