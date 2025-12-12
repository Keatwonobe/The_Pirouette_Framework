import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFilter

# =========================================================
#  PROTON ENGINE: PHOSPHOR PERSISTENCE TRACKING
#  "Letting the bright spots draw the trails"
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_phosphor_trails.gif"
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

# TARGET HINTS
HINTS = [(-10.0, 5.0), (10.0, 5.0), (0.0, -10.0), # Strong Hints
         (5.0, 5.0), (5.0, -2.5), (-5.0, -2.5)]   # Ghost Hints

# COLORS 
COLORS_STRONG = [(0, 255, 255), (255, 0, 255), (255, 255, 0)] 
COLORS_GHOST = [(255, 50, 50), (50, 255, 50), (50, 100, 255)]
COLORS = COLORS_STRONG + COLORS_GHOST

# --- MATH KERNEL (NUMBA) ---

@njit(parallel=True)
def render_microscope(center_m, center_l, width, res, src_m_s, src_l_s, src_m_w, src_l_w, global_theta, amp_boost):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    intensity_map = np.zeros((res, res), dtype=np.float64)
    
    c, s = np.cos(global_theta), np.sin(global_theta)
    
    # STRONG Sources (Low Frequency, High Amp)
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
                
    # WEAK Sources (High Frequency, Low Amp)
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

@njit
def paint_trail_blob(trail_layer, x_px, y_px, radius, color, decay):
    """
    Directly paints a soft blob onto the trail accumulation buffer.
    """
    h, w, _ = trail_layer.shape
    
    # Decay existing
    for i in range(h):
        for j in range(w):
            for c in range(3):
                trail_layer[i, j, c] *= decay

    # Paint new blob
    ix = int(x_px)
    iy = int(y_px)
    r_int = int(radius) + 2
    
    for dy in range(-r_int, r_int+1):
        for dx in range(-r_int, r_int+1):
            ny, nx = iy + dy, ix + dx
            if 0 <= ny < h and 0 <= nx < w:
                dist = np.sqrt(dx*dx + dy*dy)
                if dist < radius:
                    intensity = 1.0 - (dist / radius)
                    # Additive blending
                    for c in range(3):
                        val = trail_layer[ny, nx, c] + (color[c] * intensity * 0.8)
                        if val > 255: val = 255
                        trail_layer[ny, nx, c] = val
    return trail_layer

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

class PhosphorTracker:
    def __init__(self, hint, particle_id):
        self.id = particle_id
        self.type = 'STRONG' if particle_id < 3 else 'GHOST'
        self.color = COLORS[particle_id]
        self.cam_m, self.cam_l = hint
        
        # Fixed Widths - Stabilization
        self.width = 10.0 if self.type == 'STRONG' else 8.0
        
        # Damping
        self.damp_factor = 0.5 
        self.last_theta = np.arctan2(self.cam_l, self.cam_m)
        self.omega = 0.0 
        self.alpha = 0.0 
        self.intensity_log = [] 
        self.history = [] # Only used for helix, not map lines
        self.locked = False
        
    def update(self, pulse):
        # 1. Scan
        scan = render_microscope(self.cam_m, self.cam_l, self.width, 80, 
                                 SRC_STRONG_M, SRC_STRONG_L, SRC_WEAK_M, SRC_WEAK_L, 
                                 pulse['theta'], pulse['amp_boost'])
        
        # 2. Find Peak (Standardized search)
        peak_val, peak_m, peak_l = find_peak(scan, self.width, self.cam_m, self.cam_l, 0.6)
        
        self.locked = peak_val > 0.001
        
        if self.locked:
            # Move towards peak
            self.cam_m += (peak_m - self.cam_m) * self.damp_factor
            self.cam_l += (peak_l - self.cam_l) * self.damp_factor
            
            # Update angular prediction for when lock is lost
            curr_theta = np.arctan2(self.cam_l, self.cam_m)
            diff = curr_theta - self.last_theta
            if diff > np.pi: diff -= 2*np.pi
            if diff < -np.pi: diff += 2*np.pi
            self.omega = diff
            self.last_theta = curr_theta
        else:
            # Inertial drift if lost
            pred_theta = self.last_theta + self.omega
            r = np.sqrt(self.cam_m**2 + self.cam_l**2)
            self.cam_m = r * np.cos(pred_theta)
            self.cam_l = r * np.sin(pred_theta)
            self.last_theta = pred_theta

        self.history.append((self.cam_m, self.cam_l))
        self.intensity_log.append(peak_val)

    def render_pilot(self, pulse):
        # Render Pilot View
        raw = render_microscope(self.cam_m, self.cam_l, self.width, PILOT_SIZE, 
                                     SRC_STRONG_M, SRC_STRONG_L, SRC_WEAK_M, SRC_WEAK_L, 
                                     pulse['theta'], pulse['amp_boost'])
        
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.5) 
        
        base_c = np.array(self.color) / 255.0
        img_rgb = np.dstack((norm * base_c[0], norm * base_c[1], norm * base_c[2]))
        
        # Hotspot
        mask = norm > 0.85
        img_rgb[mask] = img_rgb[mask] * 0.5 + 0.5
        
        img_uint8 = (img_rgb * 255).astype(np.uint8)
        img_uint8 = np.flipud(img_uint8)
        pil = Image.fromarray(img_uint8)
        d = ImageDraw.Draw(pil)
        label = f"M-{self.id+1}" if self.type == 'STRONG' else f"G-{self.id-2}"
        d.text((5, 5), label, fill=COLORS[self.id])
        return pil

