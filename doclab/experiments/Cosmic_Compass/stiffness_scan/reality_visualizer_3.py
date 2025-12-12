import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from reality_basin_2 import PirouetteHamiltonian

# --------------------------------------------------
# Load raw data from your scan
# --------------------------------------------------
grid   = np.load("delta_fate_grid.npy")
m_rng  = np.load("delta_fate_m_range.npy")
l_rng  = np.load("delta_fate_l_range.npy")

# Same colormap you used for the main figure
colors = [
    (0.0, 0.0, 0.0),     # -1 or 0 => black / trapped / invalid
    (0.95, 0.35, 0.15),  # exit 1
    (0.15, 0.8, 0.95),   # exit 2
    (0.95, 0.85, 0.15),  # exit 3
]
cmap = ListedColormap(colors)


# --------------------------------------------------
# Figure 1: Zoomed Wada detail
# --------------------------------------------------
def plot_zoomed_wada(
    m_min=-0.3,
    m_max=0.3,
    l_min=0.4,
    l_max=1.0,
    out_name="fractal_wada_zoom.png",
):
    """Zoom into a rectangle in (m, λ) space and show fine Wada structure."""
    m_mask = (m_rng >= m_min) & (m_rng <= m_max)
    l_mask = (l_rng >= l_min) & (l_rng <= l_max)

    sub_grid = grid[np.ix_(l_mask, m_mask)]

    plt.figure(figsize=(6, 6), facecolor="black")
    plt.imshow(
        sub_grid,
        origin="lower",
        extent=[m_min, m_max, l_min, l_max],
        cmap=cmap,
        interpolation="nearest",
        vmin=-1,
        vmax=3,
    )
    plt.axis("off")
    plt.title("Zoomed Wada Basin Structure", color="white", pad=12)
    plt.tight_layout()
    plt.savefig(out_name, dpi=300, facecolor="black")
    plt.close()


# --------------------------------------------------
# Figure 2: Asymmetry comparison (left vs right lobes)
# --------------------------------------------------
def plot_asymmetry_comparison(
    l_min=0.8,
    l_max=1.6,
    m_span=1.0,
    out_name="fractal_asymmetry_comparison.png",
):
    """
    Compare symmetric windows on the left and right side
    of the fate map to show geometric asymmetry.
    """
    m_center = 0.0
    m_left_min, m_left_max = m_center - m_span, m_center
    m_right_min, m_right_max = m_center, m_center + m_span

    l_mask = (l_rng >= l_min) & (l_rng <= l_max)
    m_left_mask = (m_rng >= m_left_min) & (m_rng <= m_left_max)
    m_right_mask = (m_rng >= m_right_min) & (m_rng <= m_right_max)

    left_grid = grid[np.ix_(l_mask, m_left_mask)]
    right_grid = grid[np.ix_(l_mask, m_right_mask)]

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor="black")

    axes[0].imshow(
        left_grid,
        origin="lower",
        extent=[m_left_min, m_left_max, l_min, l_max],
        cmap=cmap,
        interpolation="nearest",
        vmin=-1,
        vmax=3,
    )
    axes[0].set_title("Left Basin Lobe", color="white", pad=8)
    axes[0].axis("off")

    axes[1].imshow(
        right_grid,
        origin="lower",
        extent=[m_right_min, m_right_max, l_min, l_max],
        cmap=cmap,
        interpolation="nearest",
        vmin=-1,
        vmax=3,
    )
    axes[1].set_title("Right Basin Lobe", color="white", pad=8)
    axes[1].axis("off")

    fig.suptitle(
        "Asymmetry of Δ Fractal Basins (Left vs Right)",
        color="white",
        y=0.95,
    )
    plt.tight_layout()
    plt.savefig(out_name, dpi=300, facecolor="black")
    plt.close()


# --------------------------------------------------
# Figure 3: Trajectories in the central wedge
# --------------------------------------------------
ham = PirouetteHamiltonian()


