# unification_27.py
# Phase manifold of matter in vacuum tensor space:
# 3D plot of (m_eff, anisotropy, action_mass) + vacuum "generation ridge".

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D projection)

# --------------------------------------------------
# GLOBAL PARAMETERS (match unification_26)
# --------------------------------------------------
RES   = 800
TWIST = 3.8
M_MIN, M_MAX = -3.0, 3.0
L_MIN, L_MAX = -3.0, 3.0
EPS = 1e-3

# --------------------------------------------------
# PARTICLE CANDIDATES (from unification_19 report)
# --------------------------------------------------
candidate_ids = np.array([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 13, 14, 15])

candidate_species = np.array([
    "Red", "Red", "Red", "Red", "Red", "Red", "Red", "Red",
    "Teal", "Gold", "Gold", "Teal", "Gold"
])

candidate_m = np.array([
    -2.40, -1.74, -0.12,  1.35,  2.97,
     0.12,  0.15, -0.21, -0.90,  2.46,
     1.77, -3.00,  2.85
])

candidate_l = np.array([
    -3.00, -3.00, -3.00, -3.00, -3.00,
    -1.86, -1.08, -0.60,  0.81,  1.74,
     2.76,  2.97,  2.97
])

candidate_action_mass = np.array([
     2.72406, 11.00568,  4.48516,  1.80143,  7.38332,
    10.09232,  2.23260,  3.85218,  4.81893, 13.34630,
     3.91280,  2.60456, 10.12158
])


# --------------------------------------------------
# FORCE FIELD (same as in unification_26)
# --------------------------------------------------
def get_force_vectorized(m, lam):
    # Teal (light)
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red (weak) with CP twist
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold (strong) = squeezed vector sum
    sum_m   = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude)

    F_gold_m   = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor

    # Angular weights
    angle = np.degrees(np.arctan2(lam, m)) % 360.0

    diff_g = np.abs(angle - 30.0)
    diff_g = np.minimum(diff_g, 360.0 - diff_g)
    w_gold = np.exp(-(diff_g / 80.0)**2)

    diff_t = np.abs(angle - 150.0)
    diff_t = np.minimum(diff_t, 360.0 - diff_t)
    w_teal = np.exp(-(diff_t / 80.0)**2)

    diff_r = np.abs(angle - 270.0)
    diff_r = np.minimum(diff_r, 360.0 - diff_r)
    w_red = np.exp(-(diff_r / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6
    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam


# --------------------------------------------------
# MASS TENSOR FIELD
# --------------------------------------------------
def compute_mass_tensor_map():
    print(f"[Δ] Computing mass tensor on {RES}x{RES} grid...")

    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)

    Fm, Flam = get_force_vectorized(M, L)

    # central differences
    Fm_plus_m,  Flam_plus_m  = get_force_vectorized(M + EPS, M*0 + L)
    Fm_minus_m, Flam_minus_m = get_force_vectorized(M - EPS, M*0 + L)

    Fm_plus_l,  Flam_plus_l  = get_force_vectorized(M*0 + M, L + EPS)
    Fm_minus_l, Flam_minus_l = get_force_vectorized(M*0 + M, L - EPS)

    dFx_dm = (Fm_plus_m  - Fm_minus_m)  / (2.0 * EPS)
    dFx_dl = (Fm_plus_l  - Fm_minus_l)  / (2.0 * EPS)
    dFy_dm = (Flam_plus_m - Flam_minus_m) / (2.0 * EPS)
    dFy_dl = (Flam_plus_l - Flam_minus_l) / (2.0 * EPS)

    a = dFx_dm
    b = dFx_dl
    c = dFy_dm
    d = dFy_dl

    g11 = a*a + c*c
    g12 = a*b + c*d
    g22 = b*b + d*d

    trace = g11 + g22
    det   = g11*g22 - g12*g12

    disc = np.maximum(trace*trace*0.25 - det, 0.0)
    sqrt_disc = np.sqrt(disc)

    lam_max = trace*0.5 + sqrt_disc
    lam_min = trace*0.5 - sqrt_disc

    m_eff = np.sqrt(np.maximum(lam_max, 0.0))
    lam_min_safe = np.maximum(lam_min, 1e-12)
    anisotropy = np.sqrt(lam_max / lam_min_safe)

    return M, L, m_eff, anisotropy


# --------------------------------------------------
# SAMPLING & CLUSTERING
# --------------------------------------------------
def sample_tensor_at_candidates(m_eff, anisotropy, m_coords, l_coords):
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)

    m_idx = np.searchsorted(m_range, m_coords) - 1
    l_idx = np.searchsorted(l_range, l_coords) - 1

    m_idx = np.clip(m_idx, 0, RES-1)
    l_idx = np.clip(l_idx, 0, RES-1)

    sampled_meff  = m_eff[l_idx, m_idx]
    sampled_aniso = anisotropy[l_idx, m_idx]
    return sampled_meff, sampled_aniso


