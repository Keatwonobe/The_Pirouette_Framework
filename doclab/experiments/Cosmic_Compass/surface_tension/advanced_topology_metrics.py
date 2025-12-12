# advanced_topology_metrics.py

import numpy as np
import pickle
import matplotlib.pyplot as plt

# ---------- 1. Chern-like index per strand ----------

def tangent_angle_winding(x, y):
    """
    Compute winding number of the tangent direction of a planar curve.
    Returns an integer (Chern-like index).
    """
    # Central differences for derivatives
    dx = np.gradient(x)
    dy = np.gradient(y)

    # Tangent angle
    theta = np.arctan2(dy, dx)

    # Unwrap to avoid 2π jumps
    theta_unwrapped = np.unwrap(theta)

    # Total change in angle
    dtheta_total = theta_unwrapped[-1] - theta_unwrapped[0]

    # Winding number
    winding = int(np.rint(dtheta_total / (2 * np.pi)))
    return winding


def compute_chern_indices(manifolds):
    """
    Compute Chern-like indices (tangent winding numbers) for each strand.
    Returns a list of dicts with metadata.
    """
    results = []

    for kind in ['stable', 'unstable']:
        for m in manifolds[kind]:
            x = m['x']
            y = m['y']

            if len(x) < 5:
                continue

            w = tangent_angle_winding(x, y)

            results.append({
                'type': kind,
                'saddle': m['saddle'],
                'angle': m['angle'],
                'chern_index': w
            })

    return results


def summarize_chern_indices(results):
    print("\n=== CHERN-LIKE INDICES (TANGENT WINDINGS) ===")
    by_saddle = {(kind, s): [] for kind in ['stable', 'unstable'] for s in range(3)}
    for r in results:
        by_saddle[(r['type'], r['saddle'])].append(r['chern_index'])

    for kind in ['stable', 'unstable']:
        print(f"\n{kind.upper()} strands:")
        for s in range(3):
            vals = by_saddle[(kind, s)]
            if not vals:
                continue
            vals = np.array(vals)
            print(f"  Saddle {s+1}: mean={vals.mean(): .2f}, "
                  f"std={vals.std(): .2f}, unique={sorted(set(vals))}")

# ---------- 2. Linking numbers in 3D (x, y, lyap) ----------

def resample_curve3d(x, y, z, n_samples=200):
    """Resample a curve to n_samples along index space (not perfect arc length,
    but good enough for qualitative linking)."""
    N = len(x)
    if N <= n_samples:
        return x, y, z
    idx = np.linspace(0, N - 1, n_samples).astype(int)
    return x[idx], y[idx], z[idx]


def linking_number(curve1, curve2):
    """
    Approximate Gauss linking number between two 3D curves.
    curve = (x, y, z) arrays.
    """
    x1, y1, z1 = curve1
    x2, y2, z2 = curve2

    # Segment midpoints and segment vectors
    X1 = np.vstack((x1, y1, z1)).T
    X2 = np.vstack((x2, y2, z2)).T

    dX1 = np.diff(X1, axis=0)
    dX2 = np.diff(X2, axis=0)

    mid1 = 0.5 * (X1[:-1] + X1[1:])
    mid2 = 0.5 * (X2[:-1] + X2[1:])

    lk = 0.0
    for i in range(len(dX1)):
        r1 = mid1[i]
        dr1 = dX1[i]
        # Vectorized over all segments of curve2
        r2 = mid2
        dr2 = dX2

        diff = r1 - r2                # [M, 3]
        dist = np.linalg.norm(diff, axis=1)
        # Avoid singularities
        mask = dist > 1e-6
        if not np.any(mask):
            continue

        diff = diff[mask]
        dist = dist[mask]
        dr2m = dr2[mask]

        cp = np.cross(dr1, dr2m)          # [M, 3]
        num = np.einsum('ij,ij->i', cp, diff)
        denom = dist**3

        lk += np.sum(num / denom)

    lk /= (4.0 * np.pi)
    return lk


