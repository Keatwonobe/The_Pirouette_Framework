from matplotlib import animation
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
import time
import os
CACHE_PATH = "pirouette_manifold_cache.npz"

def compute_escape_manifold(
    resolution=500,
    zoom_factor=4.0,
    max_steps=1000,
    damping=0.0,
    escape_radius_sq=20.0,
    use_cache=True,
    cache_path=CACHE_PATH,
):
    """
    Run the Pirouette Δ-field integration and return:
      - M, L: 2D grids of (m, λ)
      - Z:    log(escape_time + 1) as 'height'
      - status: basin ID (0 = trapped, 1/2/3 = teal/gold/red)
      - (m_vals, l_vals): 1D axis arrays

    If use_cache is True and cache_path exists, loads from cache instead of recomputing.
    """

    # ---------- Try to load from cache ----------
    if use_cache and os.path.exists(cache_path):
        print(f"[Δ] Loading manifold from cache: {cache_path}")
        data = np.load(cache_path)
        M = data["M"]
        L = data["L"]
        Z = data["Z"]
        status = data["status"]
        m_vals = data["m_vals"]
        l_vals = data["l_vals"]
        return M, L, Z, status, (m_vals, l_vals)

    # ---------- Otherwise compute from scratch ----------
    print(f"[Δ] Computing escape manifold...")
    print(f"    resolution = {resolution}x{resolution}")
    print(f"    zoom_factor = {zoom_factor} | max_steps = {max_steps} | damping = {damping}")

    m_center, l_center = 0.0, 0.5
    m_span = 3.0 * zoom_factor
    l_span = 3.0 * zoom_factor

    m_vals = np.linspace(m_center - m_span / 2, m_center + m_span / 2, resolution)
    l_vals = np.linspace(l_center - l_span / 2, l_center + l_span / 2, resolution)
    M, L = np.meshgrid(m_vals, l_vals)

    p_m = np.zeros_like(M)
    p_l = np.zeros_like(L)

    status = np.zeros_like(M, dtype=int)
    active_mask = np.ones_like(M, dtype=bool)
    escape_steps = np.zeros_like(M, dtype=float)

    sigma = 1.0
    dt = 0.1

    import time
    t0 = time.time()
    print("[Δ] Evolving trajectories...")

    for step in range(1, max_steps + 1):
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)

        p_m_half = p_m - (dt / 2) * grad_m - (damping * p_m * dt / 2)
        p_l_half = p_l - (dt / 2) * grad_l - (damping * p_l * dt / 2)

        M = M + dt * p_m_half
        L = L + dt * p_l_half

        grad_m_new = M + 2 * sigma * M * L
        grad_l_new = L + sigma * (M**2 - L**2)

        p_m = p_m_half - (dt / 2) * grad_m_new - (damping * p_m_half * dt / 2)
        p_l = p_l_half - (dt / 2) * grad_l_new - (damping * p_l_half * dt / 2)

        r2 = M**2 + L**2

        bad = (~np.isfinite(M)) | (~np.isfinite(L)) | (~np.isfinite(r2))
        escaped_now = ((r2 > escape_radius_sq) | bad) & active_mask

        if np.any(escaped_now):
            theta = np.arctan2(
                np.where(escaped_now, L, 0.0)[escaped_now],
                np.where(escaped_now, M, 0.0)[escaped_now],
            )

            mask_e1 = (theta > 0.5) & (theta < 2.5)
            mask_e3 = np.abs(theta) > 2.5
            mask_e2 = ~(mask_e1 | mask_e3)

            current_status = status[escaped_now]
            current_status[mask_e1] = 1
            current_status[mask_e2] = 2
            current_status[mask_e3] = 3
            status[escaped_now] = current_status

            escape_steps[escaped_now] = step
            active_mask[escaped_now] = False

        if not np.any(active_mask):
            print(f"[Δ] All trajectories escaped by step {step}.")
            break

    dt_sim = time.time() - t0
    print(f"[Δ] Integration complete in {dt_sim:.2f} s.")

    escape_steps[active_mask] = max_steps
    Z = np.log1p(escape_steps)

    # ---------- Save to cache ----------
    if use_cache:
        print(f"[Δ] Saving manifold cache to {cache_path}")
        np.savez_compressed(
            cache_path,
            M=M,
            L=L,
            Z=Z,
            status=status,
            m_vals=m_vals,
            l_vals=l_vals,
        )

    return M, L, Z, status, (m_vals, l_vals)

