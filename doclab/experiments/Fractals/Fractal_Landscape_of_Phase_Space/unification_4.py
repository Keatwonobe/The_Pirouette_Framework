import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PHYSICS CONSTANTS
# ----------------------------------------
TARGET_ANGLE = 0.23122
TOLERANCE = 0.0005     # Precision target
TWIST = 3.8
DT = 0.005
BATCH_STEPS = 15000    # Steps per measurement attempt
H_BAR_SIM = 77.41389   # Calibration unit

def get_force_tunable(m, lam, gamma_val):
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak) - Twisted
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong) - Nonlinear Confinement
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude) if magnitude > 1e-6 else 0
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights for Drag application
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Inline Gaussian
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    w_gold = gaussian(angle, 30, 80)
    w_teal = gaussian(angle, 150, 80)
    w_red = gaussian(angle, 270, 80)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    # Net Force
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    # Metrics
    E_teal = (F_teal_m**2 + F_teal_lam**2)
    E_red  = (F_red_m**2 + F_red_lam**2)
    
    return Fm, Flam, E_teal, E_red, nw_red

def leapfrog_tunable(m, lam, pm, plam, dt, gamma_val):
    Fm, Flam, Et, Er, w_red = get_force_tunable(m, lam, gamma_val)
    
    # Apply Higgs Drag to momentum
    drag = 1.0 / (1.0 + 0.5 * dt * gamma_val * w_red)
    
    pm_h = (pm + 0.5 * dt * Fm) * drag
    plam_h = (plam + 0.5 * dt * Flam) * drag
    
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    
    Fm_n, Flam_n, Et_n, Er_n, w_red_n = get_force_tunable(m_n, lam_n, gamma_val)
    drag_n = 1.0 / (1.0 + 0.5 * dt * gamma_val * w_red_n)
    
    pm_n = (pm_h + 0.5 * dt * Fm_n) * drag_n
    plam_n = (plam_h + 0.5 * dt * Flam_n) * drag_n
    
    return m_n, lam_n, pm_n, plam_n, Et, Er

def fine_tune_higgs():
    # Start with our best guess
    current_gamma = 0.11
    
    # PID Controller settings for the tuner
    kp = 2.0  # Proportional gain
    
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    
    print(f"FINE TUNING HIGGS VISCOSITY")
    print(f"Target Sin^2(theta): {TARGET_ANGLE}")
    print("-" * 65)
    print(f"{'Iter':<5} | {'Gamma':<10} | {'Weinberg Angle':<15} | {'Error':<10} | {'Mass (Action)'}")
    print("-" * 65)
    
    # Warmup
    for _ in range(5000):
        m, lam, pm, plam, _, _ = leapfrog_tunable(m, lam, pm, plam, DT, current_gamma)
        
    for iteration in range(20): # Max 20 adjustments
        hist_Et = []
        hist_Er = []
        
        hist_m = []
        hist_lam = []
        hist_pm = []
        hist_plam = []
        
        # Run Batch
        for _ in range(BATCH_STEPS):
            m, lam, pm, plam, Et, Er = leapfrog_tunable(m, lam, pm, plam, DT, current_gamma)
            hist_Et.append(Et)
            hist_Er.append(Er)
            
            hist_m.append(m)
            hist_lam.append(lam)
            hist_pm.append(pm)
            hist_plam.append(plam)
            
        # Calculate Angle
        avg_Et = np.mean(hist_Et)
        avg_Er = np.mean(hist_Er)
        current_angle = avg_Et / (avg_Et + avg_Er)
        
        # Calculate Mass (Action) for this state
        m_arr = np.array(hist_m)
        lam_arr = np.array(hist_lam)
        pm_arr = np.array(hist_pm)
        plam_arr = np.array(hist_plam)
        dm = np.diff(m_arr)
        dlam = np.diff(lam_arr)
        action_total = np.sum(pm_arr[:-1] * dm) + np.sum(plam_arr[:-1] * dlam)
        angle_unwrap = np.unwrap(np.arctan2(lam_arr, m_arr))
        cycles = (angle_unwrap[-1] - angle_unwrap[0]) / (4*np.pi)
        if cycles < 1: cycles=1
        action_calib = (abs(action_total) / cycles) / H_BAR_SIM
        
        error = current_angle - TARGET_ANGLE
        
        print(f"{iteration:<5} | {current_gamma:<10.5f} | {current_angle:<15.5f} | {error:<10.5f} | {action_calib:.4f}")
        
        if abs(error) < TOLERANCE:
            print(">> CONVERGENCE ACHIEVED <<")
            break
            
        # Adjustment Logic:
        # If Angle is too HIGH (0.30), we have too much Teal energy relative to Red.
        # We need to suppress Red? No, suppression reduces Red energy.
        # Wait: angle = Et / (Et + Er).
        # To LOWER angle, we need to INCREASE Er relative to Et.
        # Or DECREASE Et.
        # Higgs drag applies to RED.
        # If we increase Drag, velocity in Red drops -> Force/Energy in Red drops?
        # Actually, if we increase drag, the particle spends MORE time fighting the Red twist?
        # Let's trust the gradient: previous scan showed Higher Gamma -> Lower Angle.
        # So if Error > 0 (Angle too high), we need MORE Gamma.
        
        adjustment = error * kp
        current_gamma += adjustment
        
        # Safety clamps
        if current_gamma < 0.0: current_gamma = 0.001
        if current_gamma > 0.5: current_gamma = 0.5

    print("-" * 65)
    print(f"FINAL HIGGS VISCOSITY: {current_gamma:.6f}")
    
    return current_gamma

if __name__ == "__main__":
    fine_tune_higgs()