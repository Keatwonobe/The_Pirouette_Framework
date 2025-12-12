import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont

# =========================================================
#  PROTON MICROSCOPE: HYBRID FUSION (v11.0)
#  "Coarse Acquisition -> Fine Helical Dive"
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_hybrid_fusion.gif"
RENDER_RES = 500
RADAR_RES = 64

# PHASE 1: COARSE ACQUISITION (Hunter-Seeker)
SEARCH_FRAMES = 60       # How long we watch the probe "hunt"
SEARCH_WIDTH = 25.0      # Wide angle search

# PHASE 2: FINE DIVE (Helical Rail)
DIVE_FRAMES = 100        # How long the smooth dive lasts
DIVE_TARGET_WIDTH = 0.05 # The final deep zoom

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

# --- MATH MODULE: HELICAL FITTING ---

def fit_helical_path(raw_m, raw_l):
    """
    Takes the noisy 'Coarse' data and solves for the 'Fine' spiral.
    """
    if len(raw_m) < 5: return (0,0), 10.0, -0.1, 0 # Fallback
    
    center_m = np.mean(raw_m)
    center_l = np.mean(raw_l)
    
    r_vals = []
    theta_vals = []
    
    for i in range(len(raw_m)):
        dm = raw_m[i] - center_m
        dl = raw_l[i] - center_l
        r = np.sqrt(dm**2 + dl**2)
        th = np.arctan2(dl, dm)
        r_vals.append(r)
        theta_vals.append(th)
        
    r_vals = np.array(r_vals)
    theta_vals = np.unwrap(np.array(theta_vals))
    
    # Regression: ln(r) = ln(A) + kappa * theta
    x = theta_vals
    y = np.log(r_vals + 1e-9)
    A_mat = np.vstack([x, np.ones(len(x))]).T
    kappa, ln_A = np.linalg.lstsq(A_mat, y, rcond=None)[0]
    
    start_radius = np.exp(ln_A)
    
    # Force inward spiral for the dive
    if kappa > -0.01: kappa = -0.05
    
    print(f"  > TRANSITION CALCULATION: Center=({center_m:.2f}, {center_l:.2f}) | Kappa={kappa:.4f}")
    return (center_m, center_l), start_radius, kappa, theta_vals[-1] # Start from where we left off

def get_helical_pos(center, r0, kappa, start_theta, progress):
    total_rot = 4 * np.pi # 2 full turns during dive
    theta = start_theta + (progress * total_rot)
    r = r0 * np.exp(kappa * (theta - start_theta))
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return center[0] + x, center[1] + y, r

# --- MAIN MISSION ---

