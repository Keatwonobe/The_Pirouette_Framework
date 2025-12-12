import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# =========================================================
#  PIRouette π_eff Experiment
#
#  1. Compute a helicity-style grid on (m, λ).
#  2. Threshold to get a "proton basin" mask.
#  3. Downsample to multiple resolutions and measure
#     π_eff(scale) = C_eff / D_eff.
# =========================================================

# ---------- Dynamics parameters (match your manifold) ----------
TWIST = 3.8        # or 2.83814, use the proton-tuned twist you prefer
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 150
EPSILON = 1e-5
ZOOM = 50000000

# Viewport
M_MIN, M_MAX = -ZOOM, ZOOM
L_MIN, L_MAX = -ZOOM, ZOOM
RES_BASE = 20000      # high-res grid for the initial basin

# Escape / decorrelation limits
R_ESCAPE = 50.0
HELICITY_STOP = np.pi * 0.95


# ---------- Force law (scalar) ----------
def get_force(m, lam):
    """
    Same structure as your helicity scanner / electron field.
    """
    # Teal
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red with parity/twist violation
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold nonlinear
    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    # Angular weights
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


def normalize_angle_diff(delta):
    return np.arctan2(np.sin(delta), np.cos(delta))


# ---------- Helicity grid generation ----------
def measure_helicity(m0, l0):
    """
    Run a real + shadow trajectory from (m0, l0) and
    return log(max angular decorrelation).
    """
    m1, l1 = m0, l0
    pm1, pl1 = 0.0, 0.0

    m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm2, pl2 = 0.0, 0.0

    max_diff_angle = 0.0

    for _ in range(MAX_STEPS):
        # Real
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

        # Shadow
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

        # Helicity
        ang1 = np.arctan2(l1, m1)
        ang2 = np.arctan2(l2, m2)
        diff = normalize_angle_diff(ang1 - ang2)
        adiff = abs(diff)
        if adiff > max_diff_angle:
            max_diff_angle = adiff

        # Stops
        if max_diff_angle > HELICITY_STOP:
            break
        if (m1**2 + l1**2) > R_ESCAPE:
            break

    return np.log(max_diff_angle + EPSILON)


def compute_helicity_grid(res=RES_BASE):
    m_vals = np.linspace(M_MIN, M_MAX, res)
    l_vals = np.linspace(L_MIN, L_MAX, res)
    H = np.zeros((res, res), dtype=float)

    for i, lam in enumerate(l_vals):
        print(f"[GRID] row {i+1}/{res} ({100.0*(i+1)/res:.1f}%)")
        for j, m in enumerate(m_vals):
            H[i, j] = measure_helicity(m, lam)

    return H, m_vals, l_vals


# ---------- Basin identification ----------
def make_basin_mask(H, fractile=0.25):
    """
    Turn helicity values into a boolean "proton basin" mask
    by thresholding at a chosen quantile.
    Adjust fractile up/down to grow/shrink the basin.
    """
    # For many of your scans, small helicity = stable core;
    # adjust sign if your convention is inverted.
    thresh = np.quantile(H, fractile)
    mask = H <= thresh
    return mask, thresh


def extract_boundary(mask):
    """
    Return indices of boundary pixels in a boolean mask.
    4-neighbor connectivity.
    """
    ny, nx = mask.shape
    boundary = []

    for i in range(1, ny - 1):
        for j in range(1, nx - 1):
            if not mask[i, j]:
                continue
            # if any neighbor is outside, it's boundary
            if (not mask[i+1, j] or not mask[i-1, j] or
                not mask[i, j+1] or not mask[i, j-1]):
                boundary.append((i, j))

    return np.array(boundary, dtype=int)


# ---------- Downsampling ----------
def downsample_mask(mask, block):
    """
    Average over block x block tiles and threshold at 0.5.
    """
    ny, nx = mask.shape
    by = ny // block
    bx = nx // block

    trimmed = mask[:by*block, :bx*block].astype(float)
    reshaped = trimmed.reshape(by, block, bx, block)
    block_avg = reshaped.mean(axis=(1, 3))
    coarse = block_avg >= 0.5
    return coarse


