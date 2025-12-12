import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont

# =========================================================
#  PROTON MICROSCOPE: THE HELICAL OPERATOR (v10.0)
#  "When motion remembers its own turn..." [MATH-028]
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_helical_operator.gif"
RENDER_RES = 500
RADAR_RES = 64
TOTAL_FRAMES = 160

# --- HELICAL PARAMETERS ---
# We don't just zoom linearly. We zoom along the spiral arm.
# "Differentiation is perception; integration is memory."
LOCK_START = 0.0     
LOCK_END = 1.0       
ZOOM_START = 21.0    
ZOOM_END = 11.9      # Deep dive into the singularity

# --- PHYSICS ENGINE ---
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

@njit(parallel=True)
def render_microscope(center_m, center_l, width, res, src_m, src_l, src_amp):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    intensity_map = np.zeros((res, res), dtype=np.float64)
    
    k_vec = np.zeros(3)
    for i in range(3):
        dist = np.sqrt(src_m[i]**2 + src_l[i]**2)
        k_vec[i] = (2 * np.pi) / (dist + 1e-9)

    for i in prange(res):
        y = l_vals[i]
        for j in range(res):
            x = m_vals[j]
            psi_real, psi_imag = 0.0, 0.0
            for q in range(3):
                dx = x - src_m[q]
                dy = y - src_l[q]
                r = np.sqrt(dx*dx + dy*dy)
                if r < 1e-12: r = 1e-12
                phase = k_vec[q] * r
                amp = (src_amp / r)
                psi_real += amp * np.cos(phase)
                psi_imag += amp * np.sin(phase)
            intensity_map[i, j] = psi_real**2 + psi_imag**2
    return intensity_map

def rotate_coords(m, l, theta):
    c, s = np.cos(theta), np.sin(theta)
    return m*c - l*s, m*s + l*c

# --- THE HELICAL ALGEBRA MODULE [MATH-028] ---

def fit_helical_path(raw_m, raw_l):
    """
    Solves for the Spiral Parameters (Kappa).
    Model: r(theta) = A * e^(kappa * theta)
    """
    # 1. Centering (find the 'eye' of the spiral)
    # Simple mean is approx correct for a dense orbit, 
    # but for a spiral segment, we might need to assume 0,0 if the survey is small.
    # Let's assume the Attractor is roughly the center of the survey mass for now.
    center_m = np.mean(raw_m)
    center_l = np.mean(raw_l)
    
    # 2. Convert to Polar wrt Center
    r_vals = []
    theta_vals = []
    
    for i in range(len(raw_m)):
        dm = raw_m[i] - center_m
        dl = raw_l[i] - center_l
        r = np.sqrt(dm**2 + dl**2)
        th = np.arctan2(dl, dm)
        r_vals.append(r)
        theta_vals.append(th)
        
    r_vals = np.array(r_vals)
    theta_vals = np.unwrap(np.array(theta_vals)) # Handle 2pi jumps
    
    # 3. Linear Regression on Log-Space
    # ln(r) = ln(A) + kappa * theta
    # y = C + mx
    
    x = theta_vals
    y = np.log(r_vals + 1e-9)
    
    # Standard Least Squares
    A_mat = np.vstack([x, np.ones(len(x))]).T
    kappa, ln_A = np.linalg.lstsq(A_mat, y, rcond=None)[0]
    
    start_radius = np.exp(ln_A)
    
    # Enforce a negative kappa (inward spiral) if the data is ambiguous,
    # because we want to dive.
    if kappa > 0: 
        kappa = -0.1 # Default gentle inward spiral
        
    print(f"  > Helical Solve: Center=({center_m:.2f}, {center_l:.2f}) | Kappa={kappa:.4f} | r0={start_radius:.2f}")
    
    return (center_m, center_l), start_radius, kappa, theta_vals[0]

