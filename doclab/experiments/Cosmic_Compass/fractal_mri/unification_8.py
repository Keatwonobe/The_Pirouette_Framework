import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# FRACTAL CONFIGURATION
# ----------------------------------------
RES = 1000           # Resolution (1000x1000 = 1 Million Universes)
TWIST = 3.8          # The Standard Model Twist
GAMMA = 0.5          # The Critical Higgs Viscosity
DT = 0.015
STEPS = 1000         # Duration of the "Tumble"

# Viewport (The Phase Space Window)
M_MIN, M_MAX = -2.5, 2.5
L_MIN, L_MAX = -2.5, 2.5

def get_force_vectorized(m, lam):
    # Vectorized Physics Engine for 1 Million Points
    
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
    
    # Avoid division by zero in scaling
    scaling_factor = np.sqrt(magnitude)
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Fast Gaussian logic using absolute differences
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

def run_fractal_map():
    print(f"Generating High-Res Fractal ({RES}x{RES})...")
    
    # 1. Initialize Grid
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # Flatten for computation
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Tracking
    prev_ang = np.arctan2(lam, m)
    total_ang = np.zeros_like(m)
    
    # 2. Vectorized Integration Loop
    for step in range(STEPS):
        # Get Force
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        
        # Drag
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        
        # Half-Kick
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        # Drift
        m += DT * pm
        lam += DT * plam
        
        # Re-eval Force
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        
        # Half-Kick
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        # Winding Math
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        
        # Vectorized Unwrap
        # delta > pi -> delta -= 2pi
        delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
        # delta < -pi -> delta += 2pi
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        
        total_ang += delta
        prev_ang = curr_ang
        
        if step % 100 == 0:
            print(f"Step {step}/{STEPS}...")

    # 3. Process Results
    # Spin = Total Angle / 2pi / Cycles(Time)
    # We just want raw winding count to see the integers
    winding = np.abs(total_ang) / (2*np.pi)
    
    # Reshape
    fractal_map = winding.reshape(RES, RES)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(12, 12), facecolor='black')
    
    # Use a cyclic colormap to highlight the integer steps (Spin 1, 2, 3...)
    # 'twilight' or 'hsv' are good for phase/winding
    # 'inferno' is good for energy intensity
    # Let's use 'nipy_spectral' for maximum contrast of fractal bands
    
    plt.imshow(fractal_map, extent=[M_MIN, M_MAX, L_MIN, L_MAX], 
               origin='lower', cmap='nipy_spectral')
    
    plt.title(f"The Fractal of Space: Spin Topology Map\n(Twist={TWIST}, Gamma={GAMMA})", 
              color='white', fontsize=16)
    plt.xlabel("Mass Field (m)", color='white')
    plt.ylabel("Coupling Field (λ)", color='white')
    plt.tick_params(colors='white')
    
    # Add contour lines to highlight the "Edges" (The Friction Zones)
    plt.contour(fractal_map, levels=np.arange(0, 10, 0.5), 
                colors='black', linewidths=0.5, alpha=0.5, 
                extent=[M_MIN, M_MAX, L_MIN, L_MAX])

    plt.tight_layout()
    plt.savefig('fractal_spin_map.png')
    plt.show()

if __name__ == "__main__":
    run_fractal_map()