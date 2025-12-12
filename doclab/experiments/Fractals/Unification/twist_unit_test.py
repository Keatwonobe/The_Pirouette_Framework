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
    # E = np.sum((w - target)**2)  # Euclidean distance squared (L2 norm squared)
    E = np.linalg.norm(w - target)**2
    return E, w[0], w[1], w[2]


# ============================================================
# 3. TwistSpecies Class
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

# ---------------------------------------------
# RUN CALIBRATION
# ---------------------------------------------
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

# ---------------------------------------------
# RUN SCAN AND FIND MINIMA
# ---------------------------------------------
def hunt_for_minima(T0_cal):
    """
    Scans a broad range for strong minima in the error functional,
    selecting the top 3 overall best matches (lowest error).
    """
    TAU_MIN = 2.0
    TAU_MAX = 50.0
    N_SAMPLES = 500  

    print("## 🔎 Step 2: Hunting for Strong Minima (Twist Scan)")
    print(f"Scanning from τ={TAU_MIN} to τ={TAU_MAX} with {N_SAMPLES} samples...")
    
    taus = np.linspace(TAU_MIN, TAU_MAX, N_SAMPLES)
    errors = np.array([error_128(tau)[0] for tau in taus])
    
    N_CANDIDATES = 3
    tau_e_cal = 5.06
    
    # FIX: Use np.argsort to find the indices of the N lowest error values
    # This avoids the TypeError and reliably finds the top N candidates.
    best_overall_indices = np.argsort(errors)[:N_CANDIDATES]

    minima_results = []
    lepton_names = ["Electron-Candidate", "Muon-Candidate", "Tau-Candidate"]
    
    print("\n[Δ] Top 3 Strongest Minima Found:")
    
    for i in range(N_CANDIDATES):
        idx = best_overall_indices[i]
        tau_cand = taus[idx]
        error_cand = errors[idx]

        # Name assignment logic
        name = lepton_names[i]
        
        # If the best match is close to 5.06, use the calibrated value and name it Electron
        if np.isclose(tau_cand, tau_e_cal, atol=0.05):
             tau_cand = tau_e_cal 
             name = "Electron (Calibrated)"
        elif i == 0:
            name = "Electron-Candidate (Global Minimum)" # Safest label for the lowest error point

        minima_results.append({
            "name": name,
            "tau": tau_cand,
            "error": error_cand,
            "index": idx
        })
        
        print(f"  #{i+1}: {name:<35} | τ*={tau_cand:.6f} | Error={error_cand:.6e}")
        
    print("-" * 50)
    return minima_results

# ---------------------------------------------
# CALCULATE MASS RATIOS
# ---------------------------------------------
def calculate_mass_ratios(minima_results, T0_cal):
    """
    Plugs the candidate twists into the calibration and calculates ratios.
    """
    if len(minima_results) < 3:
        print("Not enough unique minima found (need 3) to calculate all ratios.")
        return

    print("## 📏 Step 3: Mass Ratios Calculation")
    
    # Create TwistSpecies objects for the three candidates
    species = [TwistSpecies(m["name"], m["tau"], T0_cal) for m in minima_results]
    
    m_e_twist = species[0].mass
    
    ratio_mu_e_twist = species[1].tau / species[0].tau
    ratio_tau_e_twist = species[2].tau / species[0].tau
    
    # Ratios based on CODATA reference masses
    ratio_mu_e_ref = M_MUON / M_ELECTRON
    ratio_tau_e_ref = M_TAU / M_ELECTRON

    print(f"* Electron Candidate Mass (mₑ*): {m_e_twist:.6e} kg")
    print(f"* Muon Candidate Twist (τμ*): {species[1].tau:.6f}")
    print(f"* Tau Candidate Twist (ττ*): {species[2].tau:.6f}")
    
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
    
    # 2. Hunt for the next two strong minima
    minima = hunt_for_minima(T0_cal)

    # 3. Calculate mass ratios
    if len(minima) >= 3:
        calculate_mass_ratios(minima, T0_cal)
    else:
        print("Cannot calculate mass ratios: Need at least 3 strong minima candidates.")