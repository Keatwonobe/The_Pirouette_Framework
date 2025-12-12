import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from numba import njit, prange
from PIL import Image, ImageDraw
from collections import deque
import colorsys

# =========================================================
#  PIROUETTE: GEMINI MK.II (TORSION-LOCKED)
# =========================================================

# --- CONFIG ---
OUTPUT_FILENAME = "gemini_torsion_locked.gif"
TOTAL_FRAMES = 450
PANEL_RES = 400
TOTAL_W = PANEL_RES * 2
TOTAL_H = PANEL_RES

# VIEW SETTINGS
ISO_ANGLE = 0.85       # Diagonal View
LEFT_ZOOM = 12.0       # Pilot View (Tight)
RIGHT_ZOOM = 35.0      # Map View (Wide)

# PHYSICS CONSTANTS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

# ROTATION DYNAMICS
OMEGA_SYS = 0.06       # The speed of the manifold spin
KAPPA_TWIST = 1.2      # THE FIX: Torsion strength (Restoring force)

# =========================================================
#  KERNELS
# =========================================================

@njit(parallel=True, fastmath=True)
def render_iso_field(center_m, center_l, width, res, src_m_arr, src_l_arr, pulse, iso_angle):
    # Standard V4 Isocontour Renderer
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
            contour = 0.5 + 0.5 * np.sin(log_amp * 20.0) 
            
            hue = (phase_val + np.pi) / (2 * np.pi)
            val = contour * np.minimum(1.0, 1.5 / (dist * 0.15 + 1.0))
            
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
    # Calculates the "Slope" of the potential well
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
#  TORSION-LOCKED PHYSICS ENGINE
# =========================================================

