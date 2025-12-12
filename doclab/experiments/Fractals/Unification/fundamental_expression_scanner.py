import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# FUNDAMENTAL EXPRESSION SCANNER ON THE PIRouette MANIFOLD
#
# Classifies each (m, λ) point by the long-term behavior
# of its trajectory under the standard Pirouette forces.
#
# Expression codes:
#   0 = VOID / trivial
#   1 = CORE_KNOT        (particle-like, tightly bound)
#   2 = HALO_ORBIT       (bounded orbital / field-like)
#   3 = RADIATIVE_RUNAWAY
#   4 = CHAOTIC_CREVASSE (high helicity chaos)
#   5 = MIXED_SHELL      (intermediate or ambiguous)
# --------------------------------------------------

# ---- Constants (aligned with your existing scripts) ----
TWIST = 2.83814      # electron-tuned twist   electron_lines.py
GAMMA = 0.5          # damping / drag         helicity scanner
DT    = 0.015
MAX_STEPS = 2000

EPSILON = 1e-5       # shadow separation
R_ESCAPE = 50.0      # hard escape radius for RUNAWAY

# Thresholds for classification (tune these!)
R_CORE   = 0.5       # radius for core-knot region
R_ORBIT  = 3.0       # radius for halo / orbital band
HELICITY_CHAOS = 0.9 * np.pi  # near-π divergence
MIN_TURNS_ORBIT = 1.5          # min total turns to be "orbital"

# ---- Scan window ----
M_MIN, M_MAX = -6.0,  6.0
L_MIN, L_MAX = -6.0,  6.0
RES = 300             # 300x300 to start; increase once it behaves

# --------------------------------------------------
# Utility
# --------------------------------------------------

def normalize_angle_diff(delta):
    """Wrap angle difference to [-pi, pi]."""
    return np.arctan2(np.sin(delta), np.cos(delta))

