import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw

# =========================================================
# PROTON ENGINE: "FUSION CORE" PROTOCOL (Hybrid 21+18)
# --- ENHANCEMENT: ROBUST TRACKING + ADJUSTABLE ZOOM ---
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_fusion_core_orbital_nib.gif"
FRAMES = 160            
GLOBAL_SCALE = 28.0     

# LAYOUT DIMENSIONS
PILOT_SIZE = 150        
PILOT_COLS = 2          
PILOT_PANEL_W = PILOT_SIZE * PILOT_COLS
MAP_DIM = 450           
SIDE_W = 300            
MAIN_H = 450            
BOTTOM_H = 150          
TOTAL_W = PILOT_PANEL_W + MAP_DIM + SIDE_W

# PHYSICS (6 Sources: 3 Strong, 3 Ghost)
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_WEAK_M = np.array([0.0, 5.0, -5.0]) 
SRC_WEAK_L = np.array([-5.0, 2.5, 2.5]) 

# TARGET HINTS (G-1 is at index 3: (5.0, 5.0) as determined by your test)
HINTS = [(-10.0, 5.0), (10.0, 5.0), (0.0, -10.0), # Strong Hints
         (5.0, 5.0), (5.0, -2.5), (-5.0, -2.5)]   # Ghost Hints

# COLORS 
COLORS_STRONG = [(0, 255, 255), (255, 0, 255), (255, 255, 0)] 
COLORS_GHOST = [(255, 50, 50), (50, 255, 50), (50, 100, 255)]
COLORS = COLORS_STRONG + COLORS_GHOST

# --- MATH KERNEL (NUMBA-accelerated) ---

@njit(parallel=True)
def render_microscope(center_m, center_l, width, res, src_m_s, src_l_s, src_m_w, src_l_w, global_theta, amp_boost):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    intensity_map = np.zeros((res, res), dtype=np.float64)
    
    c, s = np.cos(global_theta), np.sin(global_theta)
    
    # STRONG Sources
    for i in range(3):
        sm = src_m_s[i]*c - src_l_s[i]*s
        sl = src_m_s[i]*s + src_l_s[i]*c
        
        for row in prange(res):
            y = l_vals[row]
            for col in range(res):
                x = m_vals[col]
                
                dx = x - sm
                dy = y - sl
                r = np.sqrt(dx*dx + dy*dy)
                if r < 1e-12: r = 1e-12
                
                k = (2 * np.pi) / (10.0) 
                phase = k * r
                amp = (amp_boost / r)
                
                intensity_map[row, col] += amp * np.cos(phase)
                
    # WEAK Sources
    for i in range(3):
        sm = src_m_w[i]*c - src_l_w[i]*s
        sl = src_m_w[i]*s + src_l_w[i]*c
        
        for row in prange(res):
            y = l_vals[row]
            for col in range(res):
                x = m_vals[col]
                
                dx = x - sm
                dy = y - sl
                r = np.sqrt(dx*dx + dy*dy)
                if r < 1e-12: r = 1e-12
                
                k = (2 * np.pi) / (5.0) 
                amp = (0.4 * amp_boost / r)
                phase = k * r
                
                intensity_map[row, col] += amp * np.cos(phase)

    return intensity_map**2

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

def find_red_nib_peak(img, width, center_m, center_l):
    # Use a tight search ratio for the Red Nib (G-1)
    return find_peak(img, width, center_m, center_l, search_ratio=0.20) 

# --- TRACKER ---