def run_gemini_mk2():
    print("--- ♊ GEMINI Mk.II: TORSION LOCK ENGAGED ---")
    
    # 1. INITIAL STATE (Co-Rotating Frame)
    # Start at a stable orbital distance
    pm, pl = 0.0, -7.0 
    vm, vl = 0.35, 0.0 # Tangential kick
    
    ribbon_history = deque(maxlen=20)
    trail_layer = Image.new("RGBA", (PANEL_RES, PANEL_RES), (0,0,0,0))
    trail_draw = ImageDraw.Draw(trail_layer)
    last_trail_pt = None
    
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        
        # --- A. PHYSICS STEP ---
        pulse = 1.0 + 0.15 * np.sin(f * 0.1)
        
        # 1. Gradient Force (The Manifold Slope)
        gm, gl = get_gradient(pm, pl, pulse)
        force_m = gm * 0.04 # Boosted gradient grip
        force_l = gl * 0.04
        
        # 2. Rotational Pseudo-Forces
        # Because we are in a rotating frame, we feel centrifugal force pushing OUT.
        omega = OMEGA_SYS
        r_sq = pm**2 + pl**2
        r = np.sqrt(r_sq)
        
        cen_m = (omega**2) * pm
        cen_l = (omega**2) * pl
        
        # Coriolis (Deflection)
        cor_m = 2 * omega * vl
        cor_l = -2 * omega * vm
        
        # 3. THE FIX: TORSION (Elastic Binding Energy)
        # This represents the "Twist" (Kappa) in the Hamiltonian.
        # It acts like a rubber band that gets tighter the faster you spin.
        # F_twist = -kappa * omega * r
        twist_m = -KAPPA_TWIST * omega * pm
        twist_l = -KAPPA_TWIST * omega * pl
        
        # Total Acceleration
        # Notice: Twist opposes Centrifugal
        acc_m = force_m + cor_m + cen_m + twist_m
        acc_l = force_l + cor_l + cen_l + twist_l
        
        # Integrate (Verlet-ish)
        vm += acc_m
        vl += acc_l
        
        # Friction (Drag from the ether)
        vm *= 0.98
        vl *= 0.98
        
        pm += vm
        pl += vl
        
        # --- B. COORDINATE TRANSFORM (To Lab Frame) ---
        sys_theta = f * OMEGA_SYS
        c, s = np.cos(sys_theta), np.sin(sys_theta)
        
        lab_m = pm * c - pl * s
        lab_l = pm * s + pl * c
        
        ribbon_history.append((lab_m, lab_l))
        
        # --- C. RENDER LEFT: PILOT (Lab Frame) ---
        # Rotate sources to match lab time
        rot_src_m = SRC_STRONG_M * c - SRC_STRONG_L * s
        rot_src_l = SRC_STRONG_M * s + SRC_STRONG_L * c
        
        raw_left = render_iso_field(lab_m, lab_l, LEFT_ZOOM, PANEL_RES, rot_src_m, rot_src_l, pulse, ISO_ANGLE)
        img_left = Image.fromarray((raw_left * 255).astype(np.uint8))
        
        d_left = ImageDraw.Draw(img_left)
        
        # Draw Ribbon
        cx, cy = PANEL_RES/2, PANEL_RES/2
        scale_left = PANEL_RES / LEFT_ZOOM
        aspect = np.cos(ISO_ANGLE)
        
        pts_left = []
        for (hm, hl) in ribbon_history:
            dm = hm - lab_m
            dl = hl - lab_l
            sx = cx + dm * scale_left
            sy = cy - (dl * scale_left * aspect) 
            pts_left.append((sx, sy))
            
        if len(pts_left) > 1:
            d_left.line(pts_left, fill=(255, 255, 100), width=3)
            
        d_left.text((10, 10), "PILOT VIEW [LAB FRAME]", fill=(0, 255, 255))
        d_left.rectangle([cx-15, cy-15, cx+15, cy+15], outline=(0, 255, 0)) # Target Box

        # --- D. RENDER RIGHT: NAVIGATOR (Co-Rotating Frame) ---
        # Sources are FIXED here
        raw_right = render_iso_field(0.0, 0.0, RIGHT_ZOOM, PANEL_RES, SRC_STRONG_M, SRC_STRONG_L, pulse, ISO_ANGLE)
        img_right = Image.fromarray((raw_right * 120).astype(np.uint8)) # Dimmer map
        
        # Trail (Persistent)
        scale_right = PANEL_RES / RIGHT_ZOOM
        sx = cx + pm * scale_right
        sy = cy - (pl * scale_right * aspect)
        
        current_pt = (sx, sy)
        
        if last_trail_pt:
            # Color cycle based on velocity (Heat)
            speed = np.sqrt(vm**2 + vl**2)
            hue = np.clip(speed * 2.0, 0.0, 0.6) # Red/Yellow/Green
            r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
            col = (int(r*255), int(g*255), int(b*255), 255)
            trail_draw.line([last_trail_pt, current_pt], fill=col, width=2)
            
        last_trail_pt = current_pt
        
        img_right.paste(trail_layer, (0,0), trail_layer)
        
        d_right = ImageDraw.Draw(img_right)
        d_right.text((10, 10), "META-PATH [CO-ROTATING]", fill=(255, 200, 100))
        d_right.ellipse([sx-4, sy-4, sx+4, sy+4], fill=(255, 255, 255)) 

        # --- E. STITCH ---
        combined = Image.new("RGB", (TOTAL_W, TOTAL_H))
        combined.paste(img_left, (0, 0))
        combined.paste(img_right, (PANEL_RES, 0))
        
        draw_final = ImageDraw.Draw(combined)
        draw_final.line((PANEL_RES, 0, PANEL_RES, TOTAL_H), fill=(100, 100, 100), width=4)
        
        # Torsion Gauge
        gauge_w = 200
        gauge_h = 10
        gx = PANEL_RES - gauge_w//2
        gy = TOTAL_H - 20
        draw_final.rectangle([gx, gy, gx+gauge_w, gy+gauge_h], outline=(100,100,100))
        fill_w = int(gauge_w * (KAPPA_TWIST/2.0))
        draw_final.rectangle([gx, gy, gx+fill_w, gy+gauge_h], fill=(0, 255, 0))
        draw_final.text((gx, gy-15), f"TORSION LOCK: {KAPPA_TWIST}", fill=(0, 255, 0))

        frames_buffer.append(combined)
        
        if f % 20 == 0:
            print(f"Frame {f} | R: {r:.2f}")

    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=30, loop=0)
    print("✅ LOCKED AND LOADED.")

if __name__ == "__main__":
    run_gemini_mk2()