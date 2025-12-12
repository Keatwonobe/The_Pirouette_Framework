import numpy as np
import matplotlib.pyplot as plt

"""
needle_tripod_mixture.py

Goal:
  - For each point along the needle centreline, find the dominant
    curvature eigenvector v_dom in the (m, λ) plane.
  - Project v_dom onto a user-defined SU(3)-like tripod {T, R, G}.
  - Compute "color mixture" weights w_T, w_R, w_G (squared projections).
  - Analyse oscillations of the mixture (especially R vs G) to estimate
    a dominant beat frequency along the needle.

Lives next to:
  - unification_24.py
  - mass_hierarchy_apex_2.py  (or mass_hierarchy_apex.py)
"""

# ---------------------------------------------------------------------
# Tripod definition (angles in the m–λ plane)
# ---------------------------------------------------------------------
# Replace these with the angles you want, in radians, measured like atan2(λ, m).
# These can be the principal directions you extracted from JT, JR, JG.
tripod_angles = {
    "T": 0.0,                 #   0°   placeholder
    "R": 2.0 * np.pi / 3.0,   # 120°   placeholder
    "G": 4.0 * np.pi / 3.0,   # 240°   placeholder
}


# ---------------------------------------------------------------------
# Imports from your apex / needle machinery
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
# Hessian at a point
# ---------------------------------------------------------------------
def hessian_at_point(m0, l0, h_m, h_l):
    """2×2 Hessian of f = √λ₁(m, λ) at (m0, l0) via finite differences."""
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
# Helper: angle wrap
# ---------------------------------------------------------------------
def wrap_angle(a):
    return np.arctan2(np.sin(a), np.cos(a))


# ---------------------------------------------------------------------
# Main mixture analysis
# ---------------------------------------------------------------------
def analyse_tripod_mixture(step_size=0.15,
                           n_steps=220,
                           h_factor=0.5,
                           smooth_window=5):
    """
    1) Trace needle centreline.
    2) At each point:
         - compute Hessian
         - find dominant eigenvector v_dom
         - project onto tripod legs (unit vectors u_T, u_R, u_G)
         - compute weights w_k = (v_dom·u_k)^2
    3) Smooth weights along s.
    4) Estimate oscillation frequency of (w_R - w_G)(s).
    """
    # 1) Apex + field
    m0, l0, m_peak, M, L, Mass, apex_ij = find_apex()
    print("=== Needle Tripod Mixture Decoder ===")
    print(f"Apex at m0 = {m0:.6f}, λ0 = {l0:.6f}")
    print(f"Peak √λ₁ ≈ {m_peak:.6f}")

    # 2) Centreline
    cm, cl, cf = trace_centerline(
        M, L, Mass,
        start_ij=apex_ij,
        step_size=step_size,
        n_steps=n_steps,
        mode="downhill",
    )

    n = len(cm)
    if n < 5:
        raise RuntimeError("Centreline too short for mixture analysis.")

    # arc-length parameter
    ds = np.sqrt(np.diff(cm) ** 2 + np.diff(cl) ** 2)
    s = np.concatenate([[0.0], np.cumsum(ds)])
    mean_ds = float(np.mean(ds))

    # tripod unit vectors in (m, λ)
    tripod_vecs = {
        name: np.array([np.cos(phi), np.sin(phi)], dtype=float)
        for name, phi in tripod_angles.items()
    }

    # finite-difference step sizes for Hessian
    dm_grid = float(M[0, 1] - M[0, 0])
    dl_grid = float(L[1, 0] - L[0, 0])
    h_m = dm_grid * h_factor
    h_l = dl_grid * h_factor

    # storage
    theta_dom = np.zeros(n)
    weights = {name: np.zeros(n) for name in tripod_angles.keys()}

    for i in range(n):
        m = cm[i]
        l = cl[i]
        H, eigvals, eigvecs = hessian_at_point(m, l, h_m, h_l)

        # dominant eigenvector = largest |κ|
        idx_dom = 0 if abs(eigvals[0]) > abs(eigvals[1]) else 1
        v_dom = eigvecs[:, idx_dom]  # already unit

        theta_dom[i] = np.arctan2(v_dom[1], v_dom[0])

        # projections onto tripod legs
        for name, u in tripod_vecs.items():
            c = float(np.dot(v_dom, u))
            weights[name][i] = c * c  # squared projection amplitude

        # normalise so sum w_k = 1 to interpret as fractions
        total = sum(weights[name][i] for name in tripod_angles.keys())
        if total > 1e-14:
            for name in tripod_angles.keys():
                weights[name][i] /= total

    # simple moving-average smoothing (interior)
    if smooth_window > 1:
        kern = np.ones(smooth_window, dtype=float) / smooth_window
        for name in tripod_angles.keys():
            weights[name] = np.convolve(weights[name], kern, mode="same")

    return {
        "s": s,
        "cm": cm,
        "cl": cl,
        "theta_dom": theta_dom,
        "weights": weights,
        "mean_ds": mean_ds,
    }


