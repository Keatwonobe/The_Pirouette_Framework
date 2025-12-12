import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageOps
from collections import deque
import imageio.v2 as imageio

# =========================================================
#  PIROUETTE: HIGH-FIDELITY TRAJECTORY TRACER
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_wireform_trace.gif"
RENDER_FRAMES = 2500        # How many frames in the GIF
PHYSICS_SUBSTEPS = 10      # Physics updates per GIF frame (High precision tracking)

# TRACKING DYNAMICS
DEFAULT_ZOOM = 0.98        # Progressive Zoom
MAX_ZOOM_IN = 200.0        # Maximum magnification
TETHER_STIFFNESS = 0.4     # Aggressive tracking (Snaps to the "Tip")

# PHYSICS CONSTANTS
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 100
R_ESCAPE = 50.0
HELICITY_STOP = np.pi * 0.95
EPSILON = 1e-5

# VIEWPORT CONFIG
GLOBAL_EXTENT = 28000000.0 
GLOBAL_RES = 500            # Resolution of the Global Map
LOCAL_RES = 500             # Resolution of the Zoom Window

# Start at the edge where streaks usually enter
START_M = 0.0
START_L = 10000000.0 
START_WIDTH = 40000000.0    

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

    # Inline angular diff
    d_g = np.abs(angle_deg - 30.0);  d_g = np.minimum(d_g, 360.0-d_g)
    d_t = np.abs(angle_deg - 150.0); d_t = np.minimum(d_t, 360.0-d_t)
    d_r = np.abs(angle_deg - 270.0); d_r = np.minimum(d_r, 360.0-d_r)

    w_gold = np.exp(-(d_g / 80.0)**2)
    w_teal = np.exp(-(d_t / 80.0)**2)
    w_red  = np.exp(-(d_r / 80.0)**2)

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
        # Double step integration for precision
        for _ in range(2):
            Fm1, Flam1, w_red1 = get_force_numba(m1, l1)
            drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
            pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
            pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
            m1 += DT * pm1; l1 += DT * pl1

            Fm2, Flam2, w_red2 = get_force_numba(m2, l2)
            drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
            pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
            pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
            m2 += DT * pm2; l2 += DT * pl2

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
#  TRACKER LOGIC (SUB-STEPPED)
# =========================================================

class HighFidelityTracker:
    def __init__(self, start_m, start_l, start_width):
        self.m = start_m
        self.l = start_l
        self.width = start_width
        self.path_history = [] # List of (m, l) tuples
        
    def step_physics(self):
        # For the physics sub-step, we render a TINY grid just to find the peak
        # This is much faster than rendering a full view
        scan_res = 80 
        scan_data = render_view(self.m, self.l, self.width, scan_res)
        
        # Find the "Tip" (Max Helicity)
        idx = np.unravel_index(np.argmax(scan_data), scan_data.shape)
        
        # Convert to World Coords
        px_scale = self.width / (scan_res - 1)
        peak_l = (self.l - self.width/2.0) + idx[0] * px_scale
        peak_m = (self.m - self.width/2.0) + idx[1] * px_scale
        
        # Elastic Snap
        self.m += (peak_m - self.m) * TETHER_STIFFNESS
        self.l += (peak_l - self.l) * TETHER_STIFFNESS
        
        # Record High-Res Path point
        self.path_history.append((self.m, self.l))
        
        # Calculate Drift for Zoom Logic
        dist = np.sqrt((peak_m - self.m)**2 + (peak_l - self.l)**2)
        drift = dist / (self.width / 2.0)
        
        # Zoom Logic
        zoom = DEFAULT_ZOOM
        if drift > 0.3: zoom = 1.01 # Panicked zoom out
        if self.width > MAX_ZOOM_IN:
            self.width *= zoom

def array_to_image(data, cmap_name='magma'):
    d_min, d_max = data.min(), data.max()
    if d_max == d_min: d_max += 1e-9
    norm = (data - d_min) / (d_max - d_min)
    cm = plt.get_cmap(cmap_name)
    colored = cm(norm)
    img_data = (colored[:, :, :3] * 255).astype(np.uint8)
    return Image.fromarray(np.flipud(img_data))

