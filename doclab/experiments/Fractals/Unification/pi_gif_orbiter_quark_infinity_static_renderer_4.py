import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from numba import njit, prange
from PIL import Image, ImageDraw
from collections import deque
import colorsys

# =========================================================
#  PIROUETTE: GEMINI PROTOCOL (DUAL-VIEW UNIFICATION)
# =========================================================

# --- CONFIG ---
OUTPUT_FILENAME = "gemini_protocol_unified.gif"
TOTAL_FRAMES = 450
PANEL_RES = 400        # Resolution per panel
TOTAL_W = PANEL_RES * 2
TOTAL_H = PANEL_RES

# VIEW SETTINGS
ISO_ANGLE = 0.85       # ~48 degree tilt (Isometric)
LEFT_ZOOM = 12.0       # Tight lock (Pilot)
RIGHT_ZOOM = 30.0      # Wide view (Map)

# PHYSICS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0
OMEGA_SYS = 0.05       # Rotation speed of the system

# =========================================================
#  KERNELS
# =========================================================

@njit(parallel=True, fastmath=True)
def render_iso_field(center_m, center_l, width, res, src_m_arr, src_l_arr, pulse, iso_angle):
    # Generic Kernel for both views
    # Renders the V4 Isocontours
    
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
            contour = 0.5 + 0.5 * np.sin(log_amp * 20.0) # Tight rings
            
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
    # Gradient of the STATIC field (Co-rotating)
    eps = 0.01
    def val(tm, tl):
        pr, pi = 0.0, 0.0
        k = (2*np.pi)/10.0
        for q in range(3):
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
#  SIMULATION & ORCHESTRATION
# =========================================================

def run_gemini():
    print("--- ♊ GEMINI PROTOCOL INITIATED ---")
    
    # 1. SETUP
    # Particle starts in Co-Rotating Frame
    pm, pl = 0.0, -6.0
    vm, vl = 0.15, 0.0
    
    # History buffers
    ribbon_history = deque(maxlen=20) # For Left Panel (Short term)
    
    # Persistent Trail Layer for Right Panel
    trail_layer = Image.new("RGBA", (PANEL_RES, PANEL_RES), (0,0,0,0))
    trail_draw = ImageDraw.Draw(trail_layer)
    last_trail_pt = None
    
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        
        # --- PHYSICS STEP (CO-ROTATING FRAME) ---
        pulse = 1.0 + 0.15 * np.sin(f * 0.1)
        
        # Forces
        gm, gl = get_gradient(pm, pl, pulse)
        
        # Coriolis & Centrifugal (Fake forces because we are in rotating frame)
        omega = OMEGA_SYS
        
        # F_cor = -2w x v
        cor_m = 2 * omega * vl
        cor_l = -2 * omega * vm
        
        # F_cen = w^2 * r
        cen_m = (omega**2) * pm
        cen_l = (omega**2) * pl
        
        # Gradient "surf"
        force_m = gm * 0.02
        force_l = gl * 0.02
        
        vm += (force_m + cor_m + cen_m)
        vl += (force_l + cor_l + cen_l)
        
        # Friction
        vm *= 0.97
        vl *= 0.97
        
        pm += vm
        pl += vl
        
        # --- COORDINATE TRANSFORM (LAB FRAME) ---
        # For the Left Panel, we need to know where the particle is in the "Real" spinning world
        # Rotation Matrix
        sys_theta = f * OMEGA_SYS
        c, s = np.cos(sys_theta), np.sin(sys_theta)
        
        # Lab Coords
        lab_m = pm * c - pl * s
        lab_l = pm * s + pl * c
        
        ribbon_history.append((lab_m, lab_l))
        
        # --- RENDER LEFT: PILOT VIEW (LAB FRAME) ---
        # Center = Lab Particle Position
        # Sources = Rotated
        
        rot_src_m = SRC_STRONG_M * c - SRC_STRONG_L * s
        rot_src_l = SRC_STRONG_M * s + SRC_STRONG_L * c
        
        raw_left = render_iso_field(lab_m, lab_l, LEFT_ZOOM, PANEL_RES, rot_src_m, rot_src_l, pulse, ISO_ANGLE)
        img_left = Image.fromarray((raw_left * 255).astype(np.uint8))
        
        # Draw Ribbon (Lab Frame Trail)
        d_left = ImageDraw.Draw(img_left)
        # Project ribbon points relative to camera (lab_m, lab_l)
        cx, cy = PANEL_RES/2, PANEL_RES/2
        scale_left = PANEL_RES / LEFT_ZOOM
        aspect = np.cos(ISO_ANGLE)
        
        pts_left = []
        for (hm, hl) in ribbon_history:
            dm = hm - lab_m
            dl = hl - lab_l
            sx = cx + dm * scale_left
            sy = cy - (dl * scale_left * aspect) # Flip Y + aspect squash
            pts_left.append((sx, sy))
            
        if len(pts_left) > 1:
            d_left.line(pts_left, fill=(255, 255, 100), width=3)
            
        # HUD Left
        d_left.text((10, 10), "PILOT VIEW [LAB FRAME]", fill=(0, 255, 255))
        d_left.text((10, 25), "HELICAL LOCK: ACTIVE", fill=(0, 255, 255))
        d_left.rectangle([cx-10, cy-10, cx+10, cy+10], outline=(0, 255, 0)) # Reticle

        # --- RENDER RIGHT: NAVIGATOR VIEW (CO-ROTATING FRAME) ---
        # Center = (0,0)
        # Sources = Fixed (Base Position)
        
        raw_right = render_iso_field(0.0, 0.0, RIGHT_ZOOM, PANEL_RES, SRC_STRONG_M, SRC_STRONG_L, pulse, ISO_ANGLE)
        # Darken the background map to make trail pop
        img_right = Image.fromarray((raw_right * 150).astype(np.uint8)) 
        
        # Update Trail Layer (Persistent)
        scale_right = PANEL_RES / RIGHT_ZOOM
        sx = cx + pm * scale_right
        sy = cy - (pl * scale_right * aspect)
        
        current_pt = (sx, sy)
        
        if last_trail_pt:
            # Color cycle for time
            hue = (f % 100) / 100.0
            r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
            col = (int(r*255), int(g*255), int(b*255), 255)
            trail_draw.line([last_trail_pt, current_pt], fill=col, width=2)
            
        last_trail_pt = current_pt
        
        # Composite
        img_right.paste(trail_layer, (0,0), trail_layer)
        
        # HUD Right
        d_right = ImageDraw.Draw(img_right)
        d_right.text((10, 10), "TOPOLOGY MAP [CO-ROTATING]", fill=(255, 200, 100))
        d_right.text((10, 25), "META-PATH INTEGRATION", fill=(255, 200, 100))
        d_right.ellipse([sx-3, sy-3, sx+3, sy+3], fill=(255, 255, 255)) # The Particle

        # --- STITCH ---
        combined = Image.new("RGB", (TOTAL_W, TOTAL_H))
        combined.paste(img_left, (0, 0))
        combined.paste(img_right, (PANEL_RES, 0))
        
        # Divider
        d_com = ImageDraw.Draw(combined)
        d_com.line((PANEL_RES, 0, PANEL_RES, TOTAL_H), fill=(50, 50, 50), width=4)
        
        frames_buffer.append(combined)
        
        if f % 20 == 0:
            print(f"Frame {f} | P_Lab: ({lab_m:.2f}, {lab_l:.2f})")

    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=30, loop=0)
    print("✅ GEMINI PROTOCOL COMPLETE.")

if __name__ == "__main__":
    run_gemini()