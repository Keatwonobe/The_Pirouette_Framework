import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 3.8
GAMMA = 0.11         # The "Sweet Spot" we found for stability
DT = 0.005
STEPS = 10000
H_BAR_SIM = 77.41389 # Natural Unit

# Scan Settings
R_MIN = 0.1
R_MAX = 5.0
SAMPLES = 200        # Resolution of the energy scan

def get_force_generations(m, lam):
    # Standard Soliton Physics (Tension Mode)
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
    
    # Weights for Drag
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
    
    # Net Force
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def leapfrog_gen(m, lam, pm, plam, dt):
    Fm, Flam, w_red = get_force_generations(m, lam)
    
    # Higgs Drag
    drag = 1.0 / (1.0 + 0.5 * dt * GAMMA * w_red)
    
    pm = (pm + 0.5 * dt * Fm) * drag
    plam = (plam + 0.5 * dt * Flam) * drag
    
    m += dt * pm
    lam += dt * plam
    
    Fm, Flam, w_red = get_force_generations(m, lam)
    drag = 1.0 / (1.0 + 0.5 * dt * GAMMA * w_red)
    
    pm = (pm + 0.5 * dt * Fm) * drag
    plam = (plam + 0.5 * dt * Flam) * drag
    
    return m, lam, pm, plam

def analyze_orbit(start_r):
    # Initialize at a specific radius (Energy Level)
    # Start at angle 0 (Pure Mass Field)
    m, lam = start_r, 0.0
    
    # Tangential Velocity for orbit
    # V approx sqrt(r * Force). Force ~ r (harmonic) -> V ~ r
    # Let's give it a generic kick and let it settle
    pm, plam = 0.0, start_r * 0.5 
    
    # Stabilization
    for _ in range(5000):
        m, lam, pm, plam = leapfrog_gen(m, lam, pm, plam, DT)
        
        # Check for escape or collapse
        r2 = m**2 + lam**2
        if r2 > 25.0 or r2 < 0.01: return None # Unstable
        
    # Measurement
    action_accum = 0.0
    total_ang = 0.0
    prev_ang = np.arctan2(lam, m)
    
    # Record one "segment"
    for _ in range(5000):
        m_old, lam_old = m, lam
        m, lam, pm, plam = leapfrog_gen(m, lam, pm, plam, DT)
        
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
        
    # Normalize Action per Cycle
    cycles = abs(total_ang) / (4*np.pi) # Fermion Cycles
    if cycles < 0.5: return None # Frozen
    
    mass_action = abs(action_accum) / cycles
    return mass_action / H_BAR_SIM # Calibrated Mass

def run_mass_spectrum():
    print(f"Scanning for Mass Eigenstates (R={R_MIN} to {R_MAX})...")
    
    radii = np.linspace(R_MIN, R_MAX, SAMPLES)
    masses = []
    stable_radii = []
    
    for r in radii:
        mass = analyze_orbit(r)
        if mass is not None:
            masses.append(mass)
            stable_radii.append(r)
        else:
            masses.append(0) # Dead zone
            stable_radii.append(r)

    # ----------------------------------------
    # ANALYSIS
    # ----------------------------------------
    masses = np.array(masses)
    stable_radii = np.array(stable_radii)
    
    # Find Peaks (The Stable Islets)
    peaks, _ = find_peaks(masses, height=0.01, distance=5)
    
    print("-" * 60)
    print("DETECTED MASS GENERATIONS")
    print("-" * 60)
    
    if len(peaks) > 0:
        # Base Mass (Generation 1)
        m1 = masses[peaks[0]]
        print(f"Gen 1 Candidate (Radius {stable_radii[peaks[0]]:.2f}): Mass = {m1:.5f}")
        
        for i in range(1, len(peaks)):
            mi = masses[peaks[i]]
            ratio = mi / m1
            print(f"Gen {i+1} Candidate (Radius {stable_radii[peaks[i]]:.2f}): Mass = {mi:.5f} (Ratio: {ratio:.2f}x)")
            
    print("-" * 60)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(10, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    plt.plot(stable_radii, masses, color='lime', linewidth=1.5, label='Mass Spectrum')
    
    # Mark Peaks
    if len(peaks) > 0:
        plt.plot(stable_radii[peaks], masses[peaks], 'x', color='white', markersize=10, markeredgewidth=2, label='Resonance')
    
    plt.title("The Particle Spectrum: Mass vs Energy Radius", color='white', fontsize=14)
    plt.xlabel("Initial Energy Radius", color='white')
    plt.ylabel("Stable Particle Mass (Action)", color='white')
    
    plt.grid(color='#333333', alpha=0.5)
    plt.legend(facecolor='black', labelcolor='white')
    plt.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('generational_mass_spectrum.png')
    plt.show()

if __name__ == "__main__":
    run_mass_spectrum()