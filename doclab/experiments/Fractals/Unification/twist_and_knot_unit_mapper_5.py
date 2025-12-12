import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.colors import ListedColormap
import datetime
import textwrap

# ============================================================
# CONSTANTS & CALIBRATION (From twist_unit_mapper.py)
# ============================================================
C = 299_792_458.0        # m/s
HBAR = 1.054_571_817e-34 # J*s

M_ELECTRON = 9.1093837015e-31
TAU_E_CAL = 5.06         # Electron calibrated twist

# Twist-Knottedness Scale Factor (Adjust this to tune K -> tau mapping)
TAU_SCALE = 10.0 

def run_calibration(tau_e_cal=TAU_E_CAL, m_e_ref=M_ELECTRON):
    """Establishes T0 using the electron mass and a calibration tau."""
    T0_cal = HBAR * tau_e_cal / (m_e_ref * C**2)
    print(f"**-> Calculated T₀ Constant: {T0_cal:.6e}** ")
    return T0_cal

# ------------------------------------------------------------------
# Twist substrate: brute-force 1D scan E_1:2:8(τ) on a dense grid
# ------------------------------------------------------------------
TARGET_128 = np.array([1.0/11.0, 2.0/11.0, 8.0/11.0])

def precompute_twist_error_curve(tau_min, tau_max, n_tau):
    """
    Brute-force the 1D twist landscape once.

    Returns:
        tau_vals: shape (n_tau,)
        E_vals:   shape (n_tau,)
    """
    tau_vals = np.linspace(tau_min, tau_max, n_tau)
    E_vals = np.zeros_like(tau_vals)

    for i, tau in enumerate(tau_vals):
        # FIX: The active error_128 returns a tuple (E, wG, wT, wR).
        # We must take only the first element [0], which is the error E.
        E_vals[i] = error_128(tau)[0] 
        # The previous line: E_vals[i] = error_128(tau) caused the ValueError.

    return tau_vals, E_vals

# Line 69
def compute_knottedness_from_initial(
    x0,
    y0,
    px0,             # <-- Added
    py0,
    m=1.0,
    lam=1.0,
    E_hh=0.1767,          # same energy you used before (Henon–Heiles)
    t_max=200.0,
    n_samples=500,
):
    """
    Convenience wrapper: reproduce the 'old' knottedness K(x0, y0).
    ...
    """

    # Unpack all four results: K, E_128, tau, escaped
    K, _, _, escaped = compute_K_and_E128(
        x0, y0,
        px0, py0,
        m, lam,
        E_hh,
        t_max,
        n_samples,
    )
    # The calling function (scan_knottedness_only) expects two return values: K and escaped
    return K, escaped


# ============================================================
# 1. HÉNON–HEILES MANIFOLD (THE ARENA - From knottedness_2.py)
# ============================================================

def potential(x, y, lam):
    """Hénon–Heiles potential."""
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1.0 / 3.0) * y**3)

def equations_of_motion(t, state, m, lam):
    """Hamiltonian equations for Hénon–Heiles."""
    x, y, px, py = state
    Fx = -x - 2.0 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    vx = px / m
    vy = py / m
    return [vx, vy, Fx, Fy]

# ============================================================
# 2. KNOTTEDNESS (K) CALCULATION (From knottedness_2.py)
# ============================================================

def compute_knottedness_from_trajectory(t, states, lam, eps=1e-12):
    """
    Compute approximate knottedness K from trajectory history.
    K = (Sum V * kappa * dt) / (Sum V * dt)
    """
    x, y, px, py = states[0], states[1], states[2], states[3]
    vx, vy = px, py # m=1 used in integration

    dt = np.diff(t)
    if len(dt) == 0: return 0.0
    dt = np.append(dt, dt[-1])

    # Approximate accelerations (central differencing where possible)
    ax, ay = np.zeros_like(x), np.zeros_like(y)
    if len(t) > 2:
        ax[1:-1] = (vx[2:] - vx[:-2]) / (t[2:] - t[:-2] + eps)
        ay[1:-1] = (vy[2:] - vy[:-2]) / (t[2:] - t[:-2] + eps)

    # Curvature of the spatial path (kappa)
    v2 = vx**2 + vy**2
    speed = np.sqrt(v2) + eps
    num = np.abs(vx * ay - vy * ax)
    kappa = num / (speed**3 + eps)

    # Delta proxy: potential energy magnitude
    V = np.abs(potential(x, y, lam))

    I_delta = np.sum(V * dt)         # total Δ-weight
    T_delta = np.sum(V * kappa * dt) # Δ-weighted twisting

    if I_delta <= 0: return 0.0

    K = T_delta / (I_delta + eps)
    return float(K)

