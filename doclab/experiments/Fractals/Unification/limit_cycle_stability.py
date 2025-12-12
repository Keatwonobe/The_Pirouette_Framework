import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 3.8  # The "Fermion Plateau" Value
DT = 0.015
LAPS_TO_RUN = 100
# Approx steps per lap = 2*pi / (average angular velocity). 
# Let's assume angular velocity ~ 1 (natural units). 
# 2*pi/0.015 ~= 400 steps per lap. 
# 100 laps * 400 steps = 40,000 steps. Let's do 60,000 to be safe.
STEPS = 60000 

def get_force_limit_cycle(m, lam):
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak) - The Critical Asymmetry
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong) - Tension Mode
    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    # Basin Weighting
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Fast Gaussian
    diff_g = np.minimum(np.abs(angle - 30), 360 - np.abs(angle - 30))
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.minimum(np.abs(angle - 150), 360 - np.abs(angle - 150))
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.minimum(np.abs(angle - 270), 360 - np.abs(angle - 270))
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    return Fm, Flam

def leapfrog_limit_cycle(m, lam, pm, plam, dt):
    Fm, Flam = get_force_limit_cycle(m, lam)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_limit_cycle(m_n, lam_n)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def run_long_term_stability():
    # Initial Condition
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    
    # Store data
    traj_m = []
    traj_pm = []
    laps_list = []
    
    prev_angle = np.arctan2(lam, m)
    total_angle = 0.0
    
    print(f"Running Long-Term Stability Test ({LAPS_TO_RUN} laps)...")
    
    # Decimation factor for plotting (don't need every single point for 60k steps)
    DECIMATE = 5 
    
    for i in range(STEPS):
        m, lam, pm, plam = leapfrog_limit_cycle(m, lam, pm, plam, DT)
        
        # Angle Tracking
        curr_angle = np.arctan2(lam, m)
        delta = curr_angle - prev_angle
        if delta > np.pi: delta -= 2*np.pi
        if delta < -np.pi: delta += 2*np.pi
        total_angle += delta
        prev_angle = curr_angle
        
        current_laps = abs(total_angle) / (2*np.pi)
        
        if i % DECIMATE == 0:
            traj_m.append(m)
            traj_pm.append(pm)
            laps_list.append(current_laps)
            
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    traj_m = np.array(traj_m)
    traj_pm = np.array(traj_pm)
    laps_list = np.array(laps_list)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), facecolor='black')
    
    # Plot 1: The Phase Space Limit Cycle
    ax1.set_facecolor('black')
    
    # We color code by time: Blue = Early, Yellow/White = Late
    # This shows convergence
    sc = ax1.scatter(traj_m, traj_pm, c=laps_list, cmap='inferno', s=1, alpha=0.5)
    
    ax1.set_title(f"The Limit Cycle (Twist={TWIST})", color='white', fontsize=16)
    ax1.set_xlabel("Position (m)", color='white')
    ax1.set_ylabel("Momentum (p_m)", color='white')
    ax1.grid(color='#333333', alpha=0.5)
    ax1.tick_params(colors='white')
    
    # Plot 2: Stability Metric (Radius vs Time)
    ax2.set_facecolor('black')
    
    # Calculate Phase Space Radius (Energy proxy)
    radius = np.sqrt(traj_m**2 + traj_pm**2)
    
    ax2.plot(laps_list, radius, color='cyan', linewidth=0.5, alpha=0.8)
    
    ax2.set_title("Stability Metric: Radius Evolution", color='white', fontsize=16)
    ax2.set_xlabel("Laps", color='white')
    ax2.set_ylabel("Phase Space Radius", color='white')
    ax2.grid(color='#333333', alpha=0.5)
    ax2.tick_params(colors='white')
    
    # Interpretive Text
    ax2.text(0.5, 0.9, "If flat -> Stable Matter\nIf growing -> Decay", 
             transform=ax2.transAxes, color='yellow', ha='center', bbox=dict(facecolor='black', alpha=0.5))

    plt.tight_layout()
    plt.savefig('limit_cycle_stability.png')
    plt.show()

if __name__ == "__main__":
    run_long_term_stability()