#!/usr/bin/env python
"""
helical_spiral_tester.py

Quick-and-dirty viability check for using a single helical curve
on the sphere as a quadrature track and for "bowling" to tune
its parameters.

Tests:
1) Circumference "bowling" test: find w* so that one loop of the
   helix has arc length ~ 2π (for unit sphere).
2) Spherical harmonic test: sample Y_lm on the spiral and check
   if ∫ |Y_lm|^2 dΩ ≈ 1 and cross-terms ≈ 0 using spiral quadrature.

Dependencies: numpy, scipy (for sph_harm).
"""

import numpy as np
from scipy.special import sph_harm

# ---------------------------------------------------------------
# Geometry: one-parameter helix on the unit sphere
# ---------------------------------------------------------------

def helix_on_sphere(t, w):
    """
    Simple helical parameterization of S^2.

    t : array in [0, 1]
    w : winding parameter (how fast we spin in phi as we move in t)

    z(t) = 1 - 2 t   (north pole to south pole)
    r(t) = sqrt(1 - z^2)
    phi(t) = 2π w t
    """
    z = 1.0 - 2.0*t
    # numerical safety
    z = np.clip(z, -1.0, 1.0)
    r = np.sqrt(np.maximum(0.0, 1.0 - z*z))
    phi = 2.0 * np.pi * w * t
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return x, y, z, phi


# ---------------------------------------------------------------
# Bowling: arc length of (approx.) one loop
# ---------------------------------------------------------------

def arc_length_full_path(w, num_steps=2000):
    """
    Arc length of the helix from t=0 (north pole) to t=1 (south pole).

    This is now our bowling target: we tune w so that this full
    pole-to-pole helix has length ≈ 2π (the great-circle circumference
    of a unit sphere).
    """
    if w < 0:
        raise ValueError("w must be non-negative")

    t = np.linspace(0.0, 1.0, num_steps)
    x, y, z, _ = helix_on_sphere(t, w)
    dx = np.diff(x)
    dy = np.diff(y)
    dz = np.diff(z)
    ds = np.sqrt(dx*dx + dy*dy + dz*dz)
    return ds.sum()


def circumference_error(w, target=2*np.pi, num_steps=2000):
    """
    Error function: how far off is the FULL pole-to-pole helix length
    from the target circumference (2π for unit sphere)?
    """
    L = arc_length_full_path(w, num_steps=num_steps)
    return L - target, L, 1.0  # t_end is always 1.0 now



def find_w_star(w_low, w_high, tol=1e-8, max_iter=40, num_steps=2000):
    """
    Bracket and refine a w* such that circumference_error(w*) ~ 0.

    Uses simple bisection for robustness.
    Returns (w_star, error(w_star), L_star, t_end_star).
    """
    E_low, _, _ = circumference_error(w_low, num_steps=num_steps)
    E_high, _, _ = circumference_error(w_high, num_steps=num_steps)

    if E_low * E_high > 0:
        raise RuntimeError(
            f"Bracket does not straddle zero: "
            f"E({w_low})={E_low:.6e}, E({w_high})={E_high:.6e}"
        )

    for _ in range(max_iter):
        w_mid = 0.5 * (w_low + w_high)
        E_mid, L_mid, t_end_mid = circumference_error(
            w_mid, num_steps=num_steps
        )
        if abs(E_mid) < tol:
            return w_mid, E_mid, L_mid, t_end_mid

        if E_mid * E_low < 0:
            w_high = w_mid
            E_high = E_mid
        else:
            w_low = w_mid
            E_low = E_mid

    # Last mid as best effort if we didn't converge in max_iter
    return w_mid, E_mid, L_mid, t_end_mid


# ---------------------------------------------------------------
# Spiral quadrature tester for spherical harmonics
# ---------------------------------------------------------------

def spiral_sphere_points(N, w):
    """
    Generate N sample points on the helix over t in [0, 1].

    Each point is treated as representing equal area ~ 4π/N
    for quadrature, i.e. a simple 1D "space-filling" track.
    """
    k = np.arange(N) + 0.5
    t = k / N  # in (0,1)
    x, y, z, phi = helix_on_sphere(t, w)
    theta = np.arccos(z)
    return theta, phi, t


