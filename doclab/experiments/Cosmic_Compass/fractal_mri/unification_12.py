import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# MASS SPECTROMETER CONFIGURATION
# ----------------------------------------
TWIST = 3.8
GAMMA = 0.5
DT = 0.015
STEPS = 50000  # Long duration for precise mass measurement
H_BAR_SIM = 77.41389  # Calibration constant from previous runs

# The Particle Zoo Candidates
# Coordinates estimated from the Stability Map
CANDIDATES = {
    "The Anchor (Electron?)":    (-0.5, 0.5),   # Our calibration point
    "The Green Giant (Proton?)": (-2.0, -1.0),  # Deep stable green zone
    "The Red Ridge (Neutrino?)": (1.2, 0.0),    # Stable red zone
    "The Blue Sliver (Muon?)":   (-2.3, 0.5),   # Narrow blue band
    "The Void (Virtual)":        (-0.1, -0.1)   # Chaotic region
}

def get_force(m, lam):
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak)
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong)
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude)
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
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

def analyze_particle(name, m0, lam0):
    m, lam = m0, lam0
    pm, plam = 0.0, 0.0 # Start from rest
    
    # Metrics
    action_accum = 0.0
    prev_ang = np.arctan2(lam, m)
    total_ang_disp = 0.0
    
    # Trajectory for plotting
    traj_m = []
    traj_lam = []
    
    print(f"Analyzing {name} at ({m0}, {lam0})...")
    
    # Warmup to settle into orbit
    for _ in range(5000):
        Fm, Flam, w_red = get_force(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
    # Measurement Run
    for step in range(STEPS):
        m_old, lam_old = m, lam
        
        # Leapfrog
        Fm, Flam, w_red = get_force(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        # Data Collection
        if step % 10 == 0:
            traj_m.append(m)
            traj_lam.append(lam)
            
        # Action = p * dq
        dq_m = m - m_old
        dq_lam = lam - lam_old
        action_accum += (pm * dq_m + plam * dq_lam)
        
        # Winding
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        total_ang_disp += delta
        prev_ang = curr_ang
        
    # Final Calculations
    cycles = abs(total_ang_disp) / (2*np.pi)
    if cycles < 1: cycles = 1 # Avoid div/0
    
    # Mass = Average Action per Cycle
    raw_mass = abs(action_accum) / cycles
    calib_mass = raw_mass / H_BAR_SIM
    
    avg_spin = cycles / (STEPS * DT / (2*np.pi)) # Rough frequency check
    integer_spin = round(abs(total_ang_disp) / (2*np.pi)) # Net winding
    
    return {
        "name": name,
        "mass": calib_mass,
        "spin_winding": integer_spin,
        "trajectory": (traj_m, traj_lam)
    }

def run_spectrometer():
    results = []
    
    print("-" * 80)
    print(f"{'PARTICLE NAME':<30} | {'MASS (GeV?)':<15} | {'SPIN (Int)':<10} | {'STATUS'}")
    print("-" * 80)
    
    for name, coords in CANDIDATES.items():
        data = analyze_particle(name, coords[0], coords[1])
        results.append(data)
        
        # Basic stability check
        # If trajectory spread is too huge, it's unstable
        traj_m = data['trajectory'][0]
        spread = max(traj_m) - min(traj_m)
        status = "STABLE" if spread < 5.0 else "DECAYED"
        if data['name'] == "The Void (Virtual)": status = "CHAOTIC"
        
        print(f"{name:<30} | {data['mass']:<15.5f} | {data['spin_winding']:<10} | {status}")

    print("-" * 80)
    
    # ----------------------------------------
    # PLOTTING ORBITS
    # ----------------------------------------
    plt.figure(figsize=(12, 10), facecolor='black')
    
    # Plot background context (simplified)
    plt.axhline(0, color='white', alpha=0.1)
    plt.axvline(0, color='white', alpha=0.1)
    
    colors = ['cyan', 'lime', 'red', 'blue', 'white']
    
    for i, res in enumerate(results):
        m_traj, lam_traj = res['trajectory']
        name = res['name']
        c = colors[i % len(colors)]
        
        # Plot Orbit
        plt.plot(m_traj, lam_traj, color=c, linewidth=0.8, alpha=0.8, label=f"{name} (M={res['mass']:.2f})")
        
        # Plot Start Point
        plt.plot(m_traj[0], lam_traj[0], 'o', color=c, markersize=5)

    plt.title("The Particle Zoo: Orbit Spectroscopy", color='white', fontsize=16)
    plt.xlabel("Mass Field (m)", color='white')
    plt.ylabel("Coupling Field (λ)", color='white')
    plt.grid(color='#333333', alpha=0.3)
    plt.tick_params(colors='white')
    plt.legend(facecolor='black', labelcolor='white', loc='upper right')
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    
    plt.tight_layout()
    plt.savefig('particle_zoo_orbits.png')
    plt.show()

if __name__ == "__main__":
    run_spectrometer()