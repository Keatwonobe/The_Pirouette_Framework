import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont

# =========================================================
#  TRINITY TRACKER: STRUCTURAL ANALYSIS
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_structure_trinity.gif"
FRAMES = 140
GLOBAL_SCALE = 25.0     # Wide angle to see all 3
PILOT_RES = 150         # Resolution of small side panels
MAP_RES = 450           # Resolution of main map

# PHYSICS
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

# INITIAL GUESSES (Approximate locations of the 3 sources)
# Based on the SRC arrays: (-10, 5), (10, 5), (0, -10)
HINTS = [
    (-10.0, 5.0), # Quark 1
    (10.0, 5.0),  # Quark 2
    (0.0, -10.0)  # Quark 3
]

COLORS = [
    (0, 255, 255), # Cyan
    (255, 0, 255), # Magenta
    (255, 255, 0)  # Yellow
]

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
    
    pixel_l = (center_l - width/2) + idx[0] * (width / (res - 1))
    pixel_m = (center_m - width/2) + idx[1] * (width / (res - 1))
    return max_val, pixel_m, pixel_l

# --- TRACKER CLASS ---

class QuarkTracker:
    def __init__(self, hint, quark_id):
        self.id = quark_id
        self.cam_m, self.cam_l = hint
        self.width = 8.0 # Start moderately wide
        self.min_width = 0.05
        
        # Dynamics
        self.last_theta = np.arctan2(self.cam_l, self.cam_m)
        self.omega = 0.0
        self.alpha = 0.0
        
        self.history = [] # List of (m, l)
        self.locked = False
        
    def update(self, sys_src_m, sys_src_l, pulse):
        # 1. Render Sensor
        sensor_img = render_microscope(self.cam_m, self.cam_l, self.width, 100, sys_src_m, sys_src_l, pulse)
        
        # 2. Find Peak
        peak_val, peak_m, peak_l = find_peak(sensor_img, self.width, self.cam_m, self.cam_l, 0.45)
        self.locked = peak_val > 0.001
        
        if self.locked:
            # Velocity Check
            dist = np.sqrt((peak_m - self.cam_m)**2 + (peak_l - self.cam_l)**2)
            vel = dist / self.width
            
            self.cam_m, self.cam_l = peak_m, peak_l
            
            # Angular Dynamics
            curr_theta = np.arctan2(self.cam_l, self.cam_m)
            diff = curr_theta - self.last_theta
            if diff > np.pi: diff -= 2*np.pi
            if diff < -np.pi: diff += 2*np.pi
            
            new_alpha = diff - self.omega
            self.alpha = 0.5*self.alpha + 0.5*new_alpha
            self.omega = diff
            self.last_theta = curr_theta
            
            # Adaptive Zoom
            if vel > 0.10: self.width *= 1.05
            elif self.width > self.min_width: self.width *= 0.95
            
        else:
            # Inertial Prediction
            pred_theta = self.last_theta + self.omega + self.alpha
            r = np.sqrt(self.cam_m**2 + self.cam_l**2)
            self.cam_m = r * np.cos(pred_theta)
            self.cam_l = r * np.sin(pred_theta)
            self.last_theta = pred_theta
            self.alpha *= 0.9
            
        self.history.append((self.cam_m, self.cam_l))

    def render_view(self, sys_src_m, sys_src_l, pulse):
        raw = render_microscope(self.cam_m, self.cam_l, self.width, PILOT_RES, sys_src_m, sys_src_l, pulse)
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.5)
        
        # Colorize based on Quark ID
        base_color = np.array(COLORS[self.id]) / 255.0
        # Create RGB by multiplying grayscale norm by color vector
        img_rgb = np.dstack((norm * base_color[0], norm * base_color[1], norm * base_color[2]))
        
        img_uint8 = (img_rgb * 255).astype(np.uint8)
        img_uint8 = np.flipud(img_uint8)
        pil = Image.fromarray(img_uint8)
        
        d = ImageDraw.Draw(pil)
        status = "LOCKED" if self.locked else "PREDICT"
        d.text((5, 5), f"Q{self.id+1}: {status}", fill=COLORS[self.id])
        return pil

# --- MAIN MISSION ---

def run_trinity():
    print("--- ⚠️ TRINITY PROTOCOL INITIATED ---")
    
    # Initialize Trackers
    trackers = [QuarkTracker(h, i) for i, h in enumerate(HINTS)]
    
    frames_buffer = []
    
    # Find Initial Locks
    curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, 0)
    for t in trackers:
        # Pre-scan to snap to closest peak
        scan = render_microscope(t.cam_m, t.cam_l, 8.0, 100, curr_src_m, curr_src_l, 1.0)
        _, t.cam_m, t.cam_l = find_peak(scan, 8.0, t.cam_m, t.cam_l, 0.5)
    
    for f in range(FRAMES):
        sys_theta = 2 * np.pi * (f / 100)
        src_m, src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.2)
        
        # 1. Update Trackers
        for t in trackers:
            t.update(src_m, src_l, pulse)
            
        # 2. Render Pilot Views
        pilot_imgs = [t.render_view(src_m, src_l, pulse) for t in trackers]
        
        # 3. Render Global Map
        raw_map = render_microscope(0.0, 0.0, GLOBAL_SCALE, MAP_RES, src_m, src_l, pulse)
        norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
        norm_map = np.power(norm_map, 0.4)
        img_map = (plt.get_cmap('inferno')(norm_map)[:, :, :3] * 255).astype(np.uint8)
        img_map = np.flipud(img_map)
        pil_map = Image.fromarray(img_map)
        
        d_map = ImageDraw.Draw(pil_map)
        
        # 4. Draw Geometry
        current_points_px = []
        
        for t in trackers:
            # Draw Trail
            points = []
            for (tm, tl) in t.history:
                px = (tm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_RES - 1)
                py = MAP_RES - 1 - ((tl - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_RES - 1))
                points.append((px, py))
            
            if len(points) > 1:
                d_map.line(points, fill=COLORS[t.id], width=2)
                
            # Store current point for Triangle
            current_points_px.append(points[-1])
            
            # Draw Head
            cx, cy = points[-1]
            r = 4
            d_map.ellipse([cx-r, cy-r, cx+r, cy+r], fill=COLORS[t.id], outline=(255,255,255))

        # Draw Structural Triangle (Linkage)
        if len(current_points_px) == 3:
            d_map.polygon(current_points_px, outline=(255, 255, 255), width=1)
            
            # Calculate Centroid
            cent_x = sum(p[0] for p in current_points_px) / 3
            cent_y = sum(p[1] for p in current_points_px) / 3
            d_map.line([cent_x-5, cent_y, cent_x+5, cent_y], fill=(255,255,255))
            d_map.line([cent_x, cent_y-5, cent_x, cent_y+5], fill=(255,255,255))

        # 5. Composite
        # Left side: 3 stacked images (150x150 * 3 = 150x450)
        # Right side: Map (450x450)
        # Total: 600x450
        
        combo = Image.new('RGB', (PILOT_RES + MAP_RES, MAP_RES))
        
        # Stack pilots
        y_off = 0
        for p_img in pilot_imgs:
            combo.paste(p_img, (0, y_off))
            y_off += PILOT_RES
            
        combo.paste(pil_map, (PILOT_RES, 0))
        
        frames_buffer.append(combo)
        
        if f % 10 == 0:
            print(f"Frame {f} | Structural Integrity Check...")

    print(f"Saving Trinity Map to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ SYSTEM SHUTDOWN.")

if __name__ == "__main__":
    run_trinity()