def scan_knottedness_only(
    x_min=-2.0, x_max=2.0,
    y_min=-2.0, y_max=2.0,
    RES=256,
    lam=1.0,
    E_HH=0.1767,
    t_max=500.0,
    n_samples=2000
):
    """
    Brute-force HH manifold, compute K(x0,y0) everywhere, no twist yet.
    Returns:
        X, Y     : meshgrids
        K_map    : knottedness (NaN outside the HH wedge / escaped)
        forbidden: boolean mask of forbidden points
    """
    xs = np.linspace(x_min, x_max, RES)
    ys = np.linspace(y_min, y_max, RES)
    X, Y = np.meshgrid(xs, ys)

    K_map = np.full((RES, RES), np.nan, dtype=float)
    forbidden = np.zeros((RES, RES), dtype=bool)

    m = 1.0
    px0 = 0.0
    py0 = 0.0

    for i in range(RES):
        for j in range(RES):
            x0 = X[i, j]
            y0 = Y[i, j]

            # --- Hénon–Heiles energy check (same as before) ---
            V0 = potential(x0, y0, lam)
            if V0 > E_HH:
                forbidden[i, j] = True
                continue

            KE = E_HH - V0
            if KE <= 0:
                forbidden[i, j] = True
                continue

            py0 = np.sqrt(2.0 * m * KE)

            # --- integrate HH orbit & compute knottedness K ---
            K, escaped = compute_knottedness_from_initial(
                x0, y0, px0, py0,
                lam=lam, E_hh=E_HH,
                t_max=t_max, n_samples=n_samples
            )

            if escaped:
                forbidden[i, j] = True
            else:
                K_map[i, j] = K

    return X, Y, K_map, forbidden


# ============================================================
# 3. TWIST CLOCK & ERROR (From twist_unit_mapper.py)
# ============================================================

def sector_weights(tau, ring_radius=2.2, n_angles=360, t_max=5000, dt=0.01):
    """Evolve particle and return time-averaged sector weights (G, T, R)."""
    n_steps = int(t_max / dt)
    theta = 0.0
    wG = wT = wR = 0.0
    sector_count = 0
    for _ in range(n_steps):
        # nonlinear twist evolution law
        dtheta = tau * np.sin(theta) * dt
        theta += dtheta
        theta = (theta + np.pi) % (2*np.pi) - np.pi # wrap to [-pi, pi]

        # sector accumulation
        if -np.pi/3 <= theta <= np.pi/3:
            wG += 1
        elif theta > np.pi/3:
            wT += 1
        else:
            wR += 1
        sector_count += 1
    return wG/sector_count, wT/sector_count, wR/sector_count

def error_128(tau, **kwargs):
    """Calculates the L2-norm squared error against the 1:2:8 target."""
    target = np.array([1/11, 2/11, 8/11])
    w = np.array(sector_weights(tau, **kwargs))
    E = np.linalg.norm(w - target)**2
    return E, w[0], w[1], w[2]

# ============================================================
# 4. THE BRIDGE: KNOTTEDNESS -> TWIST ERROR
# ============================================================

def compute_K_and_E128(x0, y0, px0, py0, m, lam, E_hh, t_max, n_samples):
    """
    Integrate Hénon-Heiles, compute K, and map to 1:2:8 error E_128.
    """
    r_escape = 5.0
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

    # Compute Knottedness K from the sampled trajectory
    K = compute_knottedness_from_trajectory(sol.t, sol.y, lam)

    # Map K to Twist tau (The Core Hypothesis)
    tau = K * TAU_SCALE
    
    # Compute 1:2:8 Error
    E_128, *weights = error_128(tau)

    return K, E_128, tau, len(sol.t_events[0]) > 0 # K, E_128, tau, escaped

# ============================================================
# 5. GRID SCANNER (2D MANIFOLD SAMPLER)
# ============================================================

