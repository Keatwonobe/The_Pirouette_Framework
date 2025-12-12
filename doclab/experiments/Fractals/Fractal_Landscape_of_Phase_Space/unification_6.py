import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 3.8
DT = 0.005
H_BAR_SIM = 77.41389

# HYSTERESIS SCAN SETTINGS
GAMMA_MAX = 0.6
SCAN_STEPS = 300  # Number of gamma increments up and down
STEPS_PER_GAMMA = 3000 # Steps to evolve at each gamma level

def get_force_cooling(m, lam):
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak)
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong) - Nonlinear
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude) if magnitude > 1e-6 else 0
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
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
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    # Energy Densities
    E_teal = (F_teal_m**2 + F_teal_lam**2)
    E_red  = (F_red_m**2 + F_red_lam**2)
    
    return Fm, Flam, E_teal, E_red, nw_red

def leapfrog_cooling(m, lam, pm, plam, dt, gamma):
    Fm, Flam, Et, Er, w_red = get_force_cooling(m, lam)
    
    # Higgs Drag
    drag = 1.0 / (1.0 + 0.5 * dt * gamma * w_red)
    
    pm_h = (pm + 0.5 * dt * Fm) * drag
    plam_h = (plam + 0.5 * dt * Flam) * drag
    
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    
    Fm_n, Flam_n, Et_n, Er_n, w_red_n = get_force_cooling(m_n, lam_n)
    drag_n = 1.0 / (1.0 + 0.5 * dt * gamma * w_red_n)
    
    pm_n = (pm_h + 0.5 * dt * Fm_n) * drag_n
    plam_n = (plam_h + 0.5 * dt * Flam_n) * drag_n
    
    return m_n, lam_n, pm_n, plam_n, Et, Er

def run_cooling_universe():
    # Phase 1: Cooling (Gamma 0 -> Max)
    # Phase 2: Reheating (Gamma Max -> 0)
    gamma_up = np.linspace(0.0, GAMMA_MAX, SCAN_STEPS)
    gamma_down = np.linspace(GAMMA_MAX, 0.0, SCAN_STEPS)
    
    # Combined profile
    gamma_profile = np.concatenate([gamma_up, gamma_down])
    
    # Storage
    mass_history = []
    angle_history = []
    gamma_history = []
    phase_history = [] # 0 for cooling, 1 for heating
    
    # Initial Condition (Hot Universe)
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    
    print(f"Simulating The Cooling Universe ({len(gamma_profile)} epochs)...")
    
    for i, gamma in enumerate(gamma_profile):
        # We do NOT reset m, lam, pm, plam. The particle evolves.
        
        # Integrate for this epoch
        hist_Et = []
        hist_Er = []
        
        # Action accumulation
        action_accum = 0.0
        prev_ang = np.arctan2(lam, m)
        total_ang_disp = 0.0
        
        for _ in range(STEPS_PER_GAMMA):
            m_old, lam_old = m, lam
            m, lam, pm, plam, Et, Er = leapfrog_cooling(m, lam, pm, plam, DT, gamma)
            
            hist_Et.append(Et)
            hist_Er.append(Er)
            
            dq_m = m - m_old
            dq_lam = lam - lam_old
            action_accum += (pm * dq_m + plam * dq_lam)
            
            curr_ang = np.arctan2(lam, m)
            delta = curr_ang - prev_ang
            if delta > np.pi: delta -= 2*np.pi
            if delta < -np.pi: delta += 2*np.pi
            total_ang_disp += delta
            prev_ang = curr_ang
            
        # Metrics
        cycles = abs(total_ang_disp) / (4*np.pi)
        if cycles < 0.5: cycles = 0.5 # Avoid div/0 if frozen
        
        calib_mass = (abs(action_accum) / cycles) / H_BAR_SIM
        
        avg_Et = np.mean(hist_Et)
        avg_Er = np.mean(hist_Er)
        theta_w = avg_Et / (avg_Et + avg_Er)
        
        mass_history.append(calib_mass)
        angle_history.append(theta_w)
        gamma_history.append(gamma)
        phase_history.append(0 if i < SCAN_STEPS else 1)
        
        if i % 50 == 0:
            print(f"Epoch {i}/{len(gamma_profile)}: Gamma={gamma:.3f}, Mass={calib_mass:.3f}")

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), facecolor='black')
    
    # Split data into Cooling (Blue) and Heating (Red)
    split = SCAN_STEPS
    
    # 1. Mass Hysteresis
    ax1.set_facecolor('black')
    ax1.plot(gamma_history[:split], mass_history[:split], color='cyan', label='Cooling (Condensation)')
    ax1.plot(gamma_history[split:], mass_history[split:], color='red', linestyle='--', label='Reheating (Melting)')
    
    ax1.set_ylabel('Particle Mass (Action)', color='white')
    ax1.set_title("Hysteresis of the Vacuum: Mass Generation", color='white', fontsize=14)
    ax1.grid(color='#333333', alpha=0.5)
    ax1.tick_params(colors='white')
    ax1.legend(facecolor='black', labelcolor='white')
    
    # 2. Angle Hysteresis
    ax2.set_facecolor('black')
    ax2.plot(gamma_history[:split], angle_history[:split], color='cyan', label='Cooling')
    ax2.plot(gamma_history[split:], angle_history[split:], color='red', linestyle='--', label='Reheating')
    
    ax2.set_xlabel('Higgs Viscosity (Gamma)', color='white')
    ax2.set_ylabel('Weinberg Angle', color='white')
    ax2.grid(color='#333333', alpha=0.5)
    ax2.tick_params(colors='white')
    
    # Target Line
    ax2.axhline(y=0.231, color='white', linestyle=':', alpha=0.5, label='Standard Model')
    ax2.legend(facecolor='black', labelcolor='white')

    plt.tight_layout()
    plt.savefig('cooling_universe_hysteresis.png')
    plt.show()

if __name__ == "__main__":
    run_cooling_universe()