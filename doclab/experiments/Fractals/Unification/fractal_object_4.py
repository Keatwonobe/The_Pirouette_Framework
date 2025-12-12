import numpy as np
import matplotlib.pyplot as plt

# We only need the latent data from step 2
DATA_FILE = "latent_curve_data.npz"


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


def finite_diff(x, t):
    """
    Central finite-difference derivative dx/dt for 1D arrays.
    """
    x = np.asarray(x)
    t = np.asarray(t)
    v = np.zeros_like(x)

    # interior
    dt = t[2:] - t[:-2]
    v[1:-1] = (x[2:] - x[:-2]) / dt

    # endpoints: simple forward/backward diff
    v[0] = (x[1] - x[0]) / (t[1] - t[0])
    v[-1] = (x[-1] - x[-2]) / (t[-1] - t[-2])
    return v


def poly_fit_ode(xi, v, degree=3, mask_frac=0.95):
    """
    Fit v(ξ) with a polynomial f(ξ) using only the central portion
    of the data (to avoid noisy extreme ends).
    mask_frac: keep this fraction of points around the median of ξ.
    """
    xi = np.asarray(xi)
    v = np.asarray(v)

    # central mask in ξ-space
    mid = 0.5 * (xi.min() + xi.max())
    width = 0.5 * (xi.max() - xi.min()) * mask_frac
    lo = mid - width
    hi = mid + width
    mask = (xi >= lo) & (xi <= hi)

    coeffs = np.polyfit(xi[mask], v[mask], deg=degree)
    return coeffs


def integrate_ode(coeffs, xi0=0.0, n_steps=2000, dt=1e-3):
    """
    Simple forward Euler integration of dξ/dτ = f(ξ).
    """
    p = np.poly1d(coeffs)
    xi_traj = np.zeros(n_steps)
    tau = np.arange(n_steps) * dt

    xi_traj[0] = xi0
    for k in range(1, n_steps):
        xi_traj[k] = xi_traj[k-1] + dt * p(xi_traj[k-1])
        # optional: keep in [0,1] to avoid runaway
        if xi_traj[k] < 0.0:
            xi_traj[k] = 0.0
        if xi_traj[k] > 1.0:
            xi_traj[k] = 1.0
    return tau, xi_traj


