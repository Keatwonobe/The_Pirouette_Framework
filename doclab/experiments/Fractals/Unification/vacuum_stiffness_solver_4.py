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
# 2. ROBUST STIFFNESS (Central Difference)
# ============================================================

@njit(fastmath=True)
def get_stiffness_robust(m_dd, l_dd, eps):
    """
    Uses Central Difference for cleaner gradients.
    Decouples the probe size (eps) from the position precision.
    """
    # Collapse High-Precision coordinates to best possible float
    m = m_dd[0] + m_dd[1]
    lam = l_dd[0] + l_dd[1]

    # Central Difference: f(x+h) - f(x-h) / 2h
    # This is much more stable than Forward Difference at small scales.
    
    # Gradient w.r.t m
    Fm_plus_m, Fl_plus_m = get_force_scalar(m + eps, lam)
    Fm_minus_m, Fl_minus_m = get_force_scalar(m - eps, lam)
    
    dFx_dm = (Fm_plus_m - Fm_minus_m) / (2 * eps)
    dFy_dm = (Fl_plus_m - Fl_minus_m) / (2 * eps)

    # Gradient w.r.t lambda
    Fm_plus_l, Fl_plus_l = get_force_scalar(m, lam + eps)
    Fm_minus_l, Fl_minus_l = get_force_scalar(m, lam - eps)

    dFx_dl = (Fm_plus_l - Fm_minus_l) / (2 * eps)
    dFy_dl = (Fl_plus_l - Fl_minus_l) / (2 * eps)

    # Metric Tensor G = J^T J
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
def scan_surface_robust(center_m_nd, center_l_nd, zoom, res, probe_size):
    """
    Iterates pixels as offsets, translates the ND center, 
    and samples stiffness using a robust fixed-size probe.
    """
    grid = np.zeros((res, res), dtype=np.float64)
    
    # Center of image indices
    c_idx = (res - 1) / 2.0
    scale = (zoom * 2.0) / res

    for y in prange(res):
        off_y = (y - c_idx) * scale
        loc_y_nd = nd_translate(center_l_nd, off_y)
        
        for x in range(res):
            off_x = (x - c_idx) * scale
            loc_x_nd = nd_translate(center_m_nd, off_x)
            
            # Use fixed probe_size for derivative stability
            grid[y, x] = get_stiffness_robust(loc_x_nd, loc_y_nd, probe_size)
            
    return grid

def render_robust_scan(cx_val, cy_val, zoom, res=100, filename="vacuum_tip_scan.png"):
    # STABILITY FIX:
    # We set a fixed 'probe size' (epsilon) for the derivative.
    # 1e-8 is the "sweet spot" for double precision (sqrt(machine_epsilon)).
    # This measures the local slope accurately without resolving the "digital sand".
    PROBE_SIZE = 1e-8

    print(f"[-] Initializing Robust Scan (Central Diff)...")
    print(f"    Zoom: {zoom:e}")
    print(f"    Probe Size: {PROBE_SIZE:e}")
    
    cx_nd = np.array([cx_val, 0.0], dtype=np.float64)
    cy_nd = np.array([cy_val, 0.0], dtype=np.float64)
    
    t0 = time.time()
    Z_grid = scan_surface_robust(cx_nd, cy_nd, zoom, res, PROBE_SIZE)
    dt = time.time() - t0
    print(f"[+] Scan complete in {dt:.2f}s")

    # Coordinates for plotting
    vals = np.linspace(-zoom, zoom, res)
    M_grid, L_grid = np.meshgrid(vals, vals)

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(M_grid, L_grid, Z_grid, cmap='magma', 
                           edgecolor='none', alpha=0.9, antialiased=True)

    # Floor Contour
    z_min = Z_grid.min()
    z_max = Z_grid.max()
    z_range = z_max - z_min
    if z_range == 0: z_range = 1.0
    
    offset = z_min - (z_range * 0.1)
    ax.contourf(M_grid, L_grid, Z_grid, zdir='z', offset=offset, cmap='magma', alpha=0.4)

    # Raw strings (r"") fix the syntax warnings
    ax.set_title(f"Vacuum Stiffness Tip\n(Robust Scan @ {zoom:.1e})", fontsize=14)
    ax.set_xlabel(r'$\Delta m$ (offset)')
    ax.set_ylabel(r'$\Delta \lambda$ (offset)')
    ax.set_zlabel(r'Stiffness $\sqrt{\lambda_{max}(G)}$')
    ax.set_zlim(offset, z_max)

    ax.ticklabel_format(style='sci', scilimits=(0,0), axis='both')

    plt.colorbar(surf, shrink=0.5, aspect=10, label="Stiffness")
    plt.savefig(filename, dpi=300)
    print(f"[+] Saved render to {filename}")
    plt.close()

# ============================================================
# 4. EXECUTION
# ============================================================

if __name__ == "__main__":
    PEAK_M = -3.68863054184929439e-06
    PEAK_L = -9.6673215316825175e-05
    
    # 2.0e-14 is incredibly deep. 
    # If the surface is smooth (not fractal), this should look like a flat plane or a gentle dome.
    RENDER_ZOOM = 2.0e-14

    render_robust_scan(PEAK_M, PEAK_L, RENDER_ZOOM, res=150, filename="vacuum_tip_scan.png")