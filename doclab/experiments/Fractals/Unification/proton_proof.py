"""
Higgs Drift Experiment (Pirouette / Proton Channel)

This script does three things:

1. Samples the twist error landscape E_{1:2:8}(tau) near the suspected
   proton channel and fits a quadratic around its minimum to estimate
   curvature (metastable plateau stiffness) and tau_p*.

2. Uses your linear twist->mass model to turn tau_p* into a proton
   mass prediction and compare to CODATA.

3. Runs a toy "Higgs drift" experiment where the minimum tau_p*(t)
   moves slowly in time and the actual tau(t) relaxes towards it
   with a viscous relaxation rate gamma_H. This mimics a cooling
   Higgs background dragging the proton plateau.

Drop this next to twist_unit.py and twist_scan_3.py and run:

    python higgs_drift_experiment.py
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
#  Imports from your twist unit
# ---------------------------------------------------------------------
from twist_unit import error_128   # returns (E, G, T, R)

# ---------------------------------------------------------------------
#  Shared constants & mass model (copied from twist_scan_3.py)
# ---------------------------------------------------------------------
M_E = 9.1093837015e-31            # electron mass (kg)
M_P_CODATA = 1.67262192369e-27    # proton mass (kg)
R_P_E_CODATA = M_P_CODATA / M_E

# Your calibrated electron twist
TAU_E = 5.06   # keep in sync with your current best value!

def mass_from_twist_linear(tau: float,
                           tau_e: float = TAU_E,
                           m_e: float = M_E) -> float:
    """
    Minimal hypothesis: m(tau) = m_e * (tau / tau_e).
    """
    return m_e * (tau / tau_e)

# ---------------------------------------------------------------------
#  1. Sample error landscape and fit curvature near proton plateau
# ---------------------------------------------------------------------
def sample_error(t_min: float,
                 t_max: float,
                 n_samples: int = 2000):
    """
    Sample E(τ) = error_128(τ) uniformly on [t_min, t_max].
    Returns (taus, errors).
    """
    taus = np.linspace(t_min, t_max, n_samples)
    errs = np.empty_like(taus)

    for i, t in enumerate(taus):
        # error_128 returns (E, G, T, R); we only want E
        errs[i] = float(error_128(float(t))[0])

    return taus, errs

def fit_quadratic_near_min(taus, errs, window_fraction=0.15):
    """
    Fit a quadratic E(τ) ≈ a (τ - τ0)^2 + E0 around the minimum
    to estimate curvature (kappa_eff ≈ 2a) and tau_p* = τ0.

    window_fraction selects a subset around the minimum to avoid
    contamination from far-off non-quadratic structure.
    """
    idx_min = int(np.argmin(errs))
    tau_min = taus[idx_min]

    # Define a local window around the minimum
    n = len(taus)
    half_window = int(window_fraction * n)
    i0 = max(0, idx_min - half_window)
    i1 = min(n, idx_min + half_window)

    tau_local = taus[i0:i1]
    E_local = errs[i0:i1]

    # Fit quadratic: E ≈ a τ^2 + b τ + c
    coeffs = np.polyfit(tau_local, E_local, deg=2)
    a, b, c = coeffs

    # Convert to vertex form: a (τ - τ0)^2 + E0
    tau0 = -b / (2*a)
    E0 = c - a * tau0**2 - b * tau0

    # Effective curvature of the well
    kappa_eff = 2.0 * a   # proportional to d^2E/dτ^2 at minimum

    return tau0, E0, kappa_eff, coeffs, tau_local, E_local

# ---------------------------------------------------------------------
#  2. Higgs drift toy model in twist space
# ---------------------------------------------------------------------
def simulate_higgs_drift(tau_p0,
                         drift_fraction=0.02,
                         n_steps=4000,
                         dt=1.0,
                         gamma_H=0.01):
    """
    Toy Higgs drift:

        dτ/dt = -γ_H [ τ - τ_p*(t) ]

    where τ_p*(t) is a linearly drifting minimum:

        τ_p*(t) = tau_p0 * (1 + drift_fraction * (t / t_final))

    So over the total duration T = n_steps * dt, the minimum moves
    by drift_fraction * tau_p0 (e.g. 2% shift).

    This is not claiming realism; it's a controlled lab where you can
    see whether τ(t) adiabatically follows the moving Higgs minimum.

    Returns:
        t_arr      : time axis
        tau_min    : τ_p*(t)
        tau_traj   : τ(t)
        m_p_traj   : proton mass trajectory via the linear model
        ratio_traj : m_p(t) / m_e
    """
    T_final = n_steps * dt
    t_arr = np.linspace(0.0, T_final, n_steps)

    # drifting equilibrium value tau_p*(t)
    tau_min = tau_p0 * (1.0 + drift_fraction * (t_arr / T_final))

    # Relaxing actual twist τ(t)
    tau_traj = np.empty_like(t_arr)
    tau_traj[0] = tau_p0   # start at initial equilibrium

    for i in range(1, n_steps):
        tau = tau_traj[i-1]
        tau_eq = tau_min[i-1]
        d_tau = -gamma_H * (tau - tau_eq) * dt
        tau_traj[i] = tau + d_tau

    # Mass and ratio trajectories
    m_p_traj = mass_from_twist_linear(tau_traj, tau_e=TAU_E, m_e=M_E)
    ratio_traj = m_p_traj / M_E

    return t_arr, tau_min, tau_traj, m_p_traj, ratio_traj

# ---------------------------------------------------------------------
#  3. Top-level runner
# ---------------------------------------------------------------------
def run_experiment():
    # ---- Step 1: sample error landscape near proton channel ----------
    tau_guess = 3.8
    window = 2.0
    n_samples = 2400

    print("[#] Sampling twist error landscape...")
    taus, errs = sample_error(tau_guess - window,
                              tau_guess + window,
                              n_samples=n_samples)

    # ---- Step 2: fit quadratic near the minimum ----------------------
    print("[#] Fitting quadratic near proton plateau...")
    tau0, E0, kappa_eff, coeffs, tau_local, E_local = fit_quadratic_near_min(
        taus, errs, window_fraction=0.15
    )

    a, b, c = coeffs
    print("\n[Δ] Quadratic fit E(τ) ≈ a τ^2 + b τ + c:")
    print(f"    a = {a:.6e}")
    print(f"    b = {b:.6e}")
    print(f"    c = {c:.6e}")
    print(f"\n    tau_p* (vertex) ≈ {tau0:.8f}")
    print(f"    E(tau_p*)       ≈ {E0:.6e}")
    print(f"    kappa_eff ≈ d^2E/dτ^2 ≈ {kappa_eff:.6e}")

    # Proton mass prediction from fitted tau_p*
    m_p_pred = mass_from_twist_linear(tau0, tau_e=TAU_E, m_e=M_E)
    ratio_pred = m_p_pred / M_E
    rel_err_ratio = (ratio_pred - R_P_E_CODATA) / R_P_E_CODATA

    print("\n[Mass model: m ∝ τ]")
    print(f"    Electron twist τ_e        = {TAU_E:.6f}")
    print(f"    Electron mass m_e        = {M_E:.6e} kg")
    print(f"    Proton mass (predicted)  = {m_p_pred:.6e} kg")
    print(f"    Proton mass (CODATA)     = {M_P_CODATA:.6e} kg")
    print(f"    Predicted ratio m_p/m_e  = {ratio_pred:.6f}")
    print(f"    CODATA   ratio m_p/m_e   = {R_P_E_CODATA:.6f}")
    print(f"    Relative error in ratio  = {rel_err_ratio*100:.3f} %")

    # ---- Plot 1: landscape + quadratic fit ---------------------------
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(taus, errs, label=r"$E_{1:2:8}(\tau)$", alpha=0.7)

    # Overlay local quadratic in local window
    tau_fit_fine = np.linspace(tau_local.min(), tau_local.max(), 400)
    E_fit_fine = a * tau_fit_fine**2 + b * tau_fit_fine**2*0 + c  # WRONG
    # Correct vertex form for clarity:
    E_fit_fine = a*(tau_fit_fine**2) + b*tau_fit_fine + c

    ax.plot(tau_fit_fine, E_fit_fine,
            'r--', label="Quadratic fit (local)")

    ax.axvline(tau0, color="tab:red", linestyle=":", label=r"Fitted $\tau_p^*$")
    ax.axvline(TAU_E, color="tab:green", linestyle="--", label=r"Electron $\tau_e$")

    ax.set_xlabel(r"Twist $\tau$")
    ax.set_ylabel(r"Error $E_{1:2:8}(\tau)$")
    ax.set_title("Twist Error Landscape near Proton Plateau")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("higgs_drift_quadratic_fit.png", dpi=200)
    print("\n[+] Saved plot: higgs_drift_quadratic_fit.png")

    # ---- Step 3: Higgs drift toy dynamics ----------------------------
    print("\n[#] Simulating Higgs drift in twist space...")
    # You can tweak these to explore adiabatic vs lagged behaviour:
    drift_fraction = 0.02   # 2% change in tau_p* over the run
    gamma_H = 0.02          # relaxation rate; larger = better tracking
    n_steps = 4000
    dt = 1.0

    t_arr, tau_min, tau_traj, m_p_traj, ratio_traj = simulate_higgs_drift(
        tau_p0=tau0,
        drift_fraction=drift_fraction,
        n_steps=n_steps,
        dt=dt,
        gamma_H=gamma_H
    )

    # ---- Plot 2: tau(t) vs drifting minimum --------------------------
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    ax2.plot(t_arr, tau_min, label=r"Drifting minimum $\tau_p^*(t)$", alpha=0.7)
    ax2.plot(t_arr, tau_traj, label=r"Relaxing $\tau(t)$", alpha=0.9)
    ax2.set_xlabel("Toy time (arbitrary units)")
    ax2.set_ylabel(r"Twist $\tau$")
    ax2.set_title("Higgs Drift Toy Model in Twist Space")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("higgs_drift_tau_trajectory.png", dpi=200)
    print("[+] Saved plot: higgs_drift_tau_trajectory.png")

    # ---- Plot 3: proton mass ratio evolution -------------------------
    fig3, ax3 = plt.subplots(figsize=(9, 5))
    ax3.plot(t_arr, ratio_traj, label=r"$m_p(t)/m_e$")
    ax3.axhline(R_P_E_CODATA, color="tab:red", linestyle="--",
                label="CODATA ratio")
    ax3.set_xlabel("Toy time (arbitrary units)")
    ax3.set_ylabel(r"Proton mass ratio $m_p/m_e$")
    ax3.set_title("Proton Mass Ratio under Higgs Drift (Toy Model)")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("higgs_drift_mass_ratio.png", dpi=200)
    print("[+] Saved plot: higgs_drift_mass_ratio.png")

    print("\nDone. Inspect the three PNGs for:")
    print("  - How flat the plateau is (metastability).")
    print("  - How well τ(t) tracks a moving minimum for given γ_H.")
    print("  - How stable m_p/m_e remains under small Higgs drift.")


if __name__ == "__main__":
    run_experiment()
