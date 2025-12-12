import numpy as np
import matplotlib.pyplot as plt

from retrograde_lyapunov import ReverseLyapunovScanner
from retrograde_time_fractal import EntropyAnchor
from time_fractal_forward import ElasticityScanner
import space_fractal
import vacuum_stiffness_fractal as vacuum_stiff

# ----------------------------
#  MAP COMPUTATION
# ----------------------------

def diffusion_map_embedding(X, n_components=3, eps=None, alpha=0.5):
    """
    Simple diffusion-map implementation.

    X: (n_samples, n_features)
    Returns:
        coords: (n_samples, n_components)
        lam:    eigenvalues for those components
    """
    n = X.shape[0]
    # pairwise squared distances
    dists = np.sum((X[:, None, :] - X[None, :, :])**2, axis=-1)

    if eps is None:
        tri = dists[np.triu_indices(n, k=1)]
        eps = np.median(tri)
        if eps <= 0:
            eps = 1.0
    print(f"[Diffusion] Using eps={eps:.4g}")

    K = np.exp(-dists / eps)

    # anisotropic normalization (Coifman–Lafon)
    d = K.sum(axis=1)
    d_alpha = d**alpha
    K_tilde = K / (d_alpha[:, None] * d_alpha[None, :])

    d_tilde = K_tilde.sum(axis=1)
    P = K_tilde / d_tilde[:, None]

    # symmetrize for stable eigensolve
    D_half = np.sqrt(d_tilde)
    A = (P * D_half[None, :]) / D_half[:, None]

    vals, vecs = np.linalg.eigh(A)
    idx = np.argsort(vals)[::-1]
    vals = vals[idx]
    vecs = vecs[:, idx]

    # skip trivial first eigenpair (≈1, constant)
    lam = vals[1:n_components+1]
    psi = vecs[:, 1:n_components+1]

    coords = psi * lam[None, :]
    return coords, lam

def compute_anchor(res, bounds, damping=0.015):
    anchor = EntropyAnchor(resolution=res, damping=damping)
    anchor.bounds = bounds
    return anchor.run_sedimentation()

def compute_ftle(res, bounds, damping=0.015):
    scanner = ReverseLyapunovScanner(
        resolution=res,
        damping=damping,
        bounds=bounds
    )
    return scanner.compute_ftle_field()

def compute_basin_tension(res, bounds, max_steps=150):
    esc = ElasticityScanner(resolution=res)

    m_vals = np.linspace(-bounds, bounds, res)
    l_vals = np.linspace(-bounds, bounds, res)

    tension = np.zeros((res, res), dtype=float)
    basin   = np.zeros((res, res), dtype=int)

    for i, l in enumerate(l_vals):
        if i % max(1, res // 10) == 0:
            print(f"[Elasticity] Row {i}/{res}")
        for j, m in enumerate(m_vals):
            tension[i, j] = esc.measure_tension(m, l, max_steps=max_steps)
            basin[i, j]   = esc.get_destiny_simple(m, l)

    return tension, basin

def compute_spin(res, bounds, steps=600):
    m_range = np.linspace(-bounds, bounds, res)
    l_range = np.linspace(-bounds, bounds, res)
    M, L = np.meshgrid(m_range, l_range)

    m   = M.flatten()
    lam = L.flatten()
    pm  = np.zeros_like(m)
    plam = np.zeros_like(m)

    prev_ang   = np.arctan2(lam, m)
    total_ang  = np.zeros_like(m)

    DT    = space_fractal.DT
    GAMMA = space_fractal.GAMMA

    for step in range(steps):
        Fm, Flam, w_red = space_fractal.get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)

        pm   = (pm   + 0.5 * DT * Fm)   * drag
        plam = (plam + 0.5 * DT * Flam) * drag

        m   += DT * pm
        lam += DT * plam

        Fm, Flam, w_red = space_fractal.get_force_vectorized(m, lam)

        pm   = (pm   + 0.5 * DT * Fm)   * drag
        plam = (plam + 0.5 * DT * Flam) * drag

        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta >  np.pi, delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)

        total_ang += delta
        prev_ang   = curr_ang

        if step % 100 == 0:
            print(f"[Spin] Step {step}/{steps}")

    winding = np.abs(total_ang) / (2*np.pi)
    return winding.reshape(res, res)

