import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: GEODESIC FLOW MAP
# --------------------------------------------------
# This script visualizes the "Grain of the Vacuum."
# It computes the Mass Tensor G = J^T J, extracts the
# Principal Eigenvectors, and performs a Streamline
# plot to show the natural "Highways" of spacetime.
# --------------------------------------------------

RES = 600
TWIST = 3.8
M_MIN, M_MAX = -3.0, 3.0
L_MIN, L_MAX = -3.0, 3.0
EPS = 1e-3

def get_force_vectorized(m, lam):
    # --- The Unified Field Laws ---
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude) # F^1.5 scaling
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Gaussian Mixing
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
    
    return Fm, Flam

def compute_tensor_flow():
    print(f"Mapping the Grain of Spacetime ({RES}x{RES})...")
    
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # 1. Jacobian Calculation (The changing vacuum)
    Fm, Flam = get_force_vectorized(M, L)
    Fm_m, Flam_m = get_force_vectorized(M + EPS, L)
    Fm_l, Flam_l = get_force_vectorized(M, L + EPS)
    
    dFx_dm = (Fm_m - Fm)/EPS
    dFx_dl = (Fm_l - Fm)/EPS
    dFy_dm = (Flam_m - Flam)/EPS
    dFy_dl = (Flam_l - Flam)/EPS
    
    # 2. Metric Tensor Components G = J^T J
    g11 = dFx_dm**2 + dFy_dm**2
    g12 = dFx_dm*dFx_dl + dFy_dm*dFy_dl
    g22 = dFx_dl**2 + dFy_dl**2
    
    # 3. Eigen-Decomposition
    # We want the direction of MAX stiffness (The "Wall")
    # and MIN stiffness (The "Valley/Flow")
    
    # Trace and Det
    T = g11 + g22
    D = g11*g22 - g12**2
    
    # Eigenvalues
    L1 = T/2 + np.sqrt(np.maximum(T**2/4 - D, 0)) # Max Stiffness
    L2 = T/2 - np.sqrt(np.maximum(T**2/4 - D, 0)) # Min Stiffness
    
    # Eigenvectors (for L2 - The Valley/Flow direction)
    # The flow of time/matter usually follows the path of least resistance (lowest stiffness)
    
    # v = [g12, L2 - g11] (Standard formula for eigenvector of 2x2)
    # If g12 is zero, handle separately, but noise handles it usually.
    
    vx = g12
    vy = L2 - g11
    
    # Normalize
    mag = np.sqrt(vx**2 + vy**2) + 1e-9
    vx /= mag
    vy /= mag
    
    return M, L, vx, vy, np.sqrt(L1) # Return L1 (Mass) for coloring

def run_geodesic_vis():
    M, L, VX, VY, Mass = compute_tensor_flow()
    
    fig = plt.figure(figsize=(12, 12), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # 1. The Background: Mass Magnitude
    # Darker = Empty Space, Brighter = Massive Objects
    im = ax.imshow(np.log1p(Mass), extent=[M_MIN, M_MAX, L_MIN, L_MAX], 
                   origin='lower', cmap='magma', alpha=0.6)
    
    # 2. The Flow: Streamlines of the Vacuum Grain
    # This visualizes the "Geodesics" or "Field Lines" of the unified field
    print("Tracing vacuum streamlines...")
    strm = ax.streamplot(M, L, VX, VY, color='cyan', density=2.5, 
                         linewidth=0.6, arrowsize=0.8, arrowstyle='->')
    
    # 3. The Particles
    particles = [
        {'label': 'Teal (EM)', 'pos': (-0.90, 0.81), 'color': 'white'},
        {'label': 'Red (Weak)',    'pos': (-0.21, -0.60), 'color': 'white'},
        {'label': 'Gold (Strong)', 'pos': (2.46, 1.74),   'color': 'white'},
    ]
    
    for p in particles:
        mx, my = p['pos']
        ax.scatter(mx, my, color=p['color'], s=150, marker='o', zorder=10)
        ax.scatter(mx, my, color='black', s=50, marker='o', zorder=11)
        ax.text(mx+0.15, my, p['label'], color='white', fontsize=12, fontweight='bold', zorder=12)

    ax.set_title("The Geodesic Flow of the Vacuum\n(Cyan Lines = Paths of Least Resistance)", 
                 color='white', fontsize=16)
    ax.set_xlabel("Mass Field Dimension", color='white')
    ax.set_ylabel("Coupling Field Dimension", color='white')
    
    ax.tick_params(colors='white')
    ax.grid(False)
    
    # Add a colorbar for Mass
    cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
    cbar.set_label("Vacuum Stiffness (Mass)", color='white')
    cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')

    plt.tight_layout()
    plt.savefig('geodesic_flow_map.png')
    plt.show()

if __name__ == "__main__":
    run_geodesic_vis()