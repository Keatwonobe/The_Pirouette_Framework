import numpy as np
from scipy.optimize import minimize
from numba import njit

# =========================================================
#  THE QUARK HUNTER (Precision Gradient Descent)
#  Finds the exact coordinate of the Twist Singularity
# =========================================================

# --- PHYSICS PARAMETERS ---
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 1000  # High steps for precision winding count

@njit
def get_force_weights(m, lam):
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    angle_deg = np.degrees(np.arctan2(lam, m)) % 360.0

    diff_g = min(abs(angle_deg - 30.0), 360.0 - abs(angle_deg - 30.0))
    w_gold = np.exp(-(diff_g / 80.0)**2)

    diff_t = min(abs(angle_deg - 150.0), 360.0 - abs(angle_deg - 150.0))
    w_teal = np.exp(-(diff_t / 80.0)**2)

    diff_r = min(abs(angle_deg - 270.0), 360.0 - abs(angle_deg - 270.0))
    w_red  = np.exp(-(diff_r / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6
    
    # Return dominant force vector and red weight
    Fm   = (w_teal/tot)*F_teal_m + (w_red/tot)*F_red_m + (w_gold/tot)*F_gold_m
    Flam = (w_teal/tot)*F_teal_lam + (w_red/tot)*F_red_lam + (w_gold/tot)*F_gold_lam
    
    return Fm, Flam, (w_red/tot)

@njit
def measure_vorticity_and_redness(params):
    """
    Objective function to MAXIMIZE.
    Returns -(Winding Number * Red_Intensity) 
    (Negative because scipy minimizes)
    """
    m0, l0 = params[0], params[1]
    
    m, l = m0, l0
    pm, pl = 0.0, 0.0
    
    total_red = 0.0
    prev_angle = np.arctan2(l, m)
    total_winding = 0.0
    
    for i in range(MAX_STEPS):
        Fm, Flam, w_red = get_force_weights(m, l)
        
        total_red += w_red
        
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        pl = (pl + 0.5 * DT * Flam) * drag
        m += DT * pm
        l += DT * pl
        
        curr_angle = np.arctan2(l, m)
        d_angle = curr_angle - prev_angle
        if d_angle > np.pi: d_angle -= 2*np.pi
        if d_angle < -np.pi: d_angle += 2*np.pi
        total_winding += d_angle
        prev_angle = curr_angle
        
        # Divergence check
        if (m*m + l*l) > 100.0:
            break

    avg_red = total_red / (i + 1)
    abs_winding = np.abs(total_winding) / (2 * np.pi)
    
    # We want to find the spot with high winding AND high twist force
    score = abs_winding * avg_red
    
    return -score # Return negative for minimization

def hunt_quark():
    print("--- 🦅 HUNTING THE QUARK SINGULARITY ---")
    
    # Grid search to find a good starting point (The "Rough Scan")
    print("Step 1: Coarse Grid Search...")
    best_score = 0
    start_guess = [0.0, 0.0]
    
    # Scan the central region where we saw the "Eye"
    scan_range = np.linspace(-1.0, 1.0, 20)
    
    for m in scan_range:
        for l in scan_range:
            # Note: measure_vorticity returns negative score
            score = -measure_vorticity_and_redness(np.array([m, l]))
            if score > best_score:
                best_score = score
                start_guess = [m, l]
                
    print(f"  Best Rough Guess: m={start_guess[0]:.3f}, l={start_guess[1]:.3f} (Score: {best_score:.3f})")
    
    # Optimizer (The "Precision Drill")
    print("Step 2: Precision Optimization...")
    result = minimize(measure_vorticity_and_redness, start_guess, method='Nelder-Mead', tol=1e-6)
    
    quark_m, quark_l = result.x
    final_score = -result.fun
    
    print("\n--- 🎯 TARGET ACQUIRED ---")
    print(f"Quark Core Location:")
    print(f"  m (Mass Field)     = {quark_m:.8f}")
    print(f"  λ (Coupling Field) = {quark_l:.8f}")
    print(f"  Vorticity Score    = {final_score:.4f}")
    
    print("\nNext Step: Plug these coordinates into the holographic projector?")

if __name__ == "__main__":
    # Compile JIT
    measure_vorticity_and_redness(np.array([0.1, 0.1]))
    hunt_quark()