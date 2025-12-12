import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 3.8  # The "Fermion Plateau" Value
DT = 0.015
STEPS = 2000 # Enough for 2-3 full cycles

def get_force_phase(m, lam):
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
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

def leapfrog_phase(m, lam, pm, plam, dt):
    Fm, Flam = get_force_phase(m, lam)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_phase(m_n, lam_n)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def run_phase_portrait():
    # Initial Condition
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    
    # Store data
    traj_m = []
    traj_pm = []
    colors = []
    
    prev_angle = np.arctan2(lam, m)
    total_angle = 0.0
    
    print(f"Generating Phase Portrait (Twist={TWIST})...")
    
    for i in range(STEPS):
        m, lam, pm, plam = leapfrog_phase(m, lam, pm, plam, DT)
        
        traj_m.append(m)
        traj_pm.append(pm)
        
        # Angle Tracking
        curr_angle = np.arctan2(lam, m)
        delta = curr_angle - prev_angle
        if delta > np.pi: delta -= 2*np.pi
        if delta < -np.pi: delta += 2*np.pi
        total_angle += delta
        prev_angle = curr_angle
        
        # Color Code by Lap Number
        laps = abs(total_angle) / (2*np.pi)
        
        if laps < 1.0:
            colors.append('cyan')  # Lap 1
        elif laps < 2.0:
            colors.append('red')   # Lap 2 (The Fold)
        elif laps < 3.0:
            colors.append('cyan')  # Lap 3 (Reset?)
        else:
            colors.append('red')   # Lap 4
            
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(10, 8), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Plot segments manually to handle colors
    # This is slower but necessary for segment coloring
    for i in range(len(traj_m)-1):
        plt.plot(traj_m[i:i+2], traj_pm[i:i+2], color=colors[i], linewidth=1.5, alpha=0.8)
        
    # Annotations
    plt.text(0.05, 0.95, "Cyan = Lap 1 (0-360°)\nRed = Lap 2 (360-720°)", 
             transform=ax.transAxes, color='white', bbox=dict(facecolor='black', alpha=0.5))
    
    plt.title(f"The Folded Attractor: Phase Space Portrait\n(Position vs Momentum)", color='white', fontsize=16)
    plt.xlabel("Mass Field Position (m)", color='white')
    plt.ylabel("Mass Field Momentum (p_m)", color='white')
    
    plt.grid(color='#333333', alpha=0.5)
    plt.tick_params(colors='white')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_phase_portrait()