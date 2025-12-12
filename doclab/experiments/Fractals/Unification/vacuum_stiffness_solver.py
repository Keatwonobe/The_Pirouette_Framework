import numpy as np
from numba import njit, prange
import time
import math

# ============================================================
# 0. HIGH-PRECISION ND ARITHMETIC (copied from Wada solver)
# ============================================================

SPLIT = 134217729.0  # 2^27 + 1

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
    """
    Translate an N-component expansion by a scalar offset.
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
# 1. VACUUM FORCE LAW (scalar version of get_force_vectorized)
# ============================================================

TWIST = 3.8

@njit(fastmath=True)
def get_force_scalar(m, lam):
    """
    Scalar version of the unified field law from get_force_vectorized.
    Returns (Fm, Flam) at a single (m, λ).
    """
    # Teal component
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red component
    F_red_m = -(m - 0.0)
    p_violation = TWIST * math.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold proto-component (sum + F^1.5 scaling)
    sum_m   = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    magnitude = math.sqrt(sum_m * sum_m + sum_lam * sum_lam)
    scaling_factor = math.sqrt(magnitude)  # |F|^{1/2}

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
# 2. STIFFNESS FIELD: G = J^T J, λ_max(G) -> "Mass"
# ============================================================

@njit(fastmath=True)
def get_stiffness_scalar(m, lam, eps=1e-4):
    """
    Compute sqrt(λ_max(G)) at a single (m, λ),
    using the same finite-difference Jacobian as in the grid version.
    """
    Fm,  Fl  = get_force_scalar(m,        lam)
    Fm_m, Fl_m = get_force_scalar(m + eps, lam)
    Fm_l, Fl_l = get_force_scalar(m,        lam + eps)

    dFx_dm = (Fm_m - Fm) / eps
    dFx_dl = (Fm_l - Fm) / eps
    dFy_dm = (Fl_m - Fl) / eps
    dFy_dl = (Fl_l - Fl) / eps

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

    # This matches the grid code's "Mass = sqrt(L1)"
    return math.sqrt(L1)

@njit(fastmath=True)
def get_stiffness_dd(m_dd, l_dd):
    """
    Double-double entry point: collapse (hi,lo) into one scalar,
    call the stiffness kernel.
    """
    m = m_dd[0] + m_dd[1]
    lam = l_dd[0] + l_dd[1]
    return get_stiffness_scalar(m, lam)

# ============================================================
# 3. DRIFT + SPAN ESTIMATOR FOR THE PEAK (not Wada boundaries)
# ============================================================

@njit(parallel=True, fastmath=True)
def get_drift_and_span_vacuum(res, zoom, center_x_nd, center_y_nd):
    """
    Sample the stiffness field on a res×res grid around the current
    center and zoom, then:
      - pick the top percentile of stiffness values,
      - compute their centroid (drift),
      - compute their span (for zoom adjustment).
    """
    img_cx = (res - 1) * 0.5
    img_cy = (res - 1) * 0.5
    scale = (2.0 * zoom) / res

    s_map = np.empty((res, res), dtype=np.float64)

    for y in prange(res):
        offset_y = (y - img_cy) * scale
        abs_y_nd = nd_translate(center_y_nd, offset_y)
        l_dd = abs_y_nd[:2]

        for x in range(res):
            offset_x = (x - img_cx) * scale
            abs_x_nd = nd_translate(center_x_nd, offset_x)
            m_dd = abs_x_nd[:2]

            s_map[y, x] = get_stiffness_dd(m_dd, l_dd)

    # Global min/max to set a high-stiffness threshold
    s_min = s_map.min()
    s_max = s_map.max()
    if not np.isfinite(s_min) or not np.isfinite(s_max):
        return 0.0, 0.0, 0.0, 0

    # Take the top ~20% of values as the "structure"
    threshold = s_min + 0.8 * (s_max - s_min)

    # Build mask
    count = 0
    sum_x = 0.0
    sum_y = 0.0
    min_px = res
    min_py = res
    max_px = -1
    max_py = -1

    for y in range(res):
        for x in range(res):
            if s_map[y, x] >= threshold:
                count += 1
                sum_x += x
                sum_y += y
                if x < min_px: min_px = x
                if x > max_px: max_px = x
                if y < min_py: min_py = y
                if y > max_py: max_py = y

    if count == 0:
        return 0.0, 0.0, 0.0, 0

    avg_px = sum_x / count
    avg_py = sum_y / count

    drift_x = (avg_px - img_cx) * scale
    drift_y = (avg_py - img_cy) * scale

    span_px = max(max_px - min_px, max_py - min_py)
    structure_span = span_px * scale
    if structure_span == 0.0:
        structure_span = 1e-12

    return drift_x, drift_y, structure_span, count

# ============================================================
# 4. SEEKER: ZOOM TOWARD THE STIFFNESS PEAK
# ============================================================

@njit
def seek_stiffness_peak(start_zoom, start_cx, start_cy,
                        N_parts, res_low, max_iterations,
                        safety_margin):
    curr_cx_nd = np.zeros(N_parts, dtype=np.float64)
    curr_cy_nd = np.zeros(N_parts, dtype=np.float64)
    curr_cx_nd[0] = start_cx
    curr_cy_nd[0] = start_cy

    curr_zoom = start_zoom

    # History of (zoom, cx_nd, cy_nd)
    zoom_history_zoom = [start_zoom]
    zoom_history_cx = [curr_cx_nd.copy()]
    zoom_history_cy = [curr_cy_nd.copy()]

    for i in range(max_iterations):
        drift_x, drift_y, span, count = get_drift_and_span_vacuum(
            res_low, curr_zoom, curr_cx_nd, curr_cy_nd
        )

        if count == 0:
            # Lost the structure; stop here
            break

        zoom_history_zoom.append(curr_zoom)
        zoom_history_cx.append(curr_cx_nd.copy())
        zoom_history_cy.append(curr_cy_nd.copy())

        curr_cx_nd = nd_translate(curr_cx_nd, drift_x)
        curr_cy_nd = nd_translate(curr_cy_nd, drift_y)

        # --- ZOOM STRATEGY (similar logic as Wada solver) ---
        target_from_span = span * 0.6
        force_min_decay = curr_zoom * 0.8
        force_max_decay = curr_zoom * 0.01

        if target_from_span > force_min_decay:
            curr_zoom = force_min_decay
        elif target_from_span < force_max_decay:
            curr_zoom = force_max_decay
        else:
            curr_zoom = target_from_span

        if curr_zoom < 1e-60:
            break

    # Backtrack to a safe point
    hist_len = len(zoom_history_zoom)
    if hist_len <= safety_margin:
        idx = hist_len - 1
    else:
        idx = hist_len - 1 - safety_margin

    final_zoom = zoom_history_zoom[idx]
    final_cx_nd = zoom_history_cx[idx]
    final_cy_nd = zoom_history_cy[idx]

    return final_zoom, final_cx_nd, final_cy_nd

# ============================================================
# 5. OPTIONAL: HIGH-RES TILE RENDERER AROUND THE PEAK
# ============================================================

def render_stiffness_tile(width, height, zoom, cx_nd, cy_nd,
                          filename="vacuum_peak_tile.png"):
    import matplotlib.pyplot as plt

    img_cx = (width - 1) * 0.5
    img_cy = (height - 1) * 0.5
    scale = (2.0 * zoom) / width

    field = np.zeros((height, width), dtype=np.float64)

    for y in range(height):
        offset_y = (y - img_cy) * scale
        abs_y_nd = nd_translate(cy_nd, offset_y)
        l_dd = abs_y_nd[:2]

        for x in range(width):
            offset_x = (x - img_cx) * scale
            abs_x_nd = nd_translate(cx_nd, offset_x)
            m_dd = abs_x_nd[:2]
            field[y, x] = get_stiffness_dd(m_dd, l_dd)

    plt.figure(figsize=(8, 8))
    plt.imshow(field, origin='lower', cmap='magma',
               extent=[-zoom, zoom, -zoom, zoom])
    plt.colorbar(label="sqrt(λ_max(G)) (stiffness)")
    plt.title(f"Vacuum Stiffness Near Peak (zoom={zoom:.2e})")
    plt.xlabel("Δm around center")
    plt.ylabel("Δλ around center")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# ============================================================
# 6. MAIN: FIND THE "INFINITE" POINT IN THE MIDDLE
# ============================================================

if __name__ == "__main__":
    # Solver parameters – tweak as needed
    N_PARTS = 4
    RES_LOW = 600       # coarse search grid (like your geodesic map)
    MAX_ITER = 200
    START_ZOOM = 3.0    # initial window radius
    START_CX = 0.0      # guess: center of the buckle in m
    START_CY = 0.0      # guess: center of the buckle in λ
    SAFETY_MARGIN = 5

    print("[-] Seeking stiffness peak in the vacuum surface...")
    t0 = time.time()
    peak_zoom, peak_cx_nd, peak_cy_nd = seek_stiffness_peak(
        START_ZOOM, START_CX, START_CY,
        N_PARTS, RES_LOW, MAX_ITER, SAFETY_MARGIN
    )
    dt = time.time() - t0

    cx_real = peak_cx_nd[0] + peak_cx_nd[1]
    cy_real = peak_cy_nd[0] + peak_cy_nd[1]
    s_peak = get_stiffness_dd(peak_cx_nd[:2], peak_cy_nd[:2])

    print(f"[+] Search done in {dt:.2f}s")
    print(f"    Peak approx center: m = {cx_real:.18g}, λ = {cy_real:.18g}")
    print(f"    Peak zoom radius:   {peak_zoom:.3e}")
    print(f"    Stiffness at peak:  {s_peak:.6e}")

    # Optional: render a detailed tile around the found peak
    render_stiffness_tile(
        width=2000,
        height=2000,
        zoom=peak_zoom,
        cx_nd=peak_cx_nd,
        cy_nd=peak_cy_nd,
        filename="vacuum_peak_tile.png",
    )
    print("[+] Saved local stiffness tile around the peak to vacuum_peak_tile.png")
