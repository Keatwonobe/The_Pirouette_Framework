"""
WOUND CHANNEL NEEDLE TRACKER
Measure the knot thickness by tracking the needle (maximum curvature line)
through the 2276 fractal lock structure
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec
from scipy.spatial.distance import cdist
from scipy.interpolate import interp1d
import json

# ======================
# LOAD BASIN DATA
# ======================

def load_fractal_locks():
    """
    Load the 2276 fractal locks from basin catalog.
    If file doesn't exist, generate synthetic data with same statistics.
    """
    try:
        with open('basin_catalog.json', 'r') as f:
            catalog = json.load(f)
        locks = catalog['locks']
        print(f"[✓] Loaded {len(locks)} fractal locks from catalog")
        return locks
    except FileNotFoundError:
        print("[*] Catalog not found, generating synthetic 2276 locks...")
        return generate_synthetic_locks(2276)

def generate_synthetic_locks(n_locks):
    """
    Generate 2276 locks with 3-fold symmetry and fractal structure.
    """
    locks = []
    
    # Base pattern: 3-fold symmetric with fractal branching
    n_arms = 24  # Angular divisions
    n_layers = 8  # Radial layers
    
    arm_locks = n_locks // n_arms  # ~95 per arm
    
    for arm_idx in range(n_arms):
        base_angle = 2 * np.pi * arm_idx / n_arms
        
        for layer in range(n_layers):
            # Radius decreases with layer (1/3 scaling)
            r_base = 1.0 * (1.0/3.0) ** layer
            
            # Number of locks decreases with layer
            n_in_layer = max(1, arm_locks // (layer + 1))
            
            for i in range(n_in_layer):
                # Add fractal branching
                angle_offset = (np.random.rand() - 0.5) * 0.3 * (1.0/3.0)**layer
                r_offset = (np.random.rand() - 0.5) * 0.2 * r_base
                
                theta = base_angle + angle_offset
                r = r_base + r_offset
                
                # M-L coordinates
                m = r * np.cos(theta)
                l = r * np.sin(theta)
                
                locks.append({
                    'm': m,
                    'l': l,
                    'r': r,
                    'theta': theta,
                    'depth': layer,
                    'intensity': np.random.exponential(1.0)
                })
                
                if len(locks) >= n_locks:
                    return locks
    
    return locks

# ======================
# NEEDLE COMPUTATION
# ======================

def compute_needle(locks, time_phase):
    """
    Compute the "needle" - the line of maximum curvature through the knot.
    
    The needle passes through the center and extends in the direction
    of maximum density gradient.
    
    Returns: needle_points (N x 3 array), curvature_profile
    """
    # Extract positions at this time phase
    # Time phase rotates the entire structure
    rotation = 2 * np.pi * time_phase
    
    positions = []
    for lock in locks:
        m = lock['m']
        l = lock['l']
        
        # Rotate by time phase
        m_rot = m * np.cos(rotation) - l * np.sin(rotation)
        l_rot = m * np.sin(rotation) + l * np.cos(rotation)
        
        # Z coordinate from depth (fractal layers stack vertically)
        z = -0.1 * lock['depth']
        
        positions.append([m_rot, l_rot, z])
    
    positions = np.array(positions)
    
    # Find center of mass
    center = np.mean(positions, axis=0)
    
    # Compute density gradient direction
    # Find the direction with maximum density variation
    
    # Sample directions around a sphere
    n_samples = 50
    theta_samples = np.linspace(0, np.pi, n_samples)
    phi_samples = np.linspace(0, 2*np.pi, n_samples)
    
    max_gradient = 0
    needle_direction = np.array([0, 0, 1])
    
    for theta in theta_samples[::5]:  # Coarse sampling for speed
        for phi in phi_samples[::5]:
            # Unit vector
            direction = np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ])
            
            # Compute density gradient along this direction
            # Count locks in front vs behind
            dots = np.dot(positions - center, direction)
            density_front = np.sum(dots > 0)
            density_back = np.sum(dots < 0)
            gradient = abs(density_front - density_back)
            
            if gradient > max_gradient:
                max_gradient = gradient
                needle_direction = direction
    
    # Create needle line through the knot
    # Extend from -extent to +extent along needle_direction
    extent = 2.0
    t_vals = np.linspace(-extent, extent, 100)
    needle_points = center[np.newaxis, :] + t_vals[:, np.newaxis] * needle_direction[np.newaxis, :]
    
    # Compute curvature profile along needle
    # Curvature = local density of locks near the needle
    curvature_profile = np.zeros(len(t_vals))
    
    for i, point in enumerate(needle_points):
        # Distance from all locks to this point on the needle
        distances = np.linalg.norm(positions - point, axis=1)
        
        # Curvature = sum of 1/r² (inverse square)
        # Softened to avoid singularities
        curvature_profile[i] = np.sum(1.0 / (distances**2 + 0.01))
    
    return needle_points, curvature_profile, positions, center, needle_direction

def measure_wound_channel_thickness(curvature_profile):
    """
    Measure the wound channel thickness from the curvature profile.
    
    The thickness is defined as the FWHM (full width at half maximum)
    of the curvature peak.
    """
    # Find the maximum curvature
    max_curv = np.max(curvature_profile)
    half_max = max_curv / 2.0
    
    # Find where curvature crosses half maximum
    above_half = curvature_profile > half_max
    
    if not np.any(above_half):
        return 0.0
    
    # Find first and last crossing
    indices = np.where(above_half)[0]
    start_idx = indices[0]
    end_idx = indices[-1]
    
    # Thickness in units of needle length
    # Needle spans -2 to +2 (extent = 2), so total length = 4
    needle_length = 4.0
    thickness_fraction = (end_idx - start_idx) / len(curvature_profile)
    thickness = thickness_fraction * needle_length
    
    return thickness

# ======================
# FIND 3-FOLD SYMMETRY
# ======================

def detect_quark_lobes(positions):
    """
    Find the 3 "quark" centers from the 2276 lock positions.
    These are NOT individual particles - they're centers of density.
    """
    # Use k-means-like clustering with k=3
    # But we know they should be 120° apart, so use that constraint
    
    center = np.mean(positions[:, :2], axis=0)  # Use only M-L plane
    
    # Project onto M-L plane
    positions_2d = positions[:, :2]
    
    # Find 3 peaks in angular distribution
    angles = np.arctan2(positions_2d[:, 1] - center[1], 
                        positions_2d[:, 0] - center[0])
    
    # Expected angles for 3-fold symmetry
    expected_angles = [0, 2*np.pi/3, 4*np.pi/3]
    
    quark_centers = []
    for target_angle in expected_angles:
        # Find locks near this angle (±30°)
        angle_diff = np.abs((angles - target_angle + np.pi) % (2*np.pi) - np.pi)
        in_lobe = angle_diff < np.pi/6  # 30° window
        
        if np.any(in_lobe):
            # Average position of locks in this lobe
            lobe_positions = positions_2d[in_lobe]
            quark_center = np.mean(lobe_positions, axis=0)
            quark_centers.append(quark_center)
    
    return np.array(quark_centers)

# ======================
# VISUALIZATION
# ======================

def create_needle_animation():
    """
    Create animation showing:
    1. The 2276 locks structure
    2. The needle threading through
    3. Wound channel thickness measurement
    4. 3-fold symmetry emergence
    """
    print("=" * 70)
    print("WOUND CHANNEL NEEDLE TRACKER")
    print("=" * 70)
    
    # Load locks
    locks = load_fractal_locks()
    print(f"[✓] Analyzing {len(locks)} fractal locks")
    
    # Time phases for animation
    n_frames = 120
    time_phases = np.linspace(0, 1, n_frames)
    
    # Pre-compute for all frames
    print("[*] Computing needle dynamics...")
    thickness_history = []
    
    for i, t in enumerate(time_phases):
        if (i+1) % 20 == 0:
            print(f"    Frame {i+1}/{n_frames}")
        
        _, curvature, _, _, _ = compute_needle(locks, t)
        thickness = measure_wound_channel_thickness(curvature)
        thickness_history.append(thickness)
    
    thickness_history = np.array(thickness_history)
    
    print(f"\n[✓] Wound channel analysis complete:")
    print(f"    Mean thickness: {np.mean(thickness_history):.4f}")
    print(f"    Variation: {np.std(thickness_history):.4f}")
    print(f"    Min/Max: {np.min(thickness_history):.4f} / {np.max(thickness_history):.4f}")
    
    # Create figure
    fig = plt.figure(figsize=(18, 10), facecolor='#000000')
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # Main 3D view
    ax_3d = fig.add_subplot(gs[:, :2], projection='3d')
    ax_3d.set_facecolor('#000000')
    
    # Curvature profile
    ax_curv = fig.add_subplot(gs[0, 2])
    ax_curv.set_facecolor('#0a0a0a')
    
    # Thickness time series
    ax_thick = fig.add_subplot(gs[1, 2])
    ax_thick.set_facecolor('#0a0a0a')
    
    def update(frame):
        t = time_phases[frame]
        
        # Compute needle
        needle_pts, curvature, positions, center, direction = compute_needle(locks, t)
        thickness = thickness_history[frame]
        
        # Clear axes
        ax_3d.clear()
        ax_curv.clear()
        ax_thick.clear()
        
        # === 3D VIEW ===
        ax_3d.set_facecolor('#000000')
        
        # Plot all 2276 locks
        ax_3d.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                     c='cyan', s=1, alpha=0.3)
        
        # Plot needle
        ax_3d.plot(needle_pts[:, 0], needle_pts[:, 1], needle_pts[:, 2],
                  'r-', linewidth=3, alpha=0.8, label='Needle')
        
        # Plot center
        ax_3d.scatter([center[0]], [center[1]], [center[2]],
                     c='yellow', s=100, marker='o', edgecolors='red', linewidth=2)
        
        # Find and plot quark lobes
        quark_centers = detect_quark_lobes(positions)
        if len(quark_centers) == 3:
            ax_3d.scatter(quark_centers[:, 0], quark_centers[:, 1], 
                         np.zeros(3),
                         c='lime', s=300, marker='*', edgecolors='white',
                         linewidth=2, alpha=0.8, label='Quark Centers')
        
        ax_3d.set_xlabel('M', color='gray')
        ax_3d.set_ylabel('L', color='gray')
        ax_3d.set_zlabel('Z', color='gray')
        ax_3d.set_xlim(-1.5, 1.5)
        ax_3d.set_ylim(-1.5, 1.5)
        ax_3d.set_zlim(-1, 0.5)
        ax_3d.view_init(elev=20, azim=frame * 360 / n_frames)
        ax_3d.legend(loc='upper right')
        ax_3d.set_title(f"2276 Fractal Locks | t={t:.3f}", 
                       color='white', fontsize=14)
        ax_3d.xaxis.pane.fill = False
        ax_3d.yaxis.pane.fill = False
        ax_3d.zaxis.pane.fill = False
        ax_3d.tick_params(colors='gray')
        
        # === CURVATURE PROFILE ===
        t_vals = np.linspace(-2, 2, len(curvature))
        ax_curv.plot(t_vals, curvature, 'r-', linewidth=2)
        ax_curv.axhline(np.max(curvature)/2, color='yellow', linestyle='--', 
                       linewidth=1, alpha=0.5, label='FWHM')
        ax_curv.fill_between(t_vals, 0, curvature, alpha=0.3, color='red')
        ax_curv.set_xlabel("Position along needle", color='gray')
        ax_curv.set_ylabel("Curvature", color='gray')
        ax_curv.set_title(f"Curvature Profile\nThickness = {thickness:.4f}", 
                         color='white', fontsize=10)
        ax_curv.legend(loc='upper right', fontsize=8)
        ax_curv.grid(True, alpha=0.2, color='gray')
        ax_curv.tick_params(colors='gray')
        
        # === THICKNESS EVOLUTION ===
        frames_so_far = np.arange(frame + 1)
        ax_thick.plot(frames_so_far, thickness_history[:frame+1], 
                     'lime', linewidth=2)
        ax_thick.axhline(np.mean(thickness_history), color='yellow', 
                        linestyle='--', linewidth=1, alpha=0.5,
                        label=f'Mean = {np.mean(thickness_history):.4f}')
        ax_thick.set_xlim(0, n_frames)
        ax_thick.set_ylim(thickness_history.min()*0.9, thickness_history.max()*1.1)
        ax_thick.set_xlabel("Frame", color='gray')
        ax_thick.set_ylabel("Wound Channel Thickness", color='gray')
        ax_thick.set_title("Thickness vs Time", color='white', fontsize=10)
        ax_thick.legend(loc='upper right', fontsize=8)
        ax_thick.grid(True, alpha=0.2, color='gray')
        ax_thick.tick_params(colors='gray')
        
        return ax_3d, ax_curv, ax_thick
    
    print("\n[*] Creating animation...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=50, blit=False)
    
    output_file = "wound_channel_needle.gif"
    anim.save(output_file, writer=PillowWriter(fps=20), dpi=100)
    
    print(f"\n[✓] Animation saved: {output_file}")
    print("=" * 70)

# ======================
# MAIN
# ======================

if __name__ == "__main__":
    create_needle_animation()