import numpy as np
from numba import njit, prange
from PIL import Image, ImageDraw
from collections import deque
import colorsys

# =========================================================
#  PIROUETTE: UNIFIED RENDERER (GEMINI V5 Refactored)
# =========================================================

# --- CONFIG ---
OUTPUT_FILENAME_COMBINED = "combined_precession_view.gif"
TOTAL_FRAMES = 450
PANEL_RES = 400

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
TRAIL_LENGTH_MAP = TOTAL_FRAMES # Set to max length for full precession trail
DRAG_FACTOR = 0.995    # Slightly increased friction for co-rot map

# HELICAL ILLUMINATOR DYNAMICS (for run_illuminator)
TRAIL_LENGTH_HELIX = 25 # Shorter trail for the ribbon
ISO_ANGLE_2 = 0.85
KAPPA_TWIST_MAP = 0.6 # Torsion strength for wide map stabilization

# =========================================================
#  UNIFIED KERNEL (No change needed)
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

class IsoTracker:
    def __init__(self, start_m, start_l, zoom_level, trail_len):
        self.m = start_m
        self.l = start_l
        self.history = deque(maxlen=trail_len)
        self.zoom = zoom_level

    def project_trail(self, res, azimuth_phi, center_m, center_l):
        pts = []
        cx, cy = res/2, res/2
        scale = res / self.zoom
        aspect = np.cos(azimuth_phi)
        
        # Project relative to the current center_m/l
        for (hm, hl) in self.history:
            dm = hm - center_m
            dl = hl - center_l
            sx = cx + dm * scale
            sy = cy - (dl * scale * aspect) # Invert Y for screen coords
            pts.append((sx, sy))
        return pts


def simulate_wide_trail():
    """Simulates the particle path and returns the full history."""
    print("--- 🔬 WIDE-ANGLE TRAIL SIMULATION INITIATED ---")
    
    pm, pl = 0.0, -6.0
    vm, vl = 0.15, 0.0
    history = []
    
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
        twist_m = -KAPPA_TWIST_MAP * omega * pm
        twist_l = -KAPPA_TWIST_MAP * omega * pl
        
        # 4. Total Acceleration (SUM)
        acc_m = force_m + cor_m + cen_m + twist_m
        acc_l = force_l + cor_l + twist_l # cor_l is -2*omega*vm
        
        vm += acc_m
        vl += acc_l
        
        # Friction
        vm *= DRAG_FACTOR
        vl *= DRAG_FACTOR
        
        pm += vm
        pl += vl
        
        history.append((pm, pl))
        
        if f % 50 == 0:
            print(f"Simulation Frame {f} | P_CoRot: ({pm:.2f}, {pl:.2f})")

    print("✅ SIMULATION COMPLETE.")
    return history


def render_map_frame(frame_index, trail_history):
    """Renders a single wide-angle frame, centered on the current particle position."""
    
    # Current particle position is the center of the view
    center_m, center_l = trail_history[frame_index]
    
    # Pulse is re-calculated for consistency
    pulse = 1.0 + 0.15 * np.sin(frame_index * 0.1)

    # RENDER: WIDE-ANGLE STATIC VIEW, centered on the particle
    # Co-Rotating frame: Sources are static (SRC_STRONG_M/L)
    raw_image = render_iso_field_unified(center_m, center_l, WIDE_ZOOM, PANEL_RES, 
                                         SRC_STRONG_M, SRC_STRONG_L, pulse, ISO_ANGLE, 20.0)
    
    img = Image.fromarray((raw_image * 150).astype(np.uint8)).convert("RGB")
    draw = ImageDraw.Draw(img)

    # --- DRAW THE FULL PRECESSSION TRAIL ---
    cx, cy = PANEL_RES/2, PANEL_RES/2
    scale = PANEL_RES / WIDE_ZOOM
    aspect = np.cos(ISO_ANGLE)
    
    # Only use history up to the current frame index
    current_history = trail_history[:frame_index + 1]
    
    for i in range(len(current_history) - 1):
        # Coordinates relative to the center_m/l
        (m1, l1) = current_history[i]
        (m2, l2) = current_history[i+1]
        
        # Project 1st point
        sx1 = cx + (m1 - center_m) * scale
        sy1 = cy - ((l1 - center_l) * scale * aspect) 
        p1 = (sx1, sy1)
        
        # Project 2nd point
        sx2 = cx + (m2 - center_m) * scale
        sy2 = cy - ((l2 - center_l) * scale * aspect) 
        p2 = (sx2, sy2)
        
        # Color gradient based on age (fade old parts)
        progress = i / len(trail_history) # Max length is TOTAL_FRAMES
        hue = (i % 100) / 100.0
        r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
        
        # Fading trail effect
        alpha = int(255 * (0.5 + 0.5 * progress))
        col = (int(r*255), int(g*255), int(b*255), alpha)
        
        # Create a temporary overlay to draw a line with transparency
        line_overlay = Image.new("RGBA", img.size, (0,0,0,0))
        line_draw = ImageDraw.Draw(line_overlay)
        line_draw.line([p1, p2], fill=col, width=2)
        img.paste(line_overlay, (0,0), line_overlay)

    # Draw Current Particle (Center of screen)
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(255, 255, 255)) 

    # Draw HUD
    draw.text((10, 10), "MANIFOLD PRECESSION TRACE", fill=(255, 200, 100))
    draw.text((10, 30), f"Center P_CoRot: ({center_m:.2f}, {center_l:.2f})", fill=(255, 200, 100))

    return img


