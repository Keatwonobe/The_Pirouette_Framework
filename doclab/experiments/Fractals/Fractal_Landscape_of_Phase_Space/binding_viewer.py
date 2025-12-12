import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from pirouette_physics import Constants
# --- Pirouette dynamics constants (from unification_10) ---
TWIST = Constants.TWIST          # Standard Model twist
GAMMA = 0.5          # Higgs viscosity
DT    = 0.015
STEPS = 1200
EPSILON = 1e-6       # Lyapunov shadow separation
LAST_TOPOLOGY = {}   # filled by compute_topology_fields

# ---------- Unified Binding Index Mapper (UBIM) ----------

def _gaussian_kernel_1d(sigma_pix: float, ksize: int = 9):
    """
    Build a simple 1D Gaussian kernel for smoothing in pixel space.
    No SciPy dependency – just numpy.
    """
    k = np.arange(ksize) - ksize // 2
    kern = np.exp(-0.5 * (k / sigma_pix) ** 2)
    kern /= kern.sum()
    return kern


def _gaussian_blur_2d(field: np.ndarray, sigma_pix: float = 1.5, ksize: int = 9):
    """
    Separable 2D Gaussian blur: convolve rows then columns.
    """
    if sigma_pix <= 0:
        return field

    kern = _gaussian_kernel_1d(sigma_pix, ksize)
    # pad reflectively so we don't introduce edge artifacts
    tmp = np.pad(field, ((ksize//2, ksize//2), (0, 0)), mode="reflect")
    tmp = np.apply_along_axis(lambda v: np.convolve(v, kern, mode="same"),
                              axis=0, arr=tmp)
    tmp = tmp[ksize//2:-ksize//2, :]

    out = np.pad(tmp, ((0, 0), (ksize//2, ksize//2)), mode="reflect")
    out = np.apply_along_axis(lambda v: np.convolve(v, kern, mode="same"),
                              axis=1, arr=out)
    out = out[:, ksize//2:-ksize//2]

    return out


def build_binding_index_field(M, Lgrid, Lyap, binding_points,
                              sigma_pix: float = 1.5,
                              mode: str = "max"):
    """
    Turn the discrete binding samples along flux tubes into a full
    Binding Index field on the (m, λ) grid.

    Args
    ----
    M, Lgrid : 2D arrays defining the (m, λ) mesh (same as Lyap / Spin).
    Lyap     : 2D array of Lyapunov exponents on the grid.
    binding_points : list of dicts from compute_binding_points()
                     each with keys 'm', 'lam', 'B', 'Gs', 'Al', ...
    sigma_pix : Gaussian blur width in pixels (0 = no smoothing).
    mode      : 'max' or 'sum'
                - 'max': pixel gets the strongest binding point that hits it.
                - 'sum': pixel accumulates all binding contributions.

    Returns
    -------
    B_field : 2D array, same shape as Lyap, containing the unified
              Binding Index on the grid.
    """

    m_axis = M[0, :]
    lam_axis = Lgrid[:, 0]
    Ny, Nx = Lyap.shape

    B_field = np.zeros_like(Lyap, dtype=float)

    if not binding_points:
        return B_field

    dm = m_axis[1] - m_axis[0]
    dl = lam_axis[1] - lam_axis[0]

    for p in binding_points:
        mx = p["m"]
        lx = p["lam"]
        Bp = p["B"]

        ix = int(round((mx - m_axis[0]) / dm))
        iy = int(round((lx - lam_axis[0]) / dl))

        if ix < 0 or ix >= Nx or iy < 0 or iy >= Ny:
            continue

        if mode == "sum":
            B_field[iy, ix] += Bp
        else:  # 'max' (default)
            B_field[iy, ix] = max(B_field[iy, ix], Bp)

    # Normalize by max so it's dimensionless in [0,1]
    maxB = np.max(B_field)
    if maxB > 0:
        B_field = B_field / maxB

    # Optional smoothing to “inflate” the discrete knots into basins
    if sigma_pix > 0:
        B_field = _gaussian_blur_2d(B_field, sigma_pix=sigma_pix, ksize=9)

    return B_field


def plot_binding_index_map(M, Lgrid, Lyap, B_field,
                           outname: str = "binding_index_map.png"):
    """
    Visualize the Unified Binding Index over the full (m, λ) plane.

    By default we show:
        - background: Lyapunov (stability / chaos)
        - overlay: Binding Index as a semi-transparent colormap
    so you can see exactly where binding rides on top of the stability troughs.
    """

    m_axis = M[0, :]
    lam_axis = Lgrid[:, 0]

    # normalize Lyapunov for display
    Lmin, Lmax = float(Lyap.min()), float(Lyap.max())
    if Lmax > Lmin:
        Lyap_norm = (Lyap - Lmin) / (Lmax - Lmin)
    else:
        Lyap_norm = np.zeros_like(Lyap)

    fig, ax = plt.subplots(figsize=(8, 8))

    # base: Lyapunov landscape
    im0 = ax.imshow(
        Lyap_norm,
        extent=[m_axis.min(), m_axis.max(), lam_axis.min(), lam_axis.max()],
        origin="lower",
        cmap="magma"
    )
    cbar0 = plt.colorbar(im0, ax=ax)
    cbar0.set_label("Lyapunov (normalized)")

    # overlay: Binding Index
    # Use a different colormap + alpha so we can see both.
    im1 = ax.imshow(
        B_field,
        extent=[m_axis.min(), m_axis.max(), lam_axis.min(), lam_axis.max()],
        origin="lower",
        cmap="viridis",
        alpha=0.65
    )
    cbar1 = plt.colorbar(im1, ax=ax)
    cbar1.set_label("Unified Binding Index 𝓘(m, λ)")

    ax.set_xlabel("Mass field m")
    ax.set_ylabel("Coupling field λ")
    ax.set_title("Unified Binding Index Map\n(UBIM: binding = stability × tube × spin)")

    plt.tight_layout()
    plt.savefig(outname, dpi=200)
    plt.show()

def compute_topology_fields(res, m_min, m_max, l_min, l_max):
    """
    Run the full spin + Lyapunov scan on a rectangular (m, λ) window.

    Returns
    -------
    M, L : 2D arrays (res x res)
        Meshgrid of mass and coupling coordinates.
    lyap_map : 2D array
        Time-averaged Lyapunov exponent field.
    spin_map : 2D array
        Winding number / spin topology field.
    """
    global LAST_TOPOLOGY

    # 1. Build grid
    m_range = np.linspace(m_min, m_max, res)
    l_range = np.linspace(l_min, l_max, res)
    M, L = np.meshgrid(m_range, l_range)

    # Flatten for vectorized integration
    m   = M.ravel().copy()
    lam = L.ravel().copy()

    pm   = np.zeros_like(m)
    plam = np.zeros_like(lam)

    # Shadow particle for Lyapunov
    m_s   = m + EPSILON
    lam_s = lam + EPSILON
    pm_s   = np.zeros_like(m)
    plam_s = np.zeros_like(lam)

    # Metrics
    prev_ang  = np.arctan2(lam, m)
    total_ang = np.zeros_like(m)
    lyap_sum  = np.zeros_like(m)

    # 2. Time integration (Benettin algorithm for Lyapunov) :contentReference[oaicite:2]{index=2}
    for step in range(STEPS):
        # --- main particle ---
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)

        pm   = (pm   + 0.5 * DT * Fm)   * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m   += DT * pm
        lam += DT * plam

        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm   = (pm   + 0.5 * DT * Fm)   * drag
        plam = (plam + 0.5 * DT * Flam) * drag

        # --- shadow particle ---
        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)

        pm_s   = (pm_s   + 0.5 * DT * Fm_s)   * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s
        m_s   += DT * pm_s
        lam_s += DT * plam_s

        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)
        pm_s   = (pm_s   + 0.5 * DT * Fm_s)   * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s

        # --- spin (winding) ---
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta > np.pi,  delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        total_ang += delta
        prev_ang = curr_ang

        # --- Lyapunov divergence ---
        dist_sq = ((m   - m_s)   ** 2 +
                   (lam - lam_s) ** 2 +
                   (pm   - pm_s) ** 2 +
                   (plam - plam_s) ** 2)
        dist = np.sqrt(dist_sq)
        dist = np.maximum(dist, 1e-15)

        lyap_sum += np.log(dist / EPSILON)

        # Benettin renormalization
        rescale = EPSILON / dist
        m_s   = m   + (m_s   - m)   * rescale
        lam_s = lam + (lam_s - lam) * rescale
        pm_s   = pm   + (pm_s   - pm)   * rescale
        plam_s = plam + (plam_s - plam) * rescale

        if step % 200 == 0:
            print(f"[compute_topology_fields] step {step}/{STEPS}")

    # 3. Reshape and cache :contentReference[oaicite:3]{index=3}
    spin_raw  = np.abs(total_ang) / (2.0 * np.pi)
    spin_map  = spin_raw.reshape(res, res)

    lyap_exp  = lyap_sum / (STEPS * DT)
    lyap_map  = lyap_exp.reshape(res, res)

    LAST_TOPOLOGY = {
        "M": M,
        "L": L,
        "lyap": lyap_map,
        "spin": spin_map,
        "res": res,
        "bounds": (m_min, m_max, l_min, l_max),
    }

    return M, L, lyap_map, spin_map


def get_force_vectorized(m, lam):
    """
    Pirouette SU(3)-like composite force:
    Teal (EM), Red (Weak), Gold (Strong) mixed with angle weights.
    """
    # 1. Teal (EM)
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak)
    F_red_m    = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam  = -(lam + 1.0) + p_violation

    # 3. Gold (Strong) – nonlinear amplification of the vector sum
    sum_m   = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    magnitude      = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude)

    F_gold_m   = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor

    # Angle-based weights (tripod sectors)
    angle = np.degrees(np.arctan2(lam, m)) % 360

    diff_g = np.abs(angle - 30.0)
    diff_g = np.minimum(diff_g, 360.0 - diff_g)
    w_gold = np.exp(-(diff_g / 80.0) ** 2)

    diff_t = np.abs(angle - 150.0)
    diff_t = np.minimum(diff_t, 360.0 - diff_t)
    w_teal = np.exp(-(diff_t / 80.0) ** 2)

    diff_r = np.abs(angle - 270.0)
    diff_r = np.minimum(diff_r, 360.0 - diff_r)
    w_red  = np.exp(-(diff_r / 80.0) ** 2)

    tot = w_gold + w_teal + w_red + 1e-6
    nw_red, nw_teal, nw_gold = w_red / tot, w_teal / tot, w_gold / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam, nw_red


def bilinear_sample(field, xs, ys, xq, yq):
    """
    Bilinear sample of a 2D field defined on a regular grid.

    field : 2D array, shape (Ny, Nx)
    xs    : 1D array of x (m) coordinates, length Nx
    ys    : 1D array of y (lambda) coordinates, length Ny
    xq,yq : query coordinates (can be scalars or arrays of same shape)
    """
    xs = np.asarray(xs)
    ys = np.asarray(ys)
    field = np.asarray(field)

    xq = np.asarray(xq)
    yq = np.asarray(yq)

    # fractional indices
    ix = (xq - xs[0]) / (xs[1] - xs[0])
    iy = (yq - ys[0]) / (ys[1] - ys[0])

    ix0 = np.floor(ix).astype(int)
    iy0 = np.floor(iy).astype(int)
    ix1 = ix0 + 1
    iy1 = iy0 + 1

    # clamp
    ix0 = np.clip(ix0, 0, len(xs)-1)
    ix1 = np.clip(ix1, 0, len(xs)-1)
    iy0 = np.clip(iy0, 0, len(ys)-1)
    iy1 = np.clip(iy1, 0, len(ys)-1)

    dx = ix - ix0
    dy = iy - iy0

    f00 = field[iy0, ix0]
    f10 = field[iy0, ix1]
    f01 = field[iy1, ix0]
    f11 = field[iy1, ix1]

    f0 = f00 * (1 - dx) + f10 * dx
    f1 = f01 * (1 - dx) + f11 * dx
    f  = f0 * (1 - dy) + f1 * dy
    return f


def compute_binding_points(M, Lgrid, Lyap, Spin, tubes, eps_factor=2.0):
    """
    Compute per-point binding strength along flux tubes.

    Returns:
        points : list of dicts with keys
                 'm', 'lam', 'B', 'Gs', 'Al', 'tube_id'
    """
    # grid axes
    m_axis = M[0, :]
    lam_axis = Lgrid[:, 0]

    dm = m_axis[1] - m_axis[0]
    dl = lam_axis[1] - lam_axis[0]
    eps = eps_factor * max(abs(dm), abs(dl))

    # gradients of spin and Lyapunov
    dS_dm, dS_dl = np.gradient(Spin, dm, dl)
    dL_dm, dL_dl = np.gradient(Lyap, dm, dl)

    points = []

    for tube_idx, tube in enumerate(tubes):
        m_arr = np.asarray(tube["m_coords"])
        l_arr = np.asarray(tube["l_coords"])

        if len(m_arr) < 3:
            continue

        for k in range(1, len(m_arr)-1):
            mx = m_arr[k]
            lx = l_arr[k]

            # tangent along tube (central difference)
            t_vec = np.array([m_arr[k+1] - m_arr[k-1],
                              l_arr[k+1] - l_arr[k-1]])
            norm_t = np.linalg.norm(t_vec)
            if norm_t == 0:
                continue
            t_hat = t_vec / norm_t

            # normal (rotate by 90 degrees)
            n_hat = np.array([-t_hat[1], t_hat[0]])

            # gradient indices (nearest grid cell)
            ix = np.searchsorted(m_axis, mx) - 1
            iy = np.searchsorted(lam_axis, lx) - 1
            ix = np.clip(ix, 0, len(m_axis)-1)
            iy = np.clip(iy, 0, len(lam_axis)-1)

            # spin gradient projected on normal
            gs = abs(dS_dm[iy, ix] * n_hat[0] + dS_dl[iy, ix] * n_hat[1])

            # Lyapunov on each side of tube
            m_plus  = mx + eps * n_hat[0]
            l_plus  = lx + eps * n_hat[1]
            m_minus = mx - eps * n_hat[0]
            l_minus = lx - eps * n_hat[1]

            L_plus  = bilinear_sample(Lyap, m_axis, lam_axis, m_plus,  l_plus)
            L_minus = bilinear_sample(Lyap, m_axis, lam_axis, m_minus, l_minus)
            al = abs(L_plus - L_minus)

            B = gs * al

            points.append({
                "m": mx,
                "lam": lx,
                "B": B,
                "Gs": gs,
                "Al": al,
                "tube_id": tube_idx
            })

    return points


def plot_binding_hotspots_spin(M, Lgrid, Spin, binding_points,
                               outname="binding_on_spin.png",
                               B_quantile=0.97):
    """
    Overlay strongest binding points on top of the spin topology map.
    """
    m_axis = M[0, :]
    lam_axis = Lgrid[:, 0]

    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(
        Spin,
        extent=[m_axis.min(), m_axis.max(), lam_axis.min(), lam_axis.max()],
        origin="lower",
        cmap="hsv"
    )
    plt.colorbar(im, ax=ax, label="Spin topology scalar")

    # threshold on B to highlight top hotspots
    B_vals = np.array([p["B"] for p in binding_points])
    if len(B_vals) == 0:
        print("[binding] no binding points to plot")
        return
    thresh = np.quantile(B_vals, B_quantile)

    xs = [p["m"]   for p in binding_points if p["B"] >= thresh]
    ys = [p["lam"] for p in binding_points if p["B"] >= thresh]

    ax.scatter(xs, ys, s=10, c="white", edgecolors="black", linewidths=0.3,
               alpha=0.9, label="binding hotspots")

    ax.set_xlabel("Mass field m")
    ax.set_ylabel("Coupling field λ")
    ax.set_title("Binding hotspots on spin topology map")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(outname, dpi=200)
    plt.show()


def plot_binding_hotspots_lyap(M, Lgrid, Lyap, tubes, binding_points,
                               outname="binding_on_lyapunov.png",
                               B_quantile=0.97):
    """
    Overlay strongest binding points on top of Lyapunov + flux tubes.
    """
    m_axis = M[0, :]
    lam_axis = Lgrid[:, 0]

    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(
        Lyap,
        extent=[m_axis.min(), m_axis.max(), lam_axis.min(), lam_axis.max()],
        origin="lower",
        cmap="magma"
    )
    plt.colorbar(im, ax=ax, label="Lyapunov exponent")

    # draw tubes
    for tube in tubes:
        ax.plot(tube["m_coords"], tube["l_coords"],
                "-", color="cyan", linewidth=0.6, alpha=0.7)

    # hotspots
    B_vals = np.array([p["B"] for p in binding_points])
    if len(B_vals) == 0:
        print("[binding] no binding points to plot")
        return
    thresh = np.quantile(B_vals, B_quantile)

    xs = [p["m"]   for p in binding_points if p["B"] >= thresh]
    ys = [p["lam"] for p in binding_points if p["B"] >= thresh]

    ax.scatter(xs, ys, s=12, c="yellow", edgecolors="black", linewidths=0.3,
               alpha=0.95, label="binding hotspots")

    ax.set_xlabel("Mass field m")
    ax.set_ylabel("Coupling field λ")
    ax.set_title("Binding hotspots on Lyapunov + flux tubes")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(outname, dpi=200)
    plt.show()

def map_flux_tubes(
    min_points,
    percentile,
    res,
    m_min,
    m_max,
    l_min,
    l_max,
    decode_su3=False,
):
    """
    Extract flux-tube candidates from the Lyapunov field.

    - Uses the LAST_TOPOLOGY cache filled by compute_topology_fields.
    - Smooths the Lyapunov map with a 3x3 Gaussian-ish kernel.
    - Thresholds at the given percentile.
    - Returns connected ridges (>= min_points) as flux tubes.

    Returns
    -------
    tubes : list of dict
        Each dict has keys: 'tube_id', 'm_coords', 'l_coords'.
    """
    global LAST_TOPOLOGY

    if not LAST_TOPOLOGY:
        raise RuntimeError(
            "map_flux_tubes: LAST_TOPOLOGY is empty. "
            "Call compute_topology_fields(...) first."
        )

    lyap_map = LAST_TOPOLOGY["lyap"]
    M        = LAST_TOPOLOGY["M"]
    L        = LAST_TOPOLOGY["L"]

    # --- sanity check on resolution / window (optional) ---
    if lyap_map.shape != (res, res):
        print("[map_flux_tubes] WARNING: requested res does not match cached field; "
              "using cached resolution instead.")
        res = lyap_map.shape[0]

    # --- smooth Lyapunov field to emphasise ridges ---
    kernel = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]], dtype=float)
    kernel /= kernel.sum()

    padded = np.pad(lyap_map, 1, mode="edge")
    smooth = (
        kernel[0, 0] * padded[:-2, :-2] +
        kernel[0, 1] * padded[:-2, 1:-1] +
        kernel[0, 2] * padded[:-2, 2:] +
        kernel[1, 0] * padded[1:-1, :-2] +
        kernel[1, 1] * padded[1:-1, 1:-1] +
        kernel[1, 2] * padded[1:-1, 2:] +
        kernel[2, 0] * padded[2:, :-2] +
        kernel[2, 1] * padded[2:, 1:-1] +
        kernel[2, 2] * padded[2:, 2:]
    )

    # --- high-Lyapunov mask (candidate flux tubes) ---
    thresh = np.percentile(smooth, percentile)
    mask   = smooth >= thresh

    H, W = mask.shape
    visited = np.zeros_like(mask, dtype=bool)

    tubes = []
    tube_id = 0

    for iy in range(H):
        for ix in range(W):
            if not mask[iy, ix] or visited[iy, ix]:
                continue

            # flood-fill this ridge
            q = deque()
            q.append((iy, ix))
            visited[iy, ix] = True
            coords = []

            while q:
                cy, cx = q.popleft()
                coords.append((cy, cx))

                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W:
                            if mask[ny, nx] and not visited[ny, nx]:
                                visited[ny, nx] = True
                                q.append((ny, nx))

            if len(coords) < min_points:
                continue

            ys, xs = zip(*coords)
            ys = np.array(ys, dtype=int)
            xs = np.array(xs, dtype=int)

            m_coords = M[ys, xs]
            l_coords = L[ys, xs]

            tubes.append({
                "tube_id": tube_id,
                "m_coords": m_coords,
                "l_coords": l_coords,
            })
            tube_id += 1

    print(
        f"[map_flux_tubes] Found {len(tubes)} flux tubes "
        f"(>= {min_points} points, top {100.0 - percentile:.1f}% Lyapunov)."
    )

    # 'decode_su3' flag is reserved for later colour / generator decoding
    # from the spin field; we keep the parameter for API compatibility.
    return tubes