# ---------------------------------------------------------------------
# Plot + frequency analysis
# ---------------------------------------------------------------------
def plot_weights(data, prefix="needle_tripod"):
    s = data["s"]
    weights = data["weights"]

    plt.figure(figsize=(9, 5))
    for name, w in weights.items():
        plt.plot(s, w, label=f"w_{name}")
    plt.xlabel("Arc length s along needle (m–λ)")
    plt.ylabel("Mixture weight")
    plt.ylim(-0.05, 1.05)
    plt.title("Tripod Mixture Weights Along Needle")
    plt.legend()
    plt.tight_layout()
    fname = f"{prefix}_weights.png"
    plt.savefig(fname, dpi=170)
    print(f"[saved] {fname}")


def analyse_beating(data):
    """
    Look at w_R - w_G as a beating signal, estimate dominant
    spatial frequency along s.
    """
    s = data["s"]
    w = data["weights"]
    mean_ds = data["mean_ds"]

    if not (("R" in w) and ("G" in w)):
        print("\n[info] Need both 'R' and 'G' legs to analyse beating.")
        return

    # interior slice to avoid apex singular behaviour
    interior = slice(3, max(3, len(s) - 3))
    s_int = s[interior]
    signal = w["R"][interior] - w["G"][interior]

    # remove mean, apply window
    sig = signal - np.mean(signal)
    if len(sig) < 16:
        print("\n[info] Not enough samples for FFT beating analysis.")
        return

    window = np.hanning(len(sig))
    sig_win = sig * window

    # FFT
    fft_vals = np.fft.rfft(sig_win)
    freqs = np.fft.rfftfreq(len(sig_win), d=mean_ds)

    # ignore zero-frequency component
    amps = np.abs(fft_vals)
    amps[0] = 0.0

    idx_max = int(np.argmax(amps))
    f_dom = float(freqs[idx_max])
    if f_dom <= 0:
        print("\n[info] No non-zero dominant frequency found.")
        return
    period = 1.0 / f_dom

    print("\n=== Beating Analysis (R vs G) ===")
    print(f"Dominant spatial frequency ≈ {f_dom:.4f} cycles per unit s")
    print(f"Corresponding beating period ≈ {period:.3f} in arc-length units")
    print("Interpretation: over one period, the traveler 'breathes' its "
          "color mixture between R and G.")


def print_mixture_summary(data):
    s = data["s"]
    w = data["weights"]

    interior = slice(3, max(3, len(s) - 3))

    print("\n=== Mean Mixture Fractions (interior of needle) ===")
    for name, arr in w.items():
        mean_val = float(np.mean(arr[interior]))
        std_val = float(np.std(arr[interior]))
        print(f"  {name}: ⟨w_{name}⟩ ≈ {mean_val:.3f} ± {std_val:.3f}")


# ---------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------
def main():
    data = analyse_tripod_mixture(
        step_size=0.15,
        n_steps=220,
        h_factor=0.5,
        smooth_window=5,
    )

    plot_weights(data, prefix="needle_tripod")
    print_mixture_summary(data)
    analyse_beating(data)

    print("\nDone. Generated:")
    print("  - needle_tripod_weights.png")


if __name__ == "__main__":
    main()
