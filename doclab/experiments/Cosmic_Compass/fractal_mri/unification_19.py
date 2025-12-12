import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 3.8
GAMMA = 0.11         # The Standard Model Viscosity (Sweet Spot)
DT = 0.005
H_BAR_SIM = 77.41389 # Natural Unit

# Scan Settings for finding particles
RES = 200            # Lower res for quick location
M_MIN, M_MAX = -3.0, 3.0
L_MIN, L_MAX = -3.0, 3.0
SCAN_STEPS = 600

# Measurement Settings
MEASURE_STEPS = 10000

def get_force_spectrometer(m, lam):
    # Standard Soliton Physics
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # Non-linear Confinement
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    
    # Vectorized conditional for scaling factor
    scaling_factor = np.where(magnitude > 1e-6, np.sqrt(magnitude), 0)
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Vectorized Gaussian
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
    
    return Fm, Flam, nw_red, nw_teal, nw_gold

def leapfrog_spectrometer(m, lam, pm, plam, dt):
    Fm, Flam, w_red, _, _ = get_force_spectrometer(m, lam)
    
    drag = 1.0 / (1.0 + 0.5 * dt * GAMMA * w_red)
    
    pm = (pm + 0.5 * dt * Fm) * drag
    plam = (plam + 0.5 * dt * Flam) * drag
    
    m += dt * pm
    lam += dt * plam
    
    Fm, Flam, w_red, _, _ = get_force_spectrometer(m, lam)
    drag = 1.0 / (1.0 + 0.5 * dt * GAMMA * w_red)
    
    pm = (pm + 0.5 * dt * Fm) * drag
    plam = (plam + 0.5 * dt * Flam) * drag
    
    return m, lam, pm, plam

def find_particles():
    print("Scanning Vacuum for Particle Candidates...")
    
    # Grid
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    coherence = np.zeros_like(m)
    prev_pm = np.zeros_like(m)
    prev_plam = np.zeros_like(lam)
    
    # Fast Scan
    for _ in range(SCAN_STEPS):
        Fm, Flam, w_red, _, _ = get_force_spectrometer(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        v_mag = np.sqrt(pm**2 + plam**2) + 1e-9
        prev_mag = np.sqrt(prev_pm**2 + prev_plam**2) + 1e-9
        dot = (pm * prev_pm + plam * prev_plam) / (v_mag * prev_mag)
        coherence += np.maximum(0, dot)
        prev_pm = pm.copy()
        prev_plam = plam.copy()
        
    Light = coherence.reshape(RES, RES)
    Light /= np.max(Light)
    
    # Peak Finding
    local_max = maximum_filter(Light, size=10) == Light
    particles = (Light > 0.8) & local_max
    y_idx, x_idx = np.where(particles)
    
    candidates = []
    for i in range(len(x_idx)):
        px, py = x_idx[i], y_idx[i]
        phys_m = M_MIN + (px/RES)*(M_MAX-M_MIN)
        phys_l = L_MIN + (py/RES)*(L_MAX-L_MIN)
        
        # Determine Basin
        ang = np.degrees(np.arctan2(phys_l, phys_m)) % 360
        basin = "Unknown"
        if 90 <= ang < 210: basin = "Teal (EM)"
        elif 210 <= ang < 330: basin = "Red (Weak)"
        else: basin = "Gold (Strong)"
        
        candidates.append({'m': phys_m, 'l': phys_l, 'basin': basin, 'id': i})
        
    print(f"Found {len(candidates)} candidates.")
    return candidates

def measure_mass(candidate):
    # Initialize EXACTLY at the candidate spot
    m, lam = candidate['m'], candidate['l']
    # Give it a small kick to orbit the knot
    pm, plam = 0.1, 0.1 
    
    action_accum = 0.0
    prev_ang = np.arctan2(lam, m)
    total_ang = 0.0
    
    # Run high precision measurement
    for _ in range(MEASURE_STEPS):
        m_old, lam_old = m, lam
        m, lam, pm, plam = leapfrog_spectrometer(m, lam, pm, plam, DT)
        
        # Action dS = p dq
        dq_m = m - m_old
        dq_lam = lam - lam_old
        action_accum += (pm * dq_m + plam * dq_lam)
        
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        if delta > np.pi: delta -= 2*np.pi
        if delta < -np.pi: delta += 2*np.pi
        total_ang += delta
        prev_ang = curr_ang
        
    cycles = abs(total_ang) / (4*np.pi) # Fermion 720 deg cycles
    if cycles < 0.5: return 0.0 # Frozen/Decayed
    
    raw_mass = abs(action_accum) / cycles
    calib_mass = raw_mass / H_BAR_SIM
    
    return calib_mass

def run_spectrometer():
    candidates = find_particles()
    
    print("\n" + "="*60)
    print("PARTICLE MASS SPECTROMETRY REPORT")
    print("="*60)
    print(f"{'ID':<5} | {'Basin':<15} | {'Coords (m, l)':<20} | {'Mass (Action)':<15}")
    print("-" * 60)
    
    results = {'Teal (EM)': [], 'Red (Weak)': [], 'Gold (Strong)': []}
    
    for p in candidates:
        mass = measure_mass(p)
        
        # Filter noise
        if mass > 0.01:
            print(f"{p['id']:<5} | {p['basin']:<15} | ({p['m']:.2f}, {p['l']:.2f})      | {mass:.5f}")
            results[p['basin']].append(mass)
            
    print("-" * 60)
    print("ANALYSIS BY SPECIES")
    
    for basin, masses in results.items():
        if len(masses) > 0:
            avg_mass = np.mean(masses)
            min_mass = np.min(masses)
            print(f"{basin}: Avg Mass = {avg_mass:.4f}, Lightest = {min_mass:.4f}")
            
    # Visualize Spectrum
    plt.figure(figsize=(10, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Plot mass levels
    y_pos = 0
    colors = {'Teal (EM)': 'cyan', 'Red (Weak)': 'red', 'Gold (Strong)': 'gold'}
    
    for basin, masses in results.items():
        c = colors.get(basin, 'white')
        for m in masses:
            plt.plot([m, m], [y_pos, y_pos+1], color=c, linewidth=2)
        y_pos += 1.5
        
    plt.yticks([0.5, 2.0, 3.5], list(results.keys()), color='white')
    plt.xlabel("Mass (Action Units)", color='white')
    plt.title("Mass Spectrum of the Fractal Vacuum", color='white', fontsize=14)
    plt.grid(axis='x', color='#333333')
    plt.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('particle_spectroscopy.png')
    plt.show()

if __name__ == "__main__":
    run_spectrometer()