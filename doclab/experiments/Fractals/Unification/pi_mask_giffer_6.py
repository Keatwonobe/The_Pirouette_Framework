import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw
import imageio.v2 as imageio

# =========================================================
#  PIROUETTE: THE TATTLETALE (Hunt, Drill, Film)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_tattletale_hd.gif"

# DYNAMICS
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
EPSILON = 1e-5
R_ESCAPE = 50.0
HELICITY_STOP = np.pi * 0.95

# SEARCH PARAMETERS
GLOBAL_SEARCH_WIDTH = 60000000.0 # Look at EVERYTHING (-30M to +30M)
SEARCH_RES = 250                 # Resolution for the "Wide Net"
CHAOS_THRESHOLD = 0.5            # How much helicity triggers the "Tattletale"?
MAX_WAIT_STEPS = 50              # How long to wait for the first spark?

# FILMING PARAMETERS
TARGET_ZOOM_WIDTH = 500000.0     # How close do we want to get before filming?
HD_RES = 500                     # Resolution of the final GIF
RECORD_FRAMES = 120              # Duration of the tracked shot

# =========================================================
#  NUMBA PHYSICS KERNEL
# =========================================================

@njit(fastmath=True)
def get_force_numba(m, lam):
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2 + 1e-12)
    scale   = np.sqrt(mag)
    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

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
def compute_divergence(m0, l0, steps):
    """
    Runs physics for 'steps'. Returns accumulated log-divergence.
    """
    m1, l1 = m0, l0
    m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm1, pl1 = 0.0, 0.0
    pm2, pl2 = 0.0, 0.0
    max_diff_angle = 0.0
    
    for _ in range(steps):
        # Double-step integration
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
        diff = np.arctan2(np.sin(ang1 - ang2), np.cos(ang1 - ang2))
        adiff = np.abs(diff)
        if adiff > max_diff_angle: max_diff_angle = adiff
        
        # We generally don't break early in search mode to find the *peak* chaos
        if (m1**2 + l1**2) > R_ESCAPE: break

    return np.log(max_diff_angle + EPSILON)

@njit(parallel=True, fastmath=True)
def scan_sector(center_m, center_l, width, res, depth_steps):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    heatmap = np.zeros((res, res), dtype=np.float64)
    
    for i in prange(res):
        l_curr = l_vals[i]
        for j in range(res):
            m_curr = m_vals[j]
            heatmap[i, j] = compute_divergence(m_curr, l_curr, depth_steps)
            
    return heatmap

# =========================================================
#  THE PROTOCOLS
# =========================================================

def find_hotspot(heatmap, center_m, center_l, width):
    """
    Finds the world coordinates of the brightest pixel.
    """
    idx = np.unravel_index(np.argmax(heatmap), heatmap.shape)
    res = heatmap.shape[0]
    px_scale = width / (res - 1)
    
    # idx[0] is row (y/l), idx[1] is col (x/m)
    # L array goes min->max (bottom->top)
    peak_l = (center_l - width/2.0) + idx[0] * px_scale
    peak_m = (center_m - width/2.0) + idx[1] * px_scale
    val = heatmap[idx]
    
    return peak_m, peak_l, val

def run_tattletale():
    print("--- 🕵️ PIROUETTE: TATTLETALE PROTOCOL ---")
    
    cam_m = 0.0
    cam_l = 0.0
    cam_width = GLOBAL_SEARCH_WIDTH
    
    # --- PHASE 1: WIDE NET SURVEILLANCE ---
    print(f"[PHASE 1] Scanning Sector 0 (Width: {cam_width:.1e})...")
    found = False
    
    # We increase 'depth' as we wait. 
    # Maybe the chaos takes time to manifest.
    current_depth = 50 
    
    for t in range(MAX_WAIT_STEPS):
        scan_data = scan_sector(cam_m, cam_l, cam_width, SEARCH_RES, current_depth)
        peak_m, peak_l, peak_val = find_hotspot(scan_data, cam_m, cam_l, cam_width)
        
        print(f"  Step {t}: Max Signal = {peak_val:.4f}")
        
        if peak_val > CHAOS_THRESHOLD:
            print(f"  >>> TATTLETALE TRIGGERED at ({peak_m:.2e}, {peak_l:.2e}) <<<")
            cam_m = peak_m
            cam_l = peak_l
            found = True
            break
            
        current_depth += 5 # Look deeper into time if we don't see anything yet
        
    if not found:
        print("FAILURE: No signal found within wait limit.")
        return

    # --- PHASE 2: THE DRILL DOWN ---
    print("[PHASE 2] Drilling down to target...")
    
    while cam_width > TARGET_ZOOM_WIDTH:
        # Zoom in by factor of 4
        cam_width /= 4.0
        print(f"  Zooming... Width now {cam_width:.2e}")
        
        # Re-scan to refine center
        # We use deeper physics as we zoom to ensure we hold the structure
        scan_data = scan_sector(cam_m, cam_l, cam_width, SEARCH_RES, current_depth)
        peak_m, peak_l, peak_val = find_hotspot(scan_data, cam_m, cam_l, cam_width)
        
        # Re-center
        cam_m = peak_m
        cam_l = peak_l
        
    print(f"  Target Acquired. Coordinates: ({cam_m:.6e}, {cam_l:.6e})")

    # --- PHASE 3: FILMING ---
    print(f"[PHASE 3] Filming {RECORD_FRAMES} frames in HD...")
    
    frames_buffer = []
    
    # Slew limiter to prevent shaking
    slew_rate = 0.2
    
    for f in range(RECORD_FRAMES):
        # 1. Render HD
        # Increment depth slightly to let time flow? 
        # Or keep constant depth to fly over static structure?
        # Let's let time flow a bit.
        render_depth = current_depth + (f // 2) 
        
        hd_data = scan_sector(cam_m, cam_l, cam_width, HD_RES, render_depth)
        
        # 2. Tracking Update (Keep following the head)
        peak_m, peak_l, peak_val = find_hotspot(hd_data, cam_m, cam_l, cam_width)
        
        # Smooth follow
        cam_m += (peak_m - cam_m) * slew_rate
        cam_l += (peak_l - cam_l) * slew_rate
        
        # 3. Create Image
        h_min, h_max = hd_data.min(), hd_data.max()
        if h_max == h_min: h_max += 1e-9
        norm = (hd_data - h_min) / (h_max - h_min)
        cm = plt.get_cmap('magma')
        colored = (cm(norm)[:, :, :3] * 255).astype(np.uint8)
        img = Image.fromarray(np.flipud(colored))
        
        # HUD
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), f"REC: {f}/{RECORD_FRAMES}", fill=(255, 0, 0))
        draw.text((10, 25), f"ZOOM: {cam_width:.2e}", fill=(200, 200, 200))
        draw.text((10, 40), f"DEPTH: {render_depth}", fill=(200, 200, 200))
        draw.rectangle([HD_RES//2-5, HD_RES//2-5, HD_RES//2+5, HD_RES//2+5], outline=(0,255,0))
        
        frames_buffer.append(img)
        
        if f % 10 == 0:
            print(f"  Frame {f} captured.")

    # SAVE
    print(f"Saving {OUTPUT_FILENAME}...")
    imageio.mimsave(OUTPUT_FILENAME, frames_buffer, fps=20)
    print("Done.")

if __name__ == "__main__":
    run_tattletale()