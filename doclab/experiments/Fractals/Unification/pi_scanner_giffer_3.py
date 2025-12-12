import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from numba import njit, prange
from PIL import Image
import os
import shutil

# =========================================================
#  PROTON DYNAMIC SCANNER (Merged Engine)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_DIR = "proton_frames"
GIF_FILENAME = "proton_dynamic_evolution.gif"

# Resolution & Quality
RES = 512          # Image resolution (512x512)
FRAMES = 60        # Total animation frames
DURATION_MS = 50   # Speed of GIF (ms per frame)

# Camera & Zoom
# VIEW_WIDTH: Smaller = Zoomed In, Larger = Wide Angle
# 0.5 = Microscopic, 20.0 = Mid-range, 500.0 = Wide Manifold
VIEW_WIDTH = 8 
TARGET_HINT = (0.0, -5.0) # Approximate coordinate of the "South Quark"

# Physics Parameters
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])
BREATHING_FREQ = 4.0      # How fast the sources "pump"
ROTATION_SPEED = 1.0      # 1.0 = Full 360 rotation over the frame count

# =========================================================
#  1. PHYSICS KERNEL (NUMBA ACCELERATED)
# =========================================================

@njit(parallel=True)
def compute_field_data(center_m, center_l, width, res, src_m, src_l, src_amp):
    """
    Calculates the complex interference field from 3 point sources.
    """
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    psi_r = np.zeros((res, res), dtype=np.float64)
    psi_i = np.zeros((res, res), dtype=np.float64)
    
    # Pre-calculate wave vectors (k) based on distance from origin/interactions
    k_vec = np.zeros(3)
    for i in range(3):
        dist = np.sqrt(src_m[i]**2 + src_l[i]**2)
        k_vec[i] = (2 * np.pi) / (dist + 1e-12)

    for i in prange(res):
        y = l_vals[i]
        for j in range(res):
            x = m_vals[j]
            vr, vi = 0.0, 0.0
            
            for q in range(3):
                dx = x - src_m[q]
                dy = y - src_l[q]
                r = np.sqrt(dx*dx + dy*dy)
                if r < 1e-15: r = 1e-15 # Singularity protection
                
                phase = k_vec[q] * r
                amp = (src_amp / r)
                
                vr += amp * np.cos(phase)
                vi += amp * np.sin(phase)
            
            psi_r[i, j] = vr
            psi_i[i, j] = vi
            
    return psi_r, psi_i

# =========================================================
#  2. VISUALIZATION KERNEL (ISOCONTOUR STYLE)
# =========================================================

def render_isocontours(real, imag):
    """
    Converts raw complex field into the 'Psychedelic' Topographic Map.
    """
    # 1. Amplitude & Phase
    amp = np.sqrt(real**2 + imag**2)
    phase = np.arctan2(imag, real) # -pi to pi
    
    # 2. Logarithmic Compression (Handles the singularity intensity)
    log_amp = np.log1p(amp)
    
    # 3. Iso-Contour Generation (The "Wiggles")
    # Creates concentric rings based on field intensity
    contour_freq = 30.0 
    structure = np.sin(log_amp * contour_freq)
    
    # Map sine wave (-1 to 1) to brightness (0.2 to 1.0)
    val = 0.6 + 0.4 * structure
    
    # 4. Color Mapping
    # Hue = Phase (The "Spin" direction)
    hue = (phase + np.pi) / (2 * np.pi)
    
    # Saturation: Make the contour lines pop
    sat = np.ones_like(hue) * 0.95
    
    # Stack HSV and convert
    hsv = np.dstack((hue, sat, val))
    rgb = hsv_to_rgb(hsv)
    
    return (rgb * 255).astype(np.uint8)

# =========================================================
#  3. UTILITIES & ORBITAL LOGIC
# =========================================================

def rotate_coords(m, l, theta):
    """Rotates the source coordinates around the center."""
    c, s = np.cos(theta), np.sin(theta)
    return m*c - l*s, m*s + l*c

