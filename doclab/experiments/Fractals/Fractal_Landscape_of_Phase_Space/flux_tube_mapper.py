import numpy as np
import matplotlib.pyplot as plt

# Global vacuum topology (spin + chaos)
import unification_11 as topo

# Local mass / needle machinery (apex finder, local mass field, etc.)
import mass_hierarchy_apex_2 as mha


# ------------------------------------------------------------
# 1. Topology core: chaos + spin field
# ------------------------------------------------------------

def compute_topology_fields(res=None, steps=None, dt=None):
    """
    Thin wrapper around the dynamics in unification_11.

    Returns
    -------
    M, L : 2D arrays (res x res)
        Mass and coupling coordinates.
    Z : 2D array
        Lyapunov exponent (chaos height).
    C : 2D array
        Spin winding number.
    """
    RES = res if res is not None else topo.RES
    STEPS = steps if steps is not None else topo.STEPS
    DT = dt if dt is not None else topo.DT

    print(f"[FTM] Computing topology fields at {RES}x{RES}, steps={STEPS}...")

    m_range = np.linspace(topo.M_MIN, topo.M_MAX, RES)
    l_range = np.linspace(topo.L_MIN, topo.L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)

    # Flattened phase–space
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)

    # Shadows for Lyapunov
    m_s = m + topo.EPSILON
    lam_s = lam + topo.EPSILON
    pm_s = np.zeros_like(m)
    plam_s = np.zeros_like(lam)

    lyap_sum = np.zeros_like(m)
    total_ang = np.zeros_like(m)
    prev_ang = np.arctan2(lam, m)

    for step in range(STEPS):
        # Main path
        Fm, Flam, w_red = topo.get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * topo.GAMMA * w_red)

        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam

        Fm, Flam, w_red = topo.get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * topo.GAMMA * w_red)

        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag

        # Shadow path for Lyapunov
        Fm_s, Flam_s, w_red_s = topo.get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * topo.GAMMA * w_red_s)

        pm_s = (pm_s + 0.5 * DT * Fm_s) * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s
        m_s += DT * pm_s
        lam_s += DT * plam_s

        Fm_s, Flam_s, w_red_s = topo.get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * topo.GAMMA * w_red_s)

        pm_s = (pm_s + 0.5 * DT * Fm_s) * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s

        # Lyapunov separation
        dist = np.sqrt(
            (m - m_s) ** 2 + (lam - lam_s) ** 2 +
            (pm - pm_s) ** 2 + (plam - plam_s) ** 2
        )
        dist = np.maximum(dist, topo.EPSILON)
        rescale = topo.EPSILON / dist
        lyap_sum += np.log(dist / topo.EPSILON)

        # Reset shadow separation
        m_s = m + (m_s - m) * rescale
        lam_s = lam + (lam_s - lam) * rescale
        pm_s = pm + (pm_s - pm) * rescale
        plam_s = plam + (plam_s - plam) * rescale

        # Spin winding
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta > np.pi,  delta - 2 * np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2 * np.pi, delta)
        total_ang += delta
        prev_ang = curr_ang

        if step % 200 == 0:
            print(f"[FTM] step {step}/{STEPS}")

    lyap_exp = lyap_sum / (STEPS * DT)
    spin = np.abs(total_ang) / (2 * np.pi)

    Z = lyap_exp.reshape(RES, RES)
    C = spin.reshape(RES, RES)
    return M, L, Z, C


# ------------------------------------------------------------
# 2. Ridge & filament extraction
# ------------------------------------------------------------

def smooth_field(Z):
    """Simple 3×3 Gaussian-ish smoothing."""
    kernel = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]], dtype=float)
    kernel /= kernel.sum()

    Zpad = np.pad(Z, 1, mode="edge")
    out = np.zeros_like(Z)
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            patch = Zpad[i:i+3, j:j+3]
            out[i, j] = np.sum(patch * kernel)
    return out


