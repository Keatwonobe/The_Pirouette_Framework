import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST_MIN = 0.0
TWIST_MAX = 4.0
RESOLUTION = 300    # High resolution to see the sharp steps
DT = 0.02
STEPS = 5000        # Long enough to average out the wobbles

def get_force_staircase(m, lam, twist):
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak)
    F_red_m = -(m - 0.0)
    # The variable twist
    p_violation = twist * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong) - Tension Mode
    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    # Basin Weighting
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Inline Gaussian
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

def leapfrog_staircase(m, lam, pm, plam, dt, twist):
    Fm, Flam = get_force_staircase(m, lam, twist)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_staircase(m_n, lam_n, twist)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def measure_spin(twist):
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    
    prev_angle = np.arctan2(lam, m)
    total_angle = 0.0
    
    for i in range(STEPS):
        m, lam, pm, plam = leapfrog_staircase(m, lam, pm, plam, DT, twist)
        
        curr_angle = np.arctan2(lam, m)
        delta = curr_angle - prev_angle
        if delta > np.pi: delta -= 2*np.pi
        if delta < -np.pi: delta += 2*np.pi
        
        total_angle += delta
        prev_angle = curr_angle
        
    # Calculate Average Winding Number
    # Winding = Total Radians / (2 * pi)
    # We divide by the number of 'natural' orbits to normalize if needed, 
    # but raw winding count per unit time is better for checking resonance.
    # Let's normalize it to the "Boson Base Frequency" (Twist=0 approx).
    
    winding_number = abs(total_angle) / (2*np.pi)
    
    # We want "Winding Ratio". Let's assume the low-twist boson is "1.0".
    # Since step count is fixed, we can just return the raw winding.
    return winding_number

def run_devils_staircase():
    twist_values = np.linspace(TWIST_MIN, TWIST_MAX, RESOLUTION)
    spin_values = []
    
    print(f"Scanning for Quantum Steps ({RESOLUTION} points)...")
    
    # First, get the baseline (Boson) winding at Twist=0 to normalize
    baseline = measure_spin(0.0)
    print(f"Baseline Boson Winding: {baseline:.2f} laps")
    
    for t in twist_values:
        raw_spin = measure_spin(t)
        # Normalize: Spin 1.0 = The Boson State
        normalized_spin = raw_spin / baseline
        spin_values.append(normalized_spin)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(12, 7), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    plt.plot(twist_values, spin_values, color='cyan', linewidth=2, drawstyle='steps-mid')
    
    plt.title("The Devil's Staircase: Quantization of Spin", color='white', fontsize=16)
    plt.xlabel("Twist Factor (Asymmetry)", color='white')
    plt.ylabel("Normalized Spin (Winding Ratio)", color='white')
    
    # Grid lines for the "Magic Numbers"
    for y in [1.0, 0.5, 0.33, 0.66]:
        plt.axhline(y=y, color='red', linestyle=':', alpha=0.3)
        plt.text(0, y+0.02, f"Spin {y}", color='red', fontsize=8)
        
    plt.grid(color='#333333', alpha=0.5)
    plt.tick_params(colors='white')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_devils_staircase()