def run_hybrid_mission():
    frames_buffer = []
    
    # --- PHASE 1: COARSE SEARCH (Hunter-Seeker) ---
    print("--- PHASE 1: COARSE ACQUISITION ---")
    
    # Tracking Variables
    cam_m, cam_l = 0.0, -5.0
    tracked_m, tracked_l = [], [] # History for the solver
    
    for f in range(SEARCH_FRAMES):
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.1)
        
        # 1. Radar Scan (The "Coarse" Look)
        radar = render_microscope(cam_m, cam_l, SEARCH_WIDTH, RADAR_RES, curr_src_m, curr_src_l, pulse)
        
        # 2. Update Position (Twitchy Logic)
        if np.max(radar) > 0.01:
            idx = np.unravel_index(np.argmax(radar), radar.shape)
            scale = SEARCH_WIDTH / RADAR_RES
            off_m = (idx[1] - RADAR_RES/2) * scale
            off_l = (RADAR_RES/2 - idx[0]) * scale
            
            # Move camera partially towards target (Laggy follow)
            cam_m += off_m * 0.2 
            cam_l += off_l * 0.2
            
            # Record accurate position for Phase 2 math
            tracked_m.append(cam_m + off_m)
            tracked_l.append(cam_l + off_l)
        
        # 3. Render High Res
        raw = render_microscope(cam_m, cam_l, SEARCH_WIDTH, RENDER_RES, curr_src_m, curr_src_l, pulse)
        
        # 4. HUD (Red/Searching)
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.5)
        img = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
        img = np.flipud(img)
        pil_img = Image.fromarray(img)
        
        draw = ImageDraw.Draw(pil_img)
        draw.text((10, 10), "MODE: COARSE SEARCH", fill=(255, 100, 100))
        draw.text((10, 25), f"DATA POINTS: {len(tracked_m)}", fill=(255, 100, 100))
        
        # Jittery Reticle
        cx, cy = RENDER_RES//2, RENDER_RES//2
        draw.rectangle([cx-40, cy-40, cx+40, cy+40], outline=(255, 50, 50), width=1)
        
        frames_buffer.append(pil_img)

    # --- PHASE 2: HAND-OFF (Math) ---
    print("--- COMPUTING FLIGHT PATH ---")
    center, r0, kappa, theta_handoff = fit_helical_path(tracked_m, tracked_l)
    
    # We need to bridge the gap between where the camera IS (cam_m, cam_l) 
    # and where the rail STARTS. We'll use a short interpolation in the first few frames of Phase 3.
    start_rail_m, start_rail_l, _ = get_helical_pos(center, r0, kappa, theta_handoff, 0.0)
    
    # --- PHASE 3: FINE DIVE (Helical Rail) ---
    print("--- PHASE 3: FINE HELICAL DIVE ---")
    
    for f in range(DIVE_FRAMES):
        # Continue global time
        abs_frame = SEARCH_FRAMES + f
        sys_theta = 2 * np.pi * (abs_frame / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.05 * np.sin(abs_frame * 0.2)
        
        progress = f / (DIVE_FRAMES - 1)
        
        # 1. Get Rail Position (The "Fine" Path)
        rail_m, rail_l, rail_r = get_helical_pos(center, r0, kappa, theta_handoff, progress)
        
        # 2. Camera Smoothing (Transition from Coarse position to Rail)
        # For the first 20% of the dive, blend the camera position to smooth the "snap"
        blend_duration = 0.2
        if progress < blend_duration:
            blend_t = progress / blend_duration
            # Cubic ease-in-out
            t_smooth = blend_t * blend_t * (3 - 2 * blend_t)
            
            curr_cam_m = cam_m * (1 - t_smooth) + rail_m * t_smooth
            curr_cam_l = cam_l * (1 - t_smooth) + rail_l * t_smooth
        else:
            curr_cam_m = rail_m
            curr_cam_l = rail_l
            
        # 3. Zoom Logic (Helical)
        # Start at search width, decay to target
        # Use log interpolation for zoom
        log_start = np.log(SEARCH_WIDTH)
        log_end = np.log(DIVE_TARGET_WIDTH)
        current_w = np.exp(log_start + (log_end - log_start) * progress)
        
        # 4. Render
        raw = render_microscope(curr_cam_m, curr_cam_l, current_w, RENDER_RES, curr_src_m, curr_src_l, pulse)
        
        # 5. HUD (Cyan/Locked)
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.5)
        img = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
        img = np.flipud(img)
        pil_img = Image.fromarray(img)
        
        draw = ImageDraw.Draw(pil_img)
        draw.text((10, 10), "MODE: HELICAL DIVE [LOCKED]", fill=(0, 255, 255))
        draw.text((10, 25), f"ZOOM: {current_w:.4e}", fill=(0, 255, 255))
        draw.text((10, 40), f"TORSION (K): {kappa:.4f}", fill=(0, 255, 255))
        
        # Tight Locked Reticle
        cx, cy = RENDER_RES//2, RENDER_RES//2
        draw.line([cx-10, cy, cx+10, cy], fill=(0, 255, 255), width=2)
        draw.line([cx, cy-10, cx, cy+10], fill=(0, 255, 255), width=2)
        
        frames_buffer.append(pil_img)
        
        if f % 20 == 0:
            print(f"Dive Frame {f}/{DIVE_FRAMES} | Width: {current_w:.2f}")

    # SAVE
    print(f"Saving Hybrid Mission Log to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ MISSION COMPLETE.")

if __name__ == "__main__":
    run_hybrid_mission()