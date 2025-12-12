# twist_detector_1-2-8.py
#
# Scan TWIST and find where the time-averaged sector weights
# on the electron shell ring best match the 1:2:8 ratio
#   (Gold : Teal : Red) = (1 : 2 : 8)
#
# Uses the same dynamics as the previous time-average script.

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Parameters
# ----------------------------
R0        = 2.2      # ring radius
N_THETA   = 360      # number of starting angles on ring
DT        = 0.02
N_STEPS   = 400
R_ESCAPE  = 10.0

# TWIST scan range
TWIST_MIN = 0
TWIST_MAX = 100
TWIST_STEP = 0.5

TWIST_VALUES = np.arange(TWIST_MIN, TWIST_MAX + 1e-9, TWIST_STEP)

# Target 1:2:8 fractions on the simplex
fG_target = 1.0 / 11.0
fT_target = 2.0 / 11.0
fR_target = 8.0 / 11.0
TARGET = np.array([fG_target, fT_target, fR_target])


# ----------------------------
# Sector geometry
# ----------------------------
def sector_weights_from_angle(angle_deg: float):
    """Normalized (w_gold, w_teal, w_red) from polar angle in degrees."""
    angle = angle_deg % 360.0

    diff_g = np.abs(angle - 30.0)
    diff_g = np.minimum(diff_g, 360.0 - diff_g)
    w_gold = np.exp(-(diff_g / 80.0) ** 2)

    diff_t = np.abs(angle - 150.0)
    diff_t = np.minimum(diff_t, 360.0 - diff_t)
    w_teal = np.exp(-(diff_t / 80.0) ** 2)

    diff_r = np.abs(angle - 270.0)
    diff_r = np.minimum(diff_r, 360.0 - diff_r)
    w_red = np.exp(-(diff_r / 80.0) ** 2)

    tot = w_gold + w_teal + w_red + 1e-12
    return w_gold / tot, w_teal / tot, w_red / tot


def vacuum_force_with_twist(m: float, lam: float, twist: float):
    """Vacuum force field with explicit TWIST."""
    # Teal (EM-like)
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red (weak-like) with CP twist
    F_red_m    = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5)
    F_red_lam  = -(lam + 1.0) + p_violation

    # Gold (strong-like)
    sum_m   = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m * scale
    F_gold_lam = sum_lam * scale

    # Angular mixing
    angle = np.degrees(np.arctan2(lam, m)) % 360.0
    w_gold, w_teal, w_red = sector_weights_from_angle(angle)

    Fm   = w_teal * F_teal_m   + w_red * F_red_m   + w_gold * F_gold_m
    Flam = w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam
    return Fm, Flam


# ----------------------------
# Time-averaged sectors
# ----------------------------
def time_averaged_sectors_for_trajectory(m0: float, lam0: float, twist: float):
    """Return (⟨Gold⟩, ⟨Teal⟩, ⟨Red⟩) for one trajectory."""
    m = float(m0)
    lam = float(lam0)

    sum_g = 0.0
    sum_t = 0.0
    sum_r = 0.0
    steps = 0

    for _ in range(N_STEPS):
        angle = np.degrees(np.arctan2(lam, m))
        w_g, w_t, w_r = sector_weights_from_angle(angle)

        sum_g += w_g
        sum_t += w_t
        sum_r += w_r
        steps += 1

        Fm, Flam = vacuum_force_with_twist(m, lam, twist)
        m   += DT * Fm
        lam += DT * Flam

        if m * m + lam * lam > R_ESCAPE * R_ESCAPE:
            break

    if steps == 0:
        return 0.0, 0.0, 0.0

    return sum_g / steps, sum_t / steps, sum_r / steps


def time_averaged_sectors_on_ring(twist: float):
    """Average ⟨Gold, Teal, Red⟩ over all starting angles on the ring."""
    theta = np.linspace(0.0, 2.0 * np.pi, N_THETA, endpoint=False)

    vals = []
    for ang in theta:
        m0   = R0 * np.cos(ang)
        lam0 = R0 * np.sin(ang)
        vals.append(time_averaged_sectors_for_trajectory(m0, lam0, twist))

    vals = np.array(vals)
    return vals.mean(axis=0)  # (mean_g, mean_t, mean_r)


