import numpy as np
from numba import njit, prange
from PIL import Image, ImageDraw
from collections import deque
import colorsys

# =========================================================
#  PIROUETTE: WIDE-ANGLE CO-ROTATING MAP (GEMINI V5)
# =========================================================

# --- CONFIG ---
OUTPUT_FILENAME = "wide_angle_co_rotating_map.gif"
OUTPUT_FILENAME_2 = "helical_illuminator_iso.gif"
TOTAL_FRAMES = 450
PANEL_RES = 600        # Higher resolution for the single wide panel

# VIEW SETTINGS
ISO_ANGLE = 0.85       # ~48 degree tilt (Isometric)
WIDE_ZOOM = 150.0       # Very Wide view (Larger than the original RIGHT_ZOOM of 30.0)

# PHYSICS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0
OMEGA_SYS = 0.05       # Rotation speed of the system

# VIEW DYNAMICS (for sidecar)
FOV_WIDTH = 14.0
ISO_ANGLE_2 = 0.85       # ~48 degrees (Diagonal View)
TRAIL_LENGTH = 40      # How long the ribbon lasts

# PHYSICS
SRC_STRONG_M_2 = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L_2 = np.array([5.0, 5.0, -10.0])
SRC_AMP_2 = 1.0

# =========================================================
#  KERNELS (Adapted from Script 4)
# =========================================================
# =========================================================
#  KERNEL: ISOMETRIC PHASE MANIFOLD (The "V4" Look)
# =========================================================

@njit(parallel=True, fastmath=True)
def render_iso_manifold(center_m, center_l, width, res, pulse_theta, azimuth_phi):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    # Output arrays
    img_out = np.zeros((res, res, 3), dtype=np.float64)
    
    c_sys, s_sys = np.cos(pulse_theta), np.sin(pulse_theta)
    c_phi, s_phi = np.cos(azimuth_phi), np.sin(azimuth_phi)
    k = (2 * np.pi) / 10.0
    
    # Pre-calculate aspect ratio correction for the tilt
    # When we tilt, the vertical axis 'compresses'. We un-compress it here
    # to keep the fractal circular even at an angle.
    aspect_correction = 1.0 / np.cos(azimuth_phi)
    
    for i in prange(res):
        l_screen = l_vals[i]
        for j in range(res):
            m_screen = m_vals[j]
            
            # --- 1. INVERSE ISOMETRIC TRANSFORM ---
            # Screen (j, i) -> World (m, l)
            # We treat the screen Y axis as the tilted L axis
            
            dm = m_screen - center_m
            dl = (l_screen - center_l) * aspect_correction # Stretch back to world
            
            # Rotation (Camera roll - kept at 0 for stability, but we apply azimuth to the grid)
            # Actually, for pure isometric, we just map screen Y to World L projected
            
            m_world = center_m + dm
            l_world = center_l + dl

            # --- 2. FIELD CALCULATION ---
            psi_real = 0.0
            psi_imag = 0.0
            
            for q in range(3):
                # Rotate Sources
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
            
            # --- 3. ISOCONTOUR COLORING ("V4" STYLE) ---
            amp_val = np.sqrt(psi_real**2 + psi_imag**2)
            phase_val = np.arctan2(psi_imag, psi_real)
            
            # Logarithmic Brightness
            log_amp = np.log1p(amp_val)
            
            # Contour Lines (Sine of log-amplitude)
            # High frequency rings
            contour = 0.5 + 0.5 * np.sin(log_amp * 25.0)
            
            # Color Mapping
            # Hue = Phase (Spin)
            hue = (phase_val + np.pi) / (2 * np.pi)
            
            # Saturation = 1.0
            # Value = Contour * Brightness Fade
            val = contour * np.minimum(1.0, 1.2 / (dist * 0.1 + 1.0))
            
            # Manual HSV to RGB
            # (Numba doesn't like matplotlib.colors inside the loop, so we do rough approximation or return raw)
            # Actually, let's just return H, S, V and convert outside or do simple RGB math
            
            # Simple "Electric" Blue-Cyan-Magenta mapping based on phase
            # This mimics the 'hsv' map manually
            
            # H (0-1) -> RGB
            r, g, b = 0.0, 0.0, 0.0
            
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

