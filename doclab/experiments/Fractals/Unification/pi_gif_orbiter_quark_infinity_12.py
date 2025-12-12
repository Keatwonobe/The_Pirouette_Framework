import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont

# =========================================================
#  PROTON SEEKER HEAD: "SMART-GIF" GENERATOR
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_seeker_lock.gif"
FRAMES = 120
START_WIDTH = 12.0      # Starting wide view
MIN_WIDTH = 0.05        # Stop if we hit this (sub-atomic)
ZOOM_FACTOR = 0.96      # 4% Zoom per frame (aggressive)

# TARGETING
TARGET_HINT = (0.0, -5.0) # We look here first
SEARCH_RADIUS = 0.3       # As fraction of current width (Look within 30% of screen center)
SIGNAL_THRESHOLD = 0.001  # Minimum intensity to consider "Visible"

# --- PHYSICS ENGINE (Unchanged) ---
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

@njit(parallel=True)
def render_microscope(center_m, center_l, width, res, src_m, src_l, src_amp):
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
                if r < 1e-12: r = 1e-12 # Singularity clamp
                
                phase = k_vec[q] * r
                amp = (src_amp / r)
                
                psi_real += amp * np.cos(phase)
                psi_imag += amp * np.sin(phase)
            
            intensity_map[i, j] = psi_real**2 + psi_imag**2
            
    return intensity_map

def rotate_coords(m, l, theta):
    c, s = np.cos(theta), np.sin(theta)
    return m*c - l*s, m*s + l*c

# --- THE SEEKER BRAIN ---

def find_peak_in_window(img, width, center_m, center_l, relative_radius):
    """
    Finds the brightest pixel, but ONLY within a radius of the center.
    This prevents the camera from jumping to a different quark if the target fades.
    """
    res = img.shape[0]
    mid = res // 2
    pixel_radius = int(res * relative_radius)
    
    # Create a mask
    Y, X = np.ogrid[:res, :res]
    dist_from_center = np.sqrt((X - mid)**2 + (Y - mid)**2)
    mask = dist_from_center <= pixel_radius
    
    # Mask out everything outside the search radius
    masked_img = img.copy()
    masked_img[~mask] = 0
    
    # Find max in masked area
    max_val = np.max(masked_img)
    idx = np.unravel_index(np.argmax(masked_img), img.shape)
    
    # Convert pixel back to Coordinate Space
    # idx[0] is row (L), idx[1] is col (M)
    pixel_l = (center_l - width/2) + idx[0] * (width / (res - 1))
    pixel_m = (center_m - width/2) + idx[1] * (width / (res - 1))
    
    return max_val, pixel_m, pixel_l

def run_seeker_mission():
    print("--- 🎯 PROTON SEEKER INITIATED ---")
    
    # Initial State
    cam_m, cam_l = TARGET_HINT
    curr_width = START_WIDTH
    
    # Motion Memory (The "Kappa" Term)
    last_theta = np.arctan2(cam_l, cam_m)
    omega_memory = 0.0 # Angular velocity
    
    frames_buffer = []
    
    # Find Initial Lock (Frame -1)
    print("Acquiring Initial Lock...")
    # Render wide to find the specific quark
    curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, 0)
    init_scan = render_microscope(cam_m, cam_l, 6.0, 200, curr_src_m, curr_src_l, 1.0)
    _, lock_m, lock_l = find_peak_in_window(init_scan, 6.0, cam_m, cam_l, 0.5)
    
    cam_m, cam_l = lock_m, lock_l
    print(f"Locked on Quark at ({cam_m:.2f}, {cam_l:.2f})")

    # --- MAIN LOOP ---
    for f in range(FRAMES):
        # 1. Physics Update
        sys_theta = 2 * np.pi * (f / 100) # Global time
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.2)
        
        # 2. Render Sensor Frame (Low Res for decision making)
        sensor_res = 100
        sensor_img = render_microscope(cam_m, cam_l, curr_width, sensor_res, curr_src_m, curr_src_l, pulse)
        
        # 3. Analyze Signal
        # Only look within central 40% of the screen for the target
        peak_val, peak_m, peak_l = find_peak_in_window(sensor_img, curr_width, cam_m, cam_l, 0.4)
        
        # 4. Decision Logic
        is_visible = peak_val > SIGNAL_THRESHOLD
        
        mode_text = ""
        color = ""
        
        if is_visible:
            # === TRACKING MODE (SPIRAL) ===
            mode_text = "VISUAL LOCK - ZOOMING"
            color = (0, 255, 0) # Green
            
            # Update Position to the Peak
            cam_m, cam_l = peak_m, peak_l
            
            # Update Memory (Calculate Angular Velocity)
            curr_theta = np.arctan2(cam_l, cam_m)
            # Handle atan2 wrap-around (-pi to pi)
            diff = curr_theta - last_theta
            if diff > np.pi: diff -= 2*np.pi
            if diff < -np.pi: diff += 2*np.pi
            
            # Smooth the velocity update (Weighted average)
            omega_memory = (0.7 * omega_memory) + (0.3 * diff)
            last_theta = curr_theta
            
            # ZOOM EXECUTION
            if curr_width > MIN_WIDTH:
                curr_width *= ZOOM_FACTOR
                
        else:
            # === PREDICTION MODE (ELLIPSE) ===
            mode_text = "LOST SIGNAL - INERTIAL TRACK"
            color = (255, 50, 50) # Red
            
            # Apply Rotational Memory (Kappa)
            # We rotate the camera around (0,0) by the last known omega
            r_curr = np.sqrt(cam_m**2 + cam_l**2)
            theta_pred = last_theta + omega_memory
            
            cam_m = r_curr * np.cos(theta_pred)
            cam_l = r_curr * np.sin(theta_pred)
            
            last_theta = theta_pred
            
            # STOP ZOOM (Hold pattern)
            pass

        # 5. Render High Quality Output
        # We re-render centered on the *decided* camera position
        hq_res = 500
        raw = render_microscope(cam_m, cam_l, curr_width, hq_res, curr_src_m, curr_src_l, pulse)
        
        # Normalization (Overexposure Protection)
        v_min, v_max = raw.min(), raw.max()
        if v_max - v_min < 1e-9:
            norm = np.zeros_like(raw)
        else:
            norm = (raw - v_min) / (v_max - v_min)
        
        norm = np.power(norm, 0.5) # Gamma
        img_colored = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
        img_colored = np.flipud(img_colored)
        pil_img = Image.fromarray(img_colored)
        
        # 6. Draw HUD
        draw = ImageDraw.Draw(pil_img)
        draw.text((10, 10), f"SYS.TIME: {f}", fill=(200, 200, 200))
        draw.text((10, 25), mode_text, fill=color)
        draw.text((10, 40), f"ZOOM WIDTH: {curr_width:.5f}", fill=(200, 200, 200))
        draw.text((10, 55), f"OMEGA (MEM): {omega_memory:.5f}", fill=(200, 200, 200))
        
        
        frames_buffer.append(pil_img)
        
        if f % 10 == 0:
            print(f"Frame {f} | {mode_text} | W: {curr_width:.4f}")

    print(f"Saving Mission Log to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=50,
        loop=0
    )
    print("✅ MISSION COMPLETE.")

if __name__ == "__main__":
    run_seeker_mission()