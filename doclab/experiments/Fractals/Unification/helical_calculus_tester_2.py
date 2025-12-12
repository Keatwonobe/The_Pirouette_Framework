#!/usr/bin/env python
"""
helical_calculus_tester.py

Viability tests for helical calculus on the sphere.

Tests:
1) Circumference "bowling" test: find w* such that a single
   helical path from north pole to south pole has length ~ 2π.

2) Spiral spherical harmonics test: sample Y_l^m along a single
   helix with equal weights and check normalization and some
   cross terms.

3) Helical mesh spherical harmonics test: build a two-helix
   triangle mesh on the sphere, integrate using true spherical
   triangle areas, and re-check normalization + cross terms.
"""

import numpy as np
from scipy.special import sph_harm  # SciPy >=1.15: sph_harm_y is preferred later

# ---------------------------------------------------------------
# Geometry: one-parameter helix on the unit sphere
# ---------------------------------------------------------------

def helix_on_sphere(t, w, phi_offset=0.0):
    """
    Simple helical parameterization of S^2.

    t : array in [0, 1]
    w : winding parameter (how fast we spin in phi as we move in t)
    phi_offset : static azimuthal offset (for second helix wire)

    z(t) = 1 - 2 t   (north pole to south pole)
    r(t) = sqrt(1 - z^2)
    phi(t) = 2π w t + phi_offset
    """
    z = 1.0 - 2.0 * t
    z = np.clip(z, -1.0, 1.0)
    r = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    phi = 2.0 * np.pi * w * t + phi_offset
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return x, y, z, phi


# ---------------------------------------------------------------
# Bowling: full path arc length (pole-to-pole)
# ---------------------------------------------------------------

def arc_length_full_path(w, num_steps=2000):
    """
    Arc length of the helix from t=0 (north pole) to t=1 (south pole).

    This is our "bowling target": tune w so that this full pole-to-pole
    helix has length ≈ 2π (the great-circle circumference of a unit sphere).
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
    Error: how far off is the FULL pole-to-pole helix length
    from the target circumference (2π for unit sphere)?
    """
    L = arc_length_full_path(w, num_steps=num_steps)
    return L - target, L, 1.0  # t_end is always 1.0 here


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

    # Return last mid as best effort
    return w_mid, E_mid, L_mid, t_end_mid


# ---------------------------------------------------------------
# Spiral quadrature tester for spherical harmonics
# ---------------------------------------------------------------

def spiral_sphere_points(N, w):
    """
    Generate N sample points on a single helix over t in [0, 1].

    Each point is treated as representing equal area ~ 4π/N
    for quadrature, i.e. a simple 1D "space-filling" track.
    """
    k = np.arange(N) + 0.5
    t = k / N  # in (0,1)
    x, y, z, phi = helix_on_sphere(t, w)
    theta = np.arccos(z)
    return theta, phi, t


def spiral_sph_norm_test(l, m, N=50000, w=1.618034):
    """
    Test ∫ |Y_l^m|^2 dΩ ≈ 1 using spiral quadrature.

    We sample Y_lm at N points along the helix and approximate
    the integral via a uniform weight 4π/N.
    """
    theta, phi, _ = spiral_sphere_points(N, w)
    Y = sph_harm(m, l, phi, theta)
    dOmega = 4.0 * np.pi / N
    approx = np.sum(np.abs(Y)**2) * dOmega
    return approx, abs(approx - 1.0)


def spiral_sph_cross_test(l1, m1, l2, m2, N=50000, w=1.618034):
    """
    Test orthogonality: ∫ Y_{l1}^{m1} conj(Y_{l2}^{m2}) dΩ ≈ 0
    using spiral quadrature.
    """
    theta, phi, _ = spiral_sphere_points(N, w)
    Y1 = sph_harm(m1, l1, phi, theta)
    Y2 = sph_harm(m2, l2, phi, theta)
    dOmega = 4.0 * np.pi / N
    approx = np.sum(Y1 * np.conjugate(Y2)) * dOmega
    return approx, abs(approx)


# ---------------------------------------------------------------
# Helical triangle mesh construction (two-wire ladder)
# ---------------------------------------------------------------

