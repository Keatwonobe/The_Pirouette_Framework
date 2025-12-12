import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw

# =========================================================
#  PIROUETTE: ACTIVE BRAKE INTERCEPTOR
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "active_brake_lock.gif"
TOTAL_FRAMES = 350

# DYNAMICS
BASE_ZOOM_RATE = 0.985    # Default Dive Speed
BASE_AZIM_SPEED = 0.005   # How fast we tilt up per frame
MAX_AZIMUTH = 1.4         # Horizon limit

# THE "CAGE"
BOX_RATIO = 0.15          # 15% of screen is the "Safe Zone"

# PHYSICS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

# =========================================================
#  NUMBA KERNEL (Unchanged)
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
#  ADAPTIVE BRAKING TRACKER
# =========================================================

class BrakeTracker:
    def __init__(self, start_pos, start_width):
        self.m, self.l = start_pos
        self.width = start_width
        self.azimuth = 0.0
        
        # State Monitors
        self.slip_factor = 0.0 # 0.0 = Centered, 1.0 = Edge of Box
        self.status = "GREEN"

    def scan_and_lock(self, pulse_theta):
        """
        1. Render small window.
        2. Find Peak.
        3. Calculate Stress/Slip.
        4. Return Corrected Position + Suggested Dynamics
        """
        
        # A. RENDER SCAN WINDOW
        res = 120
        scan = render_field(self.m, self.l, self.width, res, pulse_theta, self.azimuth)
        
        # B. CONSTRAINED SEARCH (The Box)
        mid = res // 2
        pixel_radius = int(res * BOX_RATIO)
        
        # Extract the box
        y_min, y_max = max(0, mid-pixel_radius), min(res, mid+pixel_radius)
        x_min, x_max = max(0, mid-pixel_radius), min(res, mid+pixel_radius)
        
        sub_img = scan[y_min:y_max, x_min:x_max]
        
        # Panic Check
        if sub_img.size == 0 or np.max(sub_img) < 1e-6:
            self.status = "LOST"
            return 1.05, 0.0 # Panic Zoom OUT, Stop Azimuth

        # C. FIND PEAK
        local_idx = np.unravel_index(np.argmax(sub_img), sub_img.shape)
        
        # Map to Global Pixels
        global_y = y_min + local_idx[0]
        global_x = x_min + local_idx[1]
        
        # Map to World Coords
        pixel_scale = self.width / (res - 1)
        target_l = (self.l - self.width/2) + global_y * pixel_scale
        target_m = (self.m - self.width/2) + global_x * pixel_scale
        
        # D. CALCULATE SLIP (ERROR)
        # Distance from CENTER of screen (self.m, self.l) to TARGET (target_m, target_l)
        dist = np.sqrt((target_m - self.m)**2 + (target_l - self.l)**2)
        
        # Max allowed distance is roughly (width * BOX_RATIO)
        max_dist = (self.width * BOX_RATIO)
        
        # Slip Factor: 0.0 = Bullseye, 1.0 = Hitting the Cage Wall
        self.slip_factor = dist / max_dist
        self.slip_factor = np.clip(self.slip_factor, 0.0, 1.5)
        
        # E. INSTANT CORRECTION
        # Snap camera to target immediately
        self.m = target_m
        self.l = target_l
        
        # F. DYNAMIC RESPONSE CALCULATION
        
        # Zoom Logic:
        # If Slip < 0.5 -> Zoom Normal (0.98)
        # If Slip > 0.8 -> Hold Zoom (1.0)
        # If Slip > 1.0 -> Back Off (1.02)
        eff_zoom = BASE_ZOOM_RATE + (self.slip_factor * 0.05)
        if eff_zoom > 1.02: eff_zoom = 1.02
        
        # Azimuth Logic:
        # If Slip < 0.3 -> Full Tilt
        # If Slip > 0.6 -> STOP TILT
        eff_azimuth_delta = BASE_AZIM_SPEED * (1.0 - (self.slip_factor * 1.5))
        if eff_azimuth_delta < 0: eff_azimuth_delta = 0
        
        # Update Status String
        if self.slip_factor < 0.3: self.status = "LOCKED"
        elif self.slip_factor < 0.8: self.status = "WARN"
        else: self.status = "CRITICAL"
        
        return eff_zoom, eff_azimuth_delta

# =========================================================
#  MAIN MISSION
# =========================================================

def run_active_brake():
    print("--- 🚦 ACTIVE BRAKE SYSTEM ENGAGED ---")
    
    # Init
    tracker = BrakeTracker((0.0, -5.0), 12.0)
    
    # Stabilize
    for _ in range(10):
        tracker.scan_and_lock(0.0)

    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        
        theta = 2 * np.pi * (f / 100) # System spin
        
        # 1. RUN TRACKER LOGIC
        # This updates the camera position internally and returns suggested speeds
        rec_zoom, rec_azim_delta = tracker.scan_and_lock(theta)
        
        # 2. APPLY DYNAMICS
        tracker.width *= rec_zoom
        tracker.azimuth += rec_azim_delta
        
        # Cap Azimuth
        if tracker.azimuth > MAX_AZIMUTH: tracker.azimuth = MAX_AZIMUTH
        
        # 3. HIGH QUALITY RENDER
        hq_res = 500
        final_img = render_field(tracker.m, tracker.l, tracker.width, hq_res, theta, tracker.azimuth)
        
        # 4. HUD
        norm = (final_img - final_img.min()) / (final_img.max() - final_img.min() + 1e-9)
        norm = np.power(norm, 0.5)
        
        # Color based on Status
        if tracker.status == "LOCKED": cmap = 'viridis'
        elif tracker.status == "WARN": cmap = 'plasma'
        else: cmap = 'inferno' # RED/ORANGE for danger
        
        rgb = (plt.get_cmap(cmap)(norm)[:, :, :3] * 255).astype(np.uint8)
        panel = Image.fromarray(np.flipud(rgb))
        draw = ImageDraw.Draw(panel)
        
        # Draw Box (The Cage)
        cx, cy = hq_res//2, hq_res//2
        r = int(hq_res * BOX_RATIO)
        
        # Box Color changes with stress
        box_color = (0, 255, 0)
        if tracker.status == "WARN": box_color = (255, 255, 0)
        if tracker.status == "CRITICAL": box_color = (255, 0, 0)
        
        draw.rectangle([cx-r, cy-r, cx+r, cy+r], outline=box_color, width=2)
        
        # Text Info
        draw.text((10, 10), f"SYS: {tracker.status}", fill=box_color)
        draw.text((10, 25), f"SLIP: {tracker.slip_factor*100:.1f}%", fill=box_color)
        draw.text((10, 40), f"AZIMUTH: {tracker.azimuth:.3f} (Δ {rec_azim_delta:.4f})", fill=(200, 200, 200))
        draw.text((10, 55), f"ZOOM: x{rec_zoom:.4f}", fill=(200, 200, 200))

        frames_buffer.append(panel)
        
        if f % 20 == 0:
            print(f"Frame {f} | {tracker.status} | Slip: {tracker.slip_factor:.2f} | Azim: {tracker.azimuth:.3f}")

    print("Saving Active Brake GIF...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=40, loop=0)
    print("✅ MISSION COMPLETE.")

if __name__ == "__main__":
    run_active_brake()