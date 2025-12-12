import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw
import imageio.v2 as imageio
import math

# =========================================================
#  PIROUETTE: CINEMATIC FORMATION TRACER
#  "The Latent Wound Channel"
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_cinematic_formation.gif"

# TIMING
TOTAL_PHYSICS_STEPS = 200   # How deep we simulate. (Standard was 100, we go deeper for "Slow Mo")
FRAMES_PER_STEP = 1         # 1:1 speed. Increase to 2 or 3 to make it slower/smoother.

# DYNAMICS
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
EPSILON = 1e-5
R_ESCAPE = 50.0
HELICITY_STOP = np.pi * 0.95

# CAMERA / TRACKING
RES = 400                   # Output resolution
START_WIDTH = 35000000.0    # Start very wide
FINAL_WIDTH = 2000000.0     # Zoom level at the core (Adjust to see more/less swirlies)
LOCK_THRESHOLD = 500000.0   # Distance to (0,0) to trigger "Lock"

# STARTING POSITION (The entry point of the streak)
START_M = 0.0
START_L = 12000000.0 

# =========================================================
#  NUMBA PHYSICS KERNEL (STEP-LIMITED)
# =========================================================

@njit(fastmath=True)
def get_force_numba(m, lam):
    # Teal
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold
    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2 + 1e-12)
    scale   = np.sqrt(mag)
    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    # Weights
    angle_rad = np.arctan2(lam, m)
    angle_deg = np.degrees(angle_rad) % 360.0

    d_g = np.abs(angle_deg - 30.0);  d_g = np.minimum(d_g, 360.0-d_g)
    d_t = np.abs(angle_deg - 150.0); d_t = np.minimum(d_t, 360.0-d_t)
    d_r = np.abs(angle_deg - 270.0); d_r = np.minimum(d_r, 360.0-d_r)

    w_gold = np.exp(-(d_g / 80.0)**2)
    w_teal = np.exp(-(d_t / 80.0)**2)
    w_red  = np.exp(-(d_r / 80.0)**2)
    tot = w_gold + w_teal + w_red + 1e-6
    
    Fm   = (w_teal*F_teal_m + w_red*F_red_m + w_gold*F_gold_m)/tot
    Flam = (w_teal*F_teal_lam + w_red*F_red_lam + w_gold*F_gold_lam)/tot

    return Fm, Flam, w_red/tot

@njit(fastmath=True)
def compute_formation_state(m0, l0, limit_steps):
    """
    Runs the simulation ONLY up to 'limit_steps'.
    Returns the accumulated Helicity (Log Divergence) at that moment in time.
    """
    m1, l1 = m0, l0
    m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm1, pl1 = 0.0, 0.0
    pm2, pl2 = 0.0, 0.0
    max_diff_angle = 0.0
    
    # Run exactly 'limit_steps' iterations
    for _ in range(limit_steps):
        # Double-step integration for stability
        for _ in range(2):
            Fm1, Flam1, w_red1 = get_force_numba(m1, l1)
            drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
            pm1 = (pm1 + 0.5 * DT * Fm1) * drag1; pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
            m1 += DT * pm1; l1 += DT * pl1

            Fm2, Flam2, w_red2 = get_force_numba(m2, l2)
            drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
            pm2 = (pm2 + 0.5 * DT * Fm2) * drag2; pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
            m2 += DT * pm2; l2 += DT * pl2

        ang1 = np.arctan2(l1, m1)
        ang2 = np.arctan2(l2, m2)
        
        # Normalized difference
        diff = np.arctan2(np.sin(ang1 - ang2), np.cos(ang1 - ang2))
        adiff = np.abs(diff)
        if adiff > max_diff_angle: max_diff_angle = adiff
        
        # Note: We do NOT break early here if we want to show the full "wave" 
        # propagating, but usually optimization is fine. 
        # For "swirlies", the divergence happens later, so we must keep running.
        if max_diff_angle > HELICITY_STOP: break
        if (m1**2 + l1**2) > R_ESCAPE: break

    return np.log(max_diff_angle + EPSILON)

@njit(parallel=True, fastmath=True)
def render_frame(center_m, center_l, width, res, current_step_limit):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    heatmap = np.zeros((res, res), dtype=np.float64)
    
    for i in prange(res):
        l_curr = l_vals[i]
        for j in range(res):
            m_curr = m_vals[j]
            heatmap[i, j] = compute_formation_state(m_curr, l_curr, current_step_limit)
            
    return heatmap

