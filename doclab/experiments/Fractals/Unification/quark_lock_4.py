import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from numba import njit, prange
import time

# =========================================================
#  FRACTAL BASIN 3D TRACE
# =========================================================

# --- MISSION CONTROL ---
OUTPUT_FILENAME = "fractal_basin_3d.gif"
TOTAL_FRAMES = 150             # Frames in the final animation
TARGET_CYCLES = 3              # Full rotations of the system (for looping)
DURATION = 50                  # Milliseconds per frame

# FRACTAL LAYERING (from quark_lock_3.py)
GRID_SIZE = 4                  # 4x4 array (16 tiles)
LOCK_DEPTH = GRID_SIZE * GRID_SIZE # Total number of fractal layers
ZOOM_STEP_FACTOR = 0.2         # Magnification factor (5x per step)
INITIAL_ZOOM_WIDTH = 1.5       # The starting width for the very first lock
TARGET_HINT = (-5, 5)        # Initial starting guess

# --- PHYSICS ENGINE (from quark_lock_3.py) ---
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])
BREATHING_FREQ = 6.0 

# --- NUMBA RENDERER (required by drill_down_target) ---

@njit(parallel=True)
def render_microscope(center_m, center_l, width, res, src_m, src_l, src_amp):
    """ High-precision renderer used ONLY for the locking algorithm. """
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

# --- NAVIGATION SYSTEMS (from quark_lock_3.py) ---

def rotate_coords(m, l, theta):
    c, s = np.cos(theta), np.sin(theta)
    return m*c - l*s, m*s + l*c

def drill_down_target(src_m, src_l, hint, final_width):
    """ Recursive locking algorithm to find a single layer's lock. """
    current_m, current_l = hint
    current_width = INITIAL_ZOOM_WIDTH 
    
    while current_width > final_width:
        scan_res = 100 
        img = render_microscope(current_m, current_l, current_width, scan_res, src_m, src_l, 1.0)
        
        # Find local max
        img[0:5, :] = 0; img[-5:, :] = 0; img[:, 0:5] = 0; img[:, -5:] = 0
        idx = np.unravel_index(np.argmax(img), img.shape)
        
        half_w = current_width / 2.0
        # Re-calculate exact position of that pixel
        pixel_l = (current_l - half_w) + idx[0] * (current_width / (scan_res - 1))
        pixel_m = (current_m - half_w) + idx[1] * (current_width / (scan_res - 1))
        
        current_m, current_l = pixel_m, pixel_l
        current_width *= ZOOM_STEP_FACTOR
        
    r_lock = np.sqrt(current_m**2 + current_l**2)
    theta_lock = np.arctan2(current_l, current_m)
    
    return current_m, current_l, r_lock, theta_lock

def find_all_locks():
    """ Runs the recursive lock-in for all layers to get the static r/theta for each. """
    print(f"--- 🎯 INITIATING {LOCK_DEPTH}-LAYER FRACTAL ACQUISITION ---")
    
    lock_data = []
    current_m, current_l = TARGET_HINT
    current_width = INITIAL_ZOOM_WIDTH
    
    # We only need to run this once because the target coordinates are STATIC
    # relative to the source configuration.
    for i in range(LOCK_DEPTH):
        final_width_for_this_lock = current_width * ZOOM_STEP_FACTOR
        
        m_center, l_center, r_lock, theta_lock = drill_down_target(
            SRC_M_BASE, SRC_L_BASE, (current_m, current_l), final_width_for_this_lock
        )
        
        lock_data.append({
            'r': r_lock,
            'theta': theta_lock,
            'width': final_width_for_this_lock # Retaining width for potential future use
        })
        
        current_m, current_l = m_center, l_center
        current_width = final_width_for_this_lock
        
        print(f"  [Layer {i+1:02d}/{LOCK_DEPTH}] Zoom Width: {final_width_for_this_lock:.8f} | R-Lock: {r_lock:.5f}")
        
    print("✅ FRACTAL LOCK SEQUENCE CONFIRMED.")
    return lock_data


