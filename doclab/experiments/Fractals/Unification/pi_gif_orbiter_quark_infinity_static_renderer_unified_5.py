import numpy as np
from PIL import Image, ImageDraw
from collections import deque
import colorsys

# =========================================================
#  PIROUETTE: UNIFIED RENDERER (GEMINI V6 Refactored - Pure NumPy)
# =========================================================

# --- CONFIG ---
OUTPUT_FILENAME_COMBINED = "triple_precession_view.gif"
TOTAL_FRAMES = 450
PANEL_RES = 600

# OPTIMIZATION
FRAME_SKIP = 3              # Render only every Nth frame
RENDER_DURATION_MS = 90     # Set frame duration to 90ms (approx 11 FPS)
WIRE_PANEL_WIDTH = 120      # Width of the new wireframe panel

# VIEW SETTINGS
ISO_ANGLE = 0.85       
WIDE_ZOOM = 150.0      
LEFT_ZOOM = 14.0       

# PHYSICS CONSTANTS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0
OMEGA_SYS = 0.05       

# DYNAMICS
TRAIL_LENGTH_MAP = TOTAL_FRAMES 
DRAG_FACTOR = 0.995    
TRAIL_LENGTH_HELIX = 25 
ISO_ANGLE_2 = 0.85
KAPPA_TWIST_MAP = 0.6 

# =========================================================
#  UNIFIED KERNEL (Rewritten for Pure NumPy)
# =========================================================

def render_iso_field_unified(center_m, center_l, width, res, src_m_arr, src_l_arr, pulse, iso_angle, contour_scale):
    """NumPy implementation for rendering the field."""
    
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    # Create the coordinate grid (m_world, l_world)
    m_screen, l_screen = np.meshgrid(m_vals, l_vals)
    
    # 1. Iso Projection
    dm = m_screen - center_m
    aspect = 1.0 / np.cos(iso_angle)
    dl = (l_screen - center_l) * aspect
    
    m_world = center_m + dm
    l_world = center_l + dl
    
    # Reshape for broadcasting
    M = m_world.flatten()[:, None]
    L = l_world.flatten()[:, None]
    
    SRC_M = src_m_arr[None, :]
    SRC_L = src_l_arr[None, :]
    
    # 2. Field Calculation (Vectorized over all grid points and all sources)
    dx = M - SRC_M
    dy = L - SRC_L
    dist = np.sqrt(dx*dx + dy*dy) + 1e-9
    
    k = (2 * np.pi) / 10.0
    phase = k * dist
    amp = (SRC_AMP / dist) * pulse
    
    psi_r = np.sum(amp * np.cos(phase), axis=1)
    psi_i = np.sum(amp * np.sin(phase), axis=1)
    
    # 3. Coloring 
    amp_val = np.sqrt(psi_r**2 + psi_i**2)
    phase_val = np.arctan2(psi_i, psi_r)
    
    log_amp = np.log1p(amp_val)
    contour = 0.5 + 0.5 * np.sin(log_amp * contour_scale) 
    
    hue = (phase_val + np.pi) / (2 * np.pi)
    min_dist = np.min(dist, axis=1)
    val = contour * np.minimum(1.0, 1.5 / (min_dist * 0.15 + 1.0))
    
    # --- Convert HSV to RGB (Vectorized Numba Logic Replication) ---
    h6 = hue * 6.0
    x = (1.0 - np.abs(np.remainder(h6, 2.0) - 1.0))
    
    # Use np.select to implement the cascading if/elif logic
    r = np.select([h6 < 1, h6 < 2, h6 < 3, h6 < 4, h6 < 5, h6 >= 5], [1.0, x, 0.0, 0.0, x, 1.0])
    g = np.select([h6 < 1, h6 < 2, h6 < 3, h6 < 4, h6 < 5, h6 >= 5], [x, 1.0, 1.0, x, 0.0, 0.0])
    b = np.select([h6 < 1, h6 < 2, h6 < 3, h6 < 4, h6 < 5, h6 >= 5], [0.0, 0.0, x, 1.0, 1.0, x])
    
    # Final color scaled by 'val'
    r_final = r * val
    g_final = g * val
    b_final = b * val
    
    # Reshape back to (res, res, 3) 
    # Transpose needed to account for np.meshgrid/flatten order vs image order
    r_reshaped = r_final.reshape(res, res).T
    g_reshaped = g_final.reshape(res, res).T
    b_reshaped = b_final.reshape(res, res).T
    
    img_out = np.stack([r_reshaped, g_reshaped, b_reshaped], axis=2)

    return img_out

