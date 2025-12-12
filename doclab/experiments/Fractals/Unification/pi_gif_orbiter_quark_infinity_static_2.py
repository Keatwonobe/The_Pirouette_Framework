import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# =========================================================
#  PROTON ENGINE: "GHOST HUNTER" PROTOCOL (NO NUMBA)
#  MODIFIED FOR DYNAMIC, CONTINUOUS TRACKING ZOOM
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "dynamic_fractal_zoom_montage.gif"
TOTAL_FRAMES = 150        # Total frames for the whole montage (More frames = smoother/longer tracking)
ZOOM_FACTOR = 100.0       # Total magnification (e.g., width goes from 8.0 to 8.0/100)
THETA_START = 0.0
THETA_END = 2 * np.pi * 1.5 # 1.5 rotations over the entire sequence

# LAYOUT DIMENSIONS
ZOOM_SIZE = 450         
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

# --- TRACKER (Re-implemented for continuous tracking) ---

class ParticleTracker:
    def __init__(self, hint, pid, ptype):
        self.id = pid
        self.type = ptype 
        self.cam_m, self.cam_l = hint
        self.width = 6.0 if ptype == 'GHOST' else 8.0 # Initial window size
        self.color = COLORS_GHOST[pid] if ptype == 'GHOST' else COLORS_STRONG[pid]
        
    def initial_lock(self, pulse):
        # Scan and lock over a few iterations to settle on the peak
        for _ in range(5):
            scan = render_microscope(self.cam_m, self.cam_l, self.width, 80, pulse)
            peak, pm, pl = find_peak(scan, self.width, self.cam_m, self.cam_l)
            self.cam_m = pm 
            self.cam_l = pl
            
    def update_position(self, pulse, current_width):
        """
        Updates the camera position to track the moving peak.
        Scan window is dynamically set by current_width.
        """
        # The scan window size is slightly larger than the current render window 
        # to ensure the peak is still visible when it moves.
        scan_width = current_width * 1.5 
        
        # 1. Scan
        scan = render_microscope(self.cam_m, self.cam_l, scan_width, 80, pulse)
        
        # 2. Lock
        peak, pm, pl = find_peak(scan, scan_width, self.cam_m, self.cam_l)
        
        # 3. Move (Damped, but less damped than before for better tracking)
        # We move the camera center to the newly found peak position.
        damp = 0.8 
        self.cam_m += (pm - self.cam_m) * damp
        self.cam_l += (pl - self.cam_l) * damp
        # We don't update self.width here; that is controlled by the zoom sequence.
        
        return self.cam_m, self.cam_l


# --- DYNAMIC ZOOM RENDERER ---

def render_zoom_frame(center_m, center_l, current_width, initial_width, label, color):
    
    # 1. Render the field at the current scale
    # NOTE: 'pulse' is used as a global variable
    raw_map = render_microscope(center_m, center_l, current_width, ZOOM_SIZE, pulse)
    
    # 2. Normalization and Color Mapping 
    norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
    norm_map = np.power(norm_map, 0.4) 
    map_rgb = (plt.get_cmap('inferno')(norm_map)[:, :, :3] * 255).astype(np.uint8)
    
    # 3. PIL Image preparation
    panel = Image.fromarray(np.flipud(map_rgb))
    d_map = ImageDraw.Draw(panel)
    
    # 4. Add HUD overlay
    zoom_level = (initial_width / current_width)
    display_label = f"[{label}] Zoom: x{zoom_level:.2f} | Width: {current_width:.4f} | Θ: {pulse['theta']:.3f} rad"
    
    d_map.rectangle([5, 5, 5 + len(display_label) * 8, 25], fill=(0, 0, 0, 100))
    d_map.text((10, 8), display_label, fill=color)
    
    return panel


# --- MAIN MISSION ---

def run_dynamic_fractal_zoom():
    print("--- 🔄 INITIATING DYNAMIC FRACTAL ZOOM PROTOCOL ---")
    
    global pulse # Define 'pulse' as a global variable
    
    # 1. Setup Trackers
    trackers = []
    for i, h in enumerate(HINTS_STRONG):
        t = ParticleTracker(h, i, 'STRONG')
        trackers.append(t)
    for i, h in enumerate(HINTS_GHOST):
        t = ParticleTracker(h, i, 'GHOST')
        trackers.append(t)
    
    # 2. Pre-lock all trackers at the start angle
    pulse = {'theta': THETA_START, 'amp_boost': 1.0}
    for t in trackers:
        t.initial_lock(pulse)
        
    # 3. Generate the sequence of parameters (theta and width)
    
    # Theta changes linearly over time for the entire montage
    thetas = np.linspace(THETA_START, THETA_END, TOTAL_FRAMES)
    
    # The zoom is split evenly among the 6 particles
    FRAMES_PER_PARTICLE = TOTAL_FRAMES // len(trackers)
    if FRAMES_PER_PARTICLE == 0:
        raise ValueError("TOTAL_FRAMES must be greater than the number of trackers (6).")
        
    frames_buffer = []
    global_frame_idx = 0
    
    print(f"Total Frames: {TOTAL_FRAMES} | Frames per Particle: {FRAMES_PER_PARTICLE}")
    
    for t_idx, tracker in enumerate(trackers):
        
        # --- ZOOM SEQUENCE FOR CURRENT PARTICLE ---
        
        initial_width = tracker.width 
        final_width = initial_width / ZOOM_FACTOR
        
        # Calculate the log-space width progression for this particle's segment
        widths = np.geomspace(initial_width, final_width, FRAMES_PER_PARTICLE)
        
        particle_label = f"M{t_idx+1}" if tracker.type == 'STRONG' else f"G{t_idx-2}"
        
        print(f"Particle {particle_label}: Initial Width {initial_width:.2f}, Final Width {final_width:.4f}")
        
        # Frame generation loop for this particle
        for i in range(FRAMES_PER_PARTICLE):
            
            # --- DYNAMIC PARAMETERS ---
            
            current_width = widths[i]
            # Use the pre-calculated theta for this global frame index
            pulse['theta'] = thetas[global_frame_idx] 
            
            # --- CRITICAL: CONTINUOUS TRACKING ---
            
            # Update the camera center to follow the peak as it moves/spirals
            center_m, center_l = tracker.update_position(pulse, current_width)
            
            # --- RENDER ---
            
            frame = render_zoom_frame(
                center_m, 
                center_l, 
                current_width, 
                initial_width, 
                particle_label, 
                tracker.color
            )
            frames_buffer.append(frame)
            
            global_frame_idx += 1
            
            if global_frame_idx % 20 == 0:
                print(f"Frame {global_frame_idx}/{TOTAL_FRAMES} | Tracking {particle_label} (Zoom x{initial_width/current_width:.1f})")

        # Add a few static frames at the end to hold the final view
        for _ in range(3):
            pulse['theta'] = thetas[global_frame_idx - 1] # Freeze theta at the last value
            frame = render_zoom_frame(
                center_m, center_l, final_width, initial_width, particle_label, tracker.color
            )
            frames_buffer.append(frame)

    
    # 4. Save the GIF
    print(f"Saving {OUTPUT_FILENAME} with {len(frames_buffer)} frames...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=70, loop=0)
    
    print("✅ DYNAMIC FRACTAL ZOOM SEQUENCE COMPLETE. Look for spiraling/circling motion as the field rotates.")


if __name__ == "__main__":
    run_dynamic_fractal_zoom()