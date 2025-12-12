# Write the script content to a new file
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# =========================================================
#  PROTON ENGINE: "INFINITY GLIDE" PROTOCOL (ADAPTIVE ZOOM)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "infinity_glide_adaptive_zoom.gif"
TOTAL_FRAMES = 180        # Total frames 
MAX_ZOOM_LEVEL = 10000.0  # Total conceptual magnification 
THETA_START = 0.0
THETA_END = 2 * np.pi * 3 # 3 full rotations
BRIGHTNESS_BOOST = 0.5    # How much to boost the overall brightness (0.0 to 1.0)

# LAYOUT DIMENSIONS
ZOOM_SIZE = 450         
MAIN_H = ZOOM_SIZE      
TOTAL_W = ZOOM_SIZE

# PHYSICS (Unchanged from original)
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_WEAK_M = np.array([5.0, 5.0, -5.0]) 
SRC_WEAK_L = np.array([-5.0, 2.5, 2.5]) 

# TARGET HINTS 
INITIAL_HINT = (-10.0, 5.0) 

COLOR_GLIDE = (255, 150, 255) # New color for the dynamic track

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
    
    # Check if the image is all zero/constant (in which case argmax is arbitrary)
    if np.max(img) == np.min(img):
        # Return center if no meaningful peak is found
        return np.max(img), center_m, center_l
        
    # L (row index) corresponds to the y-axis, M (col index) to the x-axis
    pixel_l = (center_l - width/2) + idx[0] * (width / (res - 1))
    pixel_m = (center_m - width/2) + idx[1] * (width / (res - 1))
    return np.max(img), pixel_m, pixel_l

# --- TRACKER (Revised for Adaptive Zoom) ---

class InfinityTracker:
    def __init__(self, hint):
        self.anchor_m, self.anchor_l = hint 
        self.cam_m, self.cam_l = self.anchor_m, self.anchor_l 
        self.initial_width = 8.0 
        self.current_width = self.initial_width
        self.max_zoom = MAX_ZOOM_LEVEL
        self.label_idx = 0
        
        self.last_peak_offset = (0.0, 0.0) 
        self.cam_damp = 0.95 # Higher damp means smoother camera following

    def initial_lock(self, pulse):
        for _ in range(5):
            scan = render_microscope(self.anchor_m, self.anchor_l, self.initial_width, 80, pulse)
            peak, pm, pl = find_peak(scan, self.initial_width, self.anchor_m, self.anchor_l)
            self.anchor_m = pm
            self.anchor_l = pl
            self.cam_m, self.cam_l = pm, pl
        print(f"Initial Lock: M={self.anchor_m:.4f}, L={self.anchor_l:.4f}")

    def scan_for_target(self, pulse):
        
        m_offset, l_offset = self.last_peak_offset
        center_distance = np.sqrt(m_offset**2 + l_offset**2)
        
        # Check if the anchor has moved past the 'Jump Rail Radius' (15% of the camera width)
        jump_rail_radius = self.current_width * 0.15
        
        # We also need to be at a certain minimum zoom level before jumping
        min_zoom_factor = 2.0
        
        if center_distance > jump_rail_radius and (self.initial_width / self.current_width) > min_zoom_factor:
            
            # --- JUMP RAIL ACTIVATED ---
            
            # 1. Look in the wider vicinity for a new peak (The "quarkon")
            # Scan wide relative to the camera center
            scan_width = self.current_width * 5.0 
            big_scan = render_microscope(self.cam_m, self.cam_l, scan_width, ZOOM_SIZE, pulse)
            
            # 2. Mask out the old anchor to find the new target (simplified mask):
            res = ZOOM_SIZE
            anchor_m_world = self.cam_m + m_offset
            anchor_l_world = self.cam_l + l_offset
            
            # Calculate pixel position for masking
            px_m = int((anchor_m_world - (self.cam_m - scan_width/2)) / scan_width * res)
            px_l = int((anchor_l_world - (self.cam_l - scan_width/2)) / scan_width * res)
            
            # Ensure pixel coordinates are within bounds for slicing
            px_m = np.clip(px_m, 0, res - 1)
            px_l = np.clip(px_l, 0, res - 1)
            
            # Mask the anchor region (set to a low value, not zero, to preserve structure context)
            mask_size = 10 
            big_scan[max(0, px_l-mask_size):min(res, px_l+mask_size+1), 
                     max(0, px_m-mask_size):min(res, px_m+mask_size+1)] *= 0.1
                     
            target_peak, target_m, target_l = find_peak(big_scan, scan_width, self.cam_m, self.cam_l)
            
            # Check if the target is strong enough
            if target_peak > 0.05: # Minimal intensity threshold
                
                 # New target is the new anchor
                 self.anchor_m, self.anchor_l = target_m, target_l
                 # Snap camera to the new feature
                 self.cam_m, self.cam_l = target_m, target_l
                 
                 # Reset initial_width to the current width to start the new glide segment
                 self.initial_width = self.current_width 
                 
                 print(f"JUMP RAIL! New Anchor M={target_m:.4f}, L={target_l:.4f}. New Width: {self.current_width:.4f}")
                 self.label_idx += 1
                 return True
        return False
        
    def update_position_and_zoom(self, pulse):
        
        # --- 1. TRACKING ANCHOR (Peak Lock) ---
        scan_width = self.current_width * 1.5 
        scan = render_microscope(self.cam_m, self.cam_l, scan_width, 80, pulse)
        peak, pm, pl = find_peak(scan, scan_width, self.cam_m, self.cam_l)
        
        # Update Anchor position (The true target position)
        self.anchor_m = pm
        self.anchor_l = pl
        
        # --- 2. DAMPED CAMERA MOVEMENT ---
        # The camera follows the Anchor smoothly
        self.cam_m += (self.anchor_m - self.cam_m) * (1.0 - self.cam_damp)
        self.cam_l += (self.anchor_l - self.cam_l) * (1.0 - self.cam_damp)
        
        # Calculate the position of the detected peak relative to the *new* camera center
        m_offset = self.anchor_m - self.cam_m
        l_offset = self.anchor_l - self.cam_l
        self.last_peak_offset = (m_offset, l_offset)

        # --- 3. ADAPTIVE ZOOM (Distance-based) ---
        
        center_distance = np.sqrt(m_offset**2 + l_offset**2)
        
        # Normalized distance (0 at center, 1 near edge)
        # 30% of the screen radius is the effective edge for slowdown
        norm_half_width = self.current_width * 0.3 
        normalized_distance = center_distance / (norm_half_width + 1e-9) 
        normalized_distance = np.clip(normalized_distance, 0.0, 1.0)
        
        # Zoom damping factor: Zoom *slows down* as it approaches the edge
        # We use a squared function to make the slow-down dramatic near the edge
        zoom_speed_factor = (1.0 - normalized_distance)**2
        
        # Ensure minimum zoom rate to avoid stopping completely
        min_speed = 0.0005 
        base_speed = 0.005
        current_zoom_rate = min_speed + (base_speed * zoom_speed_factor)
        
        # Apply the zoom rate to shrink the current width
        self.current_width *= (1.0 - current_zoom_rate)
        
        # --- 4. JUMP RAIL CHECK ---
        self.scan_for_target(pulse)
        
        return self.cam_m, self.cam_l, self.current_width

