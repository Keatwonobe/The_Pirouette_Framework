import numpy as np
import matplotlib.pyplot as plt


def run_delta_field_sim(
    n_points=200,
    length=50.0,
    total_time=200.0,
    c=1.0,
    k_confine=1.0,
    gamma=0.05,
    drive_amp=1.0,
    drive_omega=1.0,
    drive_width=5,
    parity_bias=0.3,
    snapshot_interval=5,
):
    """
    1+1D Δ-field toy simulator.

    Field x(z, t) lives on a periodic 1D lattice.

      d²x/dt² = c² ∂²x/∂z² + F_twist(z,t) + F_confine(x) - gamma * dx/dt

    where
        F_confine = -k_confine * x³  (nonlinear confinement)
        F_twist   = localized sinusoidal drive with a chiral (parity) bias

    We identify the emergent EM-like field as

        Δ(z, t) = dx/dt

    Parameters
    ----------
    n_points : int
        Number of spatial lattice sites.
    length : float
        Physical length of the ring.
    total_time : float
        Total simulation time.
    c : float
        Wave speed in the medium.
    k_confine : float
        Strength of the cubic confining potential.
    gamma : float
        Damping coefficient (radiative loss).
    drive_amp : float
        Amplitude of the twist drive.
    drive_omega : float
        Angular frequency of the twist drive.
    drive_width : int
        Number of lattice points to drive around the center.
    parity_bias : float
        Constant offset in the drive to break symmetry (chiral bias).
    snapshot_interval : int
        Number of time steps between stored snapshots.
    """

    # --- Spatial lattice -----------------------------------------------------
    z = np.linspace(0.0, length, n_points, endpoint=False)
    dz = z[1] - z[0]

    # Choose dt with a CFL-like safety factor for stability
    dt = 0.4 * dz / max(c, 1e-8)
    n_steps = int(total_time / dt)

    # Field and velocity
    x = np.zeros(n_points, dtype=float)
    v = np.zeros(n_points, dtype=float)

    # For storing history
    snapshots_delta = []  # Δ = v
    snapshots_x = []      # underlying field
    times = []

    # Periodic-neighbor indices for Laplacian
    idx = np.arange(n_points)
    ip = (idx + 1) % n_points
    im = (idx - 1) % n_points

    # Localized drive mask (a small region in the middle)
    center = n_points // 2
    drive_mask = np.zeros(n_points, dtype=float)
    half_w = max(1, drive_width // 2)
    drive_mask[center - half_w : center + half_w + 1] = 1.0

    print(
        f"[Δ] Running 1+1D delta-field sim: "
        f"{n_points} sites, {n_steps} steps, dz={dz:.3f}, dt={dt:.4f}"
    )

    # --- Time evolution ------------------------------------------------------
    for step in range(n_steps):
        t = step * dt

        # Twist drive: localized + sinusoid + chiral offset
        F_twist = drive_amp * (np.sin(drive_omega * t) + parity_bias) * drive_mask

        # Nonlinear confinement (QCD-like)
        F_conf = -k_confine * x**3

        # Wave propagation term (discrete Laplacian)
        lap = (x[ip] - 2.0 * x + x[im]) / dz**2
        F_wave = c**2 * lap

        # Net acceleration
        a = F_wave + F_twist + F_conf - gamma * v

        # Simple explicit integration (velocity + position)
        v += a * dt
        x += v * dt

        # Store snapshots
        if step % snapshot_interval == 0:
            snapshots_delta.append(v.copy())
            snapshots_x.append(x.copy())
            times.append(t)

    snapshots_delta = np.array(snapshots_delta)
    snapshots_x = np.array(snapshots_x)
    times = np.array(times)

    return z, times, snapshots_x, snapshots_delta


def demo_plot(z, times, snapshots_x, snapshots_delta, max_frames=300):
    """
    Quick visualization:

    Top:  space-time heatmap of Δ(z,t)
    Bottom: a few snapshots of x(z,t) at selected times
    """
    # If there are too many frames, subsample for plotting
    n_frames = snapshots_delta.shape[0]
    if n_frames > max_frames:
        stride = n_frames // max_frames
        snapshots_delta = snapshots_delta[::stride]
        snapshots_x = snapshots_x[::stride]
        times = times[::stride]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), constrained_layout=True)

    # --- 1) Space-time plot of Δ --------------------------------------------
    im = ax1.imshow(
        snapshots_delta,
        aspect="auto",
        origin="lower",
        extent=[z[0], z[-1], times[0], times[-1]],
    )
    ax1.set_ylabel("Time")
    ax1.set_title("Emergent Δ Field (EM-like wave)")

    cbar = fig.colorbar(im, ax=ax1)
    cbar.set_label("Δ = ∂x/∂t")

    # --- 2) Snapshots of x(z,t) ---------------------------------------------
    n_snap = min(5, len(times))
    indices = np.linspace(0, len(times) - 1, n_snap, dtype=int)

    for idx in indices:
        ax2.plot(z, snapshots_x[idx], label=f"t = {times[idx]:.1f}")

    ax2.set_xlabel("z (space)")
    ax2.set_ylabel("x(z,t)")
    ax2.set_title("Underlying Twisted-Confining Field x(z,t)")
    ax2.legend()

    plt.show()


if __name__ == "__main__":
    # Example run with default parameters
    z, times, x_snaps, delta_snaps = run_delta_field_sim()
    demo_plot(z, times, x_snaps, delta_snaps)