def get_gradient(m, l, pulse):
    """Calculates the gradient of the static field for the co-rotating frame (Pure NumPy)."""
    eps = 0.01
    
    def val(tm, tl):
        # Sources are STATIC in this frame
        dx = tm - SRC_STRONG_M
        dy = tl - SRC_STRONG_L
        
        d = np.sqrt(dx**2 + dy**2) + 1e-9
        ph = (2*np.pi)/10.0 * d
        
        # Note: SRC_AMP is a scalar and the constant pulse is applied here
        a = (SRC_AMP/d) * pulse
        
        pr = np.sum(a*np.cos(ph))
        pi = np.sum(a*np.sin(ph))
        
        return pr**2 + pi**2
    
    v0 = val(m, l)
    gm = (val(m+eps, l) - v0)/eps
    gl = (val(m, l+eps) - v0)/eps
    return gm, gl

# =========================================================
#  SIMULATION & ORCHESTRATION (Rest of the code)
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
        
        for (hm, hl) in self.history:
            dm = hm - center_m
            dl = hl - center_l
            sx = cx + dm * scale
            sy = cy - (dl * scale * aspect) 
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
        cen_m = (omega**2) * pm
        cen_l = (omega**2) * pl
        cor_m = 2 * omega * vl
        cor_l = -2 * omega * vm
        
        # 3. HELICAL CORRECTION: Torsion
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
        
        history.append((pm, pl))
        
        if f % 50 == 0:
            print(f"Simulation Frame {f} | P_CoRot: ({pm:.2f}, {pl:.2f})")

    print("✅ SIMULATION COMPLETE.")
    return history


def draw_precession_trail(draw_target, current_history, full_history_len, center_m, center_l, res_x, res_y, zoom, angle):
    """Helper function to draw the precession trail on any canvas."""
    
    cx, cy = res_x / 2.0, res_y / 2.0
    scale = res_y / zoom # Use height for scale consistency
    aspect = np.cos(angle)
    
    # 1. Create a single transparent overlay for all lines
    trail_overlay = Image.new("RGBA", (res_x, res_y), (0,0,0,0))
    trail_draw = ImageDraw.Draw(trail_overlay)
    
    # 2. Draw all trail segments onto the overlay
    for i in range(len(current_history) - 1):
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
        progress = i / full_history_len 
        hue = (i % 100) / 100.0
        r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
        
        alpha = int(255 * (0.5 + 0.5 * progress))
        col = (int(r*255), int(g*255), int(b*255), alpha)
        
        trail_draw.line([p1, p2], fill=col, width=2)

    # 3. Paste the trail overlay onto the target image
    draw_target.paste(trail_overlay, (0,0), trail_overlay)

    # 4. Draw the Current Particle (FIX: Use ImageDraw object on the target image)
    draw = ImageDraw.Draw(draw_target)
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(255, 255, 255)) 


def render_map_frame(frame_index, trail_history):
    """Renders the wide-angle field centered on the current particle position."""
    
    center_m, center_l = trail_history[frame_index]
    pulse = 1.0 + 0.15 * np.sin(frame_index * 0.1)

    # RENDER: WIDE-ANGLE STATIC VIEW, centered on the particle
    raw_image = render_iso_field_unified(center_m, center_l, WIDE_ZOOM, PANEL_RES, 
                                         SRC_STRONG_M, SRC_STRONG_L, pulse, ISO_ANGLE, 20.0)
    
    img = Image.fromarray((raw_image * 150).astype(np.uint8)).convert("RGB")
    
    # --- DRAW THE FULL PRECESSION TRAIL ---
    current_history = trail_history[:frame_index + 1]
    draw_precession_trail(img, current_history, TOTAL_FRAMES, center_m, center_l, PANEL_RES, PANEL_RES, WIDE_ZOOM, ISO_ANGLE)

    # Draw HUD
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "MANIFOLD PRECESSION TRACE", fill=(255, 200, 100))
    draw.text((10, 30), f"Center P_CoRot: ({center_m:.2f}, {center_l:.2f})", fill=(255, 200, 100))

    return img