def spiral_sph_norm_test(l, m, N=50000, w=1.618):
    """
    Test ∫ |Y_l^m|^2 dΩ ≈ 1 using spiral quadrature.

    We sample Y_lm at N points along the helix and approximate
    the integral via a uniform weight 4π/N.

    Returns (approx_value, error_abs).
    """
    theta, phi, _ = spiral_sphere_points(N, w)
    Y = sph_harm(m, l, phi, theta)
    dOmega = 4.0 * np.pi / N
    approx = np.sum(np.abs(Y)**2) * dOmega
    return approx, abs(approx - 1.0)


def spiral_sph_cross_test(l1, m1, l2, m2, N=50000, w=1.618):
    """
    Test orthogonality: ∫ Y_{l1}^{m1} conj(Y_{l2}^{m2}) dΩ ≈ 0
    using spiral quadrature.

    Returns the approximate value and its magnitude.
    """
    theta, phi, _ = spiral_sphere_points(N, w)
    Y1 = sph_harm(m1, l1, phi, theta)
    Y2 = sph_harm(m2, l2, phi, theta)
    dOmega = 4.0 * np.pi / N
    approx = np.sum(Y1 * np.conjugate(Y2)) * dOmega
    return approx, abs(approx)


# ---------------------------------------------------------------
# Main test harness
# ---------------------------------------------------------------

def test_circumference():
    print("=== Circumference Bowling Test ===")
    # crude initial bracket guesses; tweak if needed
    w_low = 0.5
    w_high = 5.0

    E_low, L_low, t_low = circumference_error(w_low)
    E_high, L_high, t_high = circumference_error(w_high)

    print(f"w_low={w_low:.3f} -> L={L_low:.6f}, E={E_low:.6e}, t_end={t_low:.3f}")
    print(f"w_high={w_high:.3f} -> L={L_high:.6f}, E={E_high:.6e}, t_end={t_high:.3f}")

    # If signs don't differ, try to expand the bracket
    if E_low * E_high > 0:
        print("Initial bracket does not straddle zero; expanding search range...")
        for factor in [0.25, 0.1, 0.05]:
            w_low = factor
            E_low, L_low, t_low = circumference_error(w_low)
            print(f"  try w_low={w_low:.3f} -> E={E_low:.6e}")
            if E_low * E_high < 0:
                break
        else:
            raise RuntimeError("Could not find a sign change for circumference error.")

    w_star, E_star, L_star, t_star = find_w_star(w_low, w_high)
    print(f"\nFound w* ≈ {w_star:.10f}")
    print(f"Loop length L(w*) = {L_star:.10f}, target = {2*np.pi:.10f}")
    print(f"Error E(w*)       = {E_star:.3e}")
    print(f"t_end(w*)         = {t_star:.6f} (fraction of [0,1] used for ~1 loop)")


def test_spherical_harmonics():
    print("\n=== Spiral Spherical Harmonics Test ===")
    # pick some modes to check
    tests_norm = [(0, 0), (1, 0), (1, 1), (2, 0), (3, 2)]
    tests_cross = [((1, 0), (1, 1)), ((2, 0), (2, 1)), ((2, 1), (3, 1))]

    N = 50000
    w = (1 + 5**0.5) / 2  # golden-ish winding

    print(f"Using N={N}, w={w:.6f}")

    # Normalization tests
    for (l, m) in tests_norm:
        approx, err = spiral_sph_norm_test(l, m, N=N, w=w)
        print(f"Norm test (l={l}, m={m}): ∫|Y_l^m|^2 dΩ ≈ {approx:.6f}, |err|={err:.3e}")

    # Cross orthogonality tests
    for (l1_m1, l2_m2) in tests_cross:
        (l1, m1) = l1_m1
        (l2, m2) = l2_m2
        approx, mag = spiral_sph_cross_test(l1, m1, l2, m2, N=N, w=w)
        print(
            f"Cross test Y_{l1}^{m1} vs Y_{l2}^{m2}: "
            f"integral ≈ {approx.real:.3e}+{approx.imag:.3e}i, |.|={mag:.3e}"
        )


def main():
    test_circumference()
    test_spherical_harmonics()


if __name__ == "__main__":
    main()
