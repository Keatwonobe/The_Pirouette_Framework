import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE LYAPUNOV MULTIVERSE
# --------------------------------------------------
# We map the "Chaos Temperature" (Lyapunov Exponent)
# of the vacuum on a massive scale (+/- 600).
#
# Dark = Order (Stable Universes)
# Bright = Chaos (The Void between Worlds)
# --------------------------------------------------

# Constants
TWIST = 2.83814 
GAMMA = 0.02
DT = 0.015  # Slightly coarser step for macro speed
STEPS = 1500 # Sufficient to detect divergence

# Massive Viewport
RANGE = 6.0 
RES = 800   # High resolution for fractal detail

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
    
    return Fm, Flam, w_red # Return weight for drag

def run_lyapunov_scan():
    print(f"Mapping Chaos (Lyapunov) on Range +/- {RANGE}...")
    
    m_range = np.linspace(-RANGE, RANGE, RES)
    l_range = np.linspace(-RANGE, RANGE, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # Main Particle
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Shadow Particle (Perturbed by Epsilon)
    EPSILON = 1e-4
    m_s = m + EPSILON
    lam_s = lam # Only perturb Mass field
    pm_s = np.zeros_like(m)
    plam_s = np.zeros_like(lam)
    
    # Lyapunov Accumulator
    lyap_sum = np.zeros_like(m)
    
    print("Integrating Chaos...")
    
    for step in range(STEPS):
        # --- Main Particle ---
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        # --- Shadow Particle ---
        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)
        pm_s = (pm_s + 0.5 * DT * Fm_s) * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s
        m_s += DT * pm_s
        lam_s += DT * plam_s
        
        # --- Lyapunov Calculation (Benettin's Method) ---
        # 1. Measure distance
        dist_sq = (m - m_s)**2 + (lam - lam_s)**2 + (pm - pm_s)**2 + (plam - plam_s)**2
        dist = np.sqrt(dist_sq)
        
        # Avoid zero division
        dist = np.maximum(dist, 1e-15)
        
        # 2. Accumulate Log Divergence
        lyap_sum += np.log(dist / EPSILON)
        
        # 3. Renormalize Shadow (Pull it back to Epsilon distance)
        # This keeps the shadow local so we measure local chaos, not global drift
        scale = EPSILON / dist
        m_s = m + (m_s - m) * scale
        lam_s = lam + (lam_s - lam) * scale
        pm_s = pm + (pm_s - pm) * scale
        plam_s = plam + (plam_s - plam) * scale
        
        if step % 200 == 0: print(f"Step {step}/{STEPS}...")

    # Calculate Exponent
    # Lambda = Sum(log(d_i/d_0)) / (N * dt)
    Lyap = lyap_sum / (STEPS * DT)
    Lyap_Map = Lyap.reshape(RES, RES)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(14, 12), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # We use 'magma' or 'inferno' to show heat
    # Bright = High Chaos (Walls)
    # Black/Dark = Stability (Universes)
    
    # Clip extreme values for better contrast
    L_disp = np.clip(Lyap_Map, 0, 5.0)
    
    im = ax.imshow(L_disp, extent=[-RANGE, RANGE, -RANGE, RANGE], 
                   origin='lower', cmap='magma')
    
    # Mark Origin
    ax.scatter([0], [0], color='cyan', marker='+', s=100, label='Center')
    
    ax.set_title("The Lyapunov Multiverse: Map of Chaos & Order\n(Range +/- 600)", color='white', fontsize=16)
    ax.set_xlabel("Mass Field Dimension", color='white')
    ax.set_ylabel("Coupling Field Dimension", color='white')
    
    cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
    cbar.set_label("Lyapunov Exponent (Rate of Divergence)", color='white')
    cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    
    plt.tight_layout()
    plt.savefig('lyapunov_multiverse.png')
    plt.show()

if __name__ == "__main__":
    run_lyapunov_scan()