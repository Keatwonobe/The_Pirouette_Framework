import numpy as np
import matplotlib.pyplot as plt

"""
needle_internal_decoder.py

Decode the internal structure of the stiffness "needle" by
sampling curvature (Hessian eigenvalues / eigenvectors) along
its centreline and extracting:

  - principal curvatures κ₁, κ₂
  - orientation of the dominant principal direction
  - anisotropy ratio
  - twist (rotation of principal frame along the axis)

This script is designed to live next to:

    - unification_24.py
    - mass_hierarchy_apex_2.py   (or mass_hierarchy_apex.py)

and re-uses the existing apex / centreline machinery.
"""

# ---------------------------------------------------------------------
# Imports from your existing needle / apex code
# ---------------------------------------------------------------------
try:
    # Newer filename
    from mass_hierarchy_apex_2 import (
        local_mass,
        find_apex,
        compute_gradients,
        trace_centerline,
    )
except ImportError:  # pragma: no cover
    # Older filename for backwards compatibility
    from mass_hierarchy_apex import (
        local_mass,
        find_apex,
        compute_gradients,
        trace_centerline,
    )


# ---------------------------------------------------------------------
# Finite-difference Hessian for √λ₁ at an arbitrary (m, λ)
# ---------------------------------------------------------------------
def hessian_at_point(m0, l0, h_m, h_l):
    """
    Compute the 2×2 Hessian of the local mass eigenvalue √λ₁
    at (m0, l0) using central finite differences.

        H_ij = ∂²f / ∂x_i ∂x_j,  x = (m, λ)

    Returns (H, eigvals, eigvecs) with eigvals sorted ascending.
    """
    def f(m, lam):
        return local_mass(m, lam)

    f0 = f(m0, l0)

    # second derivatives along m and λ
    f_mm_p = f(m0 + h_m, l0)
    f_mm_m = f(m0 - h_m, l0)
    f_ll_p = f(m0, l0 + h_l)
    f_ll_m = f(m0, l0 - h_l)

    f_mm = (f_mm_p - 2.0 * f0 + f_mm_m) / (h_m ** 2)
    f_ll = (f_ll_p - 2.0 * f0 + f_ll_m) / (h_l ** 2)

    # mixed derivative
    f_ml_pp = f(m0 + h_m, l0 + h_l)
    f_ml_pm = f(m0 + h_m, l0 - h_l)
    f_ml_mp = f(m0 - h_m, l0 + h_l)
    f_ml_mm = f(m0 - h_m, l0 - h_l)
    f_ml = (f_ml_pp - f_ml_pm - f_ml_mp + f_ml_mm) / (4.0 * h_m * h_l)

    H = np.array([[f_mm, f_ml],
                  [f_ml, f_ll]], dtype=float)

    eigvals, eigvecs = np.linalg.eigh(H)
    return H, eigvals, eigvecs


# ---------------------------------------------------------------------
# Sample curvature along the needle centreline
# ---------------------------------------------------------------------
def sample_along_needle(M, L, Mass, apex_ij,
                        step_size=0.15,
                        n_steps=200,
                        h_factor=0.5):
    """
    Follow the needle centreline (downhill in √λ₁) starting from
    the apex, and at each step compute:

        - principal curvatures κ₁, κ₂
        - dominant direction orientation angle θ
        - anisotropy ratio A = (|κ₂| - |κ₁|) / (|κ₂| + |κ₁|)
    """
    # Trace the centreline using your existing helper
    cm, cl, cf = trace_centerline(
        M, L, Mass,
        start_ij=apex_ij,
        step_size=step_size,
        n_steps=n_steps,
        mode="downhill",
    )

    # grid spacings → finite-difference steps
    dm = float(M[0, 1] - M[0, 0])
    dl = float(L[1, 0] - L[0, 0])
    h_m = dm * h_factor
    h_l = dl * h_factor

    n = len(cm)
    k1 = np.zeros(n)
    k2 = np.zeros(n)
    theta = np.zeros(n)      # orientation of dominant curvature direction
    anis = np.zeros(n)       # anisotropy ratio

    for i in range(n):
        m0 = cm[i]
        l0 = cl[i]

        H, eigvals, eigvecs = hessian_at_point(m0, l0, h_m, h_l)
        # eigenvalues sorted ascending: κ₁ ≤ κ₂
        k1[i] = eigvals[0]
        k2[i] = eigvals[1]

        # pick eigenvector associated with largest |κ|
        idx_dom = 0 if abs(eigvals[0]) > abs(eigvals[1]) else 1
        v_dom = eigvecs[:, idx_dom]

        # orientation angle in the (m, λ) plane
        theta[i] = np.arctan2(v_dom[1], v_dom[0])

        # curvature anisotropy (−1 … 1)
        num = abs(k2[i]) - abs(k1[i])
        den = abs(k2[i]) + abs(k1[i]) + 1e-12
        anis[i] = num / den

    # arc length along the centreline in (m, λ) space
    ds = np.sqrt(np.diff(cm) ** 2 + np.diff(cl) ** 2)
    s = np.concatenate([[0.0], np.cumsum(ds)])

    return {
        "s": s,
        "cm": cm,
        "cl": cl,
        "cf": cf,
        "k1": k1,
        "k2": k2,
        "theta": theta,
        "anisotropy": anis,
    }


