# g2_two_point_fit.py
import numpy as np

# ----- INPUTS (replace with your best values) -----
# Experimental central values and 1σ uncertainties:
a_e_exp, sig_e = 1.15965218076e-3, 7.2e-13
a_mu_exp, sig_mu = 1.16592061e-3, 4.1e-10

# Baselines (QED+had+weak you want to regard as "null"):
a_e_null = 1.15965218161e-3   # example baseline — update as needed
a_mu_null = 1.16591810e-3     # example baseline — update as needed

# Lepton masses in GeV:
m_e, m_mu = 0.51099895e-3, 105.6583755e-3

# --------------------------------------------------

y   = np.array([a_e_exp, a_mu_exp])
y0  = np.array([a_e_null, a_mu_null])
dy  = np.array([sig_e, sig_mu])
m   = np.array([m_e, m_mu])

def fit_K(p):
    # Weighted least squares for a_e = a0_e + K*m_e^p, etc.
    X = m**p
    w = 1.0/(dy**2)
    # K_hat = sum(w*X*(y - y0)) / sum(w*X^2)
    num = np.sum(w * X * (y - y0))
    den = np.sum(w * X * X)
    K_hat = num / den
    # Var(K_hat) = 1 / sum(w*X^2)
    K_se = np.sqrt(1.0 / den)
    # χ^2
    resid = (y - (y0 + K_hat*X)) / dy
    chi2 = np.sum(resid**2)
    k = 1  # num free params
    AIC = 2*k + chi2
    return K_hat, K_se, chi2, AIC

for p in (1.0, 2.0):
    K, Kse, chi2, AIC = fit_K(p)
    print(f"p={p:.1f} -> K = {K:.6e} ± {Kse:.6e},  χ²={chi2:.3f},  AIC={AIC:.3f}")

# Optional: quick prediction printout
# print("Pred:", y0 + K*(m**p))
