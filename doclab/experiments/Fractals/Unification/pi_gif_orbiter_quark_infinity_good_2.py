import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# =========================================================
#  PROTON ENGINE: "DEEP GHOST HUNTER" PROTOCOL (MODIFIED)
# =========================================================

# --- CONFIGURATION (Mostly inherited) ---
OUTPUT_FILENAME = "deep_ghost_collage.gif"
FRAMES = 120            # Reduced for runtime
GLOBAL_SCALE = 32.0     

# LAYOUT DIMENSIONS for the Deep Collage
PILOT_SIZE = 150        
PILOT_COLS = 3          # New layout for a 3x3 grid or similar
DEEP_COLLAGE_W = PILOT_SIZE * PILOT_COLS
DEEP_COLLAGE_H = PILOT_SIZE * PILOT_COLS
TOTAL_W = DEEP_COLLAGE_W
TOTAL_H = DEEP_COLLAGE_H

# PHYSICS: 6 SOURCES
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_WEAK_M = np.array([5.0, 5.0, -5.0]) 
SRC_WEAK_L = np.array([-5.0, 2.5, 2.5]) 

# TARGET HINTS
HINTS_STRONG = [(-10.0, 5.0), (10.0, 5.0), (0.0, -10.0)]
HINTS_GHOST = [(0.0, 5.0), (5.0, -2.5), (-5.0, -2.5)]

# NEW TARGET HINTS for Deep Scan - Offset from original Ghosts
# We are searching near the initial Ghost positions, but with a slight offset
HINTS_DEEP_GHOST = [
    (HINTS_GHOST[0][0] + 1.0, HINTS_GHOST[0][1] + 1.0), # Near G-1
    (HINTS_GHOST[1][0] - 1.0, HINTS_GHOST[1][1] + 0.5), # Near G-2
    (HINTS_GHOST[2][0] + 0.5, HINTS_GHOST[2][1] - 1.0), # Near G-3
    # Add a couple more deeper points near the center for variety
    (-2.0, -2.0),
    (2.0, -2.0),
]

COLORS_STRONG = [(0, 255, 255), (255, 0, 255), (255, 255, 0)] 
COLORS_GHOST = [(255, 50, 50), (50, 255, 50), (50, 100, 255)] 
# New Color for Deep Scan - A variation of Ghost color
COLORS_DEEP = [(255, 150, 150), (150, 255, 150), (150, 150, 255), (255, 200, 50), (50, 200, 255)] 

# --- MATH KERNEL (VECTORIZED) ---

def render_microscope(center_m, center_l, width, res, pulse):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    M, L = np.meshgrid(m_vals, l_vals)
    
    psi_real = np.zeros((res, res), dtype=np.float64)
    psi_imag = np.zeros((res, res), dtype=np.float64)
    
    theta = pulse['theta']
    c, s = np.cos(theta), np.sin(theta)
    
    # 1. STRONG SOURCES (Unchanged)
    for i in range(3):
        sm = SRC_STRONG_M[i]*c - SRC_STRONG_L[i]*s
        sl = SRC_STRONG_M[i]*s + SRC_STRONG_L[i]*c
        
        dx = M - sm
        dy = L - sl
        r = np.sqrt(dx**2 + dy**2)
        r[r < 1e-12] = 1e-12
        
        k = (2 * np.pi) / (10.0)
        phase = k * r
        amp = (1.0 / r)
        psi_real += amp * np.cos(phase)
        psi_imag += amp * np.sin(phase)

    # 2. GHOST SOURCES (Unchanged)
    for i in range(3):
        sm = SRC_WEAK_M[i]*c - SRC_WEAK_L[i]*s
        sl = SRC_WEAK_M[i]*s + SRC_WEAK_L[i]*c
        
        dx = M - sm
        dy = L - sl
        r = np.sqrt(dx**2 + dy**2)
        r[r < 1e-12] = 1e-12
        
        k = (2 * np.pi) / (5.0) 
        phase = k * r
        amp = (0.4 / r) 
        psi_real += amp * np.cos(phase)
        psi_imag += amp * np.sin(phase)

    return psi_real**2 + psi_imag**2

def find_peak(img, width, center_m, center_l):
    res = img.shape[0]
    idx = np.unravel_index(np.argmax(img), img.shape)
    pixel_l = (center_l - width/2) + idx[0] * (width / (res - 1))
    pixel_m = (center_m - width/2) + idx[1] * (width / (res - 1))
    return np.max(img), pixel_m, pixel_l

# --- TRACKER (Modified to accept color and initial width) ---

