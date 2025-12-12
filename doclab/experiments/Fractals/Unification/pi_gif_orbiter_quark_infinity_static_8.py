import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw

# =========================================================
#  PIROUETTE: TRIFURCATION STALKER (RESONANCE CLAMP)
# =========================================================

# --- MISSION PARAMETERS ---
OUTPUT_FILENAME = "trifurcation_stalker.gif"
TOTAL_FRAMES = 300
START_WIDTH = 12.0
END_WIDTH = 0.05
ZOOM_RATE = 0.98  # Constant dive speed

# --- PHYSICS KERNEL ---
# The classic "3s" generator configuration
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

# --- CLAMP SETTINGS ---
CLAMP_RADIUS_RATIO = 0.15  # Only look at the immediate 15% neighborhood of the target
INERTIA_DAMPING = 0.9      # How much velocity is preserved (0.9 = slippery)

# =========================================================
#  NUMBA RENDERER (3D PROJECTION)
# =========================================================

@njit(parallel=True, fastmath=True)
def render_field(center_m, center_l, width, res, pulse_theta, azimuth_phi):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    intensity_map = np.zeros((res, res), dtype=np.float64)
    
    c_sys, s_sys = np.cos(pulse_theta), np.sin(pulse_theta)
    c_phi, s_phi = np.cos(azimuth_phi), np.sin(azimuth_phi)
    k = (2 * np.pi) / 10.0
    
    for i in prange(res):
        l_screen = l_vals[i]
        for j in range(res):
            m_screen = m_vals[j]
            
            # Inverse Azimuth Transform
            dm = m_screen - center_m
            dl = l_screen - center_l
            m_world = center_m + (dm * c_phi - dl * s_phi)
            l_world = center_l + (dm * s_phi + dl * c_phi)

            psi_real = 0.0
            psi_imag = 0.0
            
            for q in range(3):
                # Rotate Source System
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
#  THE RESONANCE CLAMP TRACKER
# =========================================================

class ResonanceClamp:
    def __init__(self, start_pos, start_width):
        self.m, self.l = start_pos
        self.width = start_width
        
        # Velocity Vectors
        self.vm = 0.0
        self.vl = 0.0
        
        # State
        self.locked_mass = 0.0
        self.resonance_integrity = 1.0 # 1.0 = Pure Point, <0.5 = Diffuse Cloud

    def predict(self):
        """Apply Inertial Momentum"""
        self.m += self.vm
        self.l += self.vl

    def update(self, img, center_m, center_l, current_width):
        """
        Finds the Center of Mass, BUT restricts the search to a small
        radius around the PREDICTED location. This ignores the split-off particles.
        """
        res = img.shape[0]
        
        # 1. Define the Clamp Window (Pixel Coordinates)
        # We assume the prediction puts the target near the center of the image
        # because the camera moved there.
        mid = res // 2
        radius = int(res * CLAMP_RADIUS_RATIO)
        
        y_min, y_max = max(0, mid-radius), min(res, mid+radius)
        x_min, x_max = max(0, mid-radius), min(res, mid+radius)
        
        # Extract Local Window
        window = img[y_min:y_max, x_min:x_max]
        
        # If window is empty/black, coast on inertia
        if window.size == 0 or np.max(window) < 1e-6:
            self.resonance_integrity *= 0.9
            return # Keep existing velocity
            
        # 2. Local Center of Mass Calculation
        norm_window = (window - np.min(window)) / (np.max(window) - np.min(window) + 1e-9)
        
        # Threshold to remove background noise within the window
        mask = norm_window > 0.4
        if np.sum(mask) == 0:
            self.resonance_integrity *= 0.9
            return

        Y, X = np.indices(window.shape)
        masses = norm_window[mask]
        y_coords = Y[mask]
        x_coords = X[mask]
        
        total_mass = np.sum(masses)
        local_cy = np.sum(y_coords * masses) / total_mass
        local_cx = np.sum(x_coords * masses) / total_mass
        
        # Map Local Window -> Global Pixel -> World Coordinate
        global_y = y_min + local_cy
        global_x = x_min + local_cx
        
        pixel_scale = current_width / (res - 1)
        measured_l = (center_l - current_width/2) + global_y * pixel_scale
        measured_m = (center_m - current_width/2) + global_x * pixel_scale
        
        # 3. Update Physics (Damped Spring)
        # Calculate the "pull" of the resonance
        dm = measured_m - self.m
        dl = measured_l - self.l
        
        # Update Velocity (Reaction)
        self.vm = (self.vm * INERTIA_DAMPING) + (dm * 0.2)
        self.vl = (self.vl * INERTIA_DAMPING) + (dl * 0.2)
        
        # Update Position
        self.m = measured_m
        self.l = measured_l
        
        # Update Stats
        self.locked_mass = total_mass
        self.resonance_integrity = 1.0 # Reset integrity on good lock

