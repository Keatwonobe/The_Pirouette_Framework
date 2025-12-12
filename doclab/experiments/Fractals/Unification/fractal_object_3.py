import numpy as np
import matplotlib.pyplot as plt

# Reuse everything from step 1
from fractal_object import (
    compute_anchor,
    compute_ftle,
    compute_basin_tension,
    compute_spin,
    compute_stiffness,
    build_feature_matrix,
    diffusion_map_embedding,
)


def smooth_1d(y, window=51):
    """
    Simple boxcar smoothing. 'window' must be odd and <= len(y).
    """
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


def main():
    RES    = 80
    BOUNDS = 1.5

    print("[Step2] Recomputing fields...")
    anchor  = compute_anchor(RES, BOUNDS)
    ftle    = compute_ftle(RES, BOUNDS)
    tension, basin = compute_basin_tension(RES, BOUNDS, max_steps=120)
    spin    = compute_spin(RES, BOUNDS, steps=200)
    stiff   = compute_stiffness(RES, BOUNDS)

    X, mask_flat, names = build_feature_matrix(anchor, ftle, tension, spin, stiff)
    labels = ["log1p(Anchor)", "FTLE", "Tension", "Spin", "log1p(Stiff)"]
    print(f"[Step2] Feature matrix shape: {X.shape}")
    # Map field names to column indices in X
    idx_map = {name: names.index(name) for name in names}

    # -----------------------------------
    # 1. Diffusion-map embedding to get ψ1,ψ2,ψ3
    # -----------------------------------
    print("[Step2] Running diffusion-map embedding...")
    diff_coords, lam = diffusion_map_embedding(X, n_components=3, alpha=0.5)
    psi1 = diff_coords[:, 0]
    psi2 = diff_coords[:, 1]
    psi3 = diff_coords[:, 2]
    print(f"[Step2] Leading nontrivial eigenvalues: {lam}")

    # -----------------------------------
    # 2. Define latent coordinate ξ via arc-length along the curve
    # -----------------------------------

    # Sort points roughly along ψ1 (diffusion 1 is usually the main "flow")
    sort_idx = np.argsort(psi1)
    psi_sorted = diff_coords[sort_idx, :]    # shape (N,3)
    X_sorted   = X[sort_idx, :]             # fields in same order

    # Arc-length along the curve in (ψ1,ψ2,ψ3)
    diffs = psi_sorted[1:, :] - psi_sorted[:-1, :]
    seg_len = np.linalg.norm(diffs, axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg_len)])
    xi = s / s[-1]     # normalize 0..1

    # -----------------------------------
    # 3. Plot the latent curve colored by ξ
    # -----------------------------------
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    sc = ax.scatter(
        psi_sorted[:, 0],
        psi_sorted[:, 1],
        c=xi,
        s=6,
        cmap="viridis",
        alpha=0.8,
    )
    ax.set_xlabel("ψ1")
    ax.set_ylabel("ψ2")
    ax.set_title("Latent diffusion curve colored by ξ (arc-length)")
    plt.colorbar(sc, ax=ax, label="ξ (0..1)")
    plt.tight_layout()
    plt.savefig("latent_curve_xi.png", dpi=150)
    print("Saved 'latent_curve_xi.png'")

    # -----------------------------------
    # 4. Plot each field as a function of ξ
    # -----------------------------------
    N = len(xi)
    # choose smoothing window as ~N/30, odd
    win = max(5, (N // 30) | 1)   # ensure odd with bit trick

    fig2, axes = plt.subplots(5, 1, figsize=(8, 14), sharex=True)
    for k, ax in enumerate(axes):
        y = X_sorted[:, k]
        ys = smooth_1d(y, window=win)

        ax.scatter(xi, y, s=4, alpha=0.3, label="samples")
        ax.plot(xi, ys, linewidth=2, label="smoothed")
        ax.set_ylabel(labels[k])
        ax.grid(alpha=0.2)
        ax.legend(loc="best", fontsize=8)

    axes[-1].set_xlabel("ξ (arc-length parameter along latent curve)")
    fig2.suptitle("Pirouette fields as functions of latent coordinate ξ", y=0.92)
    plt.tight_layout()
    plt.savefig("latent_fields_vs_xi.png", dpi=150)
    print("Saved 'latent_fields_vs_xi.png'")

    # -----------------------------------
    # 5. Save data for later steps
    # -----------------------------------
    np.savez(
        "latent_curve_data.npz",
        xi=xi,
        psi_sorted=psi_sorted,
        X_sorted=X_sorted,
        names=np.array(names),
        labels=np.array(labels),
        lam=lam,
    )
    print("Saved 'latent_curve_data.npz'")

    np.savez(
        "latent_cloud.npz",
        XYZ=diff_coords,             # (N, 3) Diffusion Map Coordinates (psi1, psi2, psi3)
        anchor_flat=X[:, idx_map["anchor"]],
        ftle_flat=X[:, idx_map["ftle"]],
        tension_flat=X[:, idx_map["tension"]],
        spin_flat=X[:, idx_map["spin"]],
        stiff_flat=X[:, idx_map["stiff"]],
    )


if __name__ == "__main__":
    main()
