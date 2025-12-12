import numpy as np
from numba import njit, prange
from PIL import Image, ImageDraw
from collections import deque
import colorsys

# =========================================================
#  PIROUETTE: UNIFIED RENDERER (GEMINI V5 Refactored)
# =========================================================

# --- CONFIG ---
OUTPUT_FILENAME = "wide_angle_co_rotating_map.gif"
OUTPUT_FILENAME_2 = "helical_illuminator_iso.gif"
TOTAL_FRAMES = 250
PANEL_RES = 600

# VIEW SETTINGS
ISO_ANGLE = 0.85       # ~48 degree tilt (Isometric)
WIDE_ZOOM = 150.0      # Very Wide view for run_map()
LEFT_ZOOM = 14.0       # Tight view for run_illuminator()

# PHYSICS CONSTANTS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0
OMEGA_SYS = 0.05       # Rotation speed of the system

# ORBITER DYNAMICS (for run_map)
TRAIL_LENGTH = 40
DRAG_FACTOR = 0.995    # Slightly increased friction for co-rot map

# HELICAL ILLUMINATOR DYNAMICS (for run_illuminator)
TRAIL_LENGTH_HELIX = 25 # Shorter trail for the ribbon
ISO_ANGLE_2 = 0.85
KAPPA_TWIST_MAP = 0.6 # Torsion strength for wide map stabilization

# =========================================================
#  UNIFIED KERNEL
# =========================================================

@njit(parallel=True, fastmath=True)
def render_iso_field_unified(center_m, center_l, width, res, src_m_arr, src_l_arr, pulse, iso_angle, contour_scale):
    """
    Unified Numba kernel for rendering both the Wide Map and the Illuminator view.
    
    Args:
        contour_scale: Factor for sin(log_amp * contour_scale) to control ring tightness.
    """
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
            
            # 1. Iso Projection
            dm = m_screen - center_m
            dl = (l_screen - center_l) * aspect
            m_world = center_m + dm
            l_world = center_l + dl

            # 2. Field Calculation (using passed source arrays)
            psi_r, psi_i = 0.0, 0.0
            
            for q in range(3):
                dx = m_world - src_m_arr[q]
                dy = l_world - src_l_arr[q]
                dist = np.sqrt(dx*dx + dy*dy) + 1e-9
                
                phase = k * dist
                amp = (SRC_AMP / dist) * pulse
                
                psi_r += amp * np.cos(phase)
                psi_i += amp * np.sin(phase)
            
            # 3. Coloring (V4 Neon)
            amp_val = np.sqrt(psi_r**2 + psi_i**2)
            phase_val = np.arctan2(psi_i, psi_r)
            
            log_amp = np.log1p(amp_val)
            
            # Contour controlled by the passed scale
            contour = 0.5 + 0.5 * np.sin(log_amp * contour_scale) 
            
            hue = (phase_val + np.pi) / (2 * np.pi)
            val = contour * np.minimum(1.0, 1.5 / (dist * 0.15 + 1.0)) # Brightness Fade
            
            # Fast RGB (Manual HSV to RGB)
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
    # Gradient of the STATIC field (Co-rotating) - No change needed
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
#  SIMULATION & ORCHESTRATION
# =========================================================

# The IsoTracker class is kept for run_illuminator logic

class IsoTracker:
    def __init__(self, start_m, start_l, zoom_level, trail_len):
        self.m = start_m
        self.l = start_l
        self.history = deque(maxlen=trail_len)
        self.zoom = zoom_level

    def project_trail(self, res, azimuth_phi):
        pts = []
        cx, cy = res/2, res/2
        scale = res / self.zoom
        aspect = np.cos(azimuth_phi)
        
        for (hm, hl) in self.history:
            dm = hm - self.m
            dl = hl - self.l
            sx = cx + dm * scale
            sy = cy + dl * scale * aspect # Screen Y
            pts.append((sx, sy))
        return pts


