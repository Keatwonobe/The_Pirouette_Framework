import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# --------------------------------------------------
# PIROUETTE MACRO-SCAN: THE FRACTAL GRID
# --------------------------------------------------
# We zoom out significantly (5x-10x) to look for
# large-scale structures, repeating islands, or
# the hypothetical "Antimatter Basin".
# --------------------------------------------------

# Constants
TWIST = 2.83814 
GAMMA = 0.02
DT = 0.01   # Faster timestep for macro scan
STEPS = 2000 # Shorter duration per pixel for speed

# Viewport
RANGE = 12.0 # -12 to 12
RES = 300

def get_force_vectorized(m, lam):
    # --- The Unified Physics (Tuned) ---
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
    
    return Fm, Flam, nw_red

def run_macro_scan():
    print(f"Running Macro-Scale Stability Scan ({RANGE}x{RANGE})...")
    
    m_range = np.linspace(-RANGE, RANGE, RES)
    l_range = np.linspace(-RANGE, RANGE, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Track "Chaos" (Divergence or movement)
    # We'll use displacement from start as a metric for "Structure"
    start_m = m.copy()
    start_l = lam.copy()
    
    # Metric: Average "Red" weight experienced (Does it live in the twist?)
    red_exposure = np.zeros_like(m)
    
    print("Simulating Field Dynamics...")
    for step in range(STEPS):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        red_exposure += w_red
        
    # Reshape
    Final_M = m.reshape(RES, RES)
    Final_L = lam.reshape(RES, RES)
    Red_Exp = red_exposure.reshape(RES, RES)
    
    # Calculate Displacement
    # If Displacement is Low -> Stable Attractor (The Particle)
    # If Displacement is Medium -> Limit Cycle (Orbit)
    # If Displacement is High -> Chaos/Drift
    Disp = np.sqrt((Final_M - M)**2 + (Final_L - L)**2)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # We plot "Red Exposure" to see the "Structure" of the vacuum
    # This highlights the twist bands
    # We overlay stability (displacement) as brightness?
    
    # Let's plot Stability directly
    # Dark = Stable, Bright = Chaotic
    # We want to see "Islands"
    
    # Log scale for dynamic range
    im = ax.imshow(Red_Exp, extent=[-RANGE, RANGE, -RANGE, RANGE], 
                   origin='lower', cmap='nipy_spectral', alpha=1.0)
    
    # Mark the Origin (Our Electron)
    ax.scatter([-1.8], [0.0], color='white', marker='*', s=150, label='Standard Matter')
    
    # Mark the "Mirror" point (Antimatter)
    ax.scatter([1.8], [0.0], color='white', marker='x', s=100, label='Mirror Point (Unstable)')
    
    # Add Grid lines
    ax.grid(color='white', alpha=0.1, linestyle='--')
    
    ax.set_title("The Macro-Verse: Fractal Network of the Vacuum\n(Color = Interaction with Twist Field)", color='white', fontsize=16)
    ax.set_xlabel("Mass Field", color='white')
    ax.set_ylabel("Coupling Field", color='white')
    
    cbar = plt.colorbar(im)
    cbar.set_label("Integrated Twist Exposure", color='white')
    cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    
    ax.legend(facecolor='black', labelcolor='white')
    
    plt.tight_layout()
    plt.savefig('macro_scan.png')
    plt.show()

if __name__ == "__main__":
    run_macro_scan()