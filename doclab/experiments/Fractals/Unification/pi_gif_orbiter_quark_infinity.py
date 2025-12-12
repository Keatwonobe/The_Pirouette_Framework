import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time
from PIL import Image

# =========================================================
#  PROTON MICROSCOPE: INFINITY ZOOM & TRACK (v2.0)
# =========================================================

# --- MISSION CONTROL ---

# 1. NAVIGATION LAYERS 🚀
# Define the deep-zoom sequence. Each entry is a layer.
# The script will run the full drill-down protocol for each layer *before* rendering.
LAYER_CONFIG = {
    # Layer 1: The Initial Quark View
    1: {
        "OUTPUT_FILENAME": "proton_microscope_layer_1.gif",
        "TARGET_HINT": (0.0, -5),  # Start from a wide guess
        "FINAL_ZOOM_WIDTH": 12, # Original zoom level
    },
    # Layer 2: Deep Dive into the first sub-structure
    2: {
        "OUTPUT_FILENAME": "proton_microscope_layer_2.gif",
        # TARGET_HINT for layer 2 will be set to the LOCK COORDINATE of layer 1.
        "FINAL_ZOOM_WIDTH": 11, # Significantly deeper zoom
    },
    # Layer 3: Pushing the limits
    3: {
        "OUTPUT_FILENAME": "proton_microscope_layer_3.gif",
        # TARGET_HINT for layer 3 will be set to the LOCK COORDINATE of layer 2.
        "FINAL_ZOOM_WIDTH": 10, # Nearing Float64 precision limits
    },
    # Add more layers as needed...
}

# --- CONTROLLER ---
# ⚠️ SET THIS TO THE FINAL LAYER YOU WANT TO RENDER ⚠️
# Set to 1 to just re-render the original
# Set to 2 to compute layer 1's lock and render the layer 2 deep dive
N_LAYERS = 3

# 2. OPTICS & TIMING
DIVE_FRAMES = 40          # Frames spent zooming in
ORBIT_FRAMES = 40         # Frames spent orbiting at the bottom
DURATION = 50             # Frame duration in milliseconds

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
    current_width = 1.5 # Start with a wide view
    step = 1
    
    # We drill down until our width is close to the target width
    while current_width > final_width:
        # print(f"    [Depth {step}] Scanning width {current_width:.5f} at ({current_m:.5f}, {current_l:.5f})...")
        
        scan_res = 100 
        img = render_microscope(current_m, current_l, current_width, scan_res, src_m, src_l, 1.0)
        
        # Find local max (The "Bright Object")
        # Mask edges to avoid getting stuck on the border
        img[0:5, :] = 0; img[-5:, :] = 0; img[:, 0:5] = 0; img[:, -5:] = 0
        
        # Check if we're hitting the edge and need a wider scan
        if np.max(img) == 0:
            print("WARNING: Peak hit masked edge. Resetting scan width.")
            current_width *= 5 # Try a wider view
            continue
            
        idx = np.unravel_index(np.argmax(img), img.shape)
        
        # Convert index back to coords
        half_w = current_width / 2.0
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
    
    return r_lock, theta_lock, current_m, current_l

