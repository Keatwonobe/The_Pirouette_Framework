import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Fractal Stirrer / Traveler Knot Simulator
# ==========================================================

# Global simulation parameters
N_TRAVELERS = 2          # number of stirring strands
R_BOWL       = 10.0      # radius of the "bowl" (manifold cross-section)
DT           = 0.01      # time step
N_STEPS      = 30000     # total steps
OUTPUT_EVERY = 10        # subsample for plotting
SOFTENING    = 0.05      # softening length to avoid singularities

# Force constants
K_CENTER   = 0.5         # attraction to bowl center
K_PAIRWISE = 1.0         # mutual attraction between travelers
GAMMA_DRAG = 0.02        # drag coefficient (dissipation / tension)

# Radius where we say "we're in the knot core" (COM frame)
R_CORE = 5.0


# ----------------------------------------------------------
# Initial conditions
# ----------------------------------------------------------
def init_travelers(n=N_TRAVELERS, radius=R_BOWL, ccw=True, seed=None):
    """
    Place travelers on the bowl boundary with inward-pointing velocities.
    We add a tangential component to imprint chirality (ccw vs cw).
    """
    rng = np.random.default_rng(seed)
    # Put them roughly on a semicircle, with a bit of jitter
    angles = np.linspace(0, np.pi, n, endpoint=False)
    angles += rng.normal(scale=0.05, size=n)

    pos = np.zeros((n, 2))
    vel = np.zeros((n, 2))

    for i, a in enumerate(angles):
        x = radius * np.cos(a)
        y = radius * np.sin(a)
        pos[i] = [x, y]

        # Radial inward direction
        r = pos[i]
        r_hat = -r / np.linalg.norm(r)

        # Tangential direction (perpendicular to r_hat)
        t_hat = np.array([-r_hat[1], r_hat[0]])
        if not ccw:
            t_hat *= -1.0

        v_in = 1.0   # inward speed
        v_tan = 0.8  # tangential speed

        vel[i] = v_in * r_hat + v_tan * t_hat

    return pos, vel


# ----------------------------------------------------------
# Forces
# ----------------------------------------------------------
def compute_forces(pos):
    """
    Compute accelerations due to:
      1) attraction to the origin (center of bowl),
      2) pairwise attraction between travelers,
    Drag is applied in the integrator, not here.
    """
    n = pos.shape[0]
    acc = np.zeros_like(pos)

    # Center attraction ~ -K_CENTER * r / (r^2 + eps)^(3/2)
    r2 = np.sum(pos**2, axis=1) + SOFTENING**2
    r = np.sqrt(r2)
    acc_center = (-K_CENTER * pos.T / r2**(1.5)).T
    acc += acc_center

    # Pairwise attractions ~ 1 / r^2
    for i in range(n):
        for j in range(i + 1, n):
            diff = pos[j] - pos[i]
            d2 = np.dot(diff, diff) + SOFTENING**2
            d = np.sqrt(d2)
            f_mag = K_PAIRWISE / d2
            f_vec = f_mag * diff / d
            acc[i] += f_vec
            acc[j] -= f_vec

    return acc


# ----------------------------------------------------------
# Main simulation loop
# ----------------------------------------------------------
def run_simulation(n_travelers=N_TRAVELERS, random_seed=42):
    pos, vel = init_travelers(n_travelers, ccw=True, seed=random_seed)

    pos_hist = []   # (T, N, 2)
    com_hist = []   # (T, 2)
    rel_hist = []   # (T, N, 2) positions in COM frame

    for step in range(N_STEPS):
        acc = compute_forces(pos)

        # Velocity-Verlet / leapfrog-ish
        vel += acc * DT
        vel *= (1.0 - GAMMA_DRAG * DT)  # drag
        pos += vel * DT

        if step % OUTPUT_EVERY == 0:
            pos_hist.append(pos.copy())
            com = pos.mean(axis=0)
            com_hist.append(com)
            rel_hist.append(pos - com)

    pos_hist = np.array(pos_hist)
    com_hist = np.array(com_hist)
    rel_hist = np.array(rel_hist)

    return pos_hist, com_hist, rel_hist


