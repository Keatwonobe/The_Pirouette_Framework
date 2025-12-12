import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
#  The Phase Transition Gallery: Knot vs Slip
# ==========================================================

# --- Configuration ---
DT          = 0.002
STEPS       = 40000
DECAY       = 0.9999

# --- Physics Constants ---
ROTATION_SPEED = 2.0
TEAR_INTENSITY = 1.5

def generate_geometry(lobes, angle_offset):
    t = np.linspace(0, 60 * np.pi, STEPS)
    radius = np.power(DECAY, np.arange(STEPS)) * 5.0
    theta = ROTATION_SPEED * t
    
    # Traveler 1
    x1 = radius * np.cos(theta)
    y1 = radius * np.sin(theta)
    
    # Traveler 2 (Shifted by Phase Offset)
    # The 'angle_offset' is the Manifold Variable
    x2 = radius * np.cos(theta + np.pi + angle_offset)
    y2 = radius * np.sin(theta + np.pi + angle_offset)
    
    # Z-Tear (Resonance)
    z_amp = radius * TEAR_INTENSITY * 0.5
    z1 = z_amp * np.sin(lobes * theta)
    z2 = z_amp * np.sin(lobes * theta + np.pi + angle_offset)
    
    return (x1, y1, z1), (x2, y2, z2)

def plot_transition(lobe_val):
    fig = plt.figure(figsize=(18, 6))
    
    # We test 3 points along the "Phase Manifold"
    # 0.2 (The Knot Side) -> 1.57 (The Transition) -> 3.0 (The Slip Side)
    offsets = [0.2, 1.57, 3.0] 
    labels = ["The Knot Side (Phase ~ 0.2)\n(Locked Structure)", 
              "The Manifold Transition (Phase ~ Pi/2)\n(Unstable Hybrid)", 
              "The Slip Side (Phase ~ Pi)\n(Evasion / Orbit)"]
    
    for i, offset in enumerate(offsets):
        ax = fig.add_subplot(1, 3, i+1, projection='3d')
        (x1, y1, z1), (x2, y2, z2) = generate_geometry(lobe_val, offset)
        
        # Plot with color depth
        ax.plot(x1, y1, z1, color='crimson', lw=0.5, alpha=0.6)
        ax.plot(x2, y2, z2, color='royalblue', lw=0.5, alpha=0.6)
        
        # Shadow for structure check
        ax.plot(x1, y1, -4*np.ones_like(x1), color='black', alpha=0.05)
        
        ax.set_title(labels[i], fontsize=11)
        ax.set_axis_off()
        ax.view_init(elev=50, azim=45)
        ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.set_zlim(-3, 3)

    plt.suptitle(f"Topological Phase Transition | Resonance: {lobe_val}", fontsize=16)
    plt.tight_layout()
    plt.savefig(f'phase_transition_lobe_{lobe_val}.png', dpi=150)
    print(f"[*] Generated Phase Transition Gallery for Lobe {lobe_val}")

if __name__ == "__main__":
    # Test the Proton (3) and the Heptagon (7)
    plot_transition(3.14159265358979323846)
    plot_transition(1.61803398875)