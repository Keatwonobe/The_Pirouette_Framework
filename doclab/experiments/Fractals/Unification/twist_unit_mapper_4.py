# twist_fractal_scanner.py

import numpy as np
import matplotlib.pyplot as plt

from twist_unit import error_128


def sample_error(t_min, t_max, n_samples, **err_kwargs):
    """
    Coarse sampler for E(tau) over [t_min, t_max].

    Returns
    -------
    tau : (N,) array
    E   : (N,) array
    w   : (N,3) array of sector weights (G,T,R)
    """
    tau = np.linspace(t_min, t_max, n_samples)
    E_vals = np.zeros_like(tau)
    weights = np.zeros((n_samples, 3))

    for i, t in enumerate(tau):
        E, wG, wT, wR = error_128(t, **err_kwargs)
        E_vals[i] = E
        weights[i] = (wG, wT, wR)

    return tau, E_vals, weights


def detect_candidate_intervals(tau, E, k_top=10, min_sep=3):
    """
    Use discrete derivatives to find "interesting" regions:
      • local minima of E (sign change in first derivative, positive curvature)
      • large curvature spikes |Δ²E|.

    Returns a list of (t_left, t_right, reason) intervals.
    """
    dE = np.diff(E)
    dE = np.concatenate(([dE[0]], dE))        # pad

    d2E = np.diff(E, n=2)
    d2E = np.concatenate(([d2E[0]], [d2E[0]], d2E))

    candidates = []

    # (1) local minima by slope sign change
    for i in range(1, len(tau) - 1):
        if dE[i - 1] < 0.0 and dE[i + 1] > 0.0:
            t_left = tau[max(0, i - 2)]
            t_right = tau[min(len(tau) - 1, i + 2)]
            candidates.append((t_left, t_right, "min"))

    # (2) curvature spikes
    idx_sorted = np.argsort(-np.abs(d2E))  # descending |d2E|
    picked = 0
    used = np.zeros(len(tau), dtype=bool)

    for idx in idx_sorted:
        if picked >= k_top:
            break
        if used[max(0, idx - min_sep):min(len(tau), idx + min_sep + 1)].any():
            continue
        t_left = tau[max(0, idx - 2)]
        t_right = tau[min(len(tau) - 1, idx + 2)]
        candidates.append((t_left, t_right, "curvature"))
        used[max(0, idx - min_sep):min(len(tau), idx + min_sep + 1)] = True
        picked += 1

    # merge overlapping intervals
    candidates.sort(key=lambda c: c[0])
    merged = []
    for tL, tR, reason in candidates:
        if not merged:
            merged.append([tL, tR, {reason}])
            continue
        mL, mR, reasons = merged[-1]
        if tL <= mR:
            merged[-1][1] = max(mR, tR)
            reasons.add(reason)
        else:
            merged.append([tL, tR, {reason}])

    return [(mL, mR, ",".join(sorted(reasons))) for mL, mR, reasons in merged]


def downhill_refine_interval(
    t_left,
    t_right,
    n_init=21,
    max_iter=200,
    tol=1e-6,
    **err_kwargs,
):
    """
    "Only go downhill" 1-D search inside [t_left, t_right].

    Strategy:
      1. Fine grid in the interval → pick lowest point as start.
      2. Adaptive step hill-climb:
           - propose tau_new = tau +/- step
           - if E_new < E: move there & slightly increase step
           - else: reverse direction & shrink step
      3. Stop when step < tol or max_iter reached.
    """
    tau_grid = np.linspace(t_left, t_right, n_init)
    E_grid = []
    for t in tau_grid:
        E, *_ = error_128(t, **err_kwargs)
        E_grid.append(E)
    E_grid = np.array(E_grid)

    idx_min = int(np.argmin(E_grid))
    tau_best = float(tau_grid[idx_min])
    E_best = float(E_grid[idx_min])

    step = (t_right - t_left) / 8.0
    direction = -1.0  # start by going left
    history_tau = [tau_best]
    history_E = [E_best]

    for _ in range(max_iter):
        candidate = tau_best + direction * step
        if not (t_left <= candidate <= t_right):
            # bounce off boundary
            direction *= -1.0
            step *= 0.5
            if step < tol:
                break
            continue

        E_candidate, *_ = error_128(candidate, **err_kwargs)

        if E_candidate < E_best:
            # downhill: move & slightly grow step
            tau_best, E_best = candidate, E_candidate
            step *= 1.1
        else:
            # uphill: flip direction & shrink step
            direction *= -1.0
            step *= 0.5

        history_tau.append(tau_best)
        history_E.append(E_best)

        if step < tol:
            break

    return tau_best, E_best, np.array(history_tau), np.array(history_E)


