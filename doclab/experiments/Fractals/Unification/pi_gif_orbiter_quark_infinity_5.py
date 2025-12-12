import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time

# =========================================================
#  PROTON MICROSCOPE: AUTONOMOUS HUNTER-SEEKER (v5.0)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_probe_live_feed.gif"
TOTAL_FRAMES = 300       # How long to hunt
RADAR_RES = 500           # Resolution of the "bacterial eye" (Low res for speed)
RENDER_RES = 500         # Resolution of the final GIF frames
START_WIDTH = 21.0       # Starting zoom
ZOOM_SPEED = 0.985       # Multiplier per frame (0.985 = slow steady dive)
MOMENTUM_FACTOR = 0.85   # How much velocity is kept when target blinks (0.0 to 1.0)
LOCK_SMOOTHING = 0.1     # How quickly the camera snaps to new target (0.1 = smooth, 1.0 = instant)

# --- PHYSICS ENGINE ---

SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])
BREATHING_FREQ = 6.0 

@njit(parallel=True)
def render_microscope(center_m, center_l, width, res, src_m, src_l, src_amp):
    """
    Renders the interference pattern. 
    Used for both the low-res 'Radar' and the high-res 'Output'.
    """
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

# --- THE AUTONOMOUS PROBE ---

class AutoProbe:
    def __init__(self):
        self.cam_m = 0.0
        self.cam_l = 0.0
        self.vel_m = 0.0
        self.vel_l = 0.0
        self.current_width = START_WIDTH
        self.locked = False
        self.last_max_brightness = 0.0
        
    def scan_and_track(self, radar_img, width):
        """
        Analyzes the low-res radar image to update velocity and position.
        """
        # 1. Find the brightest pixel in the radar
        max_val = np.max(radar_img)
        idx = np.unravel_index(np.argmax(radar_img), radar_img.shape)
        
        # Radar resolution scaling
        y_idx, x_idx = idx
        
        # Convert pixel index to local offset relative to current camera
        # (0,0) in image is top-left, we want offset from center
        center_idx = RADAR_RES / 2.0
        scale = width / RADAR_RES
        
        offset_m = (x_idx - center_idx) * scale
        offset_l = (center_idx - y_idx) * scale # Flip Y for standard Cartesian
        
        # 2. DECISION LOGIC: Is this a real target or just noise?
        # If the frame is too dark, we assume the particle is "blinking" (destructive interference)
        # and we maintain our previous trajectory (Inertial Guidance)
        
        signal_strength = max_val
        is_signal_strong = True
        
        # Adaptive threshold: If signal drops significantly below recent max, it's a blink
        if self.last_max_brightness > 0 and signal_strength < (self.last_max_brightness * 0.3):
            is_signal_strong = False
            # print("  > Target lost (Blink). Engaging Inertial Dampeners.")
        
        self.last_max_brightness = max(self.last_max_brightness * 0.95, signal_strength) # Decay memory
        
        if is_signal_strong:
            # We see light! Chase it.
            # Calculate target world coordinates
            target_m = self.cam_m + offset_m
            target_l = self.cam_l + offset_l
            
            # Move towards target (Smoothing)
            # We don't jump straight there; we adjust velocity to steer towards it
            desired_m = target_m
            desired_l = target_l
            
            # Simple LERP for position (Proportional Controller)
            new_m = self.cam_m + (desired_m - self.cam_m) * LOCK_SMOOTHING
            new_l = self.cam_l + (desired_l - self.cam_l) * LOCK_SMOOTHING
            
            # Update Velocity (for when we lose lock later)
            self.vel_m = new_m - self.cam_m
            self.vel_l = new_l - self.cam_l
            
            self.cam_m = new_m
            self.cam_l = new_l
            self.locked = True
        else:
            # Blind flying - Apply Momentum
            self.cam_m += self.vel_m * MOMENTUM_FACTOR
            self.cam_l += self.vel_l * MOMENTUM_FACTOR
            self.vel_m *= MOMENTUM_FACTOR # Drag
            self.vel_l *= MOMENTUM_FACTOR
            self.locked = False
            
        return self.cam_m, self.cam_l, self.locked

# --- HUD GRAPHICS ---

