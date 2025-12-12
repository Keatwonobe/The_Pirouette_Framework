import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont

# =========================================================
#  PROTON MICROSCOPE: THE KEPLER RAIL (v9.0)
#  "Smooth, Synthetic Orbital Locking"
# =========================================================

# --- MISSION CONTROL ---
OUTPUT_FILENAME = "proton_railgun_lock.gif"
RENDER_RES = 500
RADAR_RES = 64
TOTAL_FRAMES = 160

# --- THE "STICK" CONTROLS ---
# We slide the camera from the Center (0.0) to the Particle (1.0)
# while simultaneously zooming in.
LOCK_START = 0.0      # Start looking at the whole system
LOCK_END = 1.0        # End clamped to the particle
ZOOM_START = 22.0     # Wide angle
ZOOM_END = 11.9        # Macro zoom on the quark

# --- PHYSICS ENGINE ---
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

# --- THE RAILGUN GEOMETRY ---

def fit_perfect_rail(raw_m, raw_l):
    """
    Takes noisy survey points and returns the parameters for a 
    perfect, smooth parametric ellipse.
    """
    data = np.vstack((raw_m, raw_l)).T
    center = np.mean(data, axis=0)
    centered = data - center
    cov = np.cov(centered.T)
    evals, evecs = np.linalg.eig(cov)
    
    sort_idx = np.argsort(evals)[::-1]
    evals = evals[sort_idx]
    evecs = evecs[:, sort_idx]
    
    major = 2.0 * np.sqrt(evals[0])
    minor = 2.0 * np.sqrt(evals[1])
    angle = np.arctan2(evecs[1, 0], evecs[0, 0])
    
    return center, major, minor, angle

def get_rail_position(center, a, b, angle, t_phase):
    """
    Returns the exact coordinate on the rail at phase t.
    """
    # Parametric Ellipse
    x_local = a * np.cos(t_phase)
    y_local = b * np.sin(t_phase)
    
    # Rotate
    x_rot = x_local * np.cos(angle) - y_local * np.sin(angle)
    y_rot = x_local * np.sin(angle) + y_local * np.cos(angle)
    
    return center[0] + x_rot, center[1] + y_rot

# --- MAIN EXECUTION ---

def run_railgun_mission():
    frames_buffer = []
    
    # 1. THE SURVEY (Fast & Rough)
    print("--- PHASE 1: MAPPING THE TRACK ---")
    survey_duration = 60
    raw_m, raw_l = [], []
    curr_m, curr_l = 0.0, -5.0 # Guess
    
    for f in range(survey_duration):
        # We assume the universe rotates at a steady rate for the survey
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.1)
        
        # Wide scan to find the orbit
        scan_w = ZOOM_START * 1.2
        radar = render_microscope(curr_m, curr_l, scan_w, RADAR_RES, curr_src_m, curr_src_l, pulse)
        
        if np.max(radar) > 0.02:
            idx = np.unravel_index(np.argmax(radar), radar.shape)
            scale = scan_w / RADAR_RES
            off_m = (idx[1] - RADAR_RES/2) * scale
            off_l = (RADAR_RES/2 - idx[0]) * scale
            curr_m += off_m
            curr_l += off_l
            raw_m.append(curr_m)
            raw_l.append(curr_l)

    # 2. BUILD THE RAIL (The Math)
    center, a, b, angle = fit_perfect_rail(raw_m, raw_l)
    print(f"  > Rail Constructed: Center {center}, Axes ({a:.2f}, {b:.2f})")

    # 3. RENDER THE SMOOTH RIDE
    print("--- PHASE 2: EXECUTING FLIGHT PLAN ---")
    
    for f in range(TOTAL_FRAMES):
        # Time Progress (0.0 to 1.0)
        progress = f / (TOTAL_FRAMES - 1)
        
        # A. Physics Rotation
        # We sync the rotation to the frame count to ensure perfect loops
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        # Pulse: We dampen it slightly to reduce "strobe" annoyance
        pulse = 1.0 + 0.05 * np.sin(f * 0.2)
        
        # B. Calculate "Ghost" Particle Position on the Rail
        # We force a smooth orbital velocity (no jitter)
        # Assuming ~2 loops over the duration
        phase = progress * 4 * np.pi 
        rail_m, rail_l = get_rail_position(center, a, b, angle, phase)
        
        # C. Calculate "Slider" Position (The Camera Stick)
        # Smooth ease-in-out curve for the lock transition
        # smooth_t = progress * progress * (3 - 2 * progress) # Cubic ease
        smooth_t = progress # Linear is cleaner for analysis
        
        lock_ratio = LOCK_START + (LOCK_END - LOCK_START) * smooth_t
        zoom_width = ZOOM_START + (ZOOM_END - ZOOM_START) * smooth_t
        
        # Camera Position = Linear Interpolation between Center and Rail
        cam_m = center[0] * (1 - lock_ratio) + rail_m * lock_ratio
        cam_l = center[1] * (1 - lock_ratio) + rail_l * lock_ratio
        
        # D. Render
        raw = render_microscope(cam_m, cam_l, zoom_width, RENDER_RES, curr_src_m, curr_src_l, pulse)
        
        # Post-Process
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.5)
        img = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
        img = np.flipud(img)
        pil_img = Image.fromarray(img)
        
        # HUD
        draw = ImageDraw.Draw(pil_img)
        # Draw the "Stick" visualization
        cx, cy = RENDER_RES // 2, RENDER_RES // 2
        
        if lock_ratio < 0.99:
            draw.text((10, 10), "MODE: ORBIT ACQUISITION", fill="cyan")
            draw.text((10, 25), f"LOCK: {lock_ratio*100:.1f}%", fill="yellow")
        else:
            draw.text((10, 10), "MODE: RAIL LOCKED", fill=(0, 255, 0))
            
            # Reticle when locked
            draw.line((cx-10, cy, cx+10, cy), fill=(0, 255, 0))
            draw.line((cx, cy-10, cx, cy+10), fill=(0, 255, 0))

        frames_buffer.append(pil_img)
        
        if f % 20 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | Lock: {lock_ratio:.2f} | Zoom: {zoom_width:.2f}")

    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ DONE.")

if __name__ == "__main__":
    run_railgun_mission()