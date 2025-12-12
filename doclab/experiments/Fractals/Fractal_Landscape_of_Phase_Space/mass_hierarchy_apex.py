import numpy as np
import matplotlib.pyplot as plt

# Import your existing vacuum stiffness machinery
from unification_24 import (
    get_force_vectorized,
    compute_tensor_flow,
    EPS,
    M_MIN, M_MAX,
    L_MIN, L_MAX,
)

# --------------------------------------------------
# Local mass evaluator (same formula as compute_tensor_flow)
# but at a single point.
# --------------------------------------------------
def local_mass(m, lam, eps=None):
    """
    Compute the principal mass eigenvalue sqrt(L1) at a single (m, λ).
    Uses the same Jacobian -> metric -> eigenvalue chain as compute_tensor_flow.
    """
    if eps is None:
        eps = EPS * 0.5  # slightly smaller step for local probing

    # Base forces
    Fm, Flam = get_force_vectorized(m, lam)
    Fm_m, Flam_m = get_force_vectorized(m + eps, lam)
    Fm_l, Flam_l = get_force_vectorized(m, lam + eps)

    dFx_dm = (Fm_m - Fm) / eps
    dFx_dl = (Fm_l - Fm) / eps
    dFy_dm = (Flam_m - Flam) / eps
    dFy_dl = (Flam_l - Flam) / eps

    # Metric components G = J^T J
    g11 = dFx_dm**2 + dFy_dm**2
    g12 = dFx_dm * dFx_dl + dFy_dm * dFy_dl
    g22 = dFx_dl**2 + dFy_dl**2

    trace = g11 + g22
    det = g11 * g22 - g12**2
    disc = np.sqrt(max(trace**2 / 4.0 - det, 0.0))

    L1 = trace / 2.0 + disc
    return float(np.sqrt(L1))


# --------------------------------------------------
# Find the apex (maximum mass) from your global map
# --------------------------------------------------
def find_apex():
    M, L, vx, vy, Mass = compute_tensor_flow()
    idx_flat = np.argmax(Mass)
    i, j = np.unravel_index(idx_flat, Mass.shape)
    m0 = float(M[i, j])
    l0 = float(L[i, j])
    m_peak = float(Mass[i, j])
    return m0, l0, m_peak, M, L, Mass


# --------------------------------------------------
# Hessian / curvature at the apex
# --------------------------------------------------
def apex_hessian(m0, l0, h_m, h_l):
    """
    Finite-difference Hessian of the mass surface at (m0, l0).
    Returns H, eigenvalues, eigenvectors.
    """
    def f(m, lam):
        return local_mass(m, lam)

    f0 = f(m0, l0)

    f_mm_p = f(m0 + h_m, l0)
    f_mm_m = f(m0 - h_m, l0)
    f_ll_p = f(m0, l0 + h_l)
    f_ll_m = f(m0, l0 - h_l)

    f_ml_pp = f(m0 + h_m, l0 + h_l)
    f_ml_pm = f(m0 + h_m, l0 - h_l)
    f_ml_mp = f(m0 - h_m, l0 + h_l)
    f_ml_mm = f(m0 - h_m, l0 - h_l)

    f_mm = (f_mm_p - 2.0 * f0 + f_mm_m) / (h_m**2)
    f_ll = (f_ll_p - 2.0 * f0 + f_ll_m) / (h_l**2)
    f_ml = (f_ml_pp - f_ml_pm - f_ml_mp + f_ml_mm) / (4.0 * h_m * h_l)

    H = np.array([[f_mm, f_ml],
                  [f_ml, f_ll]], dtype=float)

    eigvals, eigvecs = np.linalg.eigh(H)
    return f0, H, eigvals, eigvecs


# --------------------------------------------------
# Zoomed 3D patch around the apex for visual sanity check
# --------------------------------------------------
def plot_local_patch(m0, l0, span_m=0.25, span_l=0.25, n=80):
    m_vals = np.linspace(m0 - span_m, m0 + span_m, n)
    l_vals = np.linspace(l0 - span_l, l0 + span_l, n)
    Mz, Lz = np.meshgrid(m_vals, l_vals)

    Mass_local = np.zeros_like(Mz)
    for i in range(n):
        for j in range(n):
            Mass_local[i, j] = local_mass(Mz[i, j], Lz[i, j])

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(
        Mz, Lz, Mass_local,
        rstride=1, cstride=1,
        linewidth=0, antialiased=True,
        cmap="magma"
    )

    ax.set_title("Local Vacuum Stiffness Near Needle Apex")
    ax.set_xlabel("Mass field m")
    ax.set_ylabel("Coupling field λ")
    ax.set_zlabel("Mass eigenvalue √λ₁")

    # Mark the apex
    ax.scatter([m0], [l0], [local_mass(m0, l0)], color="cyan", s=60)

    fig.colorbar(surf, shrink=0.6, aspect=12, label="√λ₁")
    plt.tight_layout()
    plt.savefig("needle_apex_local_patch.png", dpi=150)
    plt.show()


# --------------------------------------------------
# Main diagnostic
# --------------------------------------------------
def main():
    # 1. Find apex from the full stiffness map
    m0, l0, m_peak, M, L, Mass = find_apex()
    dm = float(M[0, 1] - M[0, 0])
    dl = float(L[1, 0] - L[0, 0])

    print("\n===== NEEDLE APEX LOCATION =====")
    print(f"Approx apex at m0 = {m0:.6f}, λ0 = {l0:.6f}")
    print(f"Mass eigenvalue √λ1 at grid apex ≈ {m_peak:.6f}")
    print(f"Grid spacings: Δm = {dm:.6e}, Δλ = {dl:.6e}")

    # 2. Refined local evaluation & Hessian
    h_m = dm * 0.5
    h_l = dl * 0.5
    f0, H, eigvals, eigvecs = apex_hessian(m0, l0, h_m, h_l)

    print("\n===== LOCAL MASS VALUE (refined) =====")
    print(f"√λ1 (local_mass) at apex ≈ {f0:.8f}")

    print("\n===== HESSIAN AT APEX (second derivatives of √λ1) =====")
    print("H ≈")
    print(H)

    print("\nEigenvalues (principal curvatures) κ₁ ≤ κ₂:")
    for k, ev in enumerate(eigvals):
        print(f"  κ{k+1} = {ev:.6e}")

    print("\nAssociated principal directions (columns):")
    print(eigvecs)

    # Radii of curvature (where defined / nonzero)
    print("\nApproximate radii of curvature Rᵢ = 1 / κᵢ (if |κᵢ| > 0):")
    for k, ev in enumerate(eigvals):
        if abs(ev) > 1e-10:
            print(f"  R{k+1} ≈ {1.0 / ev:.6e}")
        else:
            print(f"  R{k+1} : |κᵢ| too small / flat direction")

    # 3. Sanity: does it actually blow up as we zoom in?
    print("\n===== RADIAL PROFILE CHECK (does it diverge?) =====")
    radii = [dm, dm * 0.5, dm * 0.25, dm * 0.1, dm * 0.05]
    for r in radii:
        # sample along a diagonal ray from apex
        m_r = m0 + r / np.sqrt(2.0)
        l_r = l0 + r / np.sqrt(2.0)
        val = local_mass(m_r, l_r)
        print(f"  r = {r:.3e} -> √λ1(r) ≈ {val:.8f}")

    # 4. Plot a local patch so you can eyeball the tip shape
    plot_local_patch(m0, l0)


if __name__ == "__main__":
    main()
