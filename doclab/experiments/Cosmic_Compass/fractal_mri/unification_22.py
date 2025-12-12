import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# MASS TENSOR MAP FOR THE FRACTAL VACUUM
# --------------------------------------------------
# This script computes the full Jacobian J of your
# force field F(m, λ), constructs G = J^T J, and
# extracts:
#   m_eff  = sqrt(λ_max(G))          (scalar mass)
#   aniso  = sqrt(λ_max / λ_min)     (directional stiffness)
#
# It uses the same force law as your stiffness map
# (unification_21).  Adjust RES if needed.
# --------------------------------------------------

# Grid / physics parameters (match your other scripts)
RES   = 800
TWIST = 3.8
GAMMA = 0.11  # (unused here, but kept for context)

M_MIN, M_MAX = -3.0, 3.0
L_MIN, L_MAX = -3.0, 3.0

# Small step for numerical derivatives
EPS = 1e-3


# --------------------------------------------------
# Force field (copied from your coupling map script)
# --------------------------------------------------
def get_force_vectorized(m, lam):
    """
    Your Standard-Model-like soliton force field F(m, λ).
    Returns:
        Fm   = d(m)/dt acceleration
        Flam = d(λ)/dt acceleration
    """
    # Teal (light) component
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red (weak) component with CP-twist
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold (strong) = squeezed vector sum
    sum_m   = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude)   # F^1.5 scaling

    F_gold_m   = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor

    # Angular weights (Teal / Red / Gold sectors)
    angle = np.degrees(np.arctan2(lam, m)) % 360

    diff_g = np.abs(angle - 30.0)
    diff_g = np.minimum(diff_g, 360.0 - diff_g)
    w_gold = np.exp(-(diff_g / 80.0) ** 2)

    diff_t = np.abs(angle - 150.0)
    diff_t = np.minimum(diff_t, 360.0 - diff_t)
    w_teal = np.exp(-(diff_t / 80.0) ** 2)

    diff_r = np.abs(angle - 270.0)
    diff_r = np.minimum(diff_r, 360.0 - diff_r)
    w_red = np.exp(-(diff_r / 80.0) ** 2)

    tot = w_gold + w_teal + w_red + 1e-6
    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam


# --------------------------------------------------
# Mass tensor computation
# --------------------------------------------------
def compute_mass_tensor_map():
    print(f"Computing mass tensor on {RES}x{RES} grid...")

    # Coordinate grid
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)

    # Force at central points
    Fm, Flam = get_force_vectorized(M, L)

    # Central differences for Jacobian entries
    # Fx ≡ Fm, Fy ≡ Flam
    Fm_plus_m,  Flam_plus_m  = get_force_vectorized(M + EPS, L)
    Fm_minus_m, Flam_minus_m = get_force_vectorized(M - EPS, L)

    Fm_plus_l,  Flam_plus_l  = get_force_vectorized(M, L + EPS)
    Fm_minus_l, Flam_minus_l = get_force_vectorized(M, L - EPS)

    dFx_dm = (Fm_plus_m  - Fm_minus_m)  / (2.0 * EPS)
    dFx_dl = (Fm_plus_l  - Fm_minus_l)  / (2.0 * EPS)
    dFy_dm = (Flam_plus_m - Flam_minus_m) / (2.0 * EPS)
    dFy_dl = (Flam_plus_l - Flam_minus_l) / (2.0 * EPS)

    # Build symmetric metric G = J^T J at each point.
    # J = [[a, b],
    #      [c, d]] = [[dFx_dm, dFx_dl],
    #                 [dFy_dm, dFy_dl]]
    a = dFx_dm
    b = dFx_dl
    c = dFy_dm
    d = dFy_dl

    # Components of G = J^T J (2x2 symmetric)
    g11 = a * a + c * c
    g12 = a * b + c * d
    g22 = b * b + d * d

    # Eigenvalues of 2x2 symmetric matrix analytically:
    # λ_{1,2} = (tr ± sqrt(tr^2 - 4 det)) / 2
    trace = g11 + g22
    det   = g11 * g22 - g12 * g12

    # Numerical safety: clamp discriminant
    disc = np.maximum(trace * trace * 0.25 - det, 0.0)
    sqrt_disc = np.sqrt(disc)

    lam_max = trace * 0.5 + sqrt_disc
    lam_min = trace * 0.5 - sqrt_disc

    # Effective mass scale (sqrt of λ_max gives gradient scale)
    m_eff = np.sqrt(np.maximum(lam_max, 0.0))

    # Anisotropy: ratio of principal stiffnesses
    # (1 = isotropic, >1 = strongly directional)
    lam_min_safe = np.maximum(lam_min, 1e-12)
    anisotropy = np.sqrt(lam_max / lam_min_safe)

    return M, L, m_eff, anisotropy


