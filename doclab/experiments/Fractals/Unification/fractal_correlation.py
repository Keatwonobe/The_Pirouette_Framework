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

def correlate_fields(**fields):
    """
    Compute Pearson correlation between any number of 2D fields.
    """
    names = list(fields.keys())
    data = []

    for name in names:
        arr = np.asarray(fields[name], dtype=float)
        data.append(arr.flatten())

    data = np.vstack(data)

    # Require all indicators to be finite at a point
    mask = np.all(np.isfinite(data), axis=0)
    data = data[:, mask]

    print(f"Using {data.shape[1]} valid sample points for correlation.")
    corr = np.corrcoef(data)
    return names, corr

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

    # --- Correlation matrix ---
    names, corr = correlate_fields(
        anchor=anchor,
        ftle=ftle,
        tension=tension,
        spin=spin,
        stiff=stiff,
    )

    print("\nCorrelation matrix:")
    print("         " + " ".join(f"{n:>10}" for n in names))
    for i, ni in enumerate(names):
        row = " ".join(f"{corr[i, j]:10.3f}" for j in range(len(names)))
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

if __name__ == "__main__":
    main()
