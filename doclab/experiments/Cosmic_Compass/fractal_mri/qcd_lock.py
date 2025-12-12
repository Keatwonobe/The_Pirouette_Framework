import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# ----------------------------------------
# 1. The Pirouette Hamiltonian (Hénon-Heiles)
# ----------------------------------------
# Based on Eq (17) in "The Field Pirouette" [cite: 151]
# H = 0.5*(p_m^2 + p_lambda^2) + 0.5*(m^2 + lambda^2) + sigma*(m^2*lambda - lambda^3/3)

def get_force(m, lam, sigma=1.0):
    """
    Computes forces -dH/dm and -dH/dlambda.
    Potential V = 0.5(m^2 + lam^2) + sigma*(m^2*lam - lam^3/3)
    """
    # dV/dm = m + 2*sigma*m*lam
    # dV/dlam = lam + sigma*(m^2 - lam^2)
    
    Fm = -(m + 2.0 * sigma * m * lam)
    Flam = -(lam + sigma * (m**2 - lam**2))
    return Fm, Flam

def leapfrog_step(m, lam, pm, plam, dt, sigma=1.0):
    Fm, Flam = get_force(m, lam, sigma)
    
    # Half-kick momenta
    pm_half = pm + 0.5 * dt * Fm
    plam_half = plam + 0.5 * dt * Flam
    
    # Full drift positions
    m_new = m + dt * pm_half
    lam_new = lam + dt * plam_half
    
    # Recalculate forces at new position
    Fm_new, Flam_new = get_force(m_new, lam_new, sigma)
    
    # Second half-kick momenta
    pm_new = pm_half + 0.5 * dt * Fm_new
    plam_new = plam_half + 0.5 * dt * Flam_new
    
    return m_new, lam_new, pm_new, plam_new

# ----------------------------------------
# 2. Cycle Visualization Logic
# ----------------------------------------

def get_color_from_angle(m, lam):
    """
    Maps the phase space angle to the three gauge forces defined in the paper.
    Fig 1  shows:
    - Top Right (Gold): Strong Force?
    - Top Left (Teal): Hypercharge?
    - Bottom (Red): Weak Force?
    
    (Note: The exact mapping depends on your coordinate system rotation, 
    but this splits the circle into triads.)
    """
    angle = np.arctan2(lam, m) # -pi to pi
    
    # Convert to 0-1 hue or RGB mixing
    # We want a smooth transition to see the "Exchange"
    
    # Normalize angle for 3-way split
    # Hénon-Heiles symmetries are roughly at 90 deg (top), 210 deg, 330 deg.
    # Let's map these sectors to Red, Gold, Teal.
    
    # Simple RGB blending based on angle
    # This creates a "Color Charge" visualization
    deg = np.degrees(angle) % 360
    
    # Define centers of the basins (approximate)
    # Basin 1 (Teal/Blue): Top Left (~150 deg)
    # Basin 2 (Gold/Yellow): Top Right (~30 deg)
    # Basin 3 (Red): Bottom (~270 deg)
    
    # Create an RGB array
    colors = []
    for d in deg:
        # Distance to Red (Bottom, 270)
        dist_r = min(abs(d - 270), abs(d - (-90))) / 120.0
        r_val = np.exp(-dist_r**2 * 4) # Gaussian peak
        
        # Distance to Gold (Top Right, 30)
        dist_g = min(abs(d - 30), abs(d - 390)) / 120.0
        g_val = np.exp(-dist_g**2 * 4)
        
        # Distance to Teal (Top Left, 150)
        dist_b = min(abs(d - 150), abs(d - (-210))) / 120.0
        b_val = np.exp(-dist_b**2 * 4)
        
        # Enhance colors for visibility
        colors.append((r_val, g_val*0.8 + r_val*0.6, b_val + g_val*0.2)) # Mixing to match paper palette slightly
        
    return np.array(colors)

