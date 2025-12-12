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
    # avoid divide-by-zero
    N_norm[N_norm == 0] = 1.0
    N = dT_perp / N_norm

    # binormal
    B = np.cross(T, N)
    B_norm = np.linalg.norm(B, axis=1, keepdims=True)
    B_norm[B_norm == 0] = 1.0
    B = B / B_norm

    return T, N, B


def main():
    # -----------------------------------
    # 1. Load latent data
    # -----------------------------------
    data = np.load(DATA_FILE, allow_pickle=True)
    xi = data["xi"]              # (N,)
    X_sorted = data["X_sorted"]  # (N,5)
    names = list(data["names"])

    N = len(xi)
    print(f"[Step4] Loaded {N} samples along latent curve.")
    print(f"[Step4] Field names: {names}")

    # -----------------------------------
    # 2. PCA -> 3D embedding of the 5D field space
    # -----------------------------------
    Xc = X_sorted - X_sorted.mean(axis=0, keepdims=True)
    # SVD for PCA
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    W = Vt[:3].T          # [5,3] projection matrix
    Y = Xc @ W            # [N,3] embedded data

    print("[Step4] PCA done. Variance (first 3 comps):",
          (S[:3]**2 / np.sum(S**2)))

    # -----------------------------------
    # 3. Fit a smooth 3D curve C(ξ) in this PCA space
    # -----------------------------------
    deg_curve = 4
    p0 = np.poly1d(np.polyfit(xi, Y[:, 0], deg=deg_curve))
    p1 = np.poly1d(np.polyfit(xi, Y[:, 1], deg=deg_curve))
    p2 = np.poly1d(np.polyfit(xi, Y[:, 2], deg=deg_curve))

    xi_fine = np.linspace(0.0, 1.0, 200)
    C = np.stack([p0(xi_fine), p1(xi_fine), p2(xi_fine)], axis=1)  # [M,3]
    M = C.shape[0]

    # -----------------------------------
    # 4. Estimate tube radius r(ξ) from residuals
    # -----------------------------------
    # Residual distance of each data point to curve at its ξ
    C_at_xi = np.stack([p0(xi), p1(xi), p2(xi)], axis=1)
    residuals = np.linalg.norm(Y - C_at_xi, axis=1)

    # bin in ξ to get a smooth radius profile
    n_bins = 30
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    r_bins = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (xi >= bins[i]) & (xi < bins[i + 1])
        if np.any(mask):
            r_bins[i] = np.std(residuals[mask])
        else:
            r_bins[i] = 0.0

    # minimum radius so the tube doesn't collapse completely
    r_min = 0.05 * np.max(r_bins)
    r_bins = np.maximum(r_bins, r_min)

    # interpolate radius for fine grid
    r_fine = np.interp(xi_fine, bin_centers, r_bins)

    print("[Step4] Tube radius range:", r_fine.min(), "to", r_fine.max())

    # -----------------------------------
    # 5. Compute Frenet frame along the curve
    # -----------------------------------
    T, N_vec, B_vec = frenet_frame(C)

    # -----------------------------------
    # 6. Build tube surface
    # -----------------------------------
    n_theta = 24
    thetas = np.linspace(0.0, 2 * np.pi, n_theta, endpoint=False)

    X_tube = np.zeros((M, n_theta))
    Y_tube = np.zeros((M, n_theta))
    Z_tube = np.zeros((M, n_theta))

    for i in range(M):
        n = N_vec[i]
        b = B_vec[i]
        r = r_fine[i]
        for j, th in enumerate(thetas):
            offset = r * (np.cos(th) * n + np.sin(th) * b)
            pt = C[i] + offset
            X_tube[i, j] = pt[0]
            Y_tube[i, j] = pt[1]
            Z_tube[i, j] = pt[2]

    # -----------------------------------
    # 7. Plots
    # -----------------------------------

    # (a) PCA scatter + smooth curve
    fig1 = plt.figure(figsize=(7, 6))
    ax1 = fig1.add_subplot(111, projection="3d")
    ax1.scatter(Y[:, 0], Y[:, 1], Y[:, 2], s=5, alpha=0.1, label="data")
    ax1.plot(C[:, 0], C[:, 1], C[:, 2], lw=3, label="latent spine")
    ax1.set_xlabel("PC1")
    ax1.set_ylabel("PC2")
    ax1.set_zlabel("PC3")
    ax1.set_title("PCA embedding with latent spine C(ξ)")
    ax1.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("latent_spine_pca.png", dpi=150)
    print("Saved 'latent_spine_pca.png'")

    # (b) Tube around the spine
    fig2 = plt.figure(figsize=(8, 7))
    ax2 = fig2.add_subplot(111, projection="3d")
    ax2.plot_surface(
        X_tube, Y_tube, Z_tube, rstride=1, cstride=1,
        linewidth=0, alpha=0.6
    )
    ax2.plot(C[:, 0], C[:, 1], C[:, 2], color="k", lw=2)
    ax2.set_xlabel("PC1")
    ax2.set_ylabel("PC2")
    ax2.set_zlabel("PC3")
    ax2.set_title("Reconstructed latent object (tube around spine)")
    plt.tight_layout()
    plt.savefig("latent_tube_object.png", dpi=150)
    print("Saved 'latent_tube_object.png'")

    # (c) Radius profile vs ξ
    fig3, ax3 = plt.subplots(1, 1, figsize=(6, 4))
    ax3.plot(xi_fine, r_fine, lw=2)
    ax3.set_xlabel("ξ")
    ax3.set_ylabel("tube radius r(ξ)")
    ax3.set_title("Thickness of latent object along ξ")
    ax3.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("latent_tube_radius.png", dpi=150)
    print("Saved 'latent_tube_radius.png'")

    # Save geometry for later use
    np.save("latent_pca_coords.npy", Y)
    
    np.savez(
        "latent_tube_geometry.npz",
        xi_fine=xi_fine,
        C=C,
        X_tube=X_tube,
        Y_tube=Y_tube,
        Z_tube=Z_tube,
        r_fine=r_fine,
    )
    print("Saved 'latent_tube_geometry.npz'")


if __name__ == "__main__":
    main()