# =========================================================
#  MAIN RENDER LOOP
# =========================================================

def run_trace():
    print("1. Baking Global Context Map (28M)...")
    # Using 'inferno' for the background to differentiate from the 'magma' zoom
    global_data = render_view(0.0, 0.0, GLOBAL_EXTENT * 2, GLOBAL_RES)
    global_img_base = array_to_image(global_data, 'inferno')
    
    # Darken the global map so the trail pops
    global_img_base = Image.eval(global_img_base, lambda x: x * 0.5)

    print(f"2. Initializing Tracker ({PHYSICS_SUBSTEPS} physics steps per frame)...")
    tracker = HighFidelityTracker(START_M, START_L, START_WIDTH)
    frames_buffer = []
    
    # Coordinate mapper for global view
    def world_to_px(m, l):
        # Map (-28M, 28M) to (0, GLOBAL_RES)
        norm_m = (m + GLOBAL_EXTENT) / (GLOBAL_EXTENT * 2)
        norm_l = (l + GLOBAL_EXTENT) / (GLOBAL_EXTENT * 2)
        px_x = int(norm_m * GLOBAL_RES)
        px_y = int(norm_l * GLOBAL_RES)
        # Flip Y for image coords
        return px_x, GLOBAL_RES - px_y

    for f in range(RENDER_FRAMES):
        
        # --- A. PHYSICS SUB-STEPPING ---
        # Run multiple tracker updates for every rendered frame
        # This builds the "Wireform" trail data
        for _ in range(PHYSICS_SUBSTEPS):
            tracker.step_physics()
            
        # --- B. RENDER LOCAL VIEW ---
        # Render high-quality local view
        local_data = render_view(tracker.m, tracker.l, tracker.width, LOCAL_RES)
        local_img = array_to_image(local_data, 'magma')
        
        # Add Crosshair
        draw_local = ImageDraw.Draw(local_img)
        cx, cy = LOCAL_RES//2, LOCAL_RES//2
        draw_local.line((cx-20, cy, cx+20, cy), fill=(0, 255, 255), width=1)
        draw_local.line((cx, cy-20, cx, cy+20), fill=(0, 255, 255), width=1)
        draw_local.text((10, 10), f"ZOOM: {tracker.width:.1e}", fill=(200, 255, 255))
        
        # --- C. RENDER GLOBAL TRAIL VIEW ---
        # Copy base map
        global_overlay = global_img_base.copy()
        draw_global = ImageDraw.Draw(global_overlay)
        
        # Draw the Trail (The Wireform)
        if len(tracker.path_history) > 1:
            # We draw the full history
            # Convert world coords to pixels
            points = [world_to_px(m, l) for m, l in tracker.path_history]
            
            # Draw line
            # We can just draw one continuous line
            draw_global.line(points, fill=(0, 255, 255), width=2)
            
            # Draw Current Position Dot (The Tip)
            curr_px = points[-1]
            r = 3
            draw_global.ellipse((curr_px[0]-r, curr_px[1]-r, curr_px[0]+r, curr_px[1]+r), fill=(255, 50, 50))

        # --- D. COMPOSITE ---
        combo_w = LOCAL_RES + GLOBAL_RES
        combo_h = max(LOCAL_RES, GLOBAL_RES)
        combo_img = Image.new('RGB', (combo_w, combo_h))
        combo_img.paste(local_img, (0, 0))
        combo_img.paste(global_overlay, (LOCAL_RES, 0))
        
        frames_buffer.append(combo_img)
        
        if f % 10 == 0:
            print(f"Frame {f}/{RENDER_FRAMES} | Trail Points: {len(tracker.path_history)}")

    print(f"Saving {OUTPUT_FILENAME}...")
    imageio.mimsave(OUTPUT_FILENAME, frames_buffer, fps=24)
    print("Done.")

if __name__ == "__main__":
    run_trace()