def cluster_generations(sampled_meff, sampled_aniso):
    X = np.column_stack([sampled_meff, sampled_aniso])

    kmeans = KMeans(n_clusters=3, n_init=32, random_state=42)
    raw_labels = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_

    # Order clusters by increasing anisotropy
    order = np.argsort(centers[:, 1])
    gen_labels = np.empty(len(raw_labels), dtype="<U4")

    for gen_idx, cluster_idx in enumerate(order):
        gen_labels[raw_labels == cluster_idx] = f"G{gen_idx+1}"

    centers_ordered = centers[order]
    return gen_labels, centers_ordered


# --------------------------------------------------
# PHASE MANIFOLD PLOT
# --------------------------------------------------
def plot_phase_manifold():
    # 1) Tensor + sampling
    _, _, m_eff, anisotropy = compute_mass_tensor_map()
    sampled_meff, sampled_aniso = sample_tensor_at_candidates(
        m_eff, anisotropy, candidate_m, candidate_l
    )

    # 2) Cluster generations
    gen_labels, centers = cluster_generations(sampled_meff, sampled_aniso)

    print("\nGENERATION CENTERS (ordered by anisotropy; G1 lowest):")
    for gi, c in enumerate(centers, start=1):
        print(f"G{gi}: (m_eff={c[0]:.2f}, aniso={c[1]:.2f})")

    # 3) Compute generation means in full 3D (m_eff, aniso, action_mass)
    gen_colors = {"G1": "lime", "G2": "orange", "G3": "magenta"}
    species_edge = {"Red": "red", "Teal": "cyan", "Gold": "gold"}

    gen_mean_points = []
    for gi in ["G1", "G2", "G3"]:
        mask = (gen_labels == gi)
        if not np.any(mask):
            continue
        mean_meff  = sampled_meff[mask].mean()
        mean_aniso = sampled_aniso[mask].mean()
        mean_mass  = candidate_action_mass[mask].mean()
        gen_mean_points.append((gi, mean_meff, mean_aniso, mean_mass))

    # Sort mean points by anisotropy to form a clean ridge
    gen_mean_points.sort(key=lambda x: x[2])

    # 4) 3D plot
    fig = plt.figure(figsize=(10, 8), facecolor="black")
    ax = fig.add_subplot(111, projection="3d", facecolor="black")

    # Scatter particles
    for i in range(len(candidate_ids)):
        ax.scatter(
            sampled_meff[i],
            sampled_aniso[i],
            candidate_action_mass[i],
            s=80,
            color=gen_colors[gen_labels[i]],
            edgecolors=species_edge[candidate_species[i]],
            linewidths=1.4,
            depthshade=False,
        )
        ax.text(
            sampled_meff[i] + 0.08,
            sampled_aniso[i] + 0.8,
            candidate_action_mass[i] + 0.1,
            f"{candidate_ids[i]}",
            color="white",
            fontsize=7,
        )

    # Ridge line through generation means
    ridge_x = [p[1] for p in gen_mean_points]
    ridge_y = [p[2] for p in gen_mean_points]
    ridge_z = [p[3] for p in gen_mean_points]

    ax.plot(
        ridge_x,
        ridge_y,
        ridge_z,
        color="white",
        linewidth=2.5,
        label="Vacuum generation ridge",
    )

    # Also mark the generation mean points on the ridge
    for gi, xg, yg, zg in gen_mean_points:
        ax.scatter(
            xg, yg, zg,
            s=140,
            color=gen_colors[gi],
            edgecolors="white",
            linewidths=2.0,
            depthshade=False,
        )
        ax.text(
            xg + 0.1,
            yg + 1.5,
            zg + 0.2,
            gi,
            color="white",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_xlabel(r"$m_\mathrm{eff}$ (tensor mass)", color="white")
    ax.set_ylabel(r"Anisotropy $\sqrt{\lambda_{\max}/\lambda_{\min}}$",
                  color="white")
    ax.set_zlabel("Stable Mass (Action)", color="white")

    ax.tick_params(colors="white")
    for spine in ax.xaxis.get_ticklines() + ax.yaxis.get_ticklines() + ax.zaxis.get_ticklines():
        spine.set_color("white")

    ax.set_title(
        "Phase Manifold of Matter in Vacuum Tensor Space\n"
        "(Fill = Generation, Edge = Species, Ridge = Vacuum Mean",
        color="white",
        fontsize=12,
    )

    # Nice viewing angle
    ax.view_init(elev=25, azim=135)

    # Legend for generations & species
    from matplotlib.patches import Patch
    gen_handles = [
        Patch(facecolor=col, edgecolor="white", label=lab)
        for lab, col in gen_colors.items()
    ]
    species_handles = [
        Patch(facecolor="none", edgecolor=col, linewidth=2, label=lab)
        for lab, col in species_edge.items()
    ]
    leg = ax.legend(
        handles=gen_handles + species_handles,
        loc="upper left",
        fontsize=8,
        facecolor="black",
        edgecolor="white",
        title="Fill = Gen, Edge = Species",
        title_fontsize=8,
    )
    for text in leg.get_texts():
        text.set_color("white")
    leg.get_title().set_color("white")

    plt.tight_layout()
    plt.savefig("phase_manifold.png", dpi=220)
    plt.show()


if __name__ == "__main__":
    plot_phase_manifold()
