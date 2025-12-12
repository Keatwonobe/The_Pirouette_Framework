import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE EDGE HUNTER
# --------------------------------------------------
# We identified a phase transition between Twist 2.83
# and 2.93 where the Spin flips from ~0.65 to ~0.29.
# The Spin 1/2 particle (0.50) must exist on this
# precise boundary (The Critical Point).
# --------------------------------------------------

# Zoomed in focus area
START_TWIST = 2.80
END_TWIST = 2.95
SAMPLES = 60  # Very high resolution step

GAMMA = 0.05
DT = 0.01
STEPS = 8000

def measure_spin_precise(twist_val):
    def get_force_local(m, lam):
        F_teal_m = -(m + 0.866) 
        F_teal_lam = -(lam - 0.5)
        F_red_m = -(m - 0.0)
        p_violation = twist_val * np.sin(m * 2.5)
        F_red_lam = -(lam + 1.0) + p_violation
        
        sum_m = (F_teal_m + F_red_m)
        sum_lam = (F_teal_lam + F_red_lam)
        mag = np.sqrt(sum_m**2 + sum_lam**2)
        scale = np.sqrt(mag)
        F_gold_m = sum_m * scale
        F_gold_lam = sum_lam * scale
        
        angle = np.degrees(np.arctan2(lam, m)) % 360
        # Weights
        diff_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30))
        w_gold = np.exp(-(diff_g/80)**2)
        diff_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150))
        w_teal = np.exp(-(diff_t/80)**2)
        diff_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270))
        w_red = np.exp(-(diff_r/80)**2)
        
        tot = w_gold + w_teal + w_red + 1e-6
        nw_red, nw_teal, nw_gold = w_red/tot, w_teal/tot, w_gold/tot
        
        Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
        Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
        return Fm, Flam, nw_red

    # Run Simulation
    m, lam = -1.8, 0.0
    pm, plam = 0.0, 2.0
    
    # Burn-in
    for _ in range(2000):
        Fm, Flam, w_red = get_force_local(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        Fm, Flam, w_red = get_force_local(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag

    # Measure
    total_phi = 0.0
    total_theta = 0.0
    prev_phi = np.arctan2(lam, m)
    prev_theta = np.arctan2(plam, pm)
    
    for _ in range(STEPS):
        Fm, Flam, w_red = get_force_local(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force_local(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        curr_phi = np.arctan2(lam, m)
        dphi = curr_phi - prev_phi
        if dphi > np.pi: dphi -= 2*np.pi
        if dphi < -np.pi: dphi += 2*np.pi
        total_phi += dphi
        prev_phi = curr_phi
        
        curr_theta = np.arctan2(plam, pm)
        dtheta = curr_theta - prev_theta
        if dtheta > np.pi: dtheta -= 2*np.pi
        if dtheta < -np.pi: dtheta += 2*np.pi
        total_theta += dtheta
        prev_theta = curr_theta
        
    if abs(total_phi) < 1e-3: return 0.0
    return abs(total_theta) / abs(total_phi)

def run_edge_hunter():
    print(f"Hunting for the Electron (Spin 0.5) in gap {START_TWIST}-{END_TWIST}...")
    
    twists = np.linspace(START_TWIST, END_TWIST, SAMPLES)
    spins = []
    
    closest_twist = 0
    closest_spin = 100
    min_err = 100
    
    for t in twists:
        s = measure_spin_precise(t)
        spins.append(s)
        
        err = abs(s - 0.5)
        if err < min_err:
            min_err = err
            closest_twist = t
            closest_spin = s
            
        print(f"T={t:.4f} -> Spin={s:.4f}")

    print("-" * 40)
    print(f"RESULTS:")
    print(f"Closest Match: Twist = {closest_twist:.5f}")
    print(f"Resulting Spin: {closest_spin:.5f}")
    print("-" * 40)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(10, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    ax.plot(twists, spins, 'o-', color='cyan', linewidth=2, label='Measured Spin')
    ax.axhline(y=0.5, color='lime', linestyle='--', linewidth=2, label='Target (0.5)')
    
    # Highlight the winner
    ax.plot(closest_twist, closest_spin, 'o', color='white', markersize=10, markeredgecolor='lime', markeredgewidth=2)
    
    ax.set_title(f"The Edge State: Crossing the Fermion Boundary\nConstant = {closest_twist:.5f}", color='white', fontsize=14)
    ax.set_xlabel("Twist Parameter", color='white')
    ax.set_ylabel("Spin Ratio", color='white')
    ax.legend(facecolor='black', labelcolor='white')
    ax.grid(color='#333333', alpha=0.5)
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('edge_hunter_result.png')
    plt.show()

if __name__ == "__main__":
    run_edge_hunter()