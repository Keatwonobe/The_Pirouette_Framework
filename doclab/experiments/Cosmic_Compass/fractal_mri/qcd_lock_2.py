import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------------------
# 1. Active Force Dynamics
# ----------------------------------------

def get_basin_properties(m, lam):
    """
    Determines which force dominates at the current position (m, lam)
    and returns physics modifiers.
    
    Returns:
    - k_mod: Stiffness modifier (Strong Force tension)
    - p_mod: Parity modifier (Weak Force asymmetry)
    - color: RGB color for plotting
    """
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Gaussian weights for the three basins
    # Gold (Strong): ~30 deg
    w_gold = np.exp(-(min(abs(angle - 30), 360 - abs(angle - 30))/45)**2)
    
    # Teal (EM): ~150 deg
    w_teal = np.exp(-(min(abs(angle - 150), 360 - abs(angle - 150))/45)**2)
    
    # Red (Weak): ~270 deg
    w_red = np.exp(-(min(abs(angle - 270), 360 - abs(angle - 270))/45)**2)
    
    total = w_gold + w_teal + w_red + 1e-6
    
    # --- PHYSICS MODIFIERS ---
    
    # GOLD (Strong): High tension. Makes the potential steeper locally.
    # Represents the "gluon flux tube" tightness.
    k_strong = 1.0 + (w_gold * 0.5) 
    
    # RED (Weak): Parity Asymmetry. 
    # Represents the chiral nature (V-A theory).
    p_weak = w_red * 0.15 
    
    # TEAL (EM): Standard interaction (baseline).
    
    # Color mixing
    r = (w_gold * 1.0 + w_red * 1.0) / total
    g = (w_gold * 0.8 + w_teal * 0.8 + w_red * 0.2) / total
    b = (w_teal * 0.8 + w_red * 0.2) / total
    
    return k_strong, p_weak, (r, g, b)

def get_force_active(m, lam, sigma=1.0):
    """
    Calculates forces with ACTIVE properties based on location.
    """
    k_mod, p_mod, _ = get_basin_properties(m, lam)
    
    # Base Hénon-Heiles Force
    # V = 0.5*(m^2 + lam^2) + sigma*(m^2*lam - lam^3/3)
    
    # Modified Force:
    # 1. Apply Stiffness (k_mod) to the restoring force (linear term)
    # 2. Apply Parity Kick (p_mod) to the nonlinear interaction
    
    Fm = -k_mod * m - 2.0 * sigma * m * lam
    
    # The Weak force asymmetry (p_mod) biases the lambda direction
    Flam = -k_mod * lam - sigma * (m**2 - lam**2) + p_mod 
    
    return Fm, Flam

def leapfrog_step_active(m, lam, pm, plam, dt, sigma=1.0):
    Fm, Flam = get_force_active(m, lam, sigma)
    
    pm_half = pm + 0.5 * dt * Fm
    plam_half = plam + 0.5 * dt * Flam
    
    m_new = m + dt * pm_half
    lam_new = lam + dt * plam_half
    
    Fm_new, Flam_new = get_force_active(m_new, lam_new, sigma)
    
    pm_new = pm_half + 0.5 * dt * Fm_new
    plam_new = plam_half + 0.5 * dt * Flam_new
    
    return m_new, lam_new, pm_new, plam_new

# ----------------------------------------
# 2. Simulation with "Crazy Fast" Energy
# ----------------------------------------

def run_spacetime_knot():
    # Increase steps to see the long "strand"
    steps = 4000 
    dt = 0.015
    sigma = 1.0
    
    # High Energy Initial Conditions
    # Standard stable orbits are around E=0.10 to 0.14
    # We are pushing it to the edge of stability to test the "Knot"
    m_val = 0.0
    lam_val = 0.1
    pm_val = 0.45  # Fast initial kick
    plam_val = 0.2
    
    traj_m = []
    traj_lam = []
    traj_t = []
    colors = []
    
    t = 0
    print("Simulating Active Force Interactions...")
    
    for _ in range(steps):
        # Calculate properties for CURRENT state (before moving)
        _, _, col = get_basin_properties(m_val, lam_val)
        colors.append(col)
        
        # Step forward
        m_val, lam_val, pm_val, plam_val = leapfrog_step_active(m_val, lam_val, pm_val, plam_val, dt, sigma)
        
        traj_m.append(m_val)
        traj_lam.append(lam_val)
        traj_t.append(t)
        t += dt

    # Convert to arrays
    traj_m = np.array(traj_m)
    traj_lam = np.array(traj_lam)
    traj_t = np.array(traj_t)
    colors = np.array(colors)

    # ----------------------------------------
    # 3. Visualization: The Time-Strand
    # ----------------------------------------
    
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # We plot segments so we can color them individually
    # This is a bit computationally heavy but necessary for the "Phase Change" look
    for i in range(len(traj_m) - 1):
        ax.plot(
            traj_m[i:i+2], 
            traj_lam[i:i+2], 
            traj_t[i:i+2], 
            color=colors[i], 
            lw=1.5,
            alpha=0.8
        )

    # Styling
    ax.set_xlabel('Mass Field (m)', color='white')
    ax.set_ylabel('Coupling Field (λ)', color='white')
    ax.set_zlabel('Time (t)', color='white')
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    
    # Hide grid and panes for that "floating in void" look
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    
    # White axis ticks
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')

    plt.title("The Spacetime Knot\nParticle 'Strand' undergoing Phase Transitions", color='white', fontsize=14)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_spacetime_knot()