@njit(parallel=True, fastmath=True)
def render_iso_field(center_m, center_l, width, res, src_m_arr, src_l_arr, pulse, iso_angle):
    # Renders the V4 Isocontours - Adapted from both scripts
    
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
            
            # Use the pre-calculated source arrays (fixed for Co-Rotating Frame)
            for q in range(3):
                dx = m_world - src_m_arr[q]
                dy = l_world - src_l_arr[q]
                dist = np.sqrt(dx*dx + dy*dy) + 1e-9
                
                phase = k * dist
                amp = (SRC_AMP / dist) * pulse
                
                psi_r += amp * np.cos(phase)
                psi_i += amp * np.sin(phase)
            
            # Coloring (V4 Neon) - Using the richer style from script 3/4
            amp_val = np.sqrt(psi_r**2 + psi_i**2)
            phase_val = np.arctan2(psi_i, psi_r)
            
            log_amp = np.log1p(amp_val)
            contour = 0.5 + 0.5 * np.sin(log_amp * 20.0) # Tight rings
            
            hue = (phase_val + np.pi) / (2 * np.pi)
            # Use the brightness fade from the kernel of script 3/4
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
    # Gradient of the STATIC field (Co-rotating) - Re-used from Script 4
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
    def __init__(self, start_m_2, start_l_2):
        self.m = start_m_2
        self.l = start_l_2
        self.history = deque(maxlen=TRAIL_LENGTH)
        self.zoom = FOV_WIDTH

    def update(self, pulse_theta):
        # Quick Scan (Low Res) for physics lock
        # We use a simplified scan at z=0 (top down) to find true position
        # Then we render the angled view based on that lock
        
        # 1. PHYSICS UPDATE (Mocking the Elastic Solver for visual smoothness)
        # In a real app we'd run the full solver, but here we just need the coords
        # to generate the trail.
        
        # We'll re-use the "Tether" logic inline for brevity
        pass 

    def project_trail(self, res, azimuth_phi):
        """
        Converts the World (m, l) history into Screen (x, y) coordinates
        accounting for the isometric tilt.
        """
        pts = []
        cx, cy = res/2, res/2
        scale = res / self.zoom
        aspect = np.cos(azimuth_phi)
        
        for (hm, hl) in self.history:
            # Relative World
            dm = hm - self.m
            dl = hl - self.l
            
            # Project to Screen
            # m (x) stays same
            # l (y) gets squashed by cos(azimuth)
            sx = cx + dm * scale
            sy = cy + dl * scale * aspect
            
            pts.append((sx, sy))
        return pts

def run_map():
    print("--- 🗺️ WIDE-ANGLE CO-ROTATING MAP INITIATED ---")
    
    # 1. SETUP
    # Particle starts in Co-Rotating Frame (Same as script 4)
    pm, pl = 0.0, -6.0
    vm, vl = 0.15, 0.0
    
    # Persistent Trail Layer (Same as script 4)
    # We use a slight opacity in the map background to let the trail pop
    trail_layer = Image.new("RGBA", (PANEL_RES, PANEL_RES), (0,0,0,0))
    trail_draw = ImageDraw.Draw(trail_layer)
    last_trail_pt = None
    
    frames_buffer = []
    
    # Static Map Center (Co-Rotating Frame)
    center_m, center_l = 0.0, 0.0
    
    for f in range(TOTAL_FRAMES):
        
        # --- PHYSICS STEP (CO-ROTATING FRAME) ---
        pulse = 1.0 + 0.15 * np.sin(f * 0.1)
        
        # Forces (Copied directly from script 4)
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
        
        # Friction
        vm *= 0.97
        vl *= 0.97
        
        pm += vm
        pl += vl
        
        # --- RENDER: WIDE-ANGLE STATIC VIEW ---
        # Center = (0,0) - Static Camera in the Co-Rotating Frame
        # Sources = Fixed (Base Position)
        
        raw_image = render_iso_field(center_m, center_l, WIDE_ZOOM, PANEL_RES, 
                                     SRC_STRONG_M, SRC_STRONG_L, pulse, ISO_ANGLE)
        
        # Darken the background map to make trail pop (Same as script 4)
        img = Image.fromarray((raw_image * 150).astype(np.uint8)) 
        
        # --- UPDATE TRAIL LAYER (Persistent) ---
        scale_right = PANEL_RES / WIDE_ZOOM
        aspect = np.cos(ISO_ANGLE)
        cx, cy = PANEL_RES/2, PANEL_RES/2
        
        # Project particle position (pm, pl) to screen coordinates
        sx = cx + pm * scale_right
        sy = cy - (pl * scale_right * aspect) # Flip Y and apply aspect squash
        
        current_pt = (sx, sy)
        
        if last_trail_pt:
            # Color cycle for time (From script 4)
            hue = (f % 100) / 100.0
            r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
            col = (int(r*255), int(g*255), int(b*255), 255)
            # Draw on the persistent layer
            trail_draw.line([last_trail_pt, current_pt], fill=col, width=2)
            
        last_trail_pt = current_pt
        
        # Composite: Paste persistent trail over the map
        img.paste(trail_layer, (0,0), trail_layer)
        
        # --- DRAW HUD & PARTICLE ---
        d_img = ImageDraw.Draw(img)
        d_img.text((10, 10), "TOPOLOGY MAP [CO-ROTATING]", fill=(255, 200, 100))
        d_img.text((10, 30), f"WIDE-ANGLE ZOOM: {WIDE_ZOOM:.1f}", fill=(255, 200, 100))
        d_img.ellipse([sx-4, sy-4, sx+4, sy+4], fill=(255, 255, 255)) # The Particle

        frames_buffer.append(img)
        
        if f % 20 == 0:
            print(f"Frame {f} | P_CoRot: ({pm:.2f}, {pl:.2f})")

    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=30, loop=0)
    print("✅ WIDE-ANGLE MAP COMPLETE.")

