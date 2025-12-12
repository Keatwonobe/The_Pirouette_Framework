import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw

# =========================================================
#  PIROUETTE FRAMEWORK: DEEP SPACE INTERCEPTOR (V-CLAMP)
# =========================================================

# --- MISSION PROFILE ---
OUTPUT_FILENAME = "deep_space_interceptor.gif"
TOTAL_FRAMES = 200
START_WIDTH = 12.0
MIN_WIDTH = 0.05
BASE_ZOOM = 0.96          # Aggressive zoom in
PANIC_ZOOM = 1.05         # Pull back if unstable

# --- CAMERA DYNAMICS ---
AZIMUTH_START = 0.0       # Top down
AZIMUTH_END = 1.3         # Looking up (almost horizon)
SEARCH_WINDOW_RATIO = 0.3 # Only look for target in center 30% of screen (prevents jumping to ghosts)

# --- PHYSICS KERNEL ---
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

# =========================================================
#  NUMBA KERNEL: 3D PROJECTION INTERFERENCE
# =========================================================

@njit(parallel=True, fastmath=True)
def render_microscope_3d(center_m, center_l, width, res, pulse_theta, azimuth_phi):
    # Setup Grid
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    intensity_map = np.zeros((res, res), dtype=np.float64)
    
    # Precompute Trig for System Rotation (The Particle Spin)
    c_sys = np.cos(pulse_theta)
    s_sys = np.sin(pulse_theta)
    
    # Precompute Trig for Azimuth (The Camera Tilt)
    c_phi = np.cos(azimuth_phi)
    s_phi = np.sin(azimuth_phi)

    # Physics Constants
    k = (2 * np.pi) / 10.0
    
    for i in prange(res):
        l_screen = l_vals[i]
        for j in range(res):
            m_screen = m_vals[j]
            
            # 1. INVERSE AZIMUTH TRANSFORM
            # We map screen pixels BACK to the flat 2D plane to check distance
            # This effectively "tilts" the plane relative to the camera
            
            # Center relative coordinates
            dm = m_screen - center_m
            dl = l_screen - center_l
            
            # Rotate inputs by Azimuth to get "World" coordinates
            m_world = center_m + (dm * c_phi - dl * s_phi)
            l_world = center_l + (dm * s_phi + dl * c_phi)

            psi_real = 0.0
            psi_imag = 0.0
            
            # 2. SOURCE SUMMATION
            for q in range(3):
                # Rotate Sources (The spinning system)
                src_m = SRC_STRONG_M[q] * c_sys - SRC_STRONG_L[q] * s_sys
                src_l = SRC_STRONG_M[q] * s_sys + SRC_STRONG_L[q] * c_sys
                
                dx = m_world - src_m
                dy = l_world - src_l
                dist = np.sqrt(dx*dx + dy*dy)
                
                if dist < 1e-9: dist = 1e-9
                
                phase = k * dist
                amp = (SRC_AMP / dist)
                
                psi_real += amp * np.cos(phase)
                psi_imag += amp * np.sin(phase)
                
            intensity_map[i, j] = psi_real**2 + psi_imag**2
            
    return intensity_map

# =========================================================
#  INERTIAL TRACKING SYSTEM
# =========================================================

class InertialTracker:
    def __init__(self, start_pos):
        self.m, self.l = start_pos
        self.width = START_WIDTH
        
        # Polar Momentum
        self.angle = np.arctan2(self.l, self.m)
        self.radius = np.sqrt(self.m**2 + self.l**2)
        
        self.omega = 0.0      # Angular Velocity
        self.alpha = 0.0      # Angular Acceleration
        self.dr = 0.0         # Radial Velocity
        
        self.status = "INIT"
        self.confidence = 1.0

    def predict(self):
        """Moves the camera blindly based on previous physics."""
        # Update Angular Dynamics
        self.omega += self.alpha
        self.angle += self.omega
        
        # Dampen acceleration (friction)
        self.alpha *= 0.9
        
        # Update Radial Dynamics
        self.radius += self.dr
        
        # Convert back to Cartesian
        self.m = self.radius * np.cos(self.angle)
        self.l = self.radius * np.sin(self.angle)
        
    def correct(self, measured_m, measured_l, signal_strength):
        """Corrects the prediction with actual sensor data."""
        
        # Calculate discrepancies
        meas_angle = np.arctan2(measured_l, measured_m)
        meas_radius = np.sqrt(measured_m**2 + measured_l**2)
        
        # Handle angle wrapping
        diff_angle = meas_angle - self.angle
        if diff_angle > np.pi: diff_angle -= 2*np.pi
        if diff_angle < -np.pi: diff_angle += 2*np.pi
        
        # Update Momentum (Reaction)
        # We assume the "force" acting on the camera is the difference between prediction and reality
        instant_accel = diff_angle - self.omega
        self.alpha = (self.alpha * 0.5) + (instant_accel * 0.5) # Soften the jerk
        
        self.omega = diff_angle # Snap velocity
        self.dr = meas_radius - self.radius
        
        # Hard Lock Position
        self.m = measured_m
        self.l = measured_l
        
        # Re-calculate state
        self.angle = meas_angle
        self.radius = meas_radius
        self.confidence = 1.0

