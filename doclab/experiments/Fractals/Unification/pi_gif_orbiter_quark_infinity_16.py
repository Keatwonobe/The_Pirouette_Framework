import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw

# =========================================================
#  HELICAL TOMOGRAPHY: SIDE-SCROLLING ANALYSIS
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_helical_tomography.gif"
FRAMES = 160
GLOBAL_SCALE = 28.0     # Wide angle
MAP_RES = 400           # Resolution of Top-Down Map
SIDE_RES = 400          # Width of Side View

# PHYSICS
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

# INITIAL GUESSES
HINTS = [
    (-10.0, 5.0), # Cyan
    (10.0, 5.0),  # Magenta
    (0.0, -10.0)  # Yellow
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

# --- TRACKER LOGIC ---

class QuarkTracker:
    def __init__(self, hint, quark_id):
        self.id = quark_id
        self.cam_m, self.cam_l = hint
        self.width = 8.0 
        self.min_width = 0.05
        
        # Dynamics
        self.last_theta = np.arctan2(self.cam_l, self.cam_m)
        self.omega = 0.0
        self.alpha = 0.0
        
        self.history = [] # List of (m, l)
        self.locked = False
        
    def update(self, sys_src_m, sys_src_l, pulse):
        # 1. Sensor
        sensor_img = render_microscope(self.cam_m, self.cam_l, self.width, 100, sys_src_m, sys_src_l, pulse)
        
        # 2. Peak Find
        peak_val, peak_m, peak_l = find_peak(sensor_img, self.width, self.cam_m, self.cam_l, 0.45)
        self.locked = peak_val > 0.001
        
        if self.locked:
            dist = np.sqrt((peak_m - self.cam_m)**2 + (peak_l - self.cam_l)**2)
            vel = dist / self.width
            self.cam_m, self.cam_l = peak_m, peak_l
            
            curr_theta = np.arctan2(self.cam_l, self.cam_m)
            diff = curr_theta - self.last_theta
            if diff > np.pi: diff -= 2*np.pi
            if diff < -np.pi: diff += 2*np.pi
            
            new_alpha = diff - self.omega
            self.alpha = 0.5*self.alpha + 0.5*new_alpha
            self.omega = diff
            self.last_theta = curr_theta
            
            # Zoom Logic
            if vel > 0.10: self.width *= 1.05
            elif self.width > self.min_width: self.width *= 0.95
        else:
            # Inertial
            pred_theta = self.last_theta + self.omega + self.alpha
            r = np.sqrt(self.cam_m**2 + self.cam_l**2)
            self.cam_m = r * np.cos(pred_theta)
            self.cam_l = r * np.sin(pred_theta)
            self.last_theta = pred_theta
            self.alpha *= 0.9
            
        self.history.append((self.cam_m, self.cam_l))

# --- RENDERER ---

def run_tomography():
    print("--- 🧬 INITIATING HELICAL TOMOGRAPHY ---")
    
    trackers = [QuarkTracker(h, i) for i, h in enumerate(HINTS)]
    frames_buffer = []
    
    # Pre-lock
    curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, 0)
    for t in trackers:
        scan = render_microscope(t.cam_m, t.cam_l, 8.0, 100, curr_src_m, curr_src_l, 1.0)
        _, t.cam_m, t.cam_l = find_peak(scan, 8.0, t.cam_m, t.cam_l, 0.5)
    
    # HISTORY BUFFER FOR SIDE VIEW
    # We store the last N frames of coordinates for everyone
    # Format: list of [ (m1, l1), (m2, l2), (m3, l3) ]
    global_history = [] 
    
    for f in range(FRAMES):
        sys_theta = 2 * np.pi * (f / 100)
        src_m, src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.2)
        
        # 1. Update Physics
        frame_coords = []
        for t in trackers:
            t.update(src_m, src_l, pulse)
            frame_coords.append((t.cam_m, t.cam_l))
            
        global_history.append(frame_coords)
        if len(global_history) > MAP_RES - 20: # Keep buffer manageable
            global_history.pop(0)

        # 2. Render Left Pane (Top-Down Radar)
        raw_map = render_microscope(0.0, 0.0, GLOBAL_SCALE, MAP_RES, src_m, src_l, pulse)
        norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
        norm_map = np.power(norm_map, 0.4)
        img_map = (plt.get_cmap('magma')(norm_map)[:, :, :3] * 255).astype(np.uint8)
        img_map = np.flipud(img_map)
        pil_map = Image.fromarray(img_map)
        d_map = ImageDraw.Draw(pil_map)
        
        # Draw Radar Trails
        current_points_px = []
        for t in trackers:
            points = []
            for (tm, tl) in t.history[-50:]: # Short trail on radar
                px = (tm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_RES - 1)
                py = MAP_RES - 1 - ((tl - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_RES - 1))
                points.append((px, py))
            if len(points) > 1:
                d_map.line(points, fill=COLORS[t.id], width=1)
            cx, cy = points[-1]
            current_points_px.append((cx, cy))
            d_map.ellipse([cx-2, cy-2, cx+2, cy+2], fill=(255,255,255))

        # Radar Linkages
        if len(current_points_px) == 3:
            d_map.polygon(current_points_px, outline=(255, 255, 255, 128), width=1)

        d_map.text((10, 10), "TOP-DOWN [ORBIT]", fill=(200, 200, 200))

        # 3. Render Right Pane (Side-View Tomogram)
        pil_side = Image.new('RGB', (SIDE_RES, MAP_RES), color=(10, 0, 20)) # Dark purple bg
        d_side = ImageDraw.Draw(pil_side)
        d_side.text((10, 10), "SIDE ELEVATION [HELIX]", fill=(200, 200, 200))
        
        # We draw from oldest (top) to newest (bottom)
        # Y-axis maps to array index
        
        start_y = 40
        y_step = (MAP_RES - 50) / len(global_history)
        
        # Pre-calculate points for line drawing
        # structure: quark_id -> list of (x, y)
        quark_lines = {0:[], 1:[], 2:[]}
        
        for i, coords_set in enumerate(global_history):
            draw_y = start_y + i * y_step
            
            # Draw Horizontal Linkage (The "Rungs")
            # We need the X coordinates of the 3 quarks at this time step
            # X coord = M
            curr_row_px = []
            
            for q_id, (qm, ql) in enumerate(coords_set):
                # Map M to X (Side View Width)
                px_x = (qm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (SIDE_RES - 1)
                
                # DEPTH CUEING
                # Map L to Size/Brightness
                # L ranges roughly -10 to 10
                # Normalized -1 to 1
                norm_depth = ql / (GLOBAL_SCALE/2)
                
                radius = 3 + (norm_depth * 1.5) # Size varies 1.5 to 4.5
                if radius < 1: radius = 1
                
                # Brightness
                alpha = int(150 + (norm_depth * 100)) # 50 to 250
                if alpha < 50: alpha = 50
                if alpha > 255: alpha = 255
                
                c = COLORS[q_id]
                # Adjust color brightness manually roughly
                col = (int(c[0]*alpha/255), int(c[1]*alpha/255), int(c[2]*alpha/255))
                
                d_side.ellipse([px_x-radius, draw_y-radius, px_x+radius, draw_y+radius], fill=col)
                
                curr_row_px.append((px_x, draw_y))
                quark_lines[q_id].append((px_x, draw_y))
            
            # Draw the Rungs (White lines connecting quarks at this specific time)
            if len(curr_row_px) == 3:
                # Draw Triangle (flattened) or just lines? 
                # A line strip is better for "Ladder" look
                # Sort by X to make it a clean strip? No, preserve ID topology.
                # Just connect 0-1, 1-2, 2-0
                p0, p1, p2 = curr_row_px[0], curr_row_px[1], curr_row_px[2]
                d_side.line([p0, p1], fill=(100, 100, 100), width=1)
                d_side.line([p1, p2], fill=(100, 100, 100), width=1)
                d_side.line([p2, p0], fill=(100, 100, 100), width=1)

        # Draw Vertical Helix Lines
        for q_id in range(3):
            if len(quark_lines[q_id]) > 1:
                d_side.line(quark_lines[q_id], fill=COLORS[q_id], width=2)
                
        # 4. Combine
        combo = Image.new('RGB', (MAP_RES + SIDE_RES, MAP_RES))
        combo.paste(pil_map, (0, 0))
        combo.paste(pil_side, (MAP_RES, 0))
        
        frames_buffer.append(combo)
        
        if f % 10 == 0:
            print(f"Frame {f} | Tomography Scan...")

    print(f"Saving Tomogram to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ SCAN COMPLETE.")

if __name__ == "__main__":
    run_tomography()