import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def run_breathing_tube():
    # ----------------------------------------
    # 1. Physics Setup (The Oscillation Logic)
    # ----------------------------------------
    steps = 2000
    dt = 0.04
    t = np.linspace(0, steps*dt, steps)
    
    # The Trajectory (The Spine of the tube)
    # A spiral in (m, lambda) representing the knot
    freq_knot = 0.8
    m_path = np.sin(freq_knot * t) 
    # Lambda has the Parity Bias (The Weak Force Asymmetry)
    lam_path = np.cos(freq_knot * t) + 0.3 * np.sin(0.5 * t)

    # ----------------------------------------
    # 2. Calculate the "Breath" (Tube Radius)
    # ----------------------------------------
    # We apply the logic: Radius ~ |Twist - Tension|
    
    # Twist (Driver) = Distance from center (with bias)
    twist_mag = np.sqrt(m_path**2 + lam_path**2)
    
    # Tension (Confinement) = Response of the vacuum
    # Simplification: The "Delta" oscillation we saw in the 1D graph
    # behaves like a high-frequency harmonic on top of the base path.
    # We simulate this "EM Jitter" by calculating the local acceleration.
    
    # Acceleration roughly tracks the "Force Gap"
    dm = np.gradient(m_path)
    dlam = np.gradient(lam_path)
    velocity = np.sqrt(dm**2 + dlam**2)
    
    # The Radius is proportional to the energy (Velocity^2)
    # Base radius + expansion due to EM stress
    base_radius = 0.15
    # This "pearl_factor" creates the bulges
    pearl_factor = 0.4 * (velocity / np.max(velocity))**2 
    
    radius = base_radius + pearl_factor

    # ----------------------------------------
    # 3. Construct the 3D Tube Surface
    # ----------------------------------------
    # Grid for the tube surface
    theta = np.linspace(0, 2*np.pi, 30)
    T_grid, Theta_grid = np.meshgrid(t, theta)
    
    # We need to broadcast the path arrays to match the grid
    M_grid, _ = np.meshgrid(m_path, theta)
    L_grid, _ = np.meshgrid(lam_path, theta)
    R_grid, _ = np.meshgrid(radius, theta)
    
    # Parametric Equation for the Tube (Vertical orientation)
    # X = m(t) + r(t) * cos(theta)
    # Y = lam(t) + r(t) * sin(theta)
    # Z = t
    
    X = M_grid + R_grid * np.cos(Theta_grid)
    Y = L_grid + R_grid * np.sin(Theta_grid)
    Z = T_grid

    # ----------------------------------------
    # 4. Color Mapping (The Force Basins)
    # ----------------------------------------
    # We color the surface based on the angle in the m-lambda plane
    # Gold (Strong), Red (Weak), Teal (EM)
    
    # Calculate angle for every point on the surface
    # We use the 'base' position (M_grid, L_grid) for the color, 
    # not the surface point, to keep the pearl uniform in color
    angles = np.degrees(np.arctan2(L_grid, M_grid)) % 360
    
    # Vectorized Basin Logic (Same as before)
    # Gold (~30 deg), Teal (~150 deg), Red (~270 deg)
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    w_gold = gaussian(angles, 30, 50)
    w_teal = gaussian(angles, 150, 50)
    w_red = gaussian(angles, 270, 50)
    
    # Normalize weights
    total = w_gold + w_teal + w_red + 1e-6
    w_gold /= total
    w_teal /= total
    w_red /= total
    
    # Create RGB array (Surface shape: 30 x steps)
    colors = np.zeros(X.shape + (3,))
    colors[..., 0] = w_gold*1.0 + w_red*1.0        # R
    colors[..., 1] = w_gold*0.8 + w_teal*0.8       # G
    colors[..., 2] = w_teal*0.8 + w_red*0.2        # B

    # ----------------------------------------
    # 5. Plotting
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Plot the surface
    surf = ax.plot_surface(
        X, Y, Z, 
        facecolors=colors, 
        linewidth=0, 
        antialiased=False, # False makes it look sharper/more "crystalline"
        shade=True,
        rstride=1, cstride=10 # Downsample for speed/style
    )

    # Styling
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(0, steps*dt)
    
    ax.set_xlabel('Mass Field (m)', color='white')
    ax.set_ylabel('Coupling Field (λ)', color='white')
    ax.set_zlabel('Time (t)', color='white')
    
    # Hide grid elements for visual pop
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#444444')
    ax.yaxis.pane.set_edgecolor('#444444')
    ax.zaxis.pane.set_edgecolor('#444444')
    ax.tick_params(colors='gray')

    plt.title("The Breathing Spacetime Knot\nThickness = EM Field Magnitude (The Delta)", color='white', fontsize=14)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_breathing_tube()