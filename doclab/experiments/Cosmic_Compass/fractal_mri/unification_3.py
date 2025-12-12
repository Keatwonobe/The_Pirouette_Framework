import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 3.8
DT = 0.005
STEPS = 25000  # Sufficient for stabilization + measurement
H_BAR_SIM = 77.41389

# Scan Parameters
GAMMA_MIN = 0.0
GAMMA_MAX = 0.5
SAMPLES = 20

def get_force_higgs(m, lam):
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
    
    # Basin Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    w_gold = gaussian(angle, 30, 80)
    w_teal = gaussian(angle, 150, 80)
    w_red = gaussian(angle, 270, 80)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    # Normalized weights for the force mixing
    nw_gold = w_gold / tot
    nw_teal = w_teal / tot
    nw_red = w_red / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    # Energy Densities (Force^2 proxy)
    E_teal = (F_teal_m**2 + F_teal_lam**2)
    E_red  = (F_red_m**2 + F_red_lam**2)
    
    # Return the 'Red Weight' specifically for the Higgs Drag
    return Fm, Flam, E_teal, E_red, nw_red

def leapfrog_higgs(m, lam, pm, plam, dt, gamma):
    # 1. Get Force and Red Weight at current position
    Fm, Flam, Et, Er, w_red = get_force_higgs(m, lam)
    
    # 2. Apply "Higgs Viscosity"
    # Drag is proportional to velocity (p) AND the Red Basin Weight
    # F_drag = -gamma * w_red * v
    # We apply this as a modification to the Force effectively, or directly to momentum update.
    # Standard semi-implicit Euler for drag: v_new = v_old + (F - gamma*v)*dt
    # -> v_new = (v_old + F*dt) / (1 + gamma*dt)
    
    # Let's integrate it into the Half-Kick
    # pm_half_pred = pm + 0.5 * dt * Fm
    # pm_half = pm_half_pred / (1.0 + 0.5 * dt * gamma * w_red)
    
    drag_factor = 1.0 / (1.0 + 0.5 * dt * gamma * w_red)
    
    pm_h = (pm + 0.5 * dt * Fm) * drag_factor
    plam_h = (plam + 0.5 * dt * Flam) * drag_factor
    
    # Drift
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    
    # Re-evaluate Force at new position
    Fm_n, Flam_n, Et_n, Er_n, w_red_n = get_force_higgs(m_n, lam_n)
    
    # Second Half-Kick with Drag
    drag_factor_n = 1.0 / (1.0 + 0.5 * dt * gamma * w_red_n)
    
    pm_n = (pm_h + 0.5 * dt * Fm_n) * drag_factor_n
    plam_n = (plam_h + 0.5 * dt * Flam_n) * drag_factor_n
    
    return m_n, lam_n, pm_n, plam_n, Et_n, Er_n

def run_viscosity_scan():
    gamma_values = np.linspace(GAMMA_MIN, GAMMA_MAX, SAMPLES)
    
    weinberg_angles = []
    actions = []
    
    print(f"Scanning Higgs Viscosity (Gamma 0.0 -> {GAMMA_MAX})...")
    
    for gamma in gamma_values:
        # Reset Particle
        m, lam = -0.5, 0.5
        pm, plam = 0.9, 0.4
        
        # Stabilization
        # Viscosity actually helps stabilization, so 10k steps should be plenty
        for _ in range(10000):
            m, lam, pm, plam, _, _ = leapfrog_higgs(m, lam, pm, plam, DT, gamma)
            
        # Measurement Loop
        hist_Et = []
        hist_Er = []
        hist_m = []
        hist_lam = []
        hist_pm = []
        hist_plam = []
        
        for _ in range(8000): # Measure for a while
            m, lam, pm, plam, Et, Er = leapfrog_higgs(m, lam, pm, plam, DT, gamma)
            hist_Et.append(Et)
            hist_Er.append(Er)
            hist_m.append(m)
            hist_lam.append(lam)
            hist_pm.append(pm)
            hist_plam.append(plam)
            
        # Calculate Metrics
        # 1. Weinberg Angle
        avg_Et = np.mean(hist_Et)
        avg_Er = np.mean(hist_Er)
        theta_W = avg_Et / (avg_Et + avg_Er)
        weinberg_angles.append(theta_W)
        
        # 2. Action (Mass)
        m_arr = np.array(hist_m)
        lam_arr = np.array(hist_lam)
        pm_arr = np.array(hist_pm)
        plam_arr = np.array(hist_plam)
        
        dm = np.diff(m_arr)
        dlam = np.diff(lam_arr)
        action_total = np.sum(pm_arr[:-1] * dm) + np.sum(plam_arr[:-1] * dlam)
        
        angle = np.unwrap(np.arctan2(lam_arr, m_arr))
        cycles = (angle[-1] - angle[0]) / (4*np.pi)
        if cycles < 1.0: cycles = 1.0 # Safety
        
        raw_action = abs(action_total) / cycles
        calibrated_action = raw_action / H_BAR_SIM
        actions.append(calibrated_action)
        
        print(f"Gamma {gamma:.3f}: Angle={theta_W:.3f}, Action={calibrated_action:.3f}")

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig, ax1 = plt.subplots(figsize=(10, 6), facecolor='black')
    ax1.set_facecolor('black')
    
    # Plot Weinberg Angle (Left Axis)
    ax1.plot(gamma_values, weinberg_angles, color='cyan', marker='o', label='Weinberg Angle')
    ax1.set_xlabel('Higgs Viscosity (Gamma)', color='white')
    ax1.set_ylabel('Sin^2(Theta_W)', color='cyan')
    ax1.tick_params(axis='y', labelcolor='cyan', colors='white')
    ax1.tick_params(axis='x', colors='white')
    
    # Target Line
    ax1.axhline(y=0.231, color='cyan', linestyle=':', alpha=0.5)
    ax1.text(0, 0.235, "Standard Model (0.231)", color='cyan', fontsize=8)
    
    # Plot Action (Right Axis)
    ax2 = ax1.twinx()
    ax2.plot(gamma_values, actions, color='lime', marker='x', linestyle='--', label='Action (Mass)')
    ax2.set_ylabel('Quantized Action (J/h)', color='lime')
    ax2.tick_params(axis='y', labelcolor='lime', colors='white')
    ax2.spines['bottom'].set_color('white')
    ax2.spines['top'].set_color('white') 
    ax2.spines['right'].set_color('white')
    ax2.spines['left'].set_color('white')
    
    # Target Line
    ax2.axhline(y=np.pi, color='lime', linestyle=':', alpha=0.5)
    ax2.text(0, np.pi+0.5, "Target Mass (Pi)", color='lime', fontsize=8)
    
    plt.title("The Viscosity Scan: Finding the Higgs Coupling", color='white', fontsize=14)
    fig.tight_layout()
    plt.savefig('higgs_viscosity_scan.png')
    plt.show()

if __name__ == "__main__":
    run_viscosity_scan()