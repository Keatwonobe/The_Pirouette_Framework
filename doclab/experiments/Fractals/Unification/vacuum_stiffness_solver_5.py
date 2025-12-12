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
# 1. FORCE LAW (The Physics of the Puncture)
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
# 2. ANNEALED STIFFNESS PROBE
# ============================================================

@njit(fastmath=True)
def get_stiffness_kernel(m, l, eps):
    """
    Standard central difference stiffness calculation.
    """
    # Gradient w.r.t m
    Fm_plus_m, Fl_plus_m = get_force_scalar(m + eps, l)
    Fm_minus_m, Fl_minus_m = get_force_scalar(m - eps, l)
    
    dFx_dm = (Fm_plus_m - Fm_minus_m) / (2 * eps)
    dFy_dm = (Fl_plus_m - Fl_minus_m) / (2 * eps)

    # Gradient w.r.t lambda
    Fm_plus_l, Fl_plus_l = get_force_scalar(m, l + eps)
    Fm_minus_l, Fl_minus_l = get_force_scalar(m, l - eps)

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

@njit(fastmath=True)
def get_annealed_stiffness(m_dd, l_dd, eps, smoothing_rad):
    """
    Super-sampling: Takes the center point and averages it with
    4 surrounding points to simulate 'cooling' the lattice.
    This removes high-frequency numerical noise.
    """
    m_c = m_dd[0] + m_dd[1]
    l_c = l_dd[0] + l_dd[1]

    # Sample Center
    s0 = get_stiffness_kernel(m_c, l_c, eps)
    
    # Sample North, South, East, West at smoothing radius
    s1 = get_stiffness_kernel(m_c + smoothing_rad, l_c, eps)
    s2 = get_stiffness_kernel(m_c - smoothing_rad, l_c, eps)
    s3 = get_stiffness_kernel(m_c, l_c + smoothing_rad, eps)
    s4 = get_stiffness_kernel(m_c, l_c - smoothing_rad, eps)

    # Gaussian weights (Center is heaviest)
    return (s0 * 0.4) + ((s1 + s2 + s3 + s4) * 0.15)

# ============================================================
# 3. GEOMETRY SCANNER
# ============================================================

@njit(parallel=True)
def scan_geometry(center_m_nd, center_l_nd, zoom, res):
    grid = np.zeros((res, res), dtype=np.float64)
    
    c_idx = (res - 1) / 2.0
    scale = (zoom * 2.0) / res
    
    # The "Cane" length for the derivative
    probe_eps = zoom * 0.001 
    # The "Smoothing" radius for the annealing
    smooth_rad = scale * 0.5 

    for y in prange(res):
        off_y = (y - c_idx) * scale
        loc_y_nd = nd_translate(center_l_nd, off_y)
        
        for x in range(res):
            off_x = (x - c_idx) * scale
            loc_x_nd = nd_translate(center_m_nd, off_x)
            
            val = get_annealed_stiffness(loc_x_nd, loc_y_nd, probe_eps, smooth_rad)
            grid[y, x] = val
            
    return grid

def render_needle(cx_val, cy_val, zoom, res=150, filename="vacuum_needle.png"):
    print(f"[-] Initializing Geometry Scan (Annealing Enabled)...")
    print(f"    Zoom Level: {zoom:e}")
    print(f"    Target: The Needle Geometry")
    
    cx_nd = np.array([cx_val, 0.0], dtype=np.float64)
    cy_nd = np.array([cy_val, 0.0], dtype=np.float64)
    
    t0 = time.time()
    Z_grid = scan_geometry(cx_nd, cy_nd, zoom, res)
    dt = time.time() - t0
    print(f"[+] Scan complete in {dt:.2f}s")

    # Prepare data for 3D plot
    vals = np.linspace(-zoom, zoom, res)
    M_grid, L_grid = np.meshgrid(vals, vals)

    # Logarithmic scaling to handle the infinite nature of the spike
    # We subtract the min to focus on the shape, not the absolute height
    Z_log = np.log1p(Z_grid) 

    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')

    # Plot Surface
    surf = ax.plot_surface(M_grid, L_grid, Z_log, cmap='magma', 
                           edgecolor='none', alpha=1.0, antialiased=True, rcount=100, ccount=100)

    # Add contour at the bottom to show the "footprint" of the needle
    offset = Z_log.min() - (Z_log.max() - Z_log.min()) * 0.1
    ax.contourf(M_grid, L_grid, Z_log, zdir='z', offset=offset, cmap='magma', alpha=0.6)

    # Labels and Styling
    ax.set_title(f"The Needle Geometry\n(Annealed Scan @ {zoom:.1e})", color='white', fontsize=14)
    ax.set_xlabel(r'$\Delta m$', color='white')
    ax.set_ylabel(r'$\Delta \lambda$', color='white')
    ax.set_zlabel(r'Log Stiffness', color='white')
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    
    # Remove pane backgrounds for that "void" look
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(color='#333333', linestyle='--')

    # Force sci notation
    ax.ticklabel_format(style='sci', scilimits=(0,0), axis='both')
    
    # View angle looking down into the puncture
    ax.view_init(elev=45, azim=45)

    cbar = plt.colorbar(surf, shrink=0.5, aspect=10)
    cbar.set_label("Log Stiffness (Frustration)", color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.savefig(filename, dpi=200)
    print(f"[+] Saved render to {filename}")
    plt.close()

# ============================================================
# 4. EXECUTION
# ============================================================

if __name__ == "__main__":
    PEAK_M = -3.68863054184929439e-06
    PEAK_L = -9.6673215316825175e-05
    
    # Backing out to the "Structural Layer"
    # This should be deep enough to see the spike, but shallow enough
    # that floating point math holds together.
    RENDER_ZOOM = 1.0e-11

    render_needle(PEAK_M, PEAK_L, RENDER_ZOOM, res=200, filename="vacuum_needle_geometry.png")