def recursive_drill_down(target_layer):
    """
    Runs the drill-down protocol for all layers up to the target_layer.
    Returns the lock coordinates (r, theta) for the final layer.
    """
    lock_r_prev, lock_theta_prev = None, None
    lock_m_prev, lock_l_prev = None, None
    
    for layer in range(1, target_layer + 1):
        config = LAYER_CONFIG[layer]
        
        # Set the target hint based on the previous layer's lock
        if layer > 1:
            # The hint for the current layer is the lock of the previous one
            config["TARGET_HINT"] = (lock_m_prev, lock_l_prev)
            
        print(f"--- 🎯 Layer {layer}: INITIATING TARGET ACQUISITION (Target Width: {config['FINAL_ZOOM_WIDTH']:.8f}) ---")
        
        # Run the drill down
        lock_r, lock_theta, lock_m, lock_l = drill_down_target(
            SRC_M_BASE, SRC_L_BASE, config["TARGET_HINT"], config["FINAL_ZOOM_WIDTH"]
        )
        
        print(f"✅ Layer {layer} LOCK CONFIRMED. Coordinates: ({lock_m:.12f}, {lock_l:.12f}) | Zoom: {lock_r:.8f}")
        
        # Store for the next iteration
        lock_r_prev, lock_theta_prev = lock_r, lock_theta
        lock_m_prev, lock_l_prev = lock_m, lock_l
        
    return lock_r_prev, lock_theta_prev, LAYER_CONFIG[target_layer]["FINAL_ZOOM_WIDTH"], LAYER_CONFIG[target_layer]["OUTPUT_FILENAME"]


# --- MAIN RENDERER ---

def generate_microscope_gif():
    # 1. Warmup
    print("Pre-flight checks...")
    render_microscope(0,0,1,10, SRC_M_BASE, SRC_L_BASE, 1.0)
    
    # 2. Recursive Drill Down to find the Quark structure for the final layer
    lock_r, lock_theta_init, final_width, output_filename = recursive_drill_down(N_LAYERS)
    
    frames_buffer = []
    cmap = plt.get_cmap('magma')
    
    # 3. Render the Sequence
    print(f"Rendering Dive & Orbit sequence for Layer {N_LAYERS}...")
    
    # Combine frames: Dive + Orbit
    total_frames = DIVE_FRAMES + ORBIT_FRAMES
    
    # Calculate Zoom Curve (Logarithmic descent)
    # Start width: 1.5, End width: final_width
    zoom_levels = np.logspace(np.log10(1.5), np.log10(final_width), DIVE_FRAMES)
    
    for f in range(total_frames):
        # Global Rotation (The Universe is spinning)
        sys_theta = 2 * np.pi * (f / total_frames)
        
        # Determine Current Zoom Level
        if f < DIVE_FRAMES:
            current_width = zoom_levels[f]
            # During dive, we stick to the lock
        else:
            current_width = final_width
            # During orbit, we stay at max zoom
            
        # Determine Camera Position
        # The camera tracks the quark's rotation
        cam_theta = lock_theta_init + sys_theta
        cam_m = lock_r * np.cos(cam_theta)
        cam_l = lock_r * np.sin(cam_theta)
        
        # Rotate Sources
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        
        # Breathing Effect
        pulse = 1.0 + 0.1 * np.sin(2 * np.pi * (f / total_frames) * BREATHING_FREQ)
        
        # Render
        # We use a solid resolution of 500x500
        raw = render_microscope(cam_m, cam_l, current_width, 500, curr_src_m, curr_src_l, pulse)
        
        # --- LOCAL NORMALIZATION (The "Overexposure" Fix) ---
        v_min, v_max = raw.min(), raw.max()
        if v_max - v_min < 1e-9:
            norm = np.zeros_like(raw)
        else:
            norm = (raw - v_min) / (v_max - v_min)
            
        # Apply Gamma for "Glow"
        norm = np.power(norm, 0.5)
        
        # Colorize
        cmap_to_use = plt.get_cmap('magma') # We keep a consistent colormap
        rgba = cmap_to_use(norm)
        img_uint8 = (rgba[:, :, :3] * 255).astype(np.uint8)
        img_uint8 = np.flipud(img_uint8)
        
        frames_buffer.append(Image.fromarray(img_uint8))
        
        if f % 5 == 0:
            print(f"  Frame {f}/{total_frames} | Zoom Width: {current_width:.9f}")

    print(f"Saving Microscope Feed to {output_filename}...")
    frames_buffer[0].save(
        output_filename,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=DURATION,
        loop=0
    )
    print("✅ DONE.")

if __name__ == "__main__":
    generate_microscope_gif()