class FusionTracker:
    def __init__(self, hint, particle_id):
        self.id = particle_id
        self.type = 'STRONG' if particle_id < 3 else 'GHOST'
        self.color = COLORS[particle_id]
        self.cam_m, self.cam_l = hint
        
        # Adjustable Parameters
        self.width = 8.0 if self.type == 'STRONG' else 6.0
        self.min_width = 0.05
        
        # New: Damping and Zoom Rates
        if self.id == 3: # G-1 (Red Nib)
            self.damp_factor = 0.15  # Light damping for precision
            self.zoom_rate = 0.5     # Half the zoom speed for stability
            self.search_ratio = 0.20 # Tight search
        else:
            self.damp_factor = 0.7 if self.type == 'STRONG' else 0.5 
            self.zoom_rate = 1.0     # Normal zoom speed
            self.search_ratio = 0.45 # Wide search
            
        # Dynamics
        self.last_theta = np.arctan2(self.cam_l, self.cam_m)
        self.omega = 0.0 
        self.alpha = 0.0 
        self.history = []
        self.intensity_log = [] 
        self.radius_log = []
        self.locked = False
        
    def update(self, pulse):
        
        # 1. Scan and Lock
        scan = render_microscope(self.cam_m, self.cam_l, self.width, 100, 
                                 SRC_STRONG_M, SRC_STRONG_L, SRC_WEAK_M, SRC_WEAK_L, 
                                 pulse['theta'], pulse['amp_boost'])
        
        # Use Red Nib function for ID 3, standard for others (using self.search_ratio)
        if self.id == 3:
            peak_val, peak_m, peak_l = find_red_nib_peak(scan, self.width, self.cam_m, self.cam_l)
        else:
            peak_val, peak_m, peak_l = find_peak(scan, self.width, self.cam_m, self.cam_l, self.search_ratio)
            
        self.locked = peak_val > 0.001
        
        
        # --- ROBUST TRACKING LOGIC (Unified Damping/Prediction) ---
        
        if self.locked:
            dist = np.sqrt((peak_m - self.cam_m)**2 + (peak_l - self.cam_l)**2)
            vel = dist / self.width
            
            # 1. Positional Update (using self.damp_factor)
            self.cam_m += (peak_m - self.cam_m) * self.damp_factor
            self.cam_l += (peak_l - self.cam_l) * self.damp_factor
        
            # 2. Update Angular Dynamics 
            curr_theta = np.arctan2(self.cam_l, self.cam_m)
            diff = curr_theta - self.last_theta
            if diff > np.pi: diff -= 2*np.pi
            if diff < -np.pi: diff += 2*np.pi
            new_alpha = diff - self.omega
            self.alpha = 0.5*self.alpha + 0.5*new_alpha
            self.omega = diff
            self.last_theta = curr_theta
        
            # 3. Dynamic Zoom (using self.zoom_rate)
            if vel > 0.10: self.width *= (1.0 + 0.05 * self.zoom_rate)
            elif self.width > self.min_width: self.width /= (1.0 + 0.05 * self.zoom_rate)
        
        else:
            # --- PREDICTION LOGIC (Inertial) ---
            pred_theta = self.last_theta + self.omega + self.alpha
            r = np.sqrt(self.cam_m**2 + self.cam_l**2)
            self.cam_m = r * np.cos(pred_theta)
            self.cam_l = r * np.sin(pred_theta)
            self.last_theta = pred_theta
            self.alpha *= 0.9 # Dampen acceleration

        r_curr = np.sqrt(self.cam_m**2 + self.cam_l**2)
        self.history.append((self.cam_m, self.cam_l))
        self.intensity_log.append(peak_val)
        self.radius_log.append(r_curr)

    def render_pilot(self, pulse):
        # 1. The GLOW (Candlelight background)
        wide_w = self.width * 6.0
        raw_glow = render_microscope(self.cam_m, self.cam_l, wide_w, PILOT_SIZE, 
                                      SRC_STRONG_M, SRC_STRONG_L, SRC_WEAK_M, SRC_WEAK_L, 
                                      pulse['theta'], pulse['amp_boost'])
        norm_glow = (raw_glow - raw_glow.min()) / (raw_glow.max() - raw_glow.min() + 1e-9)
        norm_glow = np.power(norm_glow, 0.6) * 0.4 
        
        # 2. The CORE (Foreground Quark)
        raw_core = render_microscope(self.cam_m, self.cam_l, self.width, PILOT_SIZE, 
                                     SRC_STRONG_M, SRC_STRONG_L, SRC_WEAK_M, SRC_WEAK_L, 
                                     pulse['theta'], pulse['amp_boost'])
        norm_core = (raw_core - raw_core.min()) / (raw_core.max() - raw_core.min() + 1e-9)
        norm_core = np.power(norm_core, 0.4) 
        
        # 3. COMPOSITE
        final_intensity = norm_core + norm_glow
        final_intensity = np.clip(final_intensity, 0, 1)
        
        # Colorize and Hotspot
        base_c = np.array(self.color) / 255.0
        img_rgb = np.dstack((final_intensity * base_c[0], final_intensity * base_c[1], final_intensity * base_c[2]))
        
        core_mask = norm_core > 0.90
        img_rgb[core_mask] = img_rgb[core_mask] * 0.2 + 0.8
        
        img_uint8 = (img_rgb * 255).astype(np.uint8)
        img_uint8 = np.flipud(img_uint8)
        pil = Image.fromarray(img_uint8)
        d = ImageDraw.Draw(pil)
        label = f"M-{self.id+1}" if self.type == 'STRONG' else f"G-{self.id-2}"
        d.text((5, 5), label, fill=COLORS[self.id])
        
        # --- Add "NIB/ORBITAL LOCK" indicator for G-1 ---
        if self.id == 3:
            d.text((5, 25), "ORBITAL NIB", fill=(255, 255, 255))
        
        return pil