# --------------------------------------------------
# Plotting
# --------------------------------------------------
def plot_mass_tensor_maps():
    M, L, m_eff, anisotropy = compute_mass_tensor_map()

    # Log scale for mass magnitude (for dynamic range)
    mass_log = np.log1p(m_eff)

    # Log anisotropy (so 0 = isotropic, bright = highly anisotropic)
    aniso_log = np.log1p(anisotropy)

    fig = plt.figure(figsize=(16, 7), facecolor="black")

    # --- Panel 1: Mass magnitude ---
    ax1 = fig.add_subplot(1, 2, 1, facecolor="black")
    im1 = ax1.imshow(
        mass_log,
        extent=[M_MIN, M_MAX, L_MIN, L_MAX],
        origin="lower",
        cmap="gist_earth",
    )

    # Mark your three canonical points
    particles = [
        {"label": "Teal (Light)", "pos": (-0.90, 0.81), "color": "cyan"},
        {"label": "Red (Med)",    "pos": (-0.21, -0.60), "color": "red"},
        {"label": "Gold (Heavy)", "pos": (2.46, 1.74),   "color": "gold"},
    ]
    for p in particles:
        mx, my = p["pos"]
        ax1.scatter(mx, my, color=p["color"], s=80,
                    marker="o", edgecolors="white", linewidth=2)
        ax1.text(mx + 0.2, my, p["label"], color="white",
                 fontsize=10, fontweight="bold")

    ax1.set_title("Mass Tensor: Effective Stiffness $m_\\mathrm{eff}$",
                  color="white", fontsize=14)
    ax1.set_xlabel("Mass Field", color="white")
    ax1.set_ylabel("Coupling Field", color="white")
    ax1.tick_params(colors="white")

    cbar1 = plt.colorbar(im1, ax=ax1)
    cbar1.set_label("log(1 + $m_\\mathrm{eff}$)", color="white")
    cbar1.ax.yaxis.set_tick_params(color="white", labelcolor="white")

    # --- Panel 2: Anisotropy map ---
    ax2 = fig.add_subplot(1, 2, 2, facecolor="black")
    im2 = ax2.imshow(
        aniso_log,
        extent=[M_MIN, M_MAX, L_MIN, L_MAX],
        origin="lower",
        cmap="plasma",
    )

    ax2.set_title("Mass Tensor Anisotropy $\\sqrt{\\lambda_{\\max}/\\lambda_{\\min}}$",
                  color="white", fontsize=14)
    ax2.set_xlabel("Mass Field", color="white")
    ax2.set_ylabel("Coupling Field", color="white")
    ax2.tick_params(colors="white")

    cbar2 = plt.colorbar(im2, ax=ax2)
    cbar2.set_label("log(1 + anisotropy)", color="white")
    cbar2.ax.yaxis.set_tick_params(color="white", labelcolor="white")

    plt.tight_layout()
    plt.savefig("mass_tensor_maps.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    plot_mass_tensor_maps()
