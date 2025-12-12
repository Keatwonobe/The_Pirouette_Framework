import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from numba import njit, prange
from PIL import Image, ImageDraw
import os
import shutil

# =========================================================
#  PROTON DISC ANIMATOR (Fixed Camera, Evolving Physics)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_DIR = "proton_disc_frames"
GIF_FILENAME = "proton_disc_formation.gif"

# Visuals
RES = 600           # Output resolution (square)
DISC_RADIUS = 280   # Radius of the visible circle (in pixels)
VIEW_WIDTH = 16.0   # How much 'physics space' fits in the window (Zoom level)

# Animation
FRAMES = 60         # Total frames for one loop
DURATION_MS = 50    # Speed
ROTATION_SPEED = 1.0 # 1.0 = One full spin per loop

# Physics Setup (The Triplet)
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

# =========================================================
#  1. PHYSICS KERNEL (Unchanged, Numba Accelerated)
# =========================================================

@njit(parallel=True)
def compute_field_data(width, res, src_m, src_l, src_amp):
    # Camera is always centered at 0,0 now
    half_w = width / 2.0
    m_vals = np.linspace(-half_w, half_w, res)
    l_vals = np.linspace(-half_w, half_w, res)
    
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
                if r < 1e-15: r = 1e-15
                
                phase = k_vec[q] * r
                amp = (src_amp / r)
                
                vr += amp * np.cos(phase)
                vi += amp * np.sin(phase)
            
            psi_r[i, j] = vr
            psi_i[i, j] = vi
            
    return psi_r, psi_i

# =========================================================
#  2. VISUALIZATION (Psychedelic + Disc Mask)
# =========================================================

def render_isocontours(real, imag):
    # --- A. The Math (Colors) ---
    amp = np.sqrt(real**2 + imag**2)
    phase = np.arctan2(imag, real)
    
    log_amp = np.log1p(amp)
    contour_freq = 30.0 
    structure = np.sin(log_amp * contour_freq)
    
    val = 0.6 + 0.4 * structure
    hue = (phase + np.pi) / (2 * np.pi)
    sat = np.ones_like(hue) * 0.95
    
    hsv = np.dstack((hue, sat, val))
    rgb = hsv_to_rgb(hsv)
    img_array = (rgb * 255).astype(np.uint8)
    
    return np.flipud(img_array) # Flip for correct orientation

def apply_disc_mask(pil_image, radius):
    """
    Creates a circular aperture. Everything outside 'radius' becomes dark.
    """
    # Create a mask image (L mode)
    mask = Image.new("L", pil_image.size, 0) # Start black
    draw = ImageDraw.Draw(mask)
    
    # Calculate center
    cx, cy = pil_image.size[0] // 2, pil_image.size[1] // 2
    
    # Draw white circle in the center
    bbox = (cx - radius, cy - radius, cx + radius, cy + radius)
    draw.ellipse(bbox, fill=255)
    
    # Create the background (Dark Blue/Black like the reference)
    background = Image.new("RGB", pil_image.size, (20, 10, 40))
    
    # Composite: Use mask to paste the physics onto the background
    final_img = Image.composite(pil_image, background, mask)
    return final_img

# =========================================================
#  3. ANIMATION LOGIC
# =========================================================

def rotate_coords(m, l, theta):
    c, s = np.cos(theta), np.sin(theta)
    return m*c - l*s, m*s + l*c

def run_animator():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    print(f"--- 💿 PROTON DISC ANIMATOR ---")
    print(f"Rendering {FRAMES} frames at {RES}x{RES}...")
    
    # Warmup
    compute_field_data(10, 10, SRC_M_BASE, SRC_L_BASE, 1.0)
    
    frames_buffer = []
    
    for f in range(FRAMES):
        prog = f / FRAMES
        
        # 1. Physics Dynamics
        # Rotate the Sources (The "Propeller")
        sys_theta = (2 * np.pi * prog) * ROTATION_SPEED
        cur_m, cur_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        
        # Breathing (Pulse)
        pulse = 1.0 + 0.1 * np.sin(4 * np.pi * prog)
        
        # 2. Compute Field
        pr, pi = compute_field_data(VIEW_WIDTH, RES, cur_m, cur_l, pulse)
        
        # 3. Colorize
        raw_img_array = render_isocontours(pr, pi)
        pil_img = Image.fromarray(raw_img_array)
        
        # 4. Apply The Disc Mask
        # (This cuts the circle out of the square data)
        final_img = apply_disc_mask(pil_img, DISC_RADIUS)
        
        # 5. Save
        fn = os.path.join(OUTPUT_DIR, f"frame_{f:03d}.png")
        final_img.save(fn)
        frames_buffer.append(final_img)
        
        if f % 10 == 0:
            print(f"  Frame {f}/{FRAMES} done.")

    # Save GIF
    print("Stitching GIF...")
    frames_buffer[0].save(
        GIF_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=DURATION_MS,
        loop=0
    )
    print(f"✅ Saved: {GIF_FILENAME}")

if __name__ == "__main__":
    run_animator()