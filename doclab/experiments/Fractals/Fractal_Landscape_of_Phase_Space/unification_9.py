import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# LYAPUNOV CONFIGURATION
# ----------------------------------------
RES = 800            # Resolution
TWIST = 3.8
GAMMA = 0.5
DT = 0.015
STEPS = 1000         # Duration to measure divergence

# Viewport (Same as before)
M_MIN, M_MAX = -2.5, 2.5
L_MIN, L_MAX = -2.5, 2.5

# Perturbation size for Lyapunov calculation
EPSILON = 1e-6

def get_force_vectorized(m, lam):
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
    scaling_factor = np.sqrt(magnitude) # Approx for stability
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Fast Gaussian
    diff_g = np.abs(np.degrees(np.arctan2(lam, m)) % 360 - 30)
    diff_g = np.minimum(diff_g, 360-diff_g)
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.abs(np.degrees(np.arctan2(lam, m)) % 360 - 150)
    diff_t = np.minimum(diff_t, 360-diff_t)
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.abs(np.degrees(np.arctan2(lam, m)) % 360 - 270)
    diff_r = np.minimum(diff_r, 360-diff_r)
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_lyapunov_map():
    print(f"Mapping Chaos (Lyapunov Exponent)...")
    
    # 1. Initialize Grid
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # Flatten
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Initialize "Shadow" particles (perturbed by Epsilon)
    m_shadow = m + EPSILON
    lam_shadow = lam + EPSILON
    pm_shadow = pm # Velocity perturbation is 0 initially
    plam_shadow = plam
    
    # Accumulator for Log Divergence
    lyap_sum = np.zeros_like(m)
    
    # 2. Integration Loop
    for step in range(STEPS):
        # --- Evolve Main Trajectory ---
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
        
        # --- Evolve Shadow Trajectory ---
        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_shadow, lam_shadow)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)
        
        pm_shadow = (pm_shadow + 0.5 * DT * Fm_s) * drag_s
        plam_shadow = (plam_shadow + 0.5 * DT * Flam_s) * drag_s
        m_shadow += DT * pm_shadow
        lam_shadow += DT * plam_shadow
        
        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_shadow, lam_shadow)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)
        pm_shadow = (pm_shadow + 0.5 * DT * Fm_s) * drag_s
        plam_shadow = (plam_shadow + 0.5 * DT * Flam_s) * drag_s
        
        # --- Measure Divergence & Rescale ---
        # Calculate distance between Main and Shadow
        dist_sq = (m - m_shadow)**2 + (lam - lam_shadow)**2 + \
                  (pm - pm_shadow)**2 + (plam - plam_shadow)**2
        dist = np.sqrt(dist_sq)
        
        # Avoid log(0)
        dist = np.maximum(dist, 1e-15)
        
        # Accumulate the exponent: ln(d(t) / d(0))
        # Note: True Lyapunov requires periodic rescaling (Benettin algorithm)
        # to prevent overflow. We rescale the shadow back towards the main
        # to keep linear approximation valid.
        
        rescale_factor = EPSILON / dist
        
        # Log the expansion rate for this step
        lyap_sum += np.log(dist / EPSILON)
        
        # Pull shadow back
        m_shadow = m + (m_shadow - m) * rescale_factor
        lam_shadow = lam + (lam_shadow - lam) * rescale_factor
        pm_shadow = pm + (pm_shadow - pm) * rescale_factor
        plam_shadow = plam + (plam_shadow - plam) * rescale_factor
        
        if step % 100 == 0:
            print(f"Step {step}/{STEPS}...")

    # 3. Finalize
    # Average over time
    lyap_exp = lyap_sum / (STEPS * DT)
    
    # Reshape
    lyap_map = lyap_exp.reshape(RES, RES)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(12, 12), facecolor='black')
    
    # 'magma' is great for chaos (Black=Stable, Red/White=Chaos)
    # 'seismic' or 'bwr' is good if we have negative values (Convergence)
    
    plt.imshow(lyap_map, extent=[M_MIN, M_MAX, L_MIN, L_MAX], 
               origin='lower', cmap='magma', vmin=0, vmax=np.percentile(lyap_map, 95))
    
    plt.title(f"The Skeleton of Chaos: Lyapunov Exponent Map\n(Twist={TWIST}, Gamma={GAMMA})", 
              color='white', fontsize=16)
    plt.xlabel("Mass Field (m)", color='white')
    plt.ylabel("Coupling Field (λ)", color='white')
    plt.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('fractal_lyapunov_map.png')
    plt.show()

if __name__ == "__main__":
    run_lyapunov_map()