# --- DYNAMIC ZOOM RENDERER (Updated for Brightness Boost) ---

def render_zoom_frame(center_m, center_l, current_width, initial_width, label_idx, color):
    
    # NOTE: 'pulse' is used as a global variable
    raw_map = render_microscope(center_m, center_l, current_width, ZOOM_SIZE, pulse)
    
    # 2. Normalization and Color Mapping 
    norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
    
    # Apply Power Correction (for contrast)
    norm_map = np.power(norm_map, 0.4) 
    
    # Substrate Brightness Boost: Lift the entire image base level
    norm_map = np.clip(norm_map + BRIGHTNESS_BOOST, 0, 1) 
    
    map_rgb = (plt.get_cmap('inferno')(norm_map)[:, :, :3] * 255).astype(np.uint8)
    
    # PIL Image preparation
    panel = Image.fromarray(np.flipud(map_rgb))
    d_map = ImageDraw.Draw(panel)
    
    # Add HUD overlay
    zoom_level = (initial_width / current_width)
    display_label = f"[Q{label_idx}] Zoom: x{zoom_level:.2f} | Width: {current_width:.4f} | Θ: {pulse['theta']:.3f} rad"
    
    d_map.rectangle([5, 5, 5 + len(display_label) * 8, 25], fill=(0, 0, 0, 100))
    d_map.text((10, 8), display_label, fill=color)
    
    return panel

# --- MAIN MISSION ---

def run_dynamic_fractal_zoom():
    print("--- 🔄 INITIATING INFINITY GLIDE PROTOCOL (ADAPTIVE) ---")
    
    global pulse 
    
    # 1. Setup Tracker 
    tracker = InfinityTracker(INITIAL_HINT)
    
    # 2. Pre-lock the initial position
    pulse = {'theta': THETA_START, 'amp_boost': 1.0}
    tracker.initial_lock(pulse)
        
    # 3. Generate the sequence of parameters (theta)
    thetas = np.linspace(THETA_START, THETA_END, TOTAL_FRAMES)
        
    frames_buffer = []
    
    print(f"Total Frames: {TOTAL_FRAMES} | Max Zoom per Segment: x{MAX_ZOOM_LEVEL}")
    
    for global_frame_idx in range(TOTAL_FRAMES):
        
        # --- DYNAMIC PARAMETERS ---
        pulse['theta'] = thetas[global_frame_idx] 
            
        # --- CRITICAL: CONTINUOUS TRACKING & ZOOM ---
        center_m, center_l, current_width = tracker.update_position_and_zoom(pulse)
            
        # --- RENDER ---
        frame = render_zoom_frame(
            center_m, 
            center_l, 
            current_width, 
            tracker.initial_width, 
            tracker.label_idx, 
            COLOR_GLIDE
        )
        frames_buffer.append(frame)
        
        if global_frame_idx % 30 == 0:
            zoom = tracker.initial_width / current_width
            print(f"Frame {global_frame_idx}/{TOTAL_FRAMES} | Tracking Q{tracker.label_idx} (Zoom x{zoom:.1f}) | Width {current_width:.4f}")

    
    # 4. Save the GIF
    print(f"Saving {OUTPUT_FILENAME} with {len(frames_buffer)} frames...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=60, loop=0)
    
    print("✅ INFINITY GLIDE SEQUENCE COMPLETE (ADAPTIVE).")


if __name__ == "__main__":
    run_dynamic_fractal_zoom()