def compute_linking_matrix(manifolds, n_samples=200):
    """
    Compute approximate linking numbers between all pairs of strands.
    Returns:
      strands: list of metadata dicts
      L: (N x N) matrix of linking numbers
    """
    strands = []
    curves = []

    # Gather all strands (stable + unstable) in one list
    for kind in ['stable', 'unstable']:
        for m in manifolds[kind]:
            x, y, z = m['x'], m['y'], m['lyap']
            xs, ys, zs = resample_curve3d(x, y, z, n_samples=n_samples)

            strands.append({
                'type': kind,
                'saddle': m['saddle'],
                'angle': m['angle']
            })
            curves.append((xs, ys, zs))

    N = len(curves)
    L = np.zeros((N, N))

    print(f"\nComputing linking numbers for {N} strands...")
    for i in range(N):
        for j in range(i+1, N):
            lk = linking_number(curves[i], curves[j])
            L[i, j] = L[j, i] = lk

    return strands, L


def print_linking_summary(strands, L, threshold=0.25):
    """
    Print only significantly linked pairs.
    """
    print("\n=== LINKING NUMBERS (approximate) ===")
    N = len(strands)
    for i in range(N):
        for j in range(i+1, N):
            lk = L[i, j]
            if abs(lk) > threshold:
                si, sj = strands[i], strands[j]
                print(f"  Lk[{i},{j}] ≈ {lk:+.2f}  ::  "
                      f"{si['type'][0].upper()} S{si['saddle']+1} vs "
                      f"{sj['type'][0].upper()} S{sj['saddle']+1}")

# ---------- 3. Braid word extraction ----------

def project_curve_to_x_lambda(m):
    """Return (lambda, x, y) arrays for convenience."""
    lam = m['lyap']
    x = m['x']
    y = m['y']
    return lam, x, y


def build_braid_word(manifolds, n_slices=150):
    """
    Very heuristic braid word:
    - Sample a set of λ-slices.
    - At each slice, find which strand is at which y (ordering).
    - Track how the permutation changes between slices.
    - Each adjacent swap contributes a braid generator σ_i^{±1}.
    """
    # For simplicity, use only unstable manifolds (they’re usually cleaner),
    # but you can mix both if you want.
    strands = manifolds['unstable']
    M = len(strands)
    if M < 2:
        return []

    # Precompute interpolation of each strand at any λ via nearest neighbor
    lambdas_all = np.concatenate([m['lyap'] for m in strands])
    lam_min, lam_max = np.min(lambdas_all), np.max(lambdas_all)
    lam_samples = np.linspace(lam_min, lam_max, n_slices)

    # For each strand and each λ, find closest point in its param samples
    def eval_y_at_lambda(m, lam_target):
        lam, _, y = project_curve_to_x_lambda(m)
        idx = np.argmin(np.abs(lam - lam_target))
        return y[idx]

    # For each λ-slice, record permutation of strand indices by y
    perms = []
    for lam_target in lam_samples:
        ys = [eval_y_at_lambda(m, lam_target) for m in strands]
        order = np.argsort(ys)  # lowest y at left
        perms.append(order)

    # Convert permutation sequence to braid word
    braid_word = []  # list of tuples (i, sign) -> σ_i^{sign}
    prev = perms[0]
    for p in perms[1:]:
        # Find minimal sequence of adjacent swaps converting prev -> p.
        # Here we do it greedily by bubble-sort-like swaps.
        temp = list(prev.copy())
        # Invert permutation to know target position of each strand
        target_pos = {strand: np.where(p == strand)[0][0] for strand in p}

        for i in range(M - 1):
            j = np.where(temp == p[i])[0][0]
            while j > i:
                # swap temp[j-1], temp[j]
                a, b = temp[j-1], temp[j]
                # Determine sign by comparing j-1 vs j positions in ordering by y:
                sign = +1 if target_pos[a] < target_pos[b] else -1
                braid_word.append((j-1, sign))
                temp[j-1], temp[j] = temp[j], temp[j-1]
                j -= 1

        prev = p

    return braid_word


def pretty_print_braid_word(braid_word):
    """
    Show braid as σ_1, σ_2^{-1}, ...
    """
    print("\n=== BRAID WORD (heuristic) ===")
    if not braid_word:
        print("  <empty>")
        return
    symbols = []
    for i, sign in braid_word:
        if sign > 0:
            symbols.append(f"σ_{i+1}")
        else:
            symbols.append(f"σ_{i+1}⁻¹")
    print("  " + " · ".join(symbols))