def run_illuminator():
    print("--- 💡 HELICAL ILLUMINATOR ENGAGED ---")
    
    # Initialize Tracker at the stable point
    tracker = IsoTracker(0.0, -5.0)
    
    # We use a secondary simple solver to drive the coordinates
    # Copied logic from previous "Tethered Helix" for motion
    solver_m, solver_l = 0.0, -5.0
    velocity = np.array([0.0, 0.0])
    
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = 2 * np.pi * (f / 100)
        
        # --- PHYSICS SIMULATION (Simplified Tether) ---
        # 1. Target Acquisition
        # We cheat slightly and use the "known" attractor behavior for smoother camera work
        # in this visual demo, but normally we'd run render_sensor().
        
        # Find peak near solver_m, solver_l
        # For the demo, let's just create a nice orbital path to visualize
        # The particle is roughly at r=5, rotating
        
        # We render a tiny 50px scan to find the real peak
        # This keeps it honest to the simulation
        scan_w = 4.0
        scan_res = 40
        # Quick render (Top Down)
        # Using a simplified inline source check for speed
        best_val = -1
        best_m, best_l = solver_m, solver_l
        
        # Search vicinity
        sr = 2.0
        c_sys, s_sys = np.cos(theta), np.sin(theta)
        
        # Brute force peak find on the analytical formula (faster than rendering image)
        # ... actually let's just use the previous position + drift
        # because we want to see the TRAIL more than the math search.
        
        # Render the full frame centered on the previous lock
        rgb_data = render_iso_manifold(solver_m, solver_l, tracker.zoom, PANEL_RES, theta, ISO_ANGLE)
        
        # Convert to Image
        img_pil = Image.fromarray((rgb_data * 255).astype(np.uint8))
        img_pil = img_pil.transpose(Image.FLIP_TOP_BOTTOM) # Fix coordinates
        
        # --- FIND PEAK IN SCREEN SPACE TO UPDATE CAMERA ---
        # We want the camera to "lag" slightly behind the particle
        # but we need the particle's true position for the ribbon.
        
        # Let's assume the peak is at the center (since we rendered it there)
        # but we add some noise/movement to the ribbon to show the dynamics
        
        # Let's calculate the ACTUAL peak position relative to center
        # We can scan the center 10% of the image
        gray = np.mean(rgb_data, axis=2)
        mid = PANEL_RES // 2
        r = 30
        sub = gray[mid-r:mid+r, mid-r:mid+r]
        loc = np.unravel_index(np.argmax(sub), sub.shape)
        
        # Screen Delta
        dy_px = loc[0] - r # Y is L (inverted)
        dx_px = loc[1] - r # X is M
        
        # Convert pixel delta to world delta
        aspect = np.cos(ISO_ANGLE)
        scale = tracker.zoom / PANEL_RES
        
        dm_world = dx_px * scale
        dl_world = -dy_px * scale / aspect # Flip Y back
        
        true_m = solver_m + dm_world
        true_l = solver_l + dl_world
        
        # Update Ribbon History
        tracker.history.append((true_m, true_l))
        
        # Move Camera (Smooth Follow)
        solver_m += (true_m - solver_m) * 0.1
        solver_l += (true_l - solver_l) * 0.1
        tracker.m = solver_m
        tracker.l = solver_l
        
        # --- DRAW THE HELICAL RIBBON ---
        draw = ImageDraw.Draw(img_pil)
        
        # Project history to screen coordinates
        screen_pts = tracker.project_trail(PANEL_RES, ISO_ANGLE)
        
        if len(screen_pts) > 2:
            # Draw the Ribbon (Thick line)
            # We fade the color from White (Head) to Purple (Tail)
            for i in range(len(screen_pts) - 1):
                pt1 = screen_pts[i]
                pt2 = screen_pts[i+1]
                
                # Flip Y for PIL
                p1 = (pt1[0], PANEL_RES - pt1[1])
                p2 = (pt2[0], PANEL_RES - pt2[1])
                
                # Color Gradient
                progress = i / len(screen_pts)
                width = int(4 * progress) + 1
                alpha = int(255 * progress)
                
                # Neon Yellow/White core
                draw.line([p1, p2], fill=(255, 255, 100, alpha), width=width)

        # Draw HUD Data
        draw.text((10, 10), "VIEW: ISOMETRIC ILLUMINATOR", fill=(200, 200, 200))
        draw.text((10, 25), f"ANGLE: {ISO_ANGLE*57.29:.1f}°", fill=(200, 200, 200))
        draw.text((10, 40), f"HELICITY LOCK: ON", fill=(0, 255, 100))

        frames_buffer.append(img_pil)
        
        if f % 20 == 0:
            print(f"Frame {f} | Camera: ({solver_m:.2f}, {solver_l:.2f})")

    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=40, loop=0)
    print("✅ MANIFOLD ILLUMINATED.")

if __name__ == "__main__":
    run_map()