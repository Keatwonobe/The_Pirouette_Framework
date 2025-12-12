import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Load raw data from your scan
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
def plot_zoomed_wada(m_min, m_max, l_min, l_max, out_name="fractal_wada_zoom.png"):
    # boolean masks for the region of interest
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
        vmin=-1, vmax=3,
    )
    plt.axis("off")
    plt.title("Zoomed Wada Basin Structure", color="white", pad=12)
    plt.tight_layout()
    plt.savefig(out_name, dpi=300, facecolor="black")
    plt.close()

# Example: adjust these numbers based on where the detailed “spiky” region sits
plot_zoomed_wada(m_min=-0.3, m_max=0.3, l_min=0.4, l_max=1.0)
def plot_asymmetry_comparison(
    l_min, l_max, m_span=0.8, out_name="fractal_asymmetry_comparison.png"
):
    """
    l_min, l_max: vertical slice in λ where the big lobes live
    m_span: how wide (in |m|) the left/right windows are
    """

    # Choose a symmetric m-range around 0
    m_center = 0.0
    m_left_min, m_left_max   = m_center - m_span, m_center
    m_right_min, m_right_max = m_center, m_center + m_span

    # Masks
    l_mask   = (l_rng >= l_min) & (l_rng <= l_max)
    m_left_mask  = (m_rng >= m_left_min)  & (m_rng <= m_left_max)
    m_right_mask = (m_rng >= m_right_min) & (m_rng <= m_right_max)

    left_grid  = grid[np.ix_(l_mask, m_left_mask)]
    right_grid = grid[np.ix_(l_mask, m_right_mask)]

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor="black")

    # Left lobe
    axes[0].imshow(
        left_grid,
        origin="lower",
        extent=[m_left_min, m_left_max, l_min, l_max],
        cmap=cmap,
        interpolation="nearest",
        vmin=-1, vmax=3,
    )
    axes[0].set_title("Left Basin Lobe", color="white", pad=8)
    axes[0].axis("off")

    # Right lobe
    axes[1].imshow(
        right_grid,
        origin="lower",
        extent=[m_right_min, m_right_max, l_min, l_max],
        cmap=cmap,
        interpolation="nearest",
        vmin=-1, vmax=3,
    )
    axes[1].set_title("Right Basin Lobe", color="white", pad=8)
    axes[1].axis("off")

    fig.suptitle("Asymmetry of Δ Fractal Basins (Left vs Right)", color="white", y=0.95)
    plt.tight_layout()
    plt.savefig(out_name, dpi=300, facecolor="black")
    plt.close()

# Example choice: slice across the upper lobes
plot_asymmetry_comparison(l_min=0.8, l_max=1.6, m_span=1.0)
from reality_basin_2 import PirouetteHamiltonian

ham = PirouetteHamiltonian()

def henon_force(m, l, ham=ham):
    """
    Replace this with whatever your PirouetteHamiltonian uses internally.
    For standard Hénon–Heiles, one has:

        V = 0.5*(m**2 + l**2) + m**2*l - (1/3)*l**3
        dV/dm = m + 2*m*l
        dV/dl = l + m**2 - l**2

    Force is -∇V.
    """
    dV_dm = m + 2*m*l
    dV_dl = l + m**2 - l**2
    return -dV_dm, -dV_dl

def integrate_trajectory(m0, l0, E=0.17, dt=0.01, n_steps=8000, R_cut=3.0):
    """
    Symplectic leapfrog integration of a single trajectory.
    Returns arrays of (m(t), l(t)) up to escape or n_steps.
    """

    # Choose p_m = 0 and solve p_l from energy constraint
    # E = 0.5*(p_m^2 + p_l^2) + V(m,l)
    V0 = 0.5*(m0**2 + l0**2) + m0**2*l0 - (1.0/3.0)*l0**3
    if V0 >= E:
        return np.array([]), np.array([])

    p_m = 0.0
    p_l = np.sqrt(2*(E - V0))

    m, l = m0, l0
    ms = [m]
    ls = [l]

    for _ in range(n_steps):
        # half-step momenta
        Fm, Fl = henon_force(m, l)
        p_m_half = p_m + 0.5*dt*Fm
        p_l_half = p_l + 0.5*dt*Fl

        # full-step positions
        m_new = m + dt*p_m_half
        l_new = l + dt*p_l_half

        # full-step forces
        Fm_new, Fl_new = henon_force(m_new, l_new)

        # full-step momenta
        p_m_new = p_m_half + 0.5*dt*Fm_new
        p_l_new = p_l_half + 0.5*dt*Fl_new

        m, l, p_m, p_l = m_new, l_new, p_m_new, p_l_new
        ms.append(m)
        ls.append(l)

        if m*m + l*l > R_cut**2:
            break

    return np.array(ms), np.array(ls)
def sample_trapped_points(num_points=12):
    trapped_mask = (grid <= 0)  # adjust if your encoding is different
    trapped_indices = np.argwhere(trapped_mask)

    if len(trapped_indices) == 0:
        raise RuntimeError("No trapped points found in grid; adjust mask definition.")

    # Randomly pick some seeds
    idx = np.random.choice(len(trapped_indices), size=min(num_points, len(trapped_indices)), replace=False)
    seeds = []
    for k in idx:
        i, j = trapped_indices[k]
        m = m_rng[j]
        l = l_rng[i]
        seeds.append((m, l))
    return seeds

def plot_particle_trajectories_in_triangle(out_name="fractal_trajectories.png"):
    seeds = sample_trapped_points(num_points=15)

    # Background fate map for context (optional, low alpha so trajectories pop)
    plt.figure(figsize=(8, 8), facecolor="black")
    plt.imshow(
        grid,
        origin="lower",
        extent=[m_rng.min(), m_rng.max(), l_rng.min(), l_rng.max()],
        cmap=cmap,
        interpolation="nearest",
        alpha=0.35,
        vmin=-1, vmax=3,
    )

    # Overlay trajectories
    for m0, l0 in seeds:
        ms, ls = integrate_trajectory(m0, l0)
        if ms.size == 0:
            continue
        plt.plot(ms, ls, linewidth=0.7)

    plt.axis("off")
    plt.title("Particle Trajectories in the Central Δ Wedge", color="white", pad=12)
    plt.tight_layout()
    plt.savefig(out_name, dpi=300, facecolor="black")
    plt.close()

plot_particle_trajectories_in_triangle()
