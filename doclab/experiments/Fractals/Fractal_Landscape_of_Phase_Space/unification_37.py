"""
unification_36.py
-----------------
Gladiator Arch Indexing

This script builds a simple "gladiator arch" stability surface in (omega, Gamma)
and defines a clean arch-indexing scheme:

  Arch centers:  omega_k = (2k + 1) * pi / 2,   k ∈ Z

Given any list of omega values, we can assign each point the index of the
nearest arch and its offset from that arch.

You can later map your own vacuum variables to an effective omega and call
`assign_arch_indices(...)` to give each particle / orbit an "arch identity".
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
OMEGA_MIN, OMEGA_MAX = 0.0, 20.0   # horizontal axis
GAMMA_MIN, GAMMA_MAX = 0.0, 10.0   # vertical axis

N_OMEGA = 800
N_GAMMA = 400

# Example test points in (omega, Gamma) to show arch indexing.
# Replace or extend this list with your own:
TEST_POINTS = [
    (1.2,  2.0, "A"),
    (4.6,  5.0, "B"),
    (7.8,  3.5, "C"),
    (9.4,  1.0, "D"),
    (15.7, 8.0, "E"),
]

# ---------------------------------------------------------------------
# STABILITY SURFACE (simple gladiator-arch style)
# ---------------------------------------------------------------------
def stability_surface(omega, gamma):
    """
    A simple archetype surface that produces vertical "arches" where cos(omega)=0,
    and grows slowly with gamma.

    We don't need the exact earlier formula; all we need is that:
      - there are vertical ridges at (2k+1)*pi/2
      - depth increases with gamma

    S(omega, gamma) ~ (gamma + 1) / (|cos(omega)| + epsilon)
    and we plot log10(S).
    """
    eps = 1e-3
    base = np.abs(np.cos(omega)) + eps
    raw = (gamma + 1.0) / base
    return np.log10(raw)


# ---------------------------------------------------------------------
# ARCH CENTER GENERATION
# ---------------------------------------------------------------------
def compute_arch_centers(omega_min, omega_max):
    """
    Compute arch centers omega_k = (2k+1)*pi/2 that lie within [omega_min, omega_max].

    Returns:
        arch_ids      : array of integer arch indices (0..N_arch-1)
        arch_centers  : array of omega positions for each arch id
    """
    # Generate a generous range of k values and then trim to [omega_min, omega_max]
    k_vals = np.arange(-20, 40)  # wide range, will get trimmed
    centers = (2 * k_vals + 1) * np.pi / 2.0

    mask = (centers >= omega_min) & (centers <= omega_max)
    centers = centers[mask]

    # Reindex them from 0..N_arch-1 in order of increasing omega
    sort_idx = np.argsort(centers)
    centers_sorted = centers[sort_idx]
    arch_ids = np.arange(len(centers_sorted))

    return arch_ids, centers_sorted


def assign_arch_indices(omega_points, arch_centers):
    """
    For each omega in omega_points, assign the index of the nearest arch center.

    Args:
        omega_points : 1D array-like
        arch_centers : 1D array of arch center omegas

    Returns:
        indices  : integer array of same shape as omega_points
        offsets  : omega_points - arch_centers[indices] (signed distance from center)
    """
    omega_points = np.asarray(omega_points)
    centers = arch_centers[None, :]  # shape (1, N_centers)
    omega_grid = omega_points[:, None]  # shape (N_points, 1)

    # Compute absolute distance to each center, choose nearest
    dist = np.abs(omega_grid - centers)
    idx = dist.argmin(axis=1)
    offsets = omega_points - arch_centers[idx]
    return idx, offsets


# ---------------------------------------------------------------------
# PLOTTING
# ---------------------------------------------------------------------
def plot_arch_map_with_points():
    # 1) Build the grid and surface
    omega_vals = np.linspace(OMEGA_MIN, OMEGA_MAX, N_OMEGA)
    gamma_vals = np.linspace(GAMMA_MIN, GAMMA_MAX, N_GAMMA)
    OMEGA, GAMMA = np.meshgrid(omega_vals, gamma_vals)

    Z = stability_surface(OMEGA, GAMMA)

    # 2) Compute arch centers in this range
    arch_ids, arch_centers = compute_arch_centers(OMEGA_MIN, OMEGA_MAX)

    # 3) Extract test points and assign arch indices
    if len(TEST_POINTS) > 0:
        test_omega = np.array([p[0] for p in TEST_POINTS])
        test_gamma = np.array([p[1] for p in TEST_POINTS])
        test_labels = [p[2] for p in TEST_POINTS]

        arch_idx, omega_offset = assign_arch_indices(test_omega, arch_centers)
    else:
        test_omega = np.array([])
        test_gamma = np.array([])
        test_labels = []
        arch_idx = np.array([])
        omega_offset = np.array([])

    # Print arch assignment to console
    if len(TEST_POINTS) > 0:
        print("ARCH INDEX ASSIGNMENT")
        print("Label | omega | Gamma | ArchID | omega_offset")
        print("----------------------------------------------")
        for lbl, om, gm, ai, off in zip(test_labels, test_omega, test_gamma,
                                        arch_idx, omega_offset):
            print(f"{lbl:>5} | {om:6.3f} | {gm:5.2f} | "
                  f"{ai:6d} | {off:+9.4f}")

    # 4) Plot
    fig, ax = plt.subplots(figsize=(12, 7), facecolor="black")
    ax.set_facecolor("black")

    im = ax.imshow(
        Z,
        origin="lower",
        extent=[OMEGA_MIN, OMEGA_MAX, GAMMA_MIN, GAMMA_MAX],
        aspect="auto",
        cmap="magma",
    )

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Potential depth (log scale)", color="white")
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.get_yticklabels(), color="white")

    ax.set_xlabel(r"Drive Frequency $\omega$", color="white")
    ax.set_ylabel(r"Gladiator Constant $\Gamma$", color="white")
    ax.set_title(
        "Gladiator Arch Stability Map\n"
        "(Vertical ridges = arch centers, points = indexed locations)",
        color="white",
        fontsize=14,
    )

    ax.tick_params(colors="white")

    # Draw arch center lines & labels
    for arch_id, center_omega in zip(arch_ids, arch_centers):
        ax.axvline(center_omega, color="cyan", linestyle="--", alpha=0.4, linewidth=1.0)
        ax.text(
            center_omega,
            GAMMA_MAX + 0.2,
            f"{arch_id}",
            color="cyan",
            fontsize=8,
            ha="center",
            va="bottom",
        )

    # Overlay test points if any
    if len(TEST_POINTS) > 0:
        for om, gm, lbl, ai in zip(test_omega, test_gamma, test_labels, arch_idx):
            ax.plot(om, gm, marker="*", color="white", markersize=9)
            ax.text(
                om + 0.15,
                gm + 0.15,
                f"{lbl} (A{ai})",
                color="white",
                fontsize=8,
                ha="left",
                va="bottom",
            )

    plt.tight_layout()
    plt.savefig("gladiator_arch_index_map.png", dpi=220)
    plt.show()


if __name__ == "__main__":
    plot_arch_map_with_points()