def scan_twist_error_manifold(m=1.0,
                              lam=1.0,
                              E_hh=1.0/6.0 + 0.01,
                              XY_LIMITS=(-2.0, 2.0, -2.0, 2.0),
                              RES=100,
                              t_max=200.0,
                              n_samples=200):
    """
    Scans the (x0, y0) grid with constant energy E_hh.
    Returns: xs, ys, E_map (1:2:8 error), K_map (knottedness).
    """
    x_min, x_max, y_min, y_max = XY_LIMITS
    xs = np.linspace(x_min, x_max, RES)
    ys = np.linspace(y_min, y_max, RES)

    E_map = np.zeros((RES, RES), dtype=float)
    K_map = np.zeros((RES, RES), dtype=float)
    forbidden = np.zeros((RES, RES), dtype=bool)

    total = RES * RES
    print(f"Scanning 2D Twist-Error Manifold {RES}x{RES}...")

    for i, y0 in enumerate(ys):
        for j, x0 in enumerate(xs):
            # 1. Compute potential and check forbidden region
            V0 = potential(x0, y0, lam)
            
            if V0 > E_hh:
                forbidden[i, j] = True
                E_map[i, j] = np.nan
                K_map[i, j] = np.nan
                continue

            # 2. Compute initial momentum py0 (px0=0 for simplicity)
            KE = E_hh - V0
            if KE <= 0:
                forbidden[i, j] = True
                E_map[i, j] = np.nan
                K_map[i, j] = np.nan
                continue

            py0 = np.sqrt(2.0 * KE)
            px0 = 0.0

            # 3. Integrate, compute K, and map to E_128
            K, E_128, tau, escaped = compute_K_and_E128(
                x0, y0, px0, py0,
                m=m, lam=lam, E_hh=E_hh,
                t_max=t_max,
                n_samples=n_samples
            )
            
            E_map[i, j] = E_128
            K_map[i, j] = K

        if (i * RES) % (max(total // 10, 1)) == 0:
            print(f"  Progress: {100.0 * i * RES / total:5.1f}%")

    print("Scan complete.")
    return xs, ys, E_map, K_map, forbidden

# ============================================================
# 6. VISUALIZATIONS
# ============================================================

def plot_2d_maps(xs, ys, E_map, K_map, forbidden, meta, save_path=None):
    """
    Two-panel figure:
      - left: Knottedness K(x0, y0)
      - right: Twist Error E_128(x0, y0)
    """
    
    x_min, x_max, y_min, y_max = meta.get("xy_limits", (-2.0, 2.0, -2.0, 2.0))
    lam = meta.get("lam", 1.0)
    E_hh = meta.get("E_hh", 1.0/6.0 + 0.01)
    
    title_suffix = f" (λ={lam}, $E_{{HH}}$={E_hh:.4f}, $\\tau$ Scale={TAU_SCALE:.1f})"

    # Flip vertically so y increases upward in image
    K_img = np.flipud(K_map)
    E_img = np.flipud(E_map)
    forbidden_img = np.flipud(forbidden)

    # Mask forbidden region as NaN so it's transparent
    K_plot = K_img.copy().astype(float)
    K_plot[forbidden_img] = np.nan
    E_plot = E_img.copy().astype(float)
    E_plot[forbidden_img] = np.nan

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    axKnot, axError = axes

    # ---------- Knottedness plot (K) ----------
    K_max = np.nanpercentile(K_plot, 99)
    if not np.isfinite(K_max) or K_max <= 0: K_max = 1.0

    im0 = axKnot.imshow(
        K_plot,
        extent=(x_min, x_max, y_min, y_max),
        origin="lower",
        cmap="viridis",
        vmin=0.0,
        vmax=K_max,
        interpolation="nearest"
    )

    axKnot.set_title("Manifold Knottedness $K(x_0, y_0)$" + title_suffix)
    axKnot.set_xlabel("$x_0$")
    axKnot.set_ylabel("$y_0$")
    fig.colorbar(im0, ax=axKnot, fraction=0.046, pad=0.04, label="$K$")
    
    # ---------- Twist Error plot (E_128) ----------
    E_min = np.nanmin(E_plot)
    E_max = np.nanpercentile(E_plot, 99)
    if not np.isfinite(E_max) or E_max <= E_min: E_max = E_min + 1e-4

    im1 = axError.imshow(
        E_plot,
        extent=(x_min, x_max, y_min, y_max),
        origin="lower",
        cmap="magma_r", # Reversed magma: low error is bright (resonant)
        vmin=E_min,
        vmax=E_max,
        interpolation="nearest"
    )

    axError.set_title("Twist Error $E_{1:2:8}(\\tau = K \cdot \text{scale})$" + title_suffix)
    axError.set_xlabel("$x_0$")
    axError.set_ylabel("$y_0$")
    fig.colorbar(im1, ax=axError, fraction=0.046, pad=0.04, label="$E_{1:2:8}$")

    plt.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=200, bbox_inches="tight")
        print(f"[SAVE] Figure saved to {save_path}")
        plt.close(fig)
    else:
        plt.show()

# ============================================================
# 7. MAIN EXECUTION
# ============================================================

def main():
    print("[#] 2D Knottedness-Twist Error Manifold Scanner")
    
    # 1. Calibrate T0 (used implicitly for reference, not in the map itself)
    T0_cal = run_calibration()

    # --- Scanner Settings ---
    RES = 100               # Grid resolution (e.g., 50x50, 100x100)
    E_HH = 1.0/6.0 + 0.01   # Hénon-Heiles energy
    T_MAX = 100.0           # Max integration time
    N_SAMPLES = 100         # Samples per trajectory
    XY_LIMITS = (-2.0, 2.0, -2.0, 2.0)

    # 2. Run the 2D scan
    xs, ys, E_map, K_map, forbidden = scan_twist_error_manifold(
        lam=1.0,
        E_hh=E_HH,
        XY_LIMITS=XY_LIMITS,
        RES=RES,
        t_max=T_MAX,
        n_samples=N_SAMPLES,
    )
    
    # 3. Plot the results
    meta = {
        "lam": 1.0,
        "E_hh": E_HH,
        "xy_limits": XY_LIMITS,
        "res": RES,
    }
    
    out_file = f"twist_error_map_R{RES}_E{E_HH:.4f}.png"
    plot_2d_maps(xs, ys, E_map, K_map, forbidden, meta, save_path=out_file)
    print(f"\nSaved 2D map to '{out_file}'.")


if __name__ == "__main__":
    # ------------------------------
    # 1) Build the twist substrate
    # ------------------------------
    TAU_MIN = 0.0
    TAU_MAX = 100.0      # make this big enough to cover K*TAU_SCALE
    N_TAU   = 2000

    print("[Twist] Precomputing E_1:2:8(τ)...")
    tau_vals, E_vals = precompute_twist_error_curve(TAU_MIN, TAU_MAX, N_TAU)

    # ------------------------------
    # 2) Scan HH manifold for K(x,y)
    # ------------------------------
    print("[HH] Scanning manifold for knottedness K(x0,y0)...")
    X, Y, K_map, forbidden = scan_knottedness_only(
        x_min=-2.0, x_max=2.0,
        y_min=-2.0, y_max=2.0,
        RES=256,
        lam=1.0,
        E_HH=0.1767,
        t_max=500.0,
        n_samples=2000
    )

    # ------------------------------
    # 3) Map K -> τ -> E(τ) with arrays
    # ------------------------------
    TAU_SCALE = 10.0      # your old τ = K * scale mapping

    tau_map = K_map * TAU_SCALE

    # clamp into the tabulated τ range
    tau_map_clipped = np.clip(tau_map, TAU_MIN, TAU_MAX)

    # vectorized lookup: one np.interp for the whole manifold
    E_map = np.interp(
        tau_map_clipped.ravel(),
        tau_vals,
        E_vals
    ).reshape(K_map.shape)

    # mask out forbidden / escaped points
    E_map[forbidden] = np.nan

    # ------------------------------
    # 4) Plot K and E side by side
    # ------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    im1 = ax1.imshow(
        K_map,
        origin="lower",
        extent=[-2, 2, -2, 2],
        cmap="viridis"
    )
    ax1.set_title("Manifold Knottedness K(x0, y0)")
    ax1.set_xlabel("x0")
    ax1.set_ylabel("y0")
    fig.colorbar(im1, ax=ax1, label="K")

    im2 = ax2.imshow(
        E_map,
        origin="lower",
        extent=[-2, 2, -2, 2],
        cmap="magma"
    )
    ax2.set_title("Twist Error E₁:₂:₈(τ = K·scale)")
    ax2.set_xlabel("x0")
    fig.colorbar(im2, ax=ax2, label="E₁:₂:₈")

    plt.tight_layout()
    plt.savefig("twist_error_map_bruteforce.png", dpi=200)
    plt.close(fig)

    print("[✓] Saved 'twist_error_map_bruteforce.png'")
