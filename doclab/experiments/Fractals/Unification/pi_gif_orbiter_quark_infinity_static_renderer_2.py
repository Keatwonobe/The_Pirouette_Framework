import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageOps
from collections import deque

# =========================================================
#  PIROUETTE: SHADOWBOX MANIFOLD (COCKPIT VIEW)
# =========================================================

# --- MISSION CONFIG ---
OUTPUT_FILENAME = "shadowbox_manifold_cockpit.gif"
TOTAL_FRAMES = 400

# RESOLUTION (Split Screen)
HUD_RES = 400          # The Instrument Panel (Square)
VIEW_RES = 400         # The Window (Square)
TOTAL_W = HUD_RES + VIEW_RES
TOTAL_H = 400

# FLIGHT DYNAMICS
FOV_WIDTH_START = 15.0
MAX_AZIMUTH = 1.45     # Maximum horizon look
TETHER_STIFFNESS = 0.15

# PHYSICS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

# =========================================================
#  KERNEL 1: SENSOR ARRAY (Logic & Targeting)
# =========================================================

@njit(parallel=True, fastmath=True)
def render_sensor(center_m, center_l, width, res, pulse_theta, azimuth_phi):
    # Standard intensity map for the computer to read
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
                dist = np.sqrt(dx*dx + dy*dy) + 1e-9
                phase = k * dist
                amp = (SRC_AMP / dist)
                psi_real += amp * np.cos(phase)
                psi_imag += amp * np.sin(phase)
                
            intensity_map[i, j] = psi_real**2 + psi_imag**2
            
    return intensity_map

# =========================================================
#  KERNEL 2: SHADOWBOX MANIFOLD (Visuals)
# =========================================================

@njit(parallel=True, fastmath=True)
def render_shadowbox(center_m, center_l, width, res, pulse_theta, azimuth_phi, light_angle):
    # Renders the surface gradients to simulate 3D lighting
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    # We compute a slightly larger grid to calculate gradients
    out_map = np.zeros((res, res), dtype=np.float64)
    
    c_sys, s_sys = np.cos(pulse_theta), np.sin(pulse_theta)
    c_phi, s_phi = np.cos(azimuth_phi), np.sin(azimuth_phi)
    
    # Light Vector (Rotating with system or independent)
    lx = np.cos(light_angle)
    ly = np.sin(light_angle)
    
    k = (2 * np.pi) / 10.0
    
    for i in prange(1, res-1):
        l_screen = l_vals[i]
        for j in range(1, res-1):
            m_screen = m_vals[j]
            
            # We need local gradient. Sample center, right, and down.
            # INVERSE AZIMUTH (Repeated for local sampling)
            # This is expensive but necessary for per-pixel lighting
            
            # Function to get val at offset
            # We define an inline logic here for speed
            
            base_val = 0.0
            dx_val = 0.0
            dy_val = 0.0
            
            # Sample 3 points: (x,y), (x+eps, y), (x, y+eps)
            # Eps is small step
            step = width / res
            
            # offsets: 0, 1 (x), 2 (y)
            for mode in range(3): 
                
                if mode == 0: dm_loc, dl_loc = 0, 0
                if mode == 1: dm_loc, dl_loc = step, 0
                if mode == 2: dm_loc, dl_loc = 0, step
                
                m_world_s = center_m + ((m_screen + dm_loc - center_m) * c_phi - (l_screen + dl_loc - center_l) * s_phi)
                l_world_s = center_l + ((m_screen + dm_loc - center_m) * s_phi + (l_screen + dl_loc - center_l) * c_phi)

                pr, pi = 0.0, 0.0
                for q in range(3):
                    sm = SRC_STRONG_M[q] * c_sys - SRC_STRONG_L[q] * s_sys
                    sl = SRC_STRONG_M[q] * s_sys + SRC_STRONG_L[q] * c_sys
                    d = np.sqrt((m_world_s - sm)**2 + (l_world_s - sl)**2) + 1e-9
                    ph = k * d
                    amp = (SRC_AMP / d)
                    pr += amp * np.cos(ph)
                    pi += amp * np.sin(ph)
                
                intensity = pr**2 + pi**2
                
                if mode == 0: base_val = intensity
                if mode == 1: dx_val = intensity
                if mode == 2: dy_val = intensity

            # Calculate Gradient
            grad_x = (dx_val - base_val) * 5.0 # Amplify ridges
            grad_y = (dy_val - base_val) * 5.0
            
            # Hillshading (Dot product with light vector)
            # If slope faces light, it is bright. If away, dark.
            shade = (grad_x * lx + grad_y * ly)
            
            # Combine with base ambient occlusion (inverted intensity)
            final = base_val + shade * 0.5
            out_map[i, j] = final
            
    return out_map

# =========================================================
#  FLIGHT COMPUTER
# =========================================================

