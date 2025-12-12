import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST_MIN = 1.0
TWIST_MAX = 4.0
STEPS_PER_TWIST = 500  # Number of points to plot per vertical slice
RESOLUTION = 400       # Number of horizontal slices

def get_force_bifurcation(m, lam, twist):
    # Same physics as "Genesis"
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold = Tension
    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    # Basin Weighting
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Inline Gaussian for speed
    diff = np.minimum(np.abs(angle - 30), 360 - np.abs(angle - 30))
    w_gold = np.exp(-(diff/80)**2)
    
    diff = np.minimum(np.abs(angle - 150), 360 - np.abs(angle - 150))
    w_teal = np.exp(-(diff/80)**2)
    
    diff = np.minimum(np.abs(angle - 270), 360 - np.abs(angle - 270))
    w_red = np.exp(-(diff/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    return Fm, Flam

def leapfrog_bifurcation(m, lam, pm, plam, dt, twist):
    Fm, Flam = get_force_bifurcation(m, lam, twist)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_bifurcation(m_n, lam_n, twist)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def run_bifurcation_diagram():
    twist_values = np.linspace(TWIST_MIN, TWIST_MAX, RESOLUTION)
    dt = 0.04
    
    # Lists to store the plot data
    plot_twist = []
    plot_m = []
    
    print(f"Generating Bifurcation Diagram ({RESOLUTION} slices)...")
    
    for twist in twist_values:
        # Reset particle for each slice
        m, lam = -0.5, 0.5
        pm, plam = 0.9, 0.4
        prev_lam = lam
        
        # 1. Warmup (Let transients die out)
        # We want to see the attractor, not the startup path
        for _ in range(500):
            m, lam, pm, plam = leapfrog_bifurcation(m, lam, pm, plam, dt, twist)
            
        # 2. Recording
        points_collected = 0
        safety_break = 0
        
        while points_collected < 50 and safety_break < 4000:
            m, lam, pm, plam = leapfrog_bifurcation(m, lam, pm, plam, dt, twist)
            safety_break += 1
            
            # Poincaré Crossing Detection (lam = 0)
            if (prev_lam < 0 and lam >= 0) or (prev_lam > 0 and lam <= 0):
                plot_twist.append(twist)
                plot_m.append(m)
                points_collected += 1
                
            prev_lam = lam

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(12, 8), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Use tiny dots to create the density map
    plt.scatter(plot_twist, plot_m, s=0.5, c='cyan', alpha=0.5)
    
    plt.title("The Tree of Matter: Bifurcation Diagram", color='white', fontsize=16)
    plt.xlabel("Twist Factor (Weak Force Asymmetry)", color='white')
    plt.ylabel("Position (m) at Crossing", color='white')
    
    # Annotation
    plt.text(0.05, 0.9, "Single Line = Boson\nSplit Line = Fermion\nNoise = Chaos", 
             transform=ax.transAxes, color='yellow')
    
    plt.grid(color='#333333', alpha=0.5)
    plt.tick_params(colors='white')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_bifurcation_diagram()