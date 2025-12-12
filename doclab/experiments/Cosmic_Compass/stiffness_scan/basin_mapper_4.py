import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)
from matplotlib import animation
import time

# ============================================================
# Core Δ dynamics (adapted from basin_mapper_3.py)
# ============================================================

def compute_escape_manifold(
    resolution=500,
    zoom_factor=4.0,
    max_steps=1000,
    damping=0.0,
    escape_radius_sq=20.0,
):
    """
    Run the Pirouette Δ-field integration and return:
      - X, Y: 2D grids of (m, λ)
      - Z:    log(escape_time + 1) as 'height'
      - status: basin ID (0 = trapped, 1/2/3 = teal/gold/red)

    This is a 3D-ready version of run_pirouette_deep_field.
    """

    print(f"[Δ] Computing escape manifold...")
    print(f"    resolution = {resolution}x{resolution}")
    print(f"    zoom_factor = {zoom_factor} | max_steps = {max_steps} | damping = {damping}")

    # --- 1. Grid setup (same geometry as deep field) ---
    m_center, l_center = 0.0, 0.5
    m_span = 3.0 * zoom_factor
    l_span = 3.0 * zoom_factor

    m_vals = np.linspace(m_center - m_span / 2, m_center + m_span / 2, resolution)
    l_vals = np.linspace(l_center - l_span / 2, l_center + l_span / 2, resolution)
    M, L = np.meshgrid(m_vals, l_vals)

    # --- 2. Initial conditions ---
    p_m = np.zeros_like(M)
    p_l = np.zeros_like(L)

    status = np.zeros_like(M, dtype=int)         # 0 = not escaped, 1/2/3 = basins
    active_mask = np.ones_like(M, dtype=bool)    # True = still evolving
    escape_steps = np.zeros_like(M, dtype=float) # steps until escape (0 if never escapes)

    sigma = 1.0
    dt = 0.1

    t0 = time.time()
    print("[Δ] Evolving trajectories...")

    # --- 3. Symplectic-ish leapfrog integration ---
    for step in range(1, max_steps + 1):

        # Gradients of effective potential
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)

        # Half-step momentum
        p_m_half = p_m - (dt / 2) * grad_m - (damping * p_m * dt / 2)
        p_l_half = p_l - (dt / 2) * grad_l - (damping * p_l * dt / 2)

        # Full-step position
        M = M + dt * p_m_half
        L = L + dt * p_l_half

        # New gradients at updated position
        grad_m_new = M + 2 * sigma * M * L
        grad_l_new = L + sigma * (M**2 - L**2)

        # Full-step momentum update
        p_m = p_m_half - (dt / 2) * grad_m_new - (damping * p_m_half * dt / 2)
        p_l = p_l_half - (dt / 2) * grad_l_new - (damping * p_l_half * dt / 2)

        # --- Escape check ---
        r2 = M**2 + L**2
        escaped_now = (r2 > escape_radius_sq) & active_mask

        if np.any(escaped_now):
            theta = np.arctan2(L[escaped_now], M[escaped_now])

            # Same angular split as basin_mapper_3:
            # teal (1):   theta in (0.5, 2.5)
            # red  (3):   |theta| > 2.5
            # gold (2):   remainder
            mask_e1 = (theta > 0.5) & (theta < 2.5)
            mask_e3 = np.abs(theta) > 2.5
            mask_e2 = ~(mask_e1 | mask_e3)

            current_status = status[escaped_now]
            current_status[mask_e1] = 1
            current_status[mask_e2] = 2
            current_status[mask_e3] = 3
            status[escaped_now] = current_status

            # record escape step for height
            escape_steps[escaped_now] = step

            # deactivate those trajectories
            active_mask[escaped_now] = False

        # Optional early stop if everything escaped:
        if not np.any(active_mask):
            print(f"[Δ] All trajectories escaped by step {step}.")
            break

    dt_sim = time.time() - t0
    print(f"[Δ] Integration complete in {dt_sim:.2f} s.")

    # Any still-active (non-escaped) points: treat as 'max' escape time
    escape_steps[active_mask] = max_steps

    # Height field: log-scale to bring out structure
    Z = np.log1p(escape_steps)

    return M, L, Z, status, (m_vals, l_vals)


# ============================================================
# Rotating 3D animation
# ============================================================

def make_rotating_3d_animation(
    filename="pirouette_manifold_spin.gif",
    resolution=500,
    zoom_factor=4.0,
    max_steps=1000,
    damping=0.0,
    elev=35,
    n_frames=360,
    fps=30,
):
    """
    Build the 3D escape-time manifold and save a rotating animation.

    Requires ffmpeg installed for .gif output, or switch to .gif + ImageMagick.
    """

    # Compute manifold
    M, L, Z, status, (m_vals, l_vals) = compute_escape_manifold(
        resolution=resolution,
        zoom_factor=zoom_factor,
        max_steps=max_steps,
        damping=damping,
    )

    print("[Δ] Building 3D surface...")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create the surface once; we only rotate the camera
    surf = ax.plot_surface(
        M,
        L,
        Z,
        rstride=2,
        cstride=2,
        linewidth=0,
        antialiased=False,
    )

    ax.set_xlabel("m (Mass Field)")
    ax.set_ylabel(r"$\lambda$ (Coupling Field)")
    ax.set_zlabel("log(escape steps + 1)")
    ax.set_title(f"Δ-field Escape-Time Manifold\nzoom={zoom_factor}x, steps={max_steps}")

    # Fix z-limits so they don't jump between frames
    ax.set_zlim(np.nanmin(Z), np.nanmax(Z))

    # Optional: show paper v9 box as a floating rectangle projected down at min(Z)
    z0 = np.nanmin(Z)
    box_x = np.array([-1.5,  1.5,  1.5, -1.5, -1.5])
    box_y = np.array([-1.0, -1.0,  2.0,  2.0, -1.0])
    ax.plot(box_x, box_y, z0, '--', alpha=0.5)

    # Initial view
    ax.view_init(elev=elev, azim=45)

    # Animation callbacks
    def init():
        ax.view_init(elev=elev, azim=45)
        return (surf,)

    def update(frame):
        azim = 45 + frame  # simple spin
        ax.view_init(elev=elev, azim=azim)
        return (surf,)

    print("[Δ] Creating animation...")
    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=n_frames,
        interval=1000 / fps,
        blit=False,
    )

    print(f"[Δ] Saving animation to {filename} ...")
    anim.save(filename, fps=fps, dpi=200)
    print("[Δ] Done.")

    plt.close(fig)


if __name__ == "__main__":
    # Tweak these as desired:
    make_rotating_3d_animation(
        filename="pirouette_manifold_spin.gif",
        resolution=500,
        zoom_factor=4.0,   # closer than the 10x deep field
        max_steps=1000,
        damping=0.0,
        elev=35,
        n_frames=360,
        fps=30,
    )