def fractal_resonance_scan(
    t_min=0.0,
    t_max=50.0,
    n_coarse=400,
    k_top_curvature=15,
    refine_half_width=0.5,
    **err_kwargs,
):
    """
    Full "substrate" scanner:
      1) Coarse mesh over [t_min, t_max] → E(τ).
      2) Derivative + curvature → interesting bands.
      3) In each band, run downhill-only refinement.
      4) Sort all refined minima by E and report.
    """
    tau, E, weights = sample_error(t_min, t_max, n_coarse, **err_kwargs)
    intervals = detect_candidate_intervals(tau, E, k_top=k_top_curvature)

    refined = []
    for (a, b, reason) in intervals:
        center = 0.5 * (a + b)
        left = max(t_min, center - refine_half_width)
        right = min(t_max, center + refine_half_width)
        if right <= left:
            continue

        tau_min, E_min, hist_tau, hist_E = downhill_refine_interval(
            left, right, **err_kwargs
        )
        refined.append(
            {
                "interval": (left, right),
                "reason": reason,
                "tau_min": tau_min,
                "E_min": E_min,
                "history_tau": hist_tau,
                "history_E": hist_E,
            }
        )

    refined.sort(key=lambda r: r["E_min"])

    return {
        "tau": tau,
        "E": E,
        "weights": weights,
        "intervals": intervals,
        "refined": refined,
    }


def plot_scan_results(result, target=(1/11, 2/11, 8/11), out_prefix="twist_fractal_scan"):
    tau = result["tau"]
    E = result["E"]
    w = result["weights"]
    refined = result["refined"]

    # (1) Error landscape
    plt.figure(figsize=(10, 4))
    plt.plot(tau, E, lw=1.5)
    if refined:
        mins_tau = [r["tau_min"] for r in refined]
        mins_E = [r["E_min"] for r in refined]
        plt.scatter(mins_tau, mins_E, c="r", zorder=5, label="Refined minima")
        plt.legend()
    plt.xlabel("Twist τ")
    plt.ylabel("E(τ)")
    plt.title("Twist Error Landscape with Refined Minima")
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_error_landscape.png", dpi=160)

    # (2) Sector weights vs τ
    wG, wT, wR = w.T
    plt.figure(figsize=(10, 4))
    plt.plot(tau, wG, label="(Gold)")
    plt.plot(tau, wT, label="(Teal)")
    plt.plot(tau, wR, label="(Red)")
    g, t, r = target
    plt.axhline(g, ls="--", lw=1, color="gray", alpha=0.6)
    plt.axhline(t, ls="--", lw=1, color="gray", alpha=0.6)
    plt.axhline(r, ls="--", lw=1, color="gray", alpha=0.6)
    plt.xlabel("Twist τ")
    plt.ylabel("Time-averaged sector weights")
    plt.title("Sector Weights vs τ (with 1:2:8 target)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_weights.png", dpi=160)

    # (3) Downhill history for best minimum
    if refined:
        best = refined[0]
        plt.figure(figsize=(6, 4))
        plt.plot(best["history_tau"], best["history_E"], "o-", ms=3)
        plt.xlabel("τ (walk)")
        plt.ylabel("E(τ)")
        plt.title(f"Downhill Walk towards τ*={best['tau_min']:.6f}")
        plt.tight_layout()
        plt.savefig(f"{out_prefix}_best_walk.png", dpi=160)


def main():
    print("[#] Fractal twist resonance scanner")

    result = fractal_resonance_scan(
        t_min=0.0,
        t_max=50.0,
        n_coarse=500,
    )

    print("\n[Δ] Top refined minima (sorted by error):")
    for i, r in enumerate(result["refined"][:10], start=1):
        tL, tR = r["interval"]
        print(
            f"  #{i:2d}: τ*={r['tau_min']:.6f}  E*={r['E_min']:.6e}  "
            f"interval=[{tL:.3f},{tR:.3f}]  reason={r['reason']}"
        )

    plot_scan_results(result)
    print("\nSaved plots with prefix 'twist_fractal_scan_*.png'.")


if __name__ == "__main__":
    main()
