import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# =========================================================
#  PROTON ENGINE: "GHOST HUNTER" PROTOCOL (NO NUMBA)
#  MODIFIED FOR FRACTAL ZOOM SEQUENCE (FIXED 'initial_width')
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "fractal_zoom_montage.gif"
FROZEN_FRAME_THETA = 0.5  # Fixed theta to 'freeze' the field
ZOOM_STEPS = 20           # Number of zoom steps per particle
FINAL_ZOOM_FACTOR = 100.0 # Total magnification (e.g., width goes from 8.0 to 8.0/100)

# LAYOUT DIMENSIONS
ZOOM_SIZE = 450         # The size of the final zoom-in panel
MAIN_H = ZOOM_SIZE      
TOTAL_W = ZOOM_SIZE

# PHYSICS: 6 SOURCES (Retained from original)
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_WEAK_M = np.array([5.0, 5.0, -5.0]) 
SRC_WEAK_L = np.array([-5.0, 2.5, 2.5]) 

# TARGET HINTS (Retained from original)
HINTS_STRONG = [(-10.0, 5.0), (10.0, 5.0), (0.0, -10.0)]
HINTS_GHOST = [(0.0, 5.0), (5.0, -2.5), (-5.0, -2.5)]

COLORS_STRONG = [(0, 255, 255), (255, 0, 255), (255, 255, 0)] 
COLORS_GHOST = [(255, 50, 50), (50, 255, 50), (50, 100, 255)]  

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
    
    # 1. STRONG SOURCES
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

    # 2. GHOST SOURCES
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

# --- TRACKER (Simplified for initial lock) ---

class ParticleTracker:
    def __init__(self, hint, pid, ptype):
        self.id = pid
        self.type = ptype 
        self.cam_m, self.cam_l = hint
        self.width = 6.0 if ptype == 'GHOST' else 8.0
        self.color = COLORS_GHOST[pid] if ptype == 'GHOST' else COLORS_STRONG[pid]
        
    def initial_lock(self, pulse):
        # Scan and lock over a few iterations to settle on the peak
        for _ in range(5):
            scan = render_microscope(self.cam_m, self.cam_l, self.width, 80, pulse)
            peak, pm, pl = find_peak(scan, self.width, self.cam_m, self.cam_l)
            
            # Simple, non-damped move for quick lock
            self.cam_m = pm 
            self.cam_l = pl
            
        # Return the final locked position
        return self.cam_m, self.cam_l


# --- FRACTAL ZOOM RENDERER (FIXED) ---

def render_zoom_frame(center_m, center_l, current_width, initial_width, label, color):
    # 'initial_width' is now passed in as an argument.
    
    # 1. Render the field at the current scale
    # NOTE: 'pulse' is used as a global variable defined in run_fractal_zoom
    raw_map = render_microscope(center_m, center_l, current_width, ZOOM_SIZE, pulse)
    
    # 2. Normalization and Color Mapping (using 'inferno' for contrast)
    norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
    norm_map = np.power(norm_map, 0.4) # Gamma correction for visibility
    map_rgb = (plt.get_cmap('inferno')(norm_map)[:, :, :3] * 255).astype(np.uint8)
    
    # 3. PIL Image preparation
    panel = Image.fromarray(np.flipud(map_rgb))
    d_map = ImageDraw.Draw(panel)
    
    # 4. Add HUD overlay
    zoom_level = (initial_width / current_width)
    display_label = f"[{label}] Zoom: x{zoom_level:.2f} | Width: {current_width:.4f}"
    
    # Text background for legibility
    d_map.rectangle([5, 5, 5 + len(display_label) * 8, 25], fill=(0, 0, 0, 100))
    d_map.text((10, 8), display_label, fill=color)
    
    return panel


# --- MAIN MISSION ---

def run_fractal_zoom():
    print("--- 🔬 INITIATING FRACTAL ZOOM PROTOCOL ---")
    
    global pulse # Define 'pulse' as a global variable so render_zoom_frame can access it
    pulse = {
        'theta': FROZEN_FRAME_THETA,
        'amp_boost': 1.0 
    }
    
    # 1. Initialize and Lock all Trackers to their static peaks
    trackers = []
    # 3 Strong
    for i, h in enumerate(HINTS_STRONG):
        t = ParticleTracker(h, i, 'STRONG')
        t.initial_lock(pulse)
        trackers.append(t)
    # 3 Ghosts
    for i, h in enumerate(HINTS_GHOST):
        t = ParticleTracker(h, i, 'GHOST')
        t.initial_lock(pulse)
        trackers.append(t)
        
    
    # 2. Generate Zoom Sequence for each particle
    frames_buffer = []
    
    for t_idx, tracker in enumerate(trackers):
        
        # Determine the initial view width based on particle type
        initial_width = tracker.width 
        center_m, center_l = tracker.cam_m, tracker.cam_l
        
        particle_label = f"M{t_idx+1}" if tracker.type == 'STRONG' else f"G{t_idx-2}"
        print(f"Generating zoom for {particle_label} at ({center_m:.2f}, {center_l:.2f})")
        
        # Calculate the final width
        final_width = initial_width / FINAL_ZOOM_FACTOR
        
        # Calculate the width for each step (logarithmic decay for smooth zoom)
        widths = np.geomspace(initial_width, final_width, ZOOM_STEPS)
        
        # Add a few static frames at the start of each particle's zoom for context
        for _ in range(3):
            # FIXED: Passing initial_width
            frames_buffer.append(render_zoom_frame(center_m, center_l, initial_width, initial_width, particle_label, tracker.color))

        # Generate the zoom frames
        for i, current_width in enumerate(widths):
            # FIXED: Passing initial_width
            frame = render_zoom_frame(center_m, center_l, current_width, initial_width, particle_label, tracker.color)
            frames_buffer.append(frame)
            
        # Add a few static frames at the end of each zoom to observe the final state
        for _ in range(3):
            # FIXED: Passing initial_width
            frames_buffer.append(render_zoom_frame(center_m, center_l, final_width, initial_width, particle_label, tracker.color))
            
    
    # 3. Save the GIF
    print(f"Saving {OUTPUT_FILENAME} with {len(frames_buffer)} frames...")
    # Use a slightly longer duration for the zoom frames
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=100, loop=0)
    
    print("✅ FRACTAL ZOOM SEQUENCE COMPLETE.")


if __name__ == "__main__":
    run_fractal_zoom()