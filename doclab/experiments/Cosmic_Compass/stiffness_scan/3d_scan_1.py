import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)
from matplotlib.colors import ListedColormap


# ---------------------------
# 1. Dynamics: Δ-field manifold
# ---------------------------

def compute_delta_manifold(
    resolution=200,
    m_range=(-1.5, 1.5),
    l_range=(-1.0, 2.0),
    max_steps=1000,
    dt=0.05,
    sigma=1.0,
    escape_radius_sq=20.0,
):
    """
    Evolve the Δ-field Hamiltonian system and return:

    m_vals, l_vals: 1D axes
    esc_steps:      2D array of escape time (or max_steps if trapped)
    status:         2D basin ID (0 = trapped, 1/2/3 = basins)
    """

    m_vals = np.linspace(m_range[0], m_range[1], resolution)
    l_vals = np.linspace(l_range[0], l_range[1], resolution)
    M, L = np.meshgrid(m_vals, l_vals)

    # Momenta
    p_m = np.zeros_like(M)
    p_l = np.zeros_like(L)

    status = np.zeros_like(M, dtype=int)
    active = np.ones_like(M, dtype=bool)
    esc_steps = np.zeros_like(M, dtype=float)

    print(f"[Δ] Computing manifold on {resolution}x{resolution} grid...")
    print(f"    m ∈ {m_range}, λ ∈ {l_range}, max_steps={max_steps}, dt={dt}")

    for step in range(1, max_steps + 1):
        # Gradient of V at current position
        grad_m = M + 2.0 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)

        # Half-step momentum
        p_m_half = p_m - 0.5 * dt * grad_m
        p_l_half = p_l - 0.5 * dt * grad_l

        # Full-step position
        M = M + dt * p_m_half
        L = L + dt * p_l_half

        # Gradient at new position
        grad_m2 = M + 2.0 * sigma * M * L
        grad_l2 = L + sigma * (M**2 - L**2)

        # Full-step momentum
        p_m = p_m_half - 0.5 * dt * grad_m2
        p_l = p_l_half - 0.5 * dt * grad_l2

        # Escape / blowup check
        r2 = M**2 + L**2
        bad = (~np.isfinite(M)) | (~np.isfinite(L)) | (~np.isfinite(r2))
        escaped_now = ((r2 > escape_radius_sq) | bad) & active

        if np.any(escaped_now):
            theta = np.arctan2(L[escaped_now], M[escaped_now])

            mask_e1 = (theta > 0.5) & (theta < 2.5)
            mask_e3 = np.abs(theta) > 2.5
            mask_e2 = ~(mask_e1 | mask_e3)

            s = status[escaped_now]
            s[mask_e1] = 1
            s[mask_e2] = 2
            s[mask_e3] = 3
            status[escaped_now] = s

            esc_steps[escaped_now] = step
            active[escaped_now] = False

        if not np.any(active):
            print(f"[Δ] All trajectories escaped by step {step}.")
            break

    esc_steps[active] = max_steps

    # Ensure finiteness
    esc_steps = np.where(np.isfinite(esc_steps), esc_steps, max_steps).astype(float)
    status = np.where(np.isfinite(status), status, 0).astype(int)

    print("[Δ] Manifold computation done.")
    return m_vals, l_vals, esc_steps, status


# ---------------------------
# 2. Derived fields
# ---------------------------

def compute_fields(m_vals, l_vals, esc_steps, status, sigma=1.0, max_steps=1000):
    M, L = np.meshgrid(m_vals, l_vals)

    # Normalized escape time (stability height)
    esc_norm = esc_steps / float(max_steps)
    esc_norm = np.clip(esc_norm, 0.0, 1.0)

    # Coherence field σ = ∂²V/∂m∂λ = 2σm
    coherence = 2.0 * sigma * M

    # Potential gradient |∇V| at the *initial* grid
    M0, L0 = np.meshgrid(m_vals, l_vals)
    grad_m = M0 + 2.0 * sigma * M0 * L0
    grad_l = L0 + sigma * (M0**2 - L0**2)
    grad_mag = np.sqrt(grad_m**2 + grad_l**2)

    # Boundary strength ≈ |∇status|
    status_f = status.astype(float)
    gx = np.zeros_like(status_f)
    gy = np.zeros_like(status_f)
    gx[:, 1:-1] = (status_f[:, 2:] - status_f[:, :-2]) / 2.0
    gy[1:-1, :] = (status_f[2:, :] - status_f[:-2, :]) / 2.0
    boundary_strength = np.sqrt(gx**2 + gy**2)
    if boundary_strength.max() > 0:
        boundary_strength /= boundary_strength.max()

    # Triple points: local 3-basin neighborhoods
    triple = np.zeros_like(status, dtype=bool)
    h, w = status.shape
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            window = status[i - 1 : i + 2, j - 1 : j + 2].ravel()
            uniq = np.unique(window[window != 0])
            if len(uniq) >= 3:
                triple[i, j] = True

    fields = {
        "M": M,
        "L": L,
        "esc_norm": esc_norm,
        "coherence": coherence,
        "grad_mag": grad_mag,
        "boundary_strength": boundary_strength,
        "triple": triple,
    }
    return fields