def henon_force(m, l):
    """
    Force for the Hénon–Heiles-like potential in (m, λ).
    If reality_basin_2 defines a different V, replace these
    derivatives with ham's actual forces.
    """
    # Standard Hénon–Heiles:
    # V = 0.5*(m**2 + l**2) + m**2*l - (1/3)*l**3
    dV_dm = m + 2.0 * m * l
    dV_dl = l + m**2 - l**2
    return -dV_dm, -dV_dl


def integrate_trajectory(
    m0,
    l0,
    E=0.17,
    dt=0.01,
    n_steps=8000,
    R_cut=3.0,
):
    """
    Symplectic leapfrog integration of a single trajectory.
    Returns arrays of (m(t), l(t)) up to escape or n_steps.
    """

    V0 = 0.5 * (m0**2 + l0**2) + m0**2 * l0 - (1.0 / 3.0) * l0**3
    if V0 >= E:
        return np.array([]), np.array([])

    p_m = 0.0
    p_l = np.sqrt(2.0 * (E - V0))

    m, l = m0, l0
    ms = [m]
    ls = [l]

    for _ in range(n_steps):
        # half-step momenta
        Fm, Fl = henon_force(m, l)
        p_m_half = p_m + 0.5 * dt * Fm
        p_l_half = p_l + 0.5 * dt * Fl

        # full-step positions
        m_new = m + dt * p_m_half
        l_new = l + dt * p_l_half

        # full-step forces
        Fm_new, Fl_new = henon_force(m_new, l_new)

        # full-step momenta
        p_m_new = p_m_half + 0.5 * dt * Fm_new
        p_l_new = p_l_half + 0.5 * dt * Fl_new

        m, l, p_m, p_l = m_new, l_new, p_m_new, p_l_new
        ms.append(m)
        ls.append(l)

        if m * m + l * l > R_cut * R_cut:
            break

    return np.array(ms), np.array(ls)


def sample_trapped_points(num_points=12, seed=1234):
    """
    Pick initial conditions from the 'trapped' (black) region.
    Adjust the mask if your encoding differs.
    """
    rng = np.random.default_rng(seed)

    trapped_mask = grid <= 0  # -1 or 0 => central region
    trapped_indices = np.argwhere(trapped_mask)

    if len(trapped_indices) == 0:
        raise RuntimeError(
            "No trapped points found in grid; adjust mask definition."
        )

    idx = rng.choice(
        len(trapped_indices),
        size=min(num_points, len(trapped_indices)),
        replace=False,
    )
    seeds = []
    for k in idx:
        i, j = trapped_indices[k]
        m = m_rng[j]
        l = l_rng[i]
        seeds.append((m, l))
    return seeds


def plot_particle_trajectories_in_triangle(
    out_name="fractal_trajectories.png",
    num_seeds=15,
):
    seeds = sample_trapped_points(num_points=num_seeds)

    plt.figure(figsize=(8, 8), facecolor="black")
    plt.imshow(
        grid,
        origin="lower",
        extent=[m_rng.min(), m_rng.max(), l_rng.min(), l_rng.max()],
        cmap=cmap,
        interpolation="nearest",
        alpha=0.35,
        vmin=-1,
        vmax=3,
    )

    for m0, l0 in seeds:
        ms, ls = integrate_trajectory(m0, l0)
        if ms.size == 0:
            continue
        plt.plot(ms, ls, linewidth=0.7)

    plt.axis("off")
    plt.title(
        "Particle Trajectories in the Central Δ Wedge",
        color="white",
        pad=12,
    )
    plt.tight_layout()
    plt.savefig(out_name, dpi=300, facecolor="black")
    plt.close()


# --------------------------------------------------
# Main entry point
# --------------------------------------------------
def main():
    print("[Δ-Vis] Generating zoomed Wada figure...")
    plot_zoomed_wada()

    print("[Δ-Vis] Generating asymmetry comparison figure...")
    plot_asymmetry_comparison()

    print("[Δ-Vis] Generating central wedge trajectories figure...")
    plot_particle_trajectories_in_triangle()

    print("[Δ-Vis] Done.")


if __name__ == "__main__":
    main()
