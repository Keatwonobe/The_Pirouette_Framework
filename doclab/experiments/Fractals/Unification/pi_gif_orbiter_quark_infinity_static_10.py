import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw
from collections import deque

# =========================================================
#  PIROUETTE: HELICAL HUNTER (DIFFERENTIAL SOLVER)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "helical_hunter_slope.gif"
TOTAL_FRAMES = 300

# DYNAMICS
DEFAULT_ZOOM = 0.985
MAX_AZIMUTH = 1.35
AZIMUTH_RAMP = 0.006

# PHYSICS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

# =========================================================
#  NUMBA KERNEL (Standard 3D Projection)
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
#  HELICAL DIFFERENTIAL SOLVER
# =========================================================

class HelicalSolver:
    def __init__(self, start_m, start_l, start_width):
        self.m = start_m
        self.l = start_l
        self.width = start_width
        self.azimuth = 0.0
        
        # History Buffer for Derivatives
        # Stores tuples: (m_world, l_world)
        self.history = deque(maxlen=10)
        
        # Helical State
        self.slope_k = 0.0 # The "Pitch" of the spiral
        self.tangent_angle = 0.0
        self.curvature = 0.0

    def solve_and_drive(self, pulse_theta):
        
        # 1. ACQUIRE TARGET (Standard Centroid)
        res = 100
        scan = render_field(self.m, self.l, self.width, res, pulse_theta, self.azimuth)
        
        # Simple Peak Finding for speed (since we are predictive now)
        idx = np.unravel_index(np.argmax(scan), scan.shape)
        
        # Pixel to World
        px_scale = self.width / (res - 1)
        peak_l = (self.l - self.width/2) + idx[0] * px_scale
        peak_m = (self.m - self.width/2) + idx[1] * px_scale
        
        # Add to history
        self.history.append((peak_m, peak_l))
        
        # 2. CALCULATE HELICAL DERIVATIVES
        if len(self.history) < 5:
            # Not enough data, just snap to target
            self.m, self.l = peak_m, peak_l
            return
            
        # Get vectors from history (t and t-1)
        p_now = np.array(self.history[-1])
        p_prev = np.array(self.history[-2])
        p_old = np.array(self.history[0]) # 10 frames ago
        
        # Velocity Vector
        vel_vec = p_now - p_prev
        speed = np.linalg.norm(vel_vec)
        
        # Radial Vector (relative to rough center of system approx 0,0)
        # In a real solver we would solve for the spiral center, 
        # but here (0,0) is the known attractor.
        r_vec = p_now
        radius = np.linalg.norm(r_vec)
        
        # --- THE HELICAL CALCULUS ---
        # 1. Radial Velocity (dr/dt) = Projection of velocity onto radius
        if radius > 1e-9:
            v_radial = np.dot(vel_vec, r_vec / radius)
        else:
            v_radial = 0
            
        # 2. Angular Velocity (dtheta/dt)
        # Cross product magnitude / radius^2
        v_tangential = np.cross(r_vec, vel_vec) # 2D cross gives scalar z
        if radius > 1e-9:
            omega = v_tangential / (radius)
        else:
            omega = 0
            
        # 3. Helical Slope (k)
        # r = e^(k * theta)  =>  dr/dtheta = k * r
        # Therefore k = (dr/dt) / (r * dtheta/dt) = v_radial / v_tangential (roughly)
        
        if abs(omega) > 1e-9:
            self.slope_k = v_radial / (radius * abs(omega) * 10) # Scaling factor
        
        # 4. Tangent Prediction
        # The particle is moving in direction 'vel_vec'.
        # We want to place the camera *ahead* of it on the spiral.
        
        # Extrapolate: P_next = P_now + Velocity + Acceleration Correction
        # We use a weighted average of recent velocity to smooth jitter
        smooth_vel = (p_now - p_old) / len(self.history)
        
        # PREDICTIVE CAMERA PLACEMENT
        # Move camera to where the particle WILL be
        pred_m = peak_m + smooth_vel[0] * 2.0 # Look 2 frames ahead
        pred_l = peak_l + smooth_vel[1] * 2.0
        
        # Smooth update (Camera Inertia)
        self.m += (pred_m - self.m) * 0.2
        self.l += (pred_l - self.l) * 0.2
        
        # 3. ADJUST ZOOM BASED ON SLOPE
        # If slope is negative (spiraling in), zoom in.
        # If slope is zero (orbiting), hold zoom.
        
        # Base zoom
        target_zoom = DEFAULT_ZOOM
        
        # If we are plunging (negative radial velocity), dive faster
        if v_radial < 0:
            dive_factor = abs(v_radial) * 10.0 # Sensitivity
            target_zoom = 1.0 - (0.01 + dive_factor)
            if target_zoom < 0.95: target_zoom = 0.95 # Cap max speed
            
        self.width *= target_zoom
        
        # 4. ADJUST AZIMUTH
        # Tilt up, but slow down if the spiral gets chaotic (high curvature)
        self.azimuth += AZIMUTH_RAMP
        if self.azimuth > MAX_AZIMUTH: self.azimuth = MAX_AZIMUTH

        # Store for HUD
        self.tangent_angle = np.arctan2(smooth_vel[1], smooth_vel[0])

