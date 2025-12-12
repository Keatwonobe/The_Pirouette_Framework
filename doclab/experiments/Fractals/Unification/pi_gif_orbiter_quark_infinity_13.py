import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw

# =========================================================
#  PROTON INTERCEPTOR: HIGH-G TRACKING
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_interceptor_snap.gif"
FRAMES = 140
START_WIDTH = 12.0
MIN_WIDTH = 0.05
BASE_ZOOM = 0.95        # Aggressive default zoom

# TARGETING
TARGET_HINT = (0.0, -5.0)
SIGNAL_THRESHOLD = 0.001

# PHYSICS ENGINE (Standard)
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
                if r < 1e-12: r = 1e-12
                phase = k_vec[q] * r
                amp = (src_amp / r)
                psi_real += amp * np.cos(phase)
                psi_imag += amp * np.sin(phase)
            intensity_map[i, j] = psi_real**2 + psi_imag**2
    return intensity_map

def rotate_coords(m, l, theta):
    c, s = np.cos(theta), np.sin(theta)
    return m*c - l*s, m*s + l*c

def find_peak_in_window(img, width, center_m, center_l, search_ratio):
    res = img.shape[0]
    mid = res // 2
    pixel_radius = int(res * search_ratio)
    
    # Mask outside search radius
    Y, X = np.ogrid[:res, :res]
    dist = np.sqrt((X - mid)**2 + (Y - mid)**2)
    mask = dist <= pixel_radius
    
    masked_img = img.copy()
    masked_img[~mask] = 0
    
    max_val = np.max(masked_img)
    idx = np.unravel_index(np.argmax(masked_img), img.shape)
    
    pixel_l = (center_l - width/2) + idx[0] * (width / (res - 1))
    pixel_m = (center_m - width/2) + idx[1] * (width / (res - 1))
    
    return max_val, pixel_m, pixel_l

# --- HIGH-G TRACKING LOGIC ---

def run_interceptor():
    print("--- 🚀 HIGH-G INTERCEPTOR LAUNCHED ---")
    
    cam_m, cam_l = TARGET_HINT
    curr_width = START_WIDTH
    
    # TRACKING STATE
    last_theta = np.arctan2(cam_l, cam_m)
    omega = 0.0           # Angular Velocity
    alpha = 0.0           # Angular Acceleration
    
    frames_buffer = []
    
    # Initial Lock
    curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, 0)
    init_scan = render_microscope(cam_m, cam_l, 6.0, 200, curr_src_m, curr_src_l, 1.0)
    _, cam_m, cam_l = find_peak_in_window(init_scan, 6.0, cam_m, cam_l, 0.5)
    
    for f in range(FRAMES):
        # 1. Physics Update
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.2)
        
        # 2. Sensor Scan
        sensor_res = 120 # Slight bump in res for better tracking
        sensor_img = render_microscope(cam_m, cam_l, curr_width, sensor_res, curr_src_m, curr_src_l, pulse)
        
        # 3. Target Acquisition
        peak_val, peak_m, peak_l = find_peak_in_window(sensor_img, curr_width, cam_m, cam_l, 0.45)
        is_visible = peak_val > SIGNAL_THRESHOLD
        
        hud_color = (100, 100, 100)
        hud_text = "INIT"
        
        if is_visible:
            # === VISUAL TRACKING ===
            # Calculate pixel displacement (How fast is it moving across our screen?)
            move_dist = np.sqrt((peak_m - cam_m)**2 + (peak_l - cam_l)**2)
            screen_velocity = move_dist / curr_width # % of screen moved
            
            # Update Position
            cam_m, cam_l = peak_m, peak_l
            
            # Calculate Angular Dynamics
            curr_theta = np.arctan2(cam_l, cam_m)
            diff = curr_theta - last_theta
            
            # Unwrap angle
            if diff > np.pi: diff -= 2*np.pi
            if diff < -np.pi: diff += 2*np.pi
            
            # Acceleration Calculation (New!)
            new_alpha = diff - omega
            alpha = (0.5 * alpha) + (0.5 * new_alpha) # Fast reaction smoothing
            
            # Velocity Update (Less memory, more immediate response)
            omega = diff 
            last_theta = curr_theta
            
            # === ADAPTIVE ZOOM CONTROLLER ===
            # If it moves > 10% of screen width, we are losing control. BACK OFF.
            if screen_velocity > 0.10: 
                curr_width *= 1.05 # Zoom OUT (Panic expansion)
                hud_text = "⚠️ HIGH-G: PULLING BACK"
                hud_color = (255, 50, 50)
            elif curr_width > MIN_WIDTH:
                curr_width *= BASE_ZOOM # Normal Zoom
                hud_text = "LOCKED: DIVING"
                hud_color = (0, 255, 0)
                
        else:
            # === INERTIAL PREDICTION (The "Switcheroo" Handler) ===
            hud_text = "LOST: PREDICTING"
            hud_color = (255, 200, 50)
            
            # Apply Velocity + Acceleration
            # This allows us to track a curve even when blind
            pred_theta = last_theta + omega + alpha
            
            r_curr = np.sqrt(cam_m**2 + cam_l**2)
            cam_m = r_curr * np.cos(pred_theta)
            cam_l = r_curr * np.sin(pred_theta)
            
            last_theta = pred_theta
            # Decay acceleration (don't spiral forever)
            alpha *= 0.9
            
            # Hold Zoom (Don't dive when blind)
            pass

        # 4. Render
        hq_res = 500
        raw = render_microscope(cam_m, cam_l, curr_width, hq_res, curr_src_m, curr_src_l, pulse)
        
        # Normalize
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.5)
        img = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
        img = np.flipud(img)
        pil_img = Image.fromarray(img)
        
        # 5. HUD
        draw = ImageDraw.Draw(pil_img)
        draw.text((10, 10), hud_text, fill=hud_color)
        draw.text((10, 25), f"WIDTH: {curr_width:.4f}", fill=hud_color)
        draw.text((10, 40), f"OMEGA: {omega:.4f}", fill=hud_color)
        draw.text((10, 55), f"ALPHA: {alpha:.4f}", fill=hud_color)
        
        cx, cy = hq_res//2, hq_res//2
        ret_size = 20
        draw.rectangle([cx-ret_size, cy-ret_size, cx+ret_size, cy+ret_size], outline=hud_color)
        
        frames_buffer.append(pil_img)
        
        if f % 10 == 0:
            print(f"Frame {f} | {hud_text} | Alpha: {alpha:.5f}")

    print(f"Saving Interceptor Log to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ MISSION COMPLETE.")

if __name__ == "__main__":
    run_interceptor()