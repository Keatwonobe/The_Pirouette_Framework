import numpy as np
import matplotlib.pyplot as plt

from retrograde_lyapunov import ReverseLyapunovScanner
from retrograde_time_fractal import EntropyAnchor
from time_fractal_forward import ElasticityScanner
import space_fractal
import vacuum_stiffness_fractal as vacuum_stiff

def compute_anchor(res, bounds, damping=0.015):
    """
    Entropy Anchor: orbit-length / 'cold' dissipative structure.
    Uses your vectorized EntropyAnchor on a square [-bounds, bounds]^2 grid.
    """
    anchor = EntropyAnchor(resolution=res, damping=damping)
    anchor.bounds = bounds   # override default 1.5 so we match the others
    field = anchor.run_sedimentation()
    return field

def compute_ftle(res, bounds, damping=0.015):
    """
    Reverse Lyapunov FTLE field on the same grid.
    """
    scanner = ReverseLyapunovScanner(
        resolution=res,
        damping=damping,
        bounds=bounds
    )
    field = scanner.compute_ftle_field()
    return field

def compute_basin_tension(res, bounds, max_steps=150):
    """
    Uses ElasticityScanner.measure_tension + get_destiny_simple
    over our own grid (so we control window & resolution).
    """
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
    Reimplements run_fractal_map() but parameterized, and RETURNS the
    winding map instead of just plotting it.
    Uses space_fractal.get_force_vectorized.
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
        # Force + drag
        Fm, Flam, w_red = space_fractal.get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)

        # Kick-drift-kick with drag (as in your file)
        pm   = (pm   + 0.5 * DT * Fm)   * drag
        plam = (plam + 0.5 * DT * Flam) * drag

        m   += DT * pm
        lam += DT * plam

        Fm, Flam, w_red = space_fractal.get_force_vectorized(m, lam)

        pm   = (pm   + 0.5 * DT * Fm)   * drag
        plam = (plam + 0.5 * DT * Flam) * drag

        # Winding accumulation with 2π unwrap
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
    Uses your vacuum_stiffness_fractal.compute_tensor_flow,
    but overrides its globals so we sample the same window.
    Returns sqrt(L1), the 'mass / stiffness' field.
    """
    vacuum_stiff.RES  = res
    vacuum_stiff.M_MIN = -bounds
    vacuum_stiff.M_MAX =  bounds
    vacuum_stiff.L_MIN = -bounds
    vacuum_stiff.L_MAX =  bounds

    M, L, vx, vy, mass_field = vacuum_stiff.compute_tensor_flow()
    return mass_field

def _rankify(x):
    """Convert 1D array to ranks (ties averaged)."""
    x = np.asarray(x, dtype=float)
    order = np.argsort(x)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(len(x), dtype=float)
    # normalize to [0,1]
    return ranks / (len(x) - 1.0) if len(x) > 1 else ranks

def correlate_fields(**fields):
    """
    Compute Pearson + Spearman-like (rank) correlation
    between any number of 2D fields.
    """
    names = list(fields.keys())
    raw = []
    for name in names:
        arr = np.asarray(fields[name], dtype=float)
        # basic transforms to tame heavy tails
        if name in ("anchor", "stiff"):
            arr = np.log1p(arr)  # log(1+x)
        raw.append(arr.flatten())

    raw = np.vstack(raw)

    # require finiteness across all fields
    mask = np.all(np.isfinite(raw), axis=0)
    raw = raw[:, mask]

    print(f"Using {raw.shape[1]} valid sample points for correlation.")

    # Pearson on transformed data
    pearson = np.corrcoef(raw)

    # Spearman-style: rank each variable then correlate
    ranked = np.vstack([_rankify(raw[i]) for i in range(raw.shape[0])])
    spearman = np.corrcoef(ranked)

    return names, pearson, spearman


def main():
    # You can bump these once it's working.
    RES    = 80    # 80x80 grid; increase to 150–250 for prettier bones
    BOUNDS = 1.5   # central well with all 3 arms visible

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

    # --- Ridge-only correlations (focus on the bones) ---
    # Use FTLE as our "where is the chaos?" mask.
    ftle_arr = np.asarray(ftle, dtype=float)
    thresh = np.percentile(ftle_arr[np.isfinite(ftle_arr)], 90)  # top 10%
    ridge_mask = ftle_arr > thresh

    print(f"\nRidge mask: FTLE > {thresh:.3f} (top 10% of values)")

    # Gather same fields, but only at ridge pixels
    ridge_fields = {
        "anchor":  np.asarray(anchor,  dtype=float)[ridge_mask],
        "ftle":    ftle_arr[ridge_mask],
        "tension": np.asarray(tension, dtype=float)[ridge_mask],
        "spin":    np.asarray(spin,    dtype=float)[ridge_mask],
        "stiff":   np.asarray(stiff,   dtype=float)[ridge_mask],
    }

    # Stack them
    names_r = list(ridge_fields.keys())
    data_r = np.vstack([ridge_fields[n] for n in names_r])

    # Drop NaNs/Infs again
    mask_r = np.all(np.isfinite(data_r), axis=0)
    data_r = data_r[:, mask_r]

    print(f"Using {data_r.shape[1]} ridge points for ridge correlations.")
    corr_r = np.corrcoef(data_r)

    print("\nRidge-only correlation matrix:")
    print("         " + " ".join(f"{n:>10}" for n in names_r))
    for i, ni in enumerate(names_r):
        row = " ".join(f"{corr_r[i, j]:10.3f}" for j in range(len(names_r)))
        print(f"{ni:>8} {row}")

    # --- Correlation matrices ---
    names, corr_pearson, corr_spearman = correlate_fields(
        anchor=anchor,
        ftle=ftle,
        tension=tension,
        spin=spin,
        stiff=stiff,
    )

    print("\nCorrelation matrix:")
    print("         " + " ".join(f"{n:>10}" for n in names))
    for i, ni in enumerate(names):
        row = " ".join(f"{corr_pearson[i, j]:10.3f}" for j in range(len(names)))
        print(f"{ni:>8} {row}")

    # --- Visual comparison ---
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    ax = axes.ravel()

    fields_ordered = [
        ("anchor",  anchor),
        ("ftle",    ftle),
        ("tension", tension),
        ("spin",    spin),
        ("stiff",   stiff),
    ]

    for idx, (name, field) in enumerate(fields_ordered):
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
    print("Saved figure 'fractal_cross_correlations.png'")


    print("\nPearson correlation (log-tamed):")
    print("         " + " ".join(f"{n:>10}" for n in names))
    for i, ni in enumerate(names):
        row = " ".join(f"{corr_pearson[i, j]:10.3f}" for j in range(len(names)))
        print(f"{ni:>8} {row}")

    print("\nSpearman (rank) correlation:")
    print("         " + " ".join(f"{n:>10}" for n in names))
    for i, ni in enumerate(names):
        row = " ".join(f"{corr_spearman[i, j]:10.3f}" for j in range(len(names)))
        print(f"{ni:>8} {row}")



if __name__ == "__main__":
    main()
