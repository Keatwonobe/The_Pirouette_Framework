import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import scipy.signal

C = 299_792_458.0        # m/s
HBAR = 1.054_571_817e-34 # J*s

# Standard reference masses (in kg)
M_ELECTRON = 9.1093837015e-31
M_MUON     = 1.883531594e-28 # ~207 * M_e
M_TAU      = 3.167771e-27    # ~3477 * M_e

# ============================================================
# 1. Time-averaged sector weights
# ============================================================

def sector_weights(tau, ring_radius=2.2, n_angles=360, t_max=5000, dt=0.01):
    """
    Evolve a test particle on the electron-shell ring at twist=tau
    and return time-averaged sector weights (G, T, R).
    """
    n_steps = int(t_max / dt)
    theta = 0.0

    wG = wT = wR = 0.0
    sector_count = 0

    for _ in range(n_steps):
        # nonlinear twist evolution law
        dtheta = tau * np.sin(theta) * dt
        theta += dtheta
        theta = (theta + np.pi) % (2*np.pi) - np.pi

        # sector accumulation
        if -np.pi/3 <= theta <= np.pi/3:
            wG += 1
        elif theta > np.pi/3:
            wT += 1
        else:
            wR += 1

        sector_count += 1

    return wG/sector_count, wT/sector_count, wR/sector_count


# ============================================================
# 2. 1:2:8 error functional
# ============================================================

def error_128(tau, **kwargs):
    target = np.array([1/11, 2/11, 8/11])
    w = np.array(sector_weights(tau, **kwargs))
    # Euclidean distance squared (L2 norm squared)
    E = np.linalg.norm(w - target)**2
    return E, w[0], w[1], w[2]


# ============================================================
# 3. Twist-Mass Conversions
# ============================================================

def mass_from_tau(tau, T0):
    """Computes mass from twist τ and calibrated constant T0."""
    return HBAR * tau / (T0 * C**2)

def tau_from_mass(m, T0):
    """Inverts the clock: computes twist τ from mass m and T0."""
    return m * T0 * C**2 / HBAR


# ============================================================
# 4. Substrate Flow Functions (retained from previous iteration)
# ============================================================

def compute_error_grid(tau_min=2.0, tau_max=50.0, n_samples=500):
    """Generates the coarse twist/error grid."""
    print(f"[Scan] Computing error grid from τ={tau_min} to τ={tau_max} with {n_samples} samples...")
    taus = np.linspace(tau_min, tau_max, n_samples)
    errors = np.array([error_128(t)[0] for t in taus])
    return taus, errors

def downhill_labels(errors):
    """
    Walk downhill to find the local minimum ('sink') each point flows to.
    """
    errors = np.asarray(errors)
    N = len(errors)
    sink = np.zeros(N, dtype=int)

    for i in range(N):
        j = i
        while True:
            best = j
            best_err = errors[j]
            # check neighbors
            for k in (j-1, j+1):
                if 0 <= k < N and errors[k] < best_err:
                    best = k
                    best_err = errors[k]
            if best == j:
                break # Reached local minimum
            j = best
        sink[i] = j

    return sink

def segment_twist_space(taus, errors, min_span=3):
    """
    Segment twist space into basins using downhill flow.
    Returns a list of segments sorted by error_min (best first).
    """
    taus = np.asarray(taus)
    errors = np.asarray(errors)
    sink = downhill_labels(errors)

    basins = {}
    for i, s in enumerate(sink):
        basins.setdefault(s, []).append(i)

    segments = []
    for i_min, idx_list in basins.items():
        idx_arr = np.sort(np.array(idx_list))
        if len(idx_arr) < min_span:
            continue

        seg = {
            "i_min": int(i_min),
            "tau_min": float(taus[i_min]),
            "error_min": float(errors[i_min]),
            "indices": idx_arr,
            "tau_left": float(taus[idx_arr[0]]),
            "tau_right": float(taus[idx_arr[-1]]),
        }
        segments.append(seg)

    segments.sort(key=lambda s: s["error_min"])
    return segments

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

# ---------------------------------------------
# NEW: EMPIRICAL MAPPING
# ---------------------------------------------

