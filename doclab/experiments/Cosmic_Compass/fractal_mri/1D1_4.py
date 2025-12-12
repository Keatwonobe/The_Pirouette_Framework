import numpy as np

# ----------------------------------------------------------
# 1. Force = your "Genesis" tension-mode with twist param
#    (same structure as get_force_bifurcation / poincare)
# ----------------------------------------------------------
def get_force_color(m, lam, twist=1.5):
    """
    Net tension-mode force in (m, lam) for a given twist.
    This mirrors the physics in qcd_lock_11/12. 
    """
    # Teal anchor: harmonic to (-0.866, 0.5)
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red anchor: toward (0, -1) with parity violation
    F_red_m = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold = vector sum (tension)
    F_gold_m = F_teal_m + F_red_m
    F_gold_lam = F_teal_lam + F_red_lam

    # Angular basin weights
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


# ----------------------------------------------------------
# 2. Jacobian and local "generator" matrices
# ----------------------------------------------------------
def jacobian(m, lam, twist=1.5, eps=1e-3):
    """
    Finite-difference Jacobian of F at a point.
    J_ij = dF_i / dX_j, X = (m, lam)
    """
    Fm0, Flam0 = get_force_color(m, lam, twist)

    # perturb m
    Fm_p, Flam_p = get_force_color(m + eps, lam, twist)
    Fm_m, Flam_m = get_force_color(m - eps, lam, twist)

    # perturb lam
    Fm_l, Flam_l = get_force_color(m, lam + eps, twist)
    Fm_lp, Flam_lp = get_force_color(m, lam - eps, twist)

    dFm_dm    = (Fm_p    - Fm_m)    / (2 * eps)
    dFlam_dm  = (Flam_p  - Flam_m)  / (2 * eps)
    dFm_dlam  = (Fm_l    - Fm_lp)   / (2 * eps)
    dFlam_dlam= (Flam_l  - Flam_lp) / (2 * eps)

    J = np.array([[dFm_dm, dFm_dlam],
                  [dFlam_dm, dFlam_dlam]], dtype=float)
    return J


def commutator(A, B):
    return A @ B - B @ A


def flatten2(M):
    """Flatten 2x2 -> 4-vector for linear algebra."""
    return M.reshape(4)


# ----------------------------------------------------------
# 3. Pick representative "color sector" points
# ----------------------------------------------------------
def pick_sector_points(radius=1.0):
    """
    Points chosen by angle to sit deep in each basin.
    Angles match your Gaussians: gold~30, teal~150, red~270.
    """
    # convert polar to (m, lam)
    def polar(theta_deg):
        th = np.radians(theta_deg)
        return radius * np.cos(th), radius * np.sin(th)

    # Each is a point mostly dominated by one color
    m_gold, lam_gold = polar(30.0)
    m_teal, lam_teal = polar(150.0)
    m_red, lam_red   = polar(270.0)

    return (m_teal, lam_teal), (m_red, lam_red), (m_gold, lam_gold)


# ----------------------------------------------------------
# 4. Project commutators back onto {Teal, Red, Gold}
# ----------------------------------------------------------
def extract_structure_constants(twist=1.5, radius=1.0):
    # Pick sample points in each basin
    (mT, lT), (mR, lR), (mG, lG) = pick_sector_points(radius=radius)

    JT = jacobian(mT, lT, twist)
    JR = jacobian(mR, lR, twist)
    JG = jacobian(mG, lG, twist)

    # Basis as columns in 4D
    basis = np.column_stack([flatten2(JT), flatten2(JR), flatten2(JG)])

    # Precompute pseudo-inverse for projection
    B_pinv = np.linalg.pinv(basis)

    def project(M):
        """Return coefficients (cT, cR, cG) such that M ≈ Σ c_i J_i."""
        v = flatten2(M)
        coeffs = B_pinv @ v
        return coeffs

    # Compute commutators
    comms = {
        ("T", "R"): commutator(JT, JR),
        ("R", "G"): commutator(JR, JG),
        ("G", "T"): commutator(JG, JT),
    }

    print("=== Color Generators (Jacobian matrices) ===")
    print("JT (Teal):\n", JT)
    print("JR (Red):\n", JR)
    print("JG (Gold):\n", JG)
    print()

    print("=== Structure constants f_ab^c in {T,R,G} basis ===")
    for (a, b), C in comms.items():
        cT, cR, cG = project(C)
        print(f"[J_{a}, J_{b}] ≈ "
              f"{cT:+.3f} J_T  "
              f"{cR:+.3f} J_R  "
              f"{cG:+.3f} J_G")

    return JT, JR, JG


if __name__ == "__main__":
    print("Extracting SU(3)-like tripod from tension-mode geometry...")
    JT, JR, JG = extract_structure_constants(twist=1.5, radius=1.0)
