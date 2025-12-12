import numpy as np
import matplotlib.pyplot as plt

from retrograde_lyapunov import ReverseLyapunovScanner
from retrograde_time_fractal import EntropyAnchor
from time_fractal_forward import ElasticityScanner
import space_fractal
import vacuum_stiffness_fractal as vacuum_stiff

# ----------------------------
#  MAP COMPUTATION HELPERS
# ----------------------------

def compute_anchor(res, bounds, damping=0.015):
    """Entropy Anchor: orbit-length / dissipative freezing."""
    anchor = EntropyAnchor(resolution=res, damping=damping)
    anchor.bounds = bounds
    field = anchor.run_sedimentation()
    return field

def compute_ftle(res, bounds, damping=0.015):
    """Reverse Lyapunov FTLE field on the same grid."""
    scanner = ReverseLyapunovScanner(
        resolution=res,
        damping=damping,
        bounds=bounds
    )
    field = scanner.compute_ftle_field()
    return field

def compute_basin_tension(res, bounds, max_steps=150):
    """ElasticityScanner tension + basin index on our own grid."""
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
    """
    Spin (winding number) map for the unified field.
    Reuses space_fractal.get_force_vectorized + time step / drag.
    """
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
    """
    Stiffness = sqrt(largest eigenvalue of G = J^T J)
    from your vacuum_stiffness_fractal module.
    """
    vacuum_stiff.RES   = res
    vacuum_stiff.M_MIN = -bounds
    vacuum_stiff.M_MAX =  bounds
    vacuum_stiff.L_MIN = -bounds
    vacuum_stiff.L_MAX =  bounds

    M, L, vx, vy, mass_field = vacuum_stiff.compute_tensor_flow()
    return mass_field

# ----------------------------
#  STATS / PCA HELPERS
# ----------------------------

def _rankify(x):
    """Convert 1D array to ranks in [0, 1]."""
    x = np.asarray(x, dtype=float)
    order = np.argsort(x)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(len(x), dtype=float)
    if len(x) > 1:
        ranks /= (len(x) - 1.0)
    return ranks

def _prepare_matrix(fields, mask=None):
    """
    Flatten and log-tame fields into a (n_vars, n_samples) matrix.
    Optionally apply a boolean mask on the 2D grid.
    """
    names = list(fields.keys())
    flat_list = []
    mask_flat = None

    # Flatten / mask
    for name in names:
        arr = np.asarray(fields[name], dtype=float)
        if mask is not None:
            m = np.asarray(mask, dtype=bool)
            arr = arr[m]
        else:
            arr = arr.flatten()

        # tame heavy tails a bit
        if name in ("anchor", "stiff"):
            arr = np.log1p(arr)

        flat_list.append(arr)

    data = np.vstack(flat_list)  # (n_vars, n_samples)

    # require finiteness across all vars
    mask_finite = np.all(np.isfinite(data), axis=0)
    data = data[:, mask_finite]

    return names, data

def correlate_fields(fields, mask=None):
    """
    Pearson + Spearman-like correlations for a dict of 2D fields.
    Optional mask restricts to subset of the grid.
    """
    names, data = _prepare_matrix(fields, mask=mask)
    print(f"Using {data.shape[1]} sample points for correlation.")

    # Pearson
    pearson = np.corrcoef(data)

    # Spearman-style: rank each row then correlate
    ranked = np.vstack([_rankify(data[i]) for i in range(data.shape[0])])
    spearman = np.corrcoef(ranked)

    return names, pearson, spearman

def run_pca(fields, mask=None):
    """
    PCA on the same prepared matrix used for correlations.
    Returns eigenvalues, eigenvectors, and prints loadings.
    """
    names, data = _prepare_matrix(fields, mask=mask)
    # z-score each variable
    means = data.mean(axis=1, keepdims=True)
    stds  = data.std(axis=1, keepdims=True) + 1e-12
    Z = (data - means) / stds

    # covariance in variable-space (n_vars x n_vars)
    cov = (Z @ Z.T) / (Z.shape[1] - 1)
    vals, vecs = np.linalg.eigh(cov)  # ascending order
    idx = np.argsort(vals)[::-1]      # descending
    vals = vals[idx]
    vecs = vecs[:, idx]

    total_var = vals.sum()
    exp_var_ratio = vals / total_var

    print("\nPCA results:")
    for k in range(len(names)):
        print(f"PC{k+1}: eigenvalue={vals[k]:.4f}, "
              f"explained variance={100*exp_var_ratio[k]:.2f}%")

    # Print loadings for the first two PCs
    for pc in range(min(2, len(names))):
        print(f"\nLoadings for PC{pc+1}:")
        for i, name in enumerate(names):
            loading = vecs[i, pc]
            print(f"  {name:>8}: {loading:+.3f}")

    # Optional: simple bar plot of first two PCs
    fig, axes = plt.subplots(1, 2, figsize=(8, 3))
    x = np.arange(len(names))
    for pc, ax in enumerate(axes):
        if pc >= vecs.shape[1]:
            ax.axis("off")
            continue
        ax.bar(x, vecs[:, pc])
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha="right")
        ax.set_title(f"PC{pc+1} loadings")
    plt.tight_layout()
    plt.savefig("pca_loadings.png", dpi=150)
    print("Saved 'pca_loadings.png'")

    return names, vals, vecs, exp_var_ratio

# ----------------------------
#  MAIN EXPERIMENT
# ----------------------------

