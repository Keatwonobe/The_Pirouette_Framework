import numpy as np
import matplotlib.pyplot as plt

# ---------- helpers ----------

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

    # 4) overlay hotspots on spin map and Lyapunov+flux tubes
    plot_binding_hotspots_spin(M, Lgrid, Spin, binding_points,
                               outname="binding_on_spin.png",
                               B_quantile=0.97)

    plot_binding_hotspots_lyap(M, Lgrid, Lyap, tubes, binding_points,
                               outname="binding_on_lyapunov.png",
                               B_quantile=0.97)