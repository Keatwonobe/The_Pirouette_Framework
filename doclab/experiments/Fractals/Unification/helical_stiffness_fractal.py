import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --------------------------------------------------
# PIROUETTE FRAMEWORK: TORSION MAP (KAPPA-HELICITY)
# --------------------------------------------------
# This script computes the Torsion (Curl) of the Geodesic Flow 
# to reveal the intrinsic spin structure (K-Helicity) of the vacuum.
# --------------------------------------------------

RES = 400 # Lowered resolution for faster computation of derivatives
TWIST = 3.8
M_MIN, M_MAX = -3.0, 3.0
L_MIN, L_MAX = -3.0, 3.0
EPS = 1e-3 # Step size for finite difference derivative

def get_force_vectorized(m, lam):
    # --- The Unified Field Laws (Unmodified) ---
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
    """ Computes the Geodesic Flow Vector Field (Min Stiffness Eigenvector) """
    print(f"Mapping the Geodesic Flow Vector Field ({RES}x{RES})...")
    
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # --- 1. Jacobian Calculation (Skipping details, assumes force is calculated) ---
    Fm, Flam = get_force_vectorized(M, L)
    Fm_m, Flam_m = get_force_vectorized(M + EPS, L)
    Fm_l, Flam_l = get_force_vectorized(M, L + EPS)
    
    dFx_dm = (Fm_m - Fm)/EPS
    dFx_dl = (Fm_l - Fm)/EPS
    dFy_dm = (Flam_m - Flam)/EPS
    dFy_dl = (Flam_l - Flam)/EPS
    
    # --- 2. Metric Tensor Components G = J^T J ---
    g11 = dFx_dm**2 + dFy_dm**2
    g12 = dFx_dm*dFx_dl + dFy_dm*dFy_dl
    g22 = dFx_dl**2 + dFy_dl**2
    
    # --- 3. Eigen-Decomposition for L2 (Min Stiffness) ---
    T = g11 + g22
    D = g11*g22 - g12**2
    L2 = T/2 - np.sqrt(np.maximum(T**2/4 - D, 0)) # Min Stiffness
    
    # --- 4. Eigenvectors (Flow Direction v) ---
    vx = g12
    vy = L2 - g11
    
    # Normalize
    mag = np.sqrt(vx**2 + vy**2) + 1e-9
    vx /= mag
    vy /= mag
    
    # Note: M and L (grid coordinates) are needed for the next derivative step
    return M, L, vx, vy

def compute_torsion_map(M, L, vx, vy):
    """
    Calculates the Torsion (Scalar Curl) of the Geodesic Flow Vector Field.
    
    Curl = (d(vy)/dm - d(vx)/dλ)
    """
    print("Computing Torsion (Curl) of the Geodesic Flow...")
    
    # Central difference (more accurate than forward)
    # The grid spacing d_m and d_lambda are the same
    h = M[0, 1] - M[0, 0] # Horizontal step size (dm)
    
    # Calculate d(vy)/dm
    dvy_dm = np.gradient(vy, axis=1) / h
    
    # Calculate d(vx)/dλ
    dvx_dl = np.gradient(vx, axis=0) / h
    
    # Torsion (Scalar Curl)
    torsion_map = dvy_dm - dvx_dl
    
    return torsion_map

def run_torsion_map():
    M, L, VX, VY = compute_tensor_flow()
    torsion_map = compute_torsion_map(M, L, VX, VY)
    
    # ----------------------------------------
    # PLOTTING THE KAPPA-HELICITY FIELD
    # ----------------------------------------
    
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    
    # Use a diverging colormap centered at zero to clearly show 
    # positive (CW spin) vs negative (CCW spin) torsion.
    im = ax.imshow(torsion_map, extent=[M_MIN, M_MAX, L_MIN, L_MAX], 
                   origin='lower', cmap='seismic', vmin=-np.max(np.abs(torsion_map)), 
                   vmax=np.max(np.abs(torsion_map)))
    
    # Add streamlines of the Geodesic flow for context
    ax.streamplot(M, L, VX, VY, color='white', density=1.5, linewidth=0.5, 
                  arrowstyle='-', start_points=None, zorder=2, minlength=0.1)
    
    ax.set_title("Intrinsic κ-Helicity Map (Geodesic Torsion)", 
              color='white', fontsize=16)
    ax.set_xlabel("Mass Field (m)", color='white')
    ax.set_ylabel("Coupling Field (λ)", color='white')
    ax.tick_params(colors='white')
    ax.set_facecolor('black')
    
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Geodesic Torsion (Scalar Curl)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.tight_layout()
    plt.savefig('vacuum_torsion_map.png')
    plt.show()

if __name__ == "__main__":
    run_torsion_map()