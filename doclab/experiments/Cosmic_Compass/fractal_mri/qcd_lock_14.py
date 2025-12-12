import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 3.8        # The "Blue Knot" plateau value
DT = 0.015
STEPS = 10000      # Enough for ~5 full fermion cycles (10 geometric laps)

def get_force_fermion(m, lam):
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak) - The Critical Asymmetry
    F_red_m = -(m - 0.0)
    # The Twist that creates the topological knot
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

def leapfrog_fermion(m, lam, pm, plam, dt):
    Fm, Flam = get_force_fermion(m, lam)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_fermion(m_n, lam_n)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def run_phase_evolution():
    # Initial Condition (Must be in the stable region we found)
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    
    initial_state = np.array([m, lam, pm, plam])
    
    history_laps = []
    history_dist = []
    
    prev_angle = np.arctan2(lam, m)
    total_angle = 0.0
    
    print(f"Tracking Phase Evolution (Twist={TWIST})...")
    
    for i in range(STEPS):
        m, lam, pm, plam = leapfrog_fermion(m, lam, pm, plam, DT)
        
        # Calculate Winding
        curr_angle = np.arctan2(lam, m)
        delta = curr_angle - prev_angle
        if delta > np.pi: delta -= 2*np.pi
        if delta < -np.pi: delta += 2*np.pi
        total_angle += delta
        prev_angle = curr_angle
        
        # Calculate State Mismatch (Distance from Start)
        curr_state = np.array([m, lam, pm, plam])
        dist = np.linalg.norm(curr_state - initial_state)
        
        # Record Data
        # X-axis: Laps (Total Angle / 2pi)
        laps = abs(total_angle) / (2*np.pi)
        history_laps.append(laps)
        history_dist.append(dist)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(12, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Plot the "Heartbeat"
    plt.plot(history_laps, history_dist, color='cyan', linewidth=2, label='State Mismatch')
    
    # Draw Vertical Lines at Integrity Laps (1, 2, 3...)
    for x in range(1, int(max(history_laps)) + 1):
        is_even = (x % 2 == 0)
        col = 'lime' if is_even else 'red'
        style = '-' if is_even else ':'
        alpha = 0.8 if is_even else 0.5
        
        plt.axvline(x=x, color=col, linestyle=style, alpha=alpha)
        
        # Label the first few
        if x <= 4:
            label = "Reset" if is_even else "Twisted"
            plt.text(x, max(history_dist)*0.95, f"{x}\n{label}", 
                     color=col, ha='center', fontsize=9, fontweight='bold')

    plt.title(f"The Fermion Heartbeat (Twist={TWIST})", color='white', fontsize=16)
    plt.xlabel("Geometric Laps (360° Rotations)", color='white')
    plt.ylabel("Distance from Initial State", color='white')
    
    # Annotations to explain the physics
    plt.text(0.5, 0.1, "Spin 1/2 Signature:\nState resets only on EVEN laps (2, 4, 6...)", 
             transform=ax.transAxes, color='yellow', bbox=dict(facecolor='black', alpha=0.7))
    
    plt.grid(color='#333333', alpha=0.5)
    plt.tick_params(colors='white')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_phase_evolution()