def spherical_triangle_area(p1, p2, p3):
    """
    Spherical triangle area on the unit sphere via spherical excess.

    p1, p2, p3 : 3D vectors on or near the unit sphere.
    """
    u1 = p1 / np.linalg.norm(p1)
    u2 = p2 / np.linalg.norm(p2)
    u3 = p3 / np.linalg.norm(p3)

    def angle_between(a, b):
        return np.arccos(np.clip(np.dot(a, b), -1.0, 1.0))

    a = angle_between(u2, u3)  # side a opposite vertex at u1
    b = angle_between(u1, u3)  # side b opposite vertex at u2
    c = angle_between(u1, u2)  # side c opposite vertex at u3

    # Spherical law of cosines to get angles A,B,C from sides
    def vertex_angle(A_side, B_side, C_side):
        denom = np.sin(B_side)*np.sin(C_side)
        if denom < 1e-15:
            return 0.0
        cosA = (np.cos(A_side) - np.cos(B_side)*np.cos(C_side)) / denom
        cosA = np.clip(cosA, -1.0, 1.0)
        return np.arccos(cosA)

    A_ang = vertex_angle(a, b, c)
    B_ang = vertex_angle(b, a, c)
    C_ang = vertex_angle(c, a, b)

    E = A_ang + B_ang + C_ang - np.pi
    return E


def build_helical_mesh_samples(N, w, phi_offset):
    """
    Build a helical ladder mesh from two helices and return:

    points: (M,3) array of sample points (triangle barycenters)
    areas:  (M,)  array of spherical triangle areas

    Construction:
    - Helix 1: phi_offset = 0
    - Helix 2: phi_offset = given phi_offset
    - For each i, create two triangles between (i,i+1) on the two wires.
    """
    k = np.arange(N) + 0.5
    t = k / N  # in (0,1)
    x1, y1, z1, _ = helix_on_sphere(t, w, phi_offset=0.0)
    x2, y2, z2, _ = helix_on_sphere(t, w, phi_offset=phi_offset)

    pts = []
    areas = []

    for i in range(N - 1):
        p1_i = np.array([x1[i],     y1[i],     z1[i]])
        p1_ip = np.array([x1[i+1],  y1[i+1],  z1[i+1]])
        p2_i = np.array([x2[i],     y2[i],     z2[i]])
        p2_ip = np.array([x2[i+1],  y2[i+1],  z2[i+1]])

        # Triangle A: p1_i, p2_i, p1_ip
        A1 = spherical_triangle_area(p1_i, p2_i, p1_ip)
        if A1 > 0:
            pA = p1_i + p2_i + p1_ip
            pA /= np.linalg.norm(pA)
            pts.append(pA)
            areas.append(A1)

        # Triangle B: p2_i, p2_ip, p1_ip
        A2 = spherical_triangle_area(p2_i, p2_ip, p1_ip)
        if A2 > 0:
            pB = p2_i + p2_ip + p1_ip
            pB /= np.linalg.norm(pB)
            pts.append(pB)
            areas.append(A2)

    pts = np.vstack(pts)
    areas = np.array(areas)
    return pts, areas


# ---------------------------------------------------------------
# Mesh-based spherical harmonics tests
# ---------------------------------------------------------------

def mesh_sph_norm_test(l, m, pts, areas):
    """
    Norm test using helical triangle mesh.

    ∫ |Y_l^m|^2 dΩ ≈ Σ_j |Y_l^m(p_j)|^2 * A_j
    """
    x = pts[:, 0]
    y = pts[:, 1]
    z = pts[:, 2]
    theta = np.arccos(np.clip(z, -1.0, 1.0))
    phi = np.arctan2(y, x)
    phi = np.where(phi < 0, phi + 2.0*np.pi, phi)

    Y = sph_harm(m, l, phi, theta)
    approx = np.sum(np.abs(Y)**2 * areas)
    return approx, abs(approx - 1.0)


def mesh_sph_cross_test(l1, m1, l2, m2, pts, areas):
    """
    Cross-term test using helical triangle mesh.

    ∫ Y_{l1}^{m1} conj(Y_{l2}^{m2}) dΩ ≈ Σ_j Y_{l1}^{m1}(p_j) conj(Y_{l2}^{m2}(p_j)) A_j
    """
    x = pts[:, 0]
    y = pts[:, 1]
    z = pts[:, 2]
    theta = np.arccos(np.clip(z, -1.0, 1.0))
    phi = np.arctan2(y, x)
    phi = np.where(phi < 0, phi + 2.0*np.pi, phi)

    Y1 = sph_harm(m1, l1, phi, theta)
    Y2 = sph_harm(m2, l2, phi, theta)
    approx = np.sum(Y1 * np.conjugate(Y2) * areas)
    return approx, abs(approx)


