import numpy as np
import matplotlib.pyplot as plt

"""
needle_frenet_tripod_decoder.py

Refined needle analysis:

  1) Build a Frenet-like frame (tangent + normal) along the needle
     centreline in (m, λ)-space.
  2) Project the Hessian H of √λ₁ into this frame to get:
       κ_t = tᵀ H t      (curvature along axis)
       κ_n = nᵀ H n      (curvature normal to axis)
  3) Smooth the curvature profiles to suppress numerical noise.
  4) Compare the dominant principal-curvature direction to
     a user-specified SU(3)-like tripod of directions in the
     (m, λ) plane.

Lives next to:
  - unification_24.py
  - mass_hierarchy_apex_2.py  (or mass_hierarchy_apex.py)
"""

# ---------------------------------------------------------------------
# Tripod definition (EDIT THESE ANGLES TO MATCH YOUR TRIPOD)
# ---------------------------------------------------------------------
# Each angle is measured in radians in the (m, λ) plane, using the same
# convention as arctan2(λ, m). Replace these with the directions you
# inferred from JT, JR, JG in your earlier color-generator work.
#
# Example placeholder: three legs 120° apart
tripod_angles = {
    "T": 0.0,                 #   0°  (pointing roughly +m)
    "R": 2.0 * np.pi / 3.0,   # 120°
    "G": 4.0 * np.pi / 3.0,   # 240°
}


# ---------------------------------------------------------------------
# Imports from your existing apex / needle machinery
# ---------------------------------------------------------------------
try:
    from mass_hierarchy_apex_2 import (
        local_mass,
        find_apex,
        trace_centerline,
    )
except ImportError:  # pragma: no cover
    from mass_hierarchy_apex import (
        local_mass,
        find_apex,
        trace_centerline,
    )


# ---------------------------------------------------------------------
# Finite-difference Hessian for √λ₁
# ---------------------------------------------------------------------
def hessian_at_point(m0, l0, h_m, h_l):
    """2×2 Hessian of f = √λ₁(m, λ) at (m0, l0)."""
    def f(m, lam):
        return local_mass(m, lam)

    f0 = f(m0, l0)

    f_mm_p = f(m0 + h_m, l0)
    f_mm_m = f(m0 - h_m, l0)
    f_ll_p = f(m0, l0 + h_l)
    f_ll_m = f(m0, l0 - h_l)

    f_mm = (f_mm_p - 2.0 * f0 + f_mm_m) / (h_m ** 2)
    f_ll = (f_ll_p - 2.0 * f0 + f_ll_m) / (h_l ** 2)

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
# Simple moving-average smoother
# ---------------------------------------------------------------------
def smooth(arr, window=5):
    if window <= 1:
        return arr.copy()
    kernel = np.ones(window, dtype=float) / window
    return np.convolve(arr, kernel, mode="same")


# ---------------------------------------------------------------------
# Angle-difference helper → wrap to [-π, π]
# ---------------------------------------------------------------------
def angle_diff(a, b):
    d = a - b
    return np.arctan2(np.sin(d), np.cos(d))


# ---------------------------------------------------------------------
# Frenet + tripod sampling along needle
# ---------------------------------------------------------------------
def sample_frenet_tripod(M, L, Mass, apex_ij,
                         step_size=0.15,
                         n_steps=220,
                         h_factor=0.5,
                         smooth_window=7):
    """
    1) Trace needle centreline from apex (downhill in √λ₁).
    2) Build tangent / normal vectors along the path.
    3) Compute Hessian at each point and project onto:
         - tangential direction t
         - normal direction n
    4) Record principal-curvature orientation θ_dom(s) and
       its differences to the tripod directions.
    """
    # 1. Trace centreline
    cm, cl, cf = trace_centerline(
        M, L, Mass,
        start_ij=apex_ij,
        step_size=step_size,
        n_steps=n_steps,
        mode="downhill",
    )

    n = len(cm)
    if n < 5:
        raise RuntimeError("Centreline too short for Frenet analysis.")

    # 2. Arc-length parameter
    ds = np.sqrt(np.diff(cm) ** 2 + np.diff(cl) ** 2)
    s = np.concatenate([[0.0], np.cumsum(ds)])

    # 3. Tangent & normal (central differences for interior points)
    t_vecs = np.zeros((n, 2))
    for i in range(1, n - 1):
        dm = cm[i + 1] - cm[i - 1]
        dl = cl[i + 1] - cl[i - 1]
        v = np.array([dm, dl], dtype=float)
        norm = np.linalg.norm(v)
        if norm < 1e-14:
            t_vecs[i] = t_vecs[i - 1]
        else:
            t_vecs[i] = v / norm

    # endpoints: copy neighbours
    t_vecs[0] = t_vecs[1]
    t_vecs[-1] = t_vecs[-2]

    # normals = rotated tangents
    n_vecs = np.zeros_like(t_vecs)
    n_vecs[:, 0] = -t_vecs[:, 1]
    n_vecs[:, 1] =  t_vecs[:, 0]

    # 4. Finite-difference step sizes for Hessian
    dm_grid = float(M[0, 1] - M[0, 0])
    dl_grid = float(L[1, 0] - L[0, 0])
    h_m = dm_grid * h_factor
    h_l = dl_grid * h_factor

    # storage
    k_t = np.zeros(n)
    k_n = np.zeros(n)
    k_cross = np.zeros(n)
    theta_dom = np.zeros(n)

    # tripod comparison: angle differences for each leg
    tripod_deltas = {name: np.zeros(n) for name in tripod_angles.keys()}

    for i in range(n):
        m0 = cm[i]
        l0 = cl[i]
        t = t_vecs[i]
        nvec = n_vecs[i]

        H, eigvals, eigvecs = hessian_at_point(m0, l0, h_m, h_l)

        # curvature projections in Frenet frame
        k_t[i] = float(t @ (H @ t))
        k_n[i] = float(nvec @ (H @ nvec))
        k_cross[i] = float(t @ (H @ nvec))

        # dominant principal direction (largest |κ|)
        idx_dom = 0 if abs(eigvals[0]) > abs(eigvals[1]) else 1
        v_dom = eigvecs[:, idx_dom]
        theta_dom[i] = np.arctan2(v_dom[1], v_dom[0])

        # tripod alignment
        for name, phi in tripod_angles.items():
            tripod_deltas[name][i] = angle_diff(theta_dom[i], phi)

    # 5. Smooth curvature profiles (but keep endpoints as-is)
    k_t_s = smooth(k_t, smooth_window)
    k_n_s = smooth(k_n, smooth_window)

    return {
        "s": s,
        "cm": cm,
        "cl": cl,
        "cf": cf,
        "t_vecs": t_vecs,
        "n_vecs": n_vecs,
        "k_t": k_t_s,
        "k_n": k_n_s,
        "k_cross": k_cross,
        "theta_dom": theta_dom,
        "tripod_deltas": tripod_deltas,
    }


