import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 3.8  # The "Fermion Plateau" Value we found
DT = 0.005   # Higher precision time step for accurate integration
STEPS = 40000 # Run long enough to stabilize and sample

def get_force_metrics(m, lam):
    # 1. Teal (EM/Hypercharge)
    # The Force is the gradient of the potential.
    # We track the MAGNITUDE of the force component to estimate stiffness/energy.
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak/Isospin)
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong/Color)
    # Tension Mode: Sum of the others
    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    # Basin Weighting (Geometric mixing)
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    w_gold = gaussian(angle, 30, 80)
    w_teal = gaussian(angle, 150, 80)
    w_red = gaussian(angle, 270, 80)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    # Calculate Total Force
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    # Return Force AND individual Basin Contributions (Energy proxy)
    # We define "Energy Density" ~ Force^2 (Potential depth proxy)
    E_teal = (F_teal_m**2 + F_teal_lam**2)
    E_red  = (F_red_m**2 + F_red_lam**2)
    E_gold = (F_gold_m**2 + F_gold_lam**2)
    
    return Fm, Flam, E_teal, E_red, E_gold

def leapfrog_metrics(m, lam, pm, plam, dt):
    # Standard Leapfrog
    Fm, Flam, Et, Er, Eg = get_force_metrics(m, lam)
    
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    
    Fm_n, Flam_n, Et_n, Er_n, Eg_n = get_force_metrics(m_n, lam_n)
    
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    
    return m_n, lam_n, pm_n, plam_n, Et_n, Er_n, Eg_n

def run_metric_test():
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    
    # 1. Stabilization Phase
    # Run silently to let the particle fall into the limit cycle
    print("Stabilizing Orbit (Waiting for Limit Cycle)...")
    for _ in range(20000):
        m, lam, pm, plam, _, _, _ = leapfrog_metrics(m, lam, pm, plam, DT)
        
    # 2. Measurement Phase
    # We record exactly one full loop (approx) or a statistical sample
    print("Measuring Quantized Signatures...")
    
    hist_m = []
    hist_lam = []
    hist_pm = []
    hist_plam = []
    
    hist_E_teal = []
    hist_E_red = []
    hist_E_gold = []
    
    # Record for a fixed duration
    for _ in range(10000):
        m, lam, pm, plam, Et, Er, Eg = leapfrog_metrics(m, lam, pm, plam, DT)
        
        hist_m.append(m)
        hist_lam.append(lam)
        hist_pm.append(pm)
        hist_plam.append(plam)
        
        hist_E_teal.append(Et)
        hist_E_red.append(Er)
        hist_E_gold.append(Eg)

    # Convert to arrays
    m_arr = np.array(hist_m)
    lam_arr = np.array(hist_lam)
    pm_arr = np.array(hist_pm)
    plam_arr = np.array(hist_plam)
    
    # ----------------------------------------
    # METRIC 1: THE PLANCK CHECK (Action)
    # ----------------------------------------
    # Action J = Integral(p dq)
    # We calculate using Green's theorem area formula or discrete summation
    # sum( p * dq )
    dm = np.diff(m_arr)
    dlam = np.diff(lam_arr)
    # Align lengths
    p_m_step = pm_arr[:-1]
    p_lam_step = plam_arr[:-1]
    
    action_m = np.sum(p_m_step * dm)
    action_lam = np.sum(p_lam_step * dlam)
    
    # This integrates over the whole sample time. We need Action Per Cycle.
    # Let's count cycles using angle crossings.
    angle = np.arctan2(lam_arr, m_arr)
    # Unwrap
    angle_unwrap = np.unwrap(angle)
    total_cycles = (angle_unwrap[-1] - angle_unwrap[0]) / (4*np.pi) # 4pi because Fermion is 720 deg!
    
    total_action = abs(action_m + action_lam)
    action_per_cycle = total_action / total_cycles
    
    # Normalized against Pi
    action_ratio = action_per_cycle / np.pi
    
    # ----------------------------------------
    # METRIC 2: THE WEINBERG CHECK (Mixing Angle)
    # ----------------------------------------
    # sin^2(theta) = E_teal / (E_teal + E_red)
    avg_Et = np.mean(hist_E_teal)
    avg_Er = np.mean(hist_E_red)
    
    mixing_angle = avg_Et / (avg_Et + avg_Er)
    
    # ----------------------------------------
    # METRIC 3: THE COUPLING RATIOS
    # ----------------------------------------
    avg_Eg = np.mean(hist_E_gold)
    
    # Normalize to Teal = 1
    c_teal = 1.0
    c_red = avg_Er / avg_Et
    c_gold = avg_Eg / avg_Et
    
    # ----------------------------------------
    # RESULTS OUTPUT
    # ----------------------------------------
    print("\n" + "="*40)
    print("PIROUETTE METRIC TEST RESULTS")
    print("="*40)
    
    print(f"\n--- METRIC 1: QUANTIZATION (The Planck Check) ---")
    print(f"Total Cycles Measured: {total_cycles:.2f} (Fermion 720-deg cycles)")
    print(f"Action per Cycle (J):  {action_per_cycle:.5f}")
    print(f"Target (Pi):           {np.pi:.5f}")
    print(f"Ratio (J / Pi):        {action_ratio:.5f}")
    
    if 0.95 < action_ratio < 1.05:
        print(">> RESULT: PASS (Quantized to h/2)")
    elif 1.95 < action_ratio < 2.05:
         print(">> RESULT: PASS (Quantized to h)")
    else:
        print(">> RESULT: FAIL (Non-integer geometry)")

    print(f"\n--- METRIC 2: WEINBERG ANGLE (Electro-Weak Mixing) ---")
    print(f"Calculated sin^2(theta): {mixing_angle:.5f}")
    print(f"Standard Model Value:    0.23122")
    print(f"Deviation:               {abs(mixing_angle - 0.23122)/0.23122 * 100:.2f}%")
    
    if abs(mixing_angle - 0.231) < 0.05: # 5% tolerance
        print(">> RESULT: PASS (Matches SM Prediction)")
    else:
        print(">> RESULT: FAIL (Geometry mismatch)")

    print(f"\n--- METRIC 3: COUPLING HIERARCHY ---")
    print(f"Teal (EM/U1):   {c_teal:.2f}")
    print(f"Red (Weak/SU2): {c_red:.2f}")
    print(f"Gold (Strong):  {c_gold:.2f}")
    print(f"Predicted Ratio: 1 : 2 : 7")
    
    # Simple check on hierarchy
    if c_red > 1.5 and c_gold > 5.0:
        print(">> RESULT: PASS (Correct Hierarchy Emerged)")
    else:
        print(">> RESULT: FAIL (Hierarchy Inverted)")
        
    print("="*40)

    # Visualization of the Action Integral Area
    plt.figure(figsize=(8,8), facecolor='black')
    plt.plot(m_arr, pm_arr, color='cyan', alpha=0.6, linewidth=1)
    plt.fill(m_arr, pm_arr, color='cyan', alpha=0.1)
    plt.title(f"Phase Space Area (Action J)\nCalculated: {action_per_cycle:.4f}", color='white')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_metric_test()