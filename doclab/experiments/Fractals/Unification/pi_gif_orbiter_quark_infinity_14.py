import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont

# =========================================================
#  HELICAL PLOTTER: DUAL-PANE TRAJECTORY MAPPING
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_helical_plotter.gif"
FRAMES = 140
RES = 400               # Resolution per pane (Total 800x400)
GLOBAL_SCALE = 25.0     # Fixed width for the Right Pane (The Map)

# PHYSICS
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

# TRACKER SETTINGS
TARGET_HINT = (0.0, -5.0)
START_WIDTH = 12.0
MIN_WIDTH = 0.05
SIGNAL_THRESHOLD = 0.001

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

def find_peak(img, width, center_m, center_l, search_ratio):
    res = img.shape[0]
    mid = res // 2
    px_r = int(res * search_ratio)
    Y, X = np.ogrid[:res, :res]
    dist = np.sqrt((X - mid)**2 + (Y - mid)**2)
    mask = dist <= px_r
    masked = img.copy()
    masked[~mask] = 0
    
    max_val = np.max(masked)
    idx = np.unravel_index(np.argmax(masked), img.shape)
    
    # Map pixel back to Math Coords
    pixel_l = (center_l - width/2) + idx[0] * (width / (res - 1))
    pixel_m = (center_m - width/2) + idx[1] * (width / (res - 1))
    return max_val, pixel_m, pixel_l

def coord_to_pixel(m, l, center_m, center_l, width, res):
    # Converts Math Coords -> Pixel Coords for drawing lines
    # x (col) = M, y (row) = L (inverted for display usually, but here matching array)
    
    # M maps to 0..res-1
    # Start of window: center_m - width/2
    m_start = center_m - width/2
    col = (m - m_start) / width * (res - 1)
    
    l_start = center_l - width/2
    row = (l - l_start) / width * (res - 1)
    
    return col, row

# --- THE DUAL MISSION ---

