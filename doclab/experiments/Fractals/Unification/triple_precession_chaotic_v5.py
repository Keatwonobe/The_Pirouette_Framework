import numpy as np
from PIL import Image, ImageDraw
from collections import deque
import colorsys

# =========================================================
#  PIROUETTE: UNIFIED RENDERER (GEMINI V6 REFACTORED V5 - CHAOTIC START)
# =========================================================

# --- CONFIG ---
OUTPUT_FILENAME_COMBINED = "triple_precession_chaotic_v5.gif"
TOTAL_FRAMES = 600 # Increased frames for longer chaotic trace
PANEL_RES = 600

# OPTIMIZATION
FRAME_SKIP = 3              
RENDER_DURATION_MS = 90     
WIRE_PANEL_WIDTH = 300      
WIRE_STRIP_WIDTH = 100

# VIEW SETTINGS
ISO_ANGLE = 0.85       
WIDE_ZOOM = 180.0      
LEFT_ZOOM = 14.0       

# PHYSICS CONSTANTS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0
OMEGA_SYS = 0.06       # Slightly increased Omega for stronger Coriolis/Centrifugal effects

# DYNAMICS
TRAIL_LENGTH_MAP = TOTAL_FRAMES 
DRAG_FACTOR = 0.995    
TRAIL_LENGTH_HELIX = 25 
ISO_ANGLE_2 = 0.85
KAPPA_TWIST_MAP = 0.7 # Increased twist factor to promote chaotic separation

# PARTICLE COLORS for Wireframe Panels & Map
P1_COLOR = (255, 255, 255) # White on Map
P2_COLOR = (100, 255, 100) # Greenish
P3_COLOR = (100, 100, 255) # Bluish

# =========================================================
#  UNIFIED KERNEL (Rewritten for Pure NumPy)
# =========================================================

def render_iso_field_unified(center_m, center_l, width, res, src_m_arr, src_l_arr, pulse, iso_angle, contour_scale):
    """NumPy implementation for rendering the field."""
    
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
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
    
    # --- Convert HSV to RGB ---
    h6 = hue * 6.0
    x = (1.0 - np.abs(np.remainder(h6, 2.0) - 1.0))
    
    r = np.select([h6 < 1, h6 < 2, h6 < 3, h6 < 4, h6 < 5, h6 >= 5], [1.0, x, 0.0, 0.0, x, 1.0])
    g = np.select([h6 < 1, h6 < 2, h6 < 3, h6 < 4, h6 < 5, h6 >= 5], [x, 1.0, 1.0, x, 0.0, 0.0])
    b = np.select([h6 < 1, h6 < 2, h6 < 3, h6 < 4, h6 < 5, h6 >= 5], [0.0, 0.0, x, 1.0, 1.0, x])
    
    r_final = r * val
    g_final = g * val
    b_final = b * val
    
    r_reshaped = r_final.reshape(res, res)
    g_reshaped = g_final.reshape(res, res)
    b_reshaped = b_final.reshape(res, res)
    
    img_out = np.stack([r_reshaped, g_reshaped, b_reshaped], axis=2)

    return img_out

def get_gradient(m, l, pulse):
    """Calculates the gradient of the static field for the co-rotating frame (Pure NumPy)."""
    eps = 0.01
    
    def val(tm, tl):
        dx = tm - SRC_STRONG_M
        dy = tl - SRC_STRONG_L
        d = np.sqrt(dx**2 + dy**2) + 1e-9
        ph = (2*np.pi)/10.0 * d
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

