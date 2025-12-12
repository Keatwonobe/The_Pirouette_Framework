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

def compute_knottedness_and_strain_from_trajectory(t, states, lam, eps=1e-12):
    """
    Compute approximate knottedness K and curvature-strain S
    from trajectory history.

    K  = (Σ V * κ * dt) / (Σ V * dt)
    S² = (Σ V * (κ - K)² * dt) / (Σ V * dt)
    """
    x, y, px, py = states[0], states[1], states[2], states[3]
    vx, vy = px, py  # m=1 used in integration

    dt = np.diff(t)
    if len(dt) == 0:
        return 0.0, 0.0
    dt = np.append(dt, dt[-1])

    # Approximate accelerations (central differencing)
    ax, ay = np.zeros_like(x), np.zeros_like(y)
    if len(t) > 2:
        ax[1:-1] = (vx[2:] - vx[:-2]) / (t[2:] - t[:-2] + eps)
        ay[1:-1] = (vy[2:] - vy[:-2]) / (t[2:] - t[:-2] + eps)

    # Curvature κ of spatial path
    v2 = vx**2 + vy**2
    speed = np.sqrt(v2) + eps
    num = np.abs(vx * ay - vy * ax)
    kappa = num / (speed**3 + eps)

    # Δ-proxy: potential energy magnitude
    V = np.abs(potential(x, y, lam))

    I_delta = np.sum(V * dt)           # total Δ-weight
    if I_delta <= 0:
        return 0.0, 0.0

    # Δ-weighted mean curvature (your original K)
    T_delta = np.sum(V * kappa * dt)
    K = T_delta / (I_delta + eps)

    # Δ-weighted variance → strain
    var_num = np.sum(V * (kappa - K)**2 * dt)
    S = np.sqrt(var_num / (I_delta + eps))

    return float(K), float(S)


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
    Integrate Hénon-Heiles, compute K and strain S, and map to 1:2:8 error E_128.
    """
    r_escape = 5.0
    r_esc_sq = r_escape**2

    def escape_event(t, state, *args):
        x, y, px, py = state
        return x * x + y * y - r_esc_sq
    escape_event.terminal = True
    escape_event.direction = 1

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

    # NEW: knottedness + strain
    K, S = compute_knottedness_and_strain_from_trajectory(sol.t, sol.y, lam)

    tau = K * TAU_SCALE
    E_128, *weights = error_128(tau)

    escaped = len(sol.t_events[0]) > 0
    return K, S, E_128, tau, escaped


# ============================================================
# 5. GRID SCANNER (2D MANIFOLD SAMPLER) (FIXED)
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
    S_map = np.zeros((RES, RES), dtype=float)
    forbidden = np.zeros((RES, RES), dtype=bool)

    total = RES * RES
    print(f"Scanning 2D Twist-Error Manifold {RES}x{RES}...")

    for i, y0 in enumerate(ys):
        for j, x0 in enumerate(xs):
            # 1. Compute potential and check forbidden region
            V0 = potential(x0, y0, lam)
            
            if V0 > E_hh:
                forbidden[i, j] = True
                # FIX: Assign NaN to indicate forbidden/invalid state
                E_map[i, j] = np.nan 
                K_map[i, j] = np.nan
                S_map[i, j] = np.nan
                continue

            # 2. Compute initial momentum py0 (px0=0 for simplicity)
            KE = E_hh - V0
            if KE <= 0:
                forbidden[i, j] = True
                # FIX: Assign NaN to indicate forbidden/invalid state
                E_map[i, j] = np.nan
                K_map[i, j] = np.nan
                S_map[i, j] = np.nan
                continue

            py0 = np.sqrt(2.0 * KE)
            px0 = 0.0

            # 3. Integrate, compute K, and map to E_128
            # NOTE: compute_K_and_E128 returns K, S, E_128, tau, escaped
            K, S, E_128, tau, escaped = compute_K_and_E128(
                x0, y0, px0, py0,
                m=m, lam=lam, E_hh=E_hh,
                t_max=t_max,
                n_samples=n_samples
            )
            
            E_map[i, j] = E_128
            K_map[i, j] = K
            S_map[i, j] = S

        if (i * RES) % (max(total // 10, 1)) == 0:
            print(f"  Progress: {100.0 * i * RES / total:5.1f}%")

    print("Scan complete.")
    return xs, ys, E_map, K_map, S_map, forbidden

# ============================================================
# 6. VISUALIZATIONS
# ============================================================

# ============================================================
# 6. VISUALIZATIONS (FIXED)
# ============================================================

def plot_2d_maps(xs, ys, E_map, K_map, S_map, forbidden, meta, save_path=None):
    # 1. FIX: Extract limits from meta
    x_min, x_max, y_min, y_max = meta["xy_limits"]
    
    # 2. FIX: Create title suffix
    title_suffix = textwrap.fill(
        f"\n$\lambda={meta['lam']:.1f}$, $E={meta['E_hh']:.3f}$, Res={meta['res']}",
        width=50
    )
    
    # flip for plotting
    K_img = np.flipud(K_map)
    S_img = np.flipud(S_map)
    E_img = np.flipud(E_map)
    forb  = np.flipud(forbidden)

    for arr in (K_img, S_img, E_img):
        arr[forb] = np.nan

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    axKnot, axStrain, axError = axes

    # --- Knottedness K ---
    K_max = np.nanpercentile(K_img, 99)
    if not np.isfinite(K_max) or K_max <= 0: K_max = 1.0
    im0 = axKnot.imshow(
        K_img, extent=(x_min, x_max, y_min, y_max),
        origin="lower", cmap="viridis",
        vmin=0.0, vmax=K_max, interpolation="nearest"
    )
    axKnot.set_title("Knottedness $K(x_0, y_0)$" + title_suffix)
    axKnot.set_xlabel("$x_0$")
    axKnot.set_ylabel("$y_0$")
    fig.colorbar(im0, ax=axKnot, fraction=0.046, pad=0.04, label="$K$")

    # --- Strain S ---
    S_max = np.nanpercentile(S_img, 99)
    if not np.isfinite(S_max) or S_max <= 0: S_max = 1.0
    im1 = axStrain.imshow(
        S_img, extent=(x_min, x_max, y_min, y_max),
        origin="lower", cmap="plasma",
        vmin=0.0, vmax=S_max, interpolation="nearest"
    )
    axStrain.set_title("Curvature Strain $S(x_0, y_0)$" + title_suffix)
    axStrain.set_xlabel("$x_0$")
    axStrain.set_ylabel("$y_0$")
    fig.colorbar(im1, ax=axStrain, fraction=0.046, pad=0.04, label="$S$")

    # --- Twist Error E_128 ---
    E_min = np.nanmin(E_img)
    E_max = np.nanpercentile(E_img, 99)
    if not np.isfinite(E_max) or E_max <= E_min: E_max = E_min + 1e-4
    im2 = axError.imshow(
        E_img, extent=(x_min, x_max, y_min, y_max),
        origin="lower", cmap="magma_r",
        vmin=E_min, vmax=E_max, interpolation="nearest"
    )
    axError.set_title("$E_{1:2:8}(\\tau=K\\cdot\mathrm{scale})$" + title_suffix)
    axError.set_xlabel("$x_0$")
    axError.set_ylabel("$y_0$")
    fig.colorbar(im2, ax=axError, fraction=0.046, pad=0.04, label="$E_{1:2:8}$")

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
    xs, ys, E_map, K_map, S_map, forbidden = scan_twist_error_manifold(
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
    plot_2d_maps(xs, ys, E_map, K_map, S_map, forbidden, meta, save_path=out_file)
    print(f"\nSaved 2D map to '{out_file}'.")


if __name__ == "__main__":
    main()