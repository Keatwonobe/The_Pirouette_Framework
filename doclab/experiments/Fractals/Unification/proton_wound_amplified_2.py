import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# =========================================================
#  PROTON BRAID ZOOM (Micro-Scale Topology)
# =========================================================

# Dynamics parameters
TWIST = 3.8
GAMMA = 0.5
DT    = -0.005 # Slower time step for precision at high zoom
MAX_STEPS = 5 # Longer run to let the braid fold
EPSILON = 1e-6

# MICRO VIEWPORT (Zoom 0.02)
ZOOM = 0.025
M_MIN, M_MAX = -ZOOM, ZOOM
L_MIN, L_MAX = -ZOOM, ZOOM
RES = 800

def get_force(m, lam):
    # Unified Field Laws
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    angle_deg = np.degrees(np.arctan2(lam, m)) % 360.0

    # Sharper mixing for micro-scale distinctness
    diff_g = np.minimum(np.abs(angle_deg - 30.0), 360.0 - np.abs(angle_deg - 30.0))
    w_gold = np.exp(-(diff_g / 40.0)**2) # Sharper

    diff_t = np.minimum(np.abs(angle_deg - 150.0), 360.0 - np.abs(angle_deg - 150.0))
    w_teal = np.exp(-(diff_t / 40.0)**2)

    diff_r = np.minimum(np.abs(angle_deg - 270.0), 360.0 - np.abs(angle_deg - 270.0))
    w_red  = np.exp(-(diff_r / 40.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6
    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam

def run_braid_scan():
    print(f"[*] Scanning Micro-Braid ({RES}x{RES}) at Zoom {ZOOM}...")
    m_vals = np.linspace(M_MIN, M_MAX, RES)
    l_vals = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_vals, l_vals)
    
    # Simulation Arrays
    m = M.copy()
    l = L.copy()
    
    # We track TOTAL DISPLACEMENT (The folding action)
    # Instead of just lifetime, we track how far they wander
    trajectory_length = np.zeros_like(M)
    active = np.ones_like(M, dtype=bool)
    
    for t in range(MAX_STEPS):
        # RK2 Integration for stability
        Fm1, Flam1 = get_force(m[active], l[active])
        
        # Predictor
        m_pred = m[active] + Fm1 * DT
        l_pred = l[active] + Flam1 * DT
        
        # Corrector
        Fm2, Flam2 = get_force(m_pred, l_pred)
        
        dm = 0.5 * (Fm1 + Fm2) * DT
        dl = 0.5 * (Flam1 + Flam2) * DT
        
        m[active] += dm
        l[active] += dl
        
        # Accumulate Path Length (The Braid)
        step_dist = np.sqrt(dm**2 + dl**2)
        trajectory_length[active] += step_dist
        
        # Divergence Check (Stop if they fly off)
        # At this zoom, flying off means leaving the frame
        in_bounds = (np.abs(m[active]) < ZOOM*2) & (np.abs(l[active]) < ZOOM*2)
        
        # We KEEP the ones that stay (The Knot)
        # But we stop integrating the ones that left to save time
        # Actually, let's just track everything for the flow pattern
        pass

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    
    # Log-Enhance the Braid
    # The "Knot" will have high trajectory length (orbiting)
    # The "Flow" will have lower length (passing through)
    data = np.log1p(trajectory_length)
    
    # Custom "Deep Ocean" Colormap
    # Black -> Blue -> Cyan -> White
    colors = [(0, 0, 0), (0.1, 0.1, 0.4), (0, 0.8, 0.8), (1, 1, 1)]
    cmap = LinearSegmentedColormap.from_list("abyss", colors, N=256)
    
    im = ax.imshow(data, origin='lower', cmap=cmap, extent=[M_MIN, M_MAX, L_MIN, L_MAX])

    ax.set_title(f"THE LYAPUNOV BRAID | Micro-Zoom {ZOOM}", color='white', fontsize=14)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig("proton_braid_zoom.png", dpi=150)
    print("✅ Braid Visualized: proton_braid_zoom.png")

if __name__ == "__main__":
    run_braid_scan()