# ---------------------------------------------------------------
# Test harnesses
# ---------------------------------------------------------------

def test_circumference():
    print("=== Circumference Bowling Test ===")
    w_low = 0.5
    w_high = 5.0

    E_low, L_low, t_low = circumference_error(w_low)
    E_high, L_high, t_high = circumference_error(w_high)

    print(f"w_low={w_low:.3f} -> L=%.6f, E=%.3e, t_end=%.3f"
          % (L_low, E_low, t_low))
    print(f"w_high={w_high:.3f} -> L=%.6f, E=%.3e, t_end=%.3f"
          % (L_high, E_high, t_high))

    # Ensure bracket straddles zero; if not, adjust
    if E_low * E_high > 0:
        print("Initial bracket does not straddle zero; expanding search range...")
        # crude expansion
        w_low = 0.1
        E_low, L_low, t_low = circumference_error(w_low)
        print(f"  try w_low={w_low:.3f} -> E={E_low:.6e}")
        if E_low * E_high > 0:
            w_low = 0.01
            E_low, L_low, t_low = circumference_error(w_low)
            print(f"  try w_low={w_low:.3f} -> E={E_low:.6e}")
            if E_low * E_high > 0:
                raise RuntimeError("Could not find a sign change for circumference error.")

    w_star, E_star, L_star, t_star = find_w_star(w_low, w_high)
    print(f"\nFound w* ≈ {w_star:.10f}")
    print(f"Loop length L(w*) = {L_star:.10f}, target = {2*np.pi:.10f}")
    print(f"Error E(w*)       = {E_star:.3e}")
    print(f"t_end(w*)         = {t_star:.6f} (fraction of [0,1])\n")

    return w_star


def test_spiral_spherical_harmonics(w_for_spiral):
    print("=== Spiral Spherical Harmonics Test (single wire) ===")
    tests_norm = [(0, 0), (1, 0), (1, 1), (2, 0), (3, 2)]
    tests_cross = [((1, 0), (1, 1)),
                   ((2, 0), (2, 1)),
                   ((2, 1), (3, 1))]

    N = 50000
    print(f"Using N={N}, w={w_for_spiral:.6f}\n")

    # Norm tests
    for (l, m) in tests_norm:
        approx, err = spiral_sph_norm_test(l, m, N=N, w=w_for_spiral)
        print(f"Norm (spiral) (l={l}, m={m}): "
              f"≈ {approx:.6f}, |err|={err:.3e}")

    # Cross tests
    for (l1_m1, l2_m2) in tests_cross:
        (l1, m1) = l1_m1
        (l2, m2) = l2_m2
        approx, mag = spiral_sph_cross_test(l1, m1, l2, m2, N=N, w=w_for_spiral)
        print(
            f"Cross (spiral) Y_{l1}^{m1} vs Y_{l2}^{m2}: "
            f"≈ {approx.real:.3e}+{approx.imag:.3e}i, |.|={mag:.3e}"
        )
    print("")


def test_mesh_spherical_harmonics(w_star):
    print("=== Helical Mesh Spherical Harmonics Test (two-wire ladder) ===")
    phi_offset = np.pi / max(w_star, 1e-6)

    N = 2000
    pts, areas = build_helical_mesh_samples(N, w_star, phi_offset)

    total_area = np.sum(areas)
    scale = 4.0 * np.pi / total_area
    areas_scaled = areas * scale

    modes = [(0,0), (1,0), (1,1), (2,0), (2,1)]
    print("\n=== Gram / Reconstruction Test (mesh) ===")
    test_reconstruction(modes, pts, areas_scaled)

    print(f"Mesh: N={N}, w*={w_star:.10f}, phi_offset={phi_offset:.6f}")
    print(f"Total spherical area from mesh (raw)   ≈ {total_area:.10f}")
    print(f"Rescaled total area (should be 4π)     ≈ {areas_scaled.sum():.10f} "
          f"(4π={4*np.pi:.10f})\n")

    tests_norm = [(0, 0), (1, 0), (1, 1), (2, 0), (3, 2)]
    tests_cross = [((1, 0), (1, 1)),
                   ((2, 0), (2, 1)),
                   ((2, 1), (3, 1))]

    # Norms
    for (l, m) in tests_norm:
        approx, err = mesh_sph_norm_test(l, m, pts, areas_scaled)
        print(f"Norm (mesh)   (l={l}, m={m}): "
              f"≈ {approx:.6f}, |err|={err:.3e}")

    # Cross
    for (l1_m1, l2_m2) in tests_cross:
        (l1, m1) = l1_m1
        (l2, m2) = l2_m2
        approx, mag = mesh_sph_cross_test(l1, m1, l2, m2, pts, areas_scaled)
        print(
            f"Cross (mesh)  Y_{l1}^{m1} vs Y_{l2}^{m2}: "
            f"≈ {approx.real:.3e}+{approx.imag:.3e}i, |.|={mag:.3e}"
        )
    print("")

