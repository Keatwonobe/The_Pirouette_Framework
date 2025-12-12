import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# ============================================================
#  Proton Basin Geometry Toolbox
#
#  Drop-in tools for:
#   - extracting basin boundaries
#   - fitting circles to the big caps
#   - fitting a circle to the central pocket
#   - fitting the "incoming line from the left"
#   - plotting overlays
#
#  Core entry point:
#     analyze_proton_basin(basin_mask, m_vals, lam_vals, ...)
#
# ============================================================


# ---------- Utility: connected component via BFS ----------

def bfs_component(mask, start_i, start_j):
    """
    4-neighbor BFS component labeller.
    Returns list of (i, j) indices belonging to the component.
    """
    ny, nx = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    q = deque()
    q.append((start_i, start_j))
    visited[start_i, start_j] = True
    comp = [(start_i, start_j)]

    while q:
        i, j = q.popleft()
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < ny and 0 <= nj < nx:
                if mask[ni, nj] and not visited[ni, nj]:
                    visited[ni, nj] = True
                    q.append((ni, nj))
                    comp.append((ni, nj))
    return comp


# ---------- Boundary extraction ----------

def extract_boundary_points(mask, m_vals, lam_vals):
    """
    Find all boundary pixels of a boolean basin mask (True = inside).
    Returns arrays (x, y) = (m, lambda) for boundary points.
    """
    ny, nx = mask.shape
    boundary_m = []
    boundary_l = []

    for i in range(1, ny - 1):
        for j in range(1, nx - 1):
            if not mask[i, j]:
                continue
            # 4-neighbor: if any neighbor is False, this is boundary
            if (not mask[i - 1, j] or
                not mask[i + 1, j] or
                not mask[i, j - 1] or
                not mask[i, j + 1]):
                boundary_m.append(m_vals[j])
                boundary_l.append(lam_vals[i])

    return np.array(boundary_m), np.array(boundary_l)


# ---------- Circle fitting ----------

def fit_circle(x, y):
    """
    Least-squares circle fit.

    Solve:
       (x - xc)^2 + (y - yc)^2 = R^2
    in linear form.

    Returns xc, yc, R, residuals (distance error).
    """
    if len(x) < 3:
        return np.nan, np.nan, np.nan, np.array([])

    A = np.column_stack([2*x, 2*y, np.ones_like(x)])
    b = x**2 + y**2
    c1, c2, c3 = np.linalg.lstsq(A, b, rcond=None)[0]
    xc, yc = c1, c2
    R = np.sqrt(max(c3 + xc**2 + yc**2, 0.0))

    r = np.sqrt((x - xc)**2 + (y - yc)**2)
    resid = r - R
    return xc, yc, R, resid


# ---------- Line fitting ----------

def fit_line(x, y):
    """
    Least-squares fit to y = k x + b.
    Returns k, b, residuals.
    """
    if len(x) < 2:
        return np.nan, np.nan, np.array([])

    A = np.column_stack([x, np.ones_like(x)])
    k, b = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = k * x + b
    resid = y - y_pred
    return k, b, resid


# ---------- Region selectors ----------

def select_cap_points(m_b, l_b, region="bottom_right"):
    """
    Split boundary points into rough "lobes" by quadrant.
    This is heuristic but works well for the proton basin shapes.
    """
    if region == "bottom_right":
        mask = (m_b > 0) & (l_b < 0)
    elif region == "top_left":
        mask = (m_b < 0) & (l_b > 0)
    elif region == "top_right":
        mask = (m_b > 0) & (l_b > 0)
    elif region == "bottom_left":
        mask = (m_b < 0) & (l_b < 0)
    else:
        raise ValueError(f"Unknown region '{region}'")
    return m_b[mask], l_b[mask]


def find_central_component_mask(basin_mask, m_vals, lam_vals, r_cut):
    """
    Identify the connected component of the basin that sits near the origin
    (within radius r_cut). Returns a boolean mask for that component only.
    """
    ny, nx = basin_mask.shape
    M, L = np.meshgrid(m_vals, lam_vals)
    R = np.sqrt(M**2 + L**2)

    # candidate region near origin
    near_origin = basin_mask & (R < r_cut)

    # find any True cell in this region as a seed
    ys, xs = np.where(near_origin)
    if len(ys) == 0:
        return np.zeros_like(basin_mask, dtype=bool)

    start_i, start_j = int(ys[0]), int(xs[0])
    comp_indices = bfs_component(basin_mask, start_i, start_j)

    comp_mask = np.zeros_like(basin_mask, dtype=bool)
    for i, j in comp_indices:
        comp_mask[i, j] = True
    return comp_mask


