import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D

# ======================
# CONFIGURATION
# ======================
RESOLUTION = 600        # Resolution of the fractal background
FRAMES = 120            # Animation length
FPS = 20                # Framerate
WADA_ZOOM = 2.0         # Field of view for the fractal

print("=" * 60)
print("P I R O U E T T E   E N G I N E   -   H O L E   P U N C H")
print("=" * 60)

# ======================
# 1. THE FRACTAL SUBSTRATE (Wada Basins)
# ======================
def generate_wada_background(res):
    print(f"[*] Generating Wada Basin Substrate ({res}x{res})...")
    
    # Grid setup
    m = np.linspace(-2.0, 2.0, res)
    l = np.linspace(-2.0, 2.0, res)
    M, L = np.meshgrid(m, l)
    
    # Hénon-Heiles Dynamics (Simplified for speed)
    # We map escape basins to colors
    iterations = 20
    dt = 0.1
    
    # State vectors: m, l, pm, pl
    m_cur, l_cur = M.copy(), L.copy()
    pm, pl = np.zeros_like(M), np.zeros_like(L)
    
    active = np.ones_like(M, dtype=bool)
    basin = np.zeros_like(M, dtype=int)
    
    for _ in range(iterations):
        # Gradients
        dm = m_cur + 2 * m_cur * l_cur
        dl = l_cur + (m_cur**2 - l_cur**2)
        
        # Leapfrog-ish
        pm -= dm * dt
        pl -= dl * dt
        m_cur += pm * dt
        l_cur += pl * dt
        
        # Check escape
        r2 = m_cur**2 + l_cur**2
        escaped = (r2 > 10.0) & active
        
        if np.any(escaped):
            # Calculate exit angle for basin ID
            angle = np.arctan2(l_cur[escaped], m_cur[escaped])
            
            # Map angles to basins (1: Teal, 2: Red, 3: Gold)
            # Logic matches the "Fate Map" provided
            b_ids = np.zeros_like(angle, dtype=int)
            b_ids[(angle > np.pi/3) & (angle < np.pi)] = 1      # Teal
            b_ids[(angle > -np.pi) & (angle < -np.pi/3)] = 2    # Red
            b_ids[(angle > -np.pi/3) & (angle < np.pi/3)] = 3   # Gold
            
            basin[escaped] = b_ids
            active[escaped] = False
            
    print("[✓] Fractal geometry calculated.")
    
    # Color mapping
    # 0 (Trapped) = Black
    # 1 = Teal, 2 = Red, 3 = Gold
    # We creates an RGBA image
    image = np.zeros((res, res, 4))
    
    # Masks
    mask_0 = (basin == 0)
    mask_1 = (basin == 1)
    mask_2 = (basin == 2)
    mask_3 = (basin == 3)
    
    # Assign Colors (Hex to Normalized RGB)
    # Teal: #00cccc -> (0, 0.8, 0.8)
    # Red: #ff3333 -> (1, 0.2, 0.2)
    # Gold: #ffaa00 -> (1, 0.66, 0)
    # Void: Black -> (0, 0, 0)
    
    image[mask_1] = [0.0, 0.8, 0.8, 1.0] # Teal
    image[mask_2] = [1.0, 0.2, 0.2, 1.0] # Red
    image[mask_3] = [1.0, 0.66, 0.0, 1.0] # Gold
    image[mask_0] = [0.0, 0.0, 0.0, 0.0] # Black is Transparent (Void)
    
    return image, mask_0

# ======================
# 2. THE KNOT GEOMETRY
# ======================
def generate_trefoil(t, scale=1.0):
    x = scale * (np.sin(t) + 2 * np.sin(2*t))
    y = scale * (np.cos(t) - 2 * np.cos(2*t))
    z = scale * (-np.sin(3*t))
    return x, y, z

