import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
#  The Eternal Knot: Phi vs Pi Comparison
# ==========================================================

# --- Configuration ---
DT          = 0.002     # Time resolution
STEPS       = 60000     # Depth of infinity to simulate
DECAY       = 0.99992   # Slower decay to fill more space

# --- Physics Constants ---
ROTATION_SPEED = 2.0    
TEAR_INTENSITY = 1.5    

def generate_eternal_knot(lobes):
    """
    Generates the trajectory of two potentials spiraling infinitely inward.
    """
    # Time array (The "Depth")
    t = np.linspace(0, 120 * np.pi, STEPS)
    
    # 1. The Spiral (XY Plane)
    radius = np.power(DECAY, np.arange(STEPS)) * 5.0 
    theta = ROTATION_SPEED * t
    
    # Traveler 1 
    x1 = radius * np.cos(theta)
    y1 = radius * np.sin(theta)
    
    # Traveler 2 (Opposite)
    x2 = radius * np.cos(theta + np.pi)
    y2 = radius * np.sin(theta + np.pi)
    
    # 2. The Manifold Tear (Z Axis) - The Resonance
    z_amp = radius * TEAR_INTENSITY * 0.5 
    
    # The "Flip" Logic
    z1 = z_amp * np.sin(lobes * theta)
    z2 = z_amp * np.sin(lobes * theta + np.pi) 
    
    return (x1, y1, z1), (x2, y2, z2)

def plot_comparison(phi_data, pi_data):
    fig = plt.figure(figsize=(20, 10))
    
    # --- Plot 1: Phi (The Golden Ratio) ---
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    (x1, y1, z1), (x2, y2, z2) = phi_data
    
    # Plot faint lines to see the packing
    ax1.plot(x1, y1, z1, color='gold', lw=0.3, alpha=0.6, label='Phi Trajectory')
    ax1.plot(x2, y2, z2, color='indigo', lw=0.3, alpha=0.6)
    
    # Top-down shadow for pattern verification
    ax1.plot(x1, y1, -4*np.ones_like(x1), color='black', alpha=0.05)

    ax1.set_title("The Golden Ratio (Phi ~ 1.618)\nMaximum Irrationality (Perfect Packing)", fontsize=14)
    ax1.set_axis_off()
    ax1.view_init(elev=60, azim=45)

    # --- Plot 2: Pi (The Transcendent) ---
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    (px1, py1, pz1), (px2, py2, pz2) = pi_data
    
    ax2.plot(px1, py1, pz1, color='crimson', lw=0.3, alpha=0.6, label='Pi Trajectory')
    ax2.plot(px2, py2, pz2, color='cyan', lw=0.3, alpha=0.6)
    
    ax2.plot(px1, py1, -4*np.ones_like(px1), color='black', alpha=0.05)

    ax2.set_title("The Transcendent (Pi ~ 3.141)\nErgodic Orbit (The Circle)", fontsize=14)
    ax2.set_axis_off()
    ax2.view_init(elev=60, azim=45)
    
    plt.tight_layout()
    plt.savefig('phi_vs_pi_geometry.png', dpi=150)

if __name__ == "__main__":
    # Generate Data
    phi_traj = generate_eternal_knot(lobes=1.61803398875)
    pi_traj = generate_eternal_knot(lobes=3.14159265359)
    
    plot_comparison(phi_traj, pi_traj)