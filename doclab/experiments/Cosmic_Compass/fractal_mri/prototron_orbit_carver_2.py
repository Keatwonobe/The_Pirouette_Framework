"""
GPU-accelerated 'prototron' orbit tracer for the Entropy Anchor manifold.

- Uses CuPy if available, otherwise falls back to NumPy.
- Reuses the Hénon–Heiles gradient used in entropy_anchor.py / reverse_lyapunov.py
- Evolves many trajectories in parallel and builds a (M, L) density map.

You can tune:
    N_TRAJ, N_STEPS, DT, GAMMA, BOUNDS, and init_prototrons()
to explore different regimes.

"""

import numpy as _np

try:
    import cupy as _cp
    xp = _cp
    USE_GPU = True
    print("[prototron] Using CuPy (GPU)")
except ImportError:
    xp = _np
    USE_GPU = False
    print("[prototron] CuPy not found, falling back to NumPy (CPU)")

import matplotlib.pyplot as plt


# -----------------------------
#   Dynamics: Hénon–Heiles grad
# -----------------------------

def henon_heiles_grad(M, L):
    """
    Gradient of the Hénon–Heiles potential used in the Entropy Anchor:
        dV/dM = M + 2 M L
        dV/dL = L + M^2 - 2 L^2
    M, L can be xp arrays.
    """
    dM = M + 2.0 * M * L
    dL = L + M**2 - 2.0 * L**2
    return dM, dL


def step_dynamics(state, dt, gamma=0.02, bounds=1.5):
    """
    One RK2-style step of the dynamics for a whole batch of prototrons.

    state: (N, 4) array: [M, L, vM, vL]
    """
    M = state[:, 0]
    L = state[:, 1]
    vM = state[:, 2]
    vL = state[:, 3]

    # --- drift + kick (semi-implicit-ish RK2) ---
    # gradient at current position
    gM, gL = henon_heiles_grad(M, L)

    # half-step velocities (damped)
    vM_half = vM + dt * (-gM - gamma * vM) * 0.5
    vL_half = vL + dt * (-gL - gamma * vL) * 0.5

    # half-step positions
    M_half = M + dt * vM_half * 0.5
    L_half = L + dt * vL_half * 0.5

    # gradient at half-step
    gM_half, gL_half = henon_heiles_grad(M_half, L_half)

    # full-step velocities
    vM_new = vM + dt * (-gM_half - gamma * vM_half)
    vL_new = vL + dt * (-gL_half - gamma * vL_half)

    # full-step positions
    M_new = M + dt * vM_new
    L_new = L + dt * vL_new

    # soft bounding box reflection to keep them in the viewport
    # (you can replace this with your triangle mask if you like)
    mask_M_hi = M_new > bounds
    mask_M_lo = M_new < -bounds
    mask_L_hi = L_new > bounds
    mask_L_lo = L_new < -bounds

    if mask_M_hi.any():
        M_new = xp.where(mask_M_hi, bounds - (M_new - bounds), M_new)
        vM_new = xp.where(mask_M_hi, -0.5 * vM_new, vM_new)
    if mask_M_lo.any():
        M_new = xp.where(mask_M_lo, -bounds - (M_new + bounds), M_new)
        vM_new = xp.where(mask_M_lo, -0.5 * vM_new, vM_new)

    if mask_L_hi.any():
        L_new = xp.where(mask_L_hi, bounds - (L_new - bounds), L_new)
        vL_new = xp.where(mask_L_hi, -0.5 * vL_new, vL_new)
    if mask_L_lo.any():
        L_new = xp.where(mask_L_lo, -bounds - (L_new + bounds), L_new)
        vL_new = xp.where(mask_L_lo, -0.5 * vL_new, vL_new)

    out = xp.stack([M_new, L_new, vM_new, vL_new], axis=1)
    return out


# -----------------------------
#   Initial conditions
# -----------------------------