# --- SPECTROGRAPH (No changes) ---

def render_spectrograph(trackers, width, height):
    img = Image.new('RGB', (width, height), (5, 5, 10))
    d = ImageDraw.Draw(img)
    
    d.text((20, 10), "RESONANCE SPECTROGRAPH [GHOST INTENSITY]", fill=(200, 200, 200))
    
    plot_h = height - 40
    plot_w = width - 40
    ox, oy = 20, 30
    hist_len = 100
    
    ghosts = [t for t in trackers if t.type == 'GHOST']
    
    all_data = []
    for g in ghosts:
        all_data.extend(g.intensity_log[-hist_len:])
        
    if not all_data: return img
        
    d_min, d_max = min(all_data), max(all_data)
    if d_max == d_min: d_max += 1e-9
    
    for g in ghosts:
        data = g.intensity_log[-hist_len:]
        if not data: continue
        
        pts = []
        step_x = plot_w / hist_len
        
        for i, val in enumerate(data):
            x = ox + i * step_x
            norm_y = (val - d_min) / (d_max - d_min)
            y = (oy + plot_h) - (norm_y * plot_h)
            pts.append((x, y))
            
        if len(pts) > 1:
            d.line(pts, fill=g.color, width=2)
            
    d.line([ox, oy+plot_h/2, ox+plot_w, oy+plot_h/2], fill=(50, 50, 50))
    return img

# --- HELIX LATTICE RENDERER (No changes) ---

