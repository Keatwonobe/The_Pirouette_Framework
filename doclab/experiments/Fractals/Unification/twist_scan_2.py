# proton_twist_scan.py
"""
Scan the twist landscape near a suspected 'proton' channel and
estimate the corresponding mass by assuming m ∝ τ with electron
as the calibration point.

Requires:
    twist_unit.py   (must define scan_twist_range and/or error_128)

Usage:
    python proton_twist_scan.py
"""

import numpy as np
import matplotlib.pyplot as plt

# ---- Import your twist utilities -----------------------------------------
from twist_unit import scan_twist_range, error_128

# ---- Physical constants (CODATA-style numbers) ---------------------------
# Electron rest mass (kg)
M_E = 9.1093837015e-31
# Proton rest mass (kg)
M_P_CODATA = 1.67262192369e-27
# Proton / electron mass ratio (for reference)
R_P_E_CODATA = M_P_CODATA / M_E

# Your calibrated electron twist (from earlier runs)
TAU_E = 5.06   # adjust if you settle on a different electron twist


# -------------------------------------------------------------------------
#  Mass model
# -------------------------------------------------------------------------
def mass_from_twist_linear(tau: float,
                           tau_e: float = TAU_E,
                           m_e: float = M_E) -> float:
    """
    Simplest hypothesis: inertial mass is proportional to twist.
        m(τ) = m_e * (τ / τ_e)

    This is intentionally minimal: it's the direct 'twist-as-clock'
    interpretation. If you later promote a different mapping
    (e.g. exponential, rational, etc.), you can swap it in here.
    """
    return m_e * (tau / tau_e)


# -------------------------------------------------------------------------
#  Proton twist search
# -------------------------------------------------------------------------
def find_local_min_near(
    tau_guess: float = 3.8,
    window: float = 2.0,
    n_samples: int = 800,
    scan_kwargs=None,
):
    """
    Scan E(τ) in a window [tau_guess - window, tau_guess + window] and
    return the local minimum of E(τ) that lies closest to tau_guess.

    scan_kwargs are passed through to twist_unit.scan_twist_range.
    """
    if scan_kwargs is None:
        scan_kwargs = {}

    t_min = tau_guess - window
    t_max = tau_guess + window

    tau_arr, V_arr, E_arr, is_min, is_max, is_infl = scan_twist_range(
        t_min, t_max, n_samples, **scan_kwargs
    )

    tau_arr = np.asarray(tau_arr)
    E_arr = np.asarray(E_arr)
    is_min = np.asarray(is_min, dtype=bool)

    # indices of local minima
    min_indices = np.where(is_min)[0]
    if len(min_indices) == 0:
        raise RuntimeError("No local minima found in the given τ-window.")

    # choose the minimum closest to the guess
    candidate_taus = tau_arr[min_indices]
    closest_idx = min_indices[np.argmin(np.abs(candidate_taus - tau_guess))]

    tau_star = tau_arr[closest_idx]
    E_star = E_arr[closest_idx]

    return tau_arr, E_arr, tau_star, E_star


# -------------------------------------------------------------------------
#  Top-level runner
# -------------------------------------------------------------------------
def run_proton_twist_scan():
    # 1. Choose where to look
    tau_guess = 3.8     # suspected 'proton channel' from caustic
    window = 2.0        # search ±2 around guess
    n_samples = 1200    # resolution of the scan

    print("[#] Proton twist scan")
    print(f"    Guess τ_p ≈ {tau_guess:.4f}, window ±{window:.2f}, samples={n_samples}")

    # 2. Scan the twist error landscape and find a local minimum
    tau_arr, E_arr, tau_p, E_p = find_local_min_near(
        tau_guess=tau_guess,
        window=window,
        n_samples=n_samples,
    )

    print("\n[Δ] Nearest local minimum to guess:")
    print(f"    τ_p* = {tau_p:.8f}")
    print(f"    E(τ_p*) = {E_p:.6e}")

    # 3. Use the linear twist–mass model to predict proton mass
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

    # 4. Plot E(τ) with markers for τ_e and τ_p*
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(tau_arr, E_arr, label=r"$E_{1:2:8}(\tau)$")
    ax.axvline(TAU_E, color="tab:green", linestyle="--", label=r"Electron $\tau_e$")
    ax.axvline(tau_p, color="tab:red", linestyle=":", label=r"Proton candidate $\tau_p^*$")

    ax.set_xlabel(r"Twist $\tau$")
    ax.set_ylabel(r"Error $E_{1:2:8}(\tau)$")
    ax.set_title("Twist Error Landscape near Proton Candidate")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("proton_twist_scan.png", dpi=200)
    print("\n[+] Saved plot: proton_twist_scan.png")


if __name__ == "__main__":
    run_proton_twist_scan()
