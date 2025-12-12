import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# --- Configuration ---
KAPPA = 0.3          # The helical coupling constant
OMEGA = 2.0          # Base frequency
DURATION = 10.0      # Seconds
FRAMES = 200         # Total animation frames
FPS = 30

def helical_trajectory(t, kappa, omega):
    """
    Generates the trajectory based on the K-Hamiltonian energy spectrum.
    According to MATH-028, Energy scales by sqrt(1 + k^2).
    This manifests as a frequency shift (phase accumulation) in the time domain.
    """
    # The 'helical' frequency due to energy splitting
    omega_h = omega * np.sqrt(1 + kappa**2)
    
    # In the helical framework, the coordinate x_h combines linear and rotational
    # The trajectory is a helix with a modified pitch
    x = np.cos(omega_h * t)
    y = np.sin(omega_h * t)
    z = t # Time flows linearly along Z
    
    return x, y, z

def classical_trajectory(t, omega):
    """Standard harmonic oscillator (Kappa = 0)"""
    x = np.cos(omega * t)
    y = np.sin(omega * t)
    z = t
    return x, y, z

# --- Setup Plot ---
fig = plt.figure(figsize=(12, 8))
fig.patch.set_facecolor('#0f0f12') # Dark background for "Sci-Fi" look

# Create 3D Subplot
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#0f0f12')
ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Remove axes for clean aesthetic
ax.set_axis_off()

# Set limits
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(0, DURATION)

# --- Data Generation ---
t_vals = np.linspace(0, DURATION, FRAMES)

# 1. Classical Path (Blue) - The "Ideal" Sine
xc, yc, zc = classical_trajectory(t_vals, OMEGA)

# 2. Helical Path (Red) - The "Real" path with Kappa friction/memory
xh, yh, zh = helical_trajectory(t_vals, KAPPA, OMEGA)

# Initialize Lines
line_classic, = ax.plot([], [], [], color='cyan', alpha=0.4, lw=1, label='Linear Model (κ=0)')
line_helix, = ax.plot([], [], [], color='#ff0055', alpha=0.9, lw=2, label=f'Helical Reality (κ={KAPPA})')

# Initialize "Shadow" Lines (Projections on the wall)
# We project onto x=2 to simulate the "Linear Observer's View"
shadow_classic, = ax.plot([], [], [], color='cyan', alpha=0.2, lw=1, linestyle='--')
shadow_helix, = ax.plot([], [], [], color='#ff0055', alpha=0.4, lw=2, linestyle=':')

# Initialize Points (The "Particle")
point_classic, = ax.plot([], [], [], 'o', color='cyan')
point_helix, = ax.plot([], [], [], 'o', color='#ff0055')

# Annotation Text
status_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, color='white', fontsize=12, family='monospace')

def init():
    line_classic.set_data([], [])
    line_classic.set_3d_properties([])
    line_helix.set_data([], [])
    line_helix.set_3d_properties([])
    
    shadow_classic.set_data([], [])
    shadow_classic.set_3d_properties([])
    shadow_helix.set_data([], [])
    shadow_helix.set_3d_properties([])
    
    return line_classic, line_helix, shadow_classic, shadow_helix

def update(frame):
    # Current index
    i = frame
    
    # Update Classical Trace
    line_classic.set_data(xc[:i], yc[:i])
    line_classic.set_3d_properties(zc[:i])
    
    # Update Helical Trace
    line_helix.set_data(xh[:i], yh[:i])
    line_helix.set_3d_properties(zh[:i])
    
    # Update Heads
    point_classic.set_data([xc[i]], [yc[i]])
    point_classic.set_3d_properties([zc[i]])
    point_helix.set_data([xh[i]], [yh[i]])
    point_helix.set_3d_properties([zh[i]])
    
    # --- The Shadow Projection (The "Linear View") ---
    # Projecting y vs z onto a fixed x plane (e.g., x=2.0)
    wall_x = 2.0
    
    # Classical Shadow
    shadow_classic.set_data(np.full(i, wall_x), yc[:i])
    shadow_classic.set_3d_properties(zc[:i])
    
    # Helical Shadow
    shadow_helix.set_data(np.full(i, wall_x), yh[:i])
    shadow_helix.set_3d_properties(zh[:i])
    
    # Calculate Phase Drift (The "Error" in linear calc)
    # Phase difference between the two oscillators
    phase_diff = abs(np.arcsin(yc[i]) - np.arcsin(yh[i]))
    
    status_text.set_text(
        f"TIME: {t_vals[i]:.2f}\n"
        f"KAPPA: {KAPPA}\n"
        f"PHASE DRIFT: {phase_diff:.2f} rad\n\n"
        f"Using d_h/dt captures\nrotational memory."
    )
    
    # Rotate the camera slowly to emphasize depth
    ax.view_init(elev=20, azim=frame * 0.5)
    
    return line_classic, line_helix, point_classic, point_helix, shadow_classic, shadow_helix, status_text

# Run Animation
ani = animation.FuncAnimation(fig, update, frames=FRAMES, init_func=init, interval=1000/FPS, blit=False)

# To save as GIF (requires imagemagick or ffmpeg)
# ani.save('helical_demonstrator.gif', writer='pillow', fps=30)

plt.legend(loc='lower left', frameon=False, labelcolor='white')
plt.title("The Pirouette Framework: Linear vs Helical Time", color='white', pad=20)
plt.show()