import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import njit, prange
import math
import time

# ============================================================
# 0. HYPERMATH (High-Precision ND Arithmetic)
# ============================================================

SPLIT = 134217729.0

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
    """
    The 'Long Cane': Translates a high-precision coordinate 
    by a standard scalar offset without losing the tail precision.
    """
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
# 1. FORCE LAW (Standard Physics Core)
# ============================================================

TWIST = 3.8

@njit(fastmath=True)
def get_force_scalar(m, lam):
    # Teal component
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red component
    F_red_m = -(m - 0.0)
    p_violation = TWIST * math.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold proto-component
    sum_m   = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    magnitude = math.sqrt(sum_m * sum_m + sum_lam * sum_lam)
    
    scaling_factor = math.sqrt(magnitude) if magnitude > 1e-16 else 0.0

    F_gold_m   = sum_m   * scaling_factor
    F_gold_lam = sum_lam * scaling_factor

    # Angular weights
    angle = math.degrees(math.atan2(lam, m)) % 360.0

    def gauss_weight(angle, center_deg):
        diff = abs(angle - center_deg)
        if diff > 180.0: diff = 360.0 - diff
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
# 2. ADAPTIVE STIFFNESS
# ============================================================

@njit(fastmath=True)
def get_stiffness_from_dd(m_dd, l_dd, eps):
    """
    Takes High-Precision inputs (Double-Double arrays), 
    collapses them to the best possible float at the last second, 
    and probes the stiffness.
    """
    # Collapse to scalar for the force function
    # Note: If zoom is 1e-31, this collapse is where we hit the physics wall
    # unless the force law itself is upgraded. 
    # But this ensures the INPUT is clean.
    m = m_dd[0] + m_dd[1]
    lam = l_dd[0] + l_dd[1]

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
    
    return math.sqrt(L1)

# ============================================================
# 3. HYPER-ACCURATE POINT SCANNER
# ============================================================

@njit(parallel=True)
def scan_surface_nd(center_m_nd, center_l_nd, zoom, res):
    """
    Uses the 'Long Cane' method: 
    Iterates pixels as offsets, translates the ND center, 
    and samples stiffness.
    """
    grid = np.zeros((res, res), dtype=np.float64)
    
    # Adaptive epsilon: roughly 1/1000th of a pixel width
    # We clamp it to avoid underflowing machine precision (1e-16)
    # unless we really trust the small numbers.
    step_eps = (zoom * 2.0 / res) * 0.01
    if step_eps < 1e-15:
        step_eps = 1e-15

    # Center of image indices
    c_idx = (res - 1) / 2.0
    scale = (zoom * 2.0) / res

    for y in prange(res):
        # Calculate Y Offset
        off_y = (y - c_idx) * scale
        
        # TAP: Translate Center Y by Offset Y (High Precision)
        loc_y_nd = nd_translate(center_l_nd, off_y)
        
        for x in range(res):
            # Calculate X Offset
            off_x = (x - c_idx) * scale
            
            # TAP: Translate Center X by Offset X (High Precision)
            loc_x_nd = nd_translate(center_m_nd, off_x)
            
            # Measure
            grid[y, x] = get_stiffness_from_dd(loc_x_nd, loc_y_nd, step_eps)
            
    return grid

def render_hyper_scan(cx_val, cy_val, zoom, res=100, filename="vacuum_tip_scan.png"):
    print(f"[-] Initializing Hyper-Scan (Long Cane method)...")
    print(f"    Zoom: {zoom:e}")
    
    # 1. Construct the High-Precision Center (Double-Double equivalent)
    # We split the float inputs into hi/lo to simulate the structure, 
    # though initially lo is 0 if input is standard float.
    cx_nd = np.array([cx_val, 0.0], dtype=np.float64)
    cy_nd = np.array([cy_val, 0.0], dtype=np.float64)
    
    # 2. Run the ND Scanner
    t0 = time.time()
    Z_grid = scan_surface_nd(cx_nd, cy_nd, zoom, res)
    dt = time.time() - t0
    print(f"[+] Scan complete in {dt:.2f}s")

    # 3. Prepare Relatable Coordinates for Plotting
    # We map the grid indices back to relative offsets (x 1e-XX)
    vals = np.linspace(-zoom, zoom, res)
    M_grid, L_grid = np.meshgrid(vals, vals)

    # 4. Plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Surface
    surf = ax.plot_surface(M_grid, L_grid, Z_grid, cmap='magma', 
                           edgecolor='none', alpha=0.9, antialiased=True)

    # Floor Contour (shadow)
    z_min = Z_grid.min()
    z_range = Z_grid.max() - z_min
    if z_range == 0: z_range = 1.0 # prevent div by zero on flat planes
    
    offset = z_min - (z_range * 0.1)
    ax.contourf(M_grid, L_grid, Z_grid, zdir='z', offset=offset, cmap='magma', alpha=0.4)

    # Formatting
    ax.set_title(f"Vacuum Stiffness Tip\n(Long-Cane Scan @ {zoom:.1e})", fontsize=14)
    ax.set_xlabel('$\Delta m$ (offset)')
    ax.set_ylabel('$\Delta \lambda$ (offset)')
    ax.set_zlabel('Stiffness $\sqrt{\lambda_{max}(G)}$')
    ax.set_zlim(offset, Z_grid.max())

    # Force scientific notation on axes for readability
    ax.ticklabel_format(style='sci', scilimits=(0,0), axis='both')

    plt.colorbar(surf, shrink=0.5, aspect=10, label="Stiffness")
    plt.savefig(filename, dpi=300)
    print(f"[+] Saved render to {filename}")
    plt.close()

# ============================================================
# 4. EXECUTION
# ============================================================

if __name__ == "__main__":
    # The peak coordinates you found
    PEAK_M = -3.68863054184929439e-06
    PEAK_L = -9.6673215316825175e-05
    
    # Try a zoom that pushes the limits but is visible
    # 1e-14 is the safe limit for float64 physics. 
    # Because we are using ND-translation, we might get cleaner lines even at 1e-15.
    RENDER_ZOOM = 2.0e-14

    render_hyper_scan(PEAK_M, PEAK_L, RENDER_ZOOM, res=150, filename="vacuum_tip_scan.png")