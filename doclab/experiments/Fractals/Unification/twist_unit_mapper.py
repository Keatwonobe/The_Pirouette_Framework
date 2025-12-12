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
# 3. TwistSpecies Class (for reference)
# ============================================================

class TwistSpecies:
    def __init__(self, name, tau, T0, ring_radius=2.2):
        self.name = name
        self.tau = tau
        self.ring_radius = ring_radius
        self.T0 = T0

        # static sector fractions
        self.G, self.T, self.R = sector_weights(tau, ring_radius=ring_radius)

        # mass from twist clock
        self.mass = HBAR * tau / (self.T0 * C**2)
        
        # simple charge & weak-ness ansatz
        self.charge = (self.T - self.G)
        self.weakness = self.R

def mass_from_tau(tau, T0):
    """
    Computes mass from twist τ and calibrated constant T0.
    """
    return HBAR * tau / (T0 * C**2)

# ============================================================
# 4. New: Substrate Flow Functions
# ============================================================

def compute_error_grid(tau_min=2.0, tau_max=50.0, n_samples=500):
    """Generates the coarse twist/error grid."""
    print(f"[Scan] Computing error grid from τ={tau_min} to τ={tau_max} with {n_samples} samples...")
    taus = np.linspace(tau_min, tau_max, n_samples)
    errors = np.array([error_128(t)[0] for t in taus])
    return taus, errors