if __name__ == "__main__":
    # 1) compute topology on the same window you used for the spin map
    M, Lgrid, Lyap, Spin = compute_topology_fields(
        res=800,
        m_min=-2.5, m_max=2.5,
        l_min=-2.5, l_max=2.5,
    )

    # 2) build flux-tube skeleton on that window
    tubes = map_flux_tubes(
        min_points=30,
        percentile=93,
        res=800,
        m_min=-2.5, m_max=2.5,
        l_min=-2.5, l_max=2.5,
        decode_su3=False,
    )

    # 3) compute binding strength along tubes
    binding_points = compute_binding_points(M, Lgrid, Lyap, Spin, tubes,
                                            eps_factor=2.0)

    # 3.5) build unified Binding Index field from those samples
    B_field = build_binding_index_field(
        M, Lgrid, Lyap, binding_points,
        sigma_pix=1.5,   # tighten/loosen basins by changing this
        mode="max"       # try "sum" as a sanity check too
    )

    # 4) overlay hotspots on spin map and Lyapunov+flux tubes
    plot_binding_hotspots_spin(M, Lgrid, Spin, binding_points,
                               outname="binding_on_spin.png",
                               B_quantile=0.97)

    plot_binding_hotspots_lyap(M, Lgrid, Lyap, tubes, binding_points,
                               outname="binding_on_lyapunov.png",
                               B_quantile=0.97)

    # 5) Unified Binding Index Map
    plot_binding_index_map(
        M, Lgrid, Lyap, B_field,
        outname="binding_index_map.png"
    )