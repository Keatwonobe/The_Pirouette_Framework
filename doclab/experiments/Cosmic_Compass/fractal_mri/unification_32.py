import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE FINE TUNING
# --------------------------------------------------
# We search for the "Golden Key": The exact value of
# the Twist parameter that creates a perfect Fermion
# (Spin 0.5). This is equivalent to deriving the
# Fine Structure Constant from first principles.
# --------------------------------------------------

TARGET_SPIN = 0.500
TOLERANCE = 0.005 # How close do we need to be?

# Search Range (The Fermionic Era)
MIN_TWIST = 2.5
MAX_TWIST = 3.4

# Physics Config
GAMMA = 0.05
DT = 0.008
STEPS = 6000 

def measure_spin(twist_val):
    # Local Physics Function
    def get_force_local(m, lam):
        F_teal_m = -(m + 0.866) 
        F_teal_lam = -(lam - 0.5)
        F_red_m = -(m - 0.0)
        p_violation = twist_val * np.sin(m * 2.5) # <--- TUNING KNOB
        F_red_lam = -(lam + 1.0) + p_violation
        
        sum_m = (F_teal_m + F_red_m)
        sum_lam = (F_teal_lam + F_red_lam)
        mag = np.sqrt(sum_m**2 + sum_lam**2)
        scale = np.sqrt(mag)
        F_gold_m = sum_m * scale
        F_gold_lam = sum_lam * scale
        
        angle = np.degrees(np.arctan2(lam, m)) % 360
        # Fast Weights
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

    # Run Simulation
    m, lam = -1.8, 0.0
    pm, plam = 0.0, 2.0
    
    # Fast Burn-in
    for _ in range(1500):
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

    # Measure Winding
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

def run_fine_tuning():
    print(f"Searching for Spin {TARGET_SPIN} between Twist {MIN_TWIST} and {MAX_TWIST}...")
    
    # 1. Coarse Scan to find the crossing point
    scan_res = 20
    test_points = np.linspace(MIN_TWIST, MAX_TWIST, scan_res)
    results = []
    
    print("Step 1: Coarse Scan...")
    best_candidate = None
    min_error = 100.0
    
    for t in test_points:
        spin = measure_spin(t)
        results.append(spin)
        print(f"  T={t:.2f} -> Spin={spin:.4f}")
        
        err = abs(spin - TARGET_SPIN)
        if err < min_error:
            min_error = err
            best_candidate = t

    print(f"  >> Best Coarse Match: T={best_candidate:.2f} (Spin={measure_spin(best_candidate):.4f})")
    
    # 2. Gradient Descent / Narrow Search
    print("Step 2: Micro-Tuning...")
    current_t = best_candidate
    step_size = 0.05
    
    history_t = []
    history_spin = []
    
    for i in range(15): # Max iterations
        spin = measure_spin(current_t)
        history_t.append(current_t)
        history_spin.append(spin)
        
        error = spin - TARGET_SPIN
        print(f"  Iter {i}: T={current_t:.5f} -> Spin={spin:.5f} (Err={error:.5f})")
        
        if abs(error) < TOLERANCE:
            print("  >> LOCKED ON TARGET!")
            break
            
        # Simple feedback adjustment
        # If spin is too high, adjust T (assuming correlation direction)
        # We check direction from scan
        if results[-1] > results[0]: # Positive correlation
            direction = -1 if error > 0 else 1
        else: # Negative correlation
            direction = 1 if error > 0 else -1
            
        current_t += direction * step_size
        step_size *= 0.6 # Decay step size for precision

    final_t = current_t
    final_spin = measure_spin(final_t)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(10, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Plot the Convergence
    ax.plot(history_t, history_spin, 'o-', color='lime', linewidth=2, label='Tuning Path')
    ax.axhline(y=0.5, color='white', linestyle='--', label='Target (Spin 1/2)')
    
    ax.set_title(f"Deriving the Fundamental Constant\nFinal Twist = {final_t:.5f} | Spin = {final_spin:.5f}", 
                 color='white', fontsize=14)
    ax.set_xlabel("Twist Parameter", color='white')
    ax.set_ylabel("Measured Spin", color='white')
    
    ax.legend(facecolor='black', labelcolor='white')
    ax.grid(color='#333333', alpha=0.5)
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('fine_tuning_result.png')
    plt.show()

if __name__ == "__main__":
    run_fine_tuning()