# ---------------------------------------------------------------------
# Plotters
# ---------------------------------------------------------------------
def plot_frenet_curvature(data, prefix="needle_frenet"):
    s = data["s"]
    k_t = data["k_t"]
    k_n = data["k_n"]

    plt.figure(figsize=(8, 5))
    plt.plot(s, k_t, label=r"$\kappa_t$ (along axis)")
    plt.plot(s, k_n, label=r"$\kappa_n$ (normal to axis)")
    plt.axhline(0.0, linestyle="--", linewidth=0.8)
    plt.xlabel("Arc length s along needle (m–λ)")
    plt.ylabel("Curvature in Frenet frame")
    plt.title("Frenet-Frame Curvatures Along Needle")
    plt.legend()
    plt.tight_layout()
    fname = f"{prefix}_curvature.png"
    plt.savefig(fname, dpi=170)
    print(f"[saved] {fname}")


def plot_tripod_alignment(data, prefix="needle_frenet"):
    s = data["s"]
    tripod_deltas = data["tripod_deltas"]

    plt.figure(figsize=(8, 5))
    for name, deltas in tripod_deltas.items():
        plt.plot(s, deltas, label=f"Δθ vs {name}")
    plt.axhline(0.0, linestyle="--", linewidth=0.8, color="black")
    plt.xlabel("Arc length s along needle (m–λ)")
    plt.ylabel("Angle difference Δθ (rad)")
    plt.title("Needle Dominant Curvature vs Tripod Directions")
    plt.legend()
    plt.tight_layout()
    fname = f"{prefix}_tripod_alignment.png"
    plt.savefig(fname, dpi=170)
    print(f"[saved] {fname}")

    # quick numeric summary
    print("\nTripod alignment summary (mean |Δθ| over interior of needle):")
    interior = slice(3, max(3, len(s) - 3))
    best_name = None
    best_val = None
    for name, deltas in tripod_deltas.items():
        mean_abs = float(np.mean(np.abs(deltas[interior])))
        print(f"  {name}: mean |Δθ| ≈ {mean_abs:.3f} rad")
        if best_val is None or mean_abs < best_val:
            best_val = mean_abs
            best_name = name
    print(f"--> Closest tripod leg: {best_name} (≈ {best_val:.3f} rad)")


def plot_centerline_on_field(M, L, Mass, apex_ij, data, prefix="needle_frenet"):
    cm = data["cm"]
    cl = data["cl"]

    plt.figure(figsize=(9, 7))
    plt.pcolormesh(M, L, Mass, shading="auto")
    cbar = plt.colorbar()
    cbar.set_label(r"$\sqrt{\lambda_1}$ (stiffness)")

    plt.plot(cm, cl, "w.-", lw=1.5, ms=4, label="needle centreline")

    i0, j0 = apex_ij
    apex_m = M[i0, j0]
    apex_l = L[i0, j0]
    plt.scatter([apex_m], [apex_l], marker="*", s=130,
                edgecolors="black", facecolors="white", zorder=5,
                label="apex")

    plt.xlabel("Mass field m")
    plt.ylabel("Coupling field λ")
    plt.title("Needle Centreline on Vacuum Stiffness Field")
    plt.legend()
    plt.tight_layout()
    fname = f"{prefix}_centerline.png"
    plt.savefig(fname, dpi=180)
    print(f"[saved] {fname}")


# ---------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------
def main():
    # 1) Apex + global field
    m0, l0, m_peak, M, L, Mass, apex_ij = find_apex()
    print("=== Needle Frenet + Tripod Decoder ===")
    print(f"Apex at m0 = {m0:.6f}, λ0 = {l0:.6f}")
    print(f"Peak √λ₁ ≈ {m_peak:.6f}")

    # 2) Frenet + tripod sampling
    data = sample_frenet_tripod(
        M, L, Mass,
        apex_ij=apex_ij,
        step_size=0.15,
        n_steps=220,
        h_factor=0.5,
        smooth_window=7,
    )

    # 3) Plots
    plot_frenet_curvature(data, prefix="needle_frenet")
    plot_tripod_alignment(data, prefix="needle_frenet")
    plot_centerline_on_field(M, L, Mass, apex_ij, data,
                             prefix="needle_frenet")

    print("\nDone. Generated:")
    print("  - needle_frenet_curvature.png")
    print("  - needle_frenet_tripod_alignment.png")
    print("  - needle_frenet_centerline.png")


if __name__ == "__main__":
    main()
