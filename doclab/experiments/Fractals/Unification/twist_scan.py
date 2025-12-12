# unification_34_twist_scan.py
#
# TWIST Scan for Pirouette Vacuum
# --------------------------------
# For each TWIST:
#   1) Static: classify points on a ring by local angular sector
#   2) Dynamic: let them flow under the vacuum field and see which
#      sector dominates at late times
#
# This shows:
#   - Geometry of three sectors (Gold/Teal/Red) on the ring
#   - That the geodesic flow has a single red-dominated attractor
#     in the region we’re probing.

import numpy as np
import matplotlib.pyplot as plt

import pirouette_physics as pp  # uses Constants + geometry

# --------------------------------------------------
# Parameters
# --------------------------------------------------
R0           = 2.2      # radius of the ring in (m, λ)
N_THETA      = 360      # points on the ring
DT           = 0.02
N_STEPS      = 400
R_ESCAPE     = 10.0

TWIST_VALUES = np.linspace(2.5, 5.0, 21)


# --------------------------------------------------
# Geometry helpers (copied from pirouette_physics)
# --------------------------------------------------
def sector_weights_from_angle(angle_deg):
    """Return normalized (w_gold, w_teal, w_red) from polar angle."""
    angle = angle_deg % 360.0

    diff_g = np.abs(angle - 30.0)
    diff_g = np.minimum(diff_g, 360.0 - diff_g)
    w_gold = np.exp(-(diff_g / 80.0) ** 2)

    diff_t = np.abs(angle - 150.0)
    diff_t = np.minimum(diff_t, 360.0 - diff_t)
    w_teal = np.exp(-(diff_t / 80.0) ** 2)

    diff_r = np.abs(angle - 270.0)
    diff_r = np.minimum(diff_r, 360.0 - diff_r)
    w_red = np.exp(-(diff_r / 80.0) ** 2)

    tot = w_gold + w_teal + w_red + 1e-9
    return w_gold / tot, w_teal / tot, w_red / tot


def vacuum_force_with_twist(m, lam, twist):
    """
    Same structure as get_vacuum_force, but with TWIST as argument
    so we can scan instead of using a fixed constant.
    """
    # Teal (EM / hypercharge)
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red (weak) with CP twist
    F_red_m    = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5)
    F_red_lam  = -(lam + 1.0) + p_violation

    # Gold (strong) = geometric tension
    sum_m   = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m * scale
    F_gold_lam = sum_lam * scale

    # Angular mixing
    angle = np.degrees(np.arctan2(lam, m)) % 360.0
    w_gold, w_teal, w_red = sector_weights_from_angle(angle)

    Fm   = w_teal * F_teal_m   + w_red * F_red_m   + w_gold * F_gold_m
    Flam = w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam
    return Fm, Flam


# --------------------------------------------------
# Static classification (instantaneous sectors)
# --------------------------------------------------
def classify_static_ring():
    theta = np.linspace(0.0, 2.0 * np.pi, N_THETA, endpoint=False)
    counts = np.zeros(3, dtype=int)  # [Gold, Teal, Red]

    for ang in theta:
        m   = R0 * np.cos(ang)
        lam = R0 * np.sin(ang)
        angle = np.degrees(np.arctan2(lam, m))
        w_gold, w_teal, w_red = sector_weights_from_angle(angle)
        sector = int(np.argmax([w_gold, w_teal, w_red]))
        counts[sector] += 1

    return counts / counts.sum()


# --------------------------------------------------
# Dynamic classification (late-time sectors)
# --------------------------------------------------
def classify_dynamic_ring(twist):
    theta = np.linspace(0.0, 2.0 * np.pi, N_THETA, endpoint=False)
    counts = np.zeros(4, dtype=int)  # [Gold, Teal, Red, Escape]

    for ang in theta:
        m   = R0 * np.cos(ang)
        lam = R0 * np.sin(ang)

        escaped = False
        for _ in range(N_STEPS):
            Fm, Flam = vacuum_force_with_twist(m, lam, twist)
            m   += DT * Fm
            lam += DT * Flam

            if m * m + lam * lam > R_ESCAPE * R_ESCAPE:
                counts[3] += 1
                escaped = True
                break

        if not escaped:
            angle = np.degrees(np.arctan2(lam, m))
            w_gold, w_teal, w_red = sector_weights_from_angle(angle)
            sector = int(np.argmax([w_gold, w_teal, w_red]))
            counts[sector] += 1

    return counts / counts.sum()


# --------------------------------------------------
# Scan + plot
# --------------------------------------------------
def run_twist_scan():
    static_fracs = classify_static_ring()  # independent of TWIST
    print("\n[Δ] Static geometric fractions on ring R0=%.2f" % R0)
    print("Gold=%.3f, Teal=%.3f, Red=%.3f"
          % (static_fracs[0], static_fracs[1], static_fracs[2]))

    dyn_gold = []
    dyn_teal = []
    dyn_red  = []
    dyn_esc  = []

    print("\n[Δ] Dynamic TWIST scan over basins (late-time sectors)")
    print("TWIST    Gold    Teal    Red   Escape")

    for twist in TWIST_VALUES:
        fracs = classify_dynamic_ring(twist)
        g, t, r, e = fracs
        dyn_gold.append(g)
        dyn_teal.append(t)
        dyn_red.append(r)
        dyn_esc.append(e)
        print(f"{twist:5.2f}  {g:6.3f}  {t:6.3f}  {r:6.3f}  {e:6.3f}")

    # Plot only the static fractions (dynamic is almost all red)
    plt.figure(figsize=(10, 6), facecolor="black")
    ax = plt.gca()
    ax.set_facecolor("black")

    ax.hlines(static_fracs[0], TWIST_VALUES[0], TWIST_VALUES[-1],
              linestyles="-", label="Gold (static)", linewidth=2.0)
    ax.hlines(static_fracs[1], TWIST_VALUES[0], TWIST_VALUES[-1],
              linestyles="--", label="Teal (static)", linewidth=2.0)
    ax.hlines(static_fracs[2], TWIST_VALUES[0], TWIST_VALUES[-1],
              linestyles=":", label="Red (static)", linewidth=2.0)

    ax.set_xlabel("TWIST parameter", color="white")
    ax.set_ylabel("Fraction of ring in sector", color="white")
    ax.set_title("Static Sector Fractions on Electron Shell Ring",
                 color="white")

    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("white")

    leg = ax.legend(facecolor="black", edgecolor="white")
    for txt in leg.get_texts():
        txt.set_color("white")

    plt.tight_layout()
    plt.savefig("twist_scan_static_vs_dynamic.png", dpi=220)
    plt.show()


if __name__ == "__main__":
    run_twist_scan()
