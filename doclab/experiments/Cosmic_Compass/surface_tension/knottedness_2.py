import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.colors import ListedColormap
import argparse
import os
import textwrap
import datetime

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

    Returns:
        float K
    """

    x = states[0]
    y = states[1]
    px = states[2]
    py = states[3]

    # Velocities in these units (m=1 used in integration)
    vx = px
    vy = py

    dt = np.diff(t)
    if len(dt) == 0:
        return 0.0
    dt = np.append(dt, dt[-1])

    # Approximate accelerations
    ax = np.zeros_like(x)
    ay = np.zeros_like(y)

    # interior points
    if len(t) > 2:
        ax[1:-1] = (vx[2:] - vx[:-2]) / (t[2:] - t[:-2] + eps)
        ay[1:-1] = (vy[2:] - vy[:-2]) / (t[2:] - t[:-2] + eps)

    # endpoints
    ax[0] = (vx[1] - vx[0]) / (t[1] - t[0] + eps)
    ay[0] = (vy[1] - vy[0]) / (t[1] - t[0] + eps)
    ax[-1] = (vx[-1] - vx[-2]) / (t[-1] - t[-2] + eps)
    ay[-1] = (vy[-1] - vy[-2]) / (t[-1] - t[-2] + eps)

    # Curvature of the spatial path
    v2 = vx**2 + vy**2
    speed = np.sqrt(v2) + eps
    num = np.abs(vx * ay - vy * ax)
    kappa = num / (speed**3 + eps)

    # Our Δ proxy: potential energy magnitude
    V = np.abs(potential(x, y, lam))

    dt = np.asarray(dt)

    I_delta = np.sum(V * dt)         # total Δ-weight
    T_delta = np.sum(V * kappa * dt) # Δ-weighted twisting

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
        xs, ys, exit_map, K_map, forbidden
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
            if count % (max(total // 10, 1)) == 0:
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
            if KE <= 0:
                forbidden[i, j] = True
                exit_map[i, j] = -1
                K_map[i, j] = 0.0
                continue

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
# 5. SAVE / LOAD SUITE ARTIFACTS
# ============================================================

def save_scan(filename, xs, ys, exit_map, K_map, forbidden, meta=None):
    """
    Save scan results to a compressed npz file.
    """
    if meta is None:
        meta = {}

    np.savez_compressed(
        filename,
        xs=xs,
        ys=ys,
        exit_map=exit_map,
        K_map=K_map,
        forbidden=forbidden,
        meta=np.array([meta], dtype=object),
    )
    print(f"[SAVE] Scan saved to {filename}")


def load_scan(filename):
    """
    Load scan results from a compressed npz file.
    Returns:
        xs, ys, exit_map, K_map, forbidden, meta
    """
    data = np.load(filename, allow_pickle=True)
    xs = data["xs"]
    ys = data["ys"]
    exit_map = data["exit_map"]
    K_map = data["K_map"]
    forbidden = data["forbidden"]
    meta_arr = data.get("meta", np.array([{}], dtype=object))
    meta = meta_arr[0] if len(meta_arr) > 0 else {}
    print(f"[LOAD] Scan loaded from {filename}")
    return xs, ys, exit_map, K_map, forbidden, meta


# ============================================================
# 6. VISUALIZATIONS
# ============================================================

def plot_basin_and_knottedness(xs, ys, exit_map, K_map, forbidden,
                               XY_LIMITS, title_suffix="",
                               save_path=None):
    """
    Two-panel figure:
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
        "dimgray",  # index 0: will map to forbidden
        "black",    # 1: trapped
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
    if not np.isfinite(K_max) or K_max <= 0:
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

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"[SAVE] Figure saved to {save_path}")
        plt.close(fig)
    else:
        plt.show()


def plot_knottedness_summary(exit_map, K_map, forbidden,
                             title_suffix="", save_path=None):
    """
    Summary figure:
      - left: histogram of K over all allowed points
      - right: boxplot of K grouped by exit basin (0,1,2,3)
    """

    mask_valid = (~forbidden) & (exit_map >= 0)
    if not np.any(mask_valid):
        print("[WARN] No valid points for summary.")
        return

    K_valid = K_map[mask_valid]
    exits_valid = exit_map[mask_valid]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axHist, axBox = axes

    # Histogram of K
    axHist.hist(K_valid, bins=80, alpha=0.8)
    axHist.set_xlabel("Knottedness K")
    axHist.set_ylabel("Count")
    axHist.set_title("Knottedness Distribution" + title_suffix)

    # Boxplot by exit id
    data_by_exit = []
    labels = []
    for exit_id in [0, 1, 2, 3]:
        mask_e = exits_valid == exit_id
        if np.any(mask_e):
            data_by_exit.append(K_valid[mask_e])
            labels.append(str(exit_id))

    if data_by_exit:
        axBox.boxplot(data_by_exit, labels=labels, showfliers=False)
    axBox.set_xlabel("Exit basin ID (0 = trapped)")
    axBox.set_ylabel("Knottedness K")
    axBox.set_title("Knottedness by Exit Basin" + title_suffix)

    plt.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[SAVE] Summary figure saved to {save_path}")
        plt.close(fig)
    else:
        plt.show()


