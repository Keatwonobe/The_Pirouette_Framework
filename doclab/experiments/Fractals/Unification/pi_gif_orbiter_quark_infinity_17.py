import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw

# =========================================================
#  GRAND UNIFIED HELIX: TRINITY + ORBIT + DNA
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_grand_helix.gif"
FRAMES = 160
GLOBAL_SCALE = 28.0     

# LAYOUT DIMENSIONS
PILOT_H = 150           # Height of one pilot pane
PILOT_W = 150           # Width of one pilot pane
MAP_DIM = 450           # Center Map (Square)
SIDE_W = 300            # Right Side Width
TOTAL_H = 450           # Total Height (3 * 150)

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
        self.last_theta = np.arctan2(self.cam_l, self.cam_m)
        self.omega = 0.0
        self.alpha = 0.0
        self.history = []
        self.locked = False
        
    def update(self, sys_src_m, sys_src_l, pulse):
        # Sensor Scan
        sensor_img = render_microscope(self.cam_m, self.cam_l, self.width, 100, sys_src_m, sys_src_l, pulse)
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
            
            if vel > 0.10: self.width *= 1.05
            elif self.width > self.min_width: self.width *= 0.95
        else:
            pred_theta = self.last_theta + self.omega + self.alpha
            r = np.sqrt(self.cam_m**2 + self.cam_l**2)
            self.cam_m = r * np.cos(pred_theta)
            self.cam_l = r * np.sin(pred_theta)
            self.last_theta = pred_theta
            self.alpha *= 0.9
            
        self.history.append((self.cam_m, self.cam_l))

    def render_pilot(self, sys_src_m, sys_src_l, pulse):
        # The "Candlelight" Renderer
        raw = render_microscope(self.cam_m, self.cam_l, self.width, PILOT_W, sys_src_m, sys_src_l, pulse)
        
        # Soft Gamma for Ethereal Glow
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.35) # Lower gamma = brighter lows (more glow)
        
        # Colorize
        base_c = np.array(COLORS[self.id]) / 255.0
        img_rgb = np.dstack((norm * base_c[0], norm * base_c[1], norm * base_c[2]))
        
        # Add "Hot Core" (White center)
        core_mask = norm > 0.8
        img_rgb[core_mask] = img_rgb[core_mask] * 0.5 + 0.5 # Blend towards white
        
        img_uint8 = (img_rgb * 255).astype(np.uint8)
        img_uint8 = np.flipud(img_uint8)
        pil = Image.fromarray(img_uint8)
        d = ImageDraw.Draw(pil)
        d.text((5, 5), f"Q{self.id+1} LOCK", fill=COLORS[self.id])
        return pil

# --- MAIN RENDERER ---

def run_grand_helix():
    print("--- 🔬 ASSEMBLING GRAND UNIFIED VIEW ---")
    
    trackers = [QuarkTracker(h, i) for i, h in enumerate(HINTS)]
    frames_buffer = []
    global_history = [] 
    
    # Pre-flight
    curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, 0)
    for t in trackers:
        scan = render_microscope(t.cam_m, t.cam_l, 8.0, 100, curr_src_m, curr_src_l, 1.0)
        _, t.cam_m, t.cam_l = find_peak(scan, 8.0, t.cam_m, t.cam_l, 0.5)
        
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
        if len(global_history) > TOTAL_H - 50: 
            global_history.pop(0)

        # 2. Render Panel 1: Pilot Stack
        pilots = [t.render_pilot(src_m, src_l, pulse) for t in trackers]
        
        # 3. Render Panel 2: Orbital Map
        raw_map = render_microscope(0.0, 0.0, GLOBAL_SCALE, MAP_DIM, src_m, src_l, pulse)
        norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
        norm_map = np.power(norm_map, 0.4)
        img_map = (plt.get_cmap('magma')(norm_map)[:, :, :3] * 255).astype(np.uint8)
        img_map = np.flipud(img_map)
        pil_map = Image.fromarray(img_map)
        d_map = ImageDraw.Draw(pil_map)
        d_map.text((10, 10), "ORBITAL MANIFOLD", fill=(200, 200, 200))
        
        # Map Trails & Triangle
        curr_px = []
        for t in trackers:
            pts = []
            for (tm, tl) in t.history[-60:]: # Longer trail for "Circle" feel
                px = (tm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1)
                py = MAP_DIM - 1 - ((tl - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1))
                pts.append((px, py))
            if len(pts) > 1:
                d_map.line(pts, fill=COLORS[t.id], width=2)
            curr_px.append(pts[-1])
            cx, cy = pts[-1]
            d_map.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(255,255,255))
            
        if len(curr_px) == 3:
            d_map.polygon(curr_px, outline=(255, 255, 255, 180), width=1)

        # 4. Render Panel 3: DNA Helix (Side View)
        pil_side = Image.new('RGB', (SIDE_W, TOTAL_H), color=(10, 5, 20))
        d_side = ImageDraw.Draw(pil_side)
        d_side.text((10, 10), "TEMPORAL HELIX", fill=(200, 200, 200))
        
        start_y = 30
        y_step = (TOTAL_H - 40) / len(global_history)
        
        q_lines = {0:[], 1:[], 2:[]}
        
        for i, coords_set in enumerate(global_history):
            draw_y = start_y + i * y_step
            row_px = []
            
            for q_id, (qm, ql) in enumerate(coords_set):
                # Map M to X
                px_x = (qm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (SIDE_W - 1)
                
                # Depth Cueing (L)
                norm_d = ql / (GLOBAL_SCALE/2)
                rad = 3 + (norm_d * 2.0)
                if rad < 1: rad = 1
                
                alpha = int(120 + (norm_d * 135))
                if alpha < 40: alpha = 40
                if alpha > 255: alpha = 255
                
                c = COLORS[q_id]
                col = (int(c[0]*alpha/255), int(c[1]*alpha/255), int(c[2]*alpha/255))
                
                d_side.ellipse([px_x-rad, draw_y-rad, px_x+rad, draw_y+rad], fill=col)
                row_px.append((px_x, draw_y))
                q_lines[q_id].append((px_x, draw_y))
                
            # Rungs
            if len(row_px) == 3:
                p0, p1, p2 = row_px[0], row_px[1], row_px[2]
                rung_c = (80, 80, 80)
                d_side.line([p0, p1], fill=rung_c, width=1)
                d_side.line([p1, p2], fill=rung_c, width=1)
                d_side.line([p2, p0], fill=rung_c, width=1)

        for q_id in range(3):
            if len(q_lines[q_id]) > 1:
                d_side.line(q_lines[q_id], fill=COLORS[q_id], width=2)

        # 5. Composite
        final = Image.new('RGB', (PILOT_W + MAP_DIM + SIDE_W, TOTAL_H))
        
        # Paste Pilots
        y_off = 0
        for p in pilots:
            final.paste(p, (0, y_off))
            y_off += PILOT_H
            
        # Paste Map
        final.paste(pil_map, (PILOT_W, 0))
        
        # Paste Helix
        final.paste(pil_side, (PILOT_W + MAP_DIM, 0))
        
        frames_buffer.append(final)
        
        if f % 10 == 0:
            print(f"Frame {f} | Rendering Multi-View Manifold...")

    print(f"Saving Grand Unified Helix to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ MASTERPIECE RENDERED.")

if __name__ == "__main__":
    run_grand_helix()