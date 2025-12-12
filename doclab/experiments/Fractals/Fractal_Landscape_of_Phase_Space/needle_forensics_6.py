import numpy as np
import matplotlib.pyplot as plt

"""
needle_su3_suite.py

A combined analysis suite for the 'traveler' needle:

1) Reconstruct SU(3)-like color state along the needle:
     - dominant curvature eigenvector v_dom(m, λ)
     - projections c_k = v_dom · u_k onto tripod legs T, R, G
     - weights w_k = |c_k|^2, normalized sum w_k = 1
     - mean state vector |ψ> over interior of needle

2) Correlate mixture weights w_k with Frenet-frame curvatures κ_t, κ_n.

3) Extract beating frequencies between pairs of legs
   using FFT of (w_R - w_T)(s) and (w_R - w_G)(s).

4) Compare user-specified tripod directions to eigenvectors
   of actual JT, JR, JG generators.

5) Provide a scaffold to repeat the analysis for multiple
   effective needles (e.g. starting deeper along the wake).

This script assumes these are available in your path:

    - mass_hierarchy_apex_2.py (or mass_hierarchy_apex.py)
        with local_mass, find_apex, trace_centerline
    - tripod_generators.py (you create this) with JT, JR, JG
        defined as 2×2 NumPy arrays in the (m, λ) basis.
"""


# =========================
# Tripod configuration
# =========================

# Angles of the tripod legs in the (m, λ) plane, in radians.
# Replace these with your actual angles extracted from the
# JT, JR, JG work (via eigenvectors).
# Convention: angle φ = atan2(λ, m).
tripod_angles = {
    "T": 0.0,                 # placeholder; fill with your value
    "R": 2.0 * np.pi / 3.0,   # placeholder
    "G": 4.0 * np.pi / 3.0,   # placeholder
}


# =========================
# Imports from your stack
# =========================
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

# Optional: generator matrices, if you define them
try:
    from tripod_generators import JT, JR, JG  # you create this file
    HAVE_GENERATORS = True
except ImportError:  # pragma: no cover
    HAVE_GENERATORS = False


# =========================
# Differential geometry
# =========================

def hessian_at_point(m0, l0, h_m, h_l):
    """2×2 Hessian of f = √λ1(m, λ) at (m0, l0) via finite differences."""
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


def compute_frenet(M, L, cm, cl):
    """
    Build Frenet-like tangent / normal vectors and arc-length.
    """
    n = len(cm)
    ds = np.sqrt(np.diff(cm)**2 + np.diff(cl)**2)
    s = np.concatenate([[0.0], np.cumsum(ds)])
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

    t_vecs[0] = t_vecs[1]
    t_vecs[-1] = t_vecs[-2]

    n_vecs = np.zeros_like(t_vecs)
    n_vecs[:, 0] = -t_vecs[:, 1]
    n_vecs[:, 1] =  t_vecs[:, 0]

    return s, t_vecs, n_vecs, float(np.mean(ds))


def smooth(arr, window=5):
    if window <= 1:
        return arr
    kernel = np.ones(window) / window
    return np.convolve(arr, kernel, mode="same")


# =========================
# SU(3) / tripod analysis
# =========================