# ----------------------------
# Main scan
# ----------------------------
def run_128_scan():
    mean_G = []
    mean_T = []
    mean_R = []
    errors = []

    print("\n[Δ] 1:2:8 finder on electron shell ring")
    print("Target fractions: G=%.8e, T=%.8e, R=%.8e"
          % (fG_target, fT_target, fR_target))
    # Adjusted header for new formatting
    print("\nTWIST      <G>           <T>           <R>           error(1:2:8)")

    for twist in TWIST_VALUES:
        g, t, r = time_averaged_sectors_on_ring(twist)
        vec = np.array([g, t, r])
        err = np.linalg.norm(vec - TARGET)  # Euclidean distance in simplex

        mean_G.append(g)
        mean_T.append(t)
        mean_R.append(r)
        errors.append(err)

        # *** MODIFIED PRINT STATEMENT FOR SMALLER NUMBERS ***
        # TWIST: :7.5f for higher fixed precision
        # <G>, <T>, <R>: :10.4e for scientific notation with 4 significant digits
        # error: :10.6e for scientific notation with 6 significant digits
        print(f"{twist:7.5f}  {g:13.4e}  {t:13.4e}  {r:13.4e}  {err:13.6e}")

    mean_G = np.array(mean_G)
    mean_T = np.array(mean_T)
    mean_R = np.array(mean_R)
    errors = np.array(errors)

    # Find best matches
    idx_sorted = np.argsort(errors)
    print("\n[Δ] Best matches to 1:2:8 (smallest error):")
    for k in range(10):
        i = idx_sorted[k]
        # *** MODIFIED PRINT STATEMENT FOR BEST MATCHES ***
        # Increased precision for all values
        print(f"  #{k+1:2d}: TWIST={TWIST_VALUES[i]:.5f}  "
              f"<G>={mean_G[i]:.8e}  <T>={mean_T[i]:.8e}  <R>={mean_R[i]:.8e}  "
              f"err={errors[i]:.6e}")

    # ---------------- Plot fractions vs TWIST with 1:2:8 lines ----------------
    plt.figure(figsize=(10, 6), facecolor="black")
    ax = plt.gca()
    ax.set_facecolor("black")

    ax.plot(TWIST_VALUES, mean_G, label="⟨Gold⟩", linewidth=2.0)
    ax.plot(TWIST_VALUES, mean_T, label="⟨Teal⟩", linewidth=2.0, linestyle="--")
    ax.plot(TWIST_VALUES, mean_R, label="⟨Red⟩",  linewidth=2.0, linestyle=":")

    ax.axhline(fG_target, color="gray", linestyle="-.", linewidth=1.0)
    ax.axhline(fT_target, color="gray", linestyle="-.", linewidth=1.0)
    ax.axhline(fR_target, color="gray", linestyle="-.", linewidth=1.0)
    ax.text(TWIST_MIN, fG_target+0.002, "1/11", color="white")
    ax.text(TWIST_MIN, fT_target+0.002, "2/11", color="white")
    ax.text(TWIST_MIN, fR_target+0.002, "8/11", color="white")

    ax.set_xlabel("TWIST parameter", color="white")
    ax.set_ylabel("Time-averaged sector weight", color="white")
    ax.set_title("Time-Averaged Sector Weights vs TWIST\n(1:2:8 target shown)", color="white")

    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("white")
    leg = ax.legend(facecolor="black", edgecolor="white")
    for txt in leg.get_texts():
        txt.set_color("white")

    plt.tight_layout()
    plt.savefig("twist_128_fractions.png", dpi=220)

    # ---------------- Plot error vs TWIST ----------------
    plt.figure(figsize=(10, 4), facecolor="black")
    ax2 = plt.gca()
    ax2.set_facecolor("black")
    ax2.plot(TWIST_VALUES, errors, linewidth=2.0)
    ax2.set_xlabel("TWIST parameter", color="white")
    ax2.set_ylabel("‖⟨w⟩ − target(1:2:8)‖", color="white")
    ax2.set_title("Deviation from 1:2:8 Time-Average", color="white")
    ax2.tick_params(colors="white")
    for spine in ax2.spines.values():
        spine.set_color("white")
    plt.tight_layout()
    plt.savefig("twist_128_error.png", dpi=220)

    plt.show()
    
    # *** ADD RETURN STATEMENT ***
    return TWIST_VALUES, errors


# ---------------------------------------------------------
#  Parabolic bump detector on 1D scans
# ---------------------------------------------------------

