import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

# =========================================================
#  PROTON ENGINE: "GHOST HUNTER" PROTOCOL
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_ghost_hunter.gif"
FRAMES = 140            
GLOBAL_SCALE = 32.0     # Widened slightly to catch outer ghosts

# LAYOUT DIMENSIONS
PILOT_SIZE = 150        
PILOT_COLS = 2          # 2 Columns of pilots (Main + Ghost)
PILOT_PANEL_W = PILOT_SIZE * PILOT_COLS
MAP_DIM = 450           
SIDE_W = 250            # Narrowed Helix slightly to fit width
MAIN_H = 450            
BOTTOM_H = 150          
TOTAL_W = PILOT_PANEL_W + MAP_DIM + SIDE_W

# PHYSICS: 6 SOURCES (3 Strong, 3 Weak)
# Main Triangle
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
# Ghost Triangle (Inverted/Nodes)
# Roughly midpoints or anti-nodes
SRC_WEAK_M = np.array([0.0, 5.0, -5.0]) 
SRC_WEAK_L = np.array([-5.0, 2.5, 2.5]) # Approximate interference nodes

# TARGET HINTS
HINTS_STRONG = [(-10.0, 5.0), (10.0, 5.0), (0.0, -10.0)]
HINTS_GHOST = [(0.0, 5.0), (5.0, -2.5), (-5.0, -2.5)] # Midpoints

COLORS_STRONG = [(0, 255, 255), (255, 0, 255), (255, 255, 0)] # C M Y
COLORS_GHOST = [(255, 50, 50), (50, 255, 50), (50, 100, 255)]  # R G B

# --- MATH KERNEL ---

def render_microscope(center_m, center_l, width, res, pulse):
    # Vectorized Field Generator
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    M, L = np.meshgrid(m_vals, l_vals)
    
    psi_real = np.zeros((res, res), dtype=np.float64)
    psi_imag = np.zeros((res, res), dtype=np.float64)
    
    # 1. STRONG SOURCES (Amp 1.0)
    # Rotating logic handled outside? No, let's rotate sources inside loop for simplicity
    # actually, efficient to pass rotated coords.
    # We'll stick to a simpler static interference for stability + rotation of the *System*
    
    # Time-dependent rotation of sources
    theta = pulse['theta']
    c, s = np.cos(theta), np.sin(theta)
    
    # Process Strong
    for i in range(3):
        # Rotate Source
        sm = SRC_STRONG_M[i]*c - SRC_STRONG_L[i]*s
        sl = SRC_STRONG_M[i]*s + SRC_STRONG_L[i]*c
        
        dx = M - sm
        dy = L - sl
        r = np.sqrt(dx**2 + dy**2)
        r[r < 1e-12] = 1e-12
        
        k = (2 * np.pi) / (10.0) # Fixed k for stability
        phase = k * r
        amp = (1.0 / r)
        psi_real += amp * np.cos(phase)
        psi_imag += amp * np.sin(phase)

    # 2. GHOST SOURCES (Amp 0.4 - The "Substrate Boost")
    # These represent the "hidden" manifold resonance
    for i in range(3):
        sm = SRC_WEAK_M[i]*c - SRC_WEAK_L[i]*s
        sl = SRC_WEAK_M[i]*s + SRC_WEAK_L[i]*c
        
        dx = M - sm
        dy = L - sl
        r = np.sqrt(dx**2 + dy**2)
        r[r < 1e-12] = 1e-12
        
        k = (2 * np.pi) / (5.0) # Higher frequency resonance
        phase = k * r
        amp = (0.4 / r) # Weaker
        psi_real += amp * np.cos(phase)
        psi_imag += amp * np.sin(phase)

    return psi_real**2 + psi_imag**2

def find_peak(img, width, center_m, center_l):
    res = img.shape[0]
    # Simple max find
    idx = np.unravel_index(np.argmax(img), img.shape)
    # Map back
    pixel_l = (center_l - width/2) + idx[0] * (width / (res - 1))
    pixel_m = (center_m - width/2) + idx[1] * (width / (res - 1))
    return np.max(img), pixel_m, pixel_l

# --- TRACKER ---