def analyse_single_needle(step_size=0.15,
                          n_steps=220,
                          h_factor=0.5,
                          smooth_window=5):
    """
    Full analysis on one needle starting at the apex:

      - centreline
      - Frenet frame, curvatures κ_t, κ_n
      - dominant curvature eigenvector direction θ_dom
      - tripod projections c_k, weights w_k
      - SU(3) state |ψ(s)>
    """
    m0, l0, m_peak, M, L, Mass, apex_ij = find_apex()
    print("=== SU(3) Needle Analysis ===")
    print(f"Apex at m0 = {m0:.6f}, λ0 = {l0:.6f}")
    print(f"Peak √λ1 ≈ {m_peak:.6f}")

    # 1) trace centreline
    cm, cl, cf = trace_centerline(
        M, L, Mass,
        start_ij=apex_ij,
        step_size=step_size,
        n_steps=n_steps,
        mode="downhill",
    )
    n = len(cm)
    if n < 5:
        raise RuntimeError("Centreline too short for analysis.")

    # 2) Frenet frame
    s, t_vecs, n_vecs, mean_ds = compute_frenet(M, L, cm, cl)

    # 3) Hessians and principal directions
    dm_grid = float(M[0, 1] - M[0, 0])
    dl_grid = float(L[1, 0] - L[0, 0])
    h_m = dm_grid * h_factor
    h_l = dl_grid * h_factor

    k_t = np.zeros(n)
    k_n = np.zeros(n)
    theta_dom = np.zeros(n)

    # tripod unit vectors
    tripod_vecs = {
        name: np.array([np.cos(phi), np.sin(phi)], dtype=float)
        for name, phi in tripod_angles.items()
    }

    # signed coefficients and weights
    coeffs = {name: np.zeros(n) for name in tripod_angles.keys()}
    weights = {name: np.zeros(n) for name in tripod_angles.keys()}

    for i in range(n):
        m = cm[i]
        lam = cl[i]
        H, eigvals, eigvecs = hessian_at_point(m, lam, h_m, h_l)

        # Frenet curvatures
        t = t_vecs[i]
        nv = n_vecs[i]
        k_t[i] = float(t @ (H @ t))
        k_n[i] = float(nv @ (H @ nv))

        # dominant eigenvector of curvature
        idx_dom = 0 if abs(eigvals[0]) > abs(eigvals[1]) else 1
        v_dom = eigvecs[:, idx_dom]   # already normalised
        theta_dom[i] = np.arctan2(v_dom[1], v_dom[0])

        # projections onto tripod
        for name, u in tripod_vecs.items():
            c = float(np.dot(v_dom, u))   # signed
            coeffs[name][i] = c
            weights[name][i] = c * c

        # normalise weights
        total = sum(weights[name][i] for name in tripod_angles.keys())
        if total > 1e-14:
            for name in tripod_angles.keys():
                weights[name][i] /= total

    # 4) smoothing
    k_t_s = smooth(k_t, smooth_window)
    k_n_s = smooth(k_n, smooth_window)
    for name in tripod_angles.keys():
        weights[name] = smooth(weights[name], smooth_window)

    # interior slice (ignore apex and tail noise)
    interior = slice(3, max(3, n - 3))

    # 5) mean mixture and state vector
    mean_w = {name: float(np.mean(weights[name][interior]))
              for name in tripod_angles.keys()}
    # amplitude vector (real, positive)
    amps = np.array([np.sqrt(mean_w[name]) for name in ["T", "R", "G"]])
    amps /= np.linalg.norm(amps)
    print("\n=== Mean mixture fractions (interior) ===")
    for name in ["T", "R", "G"]:
        w = mean_w[name]
        print(f"  {name}: <w_{name}> ≈ {w:.3f}")
    print("\nApproximate SU(3) state vector |ψ> in {T,R,G} basis:")
    print(f"  |ψ> ≈ ({amps[0]:.3f}, {amps[1]:.3f}, {amps[2]:.3f})")

    # 6) correlations with curvature
    print("\n=== Correlations: weights vs Frenet curvatures ===")
    for name in ["T", "R", "G"]:
        w = weights[name][interior]
        corr_t = np.corrcoef(w, k_t_s[interior])[0, 1]
        corr_n = np.corrcoef(w, k_n_s[interior])[0, 1]
        print(f"  w_{name} vs κ_t: {corr_t: .3f},  w_{name} vs κ_n: {corr_n: .3f}")

    # 7) beating frequencies: w_R - w_T and w_R - w_G
    def beating(signal, label):
        sig = signal[interior] - np.mean(signal[interior])
        if len(sig) < 16:
            print(f"\n[info] Not enough samples for FFT of {label}.")
            return
        win = np.hanning(len(sig))
        sig_win = sig * win
        fft_vals = np.fft.rfft(sig_win)
        freqs = np.fft.rfftfreq(len(sig_win), d=mean_ds)
        amps_fft = np.abs(fft_vals)
        amps_fft[0] = 0.0
        idx_max = int(np.argmax(amps_fft))
        f_dom = float(freqs[idx_max])
        if f_dom <= 0:
            print(f"\n[info] No non-zero dominant frequency found for {label}.")
            return
        period = 1.0 / f_dom
        print(f"  {label}: f ≈ {f_dom:.4f} cycles / unit s, period ≈ {period:.3f}")

    print("\n=== Beating analysis ===")
    beating(weights["R"] - weights["T"], "R - T")
    beating(weights["R"] - weights["G"], "R - G")

    # 8) basic plots
    plt.figure(figsize=(9, 5))
    for name in ["T", "R", "G"]:
        plt.plot(s, weights[name], label=f"w_{name}")
    plt.xlabel("Arc length s along needle")
    plt.ylabel("Mixture weight w_k")
    plt.ylim(-0.05, 1.05)
    plt.title("Tripod mixture weights along needle")
    plt.legend()
    plt.tight_layout()
    plt.savefig("su3_weights_along_needle.png", dpi=170)
    print("\n[saved] su3_weights_along_needle.png")

    plt.figure(figsize=(9, 5))
    plt.plot(s, k_t_s, label=r"κ_t (along axis)")
    plt.plot(s, k_n_s, label=r"κ_n (normal)")
    plt.axhline(0.0, linestyle="--", linewidth=0.8)
    plt.xlabel("Arc length s")
    plt.ylabel("Curvature")
    plt.title("Frenet-frame curvatures along needle")
    plt.legend()
    plt.tight_layout()
    plt.savefig("su3_frenet_curvature.png", dpi=170)
    print("[saved] su3_frenet_curvature.png")

    return {
        "s": s,
        "cm": cm,
        "cl": cl,
        "k_t": k_t_s,
        "k_n": k_n_s,
        "coeffs": coeffs,
        "weights": weights,
        "amps": amps,
        "mean_ds": mean_ds,
    }


