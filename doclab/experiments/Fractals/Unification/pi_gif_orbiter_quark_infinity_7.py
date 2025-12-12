import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import interp1d

# =========================================================
#  PROTON MICROSCOPE: ANALYTIC ENGINE (v7.0)
#  "The Conic Section Solver"
# =========================================================

# --- MISSION CONFIGURATION ---
OUTPUT_FILENAME = "proton_analytic_zoom.gif"
RENDER_RES = 500         
RADAR_RES = 64           

# --- THE ASYMPTOTIC ZOOM SETTINGS ---
# "I want to start at 21, and flatten out at 3.0"
ZOOM_START = 21.0
ZOOM_ASYMPTOTE = 3.0  # The w_infinity
ZOOM_FRAMES = 120     # How long the dive takes

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

# --- MATH MODULE 1: ASYMPTOTIC ZOOM ---

def calculate_zoom_curve(w_start, w_end_target, w_asymptote, frames):
    """
    Implements: w_n = w_inf + (w_0 - w_inf) * s^n
    Returns the array of widths for the animation.
    """
    # 1. Calculate the Decay Constant (s)
    # s = ((w_N - w_inf) / (w_0 - w_inf)) ^ (1/N)
    
    numerator = w_end_target - w_asymptote
    denominator = w_start - w_asymptote
    
    # Safety check
    if denominator == 0 or numerator <= 0:
        return np.linspace(w_start, w_end_target, frames)
        
    s = np.power(numerator / denominator, 1.0 / frames)
    
    print(f"  > Asymptotic Decay Constant (s): {s:.6f}")
    
    # 2. Generate the curve
    widths = []
    current_w = w_start
    for _ in range(frames):
        # The update rule: w_new = w_inf + s * (w_old - w_inf)
        current_w = w_asymptote + s * (current_w - w_asymptote)
        widths.append(current_w)
        
    return widths, s

# --- MATH MODULE 2: PCA ELLIPSE FITTING ---

def fit_ellipse_to_orbit(m_points, l_points):
    """
    Uses Principal Component Analysis (PCA) to find the perfect ellipse
    that describes the noisy survey data.
    """
    # 1. Stack data
    data = np.vstack((m_points, l_points)).T # Shape (N, 2)
    
    # 2. Center the data (Find the 'Attractor Point')
    center = np.mean(data, axis=0)
    centered_data = data - center
    
    # 3. Covariance Matrix
    cov = np.cov(centered_data.T)
    
    # 4. Eigenvalues and Eigenvectors
    # These represent the magnitude and direction of the ellipse axes
    evals, evecs = np.linalg.eig(cov)
    
    # Sort by magnitude (Major axis first)
    sort_indices = np.argsort(evals)[::-1]
    evals = evals[sort_indices]
    evecs = evecs[:, sort_indices]
    
    # Calculate Radii (2 standard deviations covers ~95% of the orbit)
    # You can tune this multiplier to fit the orbit tighter or looser
    major_axis_radius = 2.0 * np.sqrt(evals[0])
    minor_axis_radius = 2.0 * np.sqrt(evals[1])
    
    # Calculate Rotation Angle of the ellipse
    angle = np.arctan2(evecs[1, 0], evecs[0, 0])
    
    print(f"  > Ellipse Solved: Center=({center[0]:.2f}, {center[1]:.2f}) | "
          f"Axes=({major_axis_radius:.2f}, {minor_axis_radius:.2f}) | "
          f"Tilt={np.degrees(angle):.1f}°")
          
    return center, major_axis_radius, minor_axis_radius, angle

def get_ellipse_point(center, a, b, angle, t):
    """
    Parametric equation of a rotated ellipse.
    t: phase (0 to 2pi)
    """
    # Unrotated coords
    x_local = a * np.cos(t)
    y_local = b * np.sin(t)
    
    # Rotate
    x_rot = x_local * np.cos(angle) - y_local * np.sin(angle)
    y_rot = x_local * np.sin(angle) + y_local * np.cos(angle)
    
    return center[0] + x_rot, center[1] + y_rot

# --- MAIN EXECUTION ---

def run_analytic_mission():
    frames_buffer = []
    
    # --- PHASE 1: THE SURVEY (Get Raw Data) ---
    print("--- PHASE 1: RADAR SURVEY ---")
    survey_frames = 60
    survey_width = ZOOM_ASYMPTOTE # We survey at the destination zoom
    
    raw_m = []
    raw_l = []
    
    # Initial blind spot (center)
    curr_m, curr_l = 0.0, -2.5
    
    for f in range(survey_frames):
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.1)
        
        # Radar Scan
        radar = render_microscope(curr_m, curr_l, survey_width*1.5, RADAR_RES, curr_src_m, curr_src_l, pulse)
        
        # Simple Max Tracking
        idx = np.unravel_index(np.argmax(radar), radar.shape)
        scale = (survey_width*1.5) / RADAR_RES
        offset_m = (idx[1] - RADAR_RES/2) * scale
        offset_l = (RADAR_RES/2 - idx[0]) * scale
        
        found_m = curr_m + offset_m
        found_l = curr_l + offset_l
        
        # Store valid points (ignore if signal is super weak/blinking)
        if np.max(radar) > 0.01: 
            raw_m.append(found_m)
            raw_l.append(found_l)
            curr_m, curr_l = found_m, found_l
            
    # --- PHASE 2: THE ANALYTIC SOLVER (Math) ---
    print("--- PHASE 2: SOLVING GEOMETRY ---")
    
    # A. Fit the Ellipse
    center, a, b, angle = fit_ellipse_to_orbit(raw_m, raw_l)
    
    # B. Calculate the Zoom Curve
    # Target ending at asymptote + tiny buffer
    target_w_end = ZOOM_ASYMPTOTE + 0.05 
    zoom_levels, decay_s = calculate_zoom_curve(ZOOM_START, target_w_end, ZOOM_ASYMPTOTE, ZOOM_FRAMES)
    
    # --- PHASE 3: THE CINEMATIC RENDER ---
    print("--- PHASE 3: RENDERING FINAL CUT ---")
    
    for f in range(ZOOM_FRAMES):
        # 1. Physics Time
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.1)
        
        # 2. Camera Position (Parametric Ellipse)
        # We assume the survey covered roughly 2pi over its duration.
        # We map current frame 'f' to an angle 't' on the ellipse.
        t_phase = (f / ZOOM_FRAMES) * (4 * np.pi) # Do 2 full loops during the dive
        cam_m, cam_l = get_ellipse_point(center, a, b, angle, t_phase)
        
        # 3. Camera Zoom (Asymptotic)
        w = zoom_levels[f]
        
        # 4. Render
        raw = render_microscope(cam_m, cam_l, w, RENDER_RES, curr_src_m, curr_src_l, pulse)
        
        # Post-Process
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.5)
        img = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
        img = np.flipud(img)
        pil_img = Image.fromarray(img)
        
        # HUD
        draw = ImageDraw.Draw(pil_img)
        draw.text((10, 10), f"MODE: ANALYTIC DIVE", fill="cyan")
        draw.text((10, 25), f"ZOOM: {w:.4f} (Asymptote: {ZOOM_ASYMPTOTE})", fill="yellow")
        draw.text((10, 40), f"DECAY CONST (s): {decay_s:.4f}", fill="yellow")
        
        frames_buffer.append(pil_img)
        
        if f % 10 == 0:
            print(f"Rendering Frame {f}/{ZOOM_FRAMES} | Width: {w:.2f}")

    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ DONE.")

if __name__ == "__main__":
    run_analytic_mission()