def select_line_points_from_left(m_b, l_b,
                                 m_min_fraction=0.5,
                                 lam_band_fraction=0.08):
    """
    Heuristic to select points belonging to the "incoming line from the left".

    - m_min_fraction: use points with m < -m_min_fraction * max(|m|)
    - lam_band_fraction: |lambda| < lam_band_fraction * max(|lambda|)
    """
    if len(m_b) == 0:
        return m_b, l_b

    m_abs_max = np.max(np.abs(m_b))
    l_abs_max = np.max(np.abs(l_b))

    m_cut = -m_min_fraction * m_abs_max
    lam_band = lam_band_fraction * l_abs_max

    mask = (m_b < m_cut) & (np.abs(l_b) < lam_band)
    return m_b[mask], l_b[mask]


# ---------- Main analysis pipeline ----------

def analyze_proton_basin(basin_mask,
                         m_vals,
                         lam_vals,
                         label="",
                         save_prefix="proton_basin_geom",
                         central_r_cut_fraction=0.15):
    """
    Full geometry analysis of a single proton basin snapshot.

    Parameters
    ----------
    basin_mask : 2D bool array
        True = inside basin.
    m_vals : 1D array
        x-axis coordinates (mass field).
    lam_vals : 1D array
        y-axis coordinates (coupling field).
    label : str
        Text label used in printouts and plot titles.
    save_prefix : str
        Prefix for saved PNGs.
    central_r_cut_fraction : float
        Radius (as fraction of max |m,lambda|) used to find central pocket.

    Effects
    -------
    - prints fitted parameters for:
        - top-left cap circle
        - bottom-right cap circle
        - central pocket circle
        - incoming line from the left
    - saves an overlay plot with all fits drawn on top of the mask.
    """

    print("\n==============================")
    print(f"[GEOM] Analyzing proton basin {label}")
    print("==============================")

    # 1. Extract boundary points
    m_b, l_b = extract_boundary_points(basin_mask, m_vals, lam_vals)
    if len(m_b) == 0:
        print("[GEOM] No boundary points found. Aborting.")
        return

    # ------------------------------------------------------------------
    # 2. Fit large caps (top-left & bottom-right)
    # ------------------------------------------------------------------
    m_br, l_br = select_cap_points(m_b, l_b, region="bottom_right")
    m_tl, l_tl = select_cap_points(m_b, l_b, region="top_left")

    print(f"[GEOM] bottom-right cap boundary points: {len(m_br)}")
    print(f"[GEOM] top-left cap boundary points   : {len(m_tl)}")

    xc_br, yc_br, R_br, resid_br = fit_circle(m_br, l_br)
    xc_tl, yc_tl, R_tl, resid_tl = fit_circle(m_tl, l_tl)

    if not np.isnan(R_br):
        print(f"[CAP BR] center = ({xc_br:.5g}, {yc_br:.5g}), "
              f"R = {R_br:.5g}, "
              f"mean|resid| = {np.mean(np.abs(resid_br)):.5g}")
    else:
        print("[CAP BR] circle fit failed (too few points).")

    if not np.isnan(R_tl):
        print(f"[CAP TL] center = ({xc_tl:.5g}, {yc_tl:.5g}), "
              f"R = {R_tl:.5g}, "
              f"mean|resid| = {np.mean(np.abs(resid_tl)):.5g}")
    else:
        print("[CAP TL] circle fit failed (too few points).")

    # ------------------------------------------------------------------
    # 3. Fit central pocket near origin
    # ------------------------------------------------------------------
    # Determine r_cut from data extents
    M, L = np.meshgrid(m_vals, lam_vals)
    R_full = np.sqrt(M**2 + L**2)
    r_max = np.max(R_full)
    r_cut = central_r_cut_fraction * r_max

    central_mask = find_central_component_mask(basin_mask, m_vals, lam_vals,
                                               r_cut=r_cut)
    m_c, l_c = extract_boundary_points(central_mask, m_vals, lam_vals)

    print(f"[GEOM] central pocket boundary points: {len(m_c)} "
          f"(r_cut ~ {r_cut:.5g})")

    xc_c, yc_c, R_c, resid_c = fit_circle(m_c, l_c)
    if not np.isnan(R_c):
        print(f"[CENTER] center = ({xc_c:.5g}, {yc_c:.5g}), "
              f"R = {R_c:.5g}, "
              f"mean|resid| = {np.mean(np.abs(resid_c)):.5g}")
    else:
        print("[CENTER] circle fit failed (too few points).")

    # ------------------------------------------------------------------
    # 4. Fit the incoming line from the left
    # ------------------------------------------------------------------
    m_line, l_line = select_line_points_from_left(m_b, l_b)

    print(f"[GEOM] candidate line-from-left points: {len(m_line)}")

    k_line, b_line, resid_line = fit_line(m_line, l_line)
    if not np.isnan(k_line):
        theta = np.degrees(np.arctan(k_line))
        print(f"[LINE] lambda ≈ {k_line:.5g} * m + {b_line:.5g}, "
              f"angle θ ≈ {theta:.3f} deg, "
              f"mean|resid| = {np.mean(np.abs(resid_line)):.5g}")
    else:
        print("[LINE] line fit failed (too few points).")

    # ------------------------------------------------------------------
    # 5. Plot overlay
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(basin_mask,
              origin="lower",
              extent=[m_vals[0], m_vals[-1], lam_vals[0], lam_vals[-1]],
              cmap="Greys_r",
              alpha=0.6)

    # boundary scatter (optionally thin it for readability)
    stride = max(len(m_b) // 4000, 1)
    ax.scatter(m_b[::stride], l_b[::stride],
               s=2, c="cyan", alpha=0.4, label="boundary samples")

    # Big caps
    if not np.isnan(R_br):
        t = np.linspace(0, 2*np.pi, 512)
        xb = xc_br + R_br*np.cos(t)
        yb = yc_br + R_br*np.sin(t)
        ax.plot(xb, yb, "r-", lw=2, label="BR circle fit")

    if not np.isnan(R_tl):
        t = np.linspace(0, 2*np.pi, 512)
        xt = xc_tl + R_tl*np.cos(t)
        yt = yc_tl + R_tl*np.sin(t)
        ax.plot(xt, yt, "b-", lw=2, label="TL circle fit")

    # Central pocket
    if not np.isnan(R_c):
        t = np.linspace(0, 2*np.pi, 512)
        xc = xc_c + R_c*np.cos(t)
        yc = yc_c + R_c*np.sin(t)
        ax.plot(xc, yc, "g-", lw=2, label="central pocket circle")

    # Incoming line
    if not np.isnan(k_line):
        m_min, m_max = m_vals[0], m_vals[-1]
        m_line_plot = np.linspace(m_min, m_max, 512)
        lam_line_plot = k_line * m_line_plot + b_line
        ax.plot(m_line_plot, lam_line_plot, "m--", lw=2, label="left line fit")

    ax.set_xlabel("Mass field m")
    ax.set_ylabel("Coupling field λ")
    title = "Proton Basin Geometry"
    if label:
        title += f" ({label})"
    ax.set_title(title)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()

    out_png = f"{save_prefix}_overlay.png"
    fig.savefig(out_png, dpi=200)
    plt.close(fig)

    print(f"[GEOM] Overlay saved to: {out_png}")
    print("[GEOM] Done.\n")


# ---------- Optional: simple loader for .npz snapshots ----------

def _load_npz_and_analyze(npz_path, label="", save_prefix=None):
    """
    Convenience helper if you store snapshots like:

        np.savez("proton_basin_snapshot.npz",
                 basin_mask=mask,
                 m_vals=m_vals,
                 lam_vals=lam_vals)

    Then run this module directly and it will analyze that file.
    """
    data = np.load(npz_path)
    basin_mask = data["basin_mask"].astype(bool)
    m_vals = data["m_vals"]
    lam_vals = data["lam_vals"]
    if save_prefix is None:
        save_prefix = npz_path.replace(".npz", "")
    analyze_proton_basin(basin_mask, m_vals, lam_vals,
                         label=label or npz_path,
                         save_prefix=save_prefix)


if __name__ == "__main__":
    # Example direct usage:
    #  python proton_basin_geometry_tools.py
    #
    # after creating a snapshot file:
    #  np.savez("proton_snapshot_12.npz",
    #           basin_mask=mask, m_vals=m_vals, lam_vals=lam_vals)
    #
    # then set NPZ_PATH below.
    NPZ_PATH = None  # e.g. "proton_snapshot_12.npz"
    if NPZ_PATH is not None:
        _load_npz_and_analyze(NPZ_PATH, label="demo")
    else:
        print("[GEOM] Module loaded. Import analyze_proton_basin() "
              "in your main script or set NPZ_PATH in __main__.")
