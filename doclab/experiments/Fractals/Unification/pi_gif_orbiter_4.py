import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from numba import njit, prange
import time
from PIL import Image

# =========================================================
#  PROTON SUBSTRUCTURE SCANNER (Iso-Contour Mode)
# =========================================================

# --- MISSION CONFIG ---
OUTPUT_FILENAME = "proton_substructure.gif"
FRAMES = 60
DURATION = 50

# --- ZOOM TARGET ---
# We use the previous lock coordinates, but we start DEEP.
# Target: The calculated "South" Quark
TARGET_HINT = (0.0, -5) # Approximate lock from previous run
ZOOM_WIDTH = 500     # extremely deep zoom (microscopic)

# --- PHYSICS ---
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])
BREATHING_FREQ = 4.0

# --- PHYSICS KERNEL ---

@njit(parallel=True)
def compute_field_data(center_m, center_l, width, res, src_m, src_l, src_amp):
    """
    Returns Real and Imaginary components separately.
    """
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    psi_r = np.zeros((res, res), dtype=np.float64)
    psi_i = np.zeros((res, res), dtype=np.float64)
    
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
                if r < 1e-15: r = 1e-15 # prevent nan
                
                phase = k_vec[q] * r
                amp = (src_amp / r)
                
                vr += amp * np.cos(phase)
                vi += amp * np.sin(phase)
            
            psi_r[i, j] = vr
            psi_i[i, j] = vi
            
    return psi_r, psi_i

# --- VISUALIZATION KERNEL (THE "PARTIAL CIRCUITS") ---

def render_isocontours(real, imag):
    """
    Converts raw complex field into a Topographic Phase Map.
    This reveals structure inside saturated areas.
    """
    # 1. Amplitude & Phase
    amp = np.sqrt(real**2 + imag**2)
    phase = np.arctan2(imag, real) # -pi to pi
    
    # 2. Logarithmic Compression (The "Sunglasses")
    # Natural log of amplitude handles the massive dynamic range
    log_amp = np.log1p(amp)
    
    # 3. Iso-Contour Generation (The "Wiggles")
    # We take the sine of the log-amplitude. 
    # As amplitude shoots to infinity, this oscillates -1 to 1.
    # This turns the "white blob" into concentric rings.
    contour_freq = 30.0 # How many rings per brightness decade
    structure = np.sin(log_amp * contour_freq)
    
    # Normalize structure to 0.0 - 1.0 range for Value (Brightness)
    # We map sine wave (-1 to 1) to (0.2 to 1.0) so it's never fully black
    val = 0.6 + 0.4 * structure
    
    # 4. Color Mapping
    # Hue = Phase (The "Spin" direction)
    hue = (phase + np.pi) / (2 * np.pi)
    
    # Saturation
    # Let's make the "nodes" (dark lines in the contour) more saturated
    sat = np.ones_like(hue) * 0.95
    
    # Stack HSV
    hsv = np.dstack((hue, sat, val))
    rgb = hsv_to_rgb(hsv)
    
    return (rgb * 255).astype(np.uint8)

# --- UTILS ---

def rotate_coords(m, l, theta):
    c, s = np.cos(theta), np.sin(theta)
    return m*c - l*s, m*s + l*c

def find_lock_at_zoom(src_m, src_l):
    # Quick drill down to ensure we are centered
    # Start at 0.1 width, go to ZOOM_WIDTH
    print("Refining Lock...")
    current_m, current_l = TARGET_HINT
    current_w = 0.5
    
    for i in range(8):
        pr, pi = compute_field_data(current_m, current_l, current_w, 100, src_m, src_l, 1.0)
        amp = pr**2 + pi**2
        
        # Mask edges
        amp[0:5,:]=0; amp[-5:,:]=0; amp[:,0:5]=0; amp[:,-5:]=0
        
        idx = np.unravel_index(np.argmax(amp), amp.shape)
        
        # Map back
        half_w = current_w/2
        pixel_l = (current_l - half_w) + idx[0] * (current_w/99)
        pixel_m = (current_m - half_w) + idx[1] * (current_w/99)
        
        current_m, current_l = pixel_m, pixel_l
        current_w *= 0.4 # Zoom in
        
    print(f"Lock Refined: ({current_m:.8f}, {current_l:.8f})")
    return np.sqrt(current_m**2 + current_l**2), np.arctan2(current_l, current_m)


# --- MAIN ---

def generate_substructure_gif():
    print(f"--- 🔬 PROTON SUBSTRUCTURE SCANNER ---")
    print(f"Zoom Width: {ZOOM_WIDTH} (Approx 10,000x Magnification)")
    
    # 1. Warmup
    compute_field_data(0,0,1,10, SRC_M_BASE, SRC_L_BASE, 1.0)
    
    # 2. Get Precise Orbit Lock
    lock_r, lock_theta_init = find_lock_at_zoom(SRC_M_BASE, SRC_L_BASE)
    
    frames_buffer = []
    
    for f in range(FRAMES):
        prog = f / FRAMES
        sys_theta = 2 * np.pi * prog
        
        # Orbit Camera
        cam_theta = lock_theta_init + sys_theta
        cam_m = lock_r * np.cos(cam_theta)
        cam_l = lock_r * np.sin(cam_theta)
        
        # Rotate Sources
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        
        # Breathing
        pulse = 1.0 + 0.15 * np.sin(2 * np.pi * prog * BREATHING_FREQ)
        
        # Render Raw Field
        pr, pi = compute_field_data(cam_m, cam_l, ZOOM_WIDTH, 500, curr_src_m, curr_src_l, pulse)
        
        # Process Isocontours
        img = render_isocontours(pr, pi)
        img = np.flipud(img)
        
        frames_buffer.append(Image.fromarray(img))
        
        if f % 10 == 0:
            print(f"  Frame {f}/{FRAMES} processed.")
            
    print(f"Saving Scan to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=DURATION,
        loop=0
    )
    print("✅ DONE.")

if __name__ == "__main__":
    generate_substructure_gif()