def get_helical_position(center, r0, kappa, start_theta, progress):
    """
    Calculates position along the spiral.
    Progress 0.0 -> 1.0 covers several loops (theta increases).
    """
    # We want to do e.g. 3 full rotations (6pi) during the sequence
    total_rotation = 6 * np.pi 
    
    current_theta = start_theta + (progress * total_rotation)
    
    # Helical radius decay
    # r = r0 * e^(kappa * (theta - theta_0))
    current_r = r0 * np.exp(kappa * (current_theta - start_theta))
    
    x = current_r * np.cos(current_theta)
    y = current_r * np.sin(current_theta)
    
    return center[0] + x, center[1] + y, current_r

# --- MAIN EXECUTION ---

def run_helical_mission():
    frames_buffer = []
    
    # 1. THE SURVEY (Finding the Arc)
    print("--- PHASE 1: SURVEYING THE SPIRAL ARM ---")
    survey_duration = 60
    raw_m, raw_l = [], []
    curr_m, curr_l = 0.0, -5.0 
    
    # We scan to find the "tail" of the spiral
    for f in range(survey_duration):
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.1)
        
        scan_w = ZOOM_START * 1.2
        radar = render_microscope(curr_m, curr_l, scan_w, RADAR_RES, curr_src_m, curr_src_l, pulse)
        
        if np.max(radar) > 0.02:
            idx = np.unravel_index(np.argmax(radar), radar.shape)
            scale = scan_w / RADAR_RES
            off_m = (idx[1] - RADAR_RES/2) * scale
            off_l = (RADAR_RES/2 - idx[0]) * scale
            curr_m += off_m
            curr_l += off_l
            raw_m.append(curr_m)
            raw_l.append(curr_l)

    if len(raw_m) < 10:
        print(" ! Signal too weak. Using Default Spiral.")
        raw_m = [10 * np.cos(t/10) for t in range(50)]
        raw_l = [10 * np.sin(t/10) for t in range(50)]

    # 2. THE HELICAL SOLVE (MATH-028)
    center, r0, kappa, theta_start = fit_helical_path(raw_m, raw_l)

    # 3. RENDER THE SPIRAL DIVE
    print("--- PHASE 2: EXECUTING HELICAL DESCENT ---")
    
    for f in range(TOTAL_FRAMES):
        progress = f / (TOTAL_FRAMES - 1)
        
        # A. Physics Rotation
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.05 * np.sin(f * 0.2)
        
        # B. Calculate Helical Path
        # The camera slides down the spiral arm
        rail_m, rail_l, current_radius = get_helical_position(center, r0, kappa, theta_start, progress)
        
        # C. Camera Logic
        # We blend from the center view to the rail view
        # But crucially, we keep the camera oriented "down" the spiral
        
        # Lock Ratio Curve (Ease In)
        lock_ratio = progress 
        
        # Zoom Logic
        # Zoom should roughly track the spiral radius, but start wide
        target_zoom = max(current_radius * 4.0, ZOOM_END) # Keep some context
        current_zoom = ZOOM_START + (target_zoom - ZOOM_START) * progress
        
        cam_m = center[0] * (1 - lock_ratio) + rail_m * lock_ratio
        cam_l = center[1] * (1 - lock_ratio) + rail_l * lock_ratio
        
        # D. Render
        raw = render_microscope(cam_m, cam_l, current_zoom, RENDER_RES, curr_src_m, curr_src_l, pulse)
        
        # Post-Process
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.5)
        img = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
        img = np.flipud(img)
        pil_img = Image.fromarray(img)
        
        # HUD
        draw = ImageDraw.Draw(pil_img)
        draw.text((10, 10), f"HELICAL OPERATOR [MATH-028]", fill="cyan")
        draw.text((10, 25), f"KAPPA (Torsion): {kappa:.4f}", fill="yellow")
        draw.text((10, 40), f"RADIUS: {current_radius:.4f}", fill="yellow")
        
        # Draw the reticle - if locked, it's green
        cx, cy = RENDER_RES // 2, RENDER_RES // 2
        draw.line((cx-10, cy, cx+10, cy), fill=(0, 255, 0))
        draw.line((cx, cy-10, cx, cy+10), fill=(0, 255, 0))

        frames_buffer.append(pil_img)
        
        if f % 20 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | R: {current_radius:.2f} | Zoom: {current_zoom:.2f}")

    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ HELICAL DIVE COMPLETE.")

if __name__ == "__main__":
    run_helical_mission()