import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 1.5    # Just past the crossover point in your graph
DT = 0.02
LAPS = 200     # Run for a long time to see the pattern
STEPS_PER_LAP = int(2 * np.pi / DT) * 2 # Approx steps for 1 lap

def get_force_poincare(m, lam):
    # Standard "Genesis" Force Setup
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    # The Twist that induces period doubling
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold = Tension (Vector Sum)
    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    # Basin Weighting
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    w_gold = gaussian(angle, 30, 80)
    w_teal = gaussian(angle, 150, 80)
    w_red = gaussian(angle, 270, 80)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    return Fm, Flam

def leapfrog_poincare(m, lam, pm, plam, dt):
    Fm, Flam = get_force_poincare(m, lam)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_poincare(m_n, lam_n)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def run_poincare():
    # Start in the "Gold" basin zone
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    
    # Poincaré Data Points
    # We record state when the particle crosses the m-axis (lam = 0)
    # This is like taking a strobe light photo of the particle
    crossings_m = []
    crossings_pm = []
    
    prev_lam = lam
    
    print(f"Generating Poincaré Map (Twist={TWIST})...")
    
    for i in range(LAPS * 1000): # Many steps
        m, lam, pm, plam = leapfrog_poincare(m, lam, pm, plam, DT)
        
        # Check for crossing of lambda=0 line (Section plane)
        if (prev_lam < 0 and lam >= 0) or (prev_lam > 0 and lam <= 0):
            # Interpolate exact crossing point for precision
            fraction = abs(prev_lam) / (abs(prev_lam) + abs(lam))
            m_cross = m # approx
            pm_cross = pm # approx
            
            crossings_m.append(m_cross)
            crossings_pm.append(pm_cross)
            
        prev_lam = lam

    # ----------------------------------------
    # VISUALIZATION
    # ----------------------------------------
    plt.figure(figsize=(8, 8), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Plot the dots
    # Alpha is low so we can see density
    plt.scatter(crossings_m, crossings_pm, c='cyan', s=10, alpha=0.6, edgecolors='none')
    
    plt.title(f"Poincaré Section (The Particle's Heartbeat)\nTwist={TWIST}", color='white', fontsize=14)
    plt.xlabel("Position (m)", color='white')
    plt.ylabel("Momentum (p_m)", color='white')
    
    plt.grid(color='#333333', linestyle=':')
    plt.tick_params(colors='white')
    
    # Interpretive Text
    plt.text(0.05, 0.95, "1 Cluster = Boson\n2 Clusters = Fermion\nRing/Cloud = Chaos", 
             transform=ax.transAxes, color='yellow', verticalalignment='top')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_poincare()