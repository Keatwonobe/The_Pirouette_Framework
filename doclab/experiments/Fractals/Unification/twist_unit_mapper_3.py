import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

# ============================================================
# CONSTANTS (retained for context)
# ============================================================
C = 299_792_458.0        # m/s
HBAR = 1.054_571_817e-34 # J*s

# Standard reference masses (in kg)
M_ELECTRON = 9.1093837015e-31
M_MUON     = 1.883531594e-28
M_TAU      = 3.167771e-27

# ============================================================
# 1. Core Functions (retained)
# ============================================================

def sector_weights(tau, ring_radius=2.2, n_angles=360, t_max=5000, dt=0.01):
    """Evolve particle and return time-averaged sector weights (G, T, R)."""
    n_steps = int(t_max / dt)
    theta = 0.0
    wG = wT = wR = 0.0
    sector_count = 0
    for _ in range(n_steps):
        dtheta = tau * np.sin(theta) * dt
        theta += dtheta
        theta = (theta + np.pi) % (2*np.pi) - np.pi
        if -np.pi/3 <= theta <= np.pi/3:
            wG += 1
        elif theta > np.pi/3:
            wT += 1
        else:
            wR += 1
        sector_count += 1
    return wG/sector_count, wT/sector_count, wR/sector_count

def error_128(tau, **kwargs):
    """Calculates the L2-norm squared error against the 1:2:8 target."""
    target = np.array([1/11, 2/11, 8/11])
    w = np.array(sector_weights(tau, **kwargs))
    E = np.linalg.norm(w - target)**2
    return E, w[0], w[1], w[2]

# ---------------------------------------------
# RUN CALIBRATION (T0 Establishment)
# ---------------------------------------------
def run_calibration(tau_e_cal=5.06, m_e_ref=M_ELECTRON):
    """Establishes T0 using the electron mass and a calibration tau."""
    T0_cal = HBAR * tau_e_cal / (m_e_ref * C**2)
    print("## ⚛️ Step 1: Electron Calibration Confirmation")
    print(f"* Reference Electron Mass (mₑ): {m_e_ref:.6e} kg")
    print(f"* Calibration Twist (τₑ): {tau_e_cal}")
    print(f"**-> Calculated T₀ Constant: {T0_cal:.6e}** ")
    print("-" * 50)
    return T0_cal


# ============================================================
# 2. NEW: Fractal Hunter Core Functions
# ============================================================

def coarse_band_scan(
    tau_min=2.0,
    tau_max=10.0,
    n_bands=8,
    samples_per_band=20
):
    """
    Slices a tau range into bands, computes the *average* 1:2:8 error
    in each band, and sorts them by lowest average error.
    """
    print(f"[Hunter] Coarse scanning τ=[{tau_min:.2f}, {tau_max:.2f}]...")
    bands = []
    edges = np.linspace(tau_min, tau_max, n_bands + 1)
    for i in range(n_bands):
        left = edges[i]
        right = edges[i+1]
        taus = np.linspace(left, right, samples_per_band)
        Es = np.array([error_128(t)[0] for t in taus])

        bands.append({
            "tau_left": left,
            "tau_right": right,
            "tau_mid": 0.5 * (left + right),
            "E_mean": float(Es.mean()),
            "E_std": float(Es.std()),
        })

    bands.sort(key=lambda b: b["E_mean"])
    return bands

def fractal_downhill_search(
    tau_start,
    tau_min,
    tau_max,
    step_init=0.1,
    min_step=1e-6,
    max_iter=300,
    patience=40
):
    """
    One-resonance hunter: only accepts downhill moves, flips direction
    and shrinks step on uphill moves (roll back).
    Returns (tau_best, E_best, history).
    """
    tau = float(tau_start)
    step = float(step_init)
    direction = 1.0  # +1 or -1
    E = error_128(tau)[0]

    tau_best = tau
    E_best = E
    history = [(tau, E)]
    no_improve = 0

    for it in range(max_iter):
        # Propose a move
        tau_trial = tau + direction * step

        # Boundary check
        if tau_trial < tau_min or tau_trial > tau_max:
            direction *= -1.0
            step *= 0.5
            if step < min_step:
                break
            continue

        E_trial = error_128(tau_trial)[0]

        if E_trial < E_best:
            # Strictly better: accept and slightly increase step
            tau = tau_trial
            E = E_trial
            tau_best = tau_trial
            E_best = E_trial
            history.append((tau_best, E_best))
            step *= 1.1  # Push harder while slope is good
            no_improve = 0

        else:
            # Worse or equal: reject, flip and shrink (roll back)
            direction *= -1.0
            step *= 0.5
            no_improve += 1
            if step < min_step or no_improve > patience:
                break

    return tau_best, E_best, history

