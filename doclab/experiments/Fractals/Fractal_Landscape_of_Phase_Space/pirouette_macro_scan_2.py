import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# --------------------------------------------------
# PIROUETTE SUPER-MACRO SCAN: THE MULTIVERSE GRID
# --------------------------------------------------
# We zoom out EXTREMELY far (Range +/- 60) to see
# the full repeating structure of the vacuum.
# We are looking for the "Grid" or "Network" of
# stable zones.
# --------------------------------------------------

# Constants
TWIST = 2.83814 
GAMMA = 0.02
DT = 0.01
STEPS = 2000

# Viewport (5x larger than before)
RANGE = 60000000.0 
RES = 600

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
    
    return Fm, Flam, nw_red

def run_super_macro_scan():
    print(f"Running Super-Macro Scan ({RANGE}x{RANGE})...")
    
    m_range = np.linspace(-RANGE, RANGE, RES)
    l_range = np.linspace(-RANGE, RANGE, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # We want to identify STABLE regions.
    # Metric: Displacement after N steps.
    # Low Displacement = Stable Island.
    
    # Also track "Redness" (Twist exposure) to see structure
    red_exposure = np.zeros_like(m)
    
    print("Simulating Vacuum Structure...")
    # Using a slightly simplified loop for speed on this massive grid
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
    
    # Displacement from original grid M, L (which we need to reconstruct)
    Orig_M, Orig_L = np.meshgrid(m_range, l_range)
    Disp = np.sqrt((Final_M - Orig_M)**2 + (Final_L - Orig_L)**2)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 12), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Visualization Strategy:
    # Use "Displacement" to define the map.
    # Dark = Stable (Low displacement)
    # Bright = Chaos (High displacement)
    # We use a Log scale because chaos explodes exponentially.
    
    im = ax.imshow(np.log1p(Disp), extent=[-RANGE, RANGE, -RANGE, RANGE], 
                   origin='lower', cmap='inferno_r') # Inverted Inferno: Dark=Stable, Fire=Chaos
    
    # Annotate our Home
    ax.scatter([-1.8], [0.0], color='cyan', marker='*', s=200, label='Our Universe (Zone 1)', zorder=10)
    
    ax.set_title("The Multiverse Grid: Super-Macro Stability Map\n(Dark Spots = Stable Universes)", color='white', fontsize=16)
    ax.set_xlabel("Mass Field Dimension", color='white')
    ax.set_ylabel("Coupling Field Dimension", color='white')
    
    # Add Grid markers to measure the periodicity
    # The twist is sin(2.5 * m), so period is 2pi/2.5 ~= 2.51
    # We expect structures every ~2.5 units
    
    plt.colorbar(im, label="Log Displacement (Instability)", fraction=0.046, pad=0.04)
    ax.legend(facecolor='black', labelcolor='white')
    
    plt.tight_layout()
    plt.savefig('super_macro_scan.png')
    plt.show()

if __name__ == "__main__":
    run_super_macro_scan()