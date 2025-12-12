import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
#  The Eternal Knot: Prime Resonance Stress Test
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

def plot_prime_stress_test(prime7_data, prime13_data):
    fig = plt.figure(figsize=(20, 10))
    
    # --- Plot 1: Prime 7 Resonance ---
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    (x1, y1, z1), (x2, y2, z2) = prime7_data
    
    # Color mapping for depth/time
    colors = np.linspace(0, 1, len(x1))
    
    ax1.scatter(x1, y1, z1, c=colors, cmap='plasma', s=0.5, alpha=0.5, label='Traveler 1')
    ax1.scatter(x2, y2, z2, c=colors, cmap='viridis', s=0.5, alpha=0.5, label='Traveler 2')
    
    # Shadow
    ax1.plot(x1, y1, -4*np.ones_like(x1), color='black', alpha=0.05)

    ax1.set_title("Prime Resonance: 7 (The Heptagon)\nHigh-Frequency Stability", fontsize=14)
    ax1.set_axis_off()
    ax1.view_init(elev=60, azim=45)

    # --- Plot 2: Prime 13 Resonance ---
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    (px1, py1, pz1), (px2, py2, pz2) = prime13_data
    
    ax2.scatter(px1, py1, pz1, c=colors, cmap='plasma', s=0.5, alpha=0.5)
    ax2.scatter(px2, py2, pz2, c=colors, cmap='viridis', s=0.5, alpha=0.5)
    
    ax2.plot(px1, py1, -4*np.ones_like(px1), color='black', alpha=0.05)

    ax2.set_title("Prime Resonance: 13 (The Tridecagon)\nApproaching the Limit of Structure", fontsize=14)
    ax2.set_axis_off()
    ax2.view_init(elev=60, azim=45)
    
    plt.tight_layout()
    plt.savefig('prime_resonance_geometry.png', dpi=150)

if __name__ == "__main__":
    # Generate Data for Primes
    traj_7 = generate_eternal_knot(lobes=7)
    traj_13 = generate_eternal_knot(lobes=13)
    
    plot_prime_stress_test(traj_7, traj_13)