class ThreeQuarkSimulator:
    """Manages the state and history for three independent particles (Quarks)."""
    def __init__(self):
        # NEW: Highly unstable, slightly offset triangular start near origin (0, 0)
        # This region tends to be unstable, promoting chaotic motion across wells.
        
        # Center point near (0, 0) is unstable.
        center_m_start = 0.0
        center_l_start = 0.0
        r_offset = 2.0 # Radius of the initial triangle
        
        # P1 (White) - Up/Right
        self.p1_m, self.p1_l = center_m_start + r_offset * np.cos(np.pi/6), center_l_start + r_offset * np.sin(np.pi/6)
        self.p1_vm, self.p1_vl = 0.1, 0.0
        self.history_1 = []
        
        # P2 (Green) - Down/Left
        self.p2_m, self.p2_l = center_m_start + r_offset * np.cos(5*np.pi/6), center_l_start + r_offset * np.sin(5*np.pi/6) 
        self.p2_vm, self.p2_vl = -0.1, 0.0
        self.history_2 = []
        
        # P3 (Blue) - Down/Right
        self.p3_m, self.p3_l = center_m_start + r_offset * np.cos(9*np.pi/6), center_l_start + r_offset * np.sin(9*np.pi/6)
        self.p3_vm, self.p3_vl = 0.0, 0.1
        self.history_3 = []
    
    def simulate_step(self, m, l, vm, vl, f):
        pulse = 1.0 + 0.15 * np.sin(f * 0.1)
        omega = OMEGA_SYS
        
        gm, gl = get_gradient(m, l, pulse)
        force_m = gm * 0.02
        force_l = gl * 0.02
        
        cen_m = (omega**2) * m
        cen_l = (omega**2) * l
        cor_m = 2 * omega * vl
        cor_l = -2 * omega * vm
        
        twist_m = -KAPPA_TWIST_MAP * omega * m
        twist_l = -KAPPA_TWIST_MAP * omega * l
        
        acc_m = force_m + cor_m + cen_m + twist_m
        acc_l = force_l + cor_l + cen_l + twist_l
        
        vm += acc_m
        vl += acc_l
        
        vm *= DRAG_FACTOR
        vl *= DRAG_FACTOR
        
        m += vm
        l += vl
        
        return m, l, vm, vl

    def simulate_all(self):
        """Simulates the path for all three particles."""
        print("--- 🔬 THREE-QUARK TRAIL SIMULATION INITIATED (CHAOTIC) ---")
        
        for f in range(TOTAL_FRAMES):
            self.p1_m, self.p1_l, self.p1_vm, self.p1_vl = self.simulate_step(self.p1_m, self.p1_l, self.p1_vm, self.p1_vl, f)
            self.history_1.append((self.p1_m, self.p1_l))
            
            self.p2_m, self.p2_l, self.p2_vm, self.p2_vl = self.simulate_step(self.p2_m, self.p2_l, self.p2_vm, self.p2_vl, f)
            self.history_2.append((self.p2_m, self.p2_l))

            self.p3_m, self.p3_l, self.p3_vm, self.p3_vl = self.simulate_step(self.p3_m, self.p3_l, self.p3_vm, self.p3_vl, f)
            self.history_3.append((self.p3_m, self.p3_l))
            
            if f % 50 == 0:
                print(f"Simulation Frame {f} | P1: ({self.p1_m:.2f}, {self.p1_l:.2f})")

        print("✅ SIMULATION COMPLETE.")
        return self.history_1, self.history_2, self.history_3

def draw_precession_trail(draw_target, current_history, full_history_len, center_m, center_l, res_x, res_y, zoom, angle, trail_color, current_p_color, draw_line_gradient=False):
    """
    Helper function to draw the precession trail on any canvas.
    trail_color is an (R,G,B) tuple for the trail lines.
    current_p_color is an (R,G,B) tuple for the current particle.
    """
    
    cx, cy = res_x / 2.0, res_y / 2.0
    scale = res_y / zoom 
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
        
        # Color gradient based on age (fade old parts) - only for the WIDE MAP, P1 only
        if draw_line_gradient:
            progress = i / full_history_len 
            hue = (i % 100) / 100.0
            r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
            alpha = int(255 * (0.5 + 0.5 * progress))
            col = (int(r*255), int(g*255), int(b*255), alpha)
        else: # For other particles/wireframe, use a consistent color
            progress = i / full_history_len 
            alpha = int(255 * (0.1 + 0.9 * progress)) 
            col = (trail_color[0], trail_color[1], trail_color[2], alpha)
        
        trail_draw.line([p1, p2], fill=col, width=2)

    # 3. Paste the trail overlay onto the target image
    draw_target.paste(trail_overlay, (0,0), trail_overlay)

    # 4. Draw the Current Particle 
    draw = ImageDraw.Draw(draw_target)
    
    # Project current particle position (last point in history)
    if current_history:
        (m_curr, l_curr) = current_history[-1]
        dm = m_curr - center_m
        dl = l_curr - center_l
        sx = cx + dm * scale
        sy = cy - (dl * scale * aspect)
        
        # Draw the particle as a small dot/ellipse
        radius = 4
        draw.ellipse([sx-radius, sy-radius, sx+radius, sy+radius], fill=current_p_color) 