def make_rotating_3d_animation(
    filename="pirouette_manifold_spin.mp4",
    resolution=500,
    zoom_factor=4.0,
    max_steps=1000,
    damping=0.0,
    elev=80,
    n_frames=360,
    fps=30,
    use_cache=True,
):
    """
    Build the 3D escape-time manifold and save a rotating animation.
    Manifold is cached to disk so failures in saving the animation
    don't cost you the simulation time.
    """

    # --- Load or compute manifold (this will cache if needed) ---
    M, L, escape_Z, status, (m_vals, l_vals) = compute_escape_manifold(
        resolution=resolution,
        zoom_factor=zoom_factor,
        max_steps=max_steps,
        damping=damping,
        use_cache=use_cache,
    )

    # --- Build height & colors (as before) ---
    steps = np.expm1(escape_Z)
    h = steps / max_steps
    h = np.clip(h, 0, 1)

    basin_cmap = ListedColormap([
        (0.0, 0.0, 0.0, 1.0),
        (0.0, 0.8, 0.8, 1.0),
        (0.9, 0.7, 0.1, 1.0),
        (0.9, 0.3, 0.1, 1.0),
    ])

    M = np.asarray(M, dtype=float)
    L = np.asarray(L, dtype=float)
    h = np.asarray(h, dtype=float)

    valid = np.isfinite(M) & np.isfinite(L) & np.isfinite(h)
    M[~valid] = np.nan
    L[~valid] = np.nan
    h[~valid] = 0.0
    status[~valid] = 0

    facecolors = basin_cmap(status)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(
        M,
        L,
        h,
        facecolors=facecolors,
        rstride=2,
        cstride=2,
        linewidth=0,
        antialiased=False,
        shade=False,
    )

    ax.set_xlim(M.min(), M.max())
    ax.set_ylim(L.min(), L.max())
    ax.set_zlim(0, 1.0)
    ax.set_box_aspect((M.ptp(), L.ptp(), 0.6))

    ax.set_xlabel("m (Mass Field)")
    ax.set_ylabel(r"$\lambda$ (Coupling Field)")
    ax.set_zlabel("normalized stability")
    ax.set_title(f"Δ-field Escape Manifold (overhead spin)\nzoom={zoom_factor}x")

    z0 = 0.0
    box_x = np.array([-1.5,  1.5,  1.5, -1.5, -1.5])
    box_y = np.array([-1.0, -1.0,  2.0,  2.0, -1.0])
    ax.plot(box_x, box_y, z0, "--", color="white", alpha=0.6)

    ax.view_init(elev=elev, azim=45)

    def init():
        ax.view_init(elev=elev, azim=45)
        return (surf,)

    def update(frame):
        azim = 45 + frame
        ax.view_init(elev=elev, azim=azim)
        return (surf,)

    print("[Δ] Creating overhead spin animation...")
    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=n_frames,
        interval=1000 / fps,
        blit=False,
    )

    # --- Save, but don't lose the manifold if writer fails ---
    try:
        print(f"[Δ] Saving animation to {filename} ...")
        anim.save(filename, fps=fps, dpi=200)
        print("[Δ] Done.")
    except Exception as e:
        print("[Δ] WARNING: animation writer failed:")
        print("    ", repr(e))
        print("    Manifold is cached in:", CACHE_PATH)
        print("    You can rerun with different filename / writer without recomputing.")

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