class FlightComputer:
    def __init__(self, start_m, start_l, start_width):
        self.m, self.l = start_m, start_l
        self.width = start_width
        self.azimuth = 0.0
        self.history = deque(maxlen=10)
        self.heading = 0.0
        self.drift = 0.0

    def update(self, pulse_theta):
        # 1. READ SENSORS (Low Res)
        scan = render_sensor(self.m, self.l, self.width, 100, pulse_theta, self.azimuth)
        
        # 2. TARGETING
        idx = np.unravel_index(np.argmax(scan), scan.shape)
        px_scale = self.width / 99.0
        peak_l = (self.l - self.width/2) + idx[0] * px_scale
        peak_m = (self.m - self.width/2) + idx[1] * px_scale
        
        self.history.append((peak_m, peak_l))
        
        # 3. CALCULATE TETHER
        dist = np.sqrt((peak_m - self.m)**2 + (peak_l - self.l)**2)
        self.drift = dist / (self.width / 2)
        
        # 4. SOLVE MOTION
        if len(self.history) > 1:
            p_now = np.array(self.history[-1])
            p_old = np.array(self.history[0])
            vel = (p_now - p_old) / len(self.history)
            
            self.heading = np.arctan2(vel[1], vel[0])
            
            # Predict
            pred_m = peak_m + vel[0] * 3.0
            pred_l = peak_l + vel[1] * 3.0
            
            # Tether
            tether = min(self.drift * TETHER_STIFFNESS * 10, 1.0)
            
            target_m = (pred_m * (1-tether)) + (peak_m * tether)
            target_l = (pred_l * (1-tether)) + (peak_l * tether)
            
            self.m += (target_m - self.m) * 0.2
            self.l += (target_l - self.l) * 0.2
        else:
            self.m, self.l = peak_m, peak_l
            
        # 5. DYNAMICS
        if self.drift < 0.2: self.azimuth += 0.01
        if self.azimuth > MAX_AZIMUTH: self.azimuth = MAX_AZIMUTH
        
        zoom = 0.99
        if self.drift > 0.3: zoom = 1.01
        self.width *= zoom

# =========================================================
#  MAIN LOOP
# =========================================================

def run_cockpit():
    print("--- 🛫 COCKPIT SYSTEMS ONLINE ---")
    
    pilot = FlightComputer(0.0, -5.0, FOV_WIDTH_START)
    # Warmup
    for _ in range(15): pilot.update(0.0)
    
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = 2 * np.pi * (f / 100)
        
        # Update Physics
        pilot.update(theta)
        
        # --- RENDER PASS 1: INSTRUMENTS (HUD) ---
        hud_raw = render_sensor(pilot.m, pilot.l, pilot.width, HUD_RES, theta, pilot.azimuth)
        norm_hud = (hud_raw - hud_raw.min()) / (hud_raw.max() - hud_raw.min() + 1e-9)
        norm_hud = np.power(norm_hud, 0.5)
        
        # HUD is Electric Green/Blue wireframe style
        rgb_hud = (plt.get_cmap('winter')(norm_hud)[:, :, :3] * 255).astype(np.uint8)
        img_hud = Image.fromarray(np.flipud(rgb_hud))
        
        # Draw HUD Vectors
        d_hud = ImageDraw.Draw(img_hud)
        cx, cy = HUD_RES//2, HUD_RES//2
        
        # Velocity Vector
        vx = cx + np.cos(pilot.heading) * 40
        vy = cy - np.sin(pilot.heading) * 40
        d_hud.line((cx, cy, vx, vy), fill=(255, 255, 0), width=2)
        d_hud.rectangle([cx-10, cy-10, cx+10, cy+10], outline=(0, 255, 0))
        d_hud.text((10, 10), f"SENSOR FEED", fill=(0, 255, 0))
        d_hud.text((10, 380), f"TENSION: {pilot.drift*100:.1f}%", fill=(0, 255, 0))

        # --- RENDER PASS 2: SHADOWBOX (Window) ---
        # Rotate light source slowly to "flash" the ridges
        light_angle = f * 0.05 
        
        win_raw = render_shadowbox(pilot.m, pilot.l, pilot.width, VIEW_RES, theta, pilot.azimuth, light_angle)
        
        # Normalize with a "substrate" curve
        norm_win = (win_raw - win_raw.min()) / (win_raw.max() - win_raw.min() + 1e-9)
        
        # Use 'copper' or 'bone' for that physical manifold look
        rgb_win = (plt.get_cmap('copper')(norm_win)[:, :, :3] * 255).astype(np.uint8)
        img_win = Image.fromarray(np.flipud(rgb_win))
        
        d_win = ImageDraw.Draw(img_win)
        d_win.text((10, 10), "VISUAL: SHADOWBOX", fill=(255, 200, 100))
        
        # --- COMPOSITE ---
        cockpit = Image.new('RGB', (TOTAL_W, TOTAL_H))
        cockpit.paste(img_hud, (0, 0))
        cockpit.paste(img_win, (HUD_RES, 0))
        
        # Draw Center Divider
        d_total = ImageDraw.Draw(cockpit)
        d_total.line((HUD_RES, 0, HUD_RES, TOTAL_H), fill=(50, 50, 50), width=4)
        
        frames_buffer.append(cockpit)
        
        if f % 20 == 0:
            print(f"Frame {f} | Azim: {pilot.azimuth:.2f} | Drift: {pilot.drift:.3f}")

    print("Saving Cockpit View...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=40, loop=0)
    print("✅ SYSTEM SHUTDOWN.")

if __name__ == "__main__":
    run_cockpit()