def render_map_frame(frame_index, histories):
    """
    Renders the wide-angle field centered on the CENTER OF MASS (COM), 
    and draws the trails of P1, P2, and P3.
    """
    
    P1_history, P2_history, P3_history = histories
    
    # Calculate Center of Mass (COM)
    p1_m, p1_l = P1_history[frame_index]
    p2_m, p2_l = P2_history[frame_index]
    p3_m, p3_l = P3_history[frame_index]
    
    # Assuming equal mass (m1=m2=m3=1)
    center_m = (p1_m + p2_m + p3_m) / 3.0
    center_l = (p1_l + p2_l + p3_l) / 3.0
    
    pulse = 1.0 + 0.15 * np.sin(frame_index * 0.1)

    # RENDER: WIDE-ANGLE STATIC VIEW, centered on the COM
    raw_image = render_iso_field_unified(center_m, center_l, WIDE_ZOOM, PANEL_RES, 
                                         SRC_STRONG_M, SRC_STRONG_L, pulse, ISO_ANGLE, 20.0)
    
    img = Image.fromarray((raw_image * 255).astype(np.uint8)).convert("RGB")
    
    # --- DRAW THE FULL PRECESSION TRAILS (All 3) ---
    
    # 1. Draw P1's trail (The original colored gradient trail)
    current_history_p1 = P1_history[:frame_index + 1]
    # Keep P1's line gradient for visual interest on the map, but use the COM center
    draw_precession_trail(img, current_history_p1, TOTAL_FRAMES, center_m, center_l, 
                          PANEL_RES, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, 
                          (255, 255, 255), P1_COLOR, draw_line_gradient=True)

    # 2. Draw P2's trail (Green/Cyan trail)
    current_history_p2 = P2_history[:frame_index + 1]
    # Set trail color to a dimmer version of P2_COLOR for contrast
    dim_p2 = (P2_COLOR[0]//2, P2_COLOR[1]//2, P2_COLOR[2]//2)
    draw_precession_trail(img, current_history_p2, TOTAL_FRAMES, center_m, center_l, 
                          PANEL_RES, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, 
                          dim_p2, P2_COLOR, draw_line_gradient=False)

    # 3. Draw P3's trail (Blue/Magenta trail)
    current_history_p3 = P3_history[:frame_index + 1]
    # Set trail color to a dimmer version of P3_COLOR for contrast
    dim_p3 = (P3_COLOR[0]//2, P3_COLOR[1]//2, P3_COLOR[2]//2)
    draw_precession_trail(img, current_history_p3, TOTAL_FRAMES, center_m, center_l, 
                          PANEL_RES, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, 
                          dim_p3, P3_COLOR, draw_line_gradient=False)

    # Draw HUD
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "MANIFOLD PRECESSION TRACE (COM-CENTERED)", fill=(255, 200, 100))
    draw.text((10, 30), f"Center of Mass CoRot: ({center_m:.2f}, {center_l:.2f})", fill=(255, 200, 100))
    draw.text((10, 50), "P1 (White), P2 (Green), P3 (Blue)", fill=(255, 255, 255))

    return img


def render_wireframe_panel(frame_index, histories):
    """Renders all three quark trails on the narrow panel."""
    
    P1_history, P2_history, P3_history = histories
    
    img = Image.new('RGB', (WIRE_PANEL_WIDTH, PANEL_RES), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Wireframe panels remain centered on P1's path for comparison to the Illuminator
    center_m, center_l = P1_history[frame_index] 
    
    # --- 1. RENDER P1 (Leftmost Strip) ---
    strip_offset = WIRE_STRIP_WIDTH * 0 
    p1_canvas = Image.new('RGB', (WIRE_STRIP_WIDTH, PANEL_RES), (0, 0, 0))
    
    current_history = P1_history[:frame_index + 1]
    draw_precession_trail(p1_canvas, current_history, TOTAL_FRAMES, center_m, center_l, 
                          WIRE_STRIP_WIDTH, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, 
                          (180, 180, 180), P1_COLOR, draw_line_gradient=False)
    
    draw_p1 = ImageDraw.Draw(p1_canvas)
    draw_p1.line([(WIRE_STRIP_WIDTH / 2.0, 0), (WIRE_STRIP_WIDTH / 2.0, PANEL_RES)], fill=(50, 50, 50), width=1)
    draw_p1.text((5, 10), "P1", fill=(255, 255, 255))
    img.paste(p1_canvas, (strip_offset, 0))
    
    # --- 2. RENDER P2 (Middle Strip) ---
    strip_offset = WIRE_STRIP_WIDTH * 1 
    p2_canvas = Image.new('RGB', (WIRE_STRIP_WIDTH, PANEL_RES), (0, 0, 0))
    
    current_history = P2_history[:frame_index + 1]
    draw_precession_trail(p2_canvas, current_history, TOTAL_FRAMES, center_m, center_l, 
                          WIRE_STRIP_WIDTH, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, 
                          (0, 200, 0), P2_COLOR, draw_line_gradient=False)
    
    draw_p2 = ImageDraw.Draw(p2_canvas)
    draw_p2.line([(WIRE_STRIP_WIDTH / 2.0, 0), (WIRE_STRIP_WIDTH / 2.0, PANEL_RES)], fill=(50, 50, 50), width=1)
    draw_p2.text((5, 10), "P2", fill=(150, 255, 150))
    img.paste(p2_canvas, (strip_offset, 0))

    # --- 3. RENDER P3 (Rightmost Strip) ---
    strip_offset = WIRE_STRIP_WIDTH * 2 
    p3_canvas = Image.new('RGB', (WIRE_STRIP_WIDTH, PANEL_RES), (0, 0, 0))
    
    current_history = P3_history[:frame_index + 1]
    draw_precession_trail(p3_canvas, current_history, TOTAL_FRAMES, center_m, center_l, 
                          WIRE_STRIP_WIDTH, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, 
                          (0, 0, 200), P3_COLOR, draw_line_gradient=False)
    
    draw_p3 = ImageDraw.Draw(p3_canvas)
    draw_p3.line([(WIRE_STRIP_WIDTH / 2.0, 0), (WIRE_STRIP_WIDTH / 2.0, PANEL_RES)], fill=(50, 50, 50), width=1)
    draw_p3.text((5, 10), "P3", fill=(150, 150, 255))
    img.paste(p3_canvas, (strip_offset, 0))

    return img.convert("RGB")


def run_illuminator_frames(p1_history):
    """
    Runs the illuminator simulation, locking onto P1's path.
    """
    print("--- 💡 HELICAL ILLUMINATOR ENGAGED (Frames Generation) ---")
    
    start_m, start_l = p1_history[0]
    tracker = IsoTracker(start_m, start_l, LEFT_ZOOM, TRAIL_LENGTH_HELIX)
    solver_m, solver_l = start_m, start_l
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = OMEGA_SYS * f 
        
        c_sys, s_sys = np.cos(theta), np.sin(theta)
        rot_src_m = SRC_STRONG_M * c_sys - SRC_STRONG_L * s_sys
        rot_src_l = SRC_STRONG_M * s_sys + SRC_STRONG_L * c_sys
        
        rgb_data = render_iso_field_unified(solver_m, solver_l, tracker.zoom, PANEL_RES, 
                                            rot_src_m, rot_src_l, 1.0, ISO_ANGLE_2, 25.0)
        
        img_pil = Image.fromarray((rgb_data * 255).astype(np.uint8)).convert("RGB")
        
        # --- B. FIND PEAK & UPDATE CAMERA/RIBBON ---
        gray = np.mean(rgb_data, axis=2)
        mid = PANEL_RES // 2
        r = 30
        
        r_start = max(0, mid-r)
        r_end = min(PANEL_RES, mid+r)
        c_start = max(0, mid-r)
        c_end = min(PANEL_RES, mid+r)

        sub = gray[r_start:r_end, c_start:c_end]
        
        if sub.size == 0:
            loc = (r, r)
        else:
            loc = np.unravel_index(np.argmax(sub), sub.shape)
        
        aspect = np.cos(ISO_ANGLE_2)
        scale = tracker.zoom / PANEL_RES
        dy_px = (loc[0] + r_start) - mid
        dx_px = (loc[1] + c_start) - mid
        
        dm_world = dx_px * scale
        dl_world = dy_px * scale / aspect
        
        true_m = solver_m + dm_world
        true_l = solver_l + dl_world
        
        tracker.history.append((true_m, true_l))
        
        solver_m += (true_m - solver_m) * 0.1
        solver_l += (true_l - solver_l) * 0.1
        tracker.m = solver_m
        tracker.l = solver_l
        
        # --- C. DRAW THE HELICAL RIBBON ---
        draw = ImageDraw.Draw(img_pil)
        screen_pts = tracker.project_trail(PANEL_RES, ISO_ANGLE_2, tracker.m, tracker.l)
        
        if len(screen_pts) > 2:
            ribbon_overlay = Image.new("RGBA", img_pil.size, (0,0,0,0))
            ribbon_draw = ImageDraw.Draw(ribbon_overlay)
            
            for i in range(len(screen_pts) - 1):
                pt1 = screen_pts[i]
                pt2 = screen_pts[i+1]
                
                p1 = pt1
                p2 = pt2
                
                progress = i / TRAIL_LENGTH_HELIX
                width = int(3 * progress) + 1
                alpha = int(255 * progress)
                
                ribbon_draw.line([p1, p2], fill=(255, 255, 100, alpha), width=width)
            
            img_pil.paste(ribbon_overlay, (0,0), ribbon_overlay)

        draw.text((10, 10), "VIEW: ISOMETRIC ILLUMINATOR (P1-LOCK)", fill=(200, 200, 200))
        draw.text((10, 25), f"Camera P_Lab: ({solver_m:.2f}, {solver_l:.2f})", fill=(200, 200, 200))
        draw.text((10, 40), f"HELICITY LOCK: ON", fill=(0, 255, 100))

        frames_buffer.append(img_pil)
        
        if f % 50 == 0:
            print(f"Illuminator Frame {f} Generated.")

    print("✅ ILLUMINATOR FRAMES COMPLETE.")
    return frames_buffer

def combine_and_save():
    """Executes the simulation, renders all views, and combines them into one GIF."""
    
    # 1. Run Simulation and get the full paths for all three quarks
    simulator = ThreeQuarkSimulator()
    p1_history, p2_history, p3_history = simulator.simulate_all()
    
    # 2. Render Illuminator Frames (based on P1 path)
    illuminator_frames = run_illuminator_frames(p1_history)
    
    print("--- 🎬 COMBINING VIEWS ---")
    
    combined_frames = []
    
    TOTAL_WIDTH = PANEL_RES * 2 + WIRE_PANEL_WIDTH
    
    # Store all histories for easy access
    all_histories = (p1_history, p2_history, p3_history)
    
    for f in range(TOTAL_FRAMES):
        
        if f % FRAME_SKIP != 0:
            continue
            
        # 3. Render the Wide Map Frame (Now centered on COM and drawing P1, P2, P3)
        map_frame = render_map_frame(f, all_histories)
        
        # 4. Render the Wireframe Panel (P1, P2, P3 strips)
        wire_frame = render_wireframe_panel(f, all_histories)
        
        # 5. Get the corresponding Illuminator Frame
        illuminator_frame = illuminator_frames[f]
        
        # 6. Create combined image
        combined_img = Image.new('RGB', (TOTAL_WIDTH, PANEL_RES))
        
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