# ============================================================
# 7. CLI / MAIN
# ============================================================

def make_default_scan_name(lam, E, RES):
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"scan_lam{lam:.2f}_E{E:.4f}_R{RES}_{ts}.npz"


def main():
    desc = textwrap.dedent("""
    Knottedness suite for Hénon–Heiles:

    Subcommands:
      scan     - run a manifold scan and save to .npz
      plot     - load a scan and plot basins + knottedness
      summary  - load a scan and plot K histogram / boxplot
    """)

    parser = argparse.ArgumentParser(description=desc)
    subparsers = parser.add_subparsers(dest="command")

    # --- scan subcommand ---
    p_scan = subparsers.add_parser("scan", help="Run a manifold scan and save results.")
    p_scan.add_argument("--lam", type=float, default=1.0, help="λ parameter.")
    p_scan.add_argument("--mass", type=float, default=1.0, help="Mass m.")
    p_scan.add_argument("--energy", type=float, default=None,
                        help="Total energy E (default: saddle + 0.01).")
    p_scan.add_argument("--xy-min", type=float, default=-2.0, help="Min x,y.")
    p_scan.add_argument("--xy-max", type=float, default=2.0, help="Max x,y.")
    p_scan.add_argument("--res", type=int, default=200, help="Grid resolution.")
    p_scan.add_argument("--t-max", type=float, default=200.0, help="Max integration time.")
    p_scan.add_argument("--r-escape", type=float, default=5.0, help="Escape radius.")
    p_scan.add_argument("--samples", type=int, default=250, help="Samples per trajectory.")
    p_scan.add_argument("--out", type=str, default=None,
                        help="Output .npz file (default: auto name).")

    # --- plot subcommand ---
    p_plot = subparsers.add_parser("plot", help="Plot basins + knottedness from a scan.")
    p_plot.add_argument("scan_file", type=str, help="Scan .npz file.")
    p_plot.add_argument("--save", type=str, default=None,
                        help="Path to save figure (default: show).")

    # --- summary subcommand ---
    p_summary = subparsers.add_parser("summary", help="Plot K histogram and boxplot.")
    p_summary.add_argument("scan_file", type=str, help="Scan .npz file.")
    p_summary.add_argument("--save", type=str, default=None,
                           help="Path to save summary figure (default: show).")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "scan":
        lam = args.lam
        m = args.mass
        E_saddle = 1.0 / 6.0 * lam**2 / lam**2  # same saddle for lam=1, generalized placeholder
        if args.energy is None:
            E = E_saddle + 0.01
        else:
            E = args.energy

        XY_LIMITS = (args.xy_min, args.xy_max, args.xy_min, args.xy_max)
        RES = args.res

        xs, ys, exit_map, K_map, forbidden = scan_manifold(
            m=m,
            lam=lam,
            E=E,
            XY_LIMITS=XY_LIMITS,
            RES=RES,
            t_max=args.t_max,
            r_escape=args.r_escape,
            n_samples=args.samples,
        )

        if args.out is None:
            out_name = make_default_scan_name(lam, E, RES)
        else:
            out_name = args.out

        meta = {
            "lam": lam,
            "mass": m,
            "energy": E,
            "xy_limits": XY_LIMITS,
            "res": RES,
            "t_max": args.t_max,
            "r_escape": args.r_escape,
            "n_samples": args.samples,
        }

        save_scan(out_name, xs, ys, exit_map, K_map, forbidden, meta)

    elif args.command == "plot":
        xs, ys, exit_map, K_map, forbidden, meta = load_scan(args.scan_file)
        XY_LIMITS = tuple(meta.get("xy_limits", (-2.0, 2.0, -2.0, 2.0)))
        lam = meta.get("lam", 1.0)
        E = meta.get("energy", 1.0 / 6.0 + 0.01)
        title_suffix = f"\n(λ={lam}, E={E:.4f})"

        plot_basin_and_knottedness(
            xs, ys, exit_map, K_map, forbidden,
            XY_LIMITS,
            title_suffix=title_suffix,
            save_path=args.save
        )

    elif args.command == "summary":
        xs, ys, exit_map, K_map, forbidden, meta = load_scan(args.scan_file)
        lam = meta.get("lam", 1.0)
        E = meta.get("energy", 1.0 / 6.0 + 0.01)
        title_suffix = f"\n(λ={lam}, E={E:.4f})"

        plot_knottedness_summary(
            exit_map, K_map, forbidden,
            title_suffix=title_suffix,
            save_path=args.save
        )


if __name__ == "__main__":
    main()
