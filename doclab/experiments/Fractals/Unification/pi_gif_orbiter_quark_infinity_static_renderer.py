import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFilter
from collections import deque

# =========================================================
#  PIROUETTE: QUARKON POV (CINEMATIC FLIGHT)
# =========================================================

# --- MISSION CONFIG ---
OUTPUT_FILENAME = "quarkon_pov_flythrough.gif"
TOTAL_FRAMES = 400
RENDER_RES = 600        # Hi-Res output
FOV_WIDTH_START = 14.0  # Wider start for context

# FLIGHT DYNAMICS
DEFAULT_ZOOM = 0.990    # Slightly more relaxed to show the "walls"
MAX_AZIMUTH = 1.40      # Looking almost at the horizon (The Tunnel)
AZIMUTH_RAMP = 0.01     # Pitch up quickly
TETHER_STIFFNESS = 0.12 # Smooth, elastic handling

# PHYSICS KERNEL
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

# =========================================================
#  NUMBA KERNEL (3D PROJECTION)
# =========================================================

@njit(parallel=True, fastmath=True)
def render_cinematic_field(center_m, center_l, width, res, pulse_theta, azimuth_phi):
    half_w = width / 2.0
    # Create grid
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    intensity_map = np.zeros((res, res), dtype=np.float64)
    
    # Trig Pre-calc
    c_sys, s_sys = np.cos(pulse_theta), np.sin(pulse_theta)
    c_phi, s_phi = np.cos(azimuth_phi), np.sin(azimuth_phi)
    k = (2 * np.pi) / 10.0
    
    # We add a slight "Fog" distance fade for depth perception
    
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
            
            # Source Summation
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
            
            val = psi_real**2 + psi_imag**2
            intensity_map[i, j] = val
            
    return intensity_map

# =========================================================
#  FLIGHT COMPUTER (ELASTIC SOLVER)
# =========================================================

class FlightComputer:
    def __init__(self, start_m, start_l, start_width):
        self.m = start_m
        self.l = start_l
        self.width = start_width
        self.azimuth = 0.0
        
        # Flight Recorder
        self.history = deque(maxlen=15)
        self.g_force = 0.0 # Metric for drift/tension
        self.velocity_heading = 0.0
        self.active_window = 15

    def update(self, pulse_theta):
        
        # 1. RADAR SCAN (Low Res for locking)
        scan_res = 120
        scan = render_cinematic_field(self.m, self.l, self.width, scan_res, pulse_theta, self.azimuth)
        
        idx = np.unravel_index(np.argmax(scan), scan.shape)
        
        px_scale = self.width / (scan_res - 1)
        peak_l = (self.l - self.width/2) + idx[0] * px_scale
        peak_m = (self.m - self.width/2) + idx[1] * px_scale
        
        self.history.append((peak_m, peak_l))
        
        # 2. G-FORCE CALCULATION (Drift from Center)
        dist_off_center = np.sqrt((peak_m - self.m)**2 + (peak_l - self.l)**2)
        drift_ratio = dist_off_center / (self.width / 2)
        self.g_force = drift_ratio
        
        # 3. ADAPTIVE RESPONSE
        target_window = 3 if drift_ratio > 0.15 else 15
        
        if self.active_window > target_window: self.active_window -= 1
        elif self.active_window < target_window: self.active_window += 1
        
        # 4. TRAJECTORY SOLVER
        curr_history = list(self.history)[-self.active_window:]
        if len(curr_history) < 2:
            self.m, self.l = peak_m, peak_l
            return

        p_now = np.array(curr_history[-1])
        p_old = np.array(curr_history[0])
        vel_vec = (p_now - p_old) / len(curr_history)
        
        # Predictive Heading
        pred_m = peak_m + vel_vec[0] * 3.0 # Look ahead 3 frames
        pred_l = peak_l + vel_vec[1] * 3.0
        
        # Tether Logic
        tether = min(drift_ratio * TETHER_STIFFNESS * 15.0, 1.0)
        
        target_m = (pred_m * (1-tether)) + (peak_m * tether)
        target_l = (pred_l * (1-tether)) + (peak_l * tether)
        
        # Smooth Fly-by-wire
        self.m += (target_m - self.m) * 0.2
        self.l += (target_l - self.l) * 0.2
        
        self.velocity_heading = np.arctan2(vel_vec[1], vel_vec[0])
        
        # 5. DYNAMICS
        # Zoom Logic
        zoom_speed = DEFAULT_ZOOM
        if self.g_force > 0.3: zoom_speed = 1.01 # Airbrake (Zoom out)
        self.width *= zoom_speed
        
        # Azimuth Ramp
        if self.g_force < 0.2:
            self.azimuth += AZIMUTH_RAMP
        if self.azimuth > MAX_AZIMUTH: self.azimuth = MAX_AZIMUTH

