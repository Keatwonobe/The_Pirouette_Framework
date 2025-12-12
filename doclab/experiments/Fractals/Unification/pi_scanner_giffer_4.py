import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Configuration ---
RES = 400               # Resolution of the field
FRAMES = 100
LIMIT = 6.0             # Grid Size
WAVELENGTH = 1.2        # Distance between twist peaks
K_TWIST = 3.0           # How tightly wound the spiral is (The "Twist" parameter)

# Setup Grid
x = np.linspace(-LIMIT, LIMIT, RES)
y = np.linspace(-LIMIT, LIMIT, RES)
X, Y = np.meshgrid(x, y)

# --- The Physics of Shear ---
def get_helical_field(cx, cy, chirality):
    """
    Generates a 'Twist Field' centered at (cx, cy).
    Chirality (+1 or -1) determines the direction of the spiral.
    """
    # Relative coordinates
    dx = X - cx
    dy = Y - cy
    r = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dy, dx)
    
    # The Helical Wave Function:
    # A spiral is defined by (Radial Phase + Angular Phase)
    # chirality * theta ensures they spin in opposite directions
    phase = (r * (2 * np.pi / WAVELENGTH)) + (chirality * K_TWIST * theta)
    
    # We use a Sine wave to represent the periodic stress of the twist
    # Damp it with distance (1/r) so it doesn't overwhelm the view
    amplitude = 1.0 / (r + 0.5)
    return amplitude * np.sin(phase)

# --- Animation State ---
# Travelers move past each other linearly
traveler1_path = np.linspace(-4, 4, FRAMES)
traveler2_path = np.linspace(4, -4, FRAMES) # Opposite direction

fig, ax = plt.subplots(figsize=(8, 8))

def update(frame):
    ax.clear()
    
    # 1. Update Positions
    t1_x, t1_y = traveler1_path[frame], 1.5  # Top track
    t2_x, t2_y = traveler2_path[frame], -1.5 # Bottom track
    
    # 2. Generate Fields (The "Universes")
    # Traveler 1: Chirality +1 (Normal Time)
    field1 = get_helical_field(t1_x, t1_y, chirality=1)
    
    # Traveler 2: Chirality -1 (Retrograde Time)
    field2 = get_helical_field(t2_x, t2_y, chirality=-1)
    
    # 3. INTERFERENCE (The "Shear")
    # Simple summation shows the constructive/destructive interference
    total_field = field1 + field2
    
    # 4. Visualize
    # We use a divergent colormap (Red/Blue) to show Shear Direction
    im = ax.imshow(total_field, extent=[-LIMIT, LIMIT, -LIMIT, LIMIT], 
                   origin='lower', cmap='RdBu_r', vmin=-1, vmax=1)
    
    # Mark the Travelers
    ax.scatter(t1_x, t1_y, color='lime', s=100, edgecolors='black', label="Traveler A (+)")
    ax.scatter(t2_x, t2_y, color='cyan', s=100, edgecolors='black', label="Traveler B (-)")
    
    ax.set_title(f"Topological Shear Interference | Frame {frame}")
    ax.set_xlabel("Space X")
    ax.set_ylabel("Space Y")
    
    # Remove ticks for clean 'substrate' look
    ax.set_xticks([])
    ax.set_yticks([])
    
    return [im]

print("Rendering the Shear Lattice...")
ani = animation.FuncAnimation(fig, update, frames=FRAMES, interval=50)
plt.show()