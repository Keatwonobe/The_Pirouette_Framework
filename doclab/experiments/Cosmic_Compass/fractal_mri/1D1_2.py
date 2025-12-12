import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


# ---------------------------------------------------------------------
# Internal force law: adapted directly from your tension-mode module
# (qcd_lock_7.py) but vectorized for arrays. :contentReference[oaicite:1]{index=1}
# ---------------------------------------------------------------------
def get_force_tension_mode(m, lam):
    """
    m, lam can be scalars or numpy arrays.
    Returns (Fm, Flam) with the same shape.
    """

    # 1. Teal (EM-like): harmonic attraction to (-0.866, 0.5)
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak-like): parity-violated attraction to (0, -1)
    F_red_m = -(m - 0.0)
    p_violation = 1.2 * np.sin(m * 3.0)  # chiral twist
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong-like): emergent tension = vector sum
    F_gold_m = F_teal_m + F_red_m
    F_gold_lam = F_teal_lam + F_red_lam

    # Sector weighting by angle
    angle = np.degrees(np.arctan2(lam, m)) % 360.0

    def gaussian(x, mu, sig):
        # circular Gaussian on [0, 360)
        diff = np.minimum(np.abs(x - mu), 360.0 - np.abs(x - mu))
        return np.exp(-(diff / sig) ** 2)

    w_gold = gaussian(angle, 30.0, 80.0)
    w_teal = gaussian(angle, 150.0, 80.0)
    w_red = gaussian(angle, 270.0, 80.0)

    tot = w_gold + w_teal + w_red + 1e-6

    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot

    return Fm, Flam