# =========================================================
#  MAIN RENDER LOOP
# =========================================================

def run_quarkon_pov():
    print("--- 🕶️ QUARKON POV: ENGAGING FLIGHT SYSTEMS ---")
    
    pilot = FlightComputer(0.0, -5.0, FOV_WIDTH_START)
    
    # Warmup
    for _ in range(20): pilot.update(0.0)
        
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = 2 * np.pi * (f / 100)
        
        pilot.update(theta)
        
        # 1. CINEMATIC RENDER
        raw_img = render_cinematic_field(pilot.m, pilot.l, pilot.width, RENDER_RES, theta, pilot.azimuth)
        
        # 2. POST-PROCESSING
        # High contrast normalization for that "Sci-Fi" look
        norm = (raw_img - raw_img.min()) / (raw_img.max() - raw_img.min() + 1e-9)
        norm = np.power(norm, 0.45) 
        
        # Color Grading: Twilight Shifted (Cool blues into deep voids)
        rgb = (plt.get_cmap('twilight_shifted')(norm)[:, :, :3] * 255).astype(np.uint8)
        
        # Create PIL Image
        img_pil = Image.fromarray(np.flipud(rgb))
        
        # 3. HUD OVERLAY
        draw = ImageDraw.Draw(img_pil)
        
        # Minimalist Crosshair
        cx, cy = RENDER_RES//2, RENDER_RES//2
        # Slight transparency
        hud_fill = (200, 255, 255, 150)
        
        # Center Dot
        r = 2
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 255, 255))
        
        # Velocity Vector (The "Nose" of the craft)
        vx = cx + np.cos(pilot.velocity_heading) * 30
        vy = cy - np.sin(pilot.velocity_heading) * 30
        draw.line((cx, cy, vx, vy), fill=hud_fill, width=2)
        
        # Peripheral Arc (G-Force Meter)
        # We draw an arc at the bottom that grows with G-Force
        arc_rect = [cx - 50, RENDER_RES - 60, cx + 50, RENDER_RES - 20]
        start_ang = 180
        # G-force 0.0 -> 0 deg, 1.0 -> 180 deg
        sweep = pilot.g_force * 180
        draw.arc(arc_rect, start=start_ang, end=start_ang + sweep, fill=(255, 50, 50), width=3)
        
        # Text Data (Small, bottom corner)
        info_text = f"M:{pilot.m:.2f} L:{pilot.l:.2f} | AZM:{pilot.azimuth:.2f} | Z:{pilot.width:.4f}"
        draw.text((10, RENDER_RES - 20), info_text, fill=(100, 100, 100))

        frames_buffer.append(img_pil)
        
        if f % 20 == 0:
            print(f"Frame {f} | G-Force: {pilot.g_force:.2f} | Alt: {pilot.width:.4f}")

    print(f"Saving {OUTPUT_FILENAME} ({len(frames_buffer)} frames)...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=40, loop=0)
    print("✅ FLIGHT COMPLETE.")

if __name__ == "__main__":
    run_quarkon_pov()