def extract_ridge_skeleton(Z, percentile=90):
    """
    Lightweight ridge finder:

    1. Smooth Z.
    2. Threshold at high percentile.
    3. Keep points that are local maxima in 3×3 neighborhood.
    """
    Zs = smooth_field(Z)
    thr = np.percentile(Zs, percentile)
    candidate = Zs >= thr

    H, W = Z.shape
    ridge = np.zeros_like(candidate, dtype=bool)
    for i in range(1, H-1):
        for j in range(1, W-1):
            if not candidate[i, j]:
                continue
            patch = Zs[i-1:i+2, j-1:j+2]
            if Zs[i, j] >= np.max(patch):
                ridge[i, j] = True
    return ridge


def connected_components(mask):
    """
    8-connected components on a boolean mask.
    Returns a list of lists of (i, j) indices.
    """
    H, W = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    comps = []
    neighbors = [(-1,-1),(-1,0),(-1,1),
                 (0,-1),        (0,1),
                 (1,-1),(1,0),(1,1)]

    for i in range(H):
        for j in range(W):
            if not mask[i, j] or visited[i, j]:
                continue
            stack = [(i, j)]
            visited[i, j] = True
            comp = []
            while stack:
                ci, cj = stack.pop()
                comp.append((ci, cj))
                for di, dj in neighbors:
                    ni, nj = ci + di, cj + dj
                    if (
                        0 <= ni < H and 0 <= nj < W and
                        not visited[ni, nj] and mask[ni, nj]
                    ):
                        visited[ni, nj] = True
                        stack.append((ni, nj))
            comps.append(comp)
    return comps


