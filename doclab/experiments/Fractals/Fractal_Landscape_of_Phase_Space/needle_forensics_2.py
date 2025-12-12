# traveler_reconstruction.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

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
    ax.scatter([m_grid[apex_ij]], [lam_grid[apex_ij]],
               [sqrt_l1_local[apex_ij]],
               color="cyan", s=50, marker="*",
               label="apex")

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
if __name__ == "__main__":
    reconstruct_traveler()