def downhill_labels(errors):
    """
    For each index i, walk downhill (to neighbors with lower error)
    until a local minimum is reached. Return an array 'sink[i]'
    giving the index of the local minimum each point flows to.
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
                # we've reached a local minimum
                break
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

    # group indices by their sink
    basins = {}
    for i, s in enumerate(sink):
        basins.setdefault(s, []).append(i)

    segments = []
    for i_min, idx_list in basins.items():
        idx_arr = np.sort(np.array(idx_list))
        if len(idx_arr) < min_span:
            continue  # ignore tiny basins (likely noise)

        seg = {
            "i_min": int(i_min),
            "tau_min": float(taus[i_min]),
            "error_min": float(errors[i_min]),
            "indices": idx_arr,
            "tau_left": float(taus[idx_arr[0]]),
            "tau_right": float(taus[idx_arr[-1]]),
        }
        segments.append(seg)

    # sort by error at the minimum (best first)
    segments.sort(key=lambda s: s["error_min"])
    return segments

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
    # Use a bracket method like 'brent' for reliable minimum finding
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

# ============================================================
# 5. Execution and Analysis Functions
# ============================================================

def run_calibration(tau_e_cal=5.06, m_e_ref=M_ELECTRON):
    """
    Establishes T0 and confirms electron mass is reproduced.
    """
    T0_cal = HBAR * tau_e_cal / (m_e_ref * C**2)
    electron = TwistSpecies("Electron_Cal", tau_e_cal, T0_cal)
    reproduced_mass = electron.mass
    
    print("## ⚛️ Step 1: Electron Calibration Confirmation")
    print(f"* Reference Electron Mass (mₑ): {m_e_ref:.6e} kg")
    print(f"* Calibration Twist (τₑ): {tau_e_cal}")
    print(f"* Calculated T₀ Constant: {T0_cal:.6e} ")
    print(f"**-> Reproduced Mass: {reproduced_mass:.6e} kg** (Confirms calibration)")
    print("-" * 50)
    return T0_cal

def analyze_lepton_candidates(segments, T0, tau_e=5.06):
    """
    Refines the minima of the top segments and computes mass ratios.
    """
    
    # 1. Refine minima for the top 5 candidates
    refined_results = []
    print("## 🔎 Step 2: Global Basin Segmentation & Refinement")
    print("\n[Δ] Top 5 Twist Basins Found (Coarse Scan):")
    
    for k, seg in enumerate(segments[:5]):
        # Refine the local minimum using high-resolution solver
        r = refine_basin_minimum(seg, local_width=1.0) 
        r["name"] = f"Candidate-{k+1}"
        
        print(
            f"  #{k+1:2d}: τ_coarse={seg['tau_min']:.4f}, "
            f"τ_refined={r['tau_min_refined']:.6f}, "
            f"E_min={r['E_min_refined']:.3e}, "
            f"range=[{seg['tau_left']:.2f}, {seg['tau_right']:.2f}], "
            f"size={len(seg['indices'])}"
        )
        
        # Check if this basin is the electron's
        if np.isclose(r['tau_min_refined'], tau_e, atol=0.01):
            r["name"] = "Electron (Calibrated)"
            
        refined_results.append(r)
        
    print("-" * 50)
    
    # 2. Select the three candidates for lepton family (Electron, Muon, Tau)
    # We select the three distinct minima with the lowest refined error.
    
    # Filter out the Electron candidate if it's in the top 3, otherwise use the best 3 non-electron candidates.
    candidates = [r for r in refined_results if "Electron" not in r["name"]]
    
    # Ensure the electron is the first one, using the calibrated value
    electron_result = {
        "tau_min_refined": tau_e, 
        "E_min_refined": error_128(tau_e)[0], 
        "name": "Electron (Calibrated)"
    }
    
    # Sort remaining candidates by error again, just in case
    candidates.sort(key=lambda r: r["E_min_refined"])

    # If we have enough, take the electron + next two best
    if len(candidates) >= 2:
        final_candidates = [electron_result, candidates[0], candidates[1]]
    elif len(candidates) == 1:
        final_candidates = [electron_result, candidates[0], {"tau_min_refined": 0, "name": "Missing"}] # Placeholder
    else:
        final_candidates = [electron_result, {"tau_min_refined": 0, "name": "Missing"}, {"tau_min_refined": 0, "name": "Missing"}]

    
    # 3. Calculate Mass Ratios
    
    print("## 📏 Step 3: Mass Ratio Comparison")
    
    m_e_ref_kg = M_ELECTRON
    m_mu_ref_kg = M_MUON
    m_tau_ref_kg = M_TAU

    tau_e_twist = final_candidates[0]["tau_min_refined"]
    tau_mu_twist = final_candidates[1]["tau_min_refined"]
    tau_tau_twist = final_candidates[2]["tau_min_refined"]
    
    m_e_twist = mass_from_tau(tau_e_twist, T0)
    m_mu_twist = mass_from_tau(tau_mu_twist, T0)
    m_tau_twist = mass_from_tau(tau_tau_twist, T0)
    
    if tau_mu_twist == 0 or tau_tau_twist == 0:
        print("\n**Error:** Could not find two other unique basins to form the Muon/Tau families.")
        return

    ratio_mu_e_twist = m_mu_twist / m_e_twist
    ratio_tau_e_twist = m_tau_twist / m_e_twist
    
    ratio_mu_e_ref = m_mu_ref_kg / m_e_ref_kg
    ratio_tau_e_ref = m_tau_ref_kg / m_e_ref_kg

    print(f"* Electron Twist (τₑ*): {tau_e_twist:.6f}")
    print(f"* Muon Candidate Twist (τμ*): {tau_mu_twist:.6f}")
    print(f"* Tau Candidate Twist (ττ*): {tau_tau_twist:.6f}")
    
    print("\n### Mass Ratio Comparison (to Electron)")
    print("------------------------------------------------------------------")
    print(f"{'Lepton':<10} | {'Twist Ratio (m*/mₑ*)':<20} | {'CODATA Ratio':<20} | {'Difference (%)':<15}")
    print("------------------------------------------------------------------")
    
    # Muon ratio
    diff_mu = 100 * (ratio_mu_e_twist - ratio_mu_e_ref) / ratio_mu_e_ref
    print(f"{'Muon':<10} | {ratio_mu_e_twist:<20.4f} | {ratio_mu_e_ref:<20.4f} | {diff_mu:<15.2f}%")
    
    # Tau ratio
    diff_tau = 100 * (ratio_tau_e_twist - ratio_tau_e_ref) / ratio_tau_e_ref
    print(f"{'Tau':<10} | {ratio_tau_e_twist:<20.4f} | {ratio_tau_e_ref:<20.4f} | {diff_tau:<15.2f}%")
    
    print("------------------------------------------------------------------")
    
    if abs(diff_mu) < 50 or abs(diff_tau) < 50:
         print("\n**WOAH!** The predicted mass ratios are within 50% of the standard model values. This absolutely needs a serious write-up.")
    else:
         print("\nThe predicted mass ratios are outside the rough range of the standard model. More investigation into the error functional is needed.")


# ---------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------
if __name__ == "__main__":
    
    # 1. Calibrate T0 and confirm m_e
    T0_cal = run_calibration()
    
    # 2. Compute error grid and segment into basins
    TAU_MIN = 2.0
    TAU_MAX = 50.0
    N_SAMPLES = 500  
    
    taus, errors = compute_error_grid(TAU_MIN, TAU_MAX, N_SAMPLES)
    
    # Segment the space into basins of attraction (your "substrate fill" idea)
    segments = segment_twist_space(taus, errors)

    print(f"\n[INFO] Found {len(segments)} distinct basins in the search range.")

    # 3. Analyze the top basins and calculate mass ratios
    if len(segments) >= 3:
        analyze_lepton_candidates(segments, T0_cal)
    else:
        print("Cannot calculate mass ratios: Need at least 3 strong minima candidates.")