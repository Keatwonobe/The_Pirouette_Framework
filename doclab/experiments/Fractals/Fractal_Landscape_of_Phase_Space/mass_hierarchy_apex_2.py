import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

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

    apex_ij = (i, j)
    return m0, l0, m_peak, M, L, Mass, apex_ij



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


###############################################
#  Helpers: gradients, centerline tracing
###############################################

def compute_gradients(m_grid, lam_grid, field):
    """
    Compute ∇(field) in physical units (∂/∂m, ∂/∂λ) on the same grid.
    field is sqrt_l1 or log(1+sqrt_l1), etc.
    """
    dm = m_grid[0,1] - m_grid[0,0]
    dl = lam_grid[1,0] - lam_grid[0,0]

    dfield_dm, dfield_dl = np.gradient(field, dm, dl, axis=(1,0))
    # note: we keep axis ordering consistent: field[lam_idx, m_idx]
    return dfield_dm, dfield_dl


def trace_centerline(m_grid, lam_grid, field,
                     start_ij, step_size=0.25, n_steps=400,
                     mode="uphill"):
    """
    Follow the "needle" through the wound by walking along the gradient.
    - mode="uphill": follow ∇field (toward stiffer vacuum)
    - mode="downhill": follow -∇field (toward relaxation / wake)

    Returns arrays of (m(s), λ(s), field(s)).
    """
    dfdm, dfdl = compute_gradients(m_grid, lam_grid, field)

    i, j = start_ij
    path_m = []
    path_lam = []
    path_val = []

    for _ in range(n_steps):
        # record current position
        path_m.append(m_grid[i, j])
        path_lam.append(lam_grid[i, j])
        path_val.append(field[i, j])

        gx = dfdm[i, j]
        gy = dfdl[i, j]
        grad = np.array([gx, gy])

        if mode == "downhill":
            grad = -grad

        norm = np.linalg.norm(grad)
        if norm == 0 or not np.isfinite(norm):
            break

        direction = grad / norm

        # step in continuous (m, λ) space
        m_new = m_grid[i, j] + step_size * direction[0]
        l_new = lam_grid[i, j] + step_size * direction[1]

        # find nearest grid index
        j = np.argmin(np.abs(m_grid[0,:] - m_new))
        i = np.argmin(np.abs(lam_grid[:,0] - l_new))

        # stop if we leave domain or field goes too small
        if (i <= 1 or i >= field.shape[0]-2 or
            j <= 1 or j >= field.shape[1]-2):
            break
        if not np.isfinite(field[i,j]):
            break

    return np.array(path_m), np.array(path_lam), np.array(path_val)


###############################################
#  Aperture → silhouette → 3D hull
###############################################

def extract_aperture_contour(m_grid, lam_grid, field,
                             apex_ij,
                             n_angles=180,
                             radius_max=0.3,
                             level_frac=0.5):
    """
    For each angle θ, march radially out from the apex until
    field falls below level_frac * field_apex.
    That intersection radius r(θ) defines the aperture curve.
    """
    i0, j0 = apex_ij
    m0 = m_grid[i0, j0]
    l0 = lam_grid[i0, j0]
    f0 = field[i0, j0]
    target = level_frac * f0

    thetas = np.linspace(0, 2*np.pi, n_angles, endpoint=False)
    radii = np.zeros_like(thetas)

    dm = m_grid[0,1] - m_grid[0,0]
    dl = lam_grid[1,0] - lam_grid[0,0]
    dr = min(dm, dl) * 0.5

    for k, theta in enumerate(thetas):
        r = dr
        last_val = f0
        found = False
        while r < radius_max:
            mm = m0 + r * np.cos(theta)
            ll = l0 + r * np.sin(theta)

            j = np.argmin(np.abs(m_grid[0,:] - mm))
            i = np.argmin(np.abs(lam_grid[:,0] - ll))

            val = field[i, j]

            if val < target and last_val >= target:
                radii[k] = r
                found = True
                break

            last_val = val
            r += dr

        if not found:
            # no crossing: set radius to 0 (angular gap)
            radii[k] = 0.0

    return thetas, radii