def render_wireframe_panel(frame_index, trail_history):
    """Renders only the trail on a narrow panel, centered on the current particle position."""
    
    center_m, center_l = trail_history[frame_index]
    
    # Create the black background image
    img = Image.new('RGB', (WIRE_PANEL_WIDTH, PANEL_RES), (0, 0, 0))
    
    # Draw center line for orientation
    draw = ImageDraw.Draw(img)
    cx_wire = WIRE_PANEL_WIDTH / 2.0
    draw.line([(cx_wire, 0), (cx_wire, PANEL_RES)], fill=(50, 50, 50), width=1)
    
    # Use the same projection logic as the wide map, but draw on the narrow panel
    current_history = trail_history[:frame_index + 1]
    draw_precession_trail(img, current_history, TOTAL_FRAMES, center_m, center_l, WIRE_PANEL_WIDTH, PANEL_RES, WIDE_ZOOM, ISO_ANGLE)
    
    # Draw HUD
    draw.text((5, 10), "WIRE", fill=(100, 100, 255))
    draw.text((5, 25), "TRACE", fill=(100, 100, 255))

    return img.convert("RGB")


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
        
        # Ensure slicing is safe
        r_start = max(0, mid-r)
        r_end = min(PANEL_RES, mid+r)
        c_start = max(0, mid-r)
        c_end = min(PANEL_RES, mid+r)

        sub = gray[r_start:r_end, c_start:c_end]
        
        if sub.size == 0:
            loc = (r, r) # Default to center if area is invalid
        else:
            loc = np.unravel_index(np.argmax(sub), sub.shape)
        
        # Convert pixel delta to world delta
        aspect = np.cos(ISO_ANGLE_2)
        scale = tracker.zoom / PANEL_RES
        dy_px = (loc[0] + r_start) - mid
        dx_px = (loc[1] + c_start) - mid
        
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
            # Create a single transparent overlay for the ribbon lines
            ribbon_overlay = Image.new("RGBA", img_pil.size, (0,0,0,0))
            ribbon_draw = ImageDraw.Draw(ribbon_overlay)
            
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
                
                ribbon_draw.line([p1, p2], fill=(255, 255, 100, alpha), width=width)
            
            img_pil.paste(ribbon_overlay, (0,0), ribbon_overlay)


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
    """Executes the simulation, renders all views, and combines them into one GIF."""
    
    # 1. Run Simulation and get the full path
    wide_trail_history = simulate_wide_trail()
    
    # 2. Render Illuminator Frames (need all of them)
    illuminator_frames = run_illuminator_frames()
    
    print("--- 🎬 COMBINING VIEWS ---")
    
    combined_frames = []
    
    TOTAL_WIDTH = PANEL_RES * 2 + WIRE_PANEL_WIDTH # 600 + 600 + 120 = 1320
    
    for f in range(TOTAL_FRAMES):
        
        # Skip rendering based on optimization constant
        if f % FRAME_SKIP != 0:
            continue
            
        # 3. Render the Wide Map Frame
        map_frame = render_map_frame(f, wide_trail_history)
        
        # 4. Render the Wireframe Panel
        wire_frame = render_wireframe_panel(f, wide_trail_history)
        
        # 5. Get the corresponding Illuminator Frame
        illuminator_frame = illuminator_frames[f]
        
        # 6. Create a new image for the three panels side-by-side
        combined_img = Image.new('RGB', (TOTAL_WIDTH, PANEL_RES))
        
        # Paste panels in order
        combined_img.paste(map_frame, (0, 0))
        combined_img.paste(illuminator_frame, (PANEL_RES, 0))
        combined_img.paste(wire_frame, (PANEL_RES * 2, 0))
        
        # 7. Add visual separator lines
        draw_combined = ImageDraw.Draw(combined_img)
        draw_combined.line([(PANEL_RES, 0), (PANEL_RES, PANEL_RES)], fill=(100, 100, 100), width=2)
        draw_combined.line([(PANEL_RES * 2, 0), (PANEL_RES * 2, PANEL_RES)], fill=(100, 100, 100), width=2)
        
        combined_frames.append(combined_img)
        
        if f % (50 * FRAME_SKIP) == 0:
            print(f"Combined Frame {f}/{TOTAL_FRAMES}")

    # 8. Save the final combined GIF
    print(f"Saving {OUTPUT_FILENAME_COMBINED}...")
    if combined_frames:
        combined_frames[0].save(OUTPUT_FILENAME_COMBINED, 
                                save_all=True, 
                                append_images=combined_frames[1:], 
                                duration=RENDER_DURATION_MS, 
                                loop=0)
    print(f"✅ COMBINED RENDER COMPLETE: {OUTPUT_FILENAME_COMBINED}")


if __name__ == "__main__":
    combine_and_save()