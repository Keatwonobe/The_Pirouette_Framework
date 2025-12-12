import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from numba import njit, prange
from PIL import Image, ImageDraw
from collections import deque

# =========================================================
#  PIROUETTE: HELICAL ILLUMINATOR (ISOMETRIC V4)
# =========================================================

# --- MISSION CONFIG ---
OUTPUT_FILENAME = "helical_illuminator_iso.gif"
TOTAL_FRAMES = 350
RENDER_RES = 500

# VIEW DYNAMICS
FOV_WIDTH = 14.0
ISO_ANGLE = 0.85       # ~48 degrees (Diagonal View)
TRAIL_LENGTH = 40      # How long the ribbon lasts

# PHYSICS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

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

# =========================================================
#  FLIGHT COMPUTER (TRACKER)
# =========================================================

class IsoTracker:
    def __init__(self, start_m, start_l):
        self.m = start_m
        self.l = start_l
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

# =========================================================
#  MAIN LOOP
# =========================================================

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
        rgb_data = render_iso_manifold(solver_m, solver_l, tracker.zoom, RENDER_RES, theta, ISO_ANGLE)
        
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
        mid = RENDER_RES // 2
        r = 30
        sub = gray[mid-r:mid+r, mid-r:mid+r]
        loc = np.unravel_index(np.argmax(sub), sub.shape)
        
        # Screen Delta
        dy_px = loc[0] - r # Y is L (inverted)
        dx_px = loc[1] - r # X is M
        
        # Convert pixel delta to world delta
        aspect = np.cos(ISO_ANGLE)
        scale = tracker.zoom / RENDER_RES
        
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
        screen_pts = tracker.project_trail(RENDER_RES, ISO_ANGLE)
        
        if len(screen_pts) > 2:
            # Draw the Ribbon (Thick line)
            # We fade the color from White (Head) to Purple (Tail)
            for i in range(len(screen_pts) - 1):
                pt1 = screen_pts[i]
                pt2 = screen_pts[i+1]
                
                # Flip Y for PIL
                p1 = (pt1[0], RENDER_RES - pt1[1])
                p2 = (pt2[0], RENDER_RES - pt2[1])
                
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
    run_illuminator()