def main():
    RES    = 80
    BOUNDS = 1.5

    print("Computing Entropy Anchor...")
    anchor = compute_anchor(RES, BOUNDS)

    print("Computing Reverse Lyapunov (FTLE)...")
    ftle = compute_ftle(RES, BOUNDS)

    print("Computing Fate/Tension...")
    tension, basin = compute_basin_tension(RES, BOUNDS, max_steps=120)

    print("Computing Spin map (unified field)...")
    spin = compute_spin(RES, BOUNDS, steps=200)

    print("Computing Stiffness surface (vacuum metric)...")
    stiff = compute_stiffness(RES, BOUNDS)

    # Package fields once
    field_dict = {
        "anchor":  anchor,
        "ftle":    ftle,
        "tension": tension,
        "spin":    spin,
        "stiff":   stiff,
    }

    # --------------------
    # Ridge-only stats
    # --------------------
    ftle_arr = np.asarray(ftle, dtype=float)
    finite_ftle = ftle_arr[np.isfinite(ftle_arr)]

    ridge_pct = 80.0   # <- knob: "thickness" of bones (80 = top 20%)
    thresh = np.percentile(finite_ftle, ridge_pct)
    ridge_mask = ftle_arr > thresh

    print(f"\nRidge mask: FTLE > {thresh:.3f} "
          f"(top {100 - ridge_pct:.1f}% of values)")

    names_r, pear_r, spear_r = correlate_fields(field_dict, mask=ridge_mask)

    print("\nRidge-only Pearson (log-tamed):")
    print("         " + " ".join(f"{n:>10}" for n in names_r))
    for i, ni in enumerate(names_r):
        row = " ".join(f"{pear_r[i, j]:10.3f}" for j in range(len(names_r)))
        print(f"{ni:>8} {row}")

    print("\nRidge-only Spearman (rank):")
    print("         " + " ".join(f"{n:>10}" for n in names_r))
    for i, ni in enumerate(names_r):
        row = " ".join(f"{spear_r[i, j]:10.3f}" for j in range(len(names_r)))
        print(f"{ni:>8} {row}")

    # --------------------
    # Global correlations
    # --------------------
    names, pear, spear = correlate_fields(field_dict, mask=None)

    print("\nGlobal Pearson (log-tamed):")
    print("         " + " ".join(f"{n:>10}" for n in names))
    for i, ni in enumerate(names):
        row = " ".join(f"{pear[i, j]:10.3f}" for j in range(len(names)))
        print(f"{ni:>8} {row}")

    print("\nGlobal Spearman (rank):")
    print("         " + " ".join(f"{n:>10}" for n in names))
    for i, ni in enumerate(names):
        row = " ".join(f"{spear[i, j]:10.3f}" for j in range(len(names)))
        print(f"{ni:>8} {row}")

    # --------------------
    # PCA on all fields
    # --------------------
    run_pca(field_dict, mask=None)

    # --------------------
    # Visual comparison maps
    # --------------------
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    ax = axes.ravel()

    ordered = [
        ("anchor",  anchor),
        ("ftle",    ftle),
        ("tension", tension),
        ("spin",    spin),
        ("stiff",   stiff),
    ]

    for idx, (name, field) in enumerate(ordered):
        im = ax[idx].imshow(
            field,
            extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS],
            origin="lower"
        )
        ax[idx].set_title(name)
        plt.colorbar(im, ax=ax[idx])

    ax[-1].axis("off")
    plt.tight_layout()
    plt.savefig("fractal_cross_correlations.png", dpi=150)
    print("Saved 'fractal_cross_correlations.png'")

    # --------------------
    # Scatter plots
    # --------------------
    anchor_f = np.log1p(np.asarray(anchor).flatten())
    ftle_f   = np.asarray(ftle).flatten()
    ten_f    = np.asarray(tension).flatten()
    spin_f   = np.asarray(spin).flatten()
    stiff_f  = np.log1p(np.asarray(stiff).flatten())

    mask_all = np.isfinite(anchor_f) & np.isfinite(ftle_f) & \
               np.isfinite(ten_f) & np.isfinite(spin_f) & \
               np.isfinite(stiff_f)

    anchor_f = anchor_f[mask_all]
    ftle_f   = ftle_f[mask_all]
    ten_f    = ten_f[mask_all]
    spin_f   = spin_f[mask_all]
    stiff_f  = stiff_f[mask_all]

    fig2, axs2 = plt.subplots(2, 2, figsize=(10, 8))

    axs2[0, 0].scatter(ftle_f, ten_f, s=4, alpha=0.3)
    axs2[0, 0].set_xlabel("FTLE")
    axs2[0, 0].set_ylabel("Tension")
    axs2[0, 0].set_title("FTLE vs Tension")

    axs2[0, 1].scatter(ftle_f, anchor_f, s=4, alpha=0.3)
    axs2[0, 1].set_xlabel("FTLE")
    axs2[0, 1].set_ylabel("log1p(Anchor)")
    axs2[0, 1].set_title("FTLE vs Anchor")

    axs2[1, 0].scatter(spin_f, stiff_f, s=4, alpha=0.3)
    axs2[1, 0].set_xlabel("Spin")
    axs2[1, 0].set_ylabel("log1p(Stiff)")
    axs2[1, 0].set_title("Spin vs Stiff")

    axs2[1, 1].scatter(anchor_f, stiff_f, s=4, alpha=0.3)
    axs2[1, 1].set_xlabel("log1p(Anchor)")
    axs2[1, 1].set_ylabel("log1p(Stiff)")
    axs2[1, 1].set_title("Anchor vs Stiff")

    plt.tight_layout()
    plt.savefig("fractal_scatter_plots.png", dpi=150)
    print("Saved 'fractal_scatter_plots.png'")

if __name__ == "__main__":
    main()
