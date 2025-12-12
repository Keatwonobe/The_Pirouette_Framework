import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


# --------------------------------------------------------
# 1. Internal force: tension-mode with twist
#    (mirrors qcd_lock_11/12 + poincare/bifurcation code) :contentReference[oaicite:0]{index=0}
# --------------------------------------------------------
def get_force_tension_mode(m, lam, twist=1.5):
    """
    Net tension-mode force in (m, lam).
    Teal + Red + Gold with angular basin weighting.
    """
    # Teal anchor: harmonic toward (-0.866, 0.5)
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red anchor: toward (0, -1) with parity-violating twist
    F_red_m = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold = tension = vector sum
    F_gold_m = F_teal_m + F_red_m
    F_gold_lam = F_teal_lam + F_red_lam

    # Basin weights by angle
    angle = np.degrees(np.arctan2(lam, m)) % 360.0

    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360.0 - np.abs(x - mu))
        return np.exp(-(diff / sig) ** 2)

    w_gold = gaussian(angle, 30.0, 80.0)
    w_teal = gaussian(angle, 150.0, 80.0)
    w_red  = gaussian(angle, 270.0, 80.0)

    tot = w_gold + w_teal + w_red + 1e-6

    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    return Fm, Flam


# --------------------------------------------------------
# 2. Jacobian and local soft (U1) eigenvector
# --------------------------------------------------------
def jacobian_tension_mode(m, lam, twist=1.5, eps=1e-3):
    """
    Finite-difference Jacobian of F at (m, lam).
    J_ij = dF_i / dX_j, X = (m, lam).
    """
    m = float(m)
    lam = float(lam)

    Fm0, Flam0 = get_force_tension_mode(m, lam, twist)

    # Perturb m
    Fm_p, Flam_p = get_force_tension_mode(m + eps, lam, twist)
    Fm_m, Flam_m = get_force_tension_mode(m - eps, lam, twist)

    # Perturb lam
    Fm_l, Flam_l = get_force_tension_mode(m, lam + eps, twist)
    Fm_lp, Flam_lp = get_force_tension_mode(m, lam - eps, twist)

    dFm_dm     = (Fm_p    - Fm_m)    / (2 * eps)
    dFlam_dm   = (Flam_p  - Flam_m)  / (2 * eps)
    dFm_dlam   = (Fm_l    - Fm_lp)   / (2 * eps)
    dFlam_dlam = (Flam_l  - Flam_lp) / (2 * eps)

    J = np.array([[dFm_dm, dFm_dlam],
                  [dFlam_dm, dFlam_dlam]], dtype=float)
    return J


def u1_direction(m, lam, twist=1.5):
    """
    Unit eigenvector of Jacobian with smallest |eigenvalue|
    => softest restoring direction (photon-like U(1) mode).
    """
    J = jacobian_tension_mode(m, lam, twist=twist)
    vals, vecs = np.linalg.eig(J)

    idx = np.argmin(np.abs(vals))
    e = vecs[:, idx].real
    n = np.linalg.norm(e)
    if n == 0:
        return np.array([1.0, 0.0])
    e /= n
    # fix sign for continuity (optional)
    if e[0] < 0:
        e *= -1.0
    return e


def decompose_velocity(m, lam, vm, vlam, twist=1.5):
    """
    For arrays m(z), lam(z), vm(z), vlam(z), compute:
      U1(z)           = v · e_soft
      Delta_perp(z)   = ||v_perp||
      E_tot(z)        = ||v||^2
      E_u1(z)         = U1^2
      E_perp(z)       = E_tot - E_u1
    """
    n = m.shape[0]
    U1 = np.zeros_like(m)
    Delta_perp = np.zeros_like(m)
    E_tot = np.zeros_like(m)
    E_u1 = np.zeros_like(m)
    E_perp = np.zeros_like(m)

    for i in range(n):
        e = u1_direction(m[i], lam[i], twist=twist)
        v = np.array([vm[i], vlam[i]])
        U1_i = np.dot(v, e)
        v_par = U1_i * e
        v_perp = v - v_par

        U1[i] = U1_i
        Delta_perp[i] = np.linalg.norm(v_perp)
        E_tot[i] = np.dot(v, v)
        E_u1[i] = U1_i**2
        E_perp[i] = E_tot[i] - E_u1[i]

    # numerical noise: clamp very small negatives
    E_perp = np.maximum(E_perp, 0.0)

    return U1, Delta_perp, E_tot, E_u1, E_perp