# ---------- 4. Knottedness vs Energy (uses your 2D scanner) ----------

from knottedness import scan_manifold as scan_2d  # <- rename your previous script
# or just paste your scan_manifold + compute_knottedness_from_trajectory
# into this file and import from there.

def knottedness_vs_energy(E_values,
                          m=1.0, lam=1.0,
                          XY_LIMITS=(-2, 2, -2, 2),
                          RES=120,
                          t_max=200.0,
                          r_escape=5.0,
                          n_samples=200):
    """
    For each energy in E_values, run the 2D knottedness scan and return
    average K for:
      - all points
      - trapped points only
      - escaping points only
    """
    stats = []

    for E in E_values:
        print(f"\n=== Energy E = {E:.5f} ===")
        xs, ys, exit_map, K_map, forbidden = scan_2d(
            m=m,
            lam=lam,
            E=E,
            XY_LIMITS=XY_LIMITS,
            RES=RES,
            t_max=t_max,
            r_escape=r_escape,
            n_samples=n_samples
        )

        mask_valid = ~forbidden
        K_valid = K_map[mask_valid]

        trapped = (exit_map == 0) & mask_valid
        escaped = (exit_map > 0) & mask_valid

        stats.append({
            'E': E,
            'K_all_mean': np.nanmean(K_valid),
            'K_trapped_mean': np.nanmean(K_map[trapped]),
            'K_escape_mean': np.nanmean(K_map[escaped]),
        })

    return stats


def plot_knottedness_vs_energy(stats):
    Es = np.array([s['E'] for s in stats])
    K_all = np.array([s['K_all_mean'] for s in stats])
    K_tr = np.array([s['K_trapped_mean'] for s in stats])
    K_ex = np.array([s['K_escape_mean'] for s in stats])

    plt.figure(figsize=(7, 5))
    plt.plot(Es, K_all, 'o-', label='All')
    plt.plot(Es, K_tr, 's-', label='Trapped only')
    plt.plot(Es, K_ex, '^-', label='Escaping only')
    plt.xlabel('Energy E')
    plt.ylabel('Mean knottedness K')
    plt.title('Knottedness vs Energy')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# ---------- 5. Δ-acceleration along manifolds ----------

def attach_delta_acceleration(manifolds, lam=1.0):
    """
    For each strand, compute Δ(t) = |V(x,y)|, vΔ, aΔ, and store them.
    """
    def V(x, y):
        return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1.0/3.0) * y**3)

    for kind in ['stable', 'unstable']:
        for m in manifolds[kind]:
            x = m['x']
            y = m['y']
            t = m['t']

            Delta = np.abs(V(x, y))
            v_delta = np.gradient(Delta, t)
            a_delta = np.gradient(v_delta, t)

            m['Delta'] = Delta
            m['v_delta'] = v_delta
            m['a_delta'] = a_delta


def plot_delta_accel_distribution(manifolds):
    """
    Quick overview: histogram of aΔ for stable vs unstable manifolds.
    """
    a_stable = np.concatenate([m['a_delta'] for m in manifolds['stable']])
    a_unstable = np.concatenate([m['a_delta'] for m in manifolds['unstable']])

    plt.figure(figsize=(7, 5))
    plt.hist(a_stable, bins=80, alpha=0.6, label='Stable', density=True)
    plt.hist(a_unstable, bins=80, alpha=0.6, label='Unstable', density=True)
    plt.xlabel('Δ-acceleration a_Δ')
    plt.ylabel('Density')
    plt.title('Distribution of Δ-acceleration along manifolds')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Load manifolds produced by knot_extractor_2.py
    with open('manifolds_data.pkl', 'rb') as f:
        manifolds = pickle.load(f)

    # 1) Chern-like indices
    chern_results = compute_chern_indices(manifolds)
    summarize_chern_indices(chern_results)

    # 2) Linking numbers
    strands, L = compute_linking_matrix(manifolds, n_samples=150)
    print_linking_summary(strands, L, threshold=0.25)

    # 3) Braid word
    braid_word = build_braid_word(manifolds, n_slices=150)
    pretty_print_braid_word(braid_word)

    # 5) Δ-acceleration (4 is separate, since it uses 2D scan)
    attach_delta_acceleration(manifolds, lam=1.0)
    plot_delta_accel_distribution(manifolds)