# ---------- π_eff computation ----------
def compute_pi_eff(mask, m_vals, l_vals):
    """
    Given a boolean interior mask at some resolution and
    the coordinate arrays for its axes, compute:
    - C_eff via boundary length
    - D_eff via 2*mean radius
    """
    # pixel sizes
    dy = (l_vals[-1] - l_vals[0]) / (len(l_vals) - 1)
    dx = (m_vals[-1] - m_vals[0]) / (len(m_vals) - 1)
    delta = np.sqrt(dx*dx + dy*dy)  # effective step for rough C

    # interior points & centroid
    ys, xs = np.where(mask)
    if ys.size == 0:
        return np.nan, np.nan, np.nan

    y_coords = l_vals[ys]
    x_coords = m_vals[xs]

    x_c = x_coords.mean()
    y_c = y_coords.mean()

    # boundary
    boundary_idx = extract_boundary(mask)
    if boundary_idx.size == 0:
        return np.nan, np.nan, np.nan

    by = l_vals[boundary_idx[:, 0]]
    bx = m_vals[boundary_idx[:, 1]]

    r = np.sqrt((bx - x_c)**2 + (by - y_c)**2)
    r_mean = r.mean()
    D_eff = 2.0 * r_mean

    C_eff = len(boundary_idx) * delta

    pi_eff = C_eff / D_eff if D_eff > 0 else np.nan
    return pi_eff, C_eff, D_eff


# ---------- Main experiment ----------
def run_pi_eff_experiment():
    # Step 1: helicity grid
    H, m_vals, l_vals = compute_helicity_grid(RES_BASE)

    # Step 2: identify basin
    basin_mask, thresh = make_basin_mask(H, fractile=0.25)
    print(f"[BASIN] threshold = {thresh:.4g}")

    # Quick visualization of the basin
    plt.figure(figsize=(6, 6))
    plt.imshow(basin_mask, origin="lower",
               extent=[M_MIN, M_MAX, L_MIN, L_MAX],
               cmap="Greys_r")
    plt.title("Proton Basin Mask (high-res)")
    plt.xlabel("Mass field m")
    plt.ylabel("Coupling field λ")
    plt.tight_layout()
    plt.savefig("proton_basin_mask.png", dpi=200)
    plt.close()

    # Step 3: π_eff vs scale
    scales = [1, 2, 4, 8, 16, 32]  # block sizes
    pi_values = []

    for s in scales:
        print(f"[SCALE] block = {s}")
        if s == 1:
            coarse_mask = basin_mask
            m_coarse = m_vals
            l_coarse = l_vals
        else:
            coarse_mask = downsample_mask(basin_mask, s)
            # rebuild coarse coordinate arrays
            ny, nx = coarse_mask.shape
            m_coarse = np.linspace(M_MIN, M_MAX, nx)
            l_coarse = np.linspace(L_MIN, L_MAX, ny)

        pi_eff, C_eff, D_eff = compute_pi_eff(coarse_mask, m_coarse, l_coarse)
        pi_values.append(pi_eff)
        print(f"  π_eff = {pi_eff:.8f}   C={C_eff:.5f}, D={D_eff:.5f}")

    # Plot π_eff(scale)
    plt.figure(figsize=(7, 4))
    plt.plot(scales, pi_values, "o-", label=r"$\pi_{\rm eff}$")
    plt.axhline(np.pi, color="k", linestyle="--", label="π")
    plt.xscale("log", base=2)
    plt.xlabel("Downsampling block size (log₂ scale)")
    plt.ylabel(r"$\pi_{\rm eff} = C_{\rm eff} / D_{\rm eff}$")
    plt.title(r"Resolution Dependence of $\pi_{\rm eff}$ on the Proton Basin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("pi_eff_vs_scale.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    run_pi_eff_experiment()
