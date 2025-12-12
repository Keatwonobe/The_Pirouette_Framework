import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from numba import njit, prange
import json

# =========================================================
#  COMPREHENSIVE PROTON BASIN EXPLORER
#  Mission: Index EVERY fractal lock point in the basin
# =========================================================

# --- EXPLORATION PARAMETERS ---
OUTPUT_FILENAME = "basin_complete_map.gif"
CATALOG_FILENAME = "basin_catalog.json"

# Search Grid Parameters
RADIAL_SAMPLES = 12        # Number of radial distances to sample
MIN_RADIUS = 0.5           # Minimum search radius
MAX_RADIUS = 15.0          # Maximum search radius
ANGULAR_SAMPLES = 24       # Number of angles per radius (360°/24 = 15° increments)

# Fractal Depth Parameters
MAX_FRACTAL_DEPTH = 8      # How deep to drill at each starting point
ZOOM_STEP_FACTOR = 0.2     # Magnification factor per step
INITIAL_ZOOM_WIDTH = 2.0   # Starting search window

# Physics
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

# Animation
TOTAL_FRAMES = 200
DURATION = 40

# --- CORE PHYSICS ENGINE ---

@njit(parallel=True)
def render_microscope(center_m, center_l, width, res, src_m, src_l, src_amp):
    """High-precision interference renderer."""
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

@njit
def calculate_basin_depth(m, l, src_m, src_l):
    """Calculate the potential basin depth at a given M-L coordinate."""
    # Sum of inverse distances creates a potential well
    depth = 0.0
    for i in range(3):
        dx = m - src_m[i]
        dy = l - src_l[i]
        r = np.sqrt(dx*dx + dy*dy)
        if r < 1e-12: r = 1e-12
        depth += 1.0 / r
    return depth

# --- FRACTAL LOCK FINDER ---

def drill_fractal_sequence(start_m, start_l, max_depth):
    """
    Starting from (start_m, start_l), drill down to find nested fractal locks.
    Returns a list of lock points, each with (m, l, r, theta, intensity).
    """
    locks = []
    current_m, current_l = start_m, start_l
    current_width = INITIAL_ZOOM_WIDTH
    
    for depth in range(max_depth):
        final_width = current_width * ZOOM_STEP_FACTOR
        
        # Render the interference pattern
        scan_res = 100
        img = render_microscope(current_m, current_l, current_width, 
                               scan_res, SRC_M_BASE, SRC_L_BASE, 1.0)
        
        # Find local maximum (avoiding edges)
        img[0:5, :] = 0
        img[-5:, :] = 0
        img[:, 0:5] = 0
        img[:, -5:] = 0
        
        idx = np.unravel_index(np.argmax(img), img.shape)
        max_intensity = img[idx]
        
        # Calculate exact position of maximum
        half_w = current_width / 2.0
        pixel_l = (current_l - half_w) + idx[0] * (current_width / (scan_res - 1))
        pixel_m = (current_m - half_w) + idx[1] * (current_width / (scan_res - 1))
        
        # Store lock data
        r_lock = np.sqrt(pixel_m**2 + pixel_l**2)
        theta_lock = np.arctan2(pixel_l, pixel_m)
        
        locks.append({
            'm': pixel_m,
            'l': pixel_l,
            'r': r_lock,
            'theta': theta_lock,
            'intensity': max_intensity,
            'depth': depth,
            'width': final_width
        })
        
        # Update for next iteration
        current_m, current_l = pixel_m, pixel_l
        current_width = final_width
        
        # Stop if intensity becomes too weak
        if max_intensity < 0.01:
            break
    
    return locks

# --- COMPREHENSIVE BASIN SURVEY ---

def survey_entire_basin():
    """
    Systematically explore the entire basin space in polar coordinates.
    Returns a catalog of ALL discovered fractal lock points.
    """
    print("=" * 70)
    print("🔬 INITIATING COMPREHENSIVE PROTON BASIN SURVEY")
    print("=" * 70)
    
    all_locks = []
    search_points = []
    
    # Generate search grid in polar coordinates
    radii = np.linspace(MIN_RADIUS, MAX_RADIUS, RADIAL_SAMPLES)
    
    total_searches = 0
    for r in radii:
        for angle_idx in range(ANGULAR_SAMPLES):
            theta = 2 * np.pi * angle_idx / ANGULAR_SAMPLES
            m_start = r * np.cos(theta)
            l_start = r * np.sin(theta)
            
            search_points.append({
                'r': r,
                'theta': theta,
                'm': m_start,
                'l': l_start
            })
            total_searches += 1
    
    print(f"📍 Total Search Positions: {total_searches}")
    print(f"   Radial Samples: {RADIAL_SAMPLES}")
    print(f"   Angular Samples: {ANGULAR_SAMPLES}")
    print(f"   Max Fractal Depth: {MAX_FRACTAL_DEPTH}")
    print()
    
    # Execute searches
    for idx, point in enumerate(search_points):
        if idx % 20 == 0:
            print(f"  Searching position {idx+1}/{total_searches}... (R={point['r']:.2f}, θ={np.degrees(point['theta']):.0f}°)")
        
        # Drill down from this starting point
        locks = drill_fractal_sequence(point['m'], point['l'], MAX_FRACTAL_DEPTH)
        
        # Tag each lock with its search origin
        for lock in locks:
            lock['origin_r'] = point['r']
            lock['origin_theta'] = point['theta']
            lock['search_id'] = idx
            all_locks.append(lock)
    
    print()
    print(f"✅ SURVEY COMPLETE")
    print(f"   Total Locks Found: {len(all_locks)}")
    print(f"   Average Locks per Position: {len(all_locks)/total_searches:.1f}")
    
    # Analyze depth distribution
    depth_counts = {}
    for lock in all_locks:
        d = lock['depth']
        depth_counts[d] = depth_counts.get(d, 0) + 1
    
    print()
    print("📊 DEPTH DISTRIBUTION:")
    for depth in sorted(depth_counts.keys()):
        print(f"   Layer {depth}: {depth_counts[depth]} locks")
    
    return all_locks, search_points