def map_empirical_masses(T0_cal, segments):
    """
    Calculates the exact tau required by empirical masses (muon, tau)
    and evaluates the error at those points.
    """
    print("## 🗺️ Step 2: Mapping Empirical Lepton Masses to Twist Space")

    # 1. Calculate required empirical tau values
    tau_mu_ref = tau_from_mass(M_MUON, T0_cal)
    tau_tau_ref = tau_from_mass(M_TAU, T0_cal)

    empirical_points = [
        {"name": "Muon", "mass": M_MUON, "tau_ref": tau_mu_ref},
        {"name": "Tau", "mass": M_TAU, "tau_ref": tau_tau_ref},
    ]

    print(f"* Reference Tau Muon (τμ): {tau_mu_ref:.6f}")
    print(f"* Reference Tau Tau (πτ): {tau_tau_ref:.6f}")
    print("-" * 50)

    # 2. Evaluate error at the exact empirical tau points
    print("### Error at Empirical Twist Values (τ_ref)")
    for p in empirical_points:
        tau_ref = p["tau_ref"]
        # Check if tau_ref is within the scanned range for meaningful comparison
        if not (segments[0]["tau_left"] <= tau_ref <= segments[-1]["tau_right"]):
            p["error"] = np.nan
            print(f"  [!] {p['name']} τ={tau_ref:.6f} is outside scan range. Skipping error calculation.")
            continue

        E, G, T, R = error_128(tau_ref)
        p["error"] = E
        p["G"] = G
        p["T"] = T
        p["R"] = R
        print(f"  {p['name']:<10}: Error={E:.6e} | <G>={G:.4f}, <T>={T:.4f}, <R>={R:.4f}")

    print("-" * 50)

    # 3. Compare with Top Basins
    print("### Comparison to Top 5 Basins (Dynamical Minima)")
    
    # Extract refined minima for comparison
    refined_minima = []
    for seg in segments[:5]:
        r = refine_basin_minimum(seg, local_width=1.0)
        refined_minima.append({
            "name": f"Basin-{len(refined_minima)+1}",
            "tau_min": r["tau_min_refined"],
            "E_min": r["E_min_refined"]
        })

    # Add the electron calibration point as the baseline (Basin 0)
    electron_E = error_128(5.06)[0]
    refined_minima.insert(0, {
        "name": "Electron (τ=5.06)",
        "tau_min": 5.06,
        "E_min": electron_E
    })
    
    print(f"{'Basin':<15} | {'τ_minimum':<15} | {'E_minimum':<15}")
    print("-" * 45)
    for r in refined_minima:
        print(f"{r['name']:<15} | {r['tau_min']:<15.6f} | {r['E_min']:<15.6e}")
        
    print("\n[Δ] Metric: The hypothesis is supported if the Muon and Tau τ_ref points")
    print("    fall very close to (i.e., inside or adjacent to) the low-error Basins.")

    # 4. Check Proximity (Optional: Can be done manually by inspecting table)
    # The output table allows for visual empirical comparison.
    
    return empirical_points

# ---------------------------------------------
# Refinement Function (Moved from previous block)
# ---------------------------------------------

def refine_basin_minimum(seg, refine_points=400, local_width=0.5):
    """
    Given a basin segment, perform a local scalar minimization (Brent method).
    """
    tau_center = seg["tau_min"]
    # Define a search bracket around the coarse minimum
    tau_left = max(seg["tau_left"], tau_center - local_width)
    tau_right = min(seg["tau_right"], tau_center + local_width)
    
    # Ensure a valid bracket for Brent's method
    if tau_left >= tau_right:
        tau_left = tau_center - 0.01
        tau_right = tau_center + 0.01

    # local scalar minimization using the coarse min as a seed
    res = scipy.optimize.minimize_scalar(
        lambda t: error_128(t)[0],
        bracket=(tau_left, tau_center, tau_right),
        method="brent"
    )

    return {
        "tau_min_coarse": seg["tau_min"],
        "tau_min_refined": float(res.x),
        "E_min_refined": float(res.fun),
    }

# ---------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------

if __name__ == "__main__":
    
    # 1. Calibrate T0
    T0_cal = run_calibration()
    
    # 2. Compute error grid and segment into basins
    TAU_MIN = 2.0
    TAU_MAX = 50.0
    N_SAMPLES = 500  
    
    taus, errors = compute_error_grid(TAU_MIN, TAU_MAX, N_SAMPLES)
    
    # Segment the space into basins of attraction (your "substrate fill" idea)
    segments = segment_twist_space(taus, errors)

    print(f"\n[INFO] Found {len(segments)} distinct basins in the search range.")

    # 3. Map empirical masses and compare to basins
    if len(segments) > 0:
        map_empirical_masses(T0_cal, segments)
    else:
        print("Cannot proceed: No distinct basins found in the search range.")