import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageOps
from collections import deque
import colorsys

# =========================================================
#  PIROUETTE: META-ORBITER TRIPLE-PANEL ORCHESTRATOR
# =========================================================

# --- MISSION CONFIG (MERGED) ---
OUTPUT_FILENAME = "meta_orbiter_triple_view.gif"
TOTAL_FRAMES = 450
TOTAL_H = 600          # Unified height for all panels

# RESOLUTION (FROM SCRIPTS 2 & 5)
HUD_RES = 400
VIEW_RES = 400
PANEL_RES = 600
TOTAL_W = HUD_RES + VIEW_RES + PANEL_RES

# FLIGHT DYNAMICS (FROM SCRIPT 2)
FOV_WIDTH_START = 15.0
MAX_AZIMUTH = 1.45
TETHER_STIFFNESS = 0.15

# VIEW SETTINGS (FROM SCRIPT 5)
ISO_ANGLE = 0.85
WIDE_ZOOM = 150.0

# PHYSICS (SHARED)
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0
OMEGA_SYS = 0.05

# =========================================================
#  KERNELS 1 & 2: SENSOR & SHADOWBOX (FROM SCRIPT 2)
# =========================================================

@njit(parallel=True, fastmath=True)
def render_sensor(center_m, center_l, width, res, pulse_theta, azimuth_phi):
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

@njit(parallel=True, fastmath=True)
def render_shadowbox(center_m, center_l, width, res, pulse_theta, azimuth_phi, light_angle):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    out_map = np.zeros((res, res), dtype=np.float64)
    
    c_sys, s_sys = np.cos(pulse_theta), np.sin(pulse_theta)
    c_phi, s_phi = np.cos(azimuth_phi), np.sin(azimuth_phi)
    
    # Light Vector
    lx = np.cos(light_angle)
    ly = np.sin(light_angle)
    
    k = (2 * np.pi) / 10.0
    
    for i in prange(1, res-1):
        l_screen = l_vals[i]
        for j in range(1, res-1):
            m_screen = m_vals[j]
            
            step = width / res
            
            # Sample 3 points: (x,y), (x+eps, y), (x, y+eps) for gradient
            base_val, dx_val, dy_val = 0.0, 0.0, 0.0
            
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

            # Calculate Gradient and Hillshading
            grad_x = (dx_val - base_val) * 5.0 
            grad_y = (dy_val - base_val) * 5.0
            shade = (grad_x * lx + grad_y * ly)
            
            final = base_val + shade * 0.5
            out_map[i, j] = final
            
    return out_map

# =========================================================
#  FLIGHT COMPUTER (FROM SCRIPT 2)
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
#  KERNELS 3 & 4: CO-ROTATING MAP & GRADIENT (FROM SCRIPT 5)
# =========================================================

@njit(parallel=True, fastmath=True)
def render_iso_field(center_m, center_l, width, res, src_m_arr, src_l_arr, pulse, iso_angle):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    img_out = np.zeros((res, res, 3), dtype=np.float64)
    aspect = 1.0 / np.cos(iso_angle)
    k = (2 * np.pi) / 10.0
    
    for i in prange(res):
        l_screen = l_vals[i]
        for j in range(res):
            m_screen = m_vals[j]
            
            # Iso Projection
            dm = m_screen - center_m
            dl = (l_screen - center_l) * aspect
            m_world = center_m + dm
            l_world = center_l + dl

            psi_r, psi_i = 0.0, 0.0
            
            # Sources are STATIC in this frame
            for q in range(3):
                dx = m_world - src_m_arr[q]
                dy = l_world - src_l_arr[q]
                dist = np.sqrt(dx*dx + dy*dy) + 1e-9
                
                phase = k * dist
                amp = (SRC_AMP / dist) * pulse
                
                psi_r += amp * np.cos(phase)
                psi_i += amp * np.sin(phase)
            
            # Coloring (V4 Neon) 
            amp_val = np.sqrt(psi_r**2 + psi_i**2)
            phase_val = np.arctan2(psi_i, psi_r)
            
            log_amp = np.log1p(amp_val)
            contour = 0.5 + 0.5 * np.sin(log_amp * 20.0)
            
            hue = (phase_val + np.pi) / (2 * np.pi)
            val = contour * np.minimum(1.0, 1.5 / (dist * 0.15 + 1.0)) 
            
            # Fast RGB (Hue Rotation)
            h6 = hue * 6.0
            x = (1.0 - abs((h6 % 2.0) - 1.0))
            if h6 < 1: r,g,b = 1,x,0
            elif h6 < 2: r,g,b = x,1,0
            elif h6 < 3: r,g,b = 0,1,x
            elif h6 < 4: r,g,b = 0,x,1
            elif h6 < 5: r,g,b = x,0,1
            else: r,g,b = 1,0,x
            
            img_out[i, j, 0] = r * val
            img_out[i, j, 1] = g * val
            img_out[i, j, 2] = b * val
            
    return img_out