class ParticleTracker:
    def __init__(self, hint, pid, ptype):
        self.id = pid
        self.type = ptype # 'STRONG' or 'GHOST'
        self.cam_m, self.cam_l = hint
        self.width = 6.0 if ptype == 'GHOST' else 8.0
        self.color = COLORS_GHOST[pid] if ptype == 'GHOST' else COLORS_STRONG[pid]
        self.history = []
        self.intensity_log = []
        
    def update(self, pulse):
        # 1. Scan
        scan = render_microscope(self.cam_m, self.cam_l, self.width, 80, pulse)
        
        # 2. Lock
        peak, pm, pl = find_peak(scan, self.width, self.cam_m, self.cam_l)
        
        # 3. Move (Damped tracking)
        # Ghosts are jittery, Strong are stable
        damp = 0.5 if self.type == 'STRONG' else 0.2
        self.cam_m += (pm - self.cam_m) * damp
        self.cam_l += (pl - self.cam_l) * damp
        
        self.history.append((self.cam_m, self.cam_l))
        self.intensity_log.append(peak)

    def render_pilot(self, pulse):
        # Dual Layer "Candlelight"
        # Context Layer
        ctx_w = self.width * 5.0
        raw_ctx = render_microscope(self.cam_m, self.cam_l, ctx_w, PILOT_SIZE, pulse)
        norm_ctx = (raw_ctx - raw_ctx.min()) / (raw_ctx.max() - raw_ctx.min() + 1e-9)
        
        # Core Layer
        raw_core = render_microscope(self.cam_m, self.cam_l, self.width, PILOT_SIZE, pulse)
        norm_core = (raw_core - raw_core.min()) / (raw_core.max() - raw_core.min() + 1e-9)
        
        # Blend: Boost substrate for ghosts
        boost = 0.6 if self.type == 'GHOST' else 0.3
        final = (norm_core * 0.7) + (norm_ctx * boost)
        final = np.clip(final, 0, 1)
        
        # Colorize
        c_vec = np.array(self.color) / 255.0
        rgb = np.dstack((final * c_vec[0], final * c_vec[1], final * c_vec[2]))
        
        # Hotspot
        mask = norm_core > 0.9
        rgb[mask] = rgb[mask] * 0.5 + 0.5
        
        img = Image.fromarray((rgb * 255).astype(np.uint8))
        d = ImageDraw.Draw(img)
        label = f"M-{self.id+1}" if self.type == 'STRONG' else f"G-{self.id+1}"
        d.text((5, 5), label, fill=self.color)
        return img

# --- DASHBOARD RENDERER ---

def render_spectrograph(trackers, width, height):
    img = Image.new('RGB', (width, height), (5, 5, 10))
    d = ImageDraw.Draw(img)
    
    d.text((20, 10), "RESONANCE SPECTROGRAPH [GHOST INTENSITY]", fill=(200, 200, 200))
    
    # Plot area
    plot_h = height - 40
    plot_w = width - 40
    ox, oy = 20, 30
    
    # Draw Ghost traces
    ghosts = [t for t in trackers if t.type == 'GHOST']
    
    for g in ghosts:
        data = g.intensity_log[-100:] # Last 100 frames
        if not data: continue
        
        # Normalize local to track relative strength
        d_min, d_max = min(data), max(data)
        if d_max == d_min: d_max += 1e-9
        
        pts = []
        step_x = plot_w / 100
        
        for i, val in enumerate(data):
            x = ox + i * step_x
            # Y scales with intensity
            norm_y = (val - d_min) / (d_max - d_min)
            y = (oy + plot_h) - (norm_y * plot_h)
            pts.append((x, y))
            
        if len(pts) > 1:
            d.line(pts, fill=g.color, width=2)
            
    # Overlay grid
    d.line([ox, oy+plot_h/2, ox+plot_w, oy+plot_h/2], fill=(50, 50, 50))
    
    return img

# --- MISSION ---

