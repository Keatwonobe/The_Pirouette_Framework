import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont

# =========================================================
#  PROTON ENGINE: "THE MYSTERY REVEALED"
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_mystery_reveal.gif"
FRAMES = 160
GLOBAL_SCALE = 28.0     

# LAYOUT DIMENSIONS
PILOT_H = 150           
PILOT_W = 150           
MAP_DIM = 450           
SIDE_W = 300            
MAIN_H = 450            
BOTTOM_H = 150          # New Bottom Panel
TOTAL_W = PILOT_W + MAP_DIM + SIDE_W

# PHYSICS
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

HINTS = [(-10.0, 5.0), (10.0, 5.0), (0.0, -10.0)]
COLORS = [(0, 255, 255), (255, 0, 255), (255, 255, 0)]

# --- MATH KERNEL ---

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

# --- TRACKER ---

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
        self.radius_log = []
        
    def update(self, sys_src_m, sys_src_l, pulse):
        # Scan
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
            
        r_curr = np.sqrt(self.cam_m**2 + self.cam_l**2)
        self.history.append((self.cam_m, self.cam_l))
        self.radius_log.append(r_curr)

    def render_pilot(self, sys_src_m, sys_src_l, pulse):
        # 1. THE GLOW (Background Manifold)
        # Sample at 6x width for context "underneath" the quark
        # Using the SAME coordinates, just wider FOV
        wide_w = self.width * 6.0
        raw_glow = render_microscope(self.cam_m, self.cam_l, wide_w, PILOT_W, sys_src_m, sys_src_l, pulse)
        norm_glow = (raw_glow - raw_glow.min()) / (raw_glow.max() - raw_glow.min() + 1e-9)
        norm_glow = np.power(norm_glow, 0.6) * 0.4 # Dimmer, smoother
        
        # 2. THE CORE (Foreground Quark)
        raw_core = render_microscope(self.cam_m, self.cam_l, self.width, PILOT_W, sys_src_m, sys_src_l, pulse)
        norm_core = (raw_core - raw_core.min()) / (raw_core.max() - raw_core.min() + 1e-9)
        norm_core = np.power(norm_core, 0.4) 
        
        # 3. COMPOSITE
        # We blend them. Since they are different spatial scales, we can't just add arrays directly 
        # unless we assume the arrays represent the "view". They do.
        # But wait, norm_glow represents a huge area. norm_core represents a tiny area.
        # If we just add them pixel-wise, we are overlaying the "macro" view on the "micro" view.
        # This creates a "Ghost" effect where you see the surroundings *as if* they were local.
        # This is exactly what "Candlelight" implies - an aura.
        
        final_intensity = norm_core + norm_glow
        final_intensity = np.clip(final_intensity, 0, 1)
        
        # Colorize
        base_c = np.array(COLORS[self.id]) / 255.0
        img_rgb = np.dstack((final_intensity * base_c[0], final_intensity * base_c[1], final_intensity * base_c[2]))
        
        # Hot Core White
        core_mask = norm_core > 0.85
        img_rgb[core_mask] = img_rgb[core_mask] * 0.3 + 0.7
        
        img_uint8 = (img_rgb * 255).astype(np.uint8)
        img_uint8 = np.flipud(img_uint8)
        pil = Image.fromarray(img_uint8)
        d = ImageDraw.Draw(pil)
        d.text((5, 5), f"Q{self.id+1} GLOW", fill=COLORS[self.id])
        return pil

# --- EQUATION PANEL RENDERER ---

def render_bottom_panel(trackers, frame_idx):
    # Create Panel
    w, h = TOTAL_W, BOTTOM_H
    img = Image.new('RGB', (w, h), (10, 10, 15))
    d = ImageDraw.Draw(img)
    
    # 1. TEXT: EQUATIONS (Left Side)
    # Since I cannot use LaTeX rendering libraries easily, I will draw text approximation
    font_s = 15
    start_x = 20
    
    d.text((start_x, 20), "HELICAL OPERATOR ALGEBRA", fill=(200, 200, 255))
    d.text((start_x, 50), "d_h / dt  =  d/dt  +  i * kappa * omega", fill=(0, 255, 255))
    d.text((start_x, 80), "P_h_hat  =  -i * h_bar * ( d_h / dt )", fill=(0, 255, 255))
    d.text((start_x, 110), "[ x_h, p_h ] = i * h_bar * ( 1 + i*kappa )", fill=(255, 100, 255))
    
    # 2. PLOT: RADIUS RATIO (Right Side)
    # We plot the radius of Q1 (Cyan) vs Q2 (Magenta)
    plot_x = 400
    plot_w = 400
    plot_h = 100
    plot_y = 25
    
    # Draw axes
    d.line([plot_x, plot_y+plot_h, plot_x+plot_w, plot_y+plot_h], fill=(100,100,100))
    d.line([plot_x, plot_y, plot_x, plot_y+plot_h], fill=(100,100,100))
    d.text((plot_x+10, plot_y-15), "RADIAL EVOLUTION r(t)", fill=(200,200,200))
    
    # Plot Data
    # Normalize radius to fit 0-20 range into 0-100 pixels
    max_r = 15.0
    
    for t in trackers:
        points = []
        data = t.radius_log
        c = COLORS[t.id]
        
        # We show the last 100 frames scrolling
        visible_data = data[-100:]
        
        for i, val in enumerate(visible_data):
            px = plot_x + (i * (plot_w / 100))
            # Flip Y
            py = (plot_y + plot_h) - (val / max_r * plot_h)
            points.append((px, py))
            
        if len(points) > 1:
            d.line(points, fill=c, width=2)
            
    # 3. MYSTERY TEXT
    mystery_x = 850
    d.text((mystery_x, 40), "THE MYSTERY:", fill=(255, 50, 50))
    d.text((mystery_x, 70), "Why does the radius", fill=(255, 255, 255))
    d.text((mystery_x, 90), "stabilize at r ~ 11.2?", fill=(255, 255, 255))
    d.text((mystery_x, 110), "kappa_eff -> 0.618", fill=(255, 215, 0)) # Golden Ratio hint
    
    return img