def reconstruct_hull_from_centerline(thetas, radii,
                                     centerline_m,
                                     centerline_lam,
                                     centerline_field,
                                     scale_with_field=True):
    """
    Extrude the aperture silhouette along the centerline.
    Returns a point cloud (X,Y,Z) in "mass–coupling–height" space.
    - thetas, radii: 2D silhouette in polar coords around apex.
    - centerline_*: 1D arrays parameterizing the needle axis.
    - If scale_with_field=True, we shrink/expand the silhouette
      proportionally to field / field_max along the axis.
    """
    # normalise radii to max = 1 for a clean shape
    r0 = radii.copy()
    max_r = np.max(r0)
    if max_r == 0:
        raise ValueError("Aperture radii are all zero; no hull to build.")
    r_norm = r0 / max_r

    if scale_with_field:
        f_norm = centerline_field / np.max(centerline_field)
    else:
        f_norm = np.ones_like(centerline_field)

    pts_m = []
    pts_lam = []
    pts_h = []   # use field itself as "height"/thickness

    for s in range(len(centerline_m)):
        m_axis = centerline_m[s]
        lam_axis = centerline_lam[s]
        scale = f_norm[s]

        for k, theta in enumerate(thetas):
            r = r_norm[k] * scale
            mm = m_axis + r * np.cos(theta)
            ll = lam_axis + r * np.sin(theta)

            pts_m.append(mm)
            pts_lam.append(ll)
            pts_h.append(centerline_field[s])

    return np.array(pts_m), np.array(pts_lam), np.array(pts_h)


###############################################
#  High-level driver (plug your data here)
###############################################

def reconstruct_traveler(m_grid, lam_grid, sqrt_l1_local,
                         apex_ij,
                         level_frac=0.5,
                         n_angles=180,
                         step_size=0.15,
                         n_steps=250):
    """
    Complete pipeline:
      1) trace downhill centerline (the 'wake') from the apex,
      2) extract aperture silhouette in polar coordinates,
      3) extrude silhouette along centerline to get a 3D hull.
    """
    # 1. trace centreline (wake) – you can also run 'uphill' for the entry path
    cm, cl, cf = trace_centerline(
        m_grid, lam_grid, sqrt_l1_local,
        start_ij=apex_ij,
        step_size=step_size,
        n_steps=n_steps,
        mode="downhill"
    )

    # 2. aperture around the apex (like your wound_channel_polar)
    thetas, radii = extract_aperture_contour(
        m_grid, lam_grid, sqrt_l1_local,
        apex_ij,
        n_angles=n_angles,
        radius_max=0.3,
        level_frac=level_frac
    )

    # 3. extrude silhouette → hull
    X, Y, Z = reconstruct_hull_from_centerline(
        thetas, radii,
        cm, cl, cf,
        scale_with_field=True
    )

    # 4. visualize
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    p = ax.scatter(X, Y, Z, s=4, alpha=0.6, c=Z, cmap="plasma")

    ax.plot(cm, cl, cf, "w-", lw=2, label="needle centreline")

    i0, j0 = apex_ij
    apex_m = m_grid[i0, j0]
    apex_l = lam_grid[i0, j0]
    apex_f = sqrt_l1_local[i0, j0]

    ax.scatter(
        [apex_m], [apex_l], [apex_f],
        color="cyan", s=50, marker="*",
        label="apex"
    )


    ax.set_xlabel("Mass field m")
    ax.set_ylabel("Coupling field λ")
    ax.set_zlabel("√λ₁ (local stiffness)")
    ax.set_title("Reconstructed Traveler Hull from Wound Geometry")
    ax.legend()
    fig.colorbar(p, ax=ax, label="√λ₁ (stiffness)")

    plt.tight_layout()
    plt.show()

    return {
        "centerline_m": cm,
        "centerline_lam": cl,
        "centerline_field": cf,
        "thetas": thetas,
        "radii": radii,
        "X": X,
        "Y": Y,
        "Z": Z,
    }

def main(run_traveler=True):
    # 1. Find apex from the full stiffness map
    m0, l0, m_peak, M, L, Mass, apex_ij = find_apex()
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

    # 5. (optional) reconstruct the traveler hull from the wound geometry
    if run_traveler:
        print("\n===== RECONSTRUCTING TRAVELER FROM WOUND GEOMETRY =====")
        reconstruct_traveler(
            M, L, Mass,
            apex_ij=apex_ij,
            level_frac=0.5,
            n_angles=180,
            step_size=0.15,
            n_steps=250,
        )


if __name__ == "__main__":
    # Set run_traveler=False if you just want the apex & Hessian diagnostics.
    main(run_traveler=True)

