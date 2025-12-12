import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import interp1d

# =========================================================
#  PROTON MICROSCOPE: ORBITAL SURVEYOR (v6.0)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_survey_path.gif"
RENDER_RES = 500         # High-Quality Output
RADAR_RES = 64           # Low-Quality 'Scout' Resolution
FPS = 20

# The Plan: Dive -> Orbit -> Dive -> Orbit
STAGES = [
    {"type": "orbit", "width": 12.0,  "frames": 60},  # Find the quark at macro scale
    {"type": "dive",  "target": 0.1,  "frames": 10},  # Zoom into it
    {"type": "orbit", "width": 11.7,   "frames": 60},  # Orbit the sub-structure
    {"type": "dive",  "target": 0.02, "frames": 10},  # Zoom deeper
    {"type": "orbit", "width": 11.68,  "frames": 60},  # Orbit the deep structure
]

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

# --- THE SURVEYOR ---

def scout_trajectory(start_m, start_l, width, frames, start_frame_idx):
    """
    Runs a low-res simulation to find the bright spots.
    Returns a CLEANED path (interpolating over dark spots).
    """
    path_m = []
    path_l = []
    
    # We maintain a 'current guess' to avoid jumping to the wrong quark
    curr_m, curr_l = start_m, start_l
    
    print(f"  > Scouting {frames} frames at Width {width}...")
    
    valid_points = [] # Store (frame_local, m, l) for valid locks
    
    for f in range(frames):
        abs_frame = start_frame_idx + f
        sys_theta = 2 * np.pi * (abs_frame / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(abs_frame * 0.1)
        
        # RADAR SCAN
        # Scan a slightly wider area than the view to ensure we don't lose it on edge
        scan_width = width * 1.2
        radar = render_microscope(curr_m, curr_l, scan_width, RADAR_RES, curr_src_m, curr_src_l, pulse)
        
        max_val = np.max(radar)
        
        # THRESHOLD: If max_val is too low, it's a blink. Ignore it.
        # We need a dynamic threshold based on the specific zoom level physics
        # For simplicity, we assume if it drops by 50% of the average, it's gone.
        
        idx = np.unravel_index(np.argmax(radar), radar.shape)
        
        # Convert index to world coords
        scale = scan_width / RADAR_RES
        offset_m = (idx[1] - RADAR_RES/2) * scale
        offset_l = (RADAR_RES/2 - idx[0]) * scale
        
        detected_m = curr_m + offset_m
        detected_l = curr_l + offset_l
        
        # DISTANCE CHECK: Don't jump to a different quark on the other side of the screen
        dist = np.sqrt((detected_m - curr_m)**2 + (detected_l - curr_l)**2)
        
        if dist < width * 0.3: # Only accept if it's reasonably close to last known
            valid_points.append((f, detected_m, detected_l))
            curr_m, curr_l = detected_m, detected_l # Update tracking
        
        # We temporarily append None to preserve frame count, fill later
        path_m.append(None)
        path_l.append(None)

    # RECONSTRUCTION: Interpolate the path
    # Extract arrays
    valid_f = [p[0] for p in valid_points]
    valid_m = [p[1] for p in valid_points]
    valid_l = [p[2] for p in valid_points]
    
    if len(valid_f) < 2:
        print("  ! CRITICAL FAILURE: Could not establish orbit lock.")
        return [start_m]*frames, [start_l]*frames, (start_m, start_l)

    # Create interpolators (Linear or Cubic)
    f_interp_m = interp1d(valid_f, valid_m, kind='linear', fill_value="extrapolate")
    f_interp_l = interp1d(valid_f, valid_l, kind='linear', fill_value="extrapolate")
    
    final_path_m = f_interp_m(np.arange(frames))
    final_path_l = f_interp_l(np.arange(frames))
    
    print(f"  > Path reconstructed. Interpolated {frames - len(valid_f)} dropped frames.")
    
    return final_path_m, final_path_l, (final_path_m[-1], final_path_l[-1])

# --- MAIN EXECUTION ---

def run_mission():
    frames_buffer = []
    
    # Global tracking variables
    # We start tracking "blind" at 0,0 - the first survey will find the quark
    cam_m, cam_l = 0.0, -5.0 
    abs_frame_counter = 0
    
    print("--- MISSION START: MULTI-STAGE FRACTAL SURVEY ---")
    
    for stage_idx, stage in enumerate(STAGES):
        print(f"\nProcessing Stage {stage_idx+1}: {stage['type'].upper()}")
        
        if stage['type'] == 'orbit':
            # 1. SCOUT THE ORBIT
            width = stage['width']
            frames = stage['frames']
            
            # Run the surveyor to get the smooth path
            path_m, path_l, end_pos = scout_trajectory(cam_m, cam_l, width, frames, abs_frame_counter)
            
            # Update camera for next stage
            cam_m, cam_l = end_pos 
            
            # 2. RENDER THE ORBIT
            print("  > Rendering High-Res Orbit...")
            for i in range(frames):
                sys_theta = 2 * np.pi * (abs_frame_counter / 100)
                curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
                pulse = 1.0 + 0.1 * np.sin(abs_frame_counter * 0.1)
                
                # Render at the SURVEYED position
                raw = render_microscope(path_m[i], path_l[i], width, RENDER_RES, curr_src_m, curr_src_l, pulse)
                
                # Visualization (Colorize)
                norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
                norm = np.power(norm, 0.5)
                img = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
                img = np.flipud(img)
                pil_img = Image.fromarray(img)
                
                # Add HUD
                draw = ImageDraw.Draw(pil_img)
                draw.text((10, 10), f"STAGE: ORBIT | WIDTH: {width:.2e}", fill="cyan")
                
                frames_buffer.append(pil_img)
                abs_frame_counter += 1
                
        elif stage['type'] == 'dive':
            # 1. CALCULATE DIVE CURVE
            target_w = stage['target']
            start_w = STAGES[stage_idx-1]['width'] # Get width from prev stage
            frames = stage['frames']
            
            print(f"  > Diving from {start_w:.2e} to {target_w:.2e}")
            
            # Asymptotic Zoom Curve (Exponential Decay)
            # w(t) = a * e^(-kt)
            log_start = np.log(start_w)
            log_end = np.log(target_w)
            zoom_curve = np.exp(np.linspace(log_start, log_end, frames))
            
            # During the dive, we assume the camera stays fixed on the LAST KNOWN location
            # (or we could linear interpolate if we knew the next start point, but fixed is safer for deep zoom)
            
            for i in range(frames):
                sys_theta = 2 * np.pi * (abs_frame_counter / 100)
                curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
                pulse = 1.0 + 0.1 * np.sin(abs_frame_counter * 0.1)
                
                w = zoom_curve[i]
                
                # Render
                raw = render_microscope(cam_m, cam_l, w, RENDER_RES, curr_src_m, curr_src_l, pulse)
                
                norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
                norm = np.power(norm, 0.5)
                img = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
                img = np.flipud(img)
                pil_img = Image.fromarray(img)
                
                draw = ImageDraw.Draw(pil_img)
                draw.text((10, 10), f"STAGE: DIVE  | WIDTH: {w:.2e}", fill="yellow")
                
                frames_buffer.append(pil_img)
                abs_frame_counter += 1

    # SAVE
    print(f"Saving {len(frames_buffer)} frames to {OUTPUT_FILENAME}...")
    frames_buffer[0].save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=50,
        loop=0
    )
    print("✅ DONE.")

if __name__ == "__main__":
    run_mission()