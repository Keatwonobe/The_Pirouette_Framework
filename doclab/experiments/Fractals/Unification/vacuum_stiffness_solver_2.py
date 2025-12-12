import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import njit, prange
import math
import time

# ============================================================
# 0. HIGH-PRECISION ND ARITHMETIC (Preserved)
# ============================================================

SPLIT = 134217729.0

@njit(fastmath=True)
def split_double(a):
    c = SPLIT * a
    a_h = c - (c - a)
    a_l = a - a_h
    return a_h, a_l

@njit(fastmath=True)
def two_sum(a, b):
    s = a + b
    v = s - a
    e = (a - (s - v)) + (b - v)
    return s, e

@njit(fastmath=True)
def renormalize_nd(x):
    for i in range(len(x) - 1, 0, -1):
        x[i-1], x[i] = two_sum(x[i-1], x[i])
    return x

@njit(fastmath=True)
def nd_translate(center_nd, offset_s):
    N = len(center_nd)
    result_nd = np.zeros_like(center_nd)
    remainder = offset_s
    for i in range(N):
        s, e = two_sum(center_nd[i], remainder)
        result_nd[i] = s
        remainder = e
    result_nd = renormalize_nd(result_nd)
    return result_nd

# ============================================================
# 1. VACUUM FORCE LAW
# ============================================================

TWIST = 3.8

@njit(fastmath=True)
def get_force_scalar(m, lam):
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * math.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m   = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    magnitude = math.sqrt(sum_m * sum_m + sum_lam * sum_lam)
    
    # Safety to prevent NaN at absolute zero
    if magnitude < 1e-16:
        scaling_factor = 0.0
    else:
        scaling_factor = math.sqrt(magnitude)

    F_gold_m   = sum_m   * scaling_factor
    F_gold_lam = sum_lam * scaling_factor

    angle = math.degrees(math.atan2(lam, m)) % 360.0

    def gauss_weight(angle, center_deg):
        diff = abs(angle - center_deg)
        if diff > 180.0:
            diff = 360.0 - diff
        return math.exp(- (diff / 80.0) ** 2)

    w_gold = gauss_weight(angle, 30.0)
    w_teal = gauss_weight(angle, 150.0)
    w_red  = gauss_weight(angle, 270.0)

    tot = w_gold + w_teal + w_red + 1e-12
    nw_gold = w_gold / tot
    nw_teal = w_teal / tot
    nw_red  = w_red  / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam

# ============================================================
# 2. ADAPTIVE STIFFNESS FIELD
# ============================================================

@njit(fastmath=True)
def get_stiffness_scalar_adaptive(m, lam, eps):
    """
    Calculates stiffness using an epsilon proportional to the zoom level.
    """
    Fm,  Fl  = get_force_scalar(m,        lam)
    Fm_m, Fl_m = get_force_scalar(m + eps, lam)
    Fm_l, Fl_l = get_force_scalar(m,        lam + eps)

    dFx_dm = (Fm_m - Fm) / eps
    dFx_dl = (Fm_l - Fm) / eps
    dFy_dm = (Fl_m - Fl) / eps
    dFy_dl = (Fl_l - Fl) / eps

    g11 = dFx_dm * dFx_dm + dFy_dm * dFy_dm
    g12 = dFx_dm * dFx_dl + dFy_dm * dFy_dl
    g22 = dFx_dl * dFx_dl + dFy_dl * dFy_dl

    T = g11 + g22
    D = g11 * g22 - g12 * g12

    disc = T * T * 0.25 - D
    if disc < 0.0: disc = 0.0
    L1 = 0.5 * T + math.sqrt(disc)
    if L1 < 0.0: L1 = 0.0

    return math.sqrt(L1)

@njit(fastmath=True)
def get_stiffness_dd_adaptive(m_dd, l_dd, eps):
    m = m_dd[0] + m_dd[1]
    lam = l_dd[0] + l_dd[1]
    return get_stiffness_scalar_adaptive(m, lam, eps)

