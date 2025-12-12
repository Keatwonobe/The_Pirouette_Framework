# twist_scan_3.py
"""
Brute-force scan of the twist landscape near a suspected 'proton' channel.
We don't rely on local-min flags; we just sample E(τ) densely and take
the smallest value in the window.

Requires:
    twist_unit.py  (must define error_128(τ))

Usage:
    python twist_scan_3.py
"""

import numpy as np
import matplotlib.pyplot as plt

# ---- Import your twist error function ------------------------------------
from twist_unit import error_128

# ---- Physical constants --------------------------------------------------
M_E = 9.1093837015e-31        # electron mass (kg)
M_P_CODATA = 1.67262192369e-27  # proton mass (kg)
R_P_E_CODATA = M_P_CODATA / M_E

# Your calibrated electron twist
TAU_E = 5.06   # adjust if you later settle on a different value


# -------------------------------------------------------------------------
#   Simple twist → mass model
# -------------------------------------------------------------------------
def mass_from_twist_linear(tau: float,
                           tau_e: float = TAU_E,
                           m_e: float = M_E) -> float:
    """
    Minimal hypothesis: inertial mass is proportional to twist:
        m(τ) = m_e * (τ / τ_e)

    Swap this out later if you adopt a different law.
    """
    return m_e * (tau / tau_e)


# -------------------------------------------------------------------------
#   Brute-force sampler
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
#   Brute-force sampler
# -------------------------------------------------------------------------
def sample_error(t_min: float,
                 t_max: float,
                 n_samples: int = 2000):
    """
    Sample E(τ) = error_128(τ) uniformly on [t_min, t_max].
    Returns (taus, errors).
    """
    taus = np.linspace(t_min, t_max, n_samples)
    errors = np.empty_like(taus)

    for i, t in enumerate(taus):
        # FIX: error_128 returns (E, G, T, R). We only want E (index 0).
        # We must access the tuple element before casting to float.
        errors[i] = float(error_128(float(t))[0]) 

    return taus, errors


def find_min_bruteforce(tau_guess: float,
                        window: float,
                        n_samples: int = 2000):
    """
    Look in [tau_guess - window, tau_guess + window] and pick
    the τ with the smallest E(τ). No curvature tests.
    """
    t_min = tau_guess - window
    t_max = tau_guess + window

    taus, errs = sample_error(t_min, t_max, n_samples=n_samples)
    idx = int(np.argmin(errs))
    tau_star = float(taus[idx])
    E_star = float(errs[idx])

    # A quick diagnostic: how flat is the plateau?
    Emin = float(np.min(errs))
    Emax = float(np.max(errs))

    return taus, errs, tau_star, E_star, Emin, Emax


# -------------------------------------------------------------------------
#   Top-level runner
# -------------------------------------------------------------------------
def run_proton_twist_scan():
    tau_guess = 3.8     # suspected proton channel from kinetic/helicity views
    window = 2.0        # look in [1.8, 5.8]
    n_samples = 2400    # fairly dense

    print("[#] Proton twist scan (brute-force)")
    print(f"    Guess τ_p ≈ {tau_guess:.4f}, window ±{window:.2f}, samples={n_samples}")

    taus, errs, tau_p, E_p, Emin, Emax = find_min_bruteforce(
        tau_guess=tau_guess,
        window=window,
        n_samples=n_samples,
    )

    print("\n[Δ] Error statistics in window:")
    print(f"    E_min   = {Emin:.6e}")
    print(f"    E_max   = {Emax:.6e}")
    print(f"    ΔE_span = {Emax - Emin:.6e}")

    print("\n[Δ] Brute-force minimum nearest the proton channel:")
    print(f"    τ_p*    = {tau_p:.8f}")
    print(f"    E(τ_p*) = {E_p:.6e}")

    # Map that τ to a proton mass via the simple clock model
    m_p_pred = mass_from_twist_linear(tau_p, tau_e=TAU_E, m_e=M_E)
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

    # Also report “how plateau-ish” that region is as a warning
    if (Emax - Emin) / max(Emin, 1e-12) < 1e-3:
        print("\n[!] Warning: E(τ) is almost flat in this window.")
        print("    This suggests the 1:2:8 error is not strongly selecting")
        print("    the proton channel; treat this mass estimate as very weak.")

    # Plot the landscape
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(taus, errs, label=r"$E_{1:2:8}(\tau)$")
    ax.axvline(TAU_E, color="tab:green", linestyle="--", label=r"Electron $\tau_e$")
    ax.axvline(tau_p, color="tab:red", linestyle=":", label=r"Proton candidate $\tau_p^*$")

    ax.set_xlabel(r"Twist $\tau$")
    ax.set_ylabel(r"Error $E_{1:2:8}(\tau)$")
    ax.set_title("Twist Error Landscape near Proton Candidate (brute-force)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("proton_twist_scan_bruteforce.png", dpi=200)
    print("\n[+] Saved plot: proton_twist_scan_bruteforce.png")


if __name__ == "__main__":
    run_proton_twist_scan()