def compute_stiffness(res, bounds):
    vacuum_stiff.RES   = res
    vacuum_stiff.M_MIN = -bounds
    vacuum_stiff.M_MAX =  bounds
    vacuum_stiff.L_MIN = -bounds
    vacuum_stiff.L_MAX =  bounds

    M, L, vx, vy, mass_field = vacuum_stiff.compute_tensor_flow()
    return mass_field

# ----------------------------
#  LATENT OBJECT MODEL
# ----------------------------

def build_feature_matrix(anchor, ftle, tension, spin, stiff):
    """Flatten fields and return X (n_samples x n_features) + mask."""
    a = np.log1p(np.asarray(anchor).flatten())   # tame heavy tails
    f = np.asarray(ftle).flatten()
    t = np.asarray(tension).flatten()
    s = np.asarray(spin).flatten()
    st = np.log1p(np.asarray(stiff).flatten())

    mask = np.isfinite(a) & np.isfinite(f) & np.isfinite(t) & \
           np.isfinite(s) & np.isfinite(st)

    X = np.vstack([a[mask], f[mask], t[mask], s[mask], st[mask]]).T
    names = ["anchor", "ftle", "tension", "spin", "stiff"]
    return X, mask, names

def pca_2d(X):
    """Return 2D PCA coords + components + explained variance."""
    # z-score
    mu = X.mean(axis=0, keepdims=True)
    sigma = X.std(axis=0, keepdims=True) + 1e-12
    Z = (X - mu) / sigma

    # covariance in feature space
    cov = (Z.T @ Z) / (Z.shape[0] - 1)
    vals, vecs = np.linalg.eigh(cov)
    idx = np.argsort(vals)[::-1]
    vals = vals[idx]
    vecs = vecs[:, idx]

    # project to first two PCs
    W2 = vecs[:, :2]               # (5 x 2)
    scores = Z @ W2                # (n_samples x 2)

    explained = vals / vals.sum()
    print("\nPCA eigenvalues:", vals)
    print("Explained variance:", explained)

    return scores, W2, mu, sigma, explained

def fit_quadratic(surface_X, surface_Y):
    """
    Fit quadratic model:
      y = b0 + b1*u + b2*v + b3*u^2 + b4*u*v + b5*v^2
    surface_X: (n_samples x 2) latent coords (u, v)
    surface_Y: (n_samples,) observable
    """
    u = surface_X[:, 0]
    v = surface_X[:, 1]
    Phi = np.column_stack([
        np.ones_like(u),
        u, v,
        u**2, u*v, v**2
    ])
    # least squares
    coef, *_ = np.linalg.lstsq(Phi, surface_Y, rcond=None)
    return coef  # length 6

def evaluate_quadratic(coef, U, V):
    """Evaluate quadratic model on grid of U,V."""
    b0, b1, b2, b3, b4, b5 = coef
    return (b0 + b1*U + b2*V + b3*U**2 + b4*U*V + b5*V**2)

# ----------------------------
#  MAIN
# ----------------------------