# ---------------------------
# 3. Plotting: 3D Atlas
# ---------------------------

def plot_3d_atlas(m_vals, l_vals, status, fields, outfile="delta_3d_atlas.png"):
    M = fields["M"]
    L = fields["L"]
    esc_norm = fields["esc_norm"]
    coherence = fields["coherence"]
    grad_mag = fields["grad_mag"]
    boundary_strength = fields["boundary_strength"]
    triple = fields["triple"]

    # Basin color map
    basin_cmap = ListedColormap(
        [
            (0.0, 0.0, 0.0, 1.0),   # 0: trapped/core
            (0.0, 0.8, 0.8, 1.0),   # 1: teal
            (0.9, 0.7, 0.1, 1.0),   # 2: gold
            (0.9, 0.3, 0.1, 1.0),   # 3: red
        ]
    )
    basin_colors = basin_cmap(status)

    fig = plt.figure(figsize=(16, 10))

    # --- Panel 1: Escape manifold + basins ---
    ax1 = fig.add_subplot(2, 2, 1, projection="3d")
    surf1 = ax1.plot_surface(
        M,
        L,
        esc_norm,
        facecolors=basin_colors,
        linewidth=0,
        antialiased=False,
        shade=False,
    )
    ax1.set_title("Stability Surface (Escape Time)\nColored by Basin")
    ax1.set_xlabel("m (Mass Field)")
    ax1.set_ylabel(r"$\lambda$ (Coupling Field)")
    ax1.set_zlabel("normalized escape time")
    ax1.view_init(elev=55, azim=-45)

    # --- Panel 2: Potential gradient |∇V| ---
    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    surf2 = ax2.plot_surface(
        M,
        L,
        grad_mag,
        cmap="viridis",
        linewidth=0,
        antialiased=False,
        shade=True,
    )
    ax2.set_title("Potential Gradient |∇V|")
    ax2.set_xlabel("m")
    ax2.set_ylabel(r"$\lambda$")
    ax2.set_zlabel("|∇V|")
    fig.colorbar(surf2, ax=ax2, shrink=0.6, pad=0.1)
    ax2.view_init(elev=55, azim=-35)

    # --- Panel 3: Coherence plane + triple points ---
    ax3 = fig.add_subplot(2, 2, 3, projection="3d")
    surf3 = ax3.plot_surface(
        M,
        L,
        coherence,
        cmap="coolwarm",
        linewidth=0,
        antialiased=False,
        alpha=0.9,
    )
    # triple points as spikes above the coherence plane
    if triple.any():
        ax3.scatter(
            M[triple],
            L[triple],
            coherence[triple] + 0.15,
            s=5,
            c="yellow",
            alpha=0.9,
        )
    ax3.set_title("Coherence Field σ = ∂²V/∂m∂λ\nTriple Points Highlighted")
    ax3.set_xlabel("m")
    ax3.set_ylabel(r"$\lambda$")
    ax3.set_zlabel("σ-field")
    fig.colorbar(surf3, ax=ax3, shrink=0.6, pad=0.1)
    ax3.view_init(elev=60, azim=-60)

    # --- Panel 4: Boundary strength surface ---
    ax4 = fig.add_subplot(2, 2, 4, projection="3d")
    surf4 = ax4.plot_surface(
        M,
        L,
        boundary_strength,
        cmap="inferno",
        linewidth=0,
        antialiased=False,
        shade=True,
    )
    ax4.set_title("Boundary Strength (Where Decision Happens)")
    ax4.set_xlabel("m")
    ax4.set_ylabel(r"$\lambda$")
    ax4.set_zlabel("boundary strength")
    fig.colorbar(surf4, ax=ax4, shrink=0.6, pad=0.1)
    ax4.view_init(elev=65, azim=-40)

    plt.tight_layout()
    print(f"[Δ] Saving atlas to {outfile} ...")
    plt.savefig(outfile, dpi=200)
    plt.show()
    print("[Δ] Done.")


# ---------------------------
# 4. Main
# ---------------------------

if __name__ == "__main__":
    # You can bump resolution to 300 if your machine is comfy with it
    m_vals, l_vals, esc_steps, status = compute_delta_manifold(
        resolution=220,
        max_steps=800,
        dt=0.05,
        sigma=1.0,
        escape_radius_sq=20.0,
    )

    fields = compute_fields(m_vals, l_vals, esc_steps, status, sigma=1.0, max_steps=800)
    plot_3d_atlas(m_vals, l_vals, status, fields, outfile="delta_3d_atlas.png")
