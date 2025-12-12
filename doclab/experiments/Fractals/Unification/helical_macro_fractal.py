import numpy as np
import matplotlib.pyplot as plt
import logging
from matplotlib.colors import LogNorm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("MACRO_HELICITY")

# --------------------------------------------------
# PIROUETTE SUPER-MACRO SCAN: HELICITY GRID
# --------------------------------------------------
# Isolates the Angular Drift (Rotational Memory) on the Multiverse Grid scale.
# --------------------------------------------------

# Constants (Using values optimized for structure visualization)
TWIST = 2.83814 
GAMMA = 0.02
DT = 0.01
STEPS = 2000

# Viewport (Using a practical range for quick visualization)
RANGE = 60.0  # Reduced from 60000000.0 for execution speed
RES = 600

def get_force_vectorized(m, lam):
    # --- The Unified Physics (Unmodified) ---
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

def run_macro_helicity_scan():
    logger.info(f"Running Macro Helicity Scan (Range +/-{RANGE})...")
    
    m_range = np.linspace(-RANGE, RANGE, RES)
    l_range = np.linspace(-RANGE, RANGE, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # --- HELICITY METRIC INITIALIZATION ---
    # We track the total unwrapped angle change.
    
    # Initial Angle
    prev_ang = np.arctan2(lam, m) 
    # Total accumulated angle (Helical Action)
    total_ang_drift = np.zeros_like(m) 
    
    logger.info("Simulating Angular Drift (Helicity)...")
    
    for step in range(STEPS):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        
        # Symplectic-Damped Integration Step (Unmodified)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        # --- HELICITY TRACKING ---
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        
        # Vectorized Unwrap: handles the 2pi boundary jump
        delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        
        total_ang_drift += delta # Accumulate the signed drift
        prev_ang = curr_ang
        
    # Reshape
    Helicity_Drift = total_ang_drift.reshape(RES, RES)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 12), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Visualization Strategy:
    # Use the absolute value of the drift normalized to 2pi (Winding Count)
    plot_data = np.abs(Helicity_Drift) / (2 * np.pi) 
    
    # Use a cyclic colormap to emphasize the integer winding structure (The Multiverse Grid)
    im = ax.imshow(plot_data, extent=[-RANGE, RANGE, -RANGE, RANGE], 
                   origin='lower', cmap='twilight_shifted') 
    
    # Annotate our Home (Relative location is conserved)
    ax.scatter([-1.8], [0.0], color='cyan', marker='*', s=200, label='Our Universe (Zone 1)', zorder=10)
    
    ax.set_title("The Multiverse Grid: Macro-Scale κ-Helicity Map\n(Winding Count = Rotational Drift)", color='white', fontsize=16)
    ax.set_xlabel("Mass Field Dimension", color='white')
    ax.set_ylabel("Coupling Field Dimension", color='white')
    
    plt.colorbar(im, label="Total Winding Count (Accumulated Helicity)", fraction=0.046, pad=0.04)
    ax.legend(facecolor='black', labelcolor='white')
    
    plt.tight_layout()
    plt.savefig('macro_helicity_grid.png')
    plt.show()

if __name__ == "__main__":
    run_macro_helicity_scan()