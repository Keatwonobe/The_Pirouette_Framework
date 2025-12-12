import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # at top of file, near other imports

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

def run_geodesic_3d():
    """
    Render the vacuum stiffness landscape (Mass) as a 3D surface so we can see
    where the gladiator arches are warped / buckled.

    Uses the same compute_tensor_flow() as the 2D geodesic map.
    """
    # Compute the full tensor field
    M, L, VX, VY, Mass = compute_tensor_flow()

    # Subsample for a lighter plot
    step = 4  # 600x600 -> 150x150
    Ms = M[::step, ::step]
    Ls = L[::step, ::step]
    Zs = np.log1p(Mass[::step, ::step])  # log scale, like the 2D map

    # -------------------------
    # 1) Wide 3D view
    # -------------------------
    fig = plt.figure(figsize=(11, 9), facecolor="black")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("black")

    surf = ax.plot_surface(
        Ms, Ls, Zs,
        cmap="magma",
        linewidth=0,
        antialiased=True,
        alpha=0.95,
    )

    # Add particles at their local heights
    particles = [
        {"label": "Teal (EM)",   "pos": (-0.90, 0.81), "color": "cyan"},
        {"label": "Red (Weak)",  "pos": (-0.21, -0.60), "color": "red"},
        {"label": "Gold (Strong)", "pos": (2.46, 1.74), "color": "gold"},
    ]

    for p in particles:
        mx, lam = p["pos"]
        # Find nearest grid point indices
        i = np.argmin(np.abs(M[0, :] - mx))
        j = np.argmin(np.abs(L[:, 0] - lam))
        z = np.log1p(Mass[j, i])
        ax.scatter(mx, lam, z, color=p["color"], s=80, edgecolor="white")
        ax.text(mx, lam, z + 0.1, p["label"], color=p["color"], fontsize=10)

    ax.set_xlabel("Mass Field m", color="white")
    ax.set_ylabel("Coupling Field λ", color="white")
    ax.set_zlabel("log(1 + stiffness)", color="white")
    ax.set_title(
        "3D Vacuum Stiffness Surface\n"
        "(gladiator arches + central warp / buckle)",
        color="white", fontsize=14,
    )

    # Ticks/colors
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    fig.colorbar(surf, shrink=0.6, pad=0.1, label="log(1 + stiffness)")

    # Nice viewing angle to see the arches
    ax.view_init(elev=30, azim=-60)

    plt.tight_layout()
    plt.savefig("vacuum_stiffness_surface_3d.png", dpi=220)
    plt.show()

    # -------------------------
    # 2) Zoomed view of the buckle
    # -------------------------
    # Choose a window around the warped region
    m_min_zoom, m_max_zoom = -1.2, 1.2
    l_min_zoom, l_max_zoom = -2.0, 1.5

    mask_m = (M[0, :] >= m_min_zoom) & (M[0, :] <= m_max_zoom)
    mask_l = (L[:, 0] >= l_min_zoom) & (L[:, 0] <= l_max_zoom)

    Mz = M[np.ix_(mask_l, mask_m)]
    Lz = L[np.ix_(mask_l, mask_m)]
    Zz = np.log1p(Mass[np.ix_(mask_l, mask_m)])

    fig2 = plt.figure(figsize=(11, 9), facecolor="black")
    ax2 = fig2.add_subplot(111, projection="3d")
    ax2.set_facecolor("black")

    surf2 = ax2.plot_surface(
        Mz, Lz, Zz,
        cmap="magma",
        linewidth=0,
        antialiased=True,
        alpha=0.95,
    )

    # Overlay the same particles if they lie in the zoom window
    for p in particles:
        mx, lam = p["pos"]
        if (m_min_zoom <= mx <= m_max_zoom) and (l_min_zoom <= lam <= l_max_zoom):
            i = np.argmin(np.abs(M[0, :] - mx))
            j = np.argmin(np.abs(L[:, 0] - lam))
            z = np.log1p(Mass[j, i])
            ax2.scatter(mx, lam, z, color=p["color"], s=80, edgecolor="white")
            ax2.text(mx, lam, z + 0.05, p["label"], color=p["color"], fontsize=10)

    ax2.set_xlabel("Mass Field m (zoom)", color="white")
    ax2.set_ylabel("Coupling Field λ (zoom)", color="white")
    ax2.set_zlabel("log(1 + stiffness)", color="white")
    ax2.set_title(
        "Central Warp of the Vacuum Stiffness Surface\n"
        "(zoomed buckle where arches distort)",
        color="white", fontsize=14,
    )

    ax2.tick_params(colors="white")
    fig2.colorbar(surf2, shrink=0.6, pad=0.1, label="log(1 + stiffness)")

    # Adjust angle to really show the buckle
    ax2.view_init(elev=35, azim=-40)

    plt.tight_layout()
    plt.savefig("vacuum_stiffness_surface_3d_zoom.png", dpi=220)
    plt.show()


if __name__ == "__main__":
    run_geodesic_3d()