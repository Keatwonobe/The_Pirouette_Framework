import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
#  The Holographic Manifold Projector: Substance vs Shadow
# ==========================================================

# --- Configuration ---
RESOLUTION = 150    # Resolution of the projected field
STEPS      = 500    # Snapshots to integrate over
LOBES      = 3.0    # The Proton resonance

def project_field(phase_offset):
    """
    Project the manifold stress field for a specific phase alignment.
    """
    grid = np.linspace(-6, 6, RESOLUTION)
    X, Y = np.meshgrid(grid, grid)
    Field = np.zeros_like(X)

    # Time-lapse of the Travelers
    t = np.linspace(0, 2 * np.pi, STEPS)
    
    # Resonance positions over one full orbit
    theta = 2.0 * t
    r = 3.0 # Radius constant for snapshot
    
    # Path of Traveler 1
    x1, y1 = r * np.cos(theta), r * np.sin(theta)
    z1 = 1.0 * np.sin(LOBES * theta)
    
    # Path of Traveler 2 (The Offset)
    x2, y2 = r * np.cos(theta + np.pi + phase_offset), r * np.sin(theta + np.pi + phase_offset)
    z2 = 1.0 * np.sin(LOBES * theta + np.pi + phase_offset)

    # Integrate the Stress Field (Inverse distance squared from travelers)
    for i in range(STEPS):
        # 3D Distance check against every point in the XY grid
        dist1_sq = (X - x1[i])**2 + (Y - y1[i])**2 + (0 - z1[i])**2 + 0.5
        dist2_sq = (X - x2[i])**2 + (Y - y2[i])**2 + (0 - z2[i])**2 + 0.5
        
        # Manifold Stress = 1/r^2 (Inverse distance potential)
        Field += (1.0 / dist1_sq) + (1.0 / dist2_sq)

    return np.log(Field) # Log scale to reveal interference patterns

def plot_projections():
    print("[*] Projecting Manifold Fields...")
    
    matter_field = project_field(0.2)   # The Knot Side
    shadow_field = project_field(np.pi) # The Slip Side

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Plot Matter Projection
    im1 = ax1.imshow(matter_field, extent=[-6, 6, -6, 6], cmap='magma')
    ax1.set_title("Substance: Manifold Stress Field (Phase ~ 0.2)\n[Localized Particles / High Structural Grip]", fontsize=12)
    plt.colorbar(im1, ax=ax1, shrink=0.7)

    # Plot Shadow Projection
    im2 = ax2.imshow(shadow_field, extent=[-6, 6, -6, 6], cmap='magma')
    ax2.set_title("Shadow: Manifold Stress Field (Phase ~ Pi)\n[Diffuse Orbit / Low Structural Grip]", fontsize=12)
    plt.colorbar(im2, ax=ax2, shrink=0.7)

    plt.suptitle(f"The Holographic Projector (Resonance: {int(LOBES)})", fontsize=16)
    plt.savefig('manifold_holographic_projection.png', dpi=150)
    print("✅ Projector finished. Check 'manifold_holographic_projection.png'")

if __name__ == "__main__":
    plot_projections()