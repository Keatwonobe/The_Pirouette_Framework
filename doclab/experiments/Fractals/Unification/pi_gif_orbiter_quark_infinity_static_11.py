import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw
from collections import deque

# =========================================================
#  PIROUETTE: TETHERED HELIX (ADAPTIVE SOLVER)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "tethered_helix_elastic.gif"
TOTAL_FRAMES = 350

# DYNAMICS
DEFAULT_ZOOM = 0.985
MAX_AZIMUTH = 1.35
AZIMUTH_RAMP = 0.006

# TETHER PHYSICS
SAFE_ZONE_RATIO = 0.10   # 10% of screen is "Green Zone"
MAX_HISTORY = 15         # Max smoothing for stable orbits
MIN_HISTORY = 3          # Min smoothing for chaotic turns
TETHER_STIFFNESS = 0.15  # How hard the rubber band snaps back

# PHYSICS KERNEL
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

# =========================================================
#  NUMBA KERNEL
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
            
            # Inverse Azimuth
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
#  ELASTIC SOLVER (VARIABLE MEMORY)
# =========================================================

class ElasticSolver:
    def __init__(self, start_m, start_l, start_width):
        self.m = start_m
        self.l = start_l
        self.width = start_width
        self.azimuth = 0.0
        
        # History Buffer
        self.history = deque(maxlen=MAX_HISTORY)
        
        # State
        self.active_window_size = MAX_HISTORY
        self.drift_penalty = 0.0
        self.slope_k = 0.0
        self.tangent_angle = 0.0

    def update(self, pulse_theta):
        
        # 1. SENSOR SCAN
        res = 100
        scan = render_field(self.m, self.l, self.width, res, pulse_theta, self.azimuth)
        
        # Find Peak
        idx = np.unravel_index(np.argmax(scan), scan.shape)
        
        # Pixel to World
        px_scale = self.width / (res - 1)
        peak_l = (self.l - self.width/2) + idx[0] * px_scale
        peak_m = (self.m - self.width/2) + idx[1] * px_scale
        
        # Store raw position
        self.history.append((peak_m, peak_l))
        
        # 2. CALCULATE DRIFT (The "Error")
        # How far is the target from the center of the camera view?
        # We are at (self.m, self.l). Target is at (peak_m, peak_l).
        dist_from_center = np.sqrt((peak_m - self.m)**2 + (peak_l - self.l)**2)
        drift_ratio = dist_from_center / (self.width / 2) # 0.0 to 1.0
        
        self.drift_penalty = drift_ratio
        
        # 3. ADAPTIVE WINDOW SIZING
        # If drift is high, noise is high -> Reduce window to react faster
        if drift_ratio > SAFE_ZONE_RATIO:
            # We are losing it! Drop memory.
            target_window = MIN_HISTORY
        else:
            # Stable. Use long memory.
            target_window = MAX_HISTORY
            
        # Smoothly adjust window size (Integer math)
        if self.active_window_size > target_window:
            self.active_window_size -= 1
        elif self.active_window_size < target_window:
            self.active_window_size += 1
            
        # 4. SOLVE TRAJECTORY
        # Slice history based on active window
        curr_history = list(self.history)[-self.active_window_size:]
        
        if len(curr_history) < 2:
            self.m, self.l = peak_m, peak_l
            return

        p_now = np.array(curr_history[-1])
        p_old = np.array(curr_history[0])
        
        # Calculate Velocity Vector (Average over the window)
        dt = len(curr_history)
        vel_vec = (p_now - p_old) / dt
        
        # HELICAL SLOPE CALC (For HUD/Zoom)
        r_vec = p_now
        radius = np.linalg.norm(r_vec)
        if radius > 1e-9:
            v_radial = np.dot(vel_vec, r_vec / radius)
            v_tangential = np.cross(r_vec, vel_vec)
            omega = v_tangential / radius
            if abs(omega) > 1e-9:
                self.slope_k = v_radial / (radius * abs(omega) * 10)

        # 5. THE ELASTIC MIXER
        # Prediction Term (Where is it going?)
        pred_m = peak_m + vel_vec[0] * 2.0 
        pred_l = peak_l + vel_vec[1] * 2.0
        
        # Correction Term (Where is it now?)
        # This is the "Tether" that pulls us back if we overshoot
        tether_force = drift_ratio * TETHER_STIFFNESS * 10.0
        if tether_force > 1.0: tether_force = 1.0
        
        # Final Camera Move
        # If drift is low, we trust prediction (fly smooth).
        # If drift is high, we trust correction (snap back).
        
        mix_prediction = (1.0 - tether_force)
        mix_correction = tether_force
        
        target_cam_m = (pred_m * mix_prediction) + (peak_m * mix_correction)
        target_cam_l = (pred_l * mix_prediction) + (peak_l * mix_correction)
        
        # Apply Move
        self.m += (target_cam_m - self.m) * 0.3
        self.l += (target_cam_l - self.l) * 0.3
        
        # Store for HUD
        self.tangent_angle = np.arctan2(vel_vec[1], vel_vec[0])
        
        # 6. DYNAMICS
        # Zoom Logic
        zoom_speed = DEFAULT_ZOOM
        if self.slope_k < -0.005: zoom_speed = 0.97 # Fast Dive
        if drift_ratio > 0.3: zoom_speed = 1.01     # Panic Zoom Out
        
        self.width *= zoom_speed
        
        # Azimuth Logic
        # If we are drifting, STOP tilting up. Stabilize first.
        if drift_ratio < 0.15:
            self.azimuth += AZIMUTH_RAMP
        
        if self.azimuth > MAX_AZIMUTH: self.azimuth = MAX_AZIMUTH