class ParticleTracker:
    def __init__(self, hint, pid, ptype, color, initial_width):
        self.id = pid
        self.type = ptype 
        self.cam_m, self.cam_l = hint
        self.width = initial_width
        self.color = color
        self.history = []
        self.intensity_log = []
        
    def update(self, pulse):
        # 1. Scan
        scan = render_microscope(self.cam_m, self.cam_l, self.width, 80, pulse)
        
        # 2. Lock
        peak, pm, pl = find_peak(scan, self.width, self.cam_m, self.cam_l)
        
        # 3. Move (Damped)
        # Use a slightly less aggressive damp for deeper tracking
        damp = 0.4 if self.type == 'STRONG' else 0.1
        self.cam_m += (pm - self.cam_m) * damp
        self.cam_l += (pl - self.cam_l) * damp
        
        self.history.append((self.cam_m, self.cam_l))
        self.intensity_log.append(peak)

    def render_pilot(self, pulse):
        # Context - wider view for orientation
        ctx_w = self.width * 5.0
        raw_ctx = render_microscope(self.cam_m, self.cam_l, ctx_w, PILOT_SIZE, pulse)
        norm_ctx = (raw_ctx - raw_ctx.min()) / (raw_ctx.max() - raw_ctx.min() + 1e-9)
        
        # Core - the main target area
        raw_core = render_microscope(self.cam_m, self.cam_l, self.width, PILOT_SIZE, pulse)
        norm_core = (raw_core - raw_core.min()) / (raw_core.max() - raw_core.min() + 1e-9)
        
        # Blend
        boost = 0.6 if self.type == 'GHOST' or self.type == 'DEEP_GHOST' else 0.3
        final = (norm_core * 0.7) + (norm_ctx * boost)
        final = np.clip(final, 0, 1)
        
        # Colorize (using 'hot' colormap for intensity)
        cmap = plt.get_cmap('hot')
        rgb_hot = cmap(final)[:, :, :3]
        
        # Overlay with tracker color
        c_vec = np.array(self.color) / 255.0
        rgb = np.dstack((rgb_hot[:,:,0] * c_vec[0], rgb_hot[:,:,1] * c_vec[1], rgb_hot[:,:,2] * c_vec[2]))
        
        # Hotspot
        mask = norm_core > 0.9
        rgb[mask] = rgb[mask] * 0.5 + 0.5 # Brighten peak
        
        img = Image.fromarray((rgb * 255).astype(np.uint8))
        d = ImageDraw.Draw(img)
        
        # Labeling
        if self.type == 'STRONG':
            label = f"M-{self.id+1}"
        elif self.type == 'GHOST':
            label = f"G-{self.id+1}"
        else: # DEEP_GHOST
            label = f"D-G-{self.id+1}"
            
        d.text((5, 5), label, fill=self.color)
        return img

# --- DASHBOARD RENDERER (Removed for collage focus) ---

# --- MISSION (Modified to focus on Deep Ghosts) ---

def run_deep_ghost_hunt():
    print("--- 👻 PUSHING LIMITS: DEEP GHOST PROTOCOL ---")
    
    # We only need the Deep Ghost trackers for the final collage
    deep_trackers = []
    
    # 5 Deep Ghosts - using a smaller initial width (e.g., 2.0)
    # The default Ghost width was 6.0
    for i, h in enumerate(HINTS_DEEP_GHOST):
        deep_trackers.append(ParticleTracker(h, i, 'DEEP_GHOST', COLORS_DEEP[i], 2.0))
        
    frames_buffer = []
    
    # 1. Run the simulation
    for f in range(FRAMES):
        pulse = {
            'theta': 2 * np.pi * (f / 100),
            'amp_boost': 1.0 + 0.2 * np.sin(f * 0.1)
        }
        
        # Update ALL Deep Trackers
        for t in deep_trackers: t.update(pulse)
        
        # 2. Render Deep Pilot Collage (3x2 or 3x3 layout)
        pilots = [t.render_pilot(pulse) for t in deep_trackers]
        
        # Create a new collage panel
        collage = Image.new('RGB', (TOTAL_W, TOTAL_H), (0, 0, 0))
        d_collage = ImageDraw.Draw(collage)
        d_collage.text((10, 10), "DEEP GHOST COLLAGE: SUBSYSTEM ANALYSIS", fill=(200, 200, 255))
        
        # Paste the pilot screens (e.g., in a 3x3 grid, skipping one row)
        row_max = (len(pilots) + PILOT_COLS - 1) // PILOT_COLS # Determine number of rows needed
        
        for i, pilot_img in enumerate(pilots):
            row = i // PILOT_COLS
            col = i % PILOT_COLS
            if row < row_max:
                collage.paste(pilot_img, (col * PILOT_SIZE, row * PILOT_SIZE + 40)) # Offset for title
        
        frames_buffer.append(collage)
        if f % 20 == 0: print(f"Frame {f} | Tracking {len(deep_trackers)} Deep Targets...")

    
    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ DEEPER GHOSTS CAPTURED.")

if __name__ == "__main__":
    run_deep_ghost_hunt()