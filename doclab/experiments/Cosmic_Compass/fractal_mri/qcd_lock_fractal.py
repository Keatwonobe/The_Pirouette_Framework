import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST_MIN = 0.0
TWIST_MAX = 4.0
SLICES = 120       # How many layers in the tower
DT = 0.02
STEPS_PER_SLICE = 2000 # Run long enough to find the attractor

def get_force_tower(m, lam, twist):
    # The "Tension Mode" Physics
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    # Basin Weighting
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Fast Gaussian Approx
    diff_g = np.abs(angle - 30);  diff_g = np.minimum(diff_g, 360-diff_g)
    diff_t = np.abs(angle - 150); diff_t = np.minimum(diff_t, 360-diff_t)
    diff_r = np.abs(angle - 270); diff_r = np.minimum(diff_r, 360-diff_r)
    
    w_gold = np.exp(-(diff_g/80)**2)
    w_teal = np.exp(-(diff_t/80)**2)
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    return Fm, Flam

def leapfrog_tower(m, lam, pm, plam, dt, twist):
    Fm, Flam = get_force_tower(m, lam, twist)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_tower(m_n, lam_n, twist)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def run_tower_scan():
    twist_levels = np.linspace(TWIST_MIN, TWIST_MAX, SLICES)
    
    # Storage for the 3D plot
    all_x = []
    all_y = []
    all_z = []
    all_colors = []
    
    print(f"Building the Fractal Tower ({SLICES} slices)...")
    
    for twist in twist_levels:
        # Reset particle
        m, lam = -0.5, 0.5
        pm, plam = 0.9, 0.4
        
        # 1. Warmup (Burn through transients)
        # We only want to plot the "Stable Attractor" shape
        for _ in range(1000):
            m, lam, pm, plam = leapfrog_tower(m, lam, pm, plam, DT, twist)
            
        # 2. Record the Orbit
        # We record about 2 laps worth of points
        lap_points_m = []
        lap_points_lam = []
        
        for _ in range(400): 
            m, lam, pm, plam = leapfrog_tower(m, lam, pm, plam, DT, twist)
            
            # Sub-sampling to keep file size manageable but visible
            lap_points_m.append(m)
            lap_points_lam.append(lam)
        
        # Add to massive lists
        all_x.extend(lap_points_m)
        all_y.extend(lap_points_lam)
        all_z.extend([twist] * len(lap_points_m))
        
        # Color Coding based on Stability/Chaos
        # We use a simple heuristic: How "wide" is the orbit?
        # Chaotic orbits tend to fly further out.
        orbit_radius = np.max(np.abs(lap_points_m))
        
        if orbit_radius > 2.0:
            # High Energy Chaos -> Red/Gold
            col = (1.0, 0.2, 0.2) 
        elif twist > 3.5:
            # The Fermion Plateau -> Deep Blue/Purple
            col = (0.2, 0.4, 1.0)
        else:
            # The Boson Base -> Cyan/Teal
            col = (0.0, 0.8, 0.8)
            
        all_colors.extend([col] * len(lap_points_m))

    # ----------------------------------------
    # 3D PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Scatter plot creates a "Point Cloud" volume
    ax.scatter(all_x, all_y, all_z, c=all_colors, s=1, alpha=0.4)
    
    # Styling
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(TWIST_MIN, TWIST_MAX)
    
    ax.set_xlabel('Position (m)', color='white')
    ax.set_ylabel('Coupling (λ)', color='white')
    ax.set_zlabel('Twist Factor (Asymmetry)', color='white')
    
    ax.set_title("The Resonance Tower: Evolution of Topology", color='white', fontsize=16)
    
    # Hide grid for clean look
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#333333')
    ax.yaxis.pane.set_edgecolor('#333333')
    ax.zaxis.pane.set_edgecolor('#333333')
    ax.tick_params(colors='gray')
    
    # View Angle
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_tower_scan()