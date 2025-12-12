import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont
from collections import deque
import os

# =========================================================
#  PIROUETTE: PROTON BASIN ORBITER (Chaos Tracker)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_nexus_tracker.gif"
TOTAL_FRAMES = 200

# TRACKING DYNAMICS
DEFAULT_ZOOM = 0.98         # Gently zoom in to resolve geometry
MAX_ZOOM_IN = 25.0         # How small can the window get? (World units)
MIN_HISTORY = 3             # React fast to sudden streaks
MAX_HISTORY = 10            # Smooth out jitter in open space
TETHER_STIFFNESS = 0.25     # High stiffness to catch fast streaks

# PHYSICS CONSTANTS (Matches your pi_scanner.py)
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 100             # Depth of simulation per pixel
R_ESCAPE = 50.0
HELICITY_STOP = np.pi * 0.95
EPSILON = 1e-5

# VIEWPORT INIT (Start Wide)
START_M = 0.0
START_L = 0.0
START_WIDTH = 8.0    # 40 Million unit width (Matches your 24M plot)

# =========================================================
#  NUMBA KERNEL (THE PHYSICS ENGINE)
# =========================================================

@njit(fastmath=True)
def get_force_numba(m, lam):
    # Teal Field
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red Field (Parity Violation)
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold Field (Nonlinear)
    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2 + 1e-12)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    # Angular weights
    angle_rad = np.arctan2(lam, m)
    angle_deg = np.degrees(angle_rad) % 360.0

    # Inline angular diff
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

    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam, nw_red

@njit(fastmath=True)
def normalize_angle_diff(delta):
    return np.arctan2(np.sin(delta), np.cos(delta))

@njit(fastmath=True)
def compute_pixel_helicity(m0, l0):
    m1, l1 = m0, l0
    pm1, pl1 = 0.0, 0.0

    m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm2, pl2 = 0.0, 0.0

    max_diff_angle = 0.0

    for _ in range(MAX_STEPS):
        # --- Real Trajectory (Double Step for Precision) ---
        # Sub-step 1
        Fm1, Flam1, w_red1 = get_force_numba(m1, l1)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
        m1 += DT * pm1
        l1 += DT * pl1
        
        # Sub-step 2
        Fm1, Flam1, w_red1 = get_force_numba(m1, l1)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
        
        # --- Shadow Trajectory (Double Step) ---
        # Sub-step 1
        Fm2, Flam2, w_red2 = get_force_numba(m2, l2)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
        m2 += DT * pm2
        l2 += DT * pl2

        # Sub-step 2
        Fm2, Flam2, w_red2 = get_force_numba(m2, l2)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2

        # --- Measure Divergence ---
        ang1 = np.arctan2(l1, m1)
        ang2 = np.arctan2(l2, m2)
        diff = normalize_angle_diff(ang1 - ang2)
        adiff = np.abs(diff)
        
        if adiff > max_diff_angle:
            max_diff_angle = adiff

        # Early exit if chaos is maximized or escaped
        if max_diff_angle > HELICITY_STOP:
            break
        if (m1**2 + l1**2) > R_ESCAPE:
            break

    return np.log(max_diff_angle + EPSILON)

@njit(parallel=True, fastmath=True)
def render_basin_view(center_m, center_l, width, res):
    half_w = width / 2.0
    # Create coordinate arrays
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    heatmap = np.zeros((res, res), dtype=np.float64)
    
    # Parallel scan
    for i in prange(res):
        l_curr = l_vals[i]
        for j in range(res):
            m_curr = m_vals[j]
            heatmap[i, j] = compute_pixel_helicity(m_curr, l_curr)
            
    return heatmap

# =========================================================
#  ELASTIC ORBITER LOGIC (Camera Control)
# =========================================================