def get_3d_locked_coordinates(frame, lock_sequence, total_frames):
    """ Calculates the M, L, and Z positions for ALL locked points at a given frame. """
    
    num_locks = len(lock_sequence)
    m_out = np.zeros(num_locks)
    l_out = np.zeros(num_locks)
    z_out = np.zeros(num_locks)
    
    # Global Rotation for this frame (The N-cycle spin)
    sys_theta = TARGET_CYCLES * 2 * np.pi * (frame / total_frames) 
    
    # Breathing Effect
    pulse = 1.0 + 0.1 * np.sin(2 * np.pi * (frame / total_frames) * BREATHING_FREQ)
    
    for i, lock in enumerate(lock_sequence):
        # 1. M-L Rotation (The point follows the system spin)
        cam_theta = lock['theta'] + sys_theta
        m_out[i] = lock['r'] * np.cos(cam_theta)
        l_out[i] = lock['r'] * np.sin(cam_theta)
        
        # 2. Z-coordinate (The Proton Basin effect)
        # Use a Z based on its radial distance and the breathing pulse.
        # Points further out are lower in the basin.
        r_sq = m_out[i]**2 + l_out[i]**2
        z_out[i] = -0.05 * r_sq * pulse 
        
    return m_out, l_out, z_out


# --- MAIN ANIMATION FUNCTION ---

def generate_3d_fractal_trace():
    
    # 1. Pre-calculate the static lock positions
    lock_sequence = find_all_locks()
    num_locks = len(lock_sequence)
    
    print("\n--- 🔬 Generating 3D Fractal Basin Trace GIF ---")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f"3D Trace of {num_locks} Fractal Lock Points", fontsize=14)
    ax.set_xlabel("M-axis", fontsize=12)
    ax.set_ylabel("L-axis", fontsize=12)
    ax.set_zlabel("Z-axis (Potential Basin)", fontsize=12)
    
    # 2. Calculate ALL coordinates for the full trace
    M_full = np.zeros((TOTAL_FRAMES, num_locks))
    L_full = np.zeros((TOTAL_FRAMES, num_locks))
    Z_full = np.zeros((TOTAL_FRAMES, num_locks))
    
    for f in range(TOTAL_FRAMES):
        m, l, z = get_3d_locked_coordinates(f, lock_sequence, TOTAL_FRAMES)
        M_full[f, :] = m
        L_full[f, :] = l
        Z_full[f, :] = z

    # Set fixed axis limits based on the full trace data
    m_min, m_max = M_full.min() - 2, M_full.max() + 2
    l_min, l_max = L_full.min() - 2, L_full.max() + 2
    z_min, z_max = Z_full.min() - 2, Z_full.max() + 2

    ax.set_xlim(m_min, m_max)
    ax.set_ylim(l_min, l_max)
    ax.set_zlim(z_min, z_max)
    
    # Color scheme: Use a colormap for depth (layer index)
    cmap = plt.cm.plasma
    
    # Initialize plots: N line traces and N moving points
    trace_lines = []
    moving_points = []
    
    for i in range(num_locks):
        # Color based on depth (i/num_locks)
        color = cmap(i / num_locks)
        
        # Trace line (dashed, transparent)
        trace_lines.append(ax.plot([], [], [], color=color, linestyle=':', alpha=0.5)[0])
        
        # Moving point (solid, larger)
        moving_points.append(ax.plot([], [], [], 'o', color=color, markersize=3, alpha=0.8)[0])

    # 3. Define the animation update function
    def update(frame):
        
        # Update the line traces (showing the path so far)
        for i in range(num_locks):
            # Only trace up to the current frame
            trace_lines[i].set_data(M_full[:frame+1, i], L_full[:frame+1, i])
            trace_lines[i].set_3d_properties(Z_full[:frame+1, i])
            
            # Update the moving point (showing the current position)
            # FIX: Wrap scalar values in a list (e.g., [value])
            moving_points[i].set_data([M_full[frame, i]], [L_full[frame, i]])
            moving_points[i].set_3d_properties([Z_full[frame, i]])

        # Rotate the view to follow the motion
        ax.view_init(elev=30, azim=frame * 360 / TOTAL_FRAMES) 
        
        if frame % 15 == 0:
            print(f"  Rendering Frame {frame+1}/{TOTAL_FRAMES}")
            
        return trace_lines + moving_points

    # 4. Create and save the animation
    ani = FuncAnimation(
        fig, 
        update, 
        frames=TOTAL_FRAMES, 
        interval=DURATION, 
        blit=False, 
        repeat=True
    )
    
    # Save the animation
    ani.save(OUTPUT_FILENAME, writer='pillow', fps=1000/DURATION)
    
    print(f"✅ DONE. Saved 3D Fractal Basin Trace to {OUTPUT_FILENAME}")

if __name__ == "__main__":
    generate_3d_fractal_trace()