def init_prototrons(n_traj=8192, jitter=0.01, seed=1234):
    """
    Three 'color' prototrons, fanned out with small noise.

    Vertices chosen to roughly match the central triangular anchor
    you see in the anchor / jet plots.

    Returns: (N, 4) xp-array with [M, L, vM, vL]
    """
    rng = _np.random.default_rng(seed)

    # Triangle vertices in (M, L)
    v0 = _np.array([0.0, 0.60])
    v1 = _np.array([0.50, -0.30])
    v2 = _np.array([-0.50, -0.30])
    verts = _np.stack([v0, v1, v2], axis=0)

    # Allocate slots and tile vertices
    idx = _np.arange(n_traj) % 3
    base_pos = verts[idx]

    # Add small isotropic jitter in position
    noise_pos = rng.normal(scale=jitter, size=(n_traj, 2))
    M0L0 = base_pos + noise_pos

    # Small initial tangential velocities around the triangle
    # (rotate vector from center by +90° and scale)
    center = _np.array([0.0, 0.0])
    d = M0L0 - center
    # rotate (dx, dy) -> (-dy, dx)
    v_tan = _np.stack([-d[:, 1], d[:, 0]], axis=1)
    # normalize and scale
    v_norm = _np.linalg.norm(v_tan, axis=1, keepdims=True) + 1e-9
    v_tan = 0.2 * v_tan / v_norm

    state0 = _np.concatenate([M0L0, v_tan], axis=1)
    state0 = xp.asarray(state0, dtype=xp.float32)
    return state0


# -----------------------------
#   Main simulation
# -----------------------------

def run_prototron_web(
    n_traj=8192,
    n_steps=4000,
    dt=0.01,
    gamma=0.02,
    bounds=1.5,
    grid_res=1024,
):
    """
    Evolve many prototrons, accumulate a 2D density on (M, L).

    Returns:
        density: (grid_res, grid_res) numpy array (for plotting),
        extent:  [M_min, M_max, L_min, L_max]
    """
    state = init_prototrons(n_traj=n_traj)
    state = state.astype(xp.float32)

    # Pre-allocate trail buffers on GPU/CPU
    # (you can downsample or store every k-th step if memory is tight)
    M_trail = xp.empty((n_steps, n_traj), dtype=xp.float32)
    L_trail = xp.empty_like(M_trail)

    for t in range(n_steps):
        state = step_dynamics(state, dt=dt, gamma=gamma, bounds=bounds)
        M_trail[t] = state[:, 0]
        L_trail[t] = state[:, 1]

    # Flatten to a big cloud of points
    M_flat = M_trail.ravel()
    L_flat = L_trail.ravel()

    # Move back to CPU for histogramming & plotting
    if USE_GPU:
        M_flat = _cp.asnumpy(M_flat)
        L_flat = _cp.asnumpy(L_flat)

    # Build histogram over the same bounds as your other plots
    M_min, M_max = -bounds, bounds
    L_min, L_max = -bounds, bounds

    H, xedges, yedges = _np.histogram2d(
        M_flat, L_flat,
        bins=grid_res,
        range=[[M_min, M_max], [L_min, L_max]]
    )

    # Normalize
    H_lin = H / H.max()
    H_log = _np.log10(H + 1.0)  # to see faint trails

    extent = [M_min, M_max, L_min, L_max]
    return H_lin, H_log, extent


def main():
    H_lin, H_log, extent = run_prototron_web(
        n_traj=12000,
        n_steps=5000,
        dt=0.008,
        gamma=0.03,
        bounds=1.5,
        grid_res=1024,
    )

    M_min, M_max, L_min, L_max = extent

    fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    ax0, ax1 = axs

    im0 = ax0.imshow(
        H_lin.T,
        origin="lower",
        extent=extent,
        aspect="equal",
        cmap="viridis",
    )
    ax0.set_title("Prototron Trail Density (linear)")
    ax0.set_xlabel("M (lateral)")
    ax0.set_ylabel("L (axial)")
    fig.colorbar(im0, ax=ax0)

    im1 = ax1.imshow(
        H_log.T,
        origin="lower",
        extent=extent,
        aspect="equal",
        cmap="viridis",
    )
    ax1.set_title("Prototron Trail Density (log10)")
    ax1.set_xlabel("M (lateral)")
    ax1.set_ylabel("L (axial)")
    fig.colorbar(im1, ax=ax1)

    plt.suptitle("Orbit-Carved Web from Three Prototrons", fontsize=14)
    plt.show()


if __name__ == "__main__":
    main()