def run_map():
    print("--- 🗺️ WIDE-ANGLE CO-ROTATING MAP INITIATED ---")
    
    # 1. SETUP
    pm, pl = 0.0, -6.0
    vm, vl = 0.15, 0.0
    
    trail_layer = Image.new("RGBA", (PANEL_RES, PANEL_RES), (0,0,0,0))
    trail_draw = ImageDraw.Draw(trail_layer)
    last_trail_pt = None
    frames_buffer = []
    
    center_m, center_l = 0.0, 0.0
    
    for f in range(TOTAL_FRAMES):
        
        # --- A. PHYSICS STEP (CO-ROTATING FRAME with full Pseudo-Forces) ---
        pulse = 1.0 + 0.15 * np.sin(f * 0.1)
        omega = OMEGA_SYS
        
        # 1. Gradient Force (The Manifold Slope)
        gm, gl = get_gradient(pm, pl, pulse)
        force_m = gm * 0.02
        force_l = gl * 0.02
        
        # 2. Rotational Pseudo-Forces
        # Centrifugal (Pushes OUTWARD from origin)
        cen_m = (omega**2) * pm
        cen_l = (omega**2) * pl
        
        # Coriolis (Deflection)
        cor_m = 2 * omega * vl
        cor_l = -2 * omega * vm
        
        # 3. HELICAL CORRECTION: Torsion (Elastic Binding)
        # Force_twist = -kappa * omega * r
        twist_m = -KAPPA_TWIST_MAP * omega * pm
        twist_l = -KAPPA_TWIST_MAP * omega * pl
        
        # 4. Total Acceleration (SUM)
        acc_m = force_m + cor_m + cen_m + twist_m
        acc_l = force_l + cor_l + cen_l + twist_l
        
        vm += acc_m
        vl += acc_l
        
        # Friction
        vm *= DRAG_FACTOR
        vl *= DRAG_FACTOR
        
        pm += vm
        pl += vl
        
        # --- B. RENDER: WIDE-ANGLE STATIC VIEW ---
        # Co-Rotating frame: Sources are static (SRC_STRONG_M/L)
        # CONTOUR_SCALE = 20.0 for wide-angle map look
        raw_image = render_iso_field_unified(center_m, center_l, WIDE_ZOOM, PANEL_RES, 
                                             SRC_STRONG_M, SRC_STRONG_L, pulse, ISO_ANGLE, 20.0)
        
        img = Image.fromarray((raw_image * 150).astype(np.uint8)) 
        
        # --- C. UPDATE TRAIL LAYER (Persistent) ---
        scale_right = PANEL_RES / WIDE_ZOOM
        aspect = np.cos(ISO_ANGLE)
        cx, cy = PANEL_RES/2, PANEL_RES/2
        
        sx = cx + pm * scale_right
        sy = cy - (pl * scale_right * aspect) 
        
        current_pt = (sx, sy)
        
        if last_trail_pt:
            hue = (f % 100) / 100.0
            r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
            col = (int(r*255), int(g*255), int(b*255), 255)
            trail_draw.line([last_trail_pt, current_pt], fill=col, width=2)
            
        last_trail_pt = current_pt
        
        img.paste(trail_layer, (0,0), trail_layer)
        
        # --- D. DRAW HUD & PARTICLE ---
        d_img = ImageDraw.Draw(img)
        d_img.text((10, 10), "TOPOLOGY MAP [CO-ROTATING]", fill=(255, 200, 100))
        d_img.text((10, 30), f"WIDE-ANGLE ZOOM: {WIDE_ZOOM:.1f}", fill=(255, 200, 100))
        d_img.ellipse([sx-4, sy-4, sx+4, sy+4], fill=(255, 255, 255)) 

        frames_buffer.append(img)
        
        if f % 20 == 0:
            print(f"Frame {f} | P_CoRot: ({pm:.2f}, {pl:.2f})")

    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=30, loop=0)
    print("✅ WIDE-ANGLE MAP COMPLETE.")


