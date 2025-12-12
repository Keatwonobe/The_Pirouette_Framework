import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# CONSTANTS
# ----------------------------------------
TWIST = 3.8
DT = 0.005
H_BAR_SIM = 77.41389

# MICRO-SCAN SETTINGS
# We zoom in on the "Critical Limit" where we found the solution
GAMMA_START = 0.40
GAMMA_END = 0.60
STEPS_RES = 400  # High resolution scan

def get_force_roughness(m, lam):
    # Standard Model Soliton Physics
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # Non-linear Confinement
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

def leapfrog_roughness(m, lam, pm, plam, dt, gamma):
    Fm, Flam, Et, Er, w_red = get_force_roughness(m, lam)
    
    # Higgs Drag
    drag = 1.0 / (1.0 + 0.5 * dt * gamma * w_red)
    
    pm_h = (pm + 0.5 * dt * Fm) * drag
    plam_h = (plam + 0.5 * dt * Flam) * drag
    
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    
    Fm_n, Flam_n, Et_n, Er_n, w_red_n = get_force_roughness(m_n, lam_n)
    drag_n = 1.0 / (1.0 + 0.5 * dt * gamma * w_red_n)
    
    pm_n = (pm_h + 0.5 * dt * Fm_n) * drag_n
    plam_n = (plam_h + 0.5 * dt * Flam_n) * drag_n
    
    return m_n, lam_n, pm_n, plam_n, Et, Er

def run_roughness_scan():
    gamma_range = np.linspace(GAMMA_START, GAMMA_END, STEPS_RES)
    
    mass_spectrum = []
    angle_spectrum = []
    
    print(f"Profiling Vacuum Texture ({STEPS_RES} micro-steps)...")
    
    for gamma in gamma_range:
        m, lam = -0.5, 0.5
        pm, plam = 0.9, 0.4
        
        # Fast stabilization (drag helps convergence)
        for _ in range(4000):
            m, lam, pm, plam, _, _ = leapfrog_roughness(m, lam, pm, plam, DT, gamma)
            
        # Measurement
        hist_Et = []
        hist_Er = []
        
        # Integrate Action 'on the fly' to save memory
        action_accum = 0.0
        cycles = 0.0
        prev_ang = np.arctan2(lam, m)
        total_ang_disp = 0.0
        
        for _ in range(4000):
            m_old, lam_old = m, lam
            m, lam, pm, plam, Et, Er = leapfrog_roughness(m, lam, pm, plam, DT, gamma)
            
            # Metrics
            hist_Et.append(Et)
            hist_Er.append(Er)
            
            # Action = p * dq
            dq_m = m - m_old
            dq_lam = lam - lam_old
            action_accum += (pm * dq_m + plam * dq_lam)
            
            # Cycles
            curr_ang = np.arctan2(lam, m)
            delta = curr_ang - prev_ang
            if delta > np.pi: delta -= 2*np.pi
            if delta < -np.pi: delta += 2*np.pi
            total_ang_disp += delta
            prev_ang = curr_ang
            
        cycles = abs(total_ang_disp) / (4*np.pi)
        if cycles < 1: cycles = 1
        
        calib_mass = (abs(action_accum) / cycles) / H_BAR_SIM
        
        avg_Et = np.mean(hist_Et)
        avg_Er = np.mean(hist_Er)
        theta_w = avg_Et / (avg_Et + avg_Er)
        
        mass_spectrum.append(calib_mass)
        angle_spectrum.append(theta_w)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True, facecolor='black')
    
    # 1. The Mass Spectrum (Roughness)
    ax1.set_facecolor('black')
    ax1.plot(gamma_range, mass_spectrum, color='lime', linewidth=1.5)
    ax1.set_ylabel('Particle Mass (Action)', color='lime')
    ax1.set_title("The Texture of the Vacuum: Mass vs Higgs Coupling", color='white', fontsize=14)
    ax1.grid(color='#333333', alpha=0.5)
    ax1.tick_params(colors='white')
    
    # Zoom window indicator (if interesting)
    
    # 2. The Weinberg Angle
    ax2.set_facecolor('black')
    ax2.plot(gamma_range, angle_spectrum, color='cyan', linewidth=1.5)
    ax2.set_xlabel('Higgs Viscosity (Gamma)', color='white')
    ax2.set_ylabel('Weinberg Angle (Sin^2 Theta)', color='cyan')
    ax2.grid(color='#333333', alpha=0.5)
    ax2.tick_params(colors='white')
    
    # Highlight the Target Zone
    ax2.axhline(y=0.231, color='white', linestyle=':', alpha=0.5, label='Standard Model')
    ax2.legend(facecolor='black', labelcolor='white')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_roughness_scan()