@njit(fastmath=True)
def get_gradient(m, l, pulse):
    eps = 0.01
    def val(tm, tl):
        pr, pi = 0.0, 0.0
        k = (2*np.pi)/10.0
        for q in range(3):
            # Sources are STATIC in this frame
            d = np.sqrt((tm-SRC_STRONG_M[q])**2 + (tl-SRC_STRONG_L[q])**2) + 1e-9
            a = (SRC_AMP/d) * pulse
            ph = k*d
            pr += a*np.cos(ph)
            pi += a*np.sin(ph)
        return pr**2 + pi**2
    
    v0 = val(m, l)
    gm = (val(m+eps, l) - v0)/eps
    gl = (val(m, l+eps) - v0)/eps
    return gm, gl

# =========================================================
#  MAIN ORCHESTRATION LOOP
# =========================================================

def run_triple_panel():
    print("--- 🚀 META-ORBITER TRIPLE-PANEL ONLINE ---")
    
    # --- PANEL 1 & 2 INIT (FlightComputer) ---
    pilot = FlightComputer(0.0, -5.0, FOV_WIDTH_START)
    for _ in range(15): pilot.update(0.0)
    
    # --- PANEL 3 INIT (Co-Rotating) ---
    pm, pl = 0.0, -6.0
    vm, vl = 0.15, 0.0
    center_m, center_l = 0.0, 0.0
    
    # Initialize trail layer (height adjusted to TOTAL_H)
    trail_layer = Image.new("RGBA", (PANEL_RES, TOTAL_H), (0,0,0,0))
    trail_draw = ImageDraw.Draw(trail_layer)
    last_trail_pt = None
    
    # --- AVERAGE TRACKING (META-WINDOW) ---
    cumulative_m = 0.0
    cumulative_l = 0.0
    total_frames_count = 0
    
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = 2 * np.pi * (f / 100)
        
        # =========================================================
        #  PANEL 1 & 2: FLIGHT COMPUTER + COCKPIT VIEW (Script 2)
        # =========================================================
        pilot.update(theta)
        
        # RENDER 1: INSTRUMENTS (HUD)
        hud_raw = render_sensor(pilot.m, pilot.l, pilot.width, HUD_RES, theta, pilot.azimuth)
        norm_hud = (hud_raw - hud_raw.min()) / (hud_raw.max() - hud_raw.min() + 1e-9)
        norm_hud = np.power(norm_hud, 0.5)
        
        rgb_hud = (plt.get_cmap('winter')(norm_hud)[:, :, :3] * 255).astype(np.uint8)
        img_hud = Image.fromarray(np.flipud(rgb_hud))
        img_hud = img_hud.resize((HUD_RES, TOTAL_H)) # Resize to unified height

        # Draw HUD Vectors (Centering on HUD_RES/2, TOTAL_H/2)
        d_hud = ImageDraw.Draw(img_hud)
        cx, cy = HUD_RES//2, TOTAL_H//2
        vx = cx + np.cos(pilot.heading) * 40
        vy = cy - np.sin(pilot.heading) * 40
        d_hud.line((cx, cy, vx, vy), fill=(255, 255, 0), width=2)
        d_hud.rectangle([cx-10, cy-10, cx+10, cy+10], outline=(0, 255, 0))
        d_hud.text((10, 10), f"SENSOR FEED", fill=(0, 255, 0))
        d_hud.text((10, TOTAL_H - 20), f"TENSION: {pilot.drift*100:.1f}%", fill=(0, 255, 0))

        # RENDER 2: SHADOWBOX (Window)
        light_angle = f * 0.05 
        win_raw = render_shadowbox(pilot.m, pilot.l, pilot.width, VIEW_RES, theta, pilot.azimuth, light_angle)
        norm_win = (win_raw - win_raw.min()) / (win_raw.max() - win_raw.min() + 1e-9)
        
        rgb_win = (plt.get_cmap('copper')(norm_win)[:, :, :3] * 255).astype(np.uint8)
        img_win = Image.fromarray(np.flipud(rgb_win))
        img_win = img_win.resize((VIEW_RES, TOTAL_H)) # Resize to unified height

        d_win = ImageDraw.Draw(img_win)
        d_win.text((10, 10), "VISUAL: SHADOWBOX", fill=(255, 200, 100))
        
        # =========================================================
        #  PANEL 3: CO-ROTATING MAP + META-AVERAGE (Script 5)
        # =========================================================
        
        # --- PHYSICS STEP (CO-ROTATING FRAME) ---
        pulse = 1.0 + 0.15 * np.sin(f * 0.1)
        
        gm, gl = get_gradient(pm, pl, pulse)
        
        omega = OMEGA_SYS
        cor_m = 2 * omega * vl
        cor_l = -2 * omega * vm
        cen_m = (omega**2) * pm
        cen_l = (omega**2) * pl
        
        force_m = gm * 0.02
        force_l = gl * 0.02
        
        vm += (force_m + cor_m + cen_m)
        vl += (force_l + cor_l + cen_l)
        
        vm *= 0.97
        vl *= 0.97
        
        pm += vm
        pl += vl
        
        # --- AVERAGE CALCULATION ---
        cumulative_m += pm
        cumulative_l += pl
        total_frames_count += 1
        average_m = cumulative_m / total_frames_count
        average_l = cumulative_l / total_frames_count
        
        # --- RENDER 3: CO-ROTATING FIELD ---
        raw_image = render_iso_field(center_m, center_l, WIDE_ZOOM, PANEL_RES, 
                                     SRC_STRONG_M, SRC_STRONG_L, pulse, ISO_ANGLE)
        
        img_map = Image.fromarray((raw_image * 150).astype(np.uint8)) 
        img_map = img_map.transpose(Image.FLIP_TOP_BOTTOM) # Flip for correct world coords
        img_map = img_map.resize((PANEL_RES, TOTAL_H))

        # --- UPDATE TRAIL LAYER (Persistent) ---
        scale = PANEL_RES / WIDE_ZOOM
        aspect = np.cos(ISO_ANGLE)
        cx, cy = PANEL_RES//2, TOTAL_H//2
        
        # Project current particle position (pm, pl)
        sx = cx + pm * scale
        sy = cy - (pl * scale * aspect) 
        current_pt = (sx, sy)
        
        if last_trail_pt:
            # Draw persistent path
            hue = (f % 100) / 100.0
            r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
            col = (int(r*255), int(g*255), int(b*255), 255)
            trail_draw.line([last_trail_pt, current_pt], fill=col, width=2)
            
        last_trail_pt = current_pt
        img_map.paste(trail_layer, (0,0), trail_layer)

        # --- DRAW PARTICLE & AVERAGE ---
        d_map = ImageDraw.Draw(img_map)
        
        # 1. Particle Marker (White)
        d_map.ellipse([sx-4, sy-4, sx+4, sy+4], fill=(255, 255, 255)) 

        # 2. META-AVERAGE MARKER (Magenta Ring)
        ax = cx + average_m * scale
        ay = cy - (average_l * scale * aspect)
        d_map.ellipse([ax-10, ay-10, ax+10, ay+10], outline=(255, 0, 255), width=3)
        
        # HUD Text
        d_map.text((10, 10), "TOPOLOGY MAP [CO-ROTATING]", fill=(255, 200, 100))
        d_map.text((10, 30), f"P_INST: ({pm:.2f}, {pl:.2f})", fill=(255, 255, 255))
        d_map.text((10, 50), f"AVG P: ({average_m:.2f}, {average_l:.2f})", fill=(255, 0, 255))
        
        # =========================================================
        #  COMPOSITE & SAVE
        # =========================================================
        cockpit = Image.new('RGB', (TOTAL_W, TOTAL_H))
        
        cockpit.paste(img_hud, (0, 0))
        cockpit.paste(img_win, (HUD_RES, 0))
        cockpit.paste(img_map, (HUD_RES + VIEW_RES, 0))
        
        # Draw Center Dividers
        d_total = ImageDraw.Draw(cockpit)
        d_total.line((HUD_RES, 0, HUD_RES, TOTAL_H), fill=(50, 50, 50), width=4)
        d_total.line((HUD_RES + VIEW_RES, 0, HUD_RES + VIEW_RES, TOTAL_H), fill=(50, 50, 50), width=4)
        
        frames_buffer.append(cockpit)
        
        if f % 50 == 0:
            print(f"Frame {f} | Avg P: ({average_m:.2f}, {average_l:.2f})")

    print(f"Saving {OUTPUT_FILENAME}...")
    # Reduce duration to 30ms for a faster animation
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=30, loop=0)
    print("✅ TRIPLE-PANEL COMPOSITE COMPLETE. System Shutdown.")

if __name__ == "__main__":
    run_triple_panel()