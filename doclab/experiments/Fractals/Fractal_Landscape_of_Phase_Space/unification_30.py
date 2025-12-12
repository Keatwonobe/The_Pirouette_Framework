# unification_26.py
# Particle Atlas: overlay candidate particles on the vacuum tensor maps.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# --------------------------------------------------
# GLOBAL PARAMETERS (match earlier scripts)
# --------------------------------------------------
RES   = 800
TWIST = 3.8
GAMMA = 0.11  # (kept for context)

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
# FORCE FIELD (same as your coupling map)
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

    # central differences for Jacobian
    Fm, Flam = get_force_vectorized(M, L)

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
# SAMPLING AND CLUSTERING
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

    # reorder centers to match G1,G2,G3
    centers_ordered = centers[order]
    return gen_labels, centers_ordered


# --------------------------------------------------
# PARTICLE ATLAS PLOTS
# --------------------------------------------------
def make_particle_atlas():
    M, L, m_eff, anisotropy = compute_mass_tensor_map()
    sampled_meff, sampled_aniso = sample_tensor_at_candidates(
        m_eff, anisotropy, candidate_m, candidate_l
    )
    gen_labels, centers = cluster_generations(sampled_meff, sampled_aniso)

    print("\nGENERATION CENTERS (ordered by anisotropy; G1 lowest):")
    for gi, c in enumerate(centers, start=1):
        print(f"G{gi}: (m_eff={c[0]:.2f}, aniso={c[1]:.2f})")

    # Color maps
    mass_log  = np.log1p(m_eff)
    aniso_log = np.log1p(anisotropy)

    gen_colors = {"G1": "lime", "G2": "orange", "G3": "magenta"}
    species_edge = {"Red": "red", "Teal": "cyan", "Gold": "gold"}

    fig = plt.figure(figsize=(18, 6), facecolor="black")

    # -------- Panel 1: m_eff map --------
    ax1 = fig.add_subplot(1, 3, 1, facecolor="black")
    im1 = ax1.imshow(
        mass_log,
        extent=[M_MIN, M_MAX, L_MIN, L_MAX],
        origin="lower",
        cmap="gist_earth",
    )
    ax1.set_title("Mass Tensor $m_\\mathrm{eff}$ with Particles",
                  color="white", fontsize=13)
    ax1.set_xlabel("Mass Field", color="white")
    ax1.set_ylabel("Coupling Field", color="white")
    ax1.tick_params(colors="white")

    for i in range(len(candidate_ids)):
        ax1.scatter(
            candidate_m[i],
            candidate_l[i],
            s=90,
            color=gen_colors[gen_labels[i]],
            edgecolors=species_edge[candidate_species[i]],
            linewidths=1.5,
        )
        ax1.text(
            candidate_m[i] + 0.08,
            candidate_l[i] + 0.05,
            f"{candidate_ids[i]}",
            color="white",
            fontsize=8,
        )

    cbar1 = plt.colorbar(im1, ax=ax1)
    cbar1.set_label("log(1 + $m_\\mathrm{eff}$)", color="white")
    cbar1.ax.yaxis.set_tick_params(color="white", labelcolor="white")

    # -------- Panel 2: anisotropy map --------
    ax2 = fig.add_subplot(1, 3, 2, facecolor="black")
    im2 = ax2.imshow(
        aniso_log,
        extent=[M_MIN, M_MAX, L_MIN, L_MAX],
        origin="lower",
        cmap="plasma",
    )
    ax2.set_title("Vacuum Anisotropy $\\sqrt{\\lambda_{\\max}/\\lambda_{\\min}}$",
                  color="white", fontsize=13)
    ax2.set_xlabel("Mass Field", color="white")
    ax2.set_ylabel("Coupling Field", color="white")
    ax2.tick_params(colors="white")

    for i in range(len(candidate_ids)):
        ax2.scatter(
            candidate_m[i],
            candidate_l[i],
            s=90,
            color=gen_colors[gen_labels[i]],
            edgecolors=species_edge[candidate_species[i]],
            linewidths=1.5,
        )
        ax2.text(
            candidate_m[i] + 0.08,
            candidate_l[i] + 0.05,
            f"{candidate_ids[i]}",
            color="white",
            fontsize=8,
        )

    cbar2 = plt.colorbar(im2, ax=ax2)
    cbar2.set_label("log(1 + anisotropy)", color="white")
    cbar2.ax.yaxis.set_tick_params(color="white", labelcolor="white")

    # -------- Panel 3: geodesic flow (force streamlines) --------
    ax3 = fig.add_subplot(1, 3, 3, facecolor="black")

    # Use a coarser grid for streamplot
    STREAM_RES = 60
    m_stream = np.linspace(M_MIN, M_MAX, STREAM_RES)
    l_stream = np.linspace(L_MIN, L_MAX, STREAM_RES)
    MS, LS = np.meshgrid(m_stream, l_stream)
    Fm, Flam = get_force_vectorized(MS, LS)

    # Background: same mass_log but resampled automatically by imshow
    im3 = ax3.imshow(
        mass_log,
        extent=[M_MIN, M_MAX, L_MIN, L_MAX],
        origin="lower",
        cmap="magma",
        alpha=0.7,
    )

    speed = np.sqrt(Fm**2 + Flam**2)
    # Normalize vectors for clearer streamlines
    Fm_n = Fm / (speed + 1e-6)
    Flam_n = Flam / (speed + 1e-6)

    ax3.streamplot(
        m_stream,
        l_stream,
        Fm_n,
        Flam_n,
        density=1.2,
        color="cyan",
        linewidth=0.7,
        arrowsize=0.8,
    )

    for i in range(len(candidate_ids)):
        ax3.scatter(
            candidate_m[i],
            candidate_l[i],
            s=90,
            color=gen_colors[gen_labels[i]],
            edgecolors=species_edge[candidate_species[i]],
            linewidths=1.5,
        )
        ax3.text(
            candidate_m[i] + 0.08,
            candidate_l[i] + 0.05,
            f"{candidate_ids[i]}",
            color="white",
            fontsize=8,
        )

    ax3.set_title("Geodesic Flow of the Vacuum\n(streamlines of force field)",
                  color="white", fontsize=13)
    ax3.set_xlabel("Mass Field", color="white")
    ax3.set_ylabel("Coupling Field", color="white")
    ax3.tick_params(colors="white")

    # Legend for generations and species
    from matplotlib.patches import Patch
    gen_handles = [
        Patch(facecolor=col, edgecolor="white", label=lab)
        for lab, col in gen_colors.items()
    ]
    species_handles = [
        Patch(facecolor="none", edgecolor=col, linewidth=2, label=lab)
        for lab, col in species_edge.items()
    ]
    ax3.legend(
        handles=gen_handles + species_handles,
        loc="upper left",
        fontsize=8,
        facecolor="black",
        edgecolor="white",
        title="Fill = Gen, Edge = Species",
        title_fontsize=8,
    )

    plt.tight_layout()
    plt.savefig("particle_atlas.png", dpi=220)
    plt.show()


if __name__ == "__main__":
    make_particle_atlas()