# =========================================================
#  MAIN EXECUTION
# =========================================================

def run_tethered_helix():
    print("--- 🔗 TETHERED HELIX: ADAPTIVE SOLVER ---")
    
    solver = ElasticSolver(0.0, -5.0, 12.0)
    
    # Pre-warm
    for _ in range(15):
        solver.update(0.0)

    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = 2 * np.pi * (f / 100)
        
        solver.update(theta)
        
        # Render
        hq_res = 500
        final_img = render_field(solver.m, solver.l, solver.width, hq_res, theta, solver.azimuth)
        
        norm = (final_img - final_img.min()) / (final_img.max() - final_img.min() + 1e-9)
        norm = np.power(norm, 0.45)
        
        # Visualization
        # Change color based on "Tension" (Drift Penalty)
        # Blue = Relaxed, Red = High Tension
        cmap_name = 'winter'
        if solver.drift_penalty > 0.2: cmap_name = 'cool'
        if solver.drift_penalty > 0.4: cmap_name = 'autumn'
        
        rgb = (plt.get_cmap(cmap_name)(norm)[:, :, :3] * 255).astype(np.uint8)
        panel = Image.fromarray(np.flipud(rgb))
        draw = ImageDraw.Draw(panel)
        
        # --- HUD ---
        hud_color = (255, 255, 255)
        cx, cy = hq_res//2, hq_res//2
        
        # 1. TETHER VISUALIZATION
        # Draw a line from center to the predicted tangent
        tx = cx + np.cos(solver.tangent_angle) * 50
        ty = cy - np.sin(solver.tangent_angle) * 50
        draw.line((cx, cy, tx, ty), fill=(255, 255, 0), width=2)
        
        # 2. DATA
        draw.text((10, 10), f"WINDOW SIZE: {solver.active_window_size} frames", fill=hud_color)
        draw.text((10, 25), f"TETHER TENSION: {solver.drift_penalty*100:.1f}%", fill=hud_color)
        draw.text((10, 40), f"HELICAL SLOPE: {solver.slope_k:.5f}", fill=hud_color)
        draw.text((10, 55), f"AZIMUTH: {solver.azimuth:.3f}", fill=hud_color)
        
        # 3. SAFE ZONE BOX
        safe_r = int(hq_res * SAFE_ZONE_RATIO)
        draw.rectangle([cx-safe_r, cy-safe_r, cx+safe_r, cy+safe_r], outline=(50, 50, 50))

        frames_buffer.append(panel)
        
        if f % 20 == 0:
            print(f"Frame {f} | Win: {solver.active_window_size} | Tension: {solver.drift_penalty:.2f}")

    print("Saving Tethered Helix GIF...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=40, loop=0)
    print("✅ DONE.")

if __name__ == "__main__":
    run_tethered_helix()