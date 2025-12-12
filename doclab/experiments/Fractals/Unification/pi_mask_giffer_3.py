import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw
from collections import deque
import imageio.v2 as imageio # Explicit v2 to avoid warnings

# =========================================================
#  PIROUETTE: DUAL-VIEW ORBITER (Global + Local)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_dual_view.gif"
TOTAL_FRAMES = 250

# TRACKING DYNAMICS
DEFAULT_ZOOM = 0.975        # Zoom speed
MAX_ZOOM_IN = 20000.0         # Smallest window size
MIN_HISTORY = 3             
MAX_HISTORY = 12            
TETHER_STIFFNESS = 0.25     

# PHYSICS CONSTANTS
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 100             
R_ESCAPE = 50.0
HELICITY_STOP = np.pi * 0.95
EPSILON = 1e-5

# VIEWPORT CONFIG
# Global Map Range (The "28M" view)
GLOBAL_EXTENT = 28000000.0 
GLOBAL_RES = 400            # Resolution of the static map

# Tracker Start (Wide view, slightly off center to catch the edge)
START_M = 0.0
START_L = 0.0
START_WIDTH = 40000000.0    
RENDER_RES = 400            # Resolution of the tracker view

# =========================================================
#  NUMBA PHYSICS KERNEL
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

    def angle_dist(a, target):
        diff = np.abs(a - target)
        return np.minimum(diff, 360.0 - diff)

    diff_g = angle_dist(angle_deg, 30.0)
    w_gold = np.exp(-(diff_g / 80.0)**2)

    diff_t = angle_dist(angle_deg, 150.0)
    w_teal = np.exp(-(diff_t / 80.0)**2)

    diff_r = angle_dist(angle_deg, 270.0)
    w_red  = np.exp(-(diff_r / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6
    nw_red, nw_teal, nw_gold = w_red/tot, w_teal/tot, w_gold/tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam, nw_red

@njit(fastmath=True)
def normalize_angle_diff(delta):
    return np.arctan2(np.sin(delta), np.cos(delta))

@njit(fastmath=True)
def compute_pixel_helicity(m0, l0):
    m1, l1 = m0, l0
    m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm1, pl1 = 0.0, 0.0
    pm2, pl2 = 0.0, 0.0
    max_diff_angle = 0.0

    for _ in range(MAX_STEPS):
        # Real (Substep 1)
        Fm1, Flam1, w_red1 = get_force_numba(m1, l1)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
        m1 += DT * pm1; l1 += DT * pl1
        # Real (Substep 2)
        Fm1, Flam1, w_red1 = get_force_numba(m1, l1)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1

        # Shadow (Substep 1)
        Fm2, Flam2, w_red2 = get_force_numba(m2, l2)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
        m2 += DT * pm2; l2 += DT * pl2
        # Shadow (Substep 2)
        Fm2, Flam2, w_red2 = get_force_numba(m2, l2)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2

        ang1 = np.arctan2(l1, m1)
        ang2 = np.arctan2(l2, m2)
        diff = normalize_angle_diff(ang1 - ang2)
        adiff = np.abs(diff)
        if adiff > max_diff_angle: max_diff_angle = adiff
        
        if max_diff_angle > HELICITY_STOP: break
        if (m1**2 + l1**2) > R_ESCAPE: break

    return np.log(max_diff_angle + EPSILON)

@njit(parallel=True, fastmath=True)
def render_view(center_m, center_l, width, res):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    heatmap = np.zeros((res, res), dtype=np.float64)
    for i in prange(res):
        l_curr = l_vals[i]
        for j in range(res):
            m_curr = m_vals[j]
            heatmap[i, j] = compute_pixel_helicity(m_curr, l_curr)
    return heatmap

# =========================================================
#  TRACKER LOGIC
# =========================================================

class ElasticSolver:
    def __init__(self, start_m, start_l, start_width):
        self.m = start_m
        self.l = start_l
        self.width = start_width
        self.history = deque(maxlen=MAX_HISTORY)
        self.active_window_size = MAX_HISTORY
        self.drift_penalty = 0.0

    def update(self, heatmap, res):
        # Find Nexus
        idx = np.unravel_index(np.argmax(heatmap), heatmap.shape)
        px_scale = self.width / (res - 1)
        peak_l = (self.l - self.width/2.0) + idx[0] * px_scale
        peak_m = (self.m - self.width/2.0) + idx[1] * px_scale
        
        # History
        self.history.append((peak_m, peak_l))
        
        # Drift
        dist = np.sqrt((peak_m - self.m)**2 + (peak_l - self.l)**2)
        drift = dist / (self.width / 2.0)
        self.drift_penalty = drift
        
        # Memory Sizing
        target_win = MIN_HISTORY if drift > 0.2 else MAX_HISTORY
        if self.active_window_size > target_win: self.active_window_size -= 1
        elif self.active_window_size < target_win: self.active_window_size += 1
            
        # Move
        curr_hist = list(self.history)[-self.active_window_size:]
        if len(curr_hist) < 2:
            self.m += (peak_m - self.m)*0.5
            self.l += (peak_l - self.l)*0.5
            return

        self.m += (peak_m - self.m) * TETHER_STIFFNESS
        self.l += (peak_l - self.l) * TETHER_STIFFNESS
        
        # Zoom
        zoom = DEFAULT_ZOOM
        if drift > 0.4: zoom = 1.02
        if self.width > MAX_ZOOM_IN:
            self.width *= zoom

def array_to_image(data, cmap_name='magma'):
    # Normalize
    d_min, d_max = data.min(), data.max()
    if d_max == d_min: d_max += 1e-9
    norm = (data - d_min) / (d_max - d_min)
    
    cm = plt.get_cmap(cmap_name)
    colored = cm(norm)
    img_data = (colored[:, :, :3] * 255).astype(np.uint8)
    # Flip because physics origin is bottom-left, image is top-left
    return Image.fromarray(np.flipud(img_data))

# =========================================================
#  MAIN EXECUTION
# =========================================================

def run_dual_tracker():
    print("1. Generating Global Map (Context Layer)...")
    # Render the full "28M" basin once
    global_data = render_view(0.0, 0.0, GLOBAL_EXTENT * 2, GLOBAL_RES)
    global_img_base = array_to_image(global_data, 'magma')
    
    print("2. Initializing Tracker...")
    solver = ElasticSolver(START_M, START_L, START_WIDTH)
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        # --- A. Render Tracker View ---
        local_data = render_view(solver.m, solver.l, solver.width, RENDER_RES)
        solver.update(local_data, RENDER_RES)
        
        local_img = array_to_image(local_data, 'magma')
        
        # --- B. Create HUD for Local View ---
        draw_local = ImageDraw.Draw(local_img)
        cx, cy = RENDER_RES//2, RENDER_RES//2
        draw_local.line((cx-10, cy, cx+10, cy), fill=(0, 255, 0), width=1)
        draw_local.line((cx, cy-10, cx, cy+10), fill=(0, 255, 0), width=1)
        draw_local.text((10, 10), f"ZOOM WIDTH: {solver.width:.2e}", fill=(100, 255, 100))
        
        # --- C. Create HUD for Global View ---
        # Copy the base map so we don't draw over the original
        global_overlay = global_img_base.copy()
        draw_global = ImageDraw.Draw(global_overlay)
        
        # Calculate bounding box of current view on global map
        # Global Map spans (-GLOBAL_EXTENT, +GLOBAL_EXTENT)
        g_min = -GLOBAL_EXTENT
        g_range = GLOBAL_EXTENT * 2
        
        # Current view bounds
        view_left = solver.m - solver.width/2
        view_right = solver.m + solver.width/2
        view_bottom = solver.l - solver.width/2
        view_top = solver.l + solver.width/2
        
        # Map to pixels (0 to GLOBAL_RES)
        def world_to_px(val, is_y=False):
            norm = (val - g_min) / g_range
            px = int(norm * GLOBAL_RES)
            if is_y: px = GLOBAL_RES - px # Flip Y
            return px
            
        px_l = world_to_px(view_left)
        px_r = world_to_px(view_right)
        px_b = world_to_px(view_bottom, is_y=True) # Bottom in physics is high pixel index
        px_t = world_to_px(view_top, is_y=True)    # Top in physics is low pixel index
        
        # Ensure the box is at least visible (min 2x2 pixels)
        if px_r - px_l < 2: px_r = px_l + 2
        if px_b - px_t < 2: px_b = px_t + 2
        
        # Draw Box
        draw_global.rectangle([px_l, px_t, px_r, px_b], outline=(0, 255, 0), width=2)
        draw_global.text((10, 10), "GLOBAL CONTEXT (28M)", fill=(200, 200, 200))

        # --- D. Stitch Views ---
        # Create composite image (Local on Left, Global on Right)
        combo_w = RENDER_RES + GLOBAL_RES
        combo_h = max(RENDER_RES, GLOBAL_RES)
        combo_img = Image.new('RGB', (combo_w, combo_h))
        combo_img.paste(local_img, (0, 0))
        combo_img.paste(global_overlay, (RENDER_RES, 0))
        
        frames_buffer.append(combo_img)
        
        if f % 10 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | Zoom: {solver.width:.2e}")

    print(f"Saving {OUTPUT_FILENAME}...")
    imageio.mimsave(OUTPUT_FILENAME, frames_buffer, fps=20)
    print("Done.")

if __name__ == "__main__":
    run_dual_tracker()