def build_gram_matrix(modes, pts, areas):
    """
    Build Gram matrix G_{ab} = ∫ Y_a conj(Y_b) dΩ ≈ Σ_j Y_a(p_j) conj(Y_b(p_j)) A_j

    modes: list of (l, m) pairs
    pts:   (M,3) sample points on sphere
    areas: (M,)  weights (already normalized to sum to 4π)
    """
    x = pts[:, 0]
    y = pts[:, 1]
    z = pts[:, 2]
    theta = np.arccos(np.clip(z, -1.0, 1.0))
    phi = np.arctan2(y, x)
    phi = np.where(phi < 0, phi + 2.0*np.pi, phi)

    M = len(modes)
    G = np.zeros((M, M), dtype=complex)

    # Precompute all Y_lm at sample points
    Y_all = []
    for (l, m) in modes:
        Y = sph_harm(m, l, phi, theta)
        Y_all.append(Y)

    for i in range(M):
        for j in range(M):
            G[i, j] = np.sum(Y_all[i] * np.conjugate(Y_all[j]) * areas)

    return G


def test_reconstruction(modes, pts, areas):
    """
    Simple reconstruction test:
    - Define f(Ω) = Σ c_a Y_a(Ω) with known coefficients c
    - Use the mesh to compute b_a ≈ ∫ f conj(Y_a) dΩ
    - Solve G a ≈ b and compare a to c
    """
    from numpy.linalg import solve, cond

    x = pts[:, 0]
    y = pts[:, 1]
    z = pts[:, 2]
    theta = np.arccos(np.clip(z, -1.0, 1.0))
    phi = np.arctan2(y, x)
    phi = np.where(phi < 0, phi + 2.0*np.pi, phi)

    M = len(modes)

    # Build basis values
    Y_all = []
    for (l, m) in modes:
        Y_all.append(sph_harm(m, l, phi, theta))

    # Choose some synthetic coefficients
    # e.g. f = 1.0*Y_0^0 + 0.7*Y_1^0 + 0.3*Y_2^1
    c_true = np.zeros(M, dtype=complex)
    for i, (l, m) in enumerate(modes):
        if (l, m) == (0, 0):
            c_true[i] = 1.0
        elif (l, m) == (1, 0):
            c_true[i] = 0.7
        elif (l, m) == (2, 1):
            c_true[i] = 0.3

    # Build f(Ω)
    f_vals = np.zeros_like(theta, dtype=complex)
    for i in range(M):
        f_vals += c_true[i] * Y_all[i]

    # Compute b_a ≈ ∫ f conj(Y_a) dΩ
    b = np.zeros(M, dtype=complex)
    for i in range(M):
        b[i] = np.sum(f_vals * np.conjugate(Y_all[i]) * areas)

    # Build Gram matrix
    G = build_gram_matrix(modes, pts, areas)
    kappa = cond(G)
    a_est = solve(G, b)

    print("Modes:", modes)
    print("Condition number(G) ≈", kappa)
    for i, (l, m) in enumerate(modes):
        print(f"Mode (l={l}, m={m}): true={c_true[i]:.3f}, est={a_est[i]:.3f}, "
              f"abs_err={abs(a_est[i]-c_true[i]):.3e}")

def main():
    # 1) Bowl for the geometric helical parameter
    w_star = test_circumference()

    # 2) Spiral SHT test — you can try golden ratio or w_star.
    #    First, replicate your previous golden-spiral results:
    golden_w = (1 + 5**0.5) / 2.0
    test_spiral_spherical_harmonics(golden_w)

    #    Then see how using w_star changes things:
    test_spiral_spherical_harmonics(w_star)

    # 3) Mesh SHT test — use the tuned w_star and two-wire ladder
    test_mesh_spherical_harmonics(w_star)

if __name__ == "__main__":
    main()
