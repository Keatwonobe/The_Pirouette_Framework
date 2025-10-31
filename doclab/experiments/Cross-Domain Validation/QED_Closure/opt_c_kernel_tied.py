# Re-run Option C with kernel width tied to plateau width: sigma_phi = beta * Delta_phi0.
import numpy as np, math, json
import matplotlib.pyplot as plt
from pathlib import Path
from numpy.fft import fft, ifft

ROOT = Path("C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Cross-Domain Validation/QED_Closure")

# Parameters
beta_kernel = 2.2   # sigma_phi = beta * Delta_phi0 (chosen from sensitivity scan region with binding)
phi_star = 0.15
Qchi = 1.5          # choose a value that exhibited strong binding at moderate sigma_phi
Delta_phi0 = 1.2
omega_c = 1.0 / phi_star
sigma_phi = beta_kernel * Delta_phi0

# Shared defs
def plateau(phi, center, Delta_phi, Qchi):
    s = max(Delta_phi, 1e-6) / 2.0
    return np.exp(-Qchi * ((phi-center)**2) / (2*s**2))

def K_line(phi, Qchi, sigma_phi):
    return np.exp(-0.5*(phi/sigma_phi)**2) * np.sinc(Qchi*phi/np.pi)

def overlap_pair(phi, psi1, psi2, Qchi, sigma_phi):
    kern = K_line(phi, Qchi, sigma_phi)
    Khat = fft(np.roll(kern, -len(kern)//2))
    conv = np.real(ifft(fft(psi2) * Khat))
    conv = np.roll(conv, len(conv)//2)
    dphi = phi[1]-phi[0]
    return float(np.sum(psi1 * conv) * dphi)

def self_energy(Delta_phi): return 1.0/(Delta_phi**2)

phi = np.linspace(-8, 8, 4096)

def minimize_pair_energy(g, n_w=45, n_s=60, w_lo=0.3, w_hi=1.2, s_lo=0.0, s_hi=3.0):
    widths = np.linspace(w_lo*Delta_phi0, w_hi*Delta_phi0, n_w)
    seps = np.linspace(s_lo, s_hi, n_s)
    Emin = 1e9; best = None
    for w in widths:
        for s in seps:
            psi1 = plateau(phi, -s/2.0, w, Qchi)
            psi2 = plateau(phi, +s/2.0, w, Qchi)
            ov = overlap_pair(phi, psi1, psi2, Qchi, sigma_phi)
            E = 2*self_energy(w) - g*ov
            if E < Emin:
                Emin = E; best = (w, s, ov)
    return Emin, best  # best = (w*, s*, overlap*)

# Observables conversion
C_XI = 0.60; K0 = 1.0
def xi_Gamma_from_plateau(omega_c, Delta_phi_eff, chi=1.0):
    return C_XI / (omega_c * Delta_phi_eff) * (chi**(-0.5))
def kappa3_from_plateau(omega_c, phi_star, Qchi, Delta_phi_eff):
    curvature = Qchi / (Delta_phi_eff**2)
    return K0 * (omega_c / phi_star)**2 * curvature
def calibrate_c_sigma(sigma_phys, kappa3_ref, xi_gamma_ref):
    return (sigma_phys * (xi_gamma_ref**2)) / kappa3_ref
def sigma_from_core(kappa3, xi_gamma, c_sigma):
    return c_sigma * (kappa3 / (xi_gamma**2))
def r0_from_sigma(sigma): return math.sqrt(1.65/sigma)
def a_from_r0(r0, ratio): return r0/ratio

# Fixed scales
sigma_phys = 0.44**2; kappa3_ref = 1.0/1.3**2; xi_gamma_ref = 0.60; r0_over_a_lat = 5.3
c_sigma = calibrate_c_sigma(sigma_phys, kappa3_ref, xi_gamma_ref)

# Tune g against sqrt(sigma)=0.44 GeV
def sigma_for_g(g):
    Emin, best = minimize_pair_energy(g)
    w_eff, s_eff, ov = best
    xi = xi_Gamma_from_plateau(omega_c, w_eff, chi=1.0)
    k3 = kappa3_from_plateau(omega_c, phi_star, Qchi, w_eff)
    sig = sigma_from_core(k3, xi, c_sigma)
    return sig, w_eff, s_eff, Emin

# bracket
g_lo, g_hi = 0.1, 50.0
s_lo, *rest = sigma_for_g(g_lo)
s_hi, *rest = sigma_for_g(g_hi)
it=0
while s_hi < sigma_phys and it<10:
    g_hi *= 1.5; s_hi, *_ = sigma_for_g(g_hi); it+=1

# bisection
for _ in range(50):
    g_mid = 0.5*(g_lo+g_hi)
    s_mid, w_eff, s_eff, E_min = sigma_for_g(g_mid)
    if abs(s_mid - sigma_phys) < 1e-8 or abs(g_hi-g_lo) < 1e-4:
        g_match = g_mid; break
    if s_mid < sigma_phys:
        g_lo = g_mid
    else:
        g_hi = g_mid
g_match = 0.5*(g_lo+g_hi)
sig, w_eff, s_eff, E_min = sigma_for_g(g_match)

# Report & basic downstream (QCD-only)
r0 = r0_from_sigma(sig); a_lat = a_from_r0(r0, r0_over_a_lat)
print({"beta_kernel": beta_kernel, "sigma_phi": sigma_phi, "g_match": g_match, "sigma": sig, "sqrt_sigma": math.sqrt(sig), "Delta_eff": w_eff, "sep_eff": s_eff, "E_min": E_min, "r0": r0, "a": a_lat})