def find_resonance_one_shot(
    tau_min=2.0,
    tau_max=10.0,
    band_count=8,
    samples_per_band=20,
    step_init=0.1
):
    """
    Stitches together the Coarse Band Scan and the Fractal Downhill Search.
    """
    print("## 🔎 Step 2: Fractal-Aware Resonance Hunting")
    
    # Step 1: coarse band search
    bands = coarse_band_scan(
        tau_min=tau_min,
        tau_max=tau_max,
        n_bands=band_count,
        samples_per_band=samples_per_band
    )
    best_band = bands[0]

    print("[Δ] Best coarse band (lowest Ē):")
    print(f"    τ ∈ [{best_band['tau_left']:.4f}, {best_band['tau_right']:.4f}], "
          f"τ_mid={best_band['tau_mid']:.6f}, Ē={best_band['E_mean']:.3e}")

    # Step 2: fractal downhill search inside that band
    tau_start = best_band["tau_mid"]
    tau_best, E_best, history = fractal_downhill_search(
        tau_start=tau_start,
        tau_min=best_band["tau_left"],
        tau_max=best_band["tau_right"],
        step_init=step_init,
        min_step=1e-6,
        max_iter=300,
        patience=40
    )

    print(f"[Δ] Fractal descent result: τ*={tau_best:.6f}, E*={E_best:.3e}")
    print(f"    Steps taken: {len(history)}")

    # Step 3: local fine refinement around tau_best (using simple grid search)
    eps = 0.02  # small radius around the found dip
    tau_left = max(tau_min, tau_best - eps)
    tau_right = min(tau_max, tau_best + eps)

    tau_fine = np.linspace(tau_left, tau_right, 300)
    E_fine = np.array([error_128(t)[0] for t in tau_fine])
    idx_min = np.argmin(E_fine)
    tau_refined = tau_fine[idx_min]
    E_refined = E_fine[idx_min]

    print(f"[Δ] Local refinement: τ_refined={tau_refined:.6f}, E_refined={E_refined:.3e}")
    
    # Plotting the descent history for visualization
    history_tau = [h[0] for h in history]
    history_E = [h[1] for h in history]
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(tau_fine, E_fine, 'C0-', alpha=0.5, label='Local Fine Scan')
    ax.plot(history_tau, history_E, 'ko-', ms=4, lw=1, label='Downhill Walk History')
    ax.plot(tau_refined, E_refined, 'r*', ms=10, label=f'Refined Min: {tau_refined:.6f}')
    
    ax.set_xlabel("Twist $\\tau$")
    ax.set_ylabel("Error $E(\\tau)$")
    ax.set_title("Fractal Downhill Search for Resonance")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("fractal_descent_history.png", dpi=150)
    print("Saved 'fractal_descent_history.png'")
    
    print("-" * 50)
    return {
        "tau_refined": tau_refined,
        "E_refined": E_refined,
    }


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    
    # 1. Calibrate T0
    T0_cal = run_calibration(tau_e_cal=5.06)
    
    # 2. Find the electron resonance using the fractal hunter
    electron_result = find_resonance_one_shot(
        tau_min=2.0,
        tau_max=10.0,
        band_count=8,
        samples_per_band=20,
        step_init=0.1
    )
    
    tau_found = electron_result['tau_refined']
    
    # 3. Compare the found tau to the calibrated tau (5.06)
    print("## 📈 Step 3: Comparison to Calibrated Electron")
    
    calibrated_tau = 5.06
    calibrated_error = error_128(calibrated_tau)[0]
    
    print(f"* Calibrated τₑ: {calibrated_tau:.6f} (Error: {calibrated_error:.6e})")
    print(f"* Found τ*: {tau_found:.6f} (Error: {electron_result['E_refined']:.6e})")
    
    if np.isclose(tau_found, calibrated_tau, atol=0.01):
        print("\n**Observation:** The dynamically found minimum (τ*) is very close to the calibrated electron twist (τₑ=5.06). This provides strong dynamical support for the electron's choice of twist.")
    else:
        print("\n**Observation:** The dynamically found minimum (τ*) is not close to the calibrated electron twist (τₑ=5.06). Review the resonance condition or search range.")