def find_peak_constrained(img, width, center_m, center_l, search_ratio):
    """
    Only looks for the peak within a small box in the center of the image.
    This prevents the tracker from getting distracted by distant shiny objects.
    """
    res = img.shape[0]
    mid = res // 2
    radius_px = int((res * search_ratio) / 2)
    
    # Extract sub-window
    y_min, y_max = max(0, mid-radius_px), min(res, mid+radius_px)
    x_min, x_max = max(0, mid-radius_px), min(res, mid+radius_px)
    
    sub_img = img[y_min:y_max, x_min:x_max]
    
    if sub_img.size == 0: return 0, center_m, center_l
    
    # Find local max
    local_max = np.max(sub_img)
    local_idx = np.unravel_index(np.argmax(sub_img), sub_img.shape)
    
    # Map back to global pixel coordinates
    global_y = y_min + local_idx[0]
    global_x = x_min + local_idx[1]
    
    # Map to World Coordinates
    pixel_l = (center_l - width/2) + global_y * (width / (res - 1))
    pixel_m = (center_m - width/2) + global_x * (width / (res - 1))
    
    return local_max, pixel_m, pixel_l

# =========================================================
#  MAIN LOOP
# =========================================================

def run_mission():
    print("--- 🔭 INITIATING DEEP SPACE SCAN ---")
    
    # Initial Targeting
    tracker = InertialTracker((0.1, -5.0)) # Rough hint
    
    # Initial Lock-on Loop (No Azimuth yet)
    print("Acquiring Lock...")
    for _ in range(10):
        scan = render_microscope_3d(tracker.m, tracker.l, tracker.width, 100, 0.0, 0.0)
        peak, pm, pl = find_peak_constrained(scan, tracker.width, tracker.m, tracker.l, 0.8)
        tracker.m, tracker.l = pm, pl
        tracker.angle = np.arctan2(pl, pm)
        tracker.radius = np.sqrt(pm**2 + pl**2)

    frames_buffer = []
    azimuths = np.linspace(AZIMUTH_START, AZIMUTH_END, TOTAL_FRAMES)
    
    for f in range(TOTAL_FRAMES):
        pulse_theta = 2 * np.pi * (f / 100) # System rotation
        current_phi = azimuths[f]           # Camera tilt (Looking UP)
        
        # 1. INERTIAL PREDICTION STEP
        # Before we even look, we guess where the particle will be based on physics.
        tracker.predict()
        
        # 2. SENSOR SCAN (Low Res for speed)
        sensor_res = 150
        scan_img = render_microscope_3d(tracker.m, tracker.l, tracker.width, sensor_res, pulse_theta, current_phi)
        
        # 3. CONSTRAINED SEARCH
        # We only accept peaks near our prediction.
        peak_val, peak_m, peak_l = find_peak_constrained(scan_img, tracker.width, tracker.m, tracker.l, SEARCH_WINDOW_RATIO)
        
        # 4. DECISION LOGIC
        # As we tilt (azimuth), peak intensity might drop naturally. We lower threshold dynamically?
        # Actually, let's keep threshold fixed but rely on coasting.
        
        lock_threshold = 0.002
        
        if peak_val > lock_threshold:
            # === SIGNAL FOUND ===
            # Calculate how far the sensor reading is from prediction
            error_dist = np.sqrt((peak_m - tracker.m)**2 + (peak_l - tracker.l)**2)
            relative_error = error_dist / tracker.width
            
            tracker.correct(peak_m, peak_l, peak_val)
            tracker.status = "LOCKED"
            hud_color = (0, 255, 100)
            
            # Zoom Logic: Dive if stable, Panic if jittery
            if relative_error < 0.05 and tracker.width > MIN_WIDTH:
                tracker.width *= BASE_ZOOM # Dive
            elif relative_error > 0.15:
                tracker.width *= PANIC_ZOOM # Pull back
                
        else:
            # === SIGNAL LOST (COASTING) ===
            # The particle is obscured or faint. Do NOT update position based on noise.
            # Trust the 'predict()' we ran in step 1.
            tracker.status = "INERTIAL (COAST)"
            tracker.confidence *= 0.95
            hud_color = (255, 100, 50)
            
            # Safety: slight zoom out when blind to increase capture area for re-acquisition
            tracker.width *= 1.01 

        # 5. HIGH QUALITY RENDER
        hq_res = 400
        # Use the (possibly updated) tracker position
        final_img = render_microscope_3d(tracker.m, tracker.l, tracker.width, hq_res, pulse_theta, current_phi)
        
        # Color Mapping
        norm = (final_img - final_img.min()) / (final_img.max() - final_img.min() + 1e-9)
        norm = np.power(norm, 0.45) # Gamma correction
        
        # Visual flair: Shift hue based on azimuth
        colormap = 'magma' if current_phi < 0.8 else 'inferno'
        rgb = (plt.get_cmap(colormap)(norm)[:, :, :3] * 255).astype(np.uint8)
        
        pil_img = Image.fromarray(np.flipud(rgb))
        draw = ImageDraw.Draw(pil_img)
        
        # 6. HUD
        draw.text((10, 10), f"SYS: {tracker.status}", fill=hud_color)
        draw.text((10, 25), f"AZIMUTH: {current_phi:.3f} rad", fill=(200, 200, 200))
        draw.text((10, 40), f"WIDTH: {tracker.width:.4f}", fill=(200, 200, 200))
        draw.text((10, 55), f"OMEGA: {tracker.omega:.4f}", fill=(200, 200, 200))
        
        # Draw reticle
        cx, cy = hq_res//2, hq_res//2
        r = 15
        draw.rectangle([cx-r, cy-r, cx+r, cy+r], outline=hud_color)
        
        frames_buffer.append(pil_img)
        
        if f % 20 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | {tracker.status} | W:{tracker.width:.3f} | Az:{current_phi:.2f}")

    print("Saving GIF...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("Done.")

if __name__ == "__main__":
    run_mission()