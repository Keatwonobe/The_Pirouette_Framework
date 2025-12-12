import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.colors import ListedColormap

# ============================================================
# 1. HÉNON–HEILES MANIFOLD (THE ARENA)
# ============================================================

def potential(x, y, lam):
    """
    Hénon–Heiles potential.
    V(x, y) = 1/2 (x^2 + y^2) + lam (x^2 y - y^3 / 3)
    """
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1.0 / 3.0) * y**3)

def equations_of_motion(t, state, m, lam):
    """
    Hamiltonian equations for Hénon–Heiles.

    state = [x, y, px, py]
    """
    x, y, px, py = state

    # Force = -∇V
    Fx = -x - 2.0 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)

    vx = px / m
    vy = py / m

    return [vx, vy, Fx, Fy]

# ============================================================
# 2. KNOTTEDNESS ALONG A SINGLE TRAJECTORY
# ============================================================

def compute_knottedness_from_trajectory(t, states, lam, eps=1e-12):
    """
    Given time array t and state array states[:, i] = (x, y, px, py) at t[i],
    compute an approximate knottedness K.

    Implementation:
    - Use curvature of (x(t), y(t)) as a measure of "twist".
    - Weight curvature by |V(x,y)| as a proxy for Δ.
    """

    x = states[0]
    y = states[1]
    px = states[2]
    py = states[3]

    # Velocities
    vx = px  # m=1 in these units
    vy = py

    # First time derivative of positions (already vx, vy),
    # second derivative from finite differences
    # (we could also recompute forces, but this keeps it self-contained in time samples)
    dt = np.diff(t)
    dt = np.append(dt, dt[-1])  # last step ~ previous

    # Approximate accelerations (central differences where possible)
    ax = np.zeros_like(x)
    ay = np.zeros_like(y)

    # interior points
    ax[1:-1] = (vx[2:] - vx[:-2]) / (t[2:] - t[:-2])
    ay[1:-1] = (vy[2:] - vy[:-2]) / (t[2:] - t[:-2])

    # endpoints (forward/backward difference)
    ax[0] = (vx[1] - vx[0]) / (t[1] - t[0] + eps)
    ay[0] = (vy[1] - vy[0]) / (t[1] - t[0] + eps)
    ax[-1] = (vx[-1] - vx[-2]) / (t[-1] - t[-2] + eps)
    ay[-1] = (vy[-1] - vy[-2]) / (t[-1] - t[-2] + eps)

    # Curvature of the spatial path
    v2 = vx**2 + vy**2
    speed = np.sqrt(v2) + eps
    # |x' y'' - y' x''| / |v|^3
    num = np.abs(vx * ay - vy * ax)
    kappa = num / (speed**3 + eps)

    # Our Δ proxy: potential energy magnitude
    V = np.abs(potential(x, y, lam))

    # Time-step array for integration
    # (we'll treat dt as piecewise, same length as arrays)
    dt = np.asarray(dt)

    I_delta = np.sum(V * dt)        # total Δ-weight
    T_delta = np.sum(V * kappa * dt)  # Δ-weighted twisting

    if I_delta <= 0:
        return 0.0

    K = T_delta / (I_delta + eps)
    return float(K)

# ============================================================
# 3. SINGLE SHOT INTEGRATION (WITH ESCAPE + KNOTTEDNESS)
# ============================================================