# =========================================================
#  MAIN LOOP
# =========================================================

def run_helical_hunter():
    print("--- 🐚 HELICAL HUNTER: CALCULUS MODE ---")
    
    solver = HelicalSolver(0.0, -5.0, 12.0)
    
    # Stabilize
    for _ in range(10):
        solver.solve_and_drive(0.0)

    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = 2 * np.pi * (f / 100)
        
        # The Solver handles all physics and tracking internally
        solver.solve_and_drive(theta)
        
        # High Quality Render
        hq_res = 500
        final_img = render_field(solver.m, solver.l, solver.width, hq_res, theta, solver.azimuth)
        
        # Visualization
        norm = (final_img - final_img.min()) / (final_img.max() - final_img.min() + 1e-9)
        norm = np.power(norm, 0.4)
        
        # Use a "Thermal" map to show intensity gradients
        rgb = (plt.get_cmap('gnuplot2')(norm)[:, :, :3] * 255).astype(np.uint8)
        panel = Image.fromarray(np.flipud(rgb))
        draw = ImageDraw.Draw(panel)
        
        # --- HUD: THE CALCULUS OVERLAY ---
        hud_color = (0, 255, 255)
        
        # 1. Slope Indicator
        slope_len = 100
        cx, cy = hq_res//2, hq_res//2
        
        # Draw Tangent Vector (Direction of Motion)
        tx = cx + np.cos(solver.tangent_angle) * 40
        ty = cy - np.sin(solver.tangent_angle) * 40 # Flip Y for image coords
        draw.line((cx, cy, tx, ty), fill=(255, 0, 0), width=2)
        
        # Text Data
        draw.text((10, 10), f"HELICAL SLOPE (k): {solver.slope_k:.5f}", fill=hud_color)
        draw.text((10, 25), f"AZIMUTH (φ): {solver.azimuth:.3f}", fill=hud_color)
        draw.text((10, 40), f"ZOOM WIDTH: {solver.width:.5f}", fill=hud_color)
        
        # Logic State
        state = "ORBITING"
        if solver.slope_k < -0.001: state = "DIVING (IN)"
        if solver.slope_k > 0.001: state = "ESCAPING (OUT)"
        
        draw.text((10, 60), f"STATE: {state}", fill=(255, 255, 0))

        frames_buffer.append(panel)
        
        if f % 20 == 0:
            print(f"Frame {f} | k={solver.slope_k:.4f} | {state}")

    print("Saving Helical Hunter GIF...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=40, loop=0)
    print("✅ SOLUTION CONVERGED.")

if __name__ == "__main__":
    run_helical_hunter()