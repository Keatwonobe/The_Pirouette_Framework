import numpy as np
from twist_unit import sector_weights

def sample_modes(min_tau=1.8, max_tau=6.0, N=1200):
    taus = np.linspace(min_tau, max_tau, N)
    Gs, Ts, Rs = [], [], []
    for t in taus:
        G, T, R = sector_weights(t)
        Gs.append(G)
        Ts.append(T)
        Rs.append(R)
    return taus, np.array(Gs), np.array(Ts), np.array(Rs)

def quadratic_fit(taus, y):
    # fit y = a τ^2 + b τ + c
    coeffs = np.polyfit(taus, y, 2)
    a, b, c = coeffs
    tau_star = -b/(2*a)
    curvature = 2*a
    return tau_star, curvature, coeffs

def main():
    taus, G, T, R = sample_modes()

    # focus on R (best structure)
    tau_p_star, kappa_eff, coeffs = quadratic_fit(taus, R)

    print("\n[ Proton Selector from Raw Mode R(τ) ]")
    print("--------------------------------------")
    print(f"τ_p* (from curvature): {tau_p_star}")
    print(f"κ_eff (local curvature): {kappa_eff}")
    print(f"Quadratic coefficients: a={coeffs[0]}, b={coeffs[1]}, c={coeffs[2]}")

    # predicted proton mass (mass ∝ τ)
    tau_e = 5.060  # from your earlier analysis
    mp_me = tau_p_star / tau_e
    print(f"\nPredicted m_p/m_e ≈ {mp_me}")

if __name__ == "__main__":
    main()