# ---------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------
def plot_curvature_profiles(data, prefix="needle"):
    s = data["s"]
    k1 = data["k1"]
    k2 = data["k2"]

    plt.figure(figsize=(8, 5))
    plt.plot(s, k1, label=r"$\kappa_1$")
    plt.plot(s, k2, label=r"$\kappa_2$")
    plt.axhline(0.0, linestyle="--", linewidth=0.8)
    plt.xlabel("Arc length s along needle (in m–λ space)")
    plt.ylabel("Principal curvatures κ")
    plt.title("Principal Curvatures Along Needle Centreline")
    plt.legend()
    plt.tight_layout()
    fname = f"{prefix}_curvature_profile.png"
    plt.savefig(fname, dpi=160)
    print(f"[saved] {fname}")


def plot_orientation_and_twist(data, prefix="needle"):
    s = data["s"]
    theta = np.unwrap(data["theta"])
    anis = data["anisotropy"]

    # Orientation & twist
    plt.figure(figsize=(8, 5))
    plt.plot(s, theta, label=r"orientation $\theta$")
    # approximate twist = dθ/ds
    dtheta_ds = np.gradient(theta, s + 1e-12)
    plt.plot(s, dtheta_ds, label=r"twist $d\theta/ds$")
    plt.xlabel("Arc length s along needle")
    plt.ylabel("Angle / twist")
    plt.title("Needle Frame Orientation and Twist")
    plt.legend()
    plt.tight_layout()
    fname = f"{prefix}_orientation_twist.png"
    plt.savefig(fname, dpi=160)
    print(f"[saved] {fname}")

    # Anisotropy along axis
    plt.figure(figsize=(8, 5))
    plt.plot(s, anis)
    plt.xlabel("Arc length s along needle")
    plt.ylabel("Anisotropy A")
    plt.title("Curvature Anisotropy Along Needle")
    plt.tight_layout()
    fname = f"{prefix}_anisotropy_profile.png"
    plt.savefig(fname, dpi=160)
    print(f"[saved] {fname}")


def plot_centerline_on_field(M, L, Mass, apex_ij, data, prefix="needle"):
    cm = data["cm"]
    cl = data["cl"]
    anis = data["anisotropy"]

    plt.figure(figsize=(9, 7))
    # background field
    plt.pcolormesh(M, L, Mass, shading="auto")
    cbar = plt.colorbar()
    cbar.set_label(r"$\sqrt{\lambda_1}$ (stiffness)")

    # colour centreline by anisotropy magnitude
    sc = plt.scatter(cm, cl, c=np.abs(anis), cmap="viridis",
                     edgecolors="white", linewidths=0.5)
    plt.colorbar(sc, label="|anisotropy| along centreline")

    i0, j0 = apex_ij
    apex_m = M[i0, j0]
    apex_l = L[i0, j0]
    plt.scatter([apex_m], [apex_l], marker="*", s=120,
                edgecolors="black", facecolors="white", zorder=5)

    plt.xlabel("Mass field m")
    plt.ylabel("Coupling field λ")
    plt.title("Needle Centreline on Vacuum Stiffness Field")
    plt.tight_layout()
    fname = f"{prefix}_centerline_anisotropy.png"
    plt.savefig(fname, dpi=180)
    print(f"[saved] {fname}")


# ---------------------------------------------------------------------
# High-level driver
# ---------------------------------------------------------------------
def main():
    # 1) recover apex and global field
    m0, l0, m_peak, M, L, Mass, apex_ij = find_apex()

    print("=== Needle Internal Decoder ===")
    print(f"Apex at m0 = {m0:.6f}, λ0 = {l0:.6f}")
    print(f"Peak √λ₁ ≈ {m_peak:.6f}")

    # 2) sample curvature along the needle axis
    data = sample_along_needle(
        M, L, Mass,
        apex_ij=apex_ij,
        step_size=0.15,
        n_steps=220,
        h_factor=0.5,
    )

    # 3) generate diagnostic plots
    plot_curvature_profiles(data, prefix="needle")
    plot_orientation_and_twist(data, prefix="needle")
    plot_centerline_on_field(M, L, Mass, apex_ij, data, prefix="needle")

    print("\nDone. Generated:")
    print("  - needle_curvature_profile.png")
    print("  - needle_orientation_twist.png")
    print("  - needle_anisotropy_profile.png")
    print("  - needle_centerline_anisotropy.png")


if __name__ == "__main__":
    main()
