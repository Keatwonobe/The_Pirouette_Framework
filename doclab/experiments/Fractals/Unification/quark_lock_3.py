import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time
from PIL import Image

# =========================================================
#  PROTON MICROSCOPE: INFINITY ZOOM & TRACK
# =========================================================

# --- MISSION CONTROL (Fractal Configuration) ---
OUTPUT_FILENAME = "fractal_microscope.gif"

# 1. NAVIGATION
TARGET_HINT = (0.0, -5)        # Initial starting guess
INITIAL_ZOOM_WIDTH = 1.5       # The starting width for the very first lock

# 2. FRACTAL LAYERING
GRID_SIZE = 4                  # 4x4 array (16 tiles)
LOCK_DEPTH = GRID_SIZE * GRID_SIZE # Total number of fractal layers
# How much smaller the next layer's window is (0.2 means 5x magnification)
ZOOM_STEP_FACTOR = 0.2

# 3. TIMING & OPTICS
TOTAL_FRAMES = 150             # Frames in the final animation
TARGET_CYCLES = 3              # Full rotations of the system (for looping)
DURATION = 50                  # Milliseconds per frame
TILE_RESOLUTION = 200          # Resolution of each individual tile (200x200)

# --- PHYSICS ENGINE ---

SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])
BREATHING_FREQ = 6.0 

@njit(parallel=True)
def render_microscope(center_m, center_l, width, res, src_m, src_l, src_amp):
    """
    High-precision renderer for deep zoom levels.
    """
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    intensity_map = np.zeros((res, res), dtype=np.float64)
    
    k_vec = np.zeros(3)
    for i in range(3):
        dist = np.sqrt(src_m[i]**2 + src_l[i]**2)
        k_vec[i] = (2 * np.pi) / (dist + 1e-9)

    for i in prange(res):
        y = l_vals[i]
        for j in range(res):
            x = m_vals[j]
            psi_real, psi_imag = 0.0, 0.0
            
            for q in range(3):
                dx = x - src_m[q]
                dy = y - src_l[q]
                r = np.sqrt(dx*dx + dy*dy)
                
                # Singularitiy Protection for Deep Zoom
                if r < 1e-12: r = 1e-12
                
                phase = k_vec[q] * r
                amp = (src_amp / r)
                
                psi_real += amp * np.cos(phase)
                psi_imag += amp * np.sin(phase)
            
            intensity_map[i, j] = psi_real**2 + psi_imag**2
            
    return intensity_map

# --- NAVIGATION SYSTEMS ---

def rotate_coords(m, l, theta):
    c, s = np.cos(theta), np.sin(theta)
    return m*c - l*s, m*s + l*c

def drill_down_target(src_m, src_l, hint, final_width):
    """
    The '5-frame' recursive locking algorithm.
    Starts wide, finds max, zooms, repeats.
    """
    current_m, current_l = hint
    # We will start the scan width at 1.5, and lock until we hit final_width
    current_width = INITIAL_ZOOM_WIDTH 
    step = 1
    
    # We drill down until our width is close to the target width
    while current_width > final_width:
        # print(f"  [Depth {step}] Scanning width {current_width:.5f} at ({current_m:.5f}, {current_l:.5f})...")
        
        # Low-res scan to find the peak in this layer
        scan_res = 100 
        img = render_microscope(current_m, current_l, current_width, scan_res, src_m, src_l, 1.0)
        
        # Find local max (The "Bright Object")
        # Mask edges to avoid getting stuck on the border
        img[0:5, :] = 0; img[-5:, :] = 0; img[:, 0:5] = 0; img[:, -5:] = 0
        
        idx = np.unravel_index(np.argmax(img), img.shape)
        
        half_w = current_width / 2.0
        # Re-calculate exact position of that pixel
        pixel_l = (current_l - half_w) + idx[0] * (current_width / (scan_res - 1))
        pixel_m = (current_m - half_w) + idx[1] * (current_width / (scan_res - 1))
        
        # Update center
        current_m, current_l = pixel_m, pixel_l
        
        # Zoom in (Decay factor 0.2 means 5x magnification per step)
        current_width *= 0.2
        step += 1
        
    # Calculate Polar coordinates for the Orbit Lock
    r_lock = np.sqrt(current_m**2 + current_l**2)
    theta_lock = np.arctan2(current_l, current_m)
    
    return current_m, current_l, r_lock, theta_lock

