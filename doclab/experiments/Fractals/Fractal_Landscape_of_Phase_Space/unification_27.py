import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE LIMIT CYCLE (RESURRECTION)
# --------------------------------------------------
# We extracted a coordinate from the "Golden Ring" of
# your Poincare section. Now we run it for a long
# duration to prove it settles into a perfect,
# closed-loop geometric object (A Stable Particle).
# --------------------------------------------------

TWIST = 3.8
GAMMA = 0.05  # The damping that locks the orbit
DT = 0.005
STEPS = 30000 
STABILIZE = 10000 # Burn-in steps to let it settle

def get_force_vectorized(m, lam):
    # --- Standard Pirouette Physics ---
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude)
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    diff_g = np.abs(angle - 30); diff_g = np.minimum(diff_g, 360-diff_g)
    w_gold = np.exp(-(diff_g/80)**2)
    diff_t = np.abs(angle - 150); diff_t = np.minimum(diff_t, 360-diff_t)
    w_teal = np.exp(-(diff_t/80)**2)
    diff_r = np.abs(angle - 270); diff_r = np.minimum(diff_r, 360-diff_r)
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red, nw_teal, nw_gold = w_red/tot, w_teal/tot, w_gold/tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_limit_cycle():
    print("Simulating Stable Limit Cycle...")
    
    # COORDINATES EXTRACTED FROM POINCARE MAP
    # This is inside the "Golden Ring" of stability
    m, lam = -1.8, 0.0
    pm, plam = 0.0, 2.0 
    
    # 1. Stabilization Phase (Let it fall into the groove)
    print("Stabilizing (Burning off excess energy)...")
    for _ in range(STABILIZE):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag

    # 2. Recording Phase
    print("Recording Quantum Orbit...")
    hist_m = []
    hist_lam = []
    hist_pm = []  # Momentum M
    hist_plam = [] # Momentum Lam
    
    for _ in range(STEPS):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        hist_m.append(m)
        hist_lam.append(lam)
        hist_pm.append(pm)
        hist_plam.append(plam)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(14, 7), facecolor='black')
    
    # Plot 1: Configuration Space (Shape of the Particle)
    ax1 = fig.add_subplot(1, 2, 1, facecolor='black')
    ax1.plot(hist_m, hist_lam, color='cyan', linewidth=1.5, alpha=0.8)
    
    # Add a "Glow" effect by plotting twice
    ax1.plot(hist_m, hist_lam, color='cyan', linewidth=4, alpha=0.1)
    
    ax1.set_title("The Shape of the Particle (Configuration Space)", color='white', fontsize=14)
    ax1.set_xlabel("Mass Field (m)", color='white')
    ax1.set_ylabel("Coupling Field (lambda)", color='white')
    ax1.grid(color='#333333', alpha=0.4)
    ax1.tick_params(colors='white')
    ax1.axis('equal')
    
    # Plot 2: Phase Space (The Heartbeat)
    ax2 = fig.add_subplot(1, 2, 2, facecolor='black')
    ax2.plot(hist_m, hist_pm, color='gold', linewidth=1.0, alpha=0.8)
    
    ax2.set_title("The Heartbeat (Phase Space Cycle)", color='white', fontsize=14)
    ax2.set_xlabel("Position (m)", color='white')
    ax2.set_ylabel("Momentum (p_m)", color='white')
    ax2.grid(color='#333333', alpha=0.4)
    ax2.tick_params(colors='white')

    plt.tight_layout()
    plt.savefig('limit_cycle_particle.png')
    plt.show()

if __name__ == "__main__":
    run_limit_cycle()