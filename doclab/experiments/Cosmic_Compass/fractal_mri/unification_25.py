import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE ORBIT TEST
# --------------------------------------------------
# We drop a test particle into the "Whirlpool" we
# just discovered to see if it spirals into oblivion
# or finds a stable quantum orbit (Limit Cycle).
# --------------------------------------------------

TWIST = 3.8
GAMMA = 0.11  # Low friction to allow orbits
DT = 0.005
STEPS = 50000

def get_force_vectorized(m, lam):
    # --- The Unified Field Laws (Standard Pirouette) ---
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

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
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_orbit_test():
    print("Dropping test particle into the Vortex...")
    
    # Start coordinates: Edge of the whirlpool (Visual estimate from previous map)
    m, lam = -0.5, 0.2 
    pm, plam = 0.8, -0.2 # Initial velocity "kick" to start orbit
    
    traj_m = []
    traj_lam = []
    velocity_profile = []
    
    print(f"Simulating {STEPS} steps...")
    
    for _ in range(STEPS):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        
        # Variable Drag (Higgs Mechanism)
        # Drag increases when passing through "Red" zones
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        
        # Leapfrog Integration
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        m += DT * pm
        lam += DT * plam
        
        # Recalculate Force for second half-step
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        traj_m.append(m)
        traj_lam.append(lam)
        velocity_profile.append(np.sqrt(pm**2 + plam**2))

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(10, 10), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Convert trajectory to arrays
    tm = np.array(traj_m)
    tl = np.array(traj_lam)
    
    # Color trajectory by Time (to show evolution)
    # Early time = Blue, Late time = White
    points = np.array([tm, tl]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    # Create a colormap that goes from Fade -> Bright White
    norm = plt.Normalize(0, STEPS)
    
    from matplotlib.collections import LineCollection
    lc = LineCollection(segments, cmap='cool', norm=norm)
    lc.set_array(np.arange(STEPS))
    lc.set_linewidth(1.0)
    ax.add_collection(lc)
    
    # Mark Start and End
    ax.scatter(tm[0], tl[0], color='green', s=100, label='Start')
    ax.scatter(tm[-1], tl[-1], color='white', s=100, marker='*', label='End (Stable?)')
    
    # Overlay the Vortex Center (Approx)
    ax.scatter(0, 0, color='red', marker='x', s=100, alpha=0.5, label='Singularity')

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    
    ax.set_title("The Orbit Test: Does Matter Survive the Vortex?", color='white', fontsize=16)
    ax.set_xlabel("Mass Field", color='white')
    ax.set_ylabel("Coupling Field", color='white')
    
    ax.legend(facecolor='black', labelcolor='white')
    ax.grid(color='#333333', alpha=0.3)
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('vortex_orbit_test.png')
    plt.show()

if __name__ == "__main__":
    run_orbit_test()