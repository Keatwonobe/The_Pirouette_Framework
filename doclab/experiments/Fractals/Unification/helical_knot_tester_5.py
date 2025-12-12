import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
#  The Eternal Knot: Infinite Descent Geometry
# ==========================================================

# --- Configuration ---
LOBES       = 3.14159       # THE GEOMETRY SEED. 3 = Triangle, 4 = Square, 5 = Pentagon.
DT          = 0.002     # Time resolution
STEPS       = 50000     # Depth of infinity to simulate
DECAY       = 0.9999    # The "Friction" that causes the slow inward creep (1.0 = stable orbit)

# --- Physics Constants ---
# We use a normalized potential model now.
# The "Singularity" is at (0,0,0).
ROTATION_SPEED = 2.0    # Orbital Velocity
TEAR_INTENSITY = 1.5    # Z-Axis Amplitude (Height of the knot)

def generate_eternal_knot(lobes=3):
    """
    Generates the trajectory of two potentials spiraling infinitely inward,
    locked in a harmonic resonance defined by 'lobes'.
    """
    # Time array (The "Depth")
    t = np.linspace(0, 100 * np.pi, STEPS)
    
    # 1. The Spiral (XY Plane)
    # They orbit with decaying radius -> "Spiraling In"
    radius = np.power(DECAY, np.arange(STEPS)) * 5.0 # Start at r=5, decay to 0
    
    # Orbital Angle
    theta = ROTATION_SPEED * t
    
    # Traveler 1 (Forward Potential)
    x1 = radius * np.cos(theta)
    y1 = radius * np.sin(theta)
    
    # Traveler 2 (Retrograde Potential) - Opposite side
    x2 = radius * np.cos(theta + np.pi)
    y2 = radius * np.sin(theta + np.pi)
    
    # 2. The Manifold Tear (Z Axis)
    # This is where the SHAPE comes from.
    # The Z-position oscillates based on the LOBE frequency relative to Theta.
    # Resonance: sin(lobes * theta)
    
    # We dampen Z as they get closer to the center, so the knot tightens.
    z_amp = radius * TEAR_INTENSITY * 0.5 
    
    # The "Flip" Logic:
    # They must alternate positions in Z to weave the knot.
    z1 = z_amp * np.sin(lobes * theta)
    z2 = z_amp * np.sin(lobes * theta + np.pi) # Out of phase
    
    return (x1, y1, z1), (x2, y2, z2)

def plot_eternal_geometry(t1, t2, lobe_count):
    x1, y1, z1 = t1
    x2, y2, z2 = t2
    
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # --- Plotting the Infinite Descent ---
    # We use a colormap that represents "Time/Depth".
    # Dark colors = The Past (Outer rim)
    # Bright colors = The Present (Inner singularity)
    
    # Traveler 1 (Forward - Warm/Fire)
    # We plot in segments to map the color gradient
    print("[*] Rendering Forward Potential (The Stretcher)...")
    ax.scatter(x1, y1, z1, c=np.linspace(0, 1, len(x1)), cmap='inferno', s=1, alpha=0.4, label='Forward (Stretcher)')
    
    # Traveler 2 (Retrograde - Cool/Ice)
    print("[*] Rendering Retrograde Potential (The Shrinker)...")
    ax.scatter(x2, y2, z2, c=np.linspace(0, 1, len(x2)), cmap='winter', s=1, alpha=0.4, label='Retrograde (Shrinker)')

    # --- THE GEOMETRY CHECK ---
    # We extract the "Poincaré Section" - a slice through the knot to reveal the shape.
    # We do this by projecting the shadow onto the bottom plane.
    ax.plot(x1, y1, -6*np.ones_like(x1), color='black', alpha=0.1) # Shadow
    
    # View Settings
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-4, 4)
    
    ax.set_axis_off() # Remove box for clean "void" look
    ax.set_title(f"The Eternal Knot | Harmonic Resonance: {lobe_count}\n(Topological Shape: {int(lobe_count)}-gon)", fontsize=15)
    
    # Looking down the barrel of the singularity
    ax.view_init(elev=60, azim=45)
    
    plt.tight_layout()
    plt.savefig('eternal_knot_geometry.png', dpi=150)
    print(f"[*] Geometry Captured: eternal_knot_geometry.png")
    plt.show()

if __name__ == "__main__":
    # --- USER CONTROLS ---
    # Change this to 3 (Triangle), 4 (Square), 5 (Pentagon), or 1.618 (Golden Spiral)
    TARGET_SHAPE = LOBES 
    
    traj1, traj2 = generate_eternal_knot(lobes=TARGET_SHAPE)
    plot_eternal_geometry(traj1, traj2, TARGET_SHAPE)