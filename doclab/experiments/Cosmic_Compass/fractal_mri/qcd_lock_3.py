import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------------------
# The "Free Rule": Color Neutrality
# ----------------------------------------

def get_neutrality_force(m, lam, sigma=1.0):
    """
    Calculates forces based on the "Free Rule" of Color Neutrality.
    The Gold (Strong) force is not calculated from a potential.
    It is the vector required to zero out the sum of Red and Teal forces.
    
    This enforces R + G + B = 0 (Neutrality/Confinement).
    """
    
    # 1. Calculate Teal Force (Electromagnetism)
    # Modeled as standard harmonic attraction (Charge)
    # Basin center approx (-0.866, 0.5)
    teal_center_m, teal_center_lam = -0.866, 0.5
    dist_teal = np.sqrt((m - teal_center_m)**2 + (lam - teal_center_lam)**2)
    # Inverse square-ish or harmonic
    F_teal_m = -(m - teal_center_m) 
    F_teal_lam = -(lam - teal_center_lam)

    # 2. Calculate Red Force (Weak Force)
    # Modeled with Parity Violation (Asymmetry)
    # Basin center approx (0.0, -1.0)
    red_center_m, red_center_lam = 0.0, -1.0
    F_red_m = -(m - red_center_m)
    # The "Parity Kick" - Weak force acts differently on left/right
    p_violation = 0.5 * np.sin(m * 5) 
    F_red_lam = -(lam - red_center_lam) + p_violation

    # 3. The Free Rule: Gold = -(Teal + Red)
    # The Gold force is the "Slipknot Tension"
    F_gold_m = -(F_teal_m + F_red_m)
    F_gold_lam = -(F_teal_lam + F_red_lam)
    
    # ----------------------------------------
    # Basin Weighting (Where are we?)
    # ----------------------------------------
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Weights for blending
    w_gold = np.exp(-(min(abs(angle - 30), 360 - abs(angle - 30))/45)**2)
    w_teal = np.exp(-(min(abs(angle - 150), 360 - abs(angle - 150))/45)**2)
    w_red = np.exp(-(min(abs(angle - 270), 360 - abs(angle - 270))/45)**2)
    
    # Normalize weights
    total_w = w_gold + w_teal + w_red + 1e-6
    w_gold /= total_w
    w_teal /= total_w
    w_red /= total_w
    
    # ----------------------------------------
    # The Total Force
    # ----------------------------------------
    # We apply the forces based on where the particle is.
    # BUT, if we are in the Gold zone, we are governed by the Neutrality Constraint.
    
    Fm_total = (w_teal * F_teal_m) + (w_red * F_red_m) + (w_gold * F_gold_m)
    Flam_total = (w_teal * F_teal_lam) + (w_red * F_red_lam) + (w_gold * F_gold_lam)
    
    # Add the nonlinear Hénon-Heiles chaos background for the "Medium"
    # This represents the vacuum fluctuations
    Fm_chaos = -(m + 2*sigma*m*lam) * 0.2
    Flam_chaos = -(lam + sigma*(m**2 - lam**2)) * 0.2
    
    return Fm_total + Fm_chaos, Flam_total + Flam_chaos

def leapfrog_neutrality(m, lam, pm, plam, dt, sigma=1.0):
    Fm, Flam = get_neutrality_force(m, lam, sigma)
    
    pm_half = pm + 0.5 * dt * Fm
    plam_half = plam + 0.5 * dt * Flam
    
    m_new = m + dt * pm_half
    lam_new = lam + dt * plam_half
    
    Fm_new, Flam_new = get_neutrality_force(m_new, lam_new, sigma)
    
    pm_new = pm_half + 0.5 * dt * Fm_new
    plam_new = plam_half + 0.5 * dt * Flam_new
    
    return m_new, lam_new, pm_new, plam_new

def run_neutrality_knot():
    steps = 5000 
    dt = 0.01
    sigma = 1.0
    
    m_val, lam_val = 0.1, 0.1
    pm_val, plam_val = 0.4, 0.2
    
    traj_m, traj_lam, traj_t, colors = [], [], [], []
    t = 0
    
    print("Simulating Color Neutrality Slipknot...")
    
    for _ in range(steps):
        # Determine color for plotting
        angle = np.degrees(np.arctan2(lam_val, m_val)) % 360
        
        # Simple coloring logic
        w_gold = np.exp(-(min(abs(angle - 30), 360 - abs(angle - 30))/60)**2)
        w_teal = np.exp(-(min(abs(angle - 150), 360 - abs(angle - 150))/60)**2)
        w_red = np.exp(-(min(abs(angle - 270), 360 - abs(angle - 270))/60)**2)
        
        tot = w_gold + w_teal + w_red + 1e-6
        col = (
            (w_gold + w_red)/tot,       # R
            (w_gold*0.8 + w_teal)/tot,  # G
            (w_teal + w_red*0.2)/tot    # B
        )
        colors.append(col)
        
        m_val, lam_val, pm_val, plam_val = leapfrog_neutrality(m_val, lam_val, pm_val, plam_val, dt, sigma)
        
        traj_m.append(m_val)
        traj_lam.append(lam_val)
        traj_t.append(t)
        t += dt

    # Visualization
    traj_m = np.array(traj_m)
    traj_lam = np.array(traj_lam)
    traj_t = np.array(traj_t)
    colors = np.array(colors)
    
    fig = plt.figure(figsize=(10, 8), facecolor='black')
    
    # 1. The Slipknot (Top Down View)
    ax1 = fig.add_subplot(121, facecolor='black')
    points = np.array([traj_m, traj_lam]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    from matplotlib.collections import LineCollection
    lc = LineCollection(segments, colors=colors, linewidth=1, alpha=0.8)
    ax1.add_collection(lc)
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.axis('off')
    ax1.set_title("The Neutrality Slipknot\n(Top Down)", color='white')

    # 2. The Time Strand (3D)
    ax2 = fig.add_subplot(122, projection='3d', facecolor='black')
    for i in range(0, len(traj_m)-1, 2): # Skip steps for speed
        ax2.plot(traj_m[i:i+2], traj_lam[i:i+2], traj_t[i:i+2], color=colors[i], lw=1.5, alpha=0.6)
        
    ax2.set_axis_off()
    ax2.set_title("Color Confinement in Time\n(Yellow is purely emergent)", color='white')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_neutrality_knot()