# ----------------------------------------------------------
# Knot core extraction & PCA
# ----------------------------------------------------------
def analyze_knot_core(rel_hist, r_core=R_CORE):
    """
    Extract points where *all* travelers are inside r_core and
    project them into the PCA plane to inspect the knot shape.

    Returns:
        coords_2d: (M, 2) array of core points in PCA plane
        idx_core: indices of timesteps included
    """
    T, N, _ = rel_hist.shape
    r = np.linalg.norm(rel_hist, axis=2)  # radial distance for each traveler

    # times where everyone is in the knot core
    mask = (r < r_core).all(axis=1)
    idx_core = np.where(mask)[0]

    if idx_core.size == 0:
        print("[analyze_knot_core] No timesteps with all travelers inside core.")
        return None, idx_core

    # stack all traveler positions from core interval
    core_pts = rel_hist[idx_core].reshape(-1, 2)

    # PCA on the core points
    core_mean = core_pts.mean(axis=0)
    centered = core_pts - core_mean
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)
    basis = Vt[:2]  # 2x2, principal directions

    coords_2d = centered @ basis.T
    return coords_2d, idx_core


# ----------------------------------------------------------
# Lobe counting heuristic
# ----------------------------------------------------------
def estimate_lobes(coords_2d, n_bins=180, prominence=0.15):
    """
    Crude estimate of how many 'lobes' the knot has in the PCA plane.

    Steps:
      - convert core points to polar angles,
      - build an angular histogram,
      - count local maxima above a prominence threshold.

    It's just a quick 'triangle vs square vs pentagon' sniff-test.
    """
    if coords_2d is None or coords_2d.shape[0] == 0:
        return 0

    x, y = coords_2d[:, 0], coords_2d[:, 1]
    angles = np.arctan2(y, x)
    angles = (angles + 2 * np.pi) % (2 * np.pi)  # wrap to [0, 2π)

    hist, edges = np.histogram(angles, bins=n_bins, range=(0, 2 * np.pi))
    hist = hist.astype(float)

    if hist.max() > 0:
        hist /= hist.max()

    peaks = 0
    for i in range(n_bins):
        prev_ = hist[i - 1]
        curr = hist[i]
        next_ = hist[(i + 1) % n_bins]
        if curr > prev_ and curr > next_ and curr > prominence:
            peaks += 1

    return peaks


# ----------------------------------------------------------
# Plotting
# ----------------------------------------------------------
def plot_results(pos_hist, com_hist, rel_hist, coords_2d, idx_core):
    T, N, _ = pos_hist.shape
    times = np.arange(T)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # 1. Absolute motion in the bowl
    for i in range(N):
        ax1.plot(pos_hist[:, i, 0], pos_hist[:, i, 1], lw=0.8)
    circle = plt.Circle((0, 0), R_BOWL, edgecolor='gray',
                        linestyle='--', fill=False, alpha=0.5)
    ax1.add_artist(circle)
    ax1.set_aspect('equal', 'box')
    ax1.set_title("Traveler Trajectories in the Bowl")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    # 2. Center-of-mass path
    ax2.plot(com_hist[:, 0], com_hist[:, 1], color='black', lw=1.2)
    ax2.set_aspect('equal', 'box')
    ax2.set_title("Center-of-Mass Path")
    ax2.set_xlabel("x_COM")
    ax2.set_ylabel("y_COM")

    # 3. Radius vs time in COM frame (with knot-core highlight)
    r = np.linalg.norm(rel_hist, axis=2)
    for i in range(N):
        ax3.plot(times, r[:, i], lw=0.7, label=f"Traveler {i+1}")
    if idx_core.size > 0:
        ax3.axvspan(times[idx_core[0]], times[idx_core[-1]],
                    color='green', alpha=0.1, label="knot core interval")
    ax3.axhline(R_CORE, color='red', linestyle='--', alpha=0.6, label="R_core")
    ax3.set_yscale('log')
    ax3.set_xlabel("Subsampled time index")
    ax3.set_ylabel("Radius in COM frame")
    ax3.set_title("Radial Distances (COM frame)")
    ax3.legend(loc='best', fontsize=8)

    # 4. Knot core PCA projection
    if coords_2d is not None:
        ax4.scatter(coords_2d[:, 0], coords_2d[:, 1], s=4, alpha=0.6)
        ax4.set_aspect('equal', 'box')
        ax4.set_title("Knot Core in PCA Plane")
        ax4.set_xlabel("PC1")
        ax4.set_ylabel("PC2")
    else:
        ax4.text(0.5, 0.5, "No core points", ha='center', va='center')
        ax4.set_axis_off()

    plt.tight_layout()
    plt.show()


# ----------------------------------------------------------
# Entry point
# ----------------------------------------------------------
if __name__ == "__main__":
    pos_hist, com_hist, rel_hist = run_simulation()
    coords_2d, idx_core = analyze_knot_core(rel_hist)
    lobes = estimate_lobes(coords_2d)
    if lobes:
        print(f"Estimated lobe count in knot core: ~{lobes}")
    else:
        print("Estimated lobe count: undefined (no core / no structure)")
    plot_results(pos_hist, com_hist, rel_hist, coords_2d, idx_core)