def run_ghost_hunt():
    print("--- 👻 INITIATING GHOST PROTOCOL ---")
    
    # Initialize 6 Trackers
    trackers = []
    # 3 Strong
    for i, h in enumerate(HINTS_STRONG):
        trackers.append(ParticleTracker(h, i, 'STRONG'))
    # 3 Ghosts
    for i, h in enumerate(HINTS_GHOST):
        trackers.append(ParticleTracker(h, i, 'GHOST'))
        
    frames_buffer = []
    
    for f in range(FRAMES):
        # Physics Pulse
        pulse = {
            'theta': 2 * np.pi * (f / 100),
            'amp_boost': 1.0 + 0.2 * np.sin(f * 0.1)
        }
        
        # 1. Update Trackers
        for t in trackers: t.update(pulse)
        
        # 2. Render Panel A: Pilots (2x3 Grid)
        pilots = [t.render_pilot(pulse) for t in trackers]
        panel_a = Image.new('RGB', (PILOT_PANEL_W, MAIN_H))
        
        # Layout: Main Left, Ghost Right
        for i in range(3):
            # Main (Strong)
            panel_a.paste(pilots[i], (0, i * PILOT_SIZE))
            # Ghost
            panel_a.paste(pilots[i+3], (PILOT_SIZE, i * PILOT_SIZE))
            
        # 3. Render Panel B: Map (Lattice)
        raw_map = render_microscope(0, 0, GLOBAL_SCALE, MAP_DIM, pulse)
        norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
        norm_map = np.power(norm_map, 0.4)
        map_rgb = (plt.get_cmap('inferno')(norm_map)[:, :, :3] * 255).astype(np.uint8)
        panel_b = Image.fromarray(np.flipud(map_rgb))
        d_map = ImageDraw.Draw(panel_b)
        
        # Draw Hexagonal Lattice
        # Connect Strong->Strong (Triangle)
        strong_pts = [t.history[-1] for t in trackers if t.type=='STRONG']
        ghost_pts = [t.history[-1] for t in trackers if t.type=='GHOST']
        
        def to_px(m, l):
            x = (m - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM-1)
            y = (MAP_DIM-1) - ((l - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM-1))
            return x, y
            
        s_px = [to_px(*p) for p in strong_pts]
        g_px = [to_px(*p) for p in ghost_pts]
        
        if len(s_px) == 3:
            d_map.polygon(s_px, outline=(200, 200, 200), width=1)
        if len(g_px) == 3:
            d_map.polygon(g_px, outline=(100, 100, 100), width=1)
            
        # Draw Linkages (Strong->Ghost)
        # Connect each Ghost to nearest Strong?
        # Just draw points for now to reduce clutter
        for i, p in enumerate(s_px):
            d_map.ellipse([p[0]-4, p[1]-4, p[0]+4, p[1]+4], fill=COLORS_STRONG[i], outline=(255,255,255))
        for i, p in enumerate(g_px):
            d_map.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=COLORS_GHOST[i], outline=(255,255,255))
            
        # 4. Render Panel C: Helix (Side View)
        # Simplified side view of all 6
        panel_c = Image.new('RGB', (SIDE_W, MAIN_H), (10, 5, 20))
        d_side = ImageDraw.Draw(panel_c)
        d_side.text((10, 10), "HELIX [ALL TRACKS]", fill=(150, 150, 150))
        
        # Draw only last 50 frames to keep it clean
        hist_len = 50
        y_step = (MAIN_H - 20) / hist_len
        start_y = 20
        
        for ti, t in enumerate(trackers):
            hist = t.history[-hist_len:]
            pts = []
            for i, (m, l) in enumerate(hist):
                # X = M, Y = Time
                px = (m - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (SIDE_W - 1)
                py = start_y + i * y_step
                pts.append((px, py))
            if len(pts) > 1:
                d_side.line(pts, fill=t.color, width=2)

        # 5. Render Panel D: Bottom Spectrograph
        panel_d = render_spectrograph(trackers, TOTAL_W, BOTTOM_H)
        
        # 6. Composite
        final = Image.new('RGB', (TOTAL_W, MAIN_H + BOTTOM_H))
        final.paste(panel_a, (0, 0))
        final.paste(panel_b, (PILOT_PANEL_W, 0))
        final.paste(panel_c, (PILOT_PANEL_W + MAP_DIM, 0))
        final.paste(panel_d, (0, MAIN_H))
        
        frames_buffer.append(final)
        if f % 20 == 0: print(f"Frame {f} | Tracking 6 Targets...")

    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ GHOSTS CAPTURED.")

if __name__ == "__main__":
    run_ghost_hunt()