# =========================================================
#  MAIN EXECUTION
# =========================================================

def run_stalker():
    print("--- 🎯 TRIFURCATION STALKER ENGAGED ---")
    
    # 1. Initialization
    # Start at the standard orbital hint
    tracker = ResonanceClamp((0.0, -5.0), START_WIDTH)
    
    # Pre-Lock Loop (Stabilize on the main attractor)
    print("Stabilizing clamp...")
    for _ in range(15):
        scan = render_field(tracker.m, tracker.l, tracker.width, 100, 0.0, 0.0)
        tracker.update(scan, tracker.m, tracker.l, tracker.width)

    frames_buffer = []
    
    # We will tilt azimuth up to 1.3 rads to see the horizon
    azimuths = np.linspace(0.0, 1.3, TOTAL_FRAMES)
    
    for f in range(TOTAL_FRAMES):
        
        # 1. Physics Update
        pulse_theta = 2 * np.pi * (f / 100) # Fast spin to force interference
        current_azimuth = azimuths[f]
        
        # 2. Predict (Inertial Fly-wheel)
        tracker.predict()
        
        # 3. Zoom Step
        tracker.width *= ZOOM_RATE
        
        # 4. Sensor Scan & Correction
        # We render at current camera pos
        scan_res = 120
        scan_img = render_field(tracker.m, tracker.l, tracker.width, scan_res, pulse_theta, current_azimuth)
        
        # The tracker looks at the scan and corrects its position
        tracker.update(scan_img, tracker.m, tracker.l, tracker.width)
        
        # 5. High Quality Render
        hq_res = 500
        # Use the updated tracker position for the final shot
        final_img = render_field(tracker.m, tracker.l, tracker.width, hq_res, pulse_theta, current_azimuth)
        
        # 6. Post-Processing
        norm = (final_img - final_img.min()) / (final_img.max() - final_img.min() + 1e-9)
        norm = np.power(norm, 0.45) # Gamma
        
        # "Electric" coloring
        rgb = (plt.get_cmap('gist_ncar')(norm)[:, :, :3] * 255).astype(np.uint8)
        panel = Image.fromarray(np.flipud(rgb))
        draw = ImageDraw.Draw(panel)
        
        # HUD
        hud_color = (0, 255, 255)
        draw.text((10, 10), f"TRACKING: RESONANCE ALPHA", fill=hud_color)
        draw.text((10, 25), f"WIDTH: {tracker.width:.6f}", fill=hud_color)
        draw.text((10, 40), f"AZIMUTH: {current_azimuth:.3f}", fill=hud_color)
        
        # Draw the Clamp Box (Visualizing the constrained search area)
        cx, cy = hq_res//2, hq_res//2
        clamp_px = int(hq_res * CLAMP_RADIUS_RATIO)
        draw.rectangle([cx-clamp_px, cy-clamp_px, cx+clamp_px, cy+clamp_px], outline=(50, 50, 50))
        draw.line((cx-5, cy, cx+5, cy), fill=hud_color)
        draw.line((cx, cy-5, cx, cy+5), fill=hud_color)

        frames_buffer.append(panel)
        
        if f % 20 == 0:
            print(f"Frame {f} | W:{tracker.width:.5f} | Pos: ({tracker.m:.2f}, {tracker.l:.2f})")

    print("Saving Stalker Log...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=40, loop=0)
    print("✅ MISSION COMPLETE.")

if __name__ == "__main__":
    run_stalker()