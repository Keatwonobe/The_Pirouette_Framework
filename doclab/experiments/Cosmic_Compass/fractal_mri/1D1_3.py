import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


# -------------------------------------------------------------
# 1. Internal force law (from qcd_lock_7.py, vectorized)
# -------------------------------------------------------------
def get_force_tension_mode(m, lam):
    """
    m, lam: scalars or numpy arrays of same shape
    Returns: (Fm, Flam) with same shape.
    """

    # Teal: harmonic toward (-0.866, 0.5)
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red: biased toward (0, -1) with parity violation in λ
    F_red_m = -(m - 0.0)
    p_violation = 1.2 * np.sin(m * 3.0)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold: emergent vector sum
    F_gold_m = F_teal_m + F_red_m
    F_gold_lam = F_teal_lam + F_red_lam

    # Sector weights by angle in (m, λ) plane
    angle = np.degrees(np.arctan2(lam, m)) % 360.0

    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360.0 - np.abs(x - mu))
        return np.exp(-(diff / sig) ** 2)

    w_gold = gaussian(angle, 30.0, 80.0)
    w_teal = gaussian(angle, 150.0, 80.0)
    w_red = gaussian(angle, 270.0, 80.0)
    tot = w_gold + w_teal + w_red + 1e-6

    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    return Fm, Flam


# -------------------------------------------------------------
# 2. Local Jacobian and U(1) eigenvector
# -------------------------------------------------------------
def jacobian_tension_mode(m, lam, eps=1e-3):
    """
    Finite-difference Jacobian of F at (m, lam).

    J_ij = dF_i / dX_j, X = (m, lam)
    Returns 2x2 numpy array.
    """
    m = float(m)
    lam = float(lam)

    # Base forces
    Fm0, Flam0 = get_force_tension_mode(m, lam)

    # Perturb m
    Fm_m, Flam_m = get_force_tension_mode(m + eps, lam)
    Fm_p, Flam_p = get_force_tension_mode(m - eps, lam)

    # Perturb lam
    Fm_l, Flam_l = get_force_tension_mode(m, lam + eps)
    Fm_lp, Flam_lp = get_force_tension_mode(m, lam - eps)

    dFm_dm = (Fm_m - Fm_p) / (2 * eps)
    dFlam_dm = (Flam_m - Flam_p) / (2 * eps)

    dFm_dlam = (Fm_l - Fm_lp) / (2 * eps)
    dFlam_dlam = (Flam_l - Flam_lp) / (2 * eps)

    J = np.array([[dFm_dm, dFm_dlam], [dFlam_dm, dFlam_dlam]], dtype=float)
    return J


def u1_direction(m, lam):
    """
    Returns a unit vector e_u1 (2,) giving the softest restoring direction
    of the tension-mode force at (m, lam).

    We take the eigenvector of the Jacobian with the smallest |eigenvalue|.
    """
    J = jacobian_tension_mode(m, lam)
    vals, vecs = np.linalg.eig(J)

    # Pick eigenvector with smallest |eigenvalue|
    idx = np.argmin(np.abs(vals))
    e = vecs[:, idx].real

    # Normalize
    n = np.linalg.norm(e)
    if n == 0:
        return np.array([1.0, 0.0])
    e /= n

    # Fix sign for continuity (optional: make first component non-negative)
    if e[0] < 0:
        e *= -1.0

    return e


def project_u1_field(m, lam, vm, vlam):
    """
    For arrays m(z), lam(z), vm(z), vlam(z),
    compute the scalar U1(z) = v · e_u1 where e_u1
    is the soft eigenvector at each site.
    """
    n = m.shape[0]
    U1 = np.zeros_like(m)
    for i in range(n):
        e = u1_direction(m[i], lam[i])
        v = np.array([vm[i], vlam[i]])
        U1[i] = np.dot(v, e)
    return U1


