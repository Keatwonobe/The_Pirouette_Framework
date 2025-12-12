import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from numba import njit, prange
import time
from PIL import Image

# =========================================================
#  HOLOGRAPHIC QUARK TRACKER (Stabilized Phase Cam)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "quark_phase_tracker.gif"
FRAMES = 60               # Frames for one full phase cycle/rotation
RES = 600                 # Resolution of the ZOOMED window
ZOOM_RADIUS = 15        # How close we are looking (Viewport size = 2*Radius)
DURATION = 50             # ms per frame

# --- PHYSICS PARAMETERS ---
# Matches the equilateral(ish) triangle from the previous experiment
SRC_M = np.array([-10.0, 10.0, 0.0])
SRC_L = np.array([5.0, 5.0, -10.0])

# --- KERNEL: COMPLEX FIELD CALCULATOR ---

@njit(parallel=True)
def compute_complex_field(m_vals, l_vals, src_m, src_l):
    """
    Returns the raw COMPLEX wavefunction Psi.
    """
    h = len(l_vals)
    w = len(m_vals)
    # We store Real and Imag parts separately for Numba compatibility 
    # (though recent Numba handles complex well, this is safer)
    psi_real_map = np.zeros((h, w), dtype=np.float64)
    psi_imag_map = np.zeros((h, w), dtype=np.float64)
    
    # Pre-compute k vectors (fixed for rigid rotation)
    k_vec = np.zeros(3)
    for i in range(3):
        dist = np.sqrt(src_m[i]**2 + src_l[i]**2)
        k_vec[i] = (2 * np.pi) / dist if dist != 0 else 0

    for i in prange(h):
        y = l_vals[i]
        for j in range(w):
            x = m_vals[j]
            
            val_r = 0.0
            val_i = 0.0
            
            for q in range(3):
                # Distance from pixel to source
                dx = x - src_m[q]
                dy = y - src_l[q]
                r = np.sqrt(dx*dx + dy*dy)
                
                # Softening to prevent singularity
                if r < 1e-9: r = 1e-9
                
                # Wave: (e^(i k r)) / r
                phase = k_vec[q] * r
                inv_r = 1.0 / r
                
                val_r += np.cos(phase) * inv_r
                val_i += np.sin(phase) * inv_r
            
            psi_real_map[i, j] = val_r
            psi_imag_map[i, j] = val_i
            
    return psi_real_map, psi_imag_map

# --- HELPER: ROTATION & TRACKING ---

def rotate_point(m, l, theta):
    """Rotates a coordinate (m, l) around (0,0) by theta."""
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    m_new = m * cos_t - l * sin_t
    l_new = m * sin_t + l * cos_t
    return m_new, l_new

def find_target_quark(src_m, src_l):
    """
    Scans the central basin at t=0 to find the coordinates 
    of the strongest internal peak (the Quark).
    """
    print("Scanning for Quark Target...")
    # Low-res scan of the central area
    scan_res = 400
    scan_range = 1.0 # [-1, 1]
    m_s = np.linspace(-scan_range, scan_range, scan_res)
    l_s = np.linspace(-scan_range, scan_range, scan_res)
    
    pr, pi = compute_complex_field(m_s, l_s, src_m, src_l)
    intensity = pr**2 + pi**2
    
    # Mask out the very center (often a singularity or zero)
    mid = scan_res // 2
    intensity[mid-10:mid+10, mid-10:mid+10] = 0
    
    # Find max
    idx = np.unravel_index(np.argmax(intensity), intensity.shape)
    peak_l = l_s[idx[0]]
    peak_m = m_s[idx[1]]
    
    print(f"Locked on Quark at: m={peak_m:.4f}, l={peak_l:.4f}")
    return peak_m, peak_l

# --- VISUALIZATION: PHASE MAPPING ---

def complex_to_image(real, imag):
    """
    Converts complex field to RGBA using Domain Coloring.
    Brightness = Amplitude
    Hue = Phase (Argument)
    """
    amp = np.sqrt(real**2 + imag**2)
    phase = np.arctan2(imag, real) # -pi to pi
    
    # Normalize Phase to 0-1 for Hue
    hue = (phase + np.pi) / (2 * np.pi)
    
    # Normalize Amplitude for Brightness (Log scale for dynamic range)
    # Using a soft sigmoid-like contrast curve
    amp_norm = np.log(1 + amp)
    # Auto-scale
    if amp_norm.max() > 0:
        amp_norm /= amp_norm.max()
    
    # Create HSV image
    # H = Phase (Spin)
    # S = 1.0 (Vibrant)
    # V = Amplitude (Structure)
    
    # Vectorized HSV to RGB
    h = hue
    s = np.ones_like(hue) * 0.9
    v = amp_norm
    
    # Matplotlib's hsv_to_rgb expects shape (H, W, 3)
    hsv_stack = np.dstack((h, s, v))
    rgb = hsv_to_rgb(hsv_stack)
    
    # Convert to 0-255 uint8
    img_uint8 = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    return img_uint8

# --- MAIN RENDERER ---

def generate_tracker_gif():
    print(f"--- 🔭 PROTON TRACKER: STABILIZED CAM ---")
    
    # 1. Initialize
    # JIT Compile
    print("Initializing Physics Engine...")
    compute_complex_field(np.linspace(0,1,10), np.linspace(0,1,10), SRC_M, SRC_L)
    
    # 2. Acquire Target
    target_m_start, target_l_start = find_target_quark(SRC_M, SRC_L)
    
    frames_buffer = []
    
    print(f"Rendering {FRAMES} stabilized frames...")
    
    for f in range(FRAMES):
        theta = 2 * np.pi * f / FRAMES
        
        # A. Rotate the Universe (External Sources)
        curr_src_m, curr_src_l = rotate_point(SRC_M, SRC_L, theta)
        
        # B. Rotate the Camera (Track the internal spot)
        # Since the interference pattern rotates with the sources, 
        # our target coordinate simply rotates by theta.
        cam_m, cam_l = rotate_point(target_m_start, target_l_start, theta)
        
        # C. Define Viewport (Zoomed in on Camera Center)
        m_vals = np.linspace(cam_m - ZOOM_RADIUS, cam_m + ZOOM_RADIUS, RES)
        l_vals = np.linspace(cam_l - ZOOM_RADIUS, cam_l + ZOOM_RADIUS, RES)
        
        # D. Render
        pr, pi = compute_complex_field(m_vals, l_vals, curr_src_m, curr_src_l)
        
        # E. Colorize (Phase Mapping)
        img = complex_to_image(pr, pi)
        
        # Add a crosshair? No, let's keep it clean.
        # Flip for image coords
        img = np.flipud(img)
        
        frames_buffer.append(Image.fromarray(img))
        
        if f % 10 == 0:
            print(f"  Frame {f}/{FRAMES} captured.")
            
    # Save
    print(f"Saving tracking data to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=DURATION,
        loop=0
    )
    print("✅ DONE.")

if __name__ == "__main__":
    generate_tracker_gif()