def find_all_locks():
    print(f"--- 🎯 INITIATING {LOCK_DEPTH}-LAYER FRACTAL ACQUISITION ---")
    
    # List to store (r_lock, theta_lock, final_width) for each layer
    lock_data = []
    
    # Start with the initial hint
    current_m, current_l = TARGET_HINT
    current_width = INITIAL_ZOOM_WIDTH
    
    for i in range(LOCK_DEPTH):
        # The final_width for this lock is the starting width for the next lock
        final_width_for_this_lock = current_width * ZOOM_STEP_FACTOR
        
        # We perform the drill-down starting from the previous lock's center
        m_center, l_center, r_lock, theta_lock = drill_down_target(
            SRC_M_BASE, SRC_L_BASE, (current_m, current_l), final_width_for_this_lock
        )
        
        # Store the locked parameters for this layer
        lock_data.append({
            'r': r_lock,
            'theta': theta_lock,
            'width': final_width_for_this_lock
        })
        
        # Set the next lock's starting hint and width to the results of this lock
        current_m, current_l = m_center, l_center
        current_width = final_width_for_this_lock
        
        print(f"  [Layer {i+1:02d}/{LOCK_DEPTH}] Zoom Width: {final_width_for_this_lock:.8f} | Center: ({m_center:.5f}, {l_center:.5f})")
        
    print("✅ FRACTAL LOCK SEQUENCE CONFIRMED.")
    return lock_data


# --- MAIN RENDERER ---

def render_tiled_fractal_gif():
    # 1. Warmup
    print("Pre-flight checks...")
    render_microscope(0,0,1,10, SRC_M_BASE, SRC_L_BASE, 1.0)
    
    # 2. Drill Down to find all Fractal Layers
    lock_sequence = find_all_locks()
    
    frames_buffer = []
    cmap = plt.get_cmap('magma')
    
    # Final image dimensions
    FINAL_WIDTH = GRID_SIZE * TILE_RESOLUTION
    FINAL_HEIGHT = GRID_SIZE * TILE_RESOLUTION
    
    # 3. Render the Tiled Orbit Sequence
    print(f"Rendering {GRID_SIZE}x{GRID_SIZE} Tiled Orbit sequence over {TOTAL_FRAMES} frames...")
    
    for f in range(TOTAL_FRAMES):
        # Global Rotation (The Universe is spinning N cycles)
        sys_theta = TARGET_CYCLES * 2 * np.pi * (f / TOTAL_FRAMES)
        
        # Rotate Sources
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        
        # Breathing Effect
        pulse = 1.0 + 0.1 * np.sin(2 * np.pi * (f / TOTAL_FRAMES) * BREATHING_FREQ)
        
        # Create a new blank canvas for this frame
        frame_canvas = Image.new('RGB', (FINAL_WIDTH, FINAL_HEIGHT))
        
        # Render all 16 tiles
        for i in range(LOCK_DEPTH):
            lock = lock_sequence[i]
            
            # 1. Determine Camera Position for this tile
            cam_theta = lock['theta'] + sys_theta
            cam_m = lock['r'] * np.cos(cam_theta)
            cam_l = lock['r'] * np.sin(cam_theta)
            
            # 2. Render the single tile at its deep zoom level
            raw = render_microscope(
                cam_m, cam_l, lock['width'], TILE_RESOLUTION, 
                curr_src_m, curr_src_l, pulse
            )
            
            # 3. Normalize, Colorize, and Flip the Tile
            v_min, v_max = raw.min(), raw.max()
            if v_max - v_min < 1e-9:
                norm = np.zeros_like(raw)
            else:
                norm = (raw - v_min) / (v_max - v_min)
                
            norm = np.power(norm, 0.5) # Gamma for "Glow"
            rgba = cmap(norm)
            img_uint8 = (rgba[:, :, :3] * 255).astype(np.uint8)
            img_uint8 = np.flipud(img_uint8) # Flip to match L-axis orientation
            
            tile_img = Image.fromarray(img_uint8)

            # 4. Calculate position in the 4x4 grid
            col = i % GRID_SIZE
            row = i // GRID_SIZE
            
            x_pos = col * TILE_RESOLUTION
            y_pos = row * TILE_RESOLUTION
            
            # 5. Paste the tile onto the main canvas
            frame_canvas.paste(tile_img, (x_pos, y_pos))

        frames_buffer.append(frame_canvas)
        
        if f % 15 == 0:
            print(f"  Frame {f}/{TOTAL_FRAMES} | Rendering Tiled Grid...")

    print(f"Saving Fractal Microscope Feed to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=DURATION,
        loop=0
    )
    print("✅ DONE.")

if __name__ == "__main__":
    render_tiled_fractal_gif()