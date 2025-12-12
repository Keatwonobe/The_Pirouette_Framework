import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont 
import imageio.v2 as imageio

# =========================================================
#  PIROUETTE: NIGHT VISION PROTOCOL (COLOR MODE FIXED)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_night_vision.gif"

# DYNAMICS
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
EPSILON = 1e-5
R_ESCAPE = 100.0
HELICITY_STOP = np.pi * 0.95

# SEARCH PARAMETERS
GLOBAL_SEARCH_WIDTH = 50000000.0 
SEARCH_RES = 150                 
START_STEPS = 50                 
STEP_INCREMENT = 50              
MAX_SEARCH_LOOPS = 25            

# VISUALIZATION
TARGET_ZOOM_WIDTH = 1500000.0    
HD_RES = 400                     
GLOBAL_RES = 400                 
RECORD_FRAMES = 120              

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
    m1, l1 = m0, l0
    m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm1, pl1 = 0.0, 0.0
    pm2, pl2 = 0.0, 0.0
    max_diff_angle = 0.0
    
    for _ in range(steps):
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
        
        if (m1**2 + l1**2) > R_ESCAPE: 
            return 10.0 

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
#  NIGHT VISION ENGINE (High Gain Normalization)
# =========================================================

def night_vision_normalize(data, cmap_name='magma'):
    structure_mask = data < 5.0
    
    if not np.any(structure_mask):
        # FIX: Explicitly set mode='RGB'
        solid_img = Image.fromarray((data * 0 + 255).astype(np.uint8), mode='RGB')
        return solid_img, 0.0, 0.0
        
    structure_data = data[structure_mask]
    
    v_min = np.percentile(structure_data, 1)  
    v_max = np.percentile(structure_data, 99) 
    
    if v_max <= v_min: v_max = v_min + 1e-9
    
    clipped = np.clip(data, v_min, v_max)
    norm = (clipped - v_min) / (v_max - v_min)
    
    cm = plt.get_cmap(cmap_name)
    colored = (cm(norm)[:, :, :3] * 255).astype(np.uint8)
    
    # FIX: Explicitly set mode='RGB'
    return Image.fromarray(np.flipud(colored), mode='RGB'), v_min, v_max

