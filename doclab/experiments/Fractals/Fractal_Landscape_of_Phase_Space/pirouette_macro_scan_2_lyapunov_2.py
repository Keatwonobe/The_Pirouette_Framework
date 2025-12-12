import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE DEEP DRILL: COMPARATIVE ANALYSIS
# --------------------------------------------------
# Comparing the microstructure of the "Quiet Zone"
# vs. the "Storm Zone".
# --------------------------------------------------

# Constants
TWIST = 2.83814 
GAMMA = 0.02
DT = 0.015
STEPS = 2000 # Higher steps for deeper stability check

# Drill Settings
DRILL_RANGE = 10.0 # +/- 10.0 units (Tiny window compared to 600)
RES = 400

def get_force_vectorized(m, lam):
    # --- The Unified Physics ---
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag = np.sqrt(sum_m**2 + sum_lam**2)
    scale = np.sqrt(mag)
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    diff_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30))
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150))
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270))
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, w_red

def run_drill(center_m, center_lam, label, filename):
    print(f"Drilling into {label} at M={center_m}, L={center_lam}...")
    
    # Create local grid
    m_range = np.linspace(center_m - DRILL_RANGE, center_m + DRILL_RANGE, RES)
    l_range = np.linspace(center_lam - DRILL_RANGE, center_lam + DRILL_RANGE, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Shadow Particle for Lyapunov
    EPSILON = 1e-5
    m_s = m + EPSILON
    lam_s = lam
    pm_s = np.zeros_like(m)
    plam_s = np.zeros_like(lam)
    
    lyap_sum = np.zeros_like(m)
    
    for step in range(STEPS):
        # Main
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        # Shadow
        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)
        pm_s = (pm_s + 0.5 * DT * Fm_s) * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s
        m_s += DT * pm_s
        lam_s += DT * plam_s
        
        # Lyapunov Logic
        dist = np.sqrt((m - m_s)**2 + (lam - lam_s)**2 + (pm - pm_s)**2 + (plam - plam_s)**2)
        dist = np.maximum(dist, 1e-15)
        lyap_sum += np.log(dist / EPSILON)
        
        scale = EPSILON / dist
        m_s = m + (m_s - m) * scale
        lam_s = lam + (lam_s - lam) * scale
        pm_s = pm + (pm_s - pm) * scale
        plam_s = plam + (plam_s - plam) * scale

    Lyap = lyap_sum / (STEPS * DT)
    Lyap_Map = Lyap.reshape(RES, RES)
    
    # Plotting
    fig = plt.figure(figsize=(10, 8), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Normalize color scale to be consistent between plots?
    # Or auto-scale to see local details? Auto-scale is better for "microstructure".
    # Using 'magma' to match previous style.
    
    im = ax.imshow(Lyap_Map, extent=[center_m - DRILL_RANGE, center_m + DRILL_RANGE, 
                                     center_lam - DRILL_RANGE, center_lam + DRILL_RANGE], 
                   origin='lower', cmap='magma')
    
    ax.set_title(f"Deep Drill: {label}\nCenter ({center_m}, {center_lam}) | Width +/- {DRILL_RANGE}", color='white', fontsize=14)
    ax.set_xlabel("Mass Field Dimension", color='white')
    ax.set_ylabel("Coupling Field Dimension", color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.colorbar(im, fraction=0.046, pad=0.04).set_label("Local Chaos (Lyapunov)", color='white')
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close() # Close to free memory

# Run the comparative drills
# Zone A: The "Quiet" Left Side. M = -300.
run_drill(-300.0, 0.0, "Zone A (Quiet / Negative Mass)", "drill_quiet.png")

# Zone B: The "Storm" Right Side. M = +300.
run_drill(300.0, 0.0, "Zone B (Storm / Positive Mass)", "drill_storm.png")