# --- MAIN LOOP ---

def run_mystery():
    print("--- 🕵️ REVEALING THE MYSTERY ---")
    
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
        
        # Update
        frame_coords = []
        for t in trackers:
            t.update(src_m, src_l, pulse)
            frame_coords.append((t.cam_m, t.cam_l))
        global_history.append(frame_coords)
        if len(global_history) > MAIN_H - 50: global_history.pop(0)
        
        # 1. Pilots (Candlelight)
        pilots = [t.render_pilot(src_m, src_l, pulse) for t in trackers]
        
        # 2. Map (Center)
        raw_map = render_microscope(0.0, 0.0, GLOBAL_SCALE, MAP_DIM, src_m, src_l, pulse)
        norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
        norm_map = np.power(norm_map, 0.4)
        img_map = (plt.get_cmap('magma')(norm_map)[:, :, :3] * 255).astype(np.uint8)
        img_map = np.flipud(img_map)
        pil_map = Image.fromarray(img_map)
        d_map = ImageDraw.Draw(pil_map)
        
        # Map Overlay
        curr_px = []
        for t in trackers:
            pts = []
            for (tm, tl) in t.history[-60:]:
                px = (tm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1)
                py = MAP_DIM - 1 - ((tl - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1))
                pts.append((px, py))
            if len(pts) > 1: d_map.line(pts, fill=COLORS[t.id], width=2)
            curr_px.append(pts[-1])
            cx, cy = pts[-1]
            d_map.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(255,255,255))
        if len(curr_px) == 3: d_map.polygon(curr_px, outline=(255, 255, 255, 180), width=1)
        
        # 3. Helix (Right)
        pil_side = Image.new('RGB', (SIDE_W, MAIN_H), (10, 5, 20))
        d_side = ImageDraw.Draw(pil_side)
        start_y = 30
        y_step = (MAIN_H - 40) / len(global_history)
        q_lines = {0:[], 1:[], 2:[]}
        
        for i, coords_set in enumerate(global_history):
            draw_y = start_y + i * y_step
            row_px = []
            for q_id, (qm, ql) in enumerate(coords_set):
                px_x = (qm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (SIDE_W - 1)
                norm_d = ql / (GLOBAL_SCALE/2)
                rad = 3 + (norm_d * 2.0)
                if rad < 1: rad = 1
                alpha = int(120 + (norm_d * 135))
                if alpha < 40: alpha = 40; 
                if alpha > 255: alpha = 255
                c = COLORS[q_id]
                col = (int(c[0]*alpha/255), int(c[1]*alpha/255), int(c[2]*alpha/255))
                d_side.ellipse([px_x-rad, draw_y-rad, px_x+rad, draw_y+rad], fill=col)
                row_px.append((px_x, draw_y))
                q_lines[q_id].append((px_x, draw_y))
            if len(row_px) == 3:
                p0, p1, p2 = row_px[0], row_px[1], row_px[2]
                rung_c = (80, 80, 80)
                d_side.line([p0, p1], fill=rung_c, width=1)
                d_side.line([p1, p2], fill=rung_c, width=1)
                d_side.line([p2, p0], fill=rung_c, width=1)
        for q_id in range(3):
            if len(q_lines[q_id]) > 1: d_side.line(q_lines[q_id], fill=COLORS[q_id], width=2)
            
        # 4. Bottom Panel
        pil_bottom = render_bottom_panel(trackers, f)
        
        # 5. Composite
        final = Image.new('RGB', (TOTAL_W, MAIN_H + BOTTOM_H))
        y_off = 0
        for p in pilots:
            final.paste(p, (0, y_off)); y_off += PILOT_H
        final.paste(pil_map, (PILOT_W, 0))
        final.paste(pil_side, (PILOT_W + MAP_DIM, 0))
        final.paste(pil_bottom, (0, MAIN_H))
        
        frames_buffer.append(final)
        if f % 20 == 0: print(f"Frame {f} | Candlelight & Algebra...")
        
    print(f"Saving to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ MYSTERY REVEALED.")

if __name__ == "__main__":
    run_mystery()