# --- HELIX LATTICE (Side View) ---
def render_helix_lattice(trackers, width, height):
    pil_side = Image.new('RGB', (width, height), (10, 5, 20))
    d_side = ImageDraw.Draw(pil_side)
    d_side.text((10, 10), "ORBITAL LATTICE", fill=(150, 150, 150))
    
    max_len = height - 50 
    hist_len = min(len(t.history) for t in trackers)
    
    # Grab last N frames
    start_idx = max(0, hist_len - max_len)
    
    start_y = 30
    y_step = 1.0 # 1 pixel per frame
    
    for i in range(start_idx, hist_len):
        draw_y = start_y + (i - start_idx) * y_step
        
        row_px = []
        for t in trackers:
            qm, ql = t.history[i]
            px_x = (qm - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (width - 1)
            
            norm_d = ql / (GLOBAL_SCALE/2) 
            rad = 2
            
            d_side.point((px_x, draw_y), fill=t.color)
            row_px.append(px_x)
            
        # Draw connectivity lines every 10 frames
        if i % 10 == 0:
            if len(row_px) == 6:
               d_side.line([(row_px[0], draw_y), (row_px[1], draw_y)], fill=(50,50,50))
               d_side.line([(row_px[1], draw_y), (row_px[2], draw_y)], fill=(50,50,50))
               d_side.line([(row_px[2], draw_y), (row_px[0], draw_y)], fill=(50,50,50))
               
               d_side.line([(row_px[3], draw_y), (row_px[4], draw_y)], fill=(30,30,30))
               d_side.line([(row_px[4], draw_y), (row_px[5], draw_y)], fill=(30,30,30))
               d_side.line([(row_px[5], draw_y), (row_px[3], draw_y)], fill=(30,30,30))

    return pil_side.transpose(Image.FLIP_TOP_BOTTOM)

# --- MAIN LOOP ---

def run_phosphor_engine():
    print("--- ☢️ INITIATING PHOSPHOR ENGINE ---")
    
    trackers = [PhosphorTracker(h, i) for i, h in enumerate(HINTS)]
    frames_buffer = []
    
    # Initialize Persistent Phosphor Layer (Float array)
    phosphor_layer = np.zeros((MAP_DIM, MAP_DIM, 3), dtype=np.float64)
    
    # Pre-run for stability
    print("Stabilizing trackers...")
    for f in range(20):
        pulse = {'theta': 2 * np.pi * (f / 100), 'amp_boost': 1.0}
        for t in trackers: t.update(pulse)
        # Clear history so helix starts clean
        if f == 19: 
            for t in trackers: t.history = []
    
    print("Rendering frames...")
    for f in range(FRAMES):
        pulse = {
            'theta': 2 * np.pi * (f / 100),
            'amp_boost': 1.0 + 0.1 * np.sin(f * 0.2)
        }
        
        # 1. Update Trackers
        for t in trackers: t.update(pulse)
        
        # 2. Update Phosphor Map (The "Trail Painting" step)
        # Decay first
        phosphor_layer *= 0.92 # 8% decay per frame (Long trails)
        
        # Paint new dots onto the layer
        for t in trackers:
            # Convert world coords to map pixels
            px = (t.cam_m - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1)
            # Flip Y for drawing
            py = MAP_DIM - 1 - ((t.cam_l - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1))
            
            # Paint blob (Size depends on type)
            blob_size = 5.0 if t.type == 'STRONG' else 3.0
            
            # This Numba function modifies phosphor_layer in place
            # Note: We pass raw color, paint_trail_blob handles blending
            # Numba expects colors as float/int consistent with array
            paint_c = np.array(t.color, dtype=np.float64)
            paint_trail_blob(phosphor_layer, px, py, blob_size, paint_c, 1.0) # Decay handled globally above

        # 3. Render Background Map
        raw_map = render_microscope(0, 0, GLOBAL_SCALE, MAP_DIM, 
                                     SRC_STRONG_M, SRC_STRONG_L, SRC_WEAK_M, SRC_WEAK_L, 
                                     pulse['theta'], pulse['amp_boost'])
        norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
        norm_map = np.power(norm_map, 0.4)
        map_rgb = (plt.get_cmap('inferno')(norm_map)[:, :, :3] * 255) # Float array
        map_rgb = np.flipud(map_rgb)
        
        # 4. Composite Phosphor + Map
        # Add phosphor layer to map (Additive)
        combined_map = map_rgb + phosphor_layer
        combined_map = np.clip(combined_map, 0, 255).astype(np.uint8)
        
        panel_b = Image.fromarray(combined_map)
        d_map = ImageDraw.Draw(panel_b)
        
        # Draw current "heads" (Hard dots)
        curr_px = []
        for t in trackers:
            px = (t.cam_m - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1)
            py = MAP_DIM - 1 - ((t.cam_l - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM - 1))
            
            r = 3 if t.type == 'STRONG' else 2
            d_map.ellipse([px-r, py-r, px+r, py+r], fill=(255,255,255), outline=t.color)
            curr_px.append((px, py))
            
        # Draw Linkage Lines (Only for current frame, no history lines)
        s_px = curr_px[0:3]
        g_px = curr_px[3:6]
        d_map.polygon(s_px, outline=(200, 200, 200, 128))
        d_map.polygon(g_px, outline=(100, 100, 100, 128))
        
        # 5. Render Pilots
        pilots = [t.render_pilot(pulse) for t in trackers]
        panel_a = Image.new('RGB', (PILOT_PANEL_W, MAIN_H))
        for i in range(3): panel_a.paste(pilots[i], (0, i * PILOT_SIZE))
        for i in range(3): panel_a.paste(pilots[i+3], (PILOT_SIZE, i * PILOT_SIZE))
        
        # 6. Render Helix
        panel_c = render_helix_lattice(trackers, SIDE_W, MAIN_H)
        
        # 7. Final Composite
        final = Image.new('RGB', (TOTAL_W, MAIN_H))
        final.paste(panel_a, (0, 0))
        final.paste(panel_b, (PILOT_PANEL_W, 0))
        final.paste(panel_c, (PILOT_PANEL_W + MAP_DIM, 0))
        
        frames_buffer.append(final)
        
        if f % 20 == 0: print(f"Frame {f} | Phosphor persistence active...")

    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ TRAILS GENERATED.")

if __name__ == "__main__":
    run_phosphor_engine()