# ----------------------------------------
# 3. Main Simulation
# ----------------------------------------

def run_cycle_check():
    # Parameters
    steps = 10000
    dt = 0.02
    sigma = 1.0
    
    # Initial conditions (Inside the "Genesect" / Black Triangle)
    # We pick a point deep inside to ensure stability, but with enough energy to explore boundaries
    m_val = 0.0
    lam_val = 0.1
    pm_val = 0.38 # Kick it to make it orbit
    plam_val = 0.15
    
    traj_m = []
    traj_lam = []
    
    print("Running Cycle Simulation...")
    for _ in range(steps):
        m_val, lam_val, pm_val, plam_val = leapfrog_step(m_val, lam_val, pm_val, plam_val, dt, sigma)
        traj_m.append(m_val)
        traj_lam.append(lam_val)
        
    traj_m = np.array(traj_m)
    traj_lam = np.array(traj_lam)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    
    # Generate segments for LineCollection
    points = np.array([traj_m, traj_lam]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    # Calculate colors based on angle (The Cycle of Forces)
    # We use the midpoint of the segment for the angle
    mid_m = (traj_m[:-1] + traj_m[1:]) / 2
    mid_lam = (traj_lam[:-1] + traj_lam[1:]) / 2
    
    # Custom coloring logic to match your paper's basins:
    # Red (Bottom), Gold (Top Right), Teal (Top Left)
    angles = np.degrees(np.arctan2(mid_lam, mid_m)) % 360
    
    # Vectorized color assignment
    colors = np.zeros((len(angles), 3))
    
    for i, ang in enumerate(angles):
        # Smooth interpolation between the 3 poles
        # Gold (30 deg), Teal (150 deg), Red (270 deg)
        
        # Proximity to Gold
        diff_g = min(abs(ang - 30), 360 - abs(ang - 30))
        weight_g = np.exp(-(diff_g/60)**2)
        
        # Proximity to Teal
        diff_t = min(abs(ang - 150), 360 - abs(ang - 150))
        weight_t = np.exp(-(diff_t/60)**2)
        
        # Proximity to Red
        diff_r = min(abs(ang - 270), 360 - abs(ang - 270))
        weight_r = np.exp(-(diff_r/60)**2)
        
        # Normalize
        total = weight_g + weight_t + weight_r + 1e-6
        
        # Assign RGB (Gold is R+G, Teal is G+B, Red is R)
        # Gold: (1, 0.8, 0)
        # Teal: (0, 0.8, 0.8)
        # Red:  (1, 0.2, 0.2)
        
        r = (weight_g * 1.0 + weight_t * 0.0 + weight_r * 1.0) / total
        g = (weight_g * 0.8 + weight_t * 0.8 + weight_r * 0.2) / total
        b = (weight_g * 0.0 + weight_t * 0.8 + weight_r * 0.2) / total
        
        colors[i] = [r, g, b]

    # Create LineCollection
    lc = LineCollection(segments, colors=colors, linewidth=1.5, alpha=0.8)
    ax.add_collection(lc)
    
    # Plot Boundaries (Approximate Triangle) to see the "Walls"
    # The triangle vertices in Hénon-Heiles are roughly (0,1), (0.866, -0.5), (-0.866, -0.5)
    # depending on scaling.
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Overlay text
    plt.text(0, 1.05, "Top Basin (Teal/Gold Split)", color='white', ha='center', fontsize=9)
    plt.text(0.9, -0.8, "Right Basin (Gold)", color='gold', ha='center', fontsize=9)
    plt.text(-0.9, -0.8, "Left Basin (Teal)", color='cyan', ha='center', fontsize=9)
    plt.text(0, -1.1, "Bottom Basin (Red)", color='red', ha='center', fontsize=9)
    
    plt.title("The Chromodynamic Cycle\nTrajectory colored by Basin Affinity", color='white', pad=20)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_cycle_check()