import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# =========================================================
#  PROTON ENGINE: "INFINITY GLIDE" PROTOCOL (AZIMUTH ENABLED)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "infinity_glide_azimuth.gif"
TOTAL_FRAMES = 450        
MAX_ZOOM_LEVEL = 10000.0  
THETA_START = 0.0
THETA_END = 2 * np.pi * 3
BRIGHTNESS_BOOST = 0.5    

# LAYOUT DIMENSIONS
ZOOM_SIZE = 450         
MAIN_H = ZOOM_SIZE      
TOTAL_W = ZOOM_SIZE

# PHYSICS (Unchanged)
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_WEAK_M = np.array([5.0, 5.0, -5.0]) 
SRC_WEAK_L = np.array([-5.0, 2.5, 2.5]) 

INITIAL_HINT = (-10.0, 5.0) 

COLOR_GLIDE = (255, 150, 255)

# --- MATH KERNEL (VECTORIZED) ---

# UPDATED to accept azimuth_phi
def render_microscope(center_m, center_l, width, res, pulse, azimuth_phi):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    M, L = np.meshgrid(m_vals, l_vals)
    
    # NEW: Apply Azimuth (Perspective Tilt)
    M_prime = M - center_m
    L_prime = L - center_l
    
    c_phi, s_phi = np.cos(azimuth_phi), np.sin(azimuth_phi)
    
    # Rotate (M', L') by phi (2D rotation matrix)
    M_rot = M_prime * c_phi - L_prime * s_phi
    L_rot = M_prime * s_phi + L_prime * c_phi
    
    # Translate back to the true world position for source calculation
    M_final = M_rot + center_m
    L_final = L_rot + center_l
    
    psi_real = np.zeros((res, res), dtype=np.float64)
    psi_imag = np.zeros((res, res), dtype=np.float64)
    
    theta = pulse['theta']
    c, s = np.cos(theta), np.sin(theta)
    
    # 1. STRONG SOURCES
    for i in range(3):
        sm = SRC_STRONG_M[i]*c - SRC_STRONG_L[i]*s
        sl = SRC_STRONG_M[i]*s + SRC_STRONG_L[i]*c
        
        # Use M_final and L_final for distance calculation
        dx = M_final - sm
        dy = L_final - sl
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
        
        # Use M_final and L_final for distance calculation
        dx = M_final - sm
        dy = L_final - sl
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
    
    if np.max(img) == np.min(img):
        return np.max(img), center_m, center_l
        
    pixel_l = (center_l - width/2) + idx[0] * (width / (res - 1))
    pixel_m = (center_m - width/2) + idx[1] * (width / (res - 1))
    return np.max(img), pixel_m, pixel_l

# --- TRACKER (Azimuth Enabled) ---

class InfinityTracker:
    def __init__(self, hint):
        self.anchor_m, self.anchor_l = hint 
        self.cam_m, self.cam_l = self.anchor_m, self.anchor_l 
        self.initial_width = 8.0 
        self.current_width = self.initial_width
        self.label_idx = 0
        self.azimuth_phi = 0.0 # New Azimuth Angle (Radians)
        self.last_peak_offset = (0.0, 0.0) 
        self.cam_damp = 0.9 
        self.constant_zoom_rate = 0.010 
        self.azimuth_hunt_period = 20 # Hunt for best azimuth every N frames

    def initial_lock(self, pulse):
        for _ in range(5):
            # Pass 0.0 for initial azimuth
            scan = render_microscope(self.anchor_m, self.anchor_l, self.initial_width, 80, pulse, 0.0)
            peak, pm, pl = find_peak(scan, self.initial_width, self.anchor_m, self.anchor_l)
            self.anchor_m = pm
            self.anchor_l = pl
            self.cam_m, self.cam_l = pm, pl
        print(f"Initial Lock: M={self.anchor_m:.4f}, L={self.anchor_l:.4f}")

    def hunt_azimuth(self, pulse):
        """ Scans nearby phi angles to maximize peak intensity. """
        
        # Sample angles: current phi, +0.1 rad, -0.1 rad
        angles = [self.azimuth_phi, self.azimuth_phi + 0.1, self.azimuth_phi - 0.1]
        best_peak = -1.0
        best_phi = self.azimuth_phi
        
        # We only need a rough, local scan, so a small res is fine
        scan_res = 40 
        
        for phi in angles:
            scan = render_microscope(self.cam_m, self.cam_l, self.current_width, scan_res, pulse, phi)
            
            # Use the *variance* of the map intensity as a proxy for "visible structure/texture"
            # Alternatively, use the peak intensity as a proxy for alignment
            current_peak = np.max(scan)
            
            if current_peak > best_peak:
                best_peak = current_peak
                best_phi = phi
        
        # Apply slight damping to prevent jittering 
        damp = 0.2
        self.azimuth_phi += (best_phi - self.azimuth_phi) * damp
        
        print(f"AZIMUTH HUNT: New φ={self.azimuth_phi:.3f} rad (Peak: {best_peak:.2f})")

    def scan_for_target(self, pulse):
        
        m_offset, l_offset = self.last_peak_offset
        center_distance = np.sqrt(m_offset**2 + l_offset**2)
        
        jump_rail_radius = self.current_width * 0.15
        min_zoom_factor = 1.5 
        
        if center_distance > jump_rail_radius and (self.initial_width / self.current_width) > min_zoom_factor:
            
            # --- JUMP RAIL ACTIVATED ---
            
            # Pass current azimuth to rendering
            scan_width = self.current_width * 5.0 
            big_scan = render_microscope(self.cam_m, self.cam_l, scan_width, ZOOM_SIZE, pulse, self.azimuth_phi)
            
            res = ZOOM_SIZE
            anchor_m_world = self.cam_m + m_offset
            anchor_l_world = self.cam_l + l_offset
            
            px_m = int((anchor_m_world - (self.cam_m - scan_width/2)) / scan_width * res)
            px_l = int((anchor_l_world - (self.cam_l - scan_width/2)) / scan_width * res)
            
            px_m = np.clip(px_m, 0, res - 1)
            px_l = np.clip(px_l, 0, res - 1)
            
            mask_size = 10 
            big_scan[max(0, px_l-mask_size):min(res, px_l+mask_size+1), 
                     max(0, px_m-mask_size):min(res, px_m+mask_size+1)] *= 0.1
                     
            target_peak, target_m, target_l = find_peak(big_scan, scan_width, self.cam_m, self.cam_l)
            
            if target_peak > 0.05: 
                
                 self.anchor_m, self.anchor_l = target_m, target_l
                 self.cam_m, self.cam_l = target_m, target_l
                 self.initial_width = self.current_width 
                 
                 print(f"JUMP RAIL! New Anchor M={target_m:.4f}, L={target_l:.4f}. New Width: {self.current_width:.4f}")
                 self.label_idx += 1
                 return True
        return False
        
    def update_position_and_zoom(self, pulse, global_frame_idx):
        
        # --- 0. AZIMUTH HUNT ---
        if global_frame_idx % self.azimuth_hunt_period == 0:
            self.hunt_azimuth(pulse)
            
        # --- 1. TRACKING ANCHOR (Peak Lock) ---
        scan_width = self.current_width * 1.5 
        # Pass current azimuth to rendering
        scan = render_microscope(self.cam_m, self.cam_l, scan_width, 80, pulse, self.azimuth_phi)
        peak, pm, pl = find_peak(scan, scan_width, self.cam_m, self.cam_l)
        
        self.anchor_m = pm
        self.anchor_l = pl
        
        # --- 2. DAMPED CAMERA MOVEMENT ---
        self.cam_m += (self.anchor_m - self.cam_m) * (1.0 - self.cam_damp)
        self.cam_l += (self.anchor_l - self.cam_l) * (1.0 - self.cam_damp)
        
        m_offset = self.anchor_m - self.cam_m
        l_offset = self.anchor_l - self.cam_l
        self.last_peak_offset = (m_offset, l_offset)

        # --- 3. CONSTANT FAST ZOOM ---
        self.current_width *= (1.0 - self.constant_zoom_rate)
        
        # --- 4. JUMP RAIL CHECK ---
        self.scan_for_target(pulse)
        
        return self.cam_m, self.cam_l, self.current_width

