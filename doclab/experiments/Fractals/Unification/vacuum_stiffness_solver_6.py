import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math
import time

# ============================================================
# 0. HIGH-PRECISION ND ARITHMETIC (same family as solver)
# ============================================================

SPLIT = 134217729.0  # 2^27 + 1

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
    Translate a high-precision coordinate by a scalar offset.
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
# 1. FORCE LAW WITH EXPLICIT TWIST PARAMETER
#    (mechanically linkable to stiffness)
# ============================================================

@njit(fastmath=True)
def get_force_scalar_param(m, lam, twist):
    """
    Same physics as your other files, but twist is an argument.
    """
    # Teal component
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red component
    F_red_m = -(m - 0.0)
    p_violation = twist * math.sin(m * 2.5)
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
# 2. ROBUST STIFFNESS KERNEL (central difference)
# ============================================================

@njit(fastmath=True)
def stiffness_at_point(m, lam, twist, eps):
    """
    sqrt(λ_max(G)) using central differences with a fixed eps.
    """
    # ∂F/∂m
    Fm_plus_m, Fl_plus_m     = get_force_scalar_param(m + eps, lam, twist)
    Fm_minus_m, Fl_minus_m   = get_force_scalar_param(m - eps, lam, twist)
    dFx_dm = (Fm_plus_m - Fm_minus_m) / (2.0 * eps)
    dFy_dm = (Fl_plus_m - Fl_minus_m) / (2.0 * eps)

    # ∂F/∂λ
    Fm_plus_l, Fl_plus_l     = get_force_scalar_param(m, lam + eps, twist)
    Fm_minus_l, Fl_minus_l   = get_force_scalar_param(m, lam - eps, twist)
    dFx_dl = (Fm_plus_l - Fm_minus_l) / (2.0 * eps)
    dFy_dl = (Fl_plus_l - Fl_minus_l) / (2.0 * eps)

    # Metric tensor G = J^T J
    g11 = dFx_dm * dFx_dm + dFy_dm * dFy_dm
    g12 = dFx_dm * dFx_dl + dFy_dm * dFy_dl
    g22 = dFx_dl * dFx_dl + dFy_dl * dFy_dl

    T = g11 + g22
    D = g11 * g22 - g12 * g12
    disc = T * T * 0.25 - D
    if disc < 0.0:
        disc = 0.0
    L1 = 0.5 * T + math.sqrt(disc)
    if L1 < 0.0:
        L1 = 0.0

    return math.sqrt(L1)

# ============================================================
# 3. ND SCAN + TWIST WIGGLE
# ============================================================

@njit(parallel=True)
def scan_stiffness_and_wiggle(center_m_nd, center_l_nd,
                              zoom, res,
                              twist, d_twist, eps):
    """
    Returns:
      base   : stiffness at twist
      dS_dTw : (S(twist + d_twist) - S(twist - d_twist)) / (2 d_twist)
    """
    base  = np.zeros((res, res), dtype=np.float64)
    dSdTw = np.zeros((res, res), dtype=np.float64)

    c_idx = (res - 1) * 0.5
    scale = (2.0 * zoom) / res

    for j in prange(res):
        off_l = (j - c_idx) * scale
        l_nd  = nd_translate(center_l_nd, off_l)
        lam   = l_nd[0] + l_nd[1]

        for i in range(res):
            off_m = (i - c_idx) * scale
            m_nd  = nd_translate(center_m_nd, off_m)
            m     = m_nd[0] + m_nd[1]

            # Base stiffness
            s0 = stiffness_at_point(m, lam, twist, eps)
            base[j, i] = s0

            # Wiggle in twist parameter (tag the needle)
            sp = stiffness_at_point(m, lam, twist + d_twist, eps)
            sm = stiffness_at_point(m, lam, twist - d_twist, eps)
            dSdTw[j, i] = (sp - sm) / (2.0 * d_twist)

    return base, dSdTw

# ============================================================
# 4. HIGH-LEVEL WRAPPER + PLOT
# ============================================================

def map_wiggle(
    cx_val,
    cy_val,
    zoom,
    twist=3.8,
    d_twist=1e-3,
    res=200,
    eps=1e-8,
    filename="vacuum_wiggle_map.png",
):
    """
    Wiggle the manifold in TWIST at a given zoom,
    and visualize both the stiffness and its response.
    """
    print("[-] Wiggle scan starting...")
    print(f"    center m,λ = ({cx_val:.18g}, {cy_val:.18g})")
    print(f"    zoom       = {zoom:.3e}")
    print(f"    twist      = {twist:.6f} ± {d_twist:.2e}")
    print(f"    eps (∂F)   = {eps:.1e}")
    print(f"    res        = {res}")

    center_m_nd = np.zeros(2, dtype=np.float64)
    center_l_nd = np.zeros(2, dtype=np.float64)
    center_m_nd[0] = cx_val
    center_l_nd[0] = cy_val

    t0 = time.time()
    base, dSdTw = scan_stiffness_and_wiggle(center_m_nd, center_l_nd,
                                            zoom, res,
                                            twist, d_twist, eps)
    dt = time.time() - t0
    print(f"[+] Wiggle scan done in {dt:.2f}s")

    # Normalise the wiggle map for plotting (sign-sensitive)
    max_abs = np.max(np.abs(dSdTw))
    if max_abs == 0.0:
        max_abs = 1.0
    norm_dSdTw = dSdTw / max_abs

    # Coordinates (for axis labels)
    vals = np.linspace(-zoom, zoom, res)
    M_grid, L_grid = np.meshgrid(vals, vals)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    im0 = axes[0].imshow(
        base,
        origin="lower",
        extent=[-zoom, zoom, -zoom, zoom],
        cmap="magma",
        aspect="equal",
    )
    axes[0].set_title("Base stiffness $\\sqrt{\\lambda_{max}(G)}$")
    axes[0].set_xlabel("$\\Delta m$ around center")
    axes[0].set_ylabel("$\\Delta \\lambda$ around center")
    fig.colorbar(im0, ax=axes[0], shrink=0.8)

    im1 = axes[1].imshow(
        norm_dSdTw,
        origin="lower",
        extent=[-zoom, zoom, -zoom, zoom],
        cmap="seismic",
        vmin=-1.0,
        vmax=1.0,
        aspect="equal",
    )
    axes[1].set_title("Sensitivity $\\partial S / \\partial \\mathrm{TWIST}$ (tag map)")
    axes[1].set_xlabel("$\\Delta m$")
    axes[1].set_ylabel("$\\Delta \\lambda$")
    fig.colorbar(im1, ax=axes[1], shrink=0.8)

    fig.suptitle(f"Vacuum Wiggle Map at zoom={zoom:.1e}", fontsize=14)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"[+] Saved wiggle map to {filename}")

# ============================================================
# 5. EXECUTION
# ============================================================

if __name__ == "__main__":
    # Use the peak you already located with the solver
    PEAK_M = -3.68863054184929439e-06
    PEAK_L = -9.6673215316825175e-05

    # Pick a zoom where float64 still sees curvature
    ZOOM = 1.0e-11   # or 2e-14 if you want the clean tip

    map_wiggle(
        cx_val=PEAK_M,
        cy_val=PEAK_L,
        zoom=ZOOM,
        twist=3.8,
        d_twist=1e-3,
        res=200,
        eps=1e-8,
        filename="vacuum_wiggle_map.png",
    )