def _fit_parabola_vertex(x0, f0, x1, f1, x2, f2):
    """
    Fit a parabola p(x) = ax^2 + bx + c through 3 points and
    return vertex position x*, value f*, and curvature a.
    """
    # Solve for a,b,c from three equations
    M = np.array([
        [x0**2, x0, 1.0],
        [x1**2, x1, 1.0],
        [x2**2, x2, 1.0],
    ], dtype=float)
    y = np.array([f0, f1, f2], dtype=float)
    a, b, c = np.linalg.solve(M, y)

    # Vertex of parabola
    if a == 0.0:
        # Degenerate: no curvature, just return middle point
        return x1, f1, a

    xv = -b / (2.0 * a)
    fv = a * xv**2 + b * xv + c
    return xv, fv, a


def find_parabolic_bumps(
    x_vals,
    f_vals,
    min_curvature=0.0,
    max_vertex_offset_factor=1.0,
    require_local_min=True,
):
    """
    Core bump finder on a 1D curve.

    Parameters
    ----------
    x_vals, f_vals : 1D arrays of same length
        Sampled parameter (TWIST) and corresponding scalar (error).
    min_curvature : float
        Minimum |a| for parabola vertex to count as 'interesting'.
        Think of this as 'how sharp must the bump be'.
    max_vertex_offset_factor : float
        Require vertex x* to lie within:
            [x_i - factor*dx, x_i + factor*dx]
        where x_i is the center sample and dx is the local step.
        Use 1.0 for 'within the neighboring samples'.
    require_local_min : bool
        If True, only accept a>0 (local minima). Set False if you
        also want local maxima.

    Returns
    -------
    bumps : list of dict
        Each dict has keys:
          'x_vertex', 'f_vertex', 'curvature', 'i_center'
    """
    x_vals = np.asarray(x_vals, dtype=float)
    f_vals = np.asarray(f_vals, dtype=float)

    n = len(x_vals)
    bumps = []

    for i in range(1, n - 1):
        x0, x1, x2 = x_vals[i-1], x_vals[i], x_vals[i+1]
        f0, f1, f2 = f_vals[i-1], f_vals[i], f_vals[i+1]

        xv, fv, a = _fit_parabola_vertex(x0, f0, x1, f1, x2, f2)

        if require_local_min and a <= 0.0:
            continue

        if abs(a) < min_curvature:
            continue

        # vertex should live reasonably inside the bracket
        dx = 0.5 * (x2 - x0)
        if not (x1 - max_vertex_offset_factor*dx <= xv <= x1 + max_vertex_offset_factor*dx):
            continue

        # Optional: require that fv <= f1 (strictly better than mid sample)
        if fv > f1:
            continue

        bumps.append({
            "x_vertex": float(xv),
            "f_vertex": float(fv),
            "curvature": float(a),
            "i_center": i,
        })

    return bumps


def scan_for_bumps(
    TWIST_VALUES,
    errors,
    min_curvature=1e-4,
    max_vertex_offset_factor=1.0,
    top_k=10,
):
    """
    Convenience wrapper for your TWIST scans.

    Call this AFTER you've filled TWIST_VALUES and errors.

    Prints the best bumps and returns them sorted by f_vertex (lowest first).
    """
    bumps = find_parabolic_bumps(
        TWIST_VALUES,
        errors,
        min_curvature=min_curvature,
        max_vertex_offset_factor=max_vertex_offset_factor,
        require_local_min=True,
    )

    if not bumps:
        print("[Δ] No parabolic bumps found with current thresholds.")
        return []

    # sort by how small the function value is (best match)
    bumps_sorted = sorted(bumps, key=lambda b: b["f_vertex"])

    print("\n[Δ] Parabolic bump detector results (best {}):".format(min(top_k, len(bumps_sorted))))
    for k, b in enumerate(bumps_sorted[:top_k], 1):
        print(
            f"  #{k:2d}: TWIST*={b['x_vertex']:.8f}  "
            f"f*={b['f_vertex']:.6e}  "
            f"a={b['curvature']:.3e}  "
            f"(i={b['i_center']})"
        )

    return bumps_sorted


if __name__ == "__main__":
    # 1. Run the main scan and CAPTURE the results
    X_vals, F_vals = run_128_scan()
    
    # 2. Pass the captured results to the bump detector
    scan_for_bumps(X_vals, F_vals)