def render_helix_lattice(trackers, width, height):
    pil_side = Image.new('RGB', (width, height), (10, 5, 20))
    d_side = ImageDraw.Draw(pil_side)
    d_side.text((10, 10), "ORBITAL LATTICE [ALL 6]", fill=(150, 150, 150))
    
    max_len = height - 50 
    history_data = [t.history for t in trackers]
    
    hist_len = min(len(h) for h in history_data)
    history_data_T = []
    for f in range(hist_len):
        frame_coords = []
        for t_id in range(6):
            frame_coords.append(history_data[t_id][f])
        history_data_T.append(frame_coords)
        
    global_history = history_data_T[-max_len:]
    
    start_y = 30
    y_step = (height - 40) / len(global_history) if len(global_history) > 1 else 10

    q_lines = {i:[] for i in range(6)}
    
    for i, coords_set in enumerate(global_history):
        draw_y = start_y + i * y_step
        row_px = []
        
        for q_id, (qm, ql) in enumerate(coords_set):
            px_x = (qm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (width - 1)
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
            
        if len(row_px) == 6:
            # Strong Triangle (M1, M2, M3)
            d_side.line([row_px[0], row_px[1]], fill=(120, 120, 120), width=1)
            d_side.line([row_px[1], row_px[2]], fill=(120, 120, 120), width=1)
            d_side.line([row_px[2], row_px[0]], fill=(120, 120, 120), width=1)
            
            # Ghost Triangle (G1, G2, G3)
            d_side.line([row_px[3], row_px[4]], fill=(60, 60, 60), width=1)
            d_side.line([row_px[4], row_px[5]], fill=(60, 60, 60), width=1)
            d_side.line([row_px[5], row_px[3]], fill=(60, 60, 60), width=1)
            
            # Cross-group links (M1-G1, M2-G2, M3-G3)
            d_side.line([row_px[0], row_px[3]], fill=(30, 30, 30), width=1)
            d_side.line([row_px[1], row_px[4]], fill=(30, 30, 30), width=1)
            d_side.line([row_px[2], row_px[5]], fill=(30, 30, 30), width=1)
            
    for q_id in range(6):
        if len(q_lines[q_id]) > 1: d_side.line(q_lines[q_id], fill=COLORS[q_id], width=2)
            
    return pil_side


# --- MODIFIED PRE-RUN STABILIZATION ---

def pre_run_stabilization(trackers, frames):
    print(f"--- ⏳ PRE-RUNNING {frames} FRAMES FOR HISTORY STABILIZATION ---")
    
    # 1. Run the simulation forward without saving frames
    for f in range(frames):
        pulse = {
            'theta': 2 * np.pi * (f / 100),
            'amp_boost': 1.0 + 0.1 * np.sin(f * 0.2)
        }
        for t in trackers: t.update(pulse)

    # 2. TRUNCATE and SYNCHRONIZE
    # We keep a small, stable history for the plot tails (e.g., 5 points)
    # and set the current state to the *end* of that kept history.
    SYNC_HISTORY_LENGTH = 5 
    print(f"--- 🔄 SYNCHRONIZING STATE TO LAST {SYNC_HISTORY_LENGTH} HISTORY POINTS ---")
    
    for i, t in enumerate(trackers):
        
        # Truncate history lists
        t.history = t.history[-SYNC_HISTORY_LENGTH:]
        t.intensity_log = t.intensity_log[-SYNC_HISTORY_LENGTH:]
        t.radius_log = t.radius_log[-SYNC_HISTORY_LENGTH:]
        
        # Synchronize current position and angle to the last point in the kept history
        if t.history:
            t.cam_m, t.cam_l = t.history[-1]
            t.last_theta = np.arctan2(t.cam_l, t.cam_m)
        else:
            # Fallback to HINT if history somehow got lost
            t.cam_m, t.cam_l = HINTS[i]
            t.last_theta = np.arctan2(t.cam_l, t.cam_m)
            
        t.width = 8.0 if t.type == 'STRONG' else 6.0 # Reset zoom


# --- MAIN LOOP (Modified) ---

def run_fusion_core():
    print("--- 🔥 INITIATING FUSION CORE PROTOCOL (ORBITAL NIB) ---")
    
    trackers = [FusionTracker(h, i) for i, h in enumerate(HINTS)]
    frames_buffer = []
    
    # NEW STEP: Pre-run 10 frames to build up orbital dynamics and sync the history.
    pre_run_stabilization(trackers, frames=10) 
        
    for f in range(FRAMES):
        pulse = {
            'theta': 2 * np.pi * (f / 100),
            'amp_boost': 1.0 + 0.1 * np.sin(f * 0.2)
        }
        
        for t in trackers: t.update(pulse)
        
        # 1. Pilots
        pilots = [t.render_pilot(pulse) for t in trackers]
        panel_a = Image.new('RGB', (PILOT_PANEL_W, MAIN_H))
        for i in range(3): panel_a.paste(pilots[i], (0, i * PILOT_SIZE))
        for i in range(3): panel_a.paste(pilots[i+3], (PILOT_SIZE, i * PILOT_SIZE))
            
        # 2. Map
        raw_map = render_microscope(0, 0, GLOBAL_SCALE, MAP_DIM, 
                                     SRC_STRONG_M, SRC_STRONG_L, SRC_WEAK_M, SRC_WEAK_L, 
                                     pulse['theta'], pulse['amp_boost'])
                                     
        norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
        norm_map = np.power(norm_map, 0.4)
        map_rgb = (plt.get_cmap('inferno')(norm_map)[:, :, :3] * 255).astype(np.uint8)
        
        panel_b = Image.fromarray(np.flipud(map_rgb))
        d_map = ImageDraw.Draw(panel_b)
        
        curr_px = []
        # History drawing uses the full history, which is now stabilized by the pre-run.
        for i, t in enumerate(trackers):
            pts = []
            # Start drawing from the synchronized history buffer
            for (tm, tl) in t.history:
                px = (tm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1)
                py = MAP_DIM - 1 - ((tl - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1))
                pts.append((px, py))
            if len(pts) > 1: d_map.line(pts, fill=COLORS[i], width=2)
            
            cx, cy = pts[-1]
            if t.type == 'STRONG':
                 d_map.ellipse([cx-4, cy-4, cx+4, cy+4], fill=COLORS[i], outline=(255,255,255))
            else:
                 d_map.ellipse([cx-3, cy-3, cx+3, cy+3], fill=COLORS[i], outline=(255,255,255))
            curr_px.append(pts[-1])
        
        s_px = curr_px[0:3]
        g_px = curr_px[3:6]
        if len(s_px) == 3: d_map.polygon(s_px, outline=(200, 200, 200), width=1)
        if len(g_px) == 3: d_map.polygon(g_px, outline=(100, 100, 100), width=1)

        # 3. Helix Lattice
        panel_c = render_helix_lattice(trackers, SIDE_W, MAIN_H)

        # 4. Bottom Panel
        panel_d = render_spectrograph(trackers, TOTAL_W, BOTTOM_H)
        
        # 5. Composite
        final = Image.new('RGB', (TOTAL_W, MAIN_H + BOTTOM_H))
        final.paste(panel_a, (0, 0))
        final.paste(panel_b, (PILOT_PANEL_W, 0))
        final.paste(panel_c, (PILOT_PANEL_W + MAP_DIM, 0))
        final.paste(panel_d, (0, MAIN_H))
        
        frames_buffer.append(final)
        if f % 20 == 0: print(f"Frame {f} | Tracking Fusion Core (ORBITAL NIB engaged)...")

    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ ORBITAL NIB PROTOCOL ACTIVE.")

if __name__ == "__main__":
    run_fusion_core()