# ---------------------------------------------------------------------
# 1+1D 2-field helix simulator
# ---------------------------------------------------------------------
def run_delta_helix_sim(
    n_points=200,
    length=50.0,
    total_time=250.0,
    c=1.0,
    gamma=0.05,
    drive_amp=0.8,
    drive_omega=1.2,
    drive_width=7,
    parity_bias=0.25,
    snapshot_interval=5,
):
    """
    Evolves coupled fields m(z,t), lam(z,t) on a 1D periodic lattice.

      m¨ = c² ∂²m/∂z² + Fm_int(m,lam) + Fm_drive - gamma ṁ
      λ¨ = c² ∂²λ/∂z² + Flam_int(m,lam) + Flam_drive - gamma λ̇

    where F*_int come from get_force_tension_mode and the drive
    is a localized twist applied to λ.

    Returns:
      z, times,
      m_snaps, lam_snaps,
      delta_snaps,      # Δ(z,t) = sqrt(ṁ² + λ̇²)
      orbit_m, orbit_l  # internal orbit at center site vs time
    """
    # Spatial grid
    z = np.linspace(0.0, length, n_points, endpoint=False)
    dz = z[1] - z[0]

    # CFL-ish timestep
    dt = 0.35 * dz / max(c, 1e-8)
    n_steps = int(total_time / dt)

    # Fields and velocities
    m = np.zeros(n_points, dtype=float)
    lam = np.zeros(n_points, dtype=float)
    vm = np.zeros_like(m)
    vlam = np.zeros_like(lam)

    # Tiny random seed so symmetry can break even without drive
    m += 0.01 * (np.random.rand(n_points) - 0.5)
    lam += 0.01 * (np.random.rand(n_points) - 0.5)

    # Periodic neighbor indices
    idx = np.arange(n_points)
    ip = (idx + 1) % n_points
    im = (idx - 1) % n_points

    # Localized twist drive region around center
    center = n_points // 2
    drive_mask = np.zeros(n_points, dtype=float)
    half_w = max(1, drive_width // 2)
    drive_mask[center - half_w : center + half_w + 1] = 1.0

    # Storage
    m_snaps = []
    lam_snaps = []
    delta_snaps = []
    times = []

    orbit_m = []   # center site internal orbit
    orbit_l = []

    print(
        f"[Δ⊗] 2-field helix sim: {n_points} sites, "
        f"{n_steps} steps, dz={dz:.3f}, dt={dt:.4f}"
    )

    for step in range(n_steps):
        t = step * dt

        # Record orbit at center site
        orbit_m.append(m[center])
        orbit_l.append(lam[center])

        # Internal forces from tension-mode geometry
        Fm_int, Flam_int = get_force_tension_mode(m, lam)

        # Twist drive acts on λ only, in a localized region
        drive_phase = np.sin(drive_omega * t) + parity_bias
        Fm_drive = 0.0
        Flam_drive = drive_amp * drive_phase * drive_mask

        # Wave coupling (Laplace operator)
        lap_m = (m[ip] - 2.0 * m + m[im]) / dz**2
        lap_lam = (lam[ip] - 2.0 * lam + lam[im]) / dz**2
        Fm_wave = c**2 * lap_m
        Flam_wave = c**2 * lap_lam

        # Total accelerations
        am = Fm_int + Fm_wave + Fm_drive - gamma * vm
        alam = Flam_int + Flam_wave + Flam_drive - gamma * vlam

        # Integrate (explicit Verlet-style)
        vm += am * dt
        vlam += alam * dt
        m += vm * dt
        lam += vlam * dt

        # Save snapshots
        if step % snapshot_interval == 0:
            times.append(t)
            m_snaps.append(m.copy())
            lam_snaps.append(lam.copy())
            delta_snaps.append(np.sqrt(vm**2 + vlam**2))

    return (
        z,
        np.array(times),
        np.array(m_snaps),
        np.array(lam_snaps),
        np.array(delta_snaps),
        np.array(orbit_m),
        np.array(orbit_l),
    )


# ---------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------
def demo_plot(
    z,
    times,
    m_snaps,
    lam_snaps,
    delta_snaps,
    orbit_m,
    orbit_l,
    max_frames=300,
):
    """
    Shows:
      1) Δ(z,t) heatmap (EM-like field)
      2) Internal orbit at the center site in (m, λ) space
    """
    # Subsample in time if necessary
    n_frames = delta_snaps.shape[0]
    if n_frames > max_frames:
        stride = max(1, n_frames // max_frames)
        delta_snaps = delta_snaps[::stride]
        m_snaps = m_snaps[::stride]
        lam_snaps = lam_snaps[::stride]
        times = times[::stride]

    # --- Figure 1: Δ field over spacetime -----------------------------
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 9), constrained_layout=True
    )

    im = ax1.imshow(
        delta_snaps,
        aspect="auto",
        origin="lower",
        extent=[z[0], z[-1], times[0], times[-1]],
    )
    ax1.set_ylabel("Time")
    ax1.set_title("Δ(z, t) = √(ṁ² + λ̇²)  (EM-like field)")

    cbar = fig.colorbar(im, ax=ax1)
    cbar.set_label("Δ magnitude")

    # --- Figure 2: internal orbit at center site ----------------------
    # Color code segments by angle sector (teal / gold / red)
    m_arr = orbit_m
    l_arr = orbit_l
    angle = np.degrees(np.arctan2(l_arr, m_arr)) % 360.0

    colors = []
    for ang in angle:
        if 210 < ang < 330:
            colors.append((1.0, 0.3, 0.3))     # red sector
        elif 330 < ang or ang < 90:
            colors.append((1.0, 0.8, 0.0))     # gold sector
        else:
            colors.append((0.0, 0.8, 0.8))     # teal sector

    pts = np.column_stack([m_arr, l_arr]).reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = LineCollection(segs, colors=colors, linewidth=2.0)

    ax2.add_collection(lc)
    ax2.scatter([-0.866], [0.5], color="cyan", marker="x", s=80, label="Teal Anchor")
    ax2.scatter([0.0], [-1.0], color="red", marker="x", s=80, label="Red Anchor")
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax2.set_xlabel("m")
    ax2.set_ylabel("λ")
    ax2.set_title("Internal Orbit at Center Site")
    ax2.legend(loc="upper right")

    plt.show()


if __name__ == "__main__":
    (
        z,
        times,
        m_snaps,
        lam_snaps,
        delta_snaps,
        orbit_m,
        orbit_l,
    ) = run_delta_helix_sim()

    demo_plot(
        z,
        times,
        m_snaps,
        lam_snaps,
        delta_snaps,
        orbit_m,
        orbit_l,
    )