def run_illuminator():
    print("--- 💡 HELICAL ILLUMINATOR ENGAGED ---")
    
    # Initialize Tracker at the stable point
    tracker = IsoTracker(0.0, -5.0, LEFT_ZOOM, TRAIL_LENGTH_HELIX)
    
    # Initial particle/camera position for the tethered view
    solver_m, solver_l = 0.0, -5.0
    
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = OMEGA_SYS * f # System rotation angle
        
        # --- A. PHYSICS/TETHER STEP (Camera Lock) ---
        # 1. Calculate Lab Frame source positions for the render
        c_sys, s_sys = np.cos(theta), np.sin(theta)
        rot_src_m = SRC_STRONG_M * c_sys - SRC_STRONG_L * s_sys
        rot_src_l = SRC_STRONG_M * s_sys + SRC_STRONG_L * c_sys
        
        # 2. Render the full frame centered on the previous lock (in Lab Frame)
        # Camera is following (solver_m, solver_l)
        # CONTOUR_SCALE = 25.0 for tight 'Illuminator' look
        rgb_data = render_iso_field_unified(solver_m, solver_l, tracker.zoom, PANEL_RES, 
                                            rot_src_m, rot_src_l, 1.0, ISO_ANGLE_2, 25.0)
        
        # Convert to Image and flip for PIL's coordinate system
        img_pil = Image.fromarray((rgb_data * 255).astype(np.uint8))
        img_pil = img_pil.transpose(Image.FLIP_TOP_BOTTOM) 
        
        # --- B. FIND PEAK & UPDATE CAMERA/RIBBON ---
        gray = np.mean(rgb_data, axis=2)
        mid = PANEL_RES // 2
        r = 30
        sub = gray[mid-r:mid+r, mid-r:mid+r]
        loc = np.unravel_index(np.argmax(sub), sub.shape)
        
        # Convert pixel delta to world delta
        aspect = np.cos(ISO_ANGLE_2)
        scale = tracker.zoom / PANEL_RES
        dy_px = loc[0] - r
        dx_px = loc[1] - r
        
        dm_world = dx_px * scale
        dl_world = -dy_px * scale / aspect # Flip Y back for world coords
        
        true_m = solver_m + dm_world
        true_l = solver_l + dl_world
        
        # Update Ribbon History (Lab Frame Position)
        tracker.history.append((true_m, true_l))
        
        # Move Camera (Smooth Follow/Lag)
        solver_m += (true_m - solver_m) * 0.1
        solver_l += (true_l - solver_l) * 0.1
        tracker.m = solver_m
        tracker.l = solver_l
        
        # --- C. DRAW THE HELICAL RIBBON ---
        draw = ImageDraw.Draw(img_pil)
        
        # Project history to screen coordinates
        screen_pts = tracker.project_trail(PANEL_RES, ISO_ANGLE_2)
        
        if len(screen_pts) > 2:
            for i in range(len(screen_pts) - 1):
                pt1 = screen_pts[i]
                pt2 = screen_pts[i+1]
                
                # Flip Y for PIL
                p1 = (pt1[0], PANEL_RES - pt1[1])
                p2 = (pt2[0], PANEL_RES - pt2[1])
                
                # Color Gradient (White/Yellow core)
                progress = i / len(screen_pts)
                width = int(3 * progress) + 1
                alpha = int(255 * progress)
                
                draw.line([p1, p2], fill=(255, 255, 100, alpha), width=width)

        # Draw HUD Data
        draw.text((10, 10), "VIEW: ISOMETRIC ILLUMINATOR", fill=(200, 200, 200))
        draw.text((10, 25), f"ANGLE: {ISO_ANGLE_2*57.29:.1f}°", fill=(200, 200, 200))
        draw.text((10, 40), f"HELICITY LOCK: ON", fill=(0, 255, 100))

        frames_buffer.append(img_pil)
        
        if f % 20 == 0:
            print(f"Frame {f} | Camera: ({solver_m:.2f}, {solver_l:.2f})")

    # The crucial fix: use OUTPUT_FILENAME_2 here!
    print(f"Saving {OUTPUT_FILENAME_2}...") 
    frames_buffer[0].save(OUTPUT_FILENAME_2, save_all=True, append_images=frames_buffer[1:], duration=40, loop=0)
    print("✅ MANIFOLD ILLUMINATED.")

if __name__ == "__main__":
    run_map()
    run_illuminator()