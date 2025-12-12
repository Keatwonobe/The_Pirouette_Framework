import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# =========================================================
#  PROTON ENGINE: "INFINITY GLIDE" PROTOCOL
#  GOAL: Continuous, rail-jumping, adaptive-zoom tracking.
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "infinity_glide_quark_jump.gif"
TOTAL_FRAMES = 180        # Increased for longer sequence
MAX_ZOOM_LEVEL = 1000.0   # Total magnification for each track segment
THETA_START = 0.0
THETA_END = 2 * np.pi * 3 # 3 full rotations for a long, spiraling path

# LAYOUT DIMENSIONS
ZOOM_SIZE = 450
MAIN_H = ZOOM_SIZE
TOTAL_W = ZOOM_SIZE

# PHYSICS (Unchanged from original)
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_WEAK_M = np.array([5.0, 5.0, -5.0]) 
SRC_WEAK_L = np.array([-5.0, 2.5, 2.5]) 

# TARGET HINTS (Now starting with just one point, the rest are found dynamically)
INITIAL_HINT = (-10.0, 5.0) 

COLORS_STRONG = [(0, 255, 255), (255, 0, 255), (255, 255, 0)] 
COLOR_GLIDE = (255, 150, 255) # New color for the dynamic track

# --- MATH KERNEL (Unchanged) ---
# (render_microscope, find_peak functions are omitted for brevity, 
#  but they are identical to the original pi_gif_orbiter_quark_infinity_static_2.py)

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

# --- TRACKER (Re-implemented for infinity glide) ---