def main():
    # --------------------------
    # 1. Load latent curve data
    # --------------------------
    data = np.load(DATA_FILE, allow_pickle=True)
    xi        = data["xi"]            # shape (N,)
    psi       = data["psi_sorted"]    # (N,3) but not needed here
    X_sorted  = data["X_sorted"]      # (N,5) fields along ξ
    names     = list(data["names"])
    labels    = list(data["labels"])
    lam       = data["lam"]

    N = len(xi)
    print(f"[Step3] Loaded {N} latent points.")
    print(f"[Step3] Fields: {names}")
    print(f"[Step3] Diffusion eigenvalues: {lam}")

    # Define parametric time τ as normalized sample index
    tau = np.linspace(0.0, 1.0, N)

    # --------------------------
    # 2. Compute dξ/dτ and smooth it
    # --------------------------
    v_raw = finite_diff(xi, tau)
    v_smooth = smooth_1d(v_raw, window=max(5, (N // 30) | 1))

    # --------------------------
    # 3. Fit polynomial ODE v(ξ) = f(ξ)
    # --------------------------
    degree = 3
    coeffs = poly_fit_ode(xi, v_smooth, degree=degree, mask_frac=0.9)
    f_poly = np.poly1d(coeffs)

    print(f"[Step3] Fitted polynomial coefficients (highest degree first):")
    print(coeffs)

    # Diagnostic grid in ξ-space
    xi_grid = np.linspace(0.0, 1.0, 400)
    v_fit = f_poly(xi_grid)

    # --------------------------
    # 4. Construct potential V(ξ) such that v = -dV/dξ
    #    (up to an additive constant)
    # --------------------------
    # numeric integral: V(ξ_i) = -∫_0^ξ f(s) ds
    V = np.zeros_like(xi_grid)
    for k in range(1, len(xi_grid)):
        dx = xi_grid[k] - xi_grid[k-1]
        V[k] = V[k-1] - 0.5 * dx * (v_fit[k] + v_fit[k-1])

    # --------------------------
    # 5. Plot v(ξ) and potential V(ξ)
    # --------------------------
    fig1, axes = plt.subplots(2, 1, figsize=(7, 8), sharex=True)

    # v(ξ)
    ax = axes[0]
    ax.scatter(xi, v_raw, s=4, alpha=0.3, label="finite diff (raw)")
    ax.plot(xi, v_smooth, "C1", lw=2, label="smoothed")
    ax.plot(xi_grid, v_fit, "C3", lw=2, label=f"poly fit (deg {degree})")
    ax.axhline(0.0, color="k", lw=1, alpha=0.5)
    ax.set_ylabel("dξ/dτ")
    ax.set_title("Latent ODE: velocity v(ξ) = dξ/dτ")
    ax.grid(alpha=0.2)
    ax.legend(loc="best", fontsize=8)

    # V(ξ)
    ax2 = axes[1]
    ax2.plot(xi_grid, V, "C2", lw=2)
    ax2.set_xlabel("ξ")
    ax2.set_ylabel("V(ξ)  (s.t.  dξ/dτ ≈ -dV/dξ)")
    ax2.set_title("Effective potential along latent coordinate")
    ax2.grid(alpha=0.2)

    plt.tight_layout()
    plt.savefig("latent_ode_velocity_potential.png", dpi=150)
    print("Saved 'latent_ode_velocity_potential.png'")

    # --------------------------
    # 6. Integrate ODE forward and compare with original ξ(τ)
    # --------------------------
    tau_sim, xi_sim = integrate_ode(coeffs, xi0=xi[0], n_steps=2000, dt=1e-3)

    fig2, ax3 = plt.subplots(1, 1, figsize=(7, 4))
    ax3.plot(tau, xi, "C0.", ms=2, alpha=0.6, label="data ξ(τ)")
    ax3.plot(tau_sim, xi_sim, "C3-", lw=2, label="ODE solution ξ(τ)")
    ax3.set_xlabel("τ (normalized sample index)")
    ax3.set_ylabel("ξ")
    ax3.set_title("Comparison of latent trajectory and fitted ODE")
    ax3.grid(alpha=0.2)
    ax3.legend(loc="best", fontsize=8)
    plt.tight_layout()
    plt.savefig("latent_ode_trajectory.png", dpi=150)
    print("Saved 'latent_ode_trajectory.png'")

    # --------------------------
    # 7. Reconstruct fields along simulated ξ(τ)
    # --------------------------
    # For each field, fit g_k(ξ) (here: low-degree polynomial for simplicity)
    K = X_sorted.shape[1]
    field_polys = []
    for k in range(K):
        # modest degree works well; too high will overfit noise
        gk = np.poly1d(np.polyfit(xi, X_sorted[:, k], deg=4))
        field_polys.append(gk)

    # Evaluate along simulated path
    fields_sim = np.zeros((len(xi_sim), K))
    for k in range(K):
        fields_sim[:, k] = field_polys[k](xi_sim)

    # Plot a quick comparison for one or two fields (FTLE, spin) as example
    fig3, axes3 = plt.subplots(2, 1, figsize=(7, 7), sharex=True)

    # FTLE
    idx_ftle = names.index("ftle")
    axes3[0].plot(tau, X_sorted[:, idx_ftle], "C0.", ms=2, alpha=0.4, label="data FTLE(τ)")
    axes3[0].plot(tau_sim, fields_sim[:, idx_ftle], "C3-", lw=2, label="recon FTLE(τ)")
    axes3[0].set_ylabel("FTLE")
    axes3[0].set_title("FTLE along latent trajectory")
    axes3[0].grid(alpha=0.2)
    axes3[0].legend(loc="best", fontsize=8)

    # Spin
    idx_spin = names.index("spin")
    axes3[1].plot(tau, X_sorted[:, idx_spin], "C0.", ms=2, alpha=0.4, label="data Spin(τ)")
    axes3[1].plot(tau_sim, fields_sim[:, idx_spin], "C3-", lw=2, label="recon Spin(τ)")
    axes3[1].set_xlabel("τ")
    axes3[1].set_ylabel("Spin")
    axes3[1].set_title("Spin along latent trajectory")
    axes3[1].grid(alpha=0.2)
    axes3[1].legend(loc="best", fontsize=8)

    plt.tight_layout()
    plt.savefig("latent_ode_field_recon.png", dpi=150)
    print("Saved 'latent_ode_field_recon.png'")

    # --------------------------
    # 8. Save coefficients & potential for future use
    # --------------------------
    np.savez(
        "latent_ode_model.npz",
        coeffs=coeffs,
        xi_grid=xi_grid,
        v_fit=v_fit,
        V=V,
        names=np.array(names),
        labels=np.array(labels),
    )
    print("Saved 'latent_ode_model.npz'")


if __name__ == "__main__":
    main()