def get_force(m, lam):
    """
    Scalar version of your Pirouette force law,
    structurally matched to get_force_vectorized in electron_lines.py.
    """
    # Teal contribution
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red contribution with parity/twist violation
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold (nonlinear) contribution
    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    # Angular weighting (same geometry as electron field)
    angle_deg = np.degrees(np.arctan2(lam, m)) % 360.0

    diff_g = np.minimum(np.abs(angle_deg - 30.0), 360.0 - np.abs(angle_deg - 30.0))
    w_gold = np.exp(-(diff_g / 80.0)**2)

    diff_t = np.minimum(np.abs(angle_deg - 150.0), 360.0 - np.abs(angle_deg - 150.0))
    w_teal = np.exp(-(diff_t / 80.0)**2)

    diff_r = np.minimum(np.abs(angle_deg - 270.0), 360.0 - np.abs(angle_deg - 270.0))
    w_red  = np.exp(-(diff_r / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6

    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam, nw_red


# --------------------------------------------------
# Trajectory analysis for one initial condition
# --------------------------------------------------

def classify_point(m0, l0):
    """
    Integrate the trajectory and its shadow from (m0, l0),
    compute invariants, and return an expression code.
    """

    # Main trajectory
    m1, l1 = m0, l0
    pm1, pl1 = 0.0, 0.0

    # Shadow trajectory (for helicity)
    m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm2, pl2 = 0.0, 0.0

    # Invariants
    r_min = np.inf
    r_max = 0.0
    total_rot = 0.0
    max_helicity = 0.0

    ang_prev = np.arctan2(l1, m1)

    escaped = False
    t_escaped = MAX_STEPS

    for t in range(MAX_STEPS):

        # --- Main trajectory update (leapfrog-ish with drag) ---
        Fm1, Flam1, w_red1 = get_force(m1, l1)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
        m1 += DT * pm1
        l1 += DT * pl1
        Fm1, Flam1, w_red1 = get_force(m1, l1)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1

        # --- Shadow trajectory update ---
        Fm2, Flam2, w_red2 = get_force(m2, l2)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
        m2 += DT * pm2
        l2 += DT * pl2
        Fm2, Flam2, w_red2 = get_force(m2, l2)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2

        # --- Radius invariants ---
        r = np.sqrt(m1**2 + l1**2)
        r_min = min(r_min, r)
        r_max = max(r_max, r)

        # --- Rotation number (accumulated angle) ---
        ang = np.arctan2(l1, m1)
        d_ang = normalize_angle_diff(ang - ang_prev)
        total_rot += d_ang
        ang_prev = ang

        # --- Helicity divergence (shadow vs main angle) ---
        ang2 = np.arctan2(l2, m2)
        d_h = normalize_angle_diff(ang - ang2)
        abs_h = abs(d_h)
        if abs_h > max_helicity:
            max_helicity = abs_h

        # --- Escape detection ---
        if not escaped and r > R_ESCAPE:
            escaped = True
            t_escaped = t
            break

    # Now classify based on invariants
    total_turns = abs(total_rot) / (2.0 * np.pi)
    bounded = (r_max < R_ESCAPE)  # never left the box

    # 3: RUNAWAY (quick escape to large radius)
    if escaped and t_escaped < MAX_STEPS * 0.5:
        return 3

    # 4: CHAOTIC CREVASSE (high helicity but not necessarily escaped)
    if max_helicity > HELICITY_CHAOS and bounded:
        return 4

    # 1: CORE-KNOT (stays near origin, low turns)
    if r_max < R_CORE and total_turns < 0.5:
        return 1

    # 2: HALO-ORBIT (bounded radius, multiple turns)
    if bounded and (R_CORE <= r_min < R_ORBIT) and (total_turns > MIN_TURNS_ORBIT):
        return 2

    # 0: VOID / trivial (very small movement or quick damping)
    if r_max < 0.1:
        return 0

    # 5: MIXED SHELL (everything else ambiguous / transitional)
    return 5


# --------------------------------------------------
# Grid scan and visualization
# --------------------------------------------------

def run_expression_scan():
    m_vals = np.linspace(M_MIN, M_MAX, RES)
    l_vals = np.linspace(L_MIN, L_MAX, RES)

    expression_map = np.zeros((RES, RES), dtype=int)

    for i, lam in enumerate(l_vals):
        print(f"Row {i+1}/{RES} ({100.0*(i+1)/RES:.1f}%)")
        for j, m in enumerate(m_vals):
            expression_map[i, j] = classify_point(m, lam)

    # --- Plotting with a discrete colormap ---
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="black")
    ax.set_facecolor("black")

    # Map expression codes to colors
    from matplotlib.colors import ListedColormap

    # colors: VOID, CORE, HALO, RUNAWAY, CHAOS, MIXED
    colors = [
        "#000000",  # 0 void - black
        "#00ffcc",  # 1 core knot - teal
        "#ffd700",  # 2 halo orbit - gold
        "#ff4500",  # 3 runaway - orange/red
        "#9400d3",  # 4 chaotic - violet
        "#808080",  # 5 mixed shell - gray
    ]
    cmap = ListedColormap(colors)

    im = ax.imshow(
        expression_map,
        origin="lower",
        extent=[M_MIN, M_MAX, L_MIN, L_MAX],
        cmap=cmap,
        interpolation="nearest",
    )

    ax.set_title("Fundamental Expression Map on the Pirouette Manifold", color="white", fontsize=16)
    ax.set_xlabel("Mass Field (m)", color="white")
    ax.set_ylabel("Coupling Field (λ)", color="white")
    ax.tick_params(colors="white")

    # Custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=colors[0], label="0: Void / trivial"),
        Patch(facecolor=colors[1], label="1: Core Knot (particle-like)"),
        Patch(facecolor=colors[2], label="2: Halo Orbit (field-like)"),
        Patch(facecolor=colors[3], label="3: Radiative Runaway"),
        Patch(facecolor=colors[4], label="4: Chaotic Crevasse"),
        Patch(facecolor=colors[5], label="5: Mixed Shell"),
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper right",
        facecolor="black",
        edgecolor="white",
        labelcolor="white",
    )

    plt.tight_layout()
    plt.savefig("fundamental_expression_map.png", dpi=200, facecolor="black")
    plt.show()


if __name__ == "__main__":
    run_expression_scan()