def run_illuminator_frames():
    """Runs the illuminator simulation and returns a list of rendered frames."""
    print("--- 💡 HELICAL ILLUMINATOR ENGAGED (Frames Generation) ---")
    
    tracker = IsoTracker(0.0, -5.0, LEFT_ZOOM, TRAIL_LENGTH_HELIX)
    solver_m, solver_l = 0.0, -5.0
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = OMEGA_SYS * f 
        
        # --- A. PHYSICS/TETHER STEP (Camera Lock) ---
        c_sys, s_sys = np.cos(theta), np.sin(theta)
        rot_src_m = SRC_STRONG_M * c_sys - SRC_STRONG_L * s_sys
        rot_src_l = SRC_STRONG_M * s_sys + SRC_STRONG_L * c_sys
        
        # RENDER: Centered on the previous lock (in Lab Frame)
        rgb_data = render_iso_field_unified(solver_m, solver_l, tracker.zoom, PANEL_RES, 
                                            rot_src_m, rot_src_l, 1.0, ISO_ANGLE_2, 25.0)
        
        img_pil = Image.fromarray((rgb_data * 255).astype(np.uint8)).convert("RGB")
        img_pil = img_pil.transpose(Image.FLIP_TOP_BOTTOM) 
        
        # --- B. FIND PEAK & UPDATE CAMERA/RIBBON ---
        gray = np.mean(rgb_data, axis=2)
        mid = PANEL_RES // 2
        r = 30
        sub = gray[mid-r:mid+r, mid-r:mid+r]
        loc = np.unravel_index(np.argmax(sub), sub.shape)
        
        aspect = np.cos(ISO_ANGLE_2)
        scale = tracker.zoom / PANEL_RES
        dy_px = loc[0] - r
        dx_px = loc[1] - r
        
        dm_world = dx_px * scale
        dl_world = -dy_px * scale / aspect
        
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
        screen_pts = tracker.project_trail(PANEL_RES, ISO_ANGLE_2, tracker.m, tracker.l)
        
        if len(screen_pts) > 2:
            for i in range(len(screen_pts) - 1):
                pt1 = screen_pts[i]
                pt2 = screen_pts[i+1]
                
                # Flip Y for PIL
                p1 = (pt1[0], PANEL_RES - pt1[1])
                p2 = (pt2[0], PANEL_RES - pt2[1])
                
                # Color Gradient 
                progress = i / TRAIL_LENGTH_HELIX
                width = int(3 * progress) + 1
                alpha = int(255 * progress)
                
                line_overlay = Image.new("RGBA", img_pil.size, (0,0,0,0))
                line_draw = ImageDraw.Draw(line_overlay)
                line_draw.line([p1, p2], fill=(255, 255, 100, alpha), width=width)
                img_pil.paste(line_overlay, (0,0), line_overlay)

        # Draw HUD Data
        draw.text((10, 10), "VIEW: ISOMETRIC ILLUMINATOR", fill=(200, 200, 200))
        draw.text((10, 25), f"Camera P_Lab: ({solver_m:.2f}, {solver_l:.2f})", fill=(200, 200, 200))
        draw.text((10, 40), f"HELICITY LOCK: ON", fill=(0, 255, 100))

        frames_buffer.append(img_pil)
        
        if f % 50 == 0:
            print(f"Illuminator Frame {f} Generated.")

    print("✅ ILLUMINATOR FRAMES COMPLETE.")
    return frames_buffer

def combine_and_save():
    """Executes the simulation, renders both views, and combines them into one GIF."""
    
    # 1. Run Simulation and get the full path
    wide_trail_history = simulate_wide_trail()
    
    # 2. Render Illuminator Frames
    illuminator_frames = run_illuminator_frames()
    
    print("--- 🎬 COMBINING VIEWS ---")
    
    combined_frames = []
    
    for f in range(TOTAL_FRAMES):
        
        # 3. Render the Wide Map Frame, centered on the current position
        map_frame = render_map_frame(f, wide_trail_history)
        
        # 4. Get the corresponding Illuminator Frame
        illuminator_frame = illuminator_frames[f]
        
        # 5. Create a new image for the two panels side-by-side
        combined_img = Image.new('RGB', (PANEL_RES * 2, PANEL_RES))
        combined_img.paste(map_frame, (0, 0))
        combined_img.paste(illuminator_frame, (PANEL_RES, 0))
        
        # 6. Add a visual separator line
        draw_combined = ImageDraw.Draw(combined_img)
        draw_combined.line([(PANEL_RES, 0), (PANEL_RES, PANEL_RES)], fill=(100, 100, 100), width=2)
        
        combined_frames.append(combined_img)
        
        if f % 50 == 0:
            print(f"Combined Frame {f}/{TOTAL_FRAMES}")

    # 7. Save the final combined GIF
    print(f"Saving {OUTPUT_FILENAME_COMBINED}...")
    if combined_frames:
        combined_frames[0].save(OUTPUT_FILENAME_COMBINED, 
                                save_all=True, 
                                append_images=combined_frames[1:], 
                                duration=30, 
                                loop=0)
    print(f"✅ COMBINED RENDER COMPLETE: {OUTPUT_FILENAME_COMBINED}")


if __name__ == "__main__":
    combine_and_save()