# =========================
# 4. Compare to JT, JR, JG
# =========================

def compare_tripod_to_generators():
    if not HAVE_GENERATORS:
        print("\n[info] tripod_generators.py not found; "
              "skipping JT/JR/JG comparison.")
        return

    gens = {"T": JT, "R": JR, "G": JG}
    print("\n=== Tripod vs generator eigenvectors ===")
    for name, G in gens.items():
        eigvals, eigvecs = np.linalg.eigh(G)
        # choose eigenvector with largest |eig|
        idx = int(np.argmax(np.abs(eigvals)))
        v = eigvecs[:, idx]
        angle = np.arctan2(v[1], v[0])
        # wrap difference to [-π, π]
        d = angle - tripod_angles[name]
        d = np.arctan2(np.sin(d), np.cos(d))
        print(f"  {name}: generator eigen-direction angle ≈ {angle:.3f} rad,"
              f"   tripod angle = {tripod_angles[name]:.3f},"
              f"   Δ = {d:.3f} rad")


# =========================
# 5. Multiple needles scaffold
# =========================

def analyse_multiple_needles(offset_indices=(0, 10, 20)):
    """
    VERY SIMPLE scaffold:

    Use the already computed centreline from apex and treat
    different *starting indices* along it as "effective needles"
    at different apex depths (i.e. same trajectory, different
    entrance point). For each starting index, recompute mixture
    statistics on the tail segment.

    This is not the same as finding separate apexes, but it lets
    you see how mixture and curvature behave when you only look
    at deeper segments of the wake.

    For proper 'different needles', you would:
      - locate additional local maxima of √λ1(m, λ),
      - rerun analyse_single_needle() with start_ij at those.
    """
    # run a base analysis to get the raw data
    base = analyse_single_needle()
    s = base["s"]
    weights = base["weights"]

    print("\n=== Multiple-segment analysis (scaffold) ===")
    for idx0 in offset_indices:
        if idx0 >= len(s) - 5:
            continue
        interior = slice(idx0, len(s) - 3)
        segment = (s[interior] - s[idx0])

        print(f"\nSegment starting at index {idx0}, length ~{segment[-1]:.3f}:")
        for name in ["T", "R", "G"]:
            mean_w = float(np.mean(weights[name][interior]))
            print(f"  {name}: <w_{name}> ≈ {mean_w:.3f}")


# =========================
# main
# =========================

def main():
    data = analyse_single_needle()
    compare_tripod_to_generators()
    # If you want the multi-segment scaffold, uncomment this:
    # analyse_multiple_needles(offset_indices=(0, 8, 16, 24))

if __name__ == "__main__":
    main()