def sort_component_points(comp, M, L):
    """
    Sorts a component's (i,j) indices along its dominant direction
    using a simple PCA axis.
    """
    pts = np.array([[M[i, j], L[i, j]] for (i, j) in comp])
    mean = pts.mean(axis=0)
    cov = np.cov(pts.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    axis = eigvecs[:, np.argmax(eigvals)]
    t = (pts - mean) @ axis
    order = np.argsort(t)
    sorted_indices = [comp[k] for k in order]
    return sorted_indices, pts[order, :], t[order]


# ------------------------------------------------------------
# 3. SU(3) decoder on arbitrary filaments
# ------------------------------------------------------------

# Tripod directions in (m, λ) — swap for your calibrated ones if needed
TRIPOD_ANGLES = {
    "T": 0.0,
    "R": 2.0 * np.pi / 3.0,
    "G": 4.0 * np.pi / 3.0,
}
TRIPOD_VECS = {k: np.array([np.cos(a), np.sin(a)]) for k, a in TRIPOD_ANGLES.items()}


def hessian_of_mass(m0, l0, h_m, h_l):
    """Hessian of √λ₁(m,λ) from mha.local_mass using finite differences."""
    def f(m, lam):
        return mha.local_mass(m, lam)

    f0 = f(m0, l0)

    f_mm_p = f(m0 + h_m, l0)
    f_mm_m = f(m0 - h_m, l0)
    f_ll_p = f(m0, l0 + h_l)
    f_ll_m = f(m0, l0 - h_l)

    f_ml_pp = f(m0 + h_m, l0 + h_l)
    f_ml_pm = f(m0 + h_m, l0 - h_l)
    f_ml_mp = f(m0 - h_m, l0 + h_l)
    f_ml_mm = f(m0 - h_m, l0 - h_l)

    f_mm = (f_mm_p - 2.0 * f0 + f_mm_m) / (h_m ** 2)
    f_ll = (f_ll_p - 2.0 * f0 + f_ll_m) / (h_l ** 2)
    f_ml = (f_ml_pp - f_ml_pm - f_ml_mp + f_ml_mm) / (4.0 * h_m * h_l)

    H = np.array([[f_mm, f_ml],
                  [f_ml, f_ll]], dtype=float)
    vals, vecs = np.linalg.eigh(H)
    return H, vals, vecs


def decode_filament_su3(m_coords, l_coords, dm, dl, h_factor=0.5):
    """
    Given coordinates along a filament, compute SU(3) mixture via local mass Hessian.
    """
    n = len(m_coords)
    h_m = dm * h_factor
    h_l = dl * h_factor

    weights = {k: np.zeros(n) for k in TRIPOD_ANGLES.keys()}
    dom_angle = np.zeros(n)

    for i in range(n):
        H, vals, vecs = hessian_of_mass(m_coords[i], l_coords[i], h_m, h_l)
        idx = 0 if abs(vals[0]) > abs(vals[1]) else 1
        v_dom = vecs[:, idx]
        theta = np.arctan2(v_dom[1], v_dom[0])
        dom_angle[i] = theta

        for name, u in TRIPOD_VECS.items():
            c = float(np.dot(v_dom, u))
            w = c * c
            weights[name][i] = w

        total = sum(weights[name][i] for name in TRIPOD_ANGLES.keys())
        if total > 1e-14:
            for name in TRIPOD_ANGLES.keys():
                weights[name][i] /= total

    # Discard a few boundary points
    interior = slice(3, max(3, n-3))
    mean_w = {k: float(np.mean(weights[k][interior])) for k in TRIPOD_ANGLES.keys()}

    # Amplitude vector |psi> ~ sqrt(w)
    amps = np.array([np.sqrt(mean_w[k]) for k in ["T", "R", "G"]])
    norm = np.linalg.norm(amps)
    if norm > 1e-14:
        amps /= norm

    return weights, mean_w, amps, dom_angle


# ------------------------------------------------------------
# 4. High-level Flux Tube Mapper
# ------------------------------------------------------------

def map_flux_tubes(min_points=20, percentile=90):
    """
    Master routine:

    1. Compute chaos+spin fields.
    2. Extract ridge skeleton of chaos.
    3. Find connected components (flux tubes).
    4. For each long-enough tube, decode SU(3) mixture along it.

    Returns
    -------
    result : list of dicts, one per tube
    (also writes a PNG for visual inspection)
    """
    M, L, Z, C = compute_topology_fields()
    Zs = smooth_field(Z)
    ridge = extract_ridge_skeleton(Zs, percentile=percentile)
    comps = connected_components(ridge)

    dm = M[0, 1] - M[0, 0]
    dl = L[1, 0] - L[0, 0]

    tube_results = []

    print(f"[FTM] found {len(comps)} ridge components before filtering")

    for idx, comp in enumerate(comps):
        if len(comp) < min_points:
            continue

        sorted_idx, pts, tvals = sort_component_points(comp, M, L)
        m_coords = pts[:, 0]
        l_coords = pts[:, 1]

        weights, mean_w, amps, dom_angle = decode_filament_su3(
            m_coords, l_coords, dm, dl
        )

        tube_results.append({
            "id": idx,
            "num_points": len(comp),
            "m_coords": m_coords,
            "l_coords": l_coords,
            "mean_w": mean_w,
            "amps": amps,
        })

        print(
            f"[FTM] tube {idx:03d} (N={len(comp)}) "
            f"<w_T,w_R,w_G> ≈ ({mean_w['T']:.3f}, "
            f"{mean_w['R']:.3f}, {mean_w['G']:.3f}) "
            f"|psi> ≈ ({amps[0]:.3f},{amps[1]:.3f},{amps[2]:.3f})"
        )

    # Visualization: chaos background + tubes colored by <w_T>
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(
        Zs,
        extent=[topo.M_MIN, topo.M_MAX, topo.L_MIN, topo.L_MAX],
        origin="lower",
        cmap="magma"
    )
    plt.colorbar(im, ax=ax, label="Lyapunov (smoothed)")

    for tr in tube_results:
        m_coords = tr["m_coords"]
        l_coords = tr["l_coords"]
        c = tr["mean_w"]["T"]  # color by T-fraction
        ax.plot(
            m_coords, l_coords, "-",
            linewidth=1.2,
            color=(1 - c, 0.2, c),  # red→magenta as T increases
            alpha=0.9,
        )

    ax.set_xlabel("Mass field m")
    ax.set_ylabel("Coupling field λ")
    ax.set_title("Flux Tube Mapper: chaos ridges + SU(3) color mix")
    plt.tight_layout()
    plt.savefig("flux_tube_map.png", dpi=180)
    plt.show()

    return tube_results


if __name__ == "__main__":
    map_flux_tubes()