def draw_hud(pil_img, probe, f):
    draw = ImageDraw.Draw(pil_img)
    w, h = pil_img.size
    
    # 1. Target Reticle (Center of Screen)
    # The camera attempts to center the target, so the reticle is always center
    cx, cy = w // 2, h // 2
    r = 40
    
    # Color depends on lock status
    color = (0, 255, 255) if probe.locked else (255, 50, 0) # Cyan if locked, Red if coasting
    
    # Draw "Brackets"
    len_line = 10
    gap = 10
    thk = 2
    
    # Top Left
    draw.line([(cx - r, cy - r + len_line), (cx - r, cy - r), (cx - r + len_line, cy - r)], fill=color, width=thk)
    # Top Right
    draw.line([(cx + r - len_line, cy - r), (cx + r, cy - r), (cx + r, cy - r + len_line)], fill=color, width=thk)
    # Bottom Left
    draw.line([(cx - r, cy + r - len_line), (cx - r, cy + r), (cx - r + len_line, cy + r)], fill=color, width=thk)
    # Bottom Right
    draw.line([(cx + r - len_line, cy + r), (cx + r, cy + r), (cx + r, cy + r - len_line)], fill=color, width=thk)
    
    # 2. Data Text
    status_text = "STATUS: TRACKING" if probe.locked else "STATUS: COASTING (NO SIGNAL)"
    zoom_text = f"ZOOM WIDTH: {probe.current_width:.4e}"
    coord_text = f"REL COORD: {probe.cam_m:.4f}, {probe.cam_l:.4f}"
    
    # Simple bitmap font usually built-in, or default
    try:
        # Load default font
        font = ImageFont.load_default()
    except:
        font = None

    draw.text((10, h - 50), status_text, fill=color, font=font)
    draw.text((10, h - 35), zoom_text, fill=(200, 200, 200), font=font)
    draw.text((10, h - 20), coord_text, fill=(200, 200, 200), font=font)

    return pil_img

# --- MAIN LOOP ---

def run_probe():
    probe = AutoProbe()
    frames_buffer = []
    
    print(f"🚀 Launching Autonomous Probe. Hunting for {TOTAL_FRAMES} frames...")
    
    for f in range(TOTAL_FRAMES):
        # 1. Physics Rotation
        sys_theta = 2 * np.pi * (f / 100) # Rotate slowly
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.1)

        # 2. RADAR SCAN (The "Bacterial Eye")
        # Render a tiny, cheap frame to see where the light is
        radar_scan = render_microscope(
            probe.cam_m, probe.cam_l, 
            probe.current_width, 
            RADAR_RES, 
            curr_src_m, curr_src_l, 
            pulse
        )
        
        # 3. UPDATE PROBE TRAJECTORY
        probe.scan_and_track(radar_scan, probe.current_width)
        
        # 4. RENDER HIGH-RES OUTPUT
        raw_img = render_microscope(
            probe.cam_m, probe.cam_l, 
            probe.current_width, 
            RENDER_RES, 
            curr_src_m, curr_src_l, 
            pulse
        )
        
        # 5. POST-PROCESS (Color & HUD)
        # Normalize
        v_min, v_max = raw_img.min(), raw_img.max()
        if v_max - v_min < 1e-9:
            norm = np.zeros_like(raw_img)
        else:
            norm = (raw_img - v_min) / (v_max - v_min)
        
        # Gamma
        norm = np.power(norm, 0.5)
        
        # Colormap
        cmap = plt.get_cmap('magma')
        rgba = cmap(norm)
        img_uint8 = (rgba[:, :, :3] * 255).astype(np.uint8)
        img_uint8 = np.flipud(img_uint8) # Fix orientation
        
        pil_img = Image.fromarray(img_uint8)
        
        # Apply HUD
        pil_img = draw_hud(pil_img, probe, f)
        
        frames_buffer.append(pil_img)
        
        # 6. ITERATE ZOOM
        probe.current_width *= ZOOM_SPEED
        
        if f % 10 == 0:
            lock_icon = "🔒" if probe.locked else "⚠️"
            print(f"Frame {f}/{TOTAL_FRAMES} | {lock_icon} | Zoom: {probe.current_width:.3e} | Pos: {probe.cam_m:.2f}, {probe.cam_l:.2f}")

    # SAVE
    print(f"Saving Mission Log to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=50,
        loop=0
    )
    print("✅ Mission Complete.")

if __name__ == "__main__":
    run_probe()