class ElasticSolver:
    def __init__(self, start_m, start_l, start_width):
        self.m = start_m
        self.l = start_l
        self.width = start_width
        self.history = deque(maxlen=MAX_HISTORY)
        self.active_window_size = MAX_HISTORY
        self.drift_penalty = 0.0
        self.tangent_angle = 0.0

    def update(self, heatmap, res):
        # 1. Find the "Nexus" (Max Chaos)
        # We want to fly towards the brightest spot (highest helicity)
        idx = np.unravel_index(np.argmax(heatmap), heatmap.shape)
        
        # Pixel to World transform
        px_scale = self.width / (res - 1)
        
        # Note: heatmap is (y, x) -> (l, m)
        # l is row (idx[0]), m is col (idx[1])
        # Image coordinates usually start top-left, but physics is bottom-left.
        # We need to match the linspace generation order.
        # l_vals went from min to max, so index 0 is bottom.
        
        peak_l = (self.l - self.width/2.0) + idx[0] * px_scale
        peak_m = (self.m - self.width/2.0) + idx[1] * px_scale
        
        # 2. Add to History
        self.history.append((peak_m, peak_l))
        
        # 3. Calculate Drift (Error from center)
        dist_from_center = np.sqrt((peak_m - self.m)**2 + (peak_l - self.l)**2)
        drift_ratio = dist_from_center / (self.width / 2.0)
        self.drift_penalty = drift_ratio
        
        # 4. Adaptive Window (Shorten memory if erratic)
        target_window = MIN_HISTORY if drift_ratio > 0.2 else MAX_HISTORY
        if self.active_window_size > target_window: self.active_window_size -= 1
        elif self.active_window_size < target_window: self.active_window_size += 1
            
        # 5. Solve Motion
        curr_history = list(self.history)[-self.active_window_size:]
        if len(curr_history) < 2:
            # Jump start
            self.m += (peak_m - self.m) * 0.5
            self.l += (peak_l - self.l) * 0.5
            return

        # Simple predictive tracking
        p_now = np.array(curr_history[-1])
        # P_target is the weighted average of where we are and where the peak is
        # Strong pull towards peak (Tether)
        
        # Elastic mix
        target_m = peak_m
        target_l = peak_l
        
        # Apply camera slew
        self.m += (target_m - self.m) * TETHER_STIFFNESS
        self.l += (target_l - self.l) * TETHER_STIFFNESS
        
        # 6. Zoom Logic
        # Zoom in naturally, but back off if we lose the target
        zoom_factor = DEFAULT_ZOOM
        if drift_ratio > 0.4: zoom_factor = 1.02 # Back off!
        
        if self.width > MAX_ZOOM_IN:
            self.width *= zoom_factor

# =========================================================
#  MAIN EXECUTION
# =========================================================

def run_tracker():
    print(f"--- 📡 PROTON BASIN: NEXUS TRACKER INITIATED ---")
    print(f"Tracking high-divergence streaks in {START_WIDTH:.1e} unit space.")

    solver = ElasticSolver(START_M, START_L, START_WIDTH)
    frames_buffer = []
    
    # Resolution for the tracker/GIF
    # Lower res for speed, but high enough to find the streak
    RENDER_RES = 300 
    
    for f in range(TOTAL_FRAMES):
        # 1. Render Physics
        heatmap = render_basin_view(solver.m, solver.l, solver.width, RENDER_RES)
        
        # 2. Update Drone Position
        solver.update(heatmap, RENDER_RES)
        
        # 3. Visualization
        # Normalize for display
        # Log scale handled in physics, so just min/max here
        h_min, h_max = heatmap.min(), heatmap.max()
        if h_max == h_min: h_max += 1e-9
        
        norm = (heatmap - h_min) / (h_max - h_min)
        
        # Apply colormap (Magma is great for 'heat')
        cm = plt.get_cmap('magma')
        colored = cm(norm)
        
        # Convert to PIL
        img_data = (colored[:, :, :3] * 255).astype(np.uint8)
        # Flip origin to bottom-left match physics
        img_data = np.flipud(img_data) 
        panel = Image.fromarray(img_data)
        
        # 4. HUD Overlay
        draw = ImageDraw.Draw(panel)
        
        # Crosshair
        cx, cy = RENDER_RES//2, RENDER_RES//2
        draw.line((cx-10, cy, cx+10, cy), fill=(0, 255, 0), width=1)
        draw.line((cx, cy-10, cx, cy+10), fill=(0, 255, 0), width=1)
        
        # Text Info
        info_color = (100, 255, 100) # Terminal Green
        draw.text((10, 10), f"FRAME: {f}", fill=info_color)
        draw.text((10, 20), f"POS: {solver.m:.2e}, {solver.l:.2e}", fill=info_color)
        draw.text((10, 30), f"WIDTH: {solver.width:.2e}", fill=info_color)
        draw.text((10, 40), f"TENSION: {solver.drift_penalty*100:.1f}%", fill=info_color)

        frames_buffer.append(panel)
        
        if f % 10 == 0:
            print(f"[TRACKER] Frame {f}/{TOTAL_FRAMES} | Width: {solver.width:.2e} | Tension: {solver.drift_penalty:.2f}")

    # Save GIF
    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("Done.")

if __name__ == "__main__":
    run_tracker()