def run_cartographer():
    print("--- 🗺️ HELICAL CARTOGRAPHER ENGAGED ---")
    
    # State Vars
    cam_m, cam_l = TARGET_HINT
    curr_width = START_WIDTH
    
    # Physics Vars
    last_theta = np.arctan2(cam_l, cam_m)
    omega, alpha = 0.0, 0.0
    
    # History for the Linkage Trace
    # Format: [(m, l), (m, l), ...]
    trajectory_log = []
    
    frames_buffer = []
    
    # Initial Lock
    curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, 0)
    init_scan = render_microscope(cam_m, cam_l, 6.0, 100, curr_src_m, curr_src_l, 1.0)
    _, cam_m, cam_l = find_peak(init_scan, 6.0, cam_m, cam_l, 0.5)
    
    for f in range(FRAMES):
        # 1. Physics
        sys_theta = 2 * np.pi * (f / 100)
        src_m, src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.2)
        
        # 2. Sensor (Low Res)
        sensor_img = render_microscope(cam_m, cam_l, curr_width, 100, src_m, src_l, pulse)
        peak_val, peak_m, peak_l = find_peak(sensor_img, curr_width, cam_m, cam_l, 0.45)
        
        # 3. Logic (High-G Interceptor)
        is_visible = peak_val > SIGNAL_THRESHOLD
        
        if is_visible:
            # Velocity Check
            dist = np.sqrt((peak_m - cam_m)**2 + (peak_l - cam_l)**2)
            vel = dist / curr_width
            
            cam_m, cam_l = peak_m, peak_l
            
            # Angular Calc
            curr_theta = np.arctan2(cam_l, cam_m)
            diff = curr_theta - last_theta
            if diff > np.pi: diff -= 2*np.pi
            if diff < -np.pi: diff += 2*np.pi
            
            new_alpha = diff - omega
            alpha = 0.5*alpha + 0.5*new_alpha
            omega = diff
            last_theta = curr_theta
            
            # Zoom
            if vel > 0.10: curr_width *= 1.05
            elif curr_width > MIN_WIDTH: curr_width *= 0.95
        else:
            # Inertial
            pred_theta = last_theta + omega + alpha
            r = np.sqrt(cam_m**2 + cam_l**2)
            cam_m = r * np.cos(pred_theta)
            cam_l = r * np.sin(pred_theta)
            last_theta = pred_theta
            alpha *= 0.9

        # LOG POSITION
        trajectory_log.append((cam_m, cam_l))
        
        # -----------------------------
        # 4. RENDER: LEFT PANE (PILOT)
        # -----------------------------
        raw_pilot = render_microscope(cam_m, cam_l, curr_width, RES, src_m, src_l, pulse)
        # Normalize
        norm_p = (raw_pilot - raw_pilot.min()) / (raw_pilot.max() - raw_pilot.min() + 1e-9)
        norm_p = np.power(norm_p, 0.5)
        img_pilot = (plt.get_cmap('magma')(norm_p)[:, :, :3] * 255).astype(np.uint8)
        img_pilot = np.flipud(img_pilot)
        pil_pilot = Image.fromarray(img_pilot)
        
        # Pilot HUD
        d1 = ImageDraw.Draw(pil_pilot)
        d1.text((10, 10), "PILOT VIEW [TRACKING]", fill=(0, 255, 0))
        d1.rectangle([RES//2-10, RES//2-10, RES//2+10, RES//2+10], outline=(0,255,0))

        # -----------------------------
        # 5. RENDER: RIGHT PANE (MAP)
        # -----------------------------
        # Fixed Wide View centered at 0,0
        raw_map = render_microscope(0.0, 0.0, GLOBAL_SCALE, RES, src_m, src_l, pulse)
        norm_m = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
        norm_m = np.power(norm_m, 0.4) # Darker gamma for map
        # Use different colormap for contrast (viridis)
        img_map = (plt.get_cmap('viridis')(norm_m)[:, :, :3] * 255).astype(np.uint8)
        img_map = np.flipud(img_map)
        pil_map = Image.fromarray(img_map)
        
        d2 = ImageDraw.Draw(pil_map)
        d2.text((10, 10), "GLOBAL TRAJECTORY", fill=(0, 255, 255))
        
        # DRAW THE LINKAGE / PATH
        # We need to convert the trajectory log to pixel coordinates for the MAP view
        map_points = []
        for (tm, tl) in trajectory_log:
            # Map coords: Center=(0,0), Width=GLOBAL_SCALE
            # Note: Image origin is Top-Left. 
            # Col (x) increases with M. Row (y) decreases with L (usually).
            # My renderer maps: row index -> L, col index -> M.
            # But PIL draws (x, y). So x=col, y=row.
            
            # Since renderer uses linspace(min, max), index 0 is min value.
            # L min is bottom. So index 0 is bottom.
            # BUT Image.fromarray(np.flipud) puts index 0 at bottom visually? 
            # Let's trust the math:
            # If map center is 0,0:
            # M goes from -7.5 to 7.5.
            # L goes from -7.5 to 7.5.
            
            px_x = (tm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (RES - 1)
            # For L, we need to be careful with the flip.
            # If we flipped the image up/down, low L is at the bottom (high y).
            px_y = RES - 1 - ((tl - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (RES - 1))
            
            map_points.append((px_x, px_y))
            
        if len(map_points) > 1:
            d2.line(map_points, fill=(0, 255, 255), width=2)
            
        # Draw "Linkage" Vector (Origin to Current)
        cx, cy = RES//2, RES//2
        curr_x, curr_y = map_points[-1]
        d2.line([cx, cy, curr_x, curr_y], fill=(255, 50, 50), width=1) # The Radius Vector
        d2.ellipse([curr_x-3, curr_y-3, curr_x+3, curr_y+3], fill=(255, 255, 255)) # The Particle
        
        # -----------------------------
        # 6. COMBINE
        # -----------------------------
        combo = Image.new('RGB', (RES*2, RES))
        combo.paste(pil_pilot, (0, 0))
        combo.paste(pil_map, (RES, 0))
        
        frames_buffer.append(combo)
        
        if f % 10 == 0:
            print(f"Frame {f} | Orbit Radius: {np.sqrt(cam_m**2+cam_l**2):.2f}")

    print(f"Saving Helical Plot to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ PLOT COMPLETE.")

if __name__ == "__main__":
    run_cartographer()