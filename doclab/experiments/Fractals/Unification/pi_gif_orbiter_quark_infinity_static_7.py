import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw

# =========================================================
#  PIROUETTE: MATRIX DIVER (CENTROID TRACKING)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "matrix_diver_hops.gif"
TOTAL_FRAMES = 250
START_WIDTH = 11.0    # Wide start to see the initial split
END_WIDTH = 0.5       # Deep dive
ZOOM_FACTOR = 0.985   # Smooth, constant zoom rate

# --- PHYSICS ---
# We use the same source config that generated the "3s"
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0

# --- MOTION SMOOTHING ---
# 0.05 = Very Heavy Weight (Cinematic), 0.5 = Snappy
CAMERA_INERTIA = 0.08 
# Threshold to define "What is a particle?" (0.0 to 1.0)
CLUSTER_THRESHOLD = 0.6 

# =========================================================
#  NUMBA KERNEL (Unchanged)
# =========================================================

@njit(parallel=True, fastmath=True)
def render_field(center_m, center_l, width, res, pulse_theta, azimuth_phi):
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
            
            # Inverse Azimuth Transform
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
                dist = np.sqrt(dx*dx + dy*dy)
                if dist < 1e-9: dist = 1e-9
                
                phase = k * dist
                amp = (SRC_AMP / dist)
                psi_real += amp * np.cos(phase)
                psi_imag += amp * np.sin(phase)
                
            intensity_map[i, j] = psi_real**2 + psi_imag**2
            
    return intensity_map

# =========================================================
#  THE GOLDILOCKS TRACKER (CENTROID LOGIC)
# =========================================================

def get_cluster_centroid(img, width, center_m, center_l):
    """
    Instead of finding the MAX pixel, this finds the weighted average position
    of all pixels in the top 40% of brightness.
    This creates a stable lock on the 'center of the group'.
    """
    res = img.shape[0]
    
    # 1. Normalize
    vmin, vmax = img.min(), img.max()
    if vmax - vmin < 1e-6: return center_m, center_l, 0.0 # Flat image
    
    norm_img = (img - vmin) / (vmax - vmin)
    
    # 2. Threshold (The Goldilocks Filter)
    # Only look at pixels brighter than X% to ignore background ripples
    # But calculate mass based on intensity
    mask = norm_img > CLUSTER_THRESHOLD
    
    # If we lost the target completely, return current center
    if np.sum(mask) == 0:
        return center_m, center_l, 0.0

    # 3. Calculate Center of Mass
    # Grid coordinates
    Y, X = np.indices(img.shape)
    
    # We use the intensity values as weights
    masses = norm_img[mask]
    y_coords = Y[mask]
    x_coords = X[mask]
    
    total_mass = np.sum(masses)
    mean_y = np.sum(y_coords * masses) / total_mass
    mean_x = np.sum(x_coords * masses) / total_mass
    
    # 4. Map back to World Coordinates
    # (Pixel 0 is top-left, which is Min L, Min M? Check axis logic)
    # L is Y-axis, M is X-axis usually
    
    pixel_l = (center_l - width/2) + mean_y * (width / (res - 1))
    pixel_m = (center_m - width/2) + mean_x * (width / (res - 1))
    
    # Calculate "Spread" (Standard Deviation) - How split is the particle?
    variance = np.sqrt(np.mean((x_coords - mean_x)**2 + (y_coords - mean_y)**2))
    
    return pixel_m, pixel_l, variance

# =========================================================
#  MAIN LOOP
# =========================================================

def run_matrix_diver():
    print("--- 🐇 FOLLOWING THE WHITE RABBIT (Matrix Diver) ---")
    
    # Starting State
    cam_m, cam_l = (0.0, -5.0) # Standard starting hint
    curr_width = START_WIDTH
    
    frames_buffer = []
    
    # We ramp azimuth up to the point where you saw the 3s, then hold
    # Let's sweep azimuth slowly
    
    print("Calibrating camera...")
    # Stabilize initial position
    for _ in range(10):
        scan = render_field(cam_m, cam_l, curr_width, 100, 0.0, 0.0)
        target_m, target_l, _ = get_cluster_centroid(scan, curr_width, cam_m, cam_l)
        cam_m = cam_m * 0.5 + target_m * 0.5
        cam_l = cam_l * 0.5 + target_l * 0.5

    for f in range(TOTAL_FRAMES):
        
        # 1. PARAMETER EVOLUTION
        # We rotate the system to induce the interference churn
        theta = 2 * np.pi * (f / 120) 
        
        # We tilt the azimuth slowly to reveal the structure
        azimuth = 0.0 + (f / TOTAL_FRAMES) * 1.4
        
        # 2. SENSOR SCAN (Low Res)
        # We scan the area to find our centroid
        scan_res = 120
        scan_img = render_field(cam_m, cam_l, curr_width, scan_res, theta, azimuth)
        
        # 3. CALCULATE TARGET
        target_m, target_l, cluster_spread = get_cluster_centroid(scan_img, curr_width, cam_m, cam_l)
        
        # 4. SMOOTH GLIDE (INTERPOLATION)
        # Instead of snapping, we move X% of the way there.
        # This acts like a spring-damper system.
        cam_m += (target_m - cam_m) * CAMERA_INERTIA
        cam_l += (target_l - cam_l) * CAMERA_INERTIA
        
        # 5. ZOOM DYNAMICS
        # If the cluster is tight, we zoom faster. 
        # If the cluster is spreading (splitting), we zoom slower to let it breathe.
        zoom_speed = ZOOM_FACTOR
        if cluster_spread > (scan_res * 0.15): # If spread is > 15% of screen
             zoom_speed = 0.995 # Slow down zoom
        
        curr_width *= zoom_speed
        
        # 6. RENDER FRAME
        hq_res = 450
        final_img = render_field(cam_m, cam_l, curr_width, hq_res, theta, azimuth)
        
        # 7. VISUALIZATION
        norm = (final_img - final_img.min()) / (final_img.max() - final_img.min() + 1e-9)
        norm = np.power(norm, 0.5) 
        
        # "Goldilocks" Coloring
        # We want to highlight the structure, not just the peaks.
        # Use 'twilight_shifted' or 'magma' to see the voids.
        color_map = plt.get_cmap('magma')
        rgb = (color_map(norm)[:, :, :3] * 255).astype(np.uint8)
        
        panel = Image.fromarray(np.flipud(rgb))
        draw = ImageDraw.Draw(panel)
        
        # HUD
        hud_color = (200, 255, 200)
        draw.text((10, 10), f"DIVING: {f}/{TOTAL_FRAMES}", fill=hud_color)
        draw.text((10, 25), f"WIDTH: {curr_width:.5f}", fill=hud_color)
        draw.text((10, 40), f"AZIMUTH: {azimuth:.3f}", fill=hud_color)
        draw.text((10, 55), f"SPREAD: {cluster_spread:.2f}px", fill=hud_color)
        
        # Draw a small crosshair at the center (where we are aiming)
        cx, cy = hq_res//2, hq_res//2
        draw.line((cx-5, cy, cx+5, cy), fill=(100, 255, 100))
        draw.line((cx, cy-5, cx, cy+5), fill=(100, 255, 100))
        
        frames_buffer.append(panel)
        
        if f % 10 == 0:
            print(f"Frame {f} | Width: {curr_width:.4f} | Spread: {cluster_spread:.1f}")

    print("Saving Matrix Diver GIF...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=40, loop=0)
    print("✅ SEQUENCE COMPLETE.")

if __name__ == "__main__":
    run_matrix_diver()