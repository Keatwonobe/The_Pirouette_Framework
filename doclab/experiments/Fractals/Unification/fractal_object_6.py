import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


DATA_FILE = "latent_curve_data.npz"


def smooth_1d(y, window=51):
    n = len(y)
    if window < 3:
        return y.copy()
    window = int(window)
    if window % 2 == 0:
        window += 1
    if window > n:
        window = n if n % 2 == 1 else n - 1
    kernel = np.ones(window) / window
    y_pad = np.pad(y, (window // 2, window // 2), mode="edge")
    ys = np.convolve(y_pad, kernel, mode="valid")
    return ys


def frenet_frame(curve):
    """
    Compute discrete Frenet frame (T, N, B) for a 3D curve sampled as [M,3].
    Returns arrays of shape (M,3) for T,N,B.
    """
    C = np.asarray(curve)
    M = C.shape[0]

    # first derivative (central differences)
    dC = np.zeros_like(C)
    dC[1:-1] = 0.5 * (C[2:] - C[:-2])
    dC[0] = C[1] - C[0]
    dC[-1] = C[-1] - C[-2]

    # tangent
    T = dC / np.linalg.norm(dC, axis=1, keepdims=True)

    # second derivative
    dT = np.zeros_like(T)
    dT[1:-1] = 0.5 * (T[2:] - T[:-2])
    dT[0] = T[1] - T[0]
    dT[-1] = T[-1] - T[-2]

    # normal (orthogonal component of dT)
    dT_perp = dT - (np.sum(dT * T, axis=1, keepdims=True) * T)
    N_norm = np.linalg.norm(dT_perp, axis=1, keepdims=True)
    N_norm[N_norm == 0] = 1.0
    N = dT_perp / N_norm

    # binormal
    B = np.cross(T, N)
    B_norm = np.linalg.norm(B, axis=1, keepdims=True)
    B_norm[B_norm == 0] = 1.0
    B = B / B_norm

    return T, N, B


def main():
    # -------------------------------------------------------
    # 1. Load latent data (ξ and 5-field vectors)
    # -------------------------------------------------------
    data = np.load(DATA_FILE, allow_pickle=True)
    xi = data["xi"]              # (N,)
    X_sorted = data["X_sorted"]  # (N,5)
    names = list(data["names"])

    N = len(xi)
    print(f"[Step5] Loaded {N} samples. Fields:", names)

    # -------------------------------------------------------
    # 2. PCA into 3D, as in Step 4
    # -------------------------------------------------------
    Xc = X_sorted - X_sorted.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    W = Vt[:3].T          # [5,3] projection matrix
    Y = Xc @ W            # [N,3] embedded data in PC space

    print("[Step5] PCA variance (first 3 components):",
          (S[:3]**2 / np.sum(S**2)))

    # -------------------------------------------------------
    # 3. Fit smooth 3D latent curve C(ξ)
    # -------------------------------------------------------
    deg_curve = 4
    p0 = np.poly1d(np.polyfit(xi, Y[:, 0], deg=deg_curve))
    p1 = np.poly1d(np.polyfit(xi, Y[:, 1], deg=deg_curve))
    p2 = np.poly1d(np.polyfit(xi, Y[:, 2], deg=deg_curve))

    xi_fine = np.linspace(0.0, 1.0, 300)
    C = np.stack([p0(xi_fine), p1(xi_fine), p2(xi_fine)], axis=1)
    T, N_vec, B_vec = frenet_frame(C)

    # -------------------------------------------------------
    # 4. Choose ξ-slices for tomography
    # -------------------------------------------------------
    # Feel free to tweak these positions:
    xi_slices = np.array([0.05, 0.20, 0.35, 0.50, 0.70, 0.90])
    xi_band = 0.02  # half-width around each slice (Δξ window)

    print("[Step5] Tomography slices at ξ =", xi_slices)

    # global radius scale for plotting
    # use residuals as a guide
    C_at_xi = np.stack([p0(xi), p1(xi), p2(xi)], axis=1)
    residuals = np.linalg.norm(Y - C_at_xi, axis=1)
    r_global = 2.0 * np.percentile(residuals, 95)  # generous radius
    print("[Step5] Using +/- {:.3f} in cross-section plots.".format(r_global))

    # -------------------------------------------------------
    # 5. Build cross-sections
    # -------------------------------------------------------
    n_slices = len(xi_slices)
    n_cols = 3
    n_rows = int(np.ceil(n_slices / n_cols))

    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=(4 * n_cols, 4 * n_rows),
        squeeze=False
    )

    for k, xi0 in enumerate(xi_slices):
        row = k // n_cols
        col = k % n_cols
        ax = axes[row, col]

        # points near this ξ
        mask = np.abs(xi - xi0) <= xi_band
        idx = np.where(mask)[0]
        if len(idx) == 0:
            ax.set_title(f"ξ={xi0:.2f} (no points)")
            ax.axis("off")
            continue

        # find nearest spine point in xi_fine
        j = np.argmin(np.abs(xi_fine - xi0))
        C0 = C[j]
        N0 = N_vec[j]
        B0 = B_vec[j]

        # project offsets onto (N0,B0) plane
        dY = Y[idx] - C0  # [K,3]
        u = dY @ N0       # coord along N
        v = dY @ B0       # coord along B

        # 2D histogram to reveal structure
        bins = 60
        H, u_edges, v_edges = np.histogram2d(
            u, v, bins=bins,
            range=[[-r_global, r_global], [-r_global, r_global]]
        )
        # plot as image
        extent = [u_edges[0], u_edges[-1], v_edges[0], v_edges[-1]]
        im = ax.imshow(
            H.T, origin="lower", extent=extent,
            cmap="viridis", interpolation="nearest", aspect="equal"
        )

        ax.set_title(f"Cross-section at ξ={xi0:.2f} (n={len(idx)})")
        ax.set_xlabel("u (normal)")
        ax.set_ylabel("v (binormal)")
        # zero axes (center of tube)
        ax.axhline(0, color="w", alpha=0.3, lw=0.5)
        ax.axvline(0, color="w", alpha=0.3, lw=0.5)

    # hide unused subplots
    for k in range(n_slices, n_rows * n_cols):
        row = k // n_cols
        col = k % n_cols
        axes[row, col].axis("off")

    plt.tight_layout()
    plt.savefig("latent_tomography_cross_sections.png", dpi=150)
    print("Saved 'latent_tomography_cross_sections.png'")

    # -------------------------------------------------------
    # 6. Optional: FTLE-weighted slice view at one ξ
    # -------------------------------------------------------
    # pick one slice (e.g. the "stomach" region around ξ ≈ 0.35)
    xi0 = 0.35
    mask = np.abs(xi - xi0) <= xi_band
    idx = np.where(mask)[0]

    if len(idx) > 0:
        j = np.argmin(np.abs(xi_fine - xi0))
        C0 = C[j]
        N0 = N_vec[j]
        B0 = B_vec[j]

        dY = Y[idx] - C0
        u = dY @ N0
        v = dY @ B0

        # FTLE is the 2nd field in X_sorted if we used [anchor, ftle, tension, spin, stiff]
        # (adapt this index if your order changed)
        ftle_idx = names.index("ftle") if "ftle" in names else 1
        ftle_vals = X_sorted[idx, ftle_idx]

        fig2, ax2 = plt.subplots(1, 1, figsize=(5, 5))
        sc = ax2.scatter(u, v, c=ftle_vals, s=8, cmap="plasma")
        ax2.set_title(f"Slice at ξ={xi0:.2f} colored by FTLE")
        ax2.set_xlabel("u (normal)")
        ax2.set_ylabel("v (binormal)")
        ax2.set_xlim(-r_global, r_global)
        ax2.set_ylim(-r_global, r_global)
        ax2.axhline(0, color="k", alpha=0.2, lw=0.5)
        ax2.axvline(0, color="k", alpha=0.2, lw=0.5)
        fig2.colorbar(sc, ax=ax2, label="FTLE")
        plt.tight_layout()
        plt.savefig("latent_tomography_ftle_slice.png", dpi=150)
        print("Saved 'latent_tomography_ftle_slice.png'")


if __name__ == "__main__":
    main()
