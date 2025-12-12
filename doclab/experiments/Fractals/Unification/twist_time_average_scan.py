# twist_time_average_scan.py
#
# Time-averaged sector weights along geodesics on the electron shell ring.
#
# For each TWIST in TWIST_VALUES:
#   - Sample initial conditions on a ring R0 in (m, λ) space
#   - Evolve each trajectory under the vacuum flow
#   - At each time step, record the angular sector weights (Gold/Teal/Red)
#   - Compute time-averaged weights per trajectory
#   - Average over all trajectories on the ring
#
# Output:
#   - Console table of <w_gold>, <w_teal>, <w_red> vs TWIST
#   - Plot: twist_time_average_scan.png

import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Parameters (same scale as your other unification scripts)
# --------------------------------------------------
R0        = 2.2        # ring radius (electron shell-ish)
N_THETA   = 360        # number of starting angles on ring
DT        = 0.02
N_STEPS   = 400        # integration steps per trajectory
R_ESCAPE  = 10.0       # treat as escape if radius exceeds this

TWIST_VALUES = np.linspace(2.5, 5.0, 21)


# --------------------------------------------------
# Sector geometry helpers
# --------------------------------------------------
def sector_weights_from_angle(angle_deg: float):
    """
    Return normalized angular weights (w_gold, w_teal, w_red)
    given a polar angle in degrees.
    """
    angle = angle_deg % 360.0

    # Gold sector centered ~30°
    diff_g = np.abs(angle - 30.0)
    diff_g = np.minimum(diff_g, 360.0 - diff_g)
    w_gold = np.exp(-(diff_g / 80.0) ** 2)

    # Teal sector centered ~150°
    diff_t = np.abs(angle - 150.0)
    diff_t = np.minimum(diff_t, 360.0 - diff_t)
    w_teal = np.exp(-(diff_t / 80.0) ** 2)

    # Red sector centered ~270°
    diff_r = np.abs(angle - 270.0)
    diff_r = np.minimum(diff_r, 360.0 - diff_r)
    w_red = np.exp(-(diff_r / 80.0) ** 2)

    tot = w_gold + w_teal + w_red + 1e-12
    return w_gold / tot, w_teal / tot, w_red / tot


def vacuum_force_with_twist(m: float, lam: float, twist: float):
    """
    Same basic field as in your unification scripts, but with TWIST explicit.
    Returns (Fm, Flam) at (m, lam).
    """

    # --- Teal (EM / hypercharge-ish) ---
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # --- Red (weak) with CP-violating twist ---
    F_red_m    = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5)
    F_red_lam  = -(lam + 1.0) + p_violation

    # --- Gold (strong) ---
    sum_m   = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m * scale
    F_gold_lam = sum_lam * scale

    # Angular mixing: sector weights from polar angle
    angle = np.degrees(np.arctan2(lam, m)) % 360.0
    w_gold, w_teal, w_red = sector_weights_from_angle(angle)

    Fm   = w_teal * F_teal_m   + w_red * F_red_m   + w_gold * F_gold_m
    Flam = w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam
    return Fm, Flam


# --------------------------------------------------
# Time-averaged sectors for a single trajectory
# --------------------------------------------------
def time_averaged_sectors_for_trajectory(m0: float, lam0: float, twist: float):
    """
    Integrate one trajectory and return
    (mean_w_gold, mean_w_teal, mean_w_red)
    based on angular sector weights sampled along the path.

    If the trajectory escapes early, averages are taken over the
    steps actually simulated.
    """
    m = float(m0)
    lam = float(lam0)

    sum_gold = 0.0
    sum_teal = 0.0
    sum_red  = 0.0
    steps    = 0

    for _ in range(N_STEPS):
        angle = np.degrees(np.arctan2(lam, m))
        w_gold, w_teal, w_red = sector_weights_from_angle(angle)

        sum_gold += w_gold
        sum_teal += w_teal
        sum_red  += w_red
        steps    += 1

        # advance
        Fm, Flam = vacuum_force_with_twist(m, lam, twist)
        m   += DT * Fm
        lam += DT * Flam

        if m * m + lam * lam > R_ESCAPE * R_ESCAPE:
            break

    if steps == 0:
        return 0.0, 0.0, 0.0

    return sum_gold / steps, sum_teal / steps, sum_red / steps


# --------------------------------------------------
# Scan over TWIST
# --------------------------------------------------
def run_twist_time_average_scan():
    theta = np.linspace(0.0, 2.0 * np.pi, N_THETA, endpoint=False)

    mean_gold_all = []
    mean_teal_all = []
    mean_red_all  = []

    print("\n[Δ] Time-averaged sector weights on ring R0=%.2f" % R0)
    print("TWIST   <Gold>   <Teal>   <Red>")

    for twist in TWIST_VALUES:
        traj_gold = []
        traj_teal = []
        traj_red  = []

        for ang in theta:
            m0   = R0 * np.cos(ang)
            lam0 = R0 * np.sin(ang)
            g, t, r = time_averaged_sectors_for_trajectory(m0, lam0, twist)
            traj_gold.append(g)
            traj_teal.append(t)
            traj_red.append(r)

        mean_g = float(np.mean(traj_gold))
        mean_t = float(np.mean(traj_teal))
        mean_r = float(np.mean(traj_red))

        mean_gold_all.append(mean_g)
        mean_teal_all.append(mean_t)
        mean_red_all.append(mean_r)

        print(f"{twist:5.2f}  {mean_g:7.4f}  {mean_t:7.4f}  {mean_r:7.4f}")

    mean_gold_all = np.array(mean_gold_all)
    mean_teal_all = np.array(mean_teal_all)
    mean_red_all  = np.array(mean_red_all)

    # --------------------------------------------------
    # Plot
    # --------------------------------------------------
    plt.figure(figsize=(10, 6), facecolor="black")
    ax = plt.gca()
    ax.set_facecolor("black")

    ax.plot(TWIST_VALUES, mean_gold_all, label="⟨Gold⟩ (strong)", linewidth=2.0)
    ax.plot(TWIST_VALUES, mean_teal_all, label="⟨Teal⟩ (EM/visible)", linewidth=2.0, linestyle="--")
    ax.plot(TWIST_VALUES, mean_red_all,  label="⟨Red⟩ (weak backbone)", linewidth=2.0, linestyle=":")

    ax.set_xlabel("TWIST parameter", color="white")
    ax.set_ylabel("Time-averaged sector weight", color="white")
    ax.set_title("Time-Averaged Sector Weights on Electron Shell Ring",
                 color="white")

    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("white")

    leg = ax.legend(facecolor="black", edgecolor="white")
    for txt in leg.get_texts():
        txt.set_color("white")

    plt.tight_layout()
    plt.savefig("twist_time_average_scan.png", dpi=220)
    plt.show()


if __name__ == "__main__":
    run_twist_time_average_scan()