# --- DYNAMIC ZOOM RENDERER (Updated for Azimuth display) ---

def render_zoom_frame(center_m, center_l, current_width, initial_width, label_idx, color, azimuth_phi):
    
    # Pass azimuth_phi to the renderer
    raw_map = render_microscope(center_m, center_l, current_width, ZOOM_SIZE, pulse, azimuth_phi)
    
    # Normalization and Color Mapping (same brightness boost)
    norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
    norm_map = np.power(norm_map, 0.4) 
    norm_map = np.clip(norm_map + BRIGHTNESS_BOOST, 0, 1) 
    map_rgb = (plt.get_cmap('inferno')(norm_map)[:, :, :3] * 255).astype(np.uint8)
    
    panel = Image.fromarray(np.flipud(map_rgb))
    d_map = ImageDraw.Draw(panel)
    
    zoom_level = (initial_width / current_width)
    
    # UPDATED HUD to show Azimuth
    display_label = f"[Q{label_idx}] Zoom: x{zoom_level:.2f} | Width: {current_width:.4f} | Θ: {pulse['theta']:.3f} | φ: {azimuth_phi:.3f} rad"
    
    d_map.rectangle([5, 5, 5 + len(display_label) * 8, 25], fill=(0, 0, 0, 100))
    d_map.text((10, 8), display_label, fill=color)
    
    return panel

# --- MAIN MISSION ---

def run_dynamic_fractal_zoom():
    print("--- 🔄 INITIATING AZIMUTHAL INFINITY GLIDE PROTOCOL ---")
    
    global pulse 
    
    tracker = InfinityTracker(INITIAL_HINT)
    
    pulse = {'theta': THETA_START, 'amp_boost': 1.0}
    tracker.initial_lock(pulse)
        
    thetas = np.linspace(THETA_START, THETA_END, TOTAL_FRAMES)
        
    frames_buffer = []
    
    print(f"Total Frames: {TOTAL_FRAMES} | Azimuth Hunting Period: {tracker.azimuth_hunt_period}")
    
    for global_frame_idx in range(TOTAL_FRAMES):
        
        pulse['theta'] = thetas[global_frame_idx] 
            
        center_m, center_l, current_width = tracker.update_position_and_zoom(pulse, global_frame_idx)
            
        frame = render_zoom_frame(
            center_m, 
            center_l, 
            current_width, 
            tracker.initial_width, 
            tracker.label_idx, 
            COLOR_GLIDE,
            tracker.azimuth_phi # Pass azimuth to renderer
        )
        frames_buffer.append(frame)
        
        if global_frame_idx % 30 == 0:
            zoom = tracker.initial_width / current_width
            print(f"Frame {global_frame_idx}/{TOTAL_FRAMES} | Tracking Q{tracker.label_idx} (Zoom x{zoom:.1f}) | φ {tracker.azimuth_phi:.3f} rad")

    
    print(f"Saving {OUTPUT_FILENAME} with {len(frames_buffer)} frames...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=60, loop=0)
    
    print("✅ AZIMUTHAL INFINITY GLIDE SEQUENCE COMPLETE.")


if __name__ == "__main__":
    run_dynamic_fractal_zoom()