def find_variance_hotspot(heatmap, center_m, center_l, width):
    if np.std(heatmap) < 1e-6:
        return center_m, center_l, heatmap[heatmap.shape[0]//2, heatmap.shape[1]//2]

    gy, gx = np.gradient(heatmap)
    magnitude = np.sqrt(gx**2 + gy**2)
    
    idx = np.unravel_index(np.argmax(magnitude), magnitude.shape)
    
    res = heatmap.shape[0]
    px_scale = width / (res - 1)
    
    peak_l = (center_l - width/2.0) + idx[0] * px_scale
    peak_m = (center_m - width/2.0) + idx[1] * px_scale
    
    return peak_m, peak_l, heatmap[idx]

# =========================================================
#  MAIN PROTOCOL
# =========================================================

def run_night_vision():
    # Load a default font for stable text drawing
    try:
        font = ImageFont.load_default()
    except IOError:
        font = None
        print("Warning: Could not load default font.")

    print("--- 🌙 PIROUETTE: NIGHT VISION PROTOCOL ---")
    
    # 1. BAKE GLOBAL MAP
    print("Generating Global Context...")
    global_data = scan_sector(0.0, 0.0, GLOBAL_SEARCH_WIDTH, GLOBAL_RES, 60)
    global_img, _, _ = night_vision_normalize(global_data, 'inferno') 
    
    global_img = Image.eval(global_img, lambda x: x * 0.6)

    cam_m = 0.0
    cam_l = 0.0
    cam_width = GLOBAL_SEARCH_WIDTH
    current_steps = START_STEPS
    
    # --- PHASE 1: HUNT ---
    print("Hunting for structure...")
    found = False
    
    for attempt in range(MAX_SEARCH_LOOPS):
        scan_data = scan_sector(cam_m, cam_l, cam_width, SEARCH_RES, current_steps)
        peak_m, peak_l, peak_val = find_variance_hotspot(scan_data, cam_m, cam_l, cam_width)
        
        if peak_val > -10.0: 
            print(f"  >>> SIGNAL FOUND: {peak_val:.4f} (Steps: {current_steps})")
            cam_m, cam_l = peak_m, peak_l
            found = True
            break
            
        print(f"  Scanning... Best Signal: {peak_val:.4f} (Steps: {current_steps})")
        current_steps += STEP_INCREMENT

    if not found:
        print("Using default deep probe...")
        current_steps = 250

    # --- PHASE 2: DRILL ---
    print("Drilling down...")
    while cam_width > TARGET_ZOOM_WIDTH:
        cam_width /= 2.0
        scan_data = scan_sector(cam_m, cam_l, cam_width, SEARCH_RES, current_steps)
        cam_m, cam_l, _ = find_variance_hotspot(scan_data, cam_m, cam_l, cam_width)

    print(f"Locked. Recording with High Gain.")

    # --- PHASE 3: RECORD ---
    frames_buffer = []
    
    def world_to_px(m, l):
        g_min = -GLOBAL_SEARCH_WIDTH / 2.0
        g_range = GLOBAL_SEARCH_WIDTH
        px_x = int(((m - g_min) / g_range) * GLOBAL_RES)
        px_y = int(((l - g_min) / g_range) * GLOBAL_RES)
        return px_x, GLOBAL_RES - px_y 

    for f in range(RECORD_FRAMES):
        
        # A. Render Local (High Gain)
        hd_data = scan_sector(cam_m, cam_l, cam_width, HD_RES, current_steps)
        local_img, vmin, vmax = night_vision_normalize(hd_data, 'magma')
        
        # Tracking
        p_m, p_l, _ = find_variance_hotspot(hd_data, cam_m, cam_l, cam_width)
        cam_m += (p_m - cam_m) * 0.15
        cam_l += (p_l - cam_l) * 0.15
        
        # HUD Local
        draw_local = ImageDraw.Draw(local_img)
        gain_str = f"Rg: [{vmin:.1f}, {vmax:.1f}]"
        
        draw_local.text((10, 10), f"REC: {f}", fill=(255, 100, 100), font=font)
        draw_local.text((10, 25), f"ZOOM: {cam_width:.1e}", fill=(200, 255, 200), font=font)
        draw_local.text((10, 40), gain_str, fill=(200, 255, 200), font=font)
        
        # B. Global Radar
        radar_img = global_img.copy()
        draw_radar = ImageDraw.Draw(radar_img)
        px, py = world_to_px(cam_m, cam_l)
        
        # Probe Marker
        r_size = 20
        draw_radar.ellipse((px-5, py-5, px+5, py+5), fill=(0, 255, 0))
        draw_radar.line((px-r_size, py, px+r_size, py), fill=(0, 255, 0), width=1)
        draw_radar.line((px, py-r_size, px, py+r_size), fill=(0, 255, 0), width=1)
        
        draw_radar.text((10, 10), "GLOBAL CONTEXT", fill=(100, 255, 100), font=font)

        # C. Stitch
        combo_w = HD_RES + GLOBAL_RES
        combo_h = max(HD_RES, GLOBAL_RES)
        combo = Image.new('RGB', (combo_w, combo_h))
        combo.paste(local_img, (0, 0))
        combo.paste(radar_img, (HD_RES, 0))
        
        frames_buffer.append(combo)
        
        # Evolve time
        if f % 2 == 0:
            current_steps += 1
            
        if f % 20 == 0:
            print(f"Frame {f}/{RECORD_FRAMES}")

    print(f"Saving {OUTPUT_FILENAME}...")
    imageio.mimsave(OUTPUT_FILENAME, frames_buffer, fps=20)
    print("Done.")

if __name__ == "__main__":
    run_night_vision()