import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
RES = 800
TWIST = 3.8
GAMMA = 0.5
DT = 0.02
STEPS = 1500

# ZOOM OUT: The Macro-Scale View
M_MIN, M_MAX = -20.0, 20.0
L_MIN, L_MAX = -20.0, 20.0

def get_force_vectorized(m, lam):
    # Standard physics (Tension Mode)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # Non-linear Confinement (The Squeeze)
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude) # F^1.5 scaling
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Basin Weights (using degrees for phase wrapping)
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Gaussian weights
    diff_g = np.abs(angle - 30); diff_g = np.minimum(diff_g, 360-diff_g)
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.abs(angle - 150); diff_t = np.minimum(diff_t, 360-diff_t)
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.abs(angle - 270); diff_r = np.minimum(diff_r, 360-diff_r)
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_cosmic_raytrace():
    print(f"Ray-Tracing the Macro-Vacuum ({RES}x{RES})...")
    
    # Grid
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Stability Accumulator (Inverse Lyapunov)
    # Instead of measuring divergence, we measure CONVERGENCE (Coherence)
    coherence = np.zeros_like(m)
    
    # Previous state for velocity correlation
    prev_pm = np.zeros_like(m)
    prev_plam = np.zeros_like(lam)
    
    for step in range(STEPS):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        # --- "Light" Calculation ---
        # Coherence is high if velocity doesn't change direction wildly.
        # Dot product of current velocity vs previous velocity.
        # Smooth flow = High Light. Chaotic jitter = Darkness.
        
        # Normalize vectors to avoid energy bias
        v_mag = np.sqrt(pm**2 + plam**2) + 1e-9
        prev_mag = np.sqrt(prev_pm**2 + prev_plam**2) + 1e-9
        
        dot = (pm * prev_pm + plam * prev_plam) / (v_mag * prev_mag)
        
        # Accumulate positive correlation (smoothness)
        # This acts like an exposure time on a camera sensor
        coherence += np.maximum(0, dot)
        
        prev_pm = pm.copy()
        prev_plam = plam.copy()
        
        if step % 100 == 0: print(f"Exposure {step}/{STEPS}...")

    # Process Image
    luminosity = coherence.reshape(RES, RES)
    
    # Log scale for High Dynamic Range (like looking at stars)
    luminosity = np.log1p(luminosity)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(12, 12), facecolor='black')
    
    # 'afmhot' or 'inferno' creates a glowing heat effect
    plt.imshow(luminosity, extent=[M_MIN, M_MAX, L_MIN, L_MAX], 
               origin='lower', cmap='afmhot')
    
    plt.title(f"The Cosmic Caustic: Coherence Ray-Trace\n(Twist={TWIST}, Gamma={GAMMA}, Zoom=10x)", 
              color='white', fontsize=16)
    plt.xlabel("Mass Field", color='white')
    plt.ylabel("Coupling Field", color='white')
    plt.axis('off')
    
    # Add a scale bar
    plt.plot([M_MIN + 2, M_MIN + 7], [L_MIN + 2, L_MIN + 2], color='white', linewidth=2)
    plt.text(M_MIN + 4.5, L_MIN + 3, "5 Planck Units", color='white', ha='center')

    plt.tight_layout()
    plt.savefig('cosmic_caustic.png')
    plt.show()

if __name__ == "__main__":
    run_cosmic_raytrace()