def find_lock_at_zoom(src_m, src_l):
    """
    Drills down to find the highest energy point near the target hint.
    This ensures the camera doesn't stare at empty space.
    """
    print(f"  [System] Acquiring Target Lock near {TARGET_HINT}...")
    current_m, current_l = TARGET_HINT
    current_w = 2.0 # Start search width
    
    # Iterative drill-down
    for i in range(8):
        pr, pi = compute_field_data(current_m, current_l, current_w, 100, src_m, src_l, 1.0)
        amp = pr**2 + pi**2
        
        # Mask edges to avoid getting stuck on the frame border
        amp[0:5,:]=0; amp[-5:,:]=0; amp[:,0:5]=0; amp[:,-5:]=0
        
        idx = np.unravel_index(np.argmax(amp), amp.shape)
        
        # Map pixel index back to coordinate space
        half_w = current_w/2
        pixel_l = (current_l - half_w) + idx[0] * (current_w/99)
        pixel_m = (current_m - half_w) + idx[1] * (current_w/99)
        
        current_m, current_l = pixel_m, pixel_l
        current_w *= 0.5 # Zoom in for next pass
        
    print(f"  [System] Lock Acquired: ({current_m:.4f}, {current_l:.4f})")
    # Return polar coordinates of the lock relative to center
    return np.sqrt(current_m**2 + current_l**2), np.arctan2(current_l, current_m)

# =========================================================
#  4. MAIN EXECUTION
# =========================================================

def run_scanner():
    # Setup Directories
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    print(f"--- 🔬 PROTON DYNAMIC SCANNER INITIALIZED ---")
    print(f"Resolution: {RES}px | Frames: {FRAMES} | View Width: {VIEW_WIDTH}")

    # 1. Warmup Numba
    print("  [System] Warming up physics kernel...")
    compute_field_data(0,0,1,10, SRC_M_BASE, SRC_L_BASE, 1.0)
    
    # 2. Calculate Initial Orbit Lock
    # We find where the interesting feature is at T=0
    lock_r, lock_theta_init = find_lock_at_zoom(SRC_M_BASE, SRC_L_BASE)
    
    frames_buffer = []
    
    print("  [System] Starting Render Loop...")
    
    for f in range(FRAMES):
        # Progress (0.0 to 1.0)
        prog = f / FRAMES
        
        # A. Calculate Dynamics
        sys_theta = (2 * np.pi * prog) * ROTATION_SPEED
        
        # B. Orbit Camera Logic
        # We rotate the camera WITH the system to keep the lock in view
        cam_theta = lock_theta_init + sys_theta
        cam_m = lock_r * np.cos(cam_theta)
        cam_l = lock_r * np.sin(cam_theta)
        
        # C. Rotate The Proton Sources
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        
        # D. Breathing Effect (Source Amplitude Pulse)
        pulse = 1.0 + 0.15 * np.sin(2 * np.pi * prog * BREATHING_FREQ)
        
        # E. Render Frame
        # Note: We pass VIEW_WIDTH here. Change this global to zoom in/out.
        pr, pi = compute_field_data(cam_m, cam_l, VIEW_WIDTH, RES, curr_src_m, curr_src_l, pulse)
        
        img_array = render_isocontours(pr, pi)
        # Flip vertically because matrix origin is usually top-left vs plot bottom-left
        img_array = np.flipud(img_array) 
        
        # F. Save Individual Frame
        img = Image.fromarray(img_array)
        frame_filename = os.path.join(OUTPUT_DIR, f"frame_{f:03d}.png")
        img.save(frame_filename)
        frames_buffer.append(img)
        
        if f % 5 == 0:
            print(f"    -> Rendered Frame {f}/{FRAMES}")

    # 3. Generate GIF
    print(f"  [System] Stitching {len(frames_buffer)} frames into GIF...")
    frames_buffer[0].save(
        GIF_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=DURATION_MS,
        loop=0
    )
    print(f"✅ DONE. Saved to: {GIF_FILENAME}")

if __name__ == "__main__":
    run_scanner()