# ======================
# 3. VISUALIZATION ENGINE
# ======================
def create_animation():
    # 1. Generate Substrate
    wada_img, void_mask = generate_wada_background(RESOLUTION)
    
    # 2. Setup Plot
    fig = plt.figure(figsize=(12, 12), facecolor='black')
    
    # We use a single 3D axes that fills the figure
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.set_facecolor('black')
    ax.axis('off')
    
    # Remove all panes/grids for "Void" look
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Pre-compute Knot path
    t_knot = np.linspace(0, 2*np.pi, 200)
    
    # Text Setup (Heads Up Display)
    status_text = ax.text2D(0.5, 0.95, "QUARK SCALE", transform=ax.transAxes, 
                           color='cyan', fontsize=20, fontweight='bold', ha='center')
    
    sub_text = ax.text2D(0.5, 0.90, "Layer n=40 | Stability Island", transform=ax.transAxes,
                        color='white', fontsize=12, ha='center')

    # 3. Animation Update
    def update(frame):
        ax.clear()
        ax.axis('off')
        
        # Animation Progress (0 to 1)
        progress = frame / FRAMES
        
        # --- BACKGROUND: THE WADA SET ---
        # We project the 2D image onto a 3D plane at z = -5
        # The plane rotates slightly to give depth
        x = np.linspace(-WADA_ZOOM, WADA_ZOOM, RESOLUTION)
        y = np.linspace(-WADA_ZOOM, WADA_ZOOM, RESOLUTION)
        X, Y = np.meshgrid(x, y)
        
        # Fractal plane is "behind" the knot
        # We rotate it slowly to show the "Landscape" quality
        ax.plot_surface(X, Y, np.full_like(X, -2.0), rstride=10, cstride=10,
                       facecolors=wada_img, shade=False, zorder=1)
        
        # --- FOREGROUND: THE KNOT ---
        # The Knot lives inside the "Void" (the black center of the fractal)
        # It spins and pulses
        
        # Rotation
        angle = 2 * np.pi * progress
        
        # Pulse (The "Punch")
        # At frame 60 (50%), the knot pulses largest
        pulse = 1.0 + 0.2 * np.sin(progress * 4 * np.pi) 
        
        kx, ky, kz = generate_trefoil(t_knot, scale=0.8 * pulse)
        
        # Rotate Knot Coordinates
        # Simple rotation matrix around Z
        xr = kx * np.cos(angle) - ky * np.sin(angle)
        yr = kx * np.sin(angle) + ky * np.cos(angle)
        zr = kz
        
        # Plot the Knot
        # We use a gradient color (Cyan to Magenta)
        # Using segments to color the line
        for i in range(len(xr)-1):
            # Gradient logic
            hue = i / len(xr)
            color = plt.cm.cool(hue) 
            
            # Thick, glowing line
            ax.plot(xr[i:i+2], yr[i:i+2], zr[i:i+2], color=color, linewidth=5, alpha=0.9, zorder=10)
            # Halo effect
            ax.plot(xr[i:i+2], yr[i:i+2], zr[i:i+2], color=color, linewidth=12, alpha=0.2, zorder=9)

        # --- THE HOLE PUNCH RAY ---
        # Draw a line from the center of the knot down into the fractal void
        # Symbolizing the "Axis" that keeps the hole open
        ax.plot([0,0], [0,0], [-2, 0], color='white', linewidth=1, linestyle='--', alpha=0.5)

        # Camera
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-2, 2)
        
        # Slow camera drift
        elev = 30 + 10 * np.sin(progress * 2 * np.pi)
        azim = 45 + progress * 20
        ax.view_init(elev=elev, azim=azim)
        
        # Text Updates
        if frame < FRAMES // 3:
            status_text.set_text("ENTERING BASIN")
            status_text.set_color('yellow')
        elif frame < 2 * FRAMES // 3:
            status_text.set_text("STABILITY ISLAND")
            status_text.set_color('white')
        else:
            status_text.set_text("KNOT SINGULARITY")
            status_text.set_color('cyan')

        return ax,

    # 4. Render
    print(f"[*] Rendering {FRAMES} frames...")
    anim = FuncAnimation(fig, update, frames=FRAMES, interval=50)
    
    output_file = "wada_knot_punch.gif"
    anim.save(output_file, writer=PillowWriter(fps=FPS))
    print(f"[✓] Saved to {output_file}")

if __name__ == "__main__":
    create_animation()