# --- 3D VISUALIZATION ---

def calculate_3d_positions(locks, frame, total_frames):
    """Calculate 3D positions for all locks at a given frame."""
    num_locks = len(locks)
    m_out = np.zeros(num_locks)
    l_out = np.zeros(num_locks)
    z_out = np.zeros(num_locks)
    
    # Global rotation
    sys_theta = 2 * 2 * np.pi * (frame / total_frames)
    
    # Breathing
    pulse = 1.0 + 0.08 * np.sin(2 * np.pi * (frame / total_frames) * 5.0)
    
    for i, lock in enumerate(locks):
        # Rotate each lock point
        cam_theta = lock['theta'] + sys_theta
        m_out[i] = lock['r'] * np.cos(cam_theta)
        l_out[i] = lock['r'] * np.sin(cam_theta)
        
        # Z-coordinate based on basin depth
        basin_depth = calculate_basin_depth(m_out[i], l_out[i], SRC_M_BASE, SRC_L_BASE)
        
        # Deeper locks sit lower in the basin
        # Scale by intensity and depth
        z_out[i] = -0.5 * basin_depth * pulse + lock['depth'] * 0.2
    
    return m_out, l_out, z_out

def create_3d_animation(all_locks):
    """Generate animated 3D visualization of the complete basin."""
    print()
    print("🎬 Generating 3D Animation...")
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f"Complete Proton Basin Map: {len(all_locks)} Fractal Locks", fontsize=16, fontweight='bold')
    ax.set_xlabel("M-axis", fontsize=12)
    ax.set_ylabel("L-axis", fontsize=12)
    ax.set_zlabel("Z-axis (Basin Depth)", fontsize=12)
    
    # Pre-calculate all positions
    M_full = np.zeros((TOTAL_FRAMES, len(all_locks)))
    L_full = np.zeros((TOTAL_FRAMES, len(all_locks)))
    Z_full = np.zeros((TOTAL_FRAMES, len(all_locks)))
    
    for f in range(TOTAL_FRAMES):
        m, l, z = calculate_3d_positions(all_locks, f, TOTAL_FRAMES)
        M_full[f, :] = m
        L_full[f, :] = l
        Z_full[f, :] = z
    
    # Set axis limits
    m_min, m_max = M_full.min() - 3, M_full.max() + 3
    l_min, l_max = L_full.min() - 3, L_full.max() + 3
    z_min, z_max = Z_full.min() - 2, Z_full.max() + 2
    
    ax.set_xlim(m_min, m_max)
    ax.set_ylim(l_min, l_max)
    ax.set_zlim(z_min, z_max)
    
    # Color by depth
    depths = np.array([lock['depth'] for lock in all_locks])
    max_depth = depths.max()
    colors = plt.cm.plasma(depths / max_depth)
    
    # Create scatter plot
    scatter = ax.scatter([], [], [], c=[], s=20, alpha=0.6, cmap='plasma')
    
    def update(frame):
        scatter._offsets3d = (M_full[frame, :], L_full[frame, :], Z_full[frame, :])
        scatter.set_array(depths)
        
        # Rotate view
        ax.view_init(elev=25, azim=frame * 360 / TOTAL_FRAMES)
        
        if frame % 20 == 0:
            print(f"  Rendering Frame {frame+1}/{TOTAL_FRAMES}")
        
        return scatter,
    
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=DURATION, blit=False, repeat=True)
    ani.save(OUTPUT_FILENAME, writer='pillow', fps=1000/DURATION)
    
    print(f"✅ Animation saved: {OUTPUT_FILENAME}")

# --- DATA EXPORT ---

def save_catalog(all_locks, search_points):
    """Save complete catalog as JSON."""
    catalog = {
        'survey_parameters': {
            'radial_samples': RADIAL_SAMPLES,
            'angular_samples': ANGULAR_SAMPLES,
            'min_radius': MIN_RADIUS,
            'max_radius': MAX_RADIUS,
            'max_fractal_depth': MAX_FRACTAL_DEPTH,
            'total_locks': len(all_locks)
        },
        'search_grid': search_points,
        'locks': all_locks
    }
    
    # Convert numpy types to Python native types for JSON
    def convert_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(item) for item in obj]
        return obj
    
    catalog = convert_types(catalog)
    
    with open(CATALOG_FILENAME, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"✅ Catalog saved: {CATALOG_FILENAME}")

# --- MAIN EXECUTION ---

def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PROTON BASIN COMPLETE SURVEY" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Step 1: Survey the entire basin
    all_locks, search_points = survey_entire_basin()
    
    # Step 2: Save catalog
    save_catalog(all_locks, search_points)
    
    # Step 3: Create visualization
    create_3d_animation(all_locks)
    
    print()
    print("=" * 70)
    print("🎯 MISSION COMPLETE")
    print("=" * 70)
    print(f"Total Fractal Locks Cataloged: {len(all_locks)}")
    print(f"Catalog File: {CATALOG_FILENAME}")
    print(f"Animation File: {OUTPUT_FILENAME}")
    print()

if __name__ == "__main__":
    main()