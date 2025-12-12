import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import os
import sys

# ======================
# CONFIGURATION
# ======================
N_DOTS = 30000          # The "Army of Travelers"
K_TRAVELER = 0.9        # The Twist
GIF_NAME = "cmb_holographic_sphere_rotate.gif"
FRAMES = 60             # Number of rotation frames

def main():
    print(f"[*] Initializing {N_DOTS} Holographic Travelers...")
    
    # 1. Generate Data (Same logic as knot_solver_30k.py)
    n_pairs = N_DOTS // 2
    phi_1 = np.random.uniform(-np.pi, np.pi, n_pairs)
    theta_1 = np.arccos(np.random.uniform(-1, 1, n_pairs))
    
    phi_2 = (phi_1 + np.pi) % (2*np.pi) - np.pi
    theta_2 = np.pi - theta_1
    
    phi_start = np.concatenate([phi_1, phi_2])
    theta_start = np.concatenate([theta_1, theta_2])
    
    # Apply Twist
    phi_end = (phi_start * K_TRAVELER)
    phi_end = (phi_end + np.pi) % (2*np.pi) - np.pi
    
    # Calculate Drift (Color)
    drift = np.abs(phi_end - phi_start) * np.sin(theta_start)
    
    # 2. Convert to Cartesian for 3D Sphere Plotting
    # x = sin(theta) * cos(phi)
    # y = sin(theta) * sin(phi)
    # z = cos(theta)
    # Note: theta is colatitude (0 at North Pole)
    
    x = np.sin(theta_start) * np.cos(phi_end)
    y = np.sin(theta_start) * np.sin(phi_end)
    z = np.cos(theta_start)
    
    print("[*] Generating 3D Rotation GIF...")
    
    frames = []
    angles = np.linspace(0, 360, FRAMES, endpoint=False)
    
    # Setup Figure once
    # We create a new figure per frame to avoid memory leaks with 3D rotation in loop
    
    for i, angle in enumerate(angles):
        sys.stdout.write(f"\r[>] Rendering Frame {i+1}/{FRAMES} (Angle={angle:.1f})")
        sys.stdout.flush()
        
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot Scatter
        # s=2 is small enough to see through, large enough to see color
        sc = ax.scatter(x, y, z, c=drift, cmap='turbo', s=2, alpha=0.8)
        
        # Draw a wireframe sphere for context (faint)
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x_wire = np.cos(u)*np.sin(v)
        y_wire = np.sin(u)*np.sin(v)
        z_wire = np.cos(v)
        ax.plot_wireframe(x_wire, y_wire, z_wire, color="black", alpha=0.1)

        # Remove axes for clean look
        ax.set_axis_off()
        ax.set_title(f"Holographic Sphere | Twist k={K_TRAVELER}", fontsize=14)
        
        # Set Camera Angle
        ax.view_init(elev=30, azim=angle)
        
        # Save Frame
        fname = f"rot_frame_{i}.png"
        plt.savefig(fname, dpi=80, bbox_inches='tight') # Lower DPI for GIF speed
        plt.close(fig)
        
        with Image.open(fname) as pim:
            frames.append(pim.copy())
        os.remove(fname)

    print(f"\n[*] Saving GIF to {GIF_NAME}...")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=100, loop=0)
    print("✅ Done. Check the seam!")

if __name__ == "__main__":
    main()