class InfinityTracker:
    def __init__(self, hint):
        # Anchor is the currently tracked point
        self.anchor_m, self.anchor_l = hint 
        # Camera always stays on the anchor until a jump
        self.cam_m, self.cam_l = self.anchor_m, self.anchor_l 
        self.initial_width = 8.0 # Starting width
        self.current_width = self.initial_width
        self.max_zoom = MAX_ZOOM_LEVEL
        self.zoom_level = 1.0
        self.segment_start_frame = 0
        self.segment_max_frames = TOTAL_FRAMES # Max frames for one segment
        self.label_idx = 0
        
    def initial_lock(self, pulse):
        # Scan and lock to the nearest peak
        for _ in range(5):
            scan = render_microscope(self.anchor_m, self.anchor_l, self.initial_width, 80, pulse)
            peak, pm, pl = find_peak(scan, self.initial_width, self.anchor_m, self.anchor_l)
            self.anchor_m = pm
            self.anchor_l = pl
            self.cam_m, self.cam_l = pm, pl # Set camera to the locked position
        print(f"Initial Lock: M={self.anchor_m:.4f}, L={self.anchor_l:.4f}")

    def scan_for_target(self, pulse):
        """ Scans a wider area for any other high-intensity peak. """
        scan_width = self.current_width * 3.0 # Look far away from the center
        
        # NOTE: A simple argmax will always find the current anchor.
        # To find a *different* peak, we'd need a multi-peak detection algorithm, 
        # or we render the whole frame and mask out the anchor area.
        # For simplicity, we'll implement a basic multi-peak check:

        big_scan = render_microscope(self.cam_m, self.cam_l, scan_width, ZOOM_SIZE, pulse)
        
        # 1. Find the current peak (Anchor)
        anchor_peak, anchor_m_scan, anchor_l_scan = find_peak(big_scan, scan_width, self.cam_m, self.cam_l)
        
        # 2. Mask the anchor region to look for the next-strongest peak
        res = ZOOM_SIZE
        # Convert anchor position to pixel coordinates
        px_m = int((anchor_m_scan - (self.cam_m - scan_width/2)) / scan_width * res)
        px_l = int((anchor_l_scan - (self.cam_l - scan_width/2)) / scan_width * res)
        # Create a local mask (e.g., 5x5 pixel block)
        mask_size = 5
        big_scan[max(0, px_l-mask_size):min(res, px_l+mask_size+1), 
                 max(0, px_m-mask_size):min(res, px_m+mask_size+1)] = 0.0
                 
        # 3. Find the next peak (Target)
        target_peak, target_m, target_l = find_peak(big_scan, scan_width, self.cam_m, self.cam_l)
        
        # Only jump if the target is strong enough (e.g., 20% of the anchor's intensity)
        if target_peak > anchor_peak * 0.2:
             # Make the target the new anchor
             self.anchor_m, self.anchor_l = target_m, target_l
             print(f"JUMP RAIL! New Anchor M={target_m:.4f}, L={target_l:.4f}")
             self.label_idx += 1
             return True
        return False
        
    def update_position_and_zoom(self, pulse, global_frame_idx):
        """
        1. Tracks the anchor.
        2. Adjusts zoom based on anchor's movement (distance from center).
        3. Checks for "jump rail" condition.
        """
        
        # --- 1. TRACKING ANCHOR (Peak Lock) ---
        
        # Scan window should be small (current_width) for high-precision lock on the anchor
        scan = render_microscope(self.cam_m, self.cam_l, self.current_width, 80, pulse)
        
        # Find the peak relative to the camera center
        peak, pm, pl = find_peak(scan, self.current_width, self.cam_m, self.cam_l)
        
        # Move the ANCHOR towards the detected peak (Damped for stability)
        damp = 0.8 
        self.anchor_m += (pm - self.anchor_m) * damp
        self.anchor_l += (pl - self.anchor_l) * damp
        
        # Move the CAMERA to the Anchor's position
        self.cam_m, self.cam_l = self.anchor_m, self.anchor_l
        
        # --- 2. DYNAMIC ZOOM (The Glide) ---
        
        # Calculate distance of the Anchor from the camera center (which is self.cam_m, self.cam_l)
        # NOTE: Since cam_m/l is set to anchor_m/l, this distance is close to zero.
        # This dynamic zoom will not work as intended with the current setup.
        # Let's change the logic: We zoom slowly and check for the JUMP.
        
        # Simple continuous log-zoom over the maximum intended frames per segment
        t = global_frame_idx - self.segment_start_frame
        
        # Calculate the intended final width based on the total frames and max zoom
        # We will use a geometric progression for the width
        total_segment_frames = self.segment_max_frames // 3 # Divide the total frames into 3 long segments
        if total_segment_frames < 1: total_segment_frames = 1
        
        log_start = np.log(self.initial_width)
        log_end = np.log(self.initial_width / MAX_ZOOM_LEVEL)
        
        # Calculate the current log-width
        if t < total_segment_frames:
            current_log_width = log_start + (log_end - log_start) * (t / total_segment_frames)
            self.current_width = np.exp(current_log_width)
        else:
            # Freeze at max zoom
            self.current_width = self.initial_width / MAX_ZOOM_LEVEL

        # --- 3. JUMP RAIL CONDITION ---
        
        # Jump if we are at max zoom for this segment and have moved to another location
        if t >= total_segment_frames:
            if self.scan_for_target(pulse):
                # Reset zoom parameters for the new anchor
                self.initial_width = self.current_width 
                self.segment_start_frame = global_frame_idx

        return self.cam_m, self.cam_l, self.current_width

# --- DYNAMIC ZOOM RENDERER (Unchanged, but now using the InfinityTracker) ---

def render_zoom_frame(center_m, center_l, current_width, initial_width, label_idx, color):
    
    # NOTE: 'pulse' is used as a global variable
    raw_map = render_microscope(center_m, center_l, current_width, ZOOM_SIZE, pulse)
    
    # Normalization and Color Mapping 
    norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
    norm_map = np.power(norm_map, 0.4) 
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
    print("--- 🔄 INITIATING INFINITY GLIDE PROTOCOL ---")
    
    global pulse 
    
    # 1. Setup Tracker (Only one needed for the continuous glide)
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
        center_m, center_l, current_width = tracker.update_position_and_zoom(pulse, global_frame_idx)
            
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
            print(f"Frame {global_frame_idx}/{TOTAL_FRAMES} | Tracking Q{tracker.label_idx} (Zoom x{zoom:.1f})")

    
    # 4. Save the GIF
    print(f"Saving {OUTPUT_FILENAME} with {len(frames_buffer)} frames...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=60, loop=0)
    
    print("✅ INFINITY GLIDE SEQUENCE COMPLETE. Look for the 'rail-jump' to a new quarkon.")


if __name__ == "__main__":
    run_dynamic_fractal_zoom()