# =========================================================
#  DIRECTOR
# =========================================================

def run_cinematic_trace():
    print(f"--- 🎬 PIROUETTE CINEMATIC TRACER ---")
    print(f"Goal: Chase the traveler to (0,0), then watch the wake form.")
    
    # Camera State
    cam_m = START_M
    cam_l = START_L
    cam_width = START_WIDTH
    
    locked = False
    frames = []
    
    # We will iterate through physics steps (Time)
    # We can generate multiple frames per physics step for slow motion if needed
    
    for t in range(1, TOTAL_PHYSICS_STEPS + 1):
        
        # "Slow Motion" support (optional sub-frame interpolation could go here)
        # For now, 1 frame per step.
        
        # 1. RENDER CURRENT STATE OF THE UNIVERSE
        # We assume the camera position from the *previous* step is good for this step
        heatmap = render_frame(cam_m, cam_l, cam_width, RES, t)
        
        # 2. IMAGE PROCESSING
        h_min, h_max = heatmap.min(), heatmap.max()
        if h_max == h_min: h_max += 1e-9
        norm = (heatmap - h_min) / (h_max - h_min)
        
        cm = plt.get_cmap('magma')
        colored = cm(norm)
        img_data = (colored[:, :, :3] * 255).astype(np.uint8)
        img_pil = Image.fromarray(np.flipud(img_data))
        
        # 3. HUD
        draw = ImageDraw.Draw(img_pil)
        status = "LOCKED" if locked else "TRACKING"
        color = (255, 100, 100) if locked else (100, 255, 100)
        
        draw.text((10, 10), f"T = {t} / {TOTAL_PHYSICS_STEPS}", fill=(255, 255, 255))
        draw.text((10, 25), f"MODE: {status}", fill=color)
        draw.text((10, 40), f"ZOOM: {cam_width:.1e}", fill=(200, 200, 200))
        
        # Crosshair
        cx, cy = RES//2, RES//2
        draw.line((cx-10, cy, cx+10, cy), fill=color, width=1)
        draw.line((cx, cy-10, cx, cy+10), fill=color, width=1)
        
        frames.append(img_pil)
        
        # 4. CAMERA UPDATE LOGIC
        if not locked:
            # FIND THE HOTSPOT (The "Tip" of the streak)
            # We look for the brightest pixel in the current frame
            idx = np.unravel_index(np.argmax(heatmap), heatmap.shape)
            
            # Convert pixel to world
            px_scale = cam_width / (RES - 1)
            target_l = (cam_l - cam_width/2.0) + idx[0] * px_scale
            target_m = (cam_m - cam_width/2.0) + idx[1] * px_scale
            
            # Move Camera (Smooth Lerp)
            lerp_factor = 0.3 # Smooth follow
            cam_m += (target_m - cam_m) * lerp_factor
            cam_l += (target_l - cam_l) * lerp_factor
            
            # Zoom Logic (Get closer as we go)
            # Simple approach: Zoom based on step count or distance
            dist_to_origin = np.sqrt(cam_m**2 + cam_l**2)
            
            # Map distance to zoom
            # Far (28M) -> START_WIDTH
            # Close (0) -> FINAL_WIDTH
            ratio = dist_to_origin / (START_WIDTH / 2) # Rough ratio
            ratio = np.clip(ratio, 0.0, 1.0)
            target_width = FINAL_WIDTH + (START_WIDTH - FINAL_WIDTH) * (ratio**0.5)
            
            cam_width += (target_width - cam_width) * 0.1
            
            # LOCK CHECK
            if dist_to_origin < LOCK_THRESHOLD:
                print(f"[EVENT] T={t}: CORE REACHED. LOCKING CAMERA.")
                locked = True
                # Snap to center
                cam_m = 0.0
                cam_l = 0.0
                cam_width = FINAL_WIDTH
        
        else:
            # LOCKED MODE
            # We just stay at (0,0) and let the time 't' increase.
            # This reveals the "latent wound channel" / swirlies forming.
            pass

        if t % 10 == 0:
            print(f"Rendered Step {t} | Cam: ({cam_m:.1e}, {cam_l:.1e}) | Width: {cam_width:.1e}")

    # SAVE
    print(f"Saving GIF to {OUTPUT_FILENAME}...")
    # FPS = 15 gives a nice cinematic feel
    imageio.mimsave(OUTPUT_FILENAME, frames, fps=15)
    print("Done.")

if __name__ == "__main__":
    run_cinematic_trace()