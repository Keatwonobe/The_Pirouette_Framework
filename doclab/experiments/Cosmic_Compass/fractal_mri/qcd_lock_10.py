import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETER SWEEP SETTINGS
# ----------------------------------------
TWIST_MIN = 0.0
TWIST_MAX = 5.0
SAMPLES = 100 
DT = 0.02
MAX_STEPS = 6000 # Cap to prevent infinite loops if it flies away

def get_force_scan(m, lam, twist):
    # Standard "Tension Mode" Setup
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    # Apply the variable twist
    p_violation = twist * np.sin(m * 2.5) 
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

def leapfrog_scan(m, lam, pm, plam, dt, twist):
    Fm, Flam = get_force_scan(m, lam, twist)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_scan(m_n, lam_n, twist)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def measure_mismatch(twist):
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    initial_state = np.array([m, lam, pm, plam])
    
    prev_angle = np.arctan2(lam, m)
    total_angle = 0.0
    
    mismatch_lap1 = None
    mismatch_lap2 = None
    
    lap_tracker = 0
    
    for i in range(MAX_STEPS):
        m, lam, pm, plam = leapfrog_scan(m, lam, pm, plam, DT, twist)
        
        # Angle Math
        curr_angle = np.arctan2(lam, m)
        delta = curr_angle - prev_angle
        if delta > np.pi: delta -= 2*np.pi
        if delta < -np.pi: delta += 2*np.pi
        total_angle += delta
        prev_angle = curr_angle
        
        curr_laps = int(abs(total_angle) / (2*np.pi))
        
        # Capture Lap 1 Data
        if curr_laps == 1 and mismatch_lap1 is None:
            curr_state = np.array([m, lam, pm, plam])
            mismatch_lap1 = np.linalg.norm(curr_state - initial_state)
            
        # Capture Lap 2 Data
        if curr_laps == 2 and mismatch_lap2 is None:
            curr_state = np.array([m, lam, pm, plam])
            mismatch_lap2 = np.linalg.norm(curr_state - initial_state)
            return mismatch_lap1, mismatch_lap2 # We got both, exit early
            
    # If we timed out before Lap 2
    return mismatch_lap1 if mismatch_lap1 else 10.0, 10.0

def run_scanner():
    twist_values = np.linspace(TWIST_MIN, TWIST_MAX, SAMPLES)
    lap1_scores = []
    lap2_scores = []
    
    print(f"Scanning {SAMPLES} Twist Factors...")
    
    for t in twist_values:
        l1, l2 = measure_mismatch(t)
        lap1_scores.append(l1)
        lap2_scores.append(l2)

    # ----------------------------------------
    # VISUALIZATION
    # ----------------------------------------
    plt.figure(figsize=(10, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    plt.plot(twist_values, lap1_scores, color='cyan', label='Lap 1 Mismatch (Boson Check)', linewidth=2)
    plt.plot(twist_values, lap2_scores, color='red', linestyle='--', label='Lap 2 Mismatch (Fermion Check)', linewidth=2)
    
    plt.title("The Stability Landscape: Hunting for Spin 1/2", color='white', fontsize=14)
    plt.xlabel("Twist Factor (Weak Force Asymmetry)", color='white')
    plt.ylabel("State Mismatch (Distance from Start)", color='white')
    
    plt.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
    plt.text(0, 0.6, "Stability Threshold", color='gray', fontsize=8)
    
    plt.grid(color='#333333')
    plt.legend(facecolor='black', labelcolor='white')
    plt.tick_params(colors='white')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_scanner()