import numpy as np
import matplotlib.pyplot as plt

from retrograde_lyapunov import ReverseLyapunovScanner
from retrograde_time_fractal import EntropyAnchor
from time_fractal_forward import ElasticityScanner
import space_fractal
import vacuum_stiffness_fractal as vacuum_stiff

# Try optional nonlinear embeddings
try:
    from umap import UMAP
    HAS_UMAP = True
except Exception:
    HAS_UMAP = False
    UMAP = None

try:
    from sklearn.manifold import Isomap  # not used yet, but handy
    HAS_ISOMAP = True
except Exception:
    HAS_ISOMAP = False
    Isomap = None


# ----------------------------
#  FIELD COMPUTATION
# ----------------------------

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
        # unwrap angle
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
#  FEATURE MATRIX
# ----------------------------

def build_feature_matrix(anchor, ftle, tension, spin, stiff):
    a  = np.log1p(np.asarray(anchor).flatten())
    f  = np.asarray(ftle).flatten()
    t  = np.asarray(tension).flatten()
    s  = np.asarray(spin).flatten()
    st = np.log1p(np.asarray(stiff).flatten())

    mask = np.isfinite(a) & np.isfinite(f) & np.isfinite(t) & \
           np.isfinite(s) & np.isfinite(st)

    X = np.vstack([a[mask], f[mask], t[mask], s[mask], st[mask]]).T
    names = ["anchor", "ftle", "tension", "spin", "stiff"]
    return X, mask, names


# ----------------------------
#  DIFFUSION MAPS
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

    X, mask_flat, names = build_feature_matrix(anchor, ftle, tension, spin, stiff)
    print(f"[Data] Feature matrix shape: {X.shape}")

    labels = ["log1p(Anchor)", "FTLE", "Tension", "Spin", "log1p(Stiff)"]

    # -------------------------------
    # UMAP embedding (if available)
    # -------------------------------
    if HAS_UMAP:
        print("[UMAP] Fitting 2D embedding...")
        umap_model = UMAP(
            n_neighbors=30,
            n_components=2,
            min_dist=0.05,
            metric="euclidean",
            random_state=42,
        )
        umap_coords = umap_model.fit_transform(X)

        fig, axes = plt.subplots(2, 3, figsize=(12, 8))
        ax = axes.ravel()
        for k in range(5):
            sc = ax[k].scatter(
                umap_coords[:, 0],
                umap_coords[:, 1],
                c=X[:, k],
                s=4,
                alpha=0.5,
            )
            ax[k].set_title(f"UMAP: {labels[k]}")
            ax[k].set_xlabel("UMAP-1")
            ax[k].set_ylabel("UMAP-2")
            plt.colorbar(sc, ax=ax[k])
        ax[-1].axis("off")
        plt.tight_layout()
        plt.savefig("umap_manifold.png", dpi=150)
        print("Saved 'umap_manifold.png'")
    else:
        print("[UMAP] umap-learn not installed; skipping UMAP embedding.")

    # -----------------------------------
    # Diffusion map embedding (always)
    # -----------------------------------
    print("[Diffusion] Computing diffusion-map embedding...")
    diff_coords, lam = diffusion_map_embedding(X, n_components=3, alpha=0.5)
    print(f"[Diffusion] Leading nontrivial eigenvalues: {lam}")

    # ψ1 vs ψ2, colored by each observable
    fig2, axes2 = plt.subplots(2, 3, figsize=(12, 8))
    ax2 = axes2.ravel()
    for k in range(5):
        sc = ax2[k].scatter(
            diff_coords[:, 0],
            diff_coords[:, 1],
            c=X[:, k],
            s=4,
            alpha=0.5,
        )
        ax2[k].set_title(f"Diffusion: {labels[k]}")
        ax2[k].set_xlabel("ψ1")
        ax2[k].set_ylabel("ψ2")
        plt.colorbar(sc, ax=ax2[k])
    ax2[-1].axis("off")
    plt.tight_layout()
    plt.savefig("diffusion_manifold.png", dpi=150)
    print("Saved 'diffusion_manifold.png'")

    # ψ1 vs ψ2 colored by ψ3 to check for hidden 3rd mode
    fig3, ax3 = plt.subplots(1, 1, figsize=(6, 5))
    sc3 = ax3.scatter(
        diff_coords[:, 0],
        diff_coords[:, 1],
        c=diff_coords[:, 2],
        s=4,
        alpha=0.6,
    )
    ax3.set_xlabel("ψ1")
    ax3.set_ylabel("ψ2")
    ax3.set_title("Diffusion coords colored by ψ3")
    plt.colorbar(sc3, ax=ax3)
    plt.tight_layout()
    plt.savefig("diffusion_psi3.png", dpi=150)
    print("Saved 'diffusion_psi3.png'")


if __name__ == "__main__":
    main()
