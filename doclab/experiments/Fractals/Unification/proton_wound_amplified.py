import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# =========================================================
#  PROTON WOUND AMPLIFIER
#  Visualizes the "Triply Lobed" Interaction Zone
# =========================================================

# Dynamics parameters (Proton Tuned)
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 150
EPSILON = 1e-5

# Viewport (Focused on the Core)
# slightly zoomed in from previous to see the lobes better
M_MIN, M_MAX = -0.02, 0.02
L_MIN, L_MAX = -0.02, 0.02
RES = 800  # High Res for detail

# Force Law (The 3-Body Field)
def get_force(m, lam):
    # Teal (Structure) at 150 deg
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red (Twist/Parity) at 270 deg
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold (Stability) at 30 deg
    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    # Mixing Weights
    angle_deg = np.degrees(np.arctan2(lam, m)) % 360.0

    diff_g = np.minimum(np.abs(angle_deg - 30.0), 360.0 - np.abs(angle_deg - 30.0))
    w_gold = np.exp(-(diff_g / 80.0)**2)

    diff_t = np.minimum(np.abs(angle_deg - 150.0), 360.0 - np.abs(angle_deg - 150.0))
    w_teal = np.exp(-(diff_t / 80.0)**2)

    diff_r = np.minimum(np.abs(angle_deg - 270.0), 360.0 - np.abs(angle_deg - 270.0))
    w_red  = np.exp(-(diff_r / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6
    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam

def normalize_angle_diff(delta):
    return np.arctan2(np.sin(delta), np.cos(delta))

def measure_helicity_field():
    print(f"[*] Scanning Interaction Zone ({RES}x{RES})...")
    m_vals = np.linspace(M_MIN, M_MAX, RES)
    l_vals = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_vals, l_vals)
    
    # Vectorized Simulation for Speed
    m1, l1 = M.copy(), L.copy()
    m2, l2 = M + EPSILON, L + EPSILON
    
    max_diff = np.zeros_like(M)
    active = np.ones_like(M, dtype=bool)
    
    # Physics Loop
    for _ in range(MAX_STEPS):
        if not np.any(active): break
        
        # Real
        Fm1, Flam1 = get_force(m1[active], l1[active])
        # Simplified drag calculation for speed (approximate w_red)
        # Re-calculating full weights every step is heavy, but necessary for accuracy.
        # We'll use a constant drag for the visualization scan to highlight topology.
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA) 
        
        m1[active] += Fm1 * DT * drag
        l1[active] += Flam1 * DT * drag
        
        # Shadow
        Fm2, Flam2 = get_force(m2[active], l2[active])
        m2[active] += Fm2 * DT * drag
        l2[active] += Flam2 * DT * drag
        
        # Divergence
        ang1 = np.arctan2(l1[active], m1[active])
        ang2 = np.arctan2(l2[active], m2[active])
        diff = np.abs(normalize_angle_diff(ang1 - ang2))
        
        # Update Max Diff
        current_max = max_diff[active]
        max_diff[active] = np.maximum(current_max, diff)
        
        # Escape condition
        escaped = (m1[active]**2 + l1[active]**2) > 50.0
        
        # We can't easily update 'active' based on 'escaped' subset without complex indexing
        # so we just let them run (vectorized is fast enough) or ignore escape for this map.
        
    return np.log1p(max_diff)

def plot_amplified_wound():
    H = measure_helicity_field()
    
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    
    # 1. The Field (Heatmap)
    # Use 'magma_r' (reversed) so the stable basin (low helicity) is light/colored
    # and the chaotic outside is dark, or vice versa.
    # Let's use a custom "Wound" map: Dark background, glowing edges.
    
    # Edge Detection (Gradient of Helicity)
    # This highlights the "Walls" of the basin
    gy, gx = np.gradient(H)
    edges = np.sqrt(gx**2 + gy**2)
    
    # Composite: Base + Edges
    # Base = Stability (Low H) -> Blue/Teal
    # Edges = Instability -> Gold/Red
    
    img = np.zeros((RES, RES, 3))
    
    # Normalize
    h_norm = (H - H.min()) / (H.max() - H.min())
    e_norm = (edges - edges.min()) / (edges.max() - edges.min())
    
    # Blue Channel (Stability) - Invert H (Low H = High Blue)
    img[:, :, 2] = (1.0 - h_norm) * 0.8
    
    # Red/Green (Edges/Wound) - High Edge = Gold
    img[:, :, 0] = np.clip(e_norm * 3.0, 0, 1) # Boost contrast
    img[:, :, 1] = np.clip(e_norm * 2.0, 0, 1)
    
    ax.imshow(img, origin='lower', extent=[M_MIN, M_MAX, L_MIN, L_MAX])

    ax.set_title("THE PROTON WOUND | Triply Lobed Interaction Zone", color='white', fontsize=16)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig("proton_wound_amplified.png", dpi=150)
    print("✅ Wound Visualized: proton_wound_amplified.png")

if __name__ == "__main__":
    plot_amplified_wound()