def main():
    RES    = 80
    BOUNDS = 1.5

    print("Computing maps...")
    anchor  = compute_anchor(RES, BOUNDS)
    ftle    = compute_ftle(RES, BOUNDS)
    tension, basin = compute_basin_tension(RES, BOUNDS, max_steps=120)
    spin    = compute_spin(RES, BOUNDS, steps=200)
    stiff   = compute_stiffness(RES, BOUNDS)

    # --- Build feature matrix and PCA ---
    X, mask_flat, names = build_feature_matrix(anchor, ftle, tension, spin, stiff)
    scores, W2, mu, sigma, explained = pca_2d(X)

    print(f"\nPC1 ~ {explained[0]*100:.2f}% variance, "
          f"PC2 ~ {explained[1]*100:.2f}% variance")

    # scores are (n_valid_pixels x 2). We want to reshape into RES x RES maps.
    pc1_full = np.zeros(RES*RES) * np.nan
    pc2_full = np.zeros(RES*RES) * np.nan
    pc1_full[mask_flat] = scores[:, 0]
    pc2_full[mask_flat] = scores[:, 1]
    pc1_map = pc1_full.reshape((RES, RES))
    pc2_map = pc2_full.reshape((RES, RES))

    # --- Visualize PC maps over (m,l) plane ---
    m_vals = np.linspace(-BOUNDS, BOUNDS, RES)
    l_vals = np.linspace(-BOUNDS, BOUNDS, RES)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    im1 = axes[0].imshow(pc1_map, extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS],
                         origin="lower")
    axes[0].set_title("PC1 (chaotic saddle mode)")
    plt.colorbar(im1, ax=axes[0])

    im2 = axes[1].imshow(pc2_map, extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS],
                         origin="lower")
    axes[1].set_title("PC2 (vacuum spin/stiffness mode)")
    plt.colorbar(im2, ax=axes[1])

    plt.tight_layout()
    plt.savefig("latent_pc_maps.png", dpi=150)
    print("Saved 'latent_pc_maps.png'")

    # --- Latent object: scatter in PC-space, colored by each observable ---
    # we already have X = [log1p(anchor), ftle, tension, spin, log1p(stiff)]
    fig2, axes2 = plt.subplots(2, 3, figsize=(12, 8))
    ax2 = axes2.ravel()
    labels = ["log1p(Anchor)", "FTLE", "Tension", "Spin", "log1p(Stiff)"]

    for k in range(5):
        sc = ax2[k].scatter(scores[:, 0], scores[:, 1], c=X[:, k],
                            s=4, alpha=0.5)
        ax2[k].set_xlabel("PC1")
        ax2[k].set_ylabel("PC2")
        ax2[k].set_title(labels[k])
        plt.colorbar(sc, ax=ax2[k])

    ax2[-1].axis("off")
    plt.tight_layout()
    plt.savefig("latent_object_scatter.png", dpi=150)
    print("Saved 'latent_object_scatter.png'")

    # --- Fit quadratic generative model: (PC1,PC2) -> each observable ---
    print("\nFitting quadratic surfaces in latent space...")
    coefs = {}
    for k, name in enumerate(names):
        coefs[name] = fit_quadratic(scores, X[:, k])
        print(f"{name} coefficients:", coefs[name])

    # Evaluate these surfaces on a regular latent grid just for visualization
    u_min, u_max = np.percentile(scores[:, 0], [1, 99])
    v_min, v_max = np.percentile(scores[:, 1], [1, 99])
    u_grid = np.linspace(u_min, u_max, RES)
    v_grid = np.linspace(v_min, v_max, RES)
    U, V   = np.meshgrid(u_grid, v_grid)

    fig3, axes3 = plt.subplots(2, 3, figsize=(12, 8))
    ax3 = axes3.ravel()

    for idx, name in enumerate(names):
        Z = evaluate_quadratic(coefs[name], U, V)
        im = ax3[idx].imshow(Z, extent=[u_min, u_max, v_min, v_max],
                             origin="lower")
        ax3[idx].set_title(f"{name} from quadratic(PC1,PC2)")
        plt.colorbar(im, ax=ax3[idx])

    ax3[-1].axis("off")
    plt.tight_layout()
    plt.savefig("latent_quadratic_surfaces.png", dpi=150)
    print("Saved 'latent_quadratic_surfaces.png'")

if __name__ == "__main__":
    main()