# ============================================================
# 3. 3D POINT SCAN RENDERER
# ============================================================

def render_peak_topology(cx_val, cy_val, zoom, res=100, filename="peak_topology.png"):
    """
    Renders a 3D surface plot of the peak geometry.
    """
    print(f"[-] Generating 3D Topology scan centered at:")
    print(f"    m: {cx_val}")
    print(f"    λ: {cy_val}")
    print(f"    zoom: {zoom}")

    # Set up the grid arrays
    m_vals = np.linspace(-zoom, zoom, res)
    l_vals = np.linspace(-zoom, zoom, res)
    
    M_grid, L_grid = np.meshgrid(m_vals, l_vals)
    Z_grid = np.zeros((res, res))

    # Calculate Adaptive Epsilon
    # The derivative step must be smaller than the visual features
    # but large enough to avoid float underflow.
    adaptive_eps = zoom / (res * 10.0) 
    if adaptive_eps < 1e-15:
        # Warning: At 1e-31 zoom, standard float math breaks down.
        # We clamp eps to machine precision for calculation, even if grid is smaller.
        # This might result in a flat plane if zoom is << 1e-15.
        adaptive_eps = 1e-15 
        print("[!] WARNING: Zoom is below float64 machine epsilon.")
        print("    Geometry may appear flat due to precision limits.")
        print("    Try zooming out to 1e-14 if the plot is flat.")

    # Convert center to ND format for the wrapper
    cx_nd = np.array([cx_val, 0.0]) # Simplified for this render pass
    cy_nd = np.array([cy_val, 0.0])

    print("[-] Computing stiffness matrix...")
    for i in range(res):
        for j in range(res):
            # Calculate absolute coordinates
            local_m = cx_val + M_grid[i, j]
            local_l = cy_val + L_grid[i, j]
            
            # Pass to solver
            # We construct temp DD arrays just to satisfy the function signature
            # or call the scalar one directly since we are using floats here anyway
            s = get_stiffness_scalar_adaptive(local_m, local_l, adaptive_eps)
            Z_grid[i, j] = s

    # --- PLOTTING ---
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(M_grid, L_grid, Z_grid, cmap='magma', 
                           edgecolor='none', antialiased=False, alpha=0.9)

    # Add contour projection on the bottom
    offset = Z_grid.min() - (Z_grid.max() - Z_grid.min()) * 0.1
    ax.contourf(M_grid, L_grid, Z_grid, zdir='z', offset=offset, cmap='magma', alpha=0.5)

    ax.set_title(f"Stiffness Peak Geometry\n(Zoom: {zoom:.2e})", fontsize=14)
    ax.set_xlabel('$\Delta m$')
    ax.set_ylabel('$\Delta \lambda$')
    ax.set_zlabel('Stiffness $\sqrt{\lambda_{max}(G)}$')
    
    # Tighten view
    ax.set_zlim(offset, Z_grid.max())
    
    plt.colorbar(surf, shrink=0.5, aspect=10, label="Stiffness")
    plt.savefig(filename, dpi=300)
    print(f"[+] Saved 3D topology scan to {filename}")
    plt.close()

# ============================================================
# 4. EXECUTION
# ============================================================

if __name__ == "__main__":
    # coordinates from your previous successful run
    PEAK_M = -3.68863054184929439e-06
    PEAK_L = -9.6673215316825175e-05
    
    # We back off the zoom slightly to ensure we catch the curve geometry
    # 1e-31 is too deep for standard float math (precision ends at 1e-16).
    # Setting zoom to 1e-14 to visualize the local "tip" structure properly.
    # If you want the exact 1e-31, change this, but it will likely look flat.
    RENDER_ZOOM = 1.0e-14 

    render_peak_topology(PEAK_M, PEAK_L, RENDER_ZOOM, res=120, filename="vacuum_tip_scan.png")