def integrate_trajectory(x0, y0, px0, py0, m, lam,
                         t_max=200.0, r_escape=5.0,
                         n_samples=200):
    """
    Integrate one trajectory and return:
    - exit_id (0 = trapped, 1–3 = escapes into each sector)
    - knottedness K
    """

    r_esc_sq = r_escape**2

    def escape_event(t, state, *args):
        x, y, px, py = state
        return x * x + y * y - r_esc_sq

    escape_event.terminal = True
    escape_event.direction = 1

    # Time samples along trajectory for knottedness
    t_eval = np.linspace(0.0, t_max, n_samples)

    sol = solve_ivp(
        equations_of_motion,
        t_span=(0.0, t_max),
        y0=[x0, y0, px0, py0],
        args=(m, lam),
        events=escape_event,
        t_eval=t_eval,
        rtol=1e-7,
        atol=1e-9,
    )

    # Compute knottedness from the sampled trajectory we have (even if it escaped early)
    K = compute_knottedness_from_trajectory(sol.t, sol.y, lam)

    # Did it escape?
    escaped = len(sol.t_events[0]) > 0

    if escaped:
        x_end = sol.y[0, -1]
        y_end = sol.y[1, -1]

        angle = np.arctan2(y_end, x_end) % (2.0 * np.pi)
        sector = int(angle // (2.0 * np.pi / 3.0)) + 1  # 1,2,3
        return sector, K
    else:
        # Trapped / residue
        return 0, K

# ============================================================
# 4. GRID SCANNER (2D MANIFOLD SAMPLER)
# ============================================================

def scan_manifold(m=1.0,
                  lam=1.0,
                  E=1.0/6.0 + 0.01,
                  XY_LIMITS=(-2.0, 2.0, -2.0, 2.0),
                  RES=200,
                  t_max=200.0,
                  r_escape=5.0,
                  n_samples=200):
    """
    For a grid of initial positions (x0, y0) with energy E,
    choose initial momenta so that total energy is E and scan:

        - exit id (0..3)
        - knottedness K

    Returns:
        exit_map, K_map, mask_forbidden
    """

    x_min, x_max, y_min, y_max = XY_LIMITS
    xs = np.linspace(x_min, x_max, RES)
    ys = np.linspace(y_min, y_max, RES)

    exit_map = np.zeros((RES, RES), dtype=int)
    K_map = np.zeros((RES, RES), dtype=float)
    forbidden = np.zeros((RES, RES), dtype=bool)

    total = RES * RES
    count = 0
    print(f"Scanning manifold {RES}x{RES} ...")

    for i, y0 in enumerate(ys):
        for j, x0 in enumerate(xs):
            count += 1
            if count % (total // 10 or 1) == 0:
                print(f"  Progress: {100.0 * count / total:5.1f}%")

            # Compute potential at (x0, y0)
            V0 = potential(x0, y0, lam)

            if V0 > E:
                # Classically forbidden region for this energy
                forbidden[i, j] = True
                exit_map[i, j] = -1  # mark special
                K_map[i, j] = 0.0
                continue

            # Simple choice: start with px0 = 0, and choose py0 from energy
            # E = 1/2 (px^2 + py^2) + V0
            KE = E - V0
            py0 = np.sqrt(2.0 * KE)
            px0 = 0.0

            exit_id, K = integrate_trajectory(
                x0, y0, px0, py0,
                m=m, lam=lam,
                t_max=t_max,
                r_escape=r_escape,
                n_samples=n_samples
            )

            exit_map[i, j] = exit_id
            K_map[i, j] = K

    return xs, ys, exit_map, K_map, forbidden

# ============================================================
# 5. VISUALIZATION
# ============================================================

def plot_results(xs, ys, exit_map, K_map, forbidden,
                 XY_LIMITS, title_suffix=""):
    """
    Make a two-panel figure:
      - left: exit basin structure
      - right: knottedness (with residue colored by final K)
    """

    RES = exit_map.shape[0]

    # Flip vertically so y increases upward in image
    exits_img = np.flipud(exit_map)
    K_img = np.flipud(K_map)
    forbidden_img = np.flipud(forbidden)

    x_min, x_max, y_min, y_max = XY_LIMITS

    fig, axes = plt.subplots(1, 2, figsize=(14, 7), facecolor="black")
    axBasin, axKnot = axes

    # ---------- Basin plot ----------
    axBasin.set_facecolor("black")
    # Map: -1 = forbidden (gray), 0 = trapped (black), 1..3 = different colors
    basin_cmap = ListedColormap([
        "dimgray",  # index 0: we won't use this, but needed
        "black",    # 1: trapped (we'll remap indices)
        "red",      # 2: exit 1
        "green",    # 3: exit 2
        "blue"      # 4: exit 3
    ])

    # Build an index image: 1 = trapped, 2..4 = exits, 0 = forbidden
    basin_index = np.zeros_like(exits_img, dtype=int)
    basin_index[forbidden_img] = 0
    basin_index[exits_img == 0] = 1
    basin_index[exits_img == 1] = 2
    basin_index[exits_img == 2] = 3
    basin_index[exits_img == 3] = 4

    im0 = axBasin.imshow(
        basin_index,
        extent=(x_min, x_max, y_min, y_max),
        origin="lower",
        cmap=basin_cmap,
        interpolation="nearest"
    )

    axBasin.set_title("Exit Basins + Trapped Region" + title_suffix,
                      color="white")
    axBasin.set_xlabel("x", color="white")
    axBasin.set_ylabel("y", color="white")
    axBasin.tick_params(colors="white")

    # ---------- Knottedness plot ----------
    axKnot.set_facecolor("black")

    # Mask forbidden region as NaN so it's transparent
    K_plot = K_img.copy().astype(float)
    K_plot[forbidden_img] = np.nan

    # Normalize knottedness for color scaling
    K_max = np.nanpercentile(K_plot, 99)  # robust upper limit
    if K_max <= 0:
        K_max = 1.0

    im1 = axKnot.imshow(
        K_plot,
        extent=(x_min, x_max, y_min, y_max),
        origin="lower",
        cmap="magma",
        vmin=0.0,
        vmax=K_max,
        interpolation="nearest"
    )

    axKnot.set_title("Knottedness K (Residue colored by final K)" + title_suffix,
                     color="white")
    axKnot.set_xlabel("x", color="white")
    axKnot.set_ylabel("y", color="white")
    axKnot.tick_params(colors="white")

    cbar = fig.colorbar(im1, ax=axKnot, fraction=0.046, pad=0.04)
    cbar.set_label("K", color="white")
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.get_yticklabels(), color="white")

    plt.tight_layout()
    plt.show()

# ============================================================
# 6. MAIN
# ============================================================

if __name__ == "__main__":
    # Parameters you can play with
    MASS = 1.0
    LAMBDA = 1.0
    E_SADDLE = 1.0 / 6.0     # saddle energy for lam=1
    ENERGY = E_SADDLE + 0.01 # just above escape threshold

    XY_LIMITS = (-2.0, 2.0, -2.0, 2.0)
    RES = 200

    T_MAX = 200.0
    R_ESCAPE = 5.0
    N_SAMPLES = 250

    xs, ys, exit_map, K_map, forbidden = scan_manifold(
        m=MASS,
        lam=LAMBDA,
        E=ENERGY,
        XY_LIMITS=XY_LIMITS,
        RES=RES,
        t_max=T_MAX,
        r_escape=R_ESCAPE,
        n_samples=N_SAMPLES,
    )

    plot_results(xs, ys, exit_map, K_map, forbidden,
                 XY_LIMITS,
                 title_suffix=f"\n(λ={LAMBDA}, E={ENERGY:.4f})")
