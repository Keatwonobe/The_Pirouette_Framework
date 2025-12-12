import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw
import imageio.v2 as imageio

# =========================================================
#  PIROUETTE: DEEP TIME DUAL-VIEW
#  (Tattletale Logic + Global Radar)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_dual_tattletale.gif"

# DYNAMICS
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
EPSILON = 1e-5
R_ESCAPE = 100.0
HELICITY_STOP = np.pi * 0.95

# SEARCH PARAMETERS
GLOBAL_SEARCH_WIDTH = 50000000.0 
SEARCH_RES = 150                 # Speed > Quality for hunting
START_STEPS = 50                 
STEP_INCREMENT = 50              
MAX_SEARCH_LOOPS = 20            

# FILMING PARAMETERS
TARGET_ZOOM_WIDTH = 1000000.0    # Final zoom level
HD_RES = 400                     # Left Panel Resolution
GLOBAL_RES = 400                 # Right Panel Resolution
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
        for _ in range(2): # Double step
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
        
        # If escaped, return a distinct high value
        if (m1**2 + l1**2) > R_ESCAPE: 
            return 5.0 

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
#  VISUALIZATION ENGINE
# =========================================================

def array_to_image(data, cmap_name='magma'):
    # SMART NORMALIZATION
    # 1. Clamp the "Escape" values (5.0) down so they don't hide the fractal
    # Most chaos is around -2 to 0.5. Escape is 5.0.
    # We clip at 1.0 to keep the gradient visible.
    clipped = np.clip(data, -12.0, 1.0)
    
    d_min, d_max = clipped.min(), clipped.max()
    if d_max == d_min: d_max += 1e-9
    
    norm = (clipped - d_min) / (d_max - d_min)
    
    cm = plt.get_cmap(cmap_name)
    colored = (cm(norm)[:, :, :3] * 255).astype(np.uint8)
    return Image.fromarray(np.flipud(colored))

def find_edge_hotspot(heatmap, center_m, center_l, width):
    """
    Finds the area with the highest VARIANCE (Edge), not just brightness.
    This prevents zooming into solid black or solid white.
    """
    # Simple edge detection via gradients
    gy, gx = np.gradient(heatmap)
    magnitude = np.sqrt(gx**2 + gy**2)
    
    idx = np.unravel_index(np.argmax(magnitude), magnitude.shape)
    
    res = heatmap.shape[0]
    px_scale = width / (res - 1)
    
    peak_l = (center_l - width/2.0) + idx[0] * px_scale
    peak_m = (center_m - width/2.0) + idx[1] * px_scale
    
    # Return the max value of the original map at this edge location
    return peak_m, peak_l, heatmap[idx]

# =========================================================
#  MAIN PROTOCOL
# =========================================================

def run_dual_tattletale():
    print("--- 📡 PIROUETTE: DUAL-VIEW TATTLETALE ---")
    
    # 1. BAKE GLOBAL MAP
    print("Generating Global Radar Map (50M)...")
    # We use a shallow depth for the map just to show context
    global_data = scan_sector(0.0, 0.0, GLOBAL_SEARCH_WIDTH, GLOBAL_RES, 50)
    global_base_img = array_to_image(global_data, 'inferno')
    # Dim it slightly
    global_base_img = Image.eval(global_base_img, lambda x: x * 0.6)

    cam_m = 0.0
    cam_l = 0.0
    cam_width = GLOBAL_SEARCH_WIDTH
    current_steps = START_STEPS
    
    # --- PHASE 1: HUNT FOR TIME ---
    print("Searching for instability...")
    found = False
    for attempt in range(MAX_SEARCH_LOOPS):
        scan_data = scan_sector(cam_m, cam_l, cam_width, SEARCH_RES, current_steps)
        peak_m, peak_l, peak_val = find_edge_hotspot(scan_data, cam_m, cam_l, cam_width)
        
        print(f"  Steps: {current_steps} | Signal: {peak_val:.4f}")
        
        # If we see variance/chaos significantly above the noise floor (-11)
        if peak_val > -5.0:
            print("  >>> ANOMALY DETECTED <<<")
            cam_m, cam_l = peak_m, peak_l
            found = True
            break
        current_steps += STEP_INCREMENT

    if not found:
        print("System stable. Defaulting to center for demo.")
        current_steps = 200 # Force it deep

    # --- PHASE 2: DRILL DOWN ---
    print("Drilling down...")
    while cam_width > TARGET_ZOOM_WIDTH:
        cam_width /= 2.0
        scan_data = scan_sector(cam_m, cam_l, cam_width, SEARCH_RES, current_steps)
        # Re-center on the most complex part
        cam_m, cam_l, _ = find_edge_hotspot(scan_data, cam_m, cam_l, cam_width)

    print(f"Locked at ({cam_m:.2e}, {cam_l:.2e}). Starting Dual-View Record.")

    # --- PHASE 3: RECORDING ---
    frames_buffer = []
    
    # Coordinate mapper for Radar
    def world_to_px(m, l):
        g_min = -GLOBAL_SEARCH_WIDTH / 2.0
        g_range = GLOBAL_SEARCH_WIDTH
        px_x = int(((m - g_min) / g_range) * GLOBAL_RES)
        px_y = int(((l - g_min) / g_range) * GLOBAL_RES)
        return px_x, GLOBAL_RES - px_y # Flip Y

    for f in range(RECORD_FRAMES):
        
        # A. Render Local HD
        hd_data = scan_sector(cam_m, cam_l, cam_width, HD_RES, current_steps)
        local_img = array_to_image(hd_data, 'magma')
        
        # Tracking update (Keep following the complexity)
        p_m, p_l, _ = find_edge_hotspot(hd_data, cam_m, cam_l, cam_width)
        cam_m += (p_m - cam_m) * 0.1
        cam_l += (p_l - cam_l) * 0.1
        
        # HUD Local
        draw_local = ImageDraw.Draw(local_img)
        draw_local.text((10, 10), f"REC: {f}", fill=(255, 0, 0))
        draw_local.text((10, 25), f"ZOOM: {cam_width:.1e}", fill=(200, 200, 200))
        
        # B. Render Global Radar
        radar_img = global_base_img.copy()
        draw_radar = ImageDraw.Draw(radar_img)
        
        # Draw Probe Location
        px, py = world_to_px(cam_m, cam_l)
        
        # Crosshair on Radar
        r_size = 15
        draw_radar.line((px-r_size, py, px+r_size, py), fill=(0, 255, 0), width=2)
        draw_radar.line((px, py-r_size, px, py+r_size), fill=(0, 255, 0), width=2)
        draw_radar.text((10, 10), "GLOBAL CONTEXT", fill=(0, 255, 0))
        draw_radar.text((10, 25), f"POS: {cam_m:.1e}, {cam_l:.1e}", fill=(0, 255, 0))

        # C. Stitch
        combo_w = HD_RES + GLOBAL_RES
        combo_h = max(HD_RES, GLOBAL_RES)
        combo = Image.new('RGB', (combo_w, combo_h))
        combo.paste(local_img, (0, 0))
        combo.paste(radar_img, (HD_RES, 0))
        
        frames_buffer.append(combo)
        
        # Evolve time slowly
        if f % 2 == 0:
            current_steps += 1
            
        if f % 10 == 0:
            print(f"Frame {f}/{RECORD_FRAMES}")

    print(f"Saving {OUTPUT_FILENAME}...")
    imageio.mimsave(OUTPUT_FILENAME, frames_buffer, fps=20)
    print("Done.")

if __name__ == "__main__":
    run_dual_tattletale()