# --------------------------------------------------------
# 3. 1+1D helix simulation with gauge split
# --------------------------------------------------------
def run_helix_gauge_split(
    n_points=200,
    length=50.0,
    total_time=250.0,
    c=1.0,
    gamma=0.05,
    twist=1.5,
    drive_amp=0.8,
    drive_omega=1.2,
    drive_width=7,
    parity_bias=0.25,
    snapshot_interval=5,
):
    """
    Evolves fields m(z,t), lam(z,t) with tension-mode force + wave coupling
    and returns snapshots of:
      Δ_total(z,t) = ||v||
      U1(z,t)      = photon-like amplitude
      Δ_perp(z,t)  = ||v_perp||
      E_tot, E_u1, E_perp for energy diagnostics
      orbit at center site (for sanity visuals)
    """
    # Spatial grid
    z = np.linspace(0.0, length, n_points, endpoint=False)
    dz = z[1] - z[0]

    dt = 0.35 * dz / max(c, 1e-8)
    n_steps = int(total_time / dt)

    # Fields & velocities
    m = np.zeros(n_points)
    lam = np.zeros(n_points)
    vm = np.zeros_like(m)
    vlam = np.zeros_like(lam)

    # Small symmetry-breaking seed
    m += 0.01 * (np.random.rand(n_points) - 0.5)
    lam += 0.01 * (np.random.rand(n_points) - 0.5)

    idx = np.arange(n_points)
    ip = (idx + 1) % n_points
    im = (idx - 1) % n_points

    center = n_points // 2
    drive_mask = np.zeros(n_points)
    half_w = max(1, drive_width // 2)
    drive_mask[center - half_w : center + half_w + 1] = 1.0

    # Storage
    times = []
    Delta_tot_snaps = []
    U1_snaps = []
    Delta_perp_snaps = []
    E_tot_snaps = []
    E_u1_snaps = []
    E_perp_snaps = []
    orbit_m = []
    orbit_l = []

    print(
        f"[GaugeSplit] Running helix sim: {n_points} sites, "
        f"{n_steps} steps, dz={dz:.3f}, dt={dt:.4f}"
    )

    for step in range(n_steps):
        t = step * dt

        orbit_m.append(m[center])
        orbit_l.append(lam[center])

        Fm_int, Flam_int = get_force_tension_mode(m, lam, twist=twist)

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

            # Δ_total
            Delta_tot = np.sqrt(vm**2 + vlam**2)

            # Decompose into U1 and perpendicular
            U1, Delta_perp, E_tot, E_u1, E_perp = decompose_velocity(
                m, lam, vm, vlam, twist=twist
            )

            Delta_tot_snaps.append(Delta_tot.copy())
            U1_snaps.append(U1.copy())
            Delta_perp_snaps.append(Delta_perp.copy())
            E_tot_snaps.append(E_tot.copy())
            E_u1_snaps.append(E_u1.copy())
            E_perp_snaps.append(E_perp.copy())

    return (
        z,
        np.array(times),
        np.array(Delta_tot_snaps),
        np.array(U1_snaps),
        np.array(Delta_perp_snaps),
        np.array(E_tot_snaps),
        np.array(E_u1_snaps),
        np.array(E_perp_snaps),
        np.array(orbit_m),
        np.array(orbit_l),
    )


# --------------------------------------------------------
# 4. Visualization: Δ_total vs U1 vs Δ_perp + energy flow
# --------------------------------------------------------
def demo_plot_gauge_split(
    z,
    times,
    Delta_tot_snaps,
    U1_snaps,
    Delta_perp_snaps,
    E_tot_snaps,
    E_u1_snaps,
    E_perp_snaps,
    orbit_m,
    orbit_l,
):
    # Spatial averages for energy plot
    mean_E_tot = E_tot_snaps.mean(axis=1)
    mean_E_u1 = E_u1_snaps.mean(axis=1)
    mean_E_perp = E_perp_snaps.mean(axis=1)

    fig, axes = plt.subplots(4, 1, figsize=(10, 14), constrained_layout=True)

    # 1) Δ_total
    im0 = axes[0].imshow(
        Delta_tot_snaps,
        aspect="auto",
        origin="lower",
        extent=[z[0], z[-1], times[0], times[-1]],
    )
    axes[0].set_ylabel("Time")
    axes[0].set_title("Δ_total(z,t) = ||v||  (all motion)")
    cbar0 = fig.colorbar(im0, ax=axes[0])
    cbar0.set_label("Δ_total")

    # 2) U1 (photon)
    im1 = axes[1].imshow(
        U1_snaps,
        aspect="auto",
        origin="lower",
        extent=[z[0], z[-1], times[0], times[-1]],
    )
    axes[1].set_ylabel("Time")
    axes[1].set_title("U₁(z,t) = v · e_soft  (photon-like mode)")
    cbar1 = fig.colorbar(im1, ax=axes[1])
    cbar1.set_label("U₁")

    # 3) Δ_perp (confining)
    im2 = axes[2].imshow(
        Delta_perp_snaps,
        aspect="auto",
        origin="lower",
        extent=[z[0], z[-1], times[0], times[-1]],
    )
    axes[2].set_ylabel("Time")
    axes[2].set_title("Δ⊥(z,t) = ||v_perp||  (confining/color motion)")
    cbar2 = fig.colorbar(im2, ax=axes[2])
    cbar2.set_label("Δ⊥")

    # 4) Energy flow (spatial averages)
    axes[3].plot(times, mean_E_tot, label="E_tot", color="black", linewidth=1.5)
    axes[3].plot(times, mean_E_u1, label="E_U1 (photon)", linestyle="--")
    axes[3].plot(times, mean_E_perp, label="E_perp (confining)", linestyle=":")
    axes[3].set_xlabel("Time")
    axes[3].set_ylabel("⟨Energy⟩ (arb. units)")
    axes[3].set_title("Energy flow between photon and confining channels")
    axes[3].legend()

    plt.show()


if __name__ == "__main__":
    (
        z,
        times,
        Delta_tot_snaps,
        U1_snaps,
        Delta_perp_snaps,
        E_tot_snaps,
        E_u1_snaps,
        E_perp_snaps,
        orbit_m,
        orbit_l,
    ) = run_helix_gauge_split()

    demo_plot_gauge_split(
        z,
        times,
        Delta_tot_snaps,
        U1_snaps,
        Delta_perp_snaps,
        E_tot_snaps,
        E_u1_snaps,
        E_perp_snaps,
        orbit_m,
        orbit_l,
    )

def color_frame(m, lam, twist=1.5):
    J = jacobian_tension_mode(m, lam, twist)
    vals, vecs = np.linalg.eig(J)

    # Sort eigenvectors by eigenvalue magnitude
    idx = np.argsort(np.abs(vals))
    e_soft = vecs[:, idx[0]].real  # U(1)
    e_mid  = vecs[:, idx[1]].real  # SU(3) direction 1
    e_hard = vecs[:, idx[2]].real  # SU(3) direction 2

    # Normalize and enforce consistent orientation
    def fix(v):
        v = v.real
        if np.linalg.norm(v) == 0:
            return np.array([1.0,0.0])
        v = v / np.linalg.norm(v)
        if v[0] < 0: v = -v
        return v

    return fix(e_soft), fix(e_mid), fix(e_hard)

def gauge_connection(m, lam, twist=1.5):
    n = len(m)
    A_soft  = np.zeros(n)
    A_mid   = np.zeros(n)
    A_hard  = np.zeros(n)

    for i in range(n):
        ip = (i + 1) % n
        e_s, e_m, e_h = color_frame(m[i], lam[i], twist)
        e_s2, e_m2, e_h2 = color_frame(m[ip], lam[ip], twist)

        # discrete derivative
        ds = e_s2 - e_s
        dm = e_m2 - e_m
        dh = e_h2 - e_h

        # projection onto axes
        A_soft[i] = np.dot(ds, e_s)
        A_mid[i]  = np.dot(dm, e_m)
        A_hard[i] = np.dot(dh, e_h)

    return A_soft, A_mid, A_hard

def gauge_curvature(A):
    n = len(A)
    F = np.zeros(n)
    for i in range(n):
        ip = (i + 1) % n
        F[i] = A[ip] - A[i]
    return F

def plot_gauge_fields(z, A_soft, A_mid, A_hard, F_soft, F_mid, F_hard):
    fig, ax = plt.subplots(2,1,figsize=(12,8),sharex=True)

    ax[0].plot(z, A_soft, label='A_soft (U1)', color='cyan')
    ax[0].plot(z, A_mid,  label='A_mid (color 1)', color='orange')
    ax[0].plot(z, A_hard, label='A_hard (color 2)', color='red')
    ax[0].set_title("Gauge Potentials A_z^a extracted from frame rotation")
    ax[0].legend()

    ax[1].plot(z, F_soft, label='F_soft', color='cyan')
    ax[1].plot(z, F_mid,  label='F_mid', color='orange')
    ax[1].plot(z, F_hard, label='F_hard', color='red')
    ax[1].set_title("Curvature F_z^a (gluon-like field strength)")
    ax[1].set_xlabel("z")

    plt.show()
