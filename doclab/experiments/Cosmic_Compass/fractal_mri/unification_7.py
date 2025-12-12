import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
# We scan "Global Energy" via the Twist Factor (Asymmetry)
ENERGY_MIN = 0.0
ENERGY_MAX = 5.0
ENERGY_STEPS = 50 

# Simulation settings for stability check
DT = 0.02
STEPS = 1000
BOUND_LIMIT = 4.0 # If it goes past this, it escaped (unstable)

def get_force_space(m, lam, twist):
    # Physics of the Pirouette (Tension Mode)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    # Basin Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Fast Gaussian (Inline)
    diff_g = np.abs(angle - 30); diff_g = np.minimum(diff_g, 360-diff_g)
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.abs(angle - 150); diff_t = np.minimum(diff_t, 360-diff_t)
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.abs(angle - 270); diff_r = np.minimum(diff_r, 360-diff_r)
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    return Fm, Flam

def check_stability_grid(twist, res=100):
    # Create a grid of initial conditions (The "Space")
    m_range = np.linspace(-2.5, 2.5, res)
    l_range = np.linspace(-2.5, 2.5, res)
    M, L = np.meshgrid(m_range, l_range)
    
    # Flatten for simulation
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m) # Start from rest (Potential Energy map)
    plam = np.zeros_like(lam)
    
    active_mask = np.ones_like(m, dtype=bool)
    
    # Run batch integration
    for _ in range(STEPS):
        # We only update active particles to save time
        if not np.any(active_mask): break
        
        m_curr = m[active_mask]
        l_curr = lam[active_mask]
        pm_curr = pm[active_mask]
        pl_curr = plam[active_mask]
        
        # Leapfrog Step
        Fm, Flam = get_force_space(m_curr, l_curr, twist)
        
        pm_h = pm_curr + 0.5 * DT * Fm
        pl_h = pl_curr + 0.5 * DT * Flam
        
        m_n = m_curr + DT * pm_h
        l_n = l_curr + DT * pl_h
        
        Fm_n, Flam_n = get_force_space(m_n, l_n, twist)
        
        pm_n = pm_h + 0.5 * DT * Fm_n
        pl_n = pl_h + 0.5 * DT * Flam_n
        
        # Update
        m[active_mask] = m_n
        lam[active_mask] = l_n
        pm[active_mask] = pm_n
        plam[active_mask] = pl_n
        
        # Check bounds
        r2 = m_n**2 + l_n**2
        escaped = r2 > BOUND_LIMIT**2
        
        # Mark escaped particles as inactive (0)
        # We need to update the mask carefully
        current_indices = np.where(active_mask)[0]
        escaped_indices = current_indices[escaped]
        active_mask[escaped_indices] = False
        
    # Count stable points (Volume of Space)
    stable_volume = np.sum(active_mask)
    return stable_volume, active_mask.reshape(res, res)

def run_fractal_space_scan():
    energies = np.linspace(ENERGY_MIN, ENERGY_MAX, ENERGY_STEPS)
    volumes = []
    
    print(f"Scanning Space Stability vs Energy ({ENERGY_STEPS} steps)...")
    
    # Store the map for low, med, high energy for visualization
    map_low = None
    map_med = None
    map_high = None
    
    idx_low = 0
    idx_med = len(energies) // 2
    idx_high = len(energies) - 1
    
    for i, E in enumerate(energies):
        vol, stability_map = check_stability_grid(E, res=80) # Lower res for speed in loop
        volumes.append(vol)
        
        if i == idx_low: map_low = stability_map
        if i == idx_med: map_med = stability_map
        if i == idx_high: map_high = stability_map
        
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    
    # 1. The Scaling Law (Volume vs Energy)
    ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=3, facecolor='black')
    ax1.plot(energies, volumes, color='lime', linewidth=2, marker='o', markersize=3)
    ax1.set_title("The Shrinking Universe: Space Volume vs Energy", color='white', fontsize=14)
    ax1.set_xlabel("Energy / Asymmetry (Twist Factor)", color='white')
    ax1.set_ylabel("Volume of Stable Space (Pixels)", color='white')
    ax1.grid(color='#333333', alpha=0.5)
    ax1.tick_params(colors='white')
    
    # 2. Visualizing the Shrinkage
    # Low Energy
    ax2 = plt.subplot2grid((2, 3), (1, 0))
    ax2.imshow(map_low, cmap='bone', origin='lower')
    ax2.set_title(f"Low Energy (Twist={energies[idx_low]:.1f})", color='white')
    ax2.axis('off')
    
    # Med Energy
    ax3 = plt.subplot2grid((2, 3), (1, 1))
    ax3.imshow(map_med, cmap='bone', origin='lower')
    ax3.set_title(f"Med Energy (Twist={energies[idx_med]:.1f})", color='white')
    ax3.axis('off')
    
    # High Energy
    ax4 = plt.subplot2grid((2, 3), (1, 2))
    ax4.imshow(map_high, cmap='bone', origin='lower')
    ax4.set_title(f"High Energy (Twist={energies[idx_high]:.1f})", color='white')
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig('fractal_space_scaling.png')
    plt.show()

if __name__ == "__main__":
    run_fractal_space_scan()