# -------------------------------------------------------------
# 3. 1+1D 2-field sim with U(1) extraction
# -------------------------------------------------------------
def run_delta_helix_u1(
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
    Same dynamics as the previous helix sim, but also returns:

      U1_snaps[z,t] = projection of velocity onto local U(1) direction.
    """
    # Spatial grid
    z = np.linspace(0.0, length, n_points, endpoint=False)
    dz = z[1] - z[0]

    dt = 0.35 * dz / max(c, 1e-8)
    n_steps = int(total_time / dt)

    # Fields + velocities
    m = np.zeros(n_points)
    lam = np.zeros(n_points)
    vm = np.zeros_like(m)
    vlam = np.zeros_like(lam)

    # Small random seed
    m += 0.01 * (np.random.rand(n_points) - 0.5)
    lam += 0.01 * (np.random.rand(n_points) - 0.5)

    idx = np.arange(n_points)
    ip = (idx + 1) % n_points
    im = (idx - 1) % n_points

    center = n_points // 2
    drive_mask = np.zeros(n_points)
    half_w = max(1, drive_width // 2)
    drive_mask[center - half_w : center + half_w + 1] = 1.0

    m_snaps = []
    lam_snaps = []
    delta_snaps = []
    U1_snaps = []
    times = []

    orbit_m = []
    orbit_l = []

    print(
        f"[U1] helix sim: {n_points} sites, {n_steps} steps, "
        f"dz={dz:.3f}, dt={dt:.4f}"
    )

    for step in range(n_steps):
        t = step * dt

        orbit_m.append(m[center])
        orbit_l.append(lam[center])

        Fm_int, Flam_int = get_force_tension_mode(m, lam)

        drive_phase = np.sin(drive_omega * t) + parity_bias
        Fm_drive = 0.0
        Flam_drive = drive_amp * drive_phase * drive_mask

        lap_m = (m[ip] - 2.0 * m + m[im]) / dz**2
        lap_lam = (lam[ip] - 2.0 * lam + lam[im]) / dz**2
        Fm_wave = c**2 * lap_m
        Flam_wave = c**2 * lap_lam

        am = Fm_int + Fm_wave + Fm_drive - gamma * vm
        alam = Flam_int + Flam_wave + Flam_drive - gamma * vlam

        vm += am * dt
        vlam += alam * dt
        m += vm * dt
        lam += vlam * dt

        if step % snapshot_interval == 0:
            times.append(t)
            m_snaps.append(m.copy())
            lam_snaps.append(lam.copy())

            # Δ = magnitude of velocity
            delta_snaps.append(np.sqrt(vm**2 + vlam**2))

            # U1 = projection of velocity onto soft eigenvector
            U1_snaps.append(project_u1_field(m, lam, vm, vlam))

    return (
        z,
        np.array(times),
        np.array(m_snaps),
        np.array(lam_snaps),
        np.array(delta_snaps),
        np.array(U1_snaps),
        np.array(orbit_m),
        np.array(orbit_l),
    )


# -------------------------------------------------------------
# 4. Visualization: Δ vs U1 + orbit
# -------------------------------------------------------------
def demo_plot_u1(
    z,
    times,
    delta_snaps,
    U1_snaps,
    orbit_m,
    orbit_l,
    max_frames=300,
):
    # Subsample if needed
    n_frames = delta_snaps.shape[0]
    if n_frames > max_frames:
        stride = max(1, n_frames // max_frames)
        delta_snaps = delta_snaps[::stride]
        U1_snaps = U1_snaps[::stride]
        times = times[::stride]

    fig, axes = plt.subplots(3, 1, figsize=(10, 11), constrained_layout=True)

    # 1) Δ heatmap
    im0 = axes[0].imshow(
        delta_snaps,
        aspect="auto",
        origin="lower",
        extent=[z[0], z[-1], times[0], times[-1]],
    )
    axes[0].set_ylabel("Time")
    axes[0].set_title("Δ(z,t) = ||v||  (total kinetic field)")
    cbar0 = fig.colorbar(im0, ax=axes[0])
    cbar0.set_label("Δ magnitude")

    # 2) U1 heatmap
    im1 = axes[1].imshow(
        U1_snaps,
        aspect="auto",
        origin="lower",
        extent=[z[0], z[-1], times[0], times[-1]],
    )
    axes[1].set_ylabel("Time")
    axes[1].set_title("U₁(z,t) = v · e_soft  (true photon-like mode)")
    cbar1 = fig.colorbar(im1, ax=axes[1])
    cbar1.set_label("U₁ amplitude")

    # 3) internal orbit with sector colors
    m_arr = orbit_m
    l_arr = orbit_l
    angle = np.degrees(np.arctan2(l_arr, m_arr)) % 360.0

    colors = []
    for ang in angle:
        if 210 < ang < 330:
            colors.append((1.0, 0.3, 0.3))   # red
        elif 330 < ang or ang < 90:
            colors.append((1.0, 0.8, 0.0))   # gold
        else:
            colors.append((0.0, 0.8, 0.8))   # teal

    pts = np.column_stack([m_arr, l_arr]).reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = LineCollection(segs, colors=colors, linewidth=2.0)
    axes[2].add_collection(lc)
    axes[2].scatter([-0.866], [0.5], color="cyan", marker="x", s=80, label="Teal anchor")
    axes[2].scatter([0.0], [-1.0], color="red", marker="x", s=80, label="Red anchor")
    axes[2].set_xlim(-2, 2)
    axes[2].set_ylim(-2, 2)
    axes[2].set_xlabel("m")
    axes[2].set_ylabel("λ")
    axes[2].set_title("Internal Orbit at Center Site")
    axes[2].legend(loc="upper right")

    plt.show()


if __name__ == "__main__":
    (
        z,
        times,
        m_snaps,
        lam_snaps,
        delta_snaps,
        U1_snaps,
        orbit_m,
        orbit_l,
    ) = run_delta_helix_u1()

    demo_plot_u1(z, times, delta_snaps, U1_snaps, orbit_m, orbit_l)
