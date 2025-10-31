---
id: COSMO‑Γ‑CMB‑APP
title: Equations & Configs (Appendix to COSMO‑Γ‑CMB)
Version: 1.0
Status: Technical Appendix (Normative to COSMO‑Γ‑CMB)
Parents: [COSMO‑Γ‑CMB, MATH‑018, MATH‑019]
Children: []

Summary: "Purpose
Provide exact conformal‑time equations for background and linear perturbations of Γ suitable for direct insertion into CLASS/CAMB, plus a Freeze Manifest template and runnable YAML/INI configs for the Γ cosmology and halo/merge solvers."

---

A) Exact Equations (Conformal Time η)
Notation: a(η) scale factor; ℋ ≡ a′/a; primes = d/dη; k = comoving wavenumber; metric potentials (Newtonian gauge) Φ,Ψ.

A1. Background (FIELD FORM)
Γ′′ + 2ℋ Γ′ + a² V_{,Γ}(Γ) = 0
ρ_Γ = (Γ′²)/(2 a²) + V(Γ)
p_Γ = (Γ′²)/(2 a²) − V(Γ)
Conformal Friedmann: ℋ² = (8πG/3) a² (ρ_r + ρ_b + ρ_Γ)

A2. Perturbations (Newtonian Gauge, FULL FIELD)
δΓ′′ + 2ℋ δΓ′ + (k² + a² V_{,ΓΓ}) δΓ = 4 Γ′ Φ′ − 2 a² V_{,Γ} Φ
δρ_Γ = (1/a²) (Γ′ δΓ′ − Γ′² Φ) + V_{,Γ} δΓ
δp_Γ = (1/a²) (Γ′ δΓ′ − Γ′² Φ) − V_{,Γ} δΓ
(ρ_Γ + p_Γ) θ_Γ = (k²/a²) Γ′ δΓ
σ_Γ = 0 (canonical scalar)

Einstein closures (for completeness):
k² Φ + 3ℋ (Φ′ + ℋ Ψ) = 4πG a² δρ_tot
Φ′ + ℋ Ψ = 4πG a² Σ_s (ρ_s + p_s) θ_s / k²
Φ − Ψ = 8πG a² Σ_s (ρ_s + p_s) σ_s  (→ 0 here since σ_Γ=0)

A3. Fluid Mapping (Oscillatory Regime, OPTIONAL)
When m_Γ ≫ H and the field oscillates rapidly,
w_Γ ≈ 0,
c_{s,eff}²(k,a) ≈ (k²/a²) / (4 m_Γ² + k²/a²)
Evolution equations:
δ̇_Γ = −(1 + w_Γ)(θ_Γ − 3 Φ̇) − 3H (c_{s,eff}² − w_Γ) δ_Γ
θ̇_Γ = −H θ_Γ + k² Ψ + k² c_{s,eff}² δ_Γ/(1 + w_Γ)
(Overdots here are physical‑time derivatives; in code, convert using d/dη = a d/dt.)

A4. Initial Conditions (Super‑Horizon, Adiabatic)
Given primordial curvature ζ and Φ≈const, a consistent choice is:
δΓ_ini = − (Γ′/ℋ) Φ_ini
δΓ′_ini = − [ (Γ′′/ℋ) − Γ′ (ℋ′/ℋ²) ] Φ_ini
with other species set by standard adiabatic relations. In CLASS, hook this into the adiabatic IC branch for the new species.

---

B) CLASS/CAMB Patch Points (Skeleton)
Background:
/* background_derivs.c */
/* y[igamma] = Γ, y[igammap] = Γ′ */
dydeta[igamma]   = y[igammap];
dydeta[igammap]  = -2*H_conf*y[igammap] - a*a*Vprime(gamma);
rho_gamma = 0.5*(y[igammap]*y[igammap])/(a*a) + V(gamma);
pre_gamma = 0.5*(y[igammap]*y[igammap])/(a*a) - V(gamma);

Perturbations:
/* perturbations_derivs.c */
/* u[delta_gamma] = δΓ, u[delta_gamma_p] = δΓ′ */
udot[delta_gamma]    = u[delta_gamma_p];
udot[delta_gamma_p]  = -2*H_conf*u[delta_gamma_p]
- (k2 + a*a*Vsecond(gamma)) * u[delta_gamma]
+ 4*gamma_p*phi_p - 2*a*a*Vprime(gamma)*phi;
/* sources */
delta_rho_gamma = (gamma_p*u[delta_gamma_p] - gamma_p*gamma_p*phi)/(a*a)
+ Vprime(gamma)*u[delta_gamma];
delta_p_gamma   = (gamma_p*u[delta_gamma_p] - gamma_p*gamma_p*phi)/(a*a)
- Vprime(gamma)*u[delta_gamma];
theta_gamma     = (k2*gamma_p*u[delta_gamma])/(a*a) / (rho_gamma + pre_gamma);
shear_gamma     = 0.0;

Switching (optional): when m_Γ/H > switch_threshold and k/a < κ_switch m_Γ, route to fluid mapping branch using c_{s,eff}².

---

C) Freeze Manifest Template (YAML)
freeze_manifest.yaml
anchor:
type: Omega_m0 | H0 | a_e  # choose one (MATH‑018 D3)
value: 0.315
justification: "One‑shot global scale set; all U,T frozen thereafter."
commit:
repo: [git@github.com](mailto:git@github.com):.../pirouette.git
hash: <GIT_HASH>
timestamp_utc: 2025‑10‑10T13:00:00Z
U_parameters:
m_Gamma_eV: 1.7e7     # 17 MeV (pressuron)
lambda4: 0.0
V_tail:
type: exp_shallow
mu_eV: 1.0e-33
Gamma_star_Mpl: 1.0
T_indices:
allowed: [−2, −1, 0, 1, 2]
chosen_defaults: {halos: 1}
seeds:
rng: 1337
mc: 424242
environment:
compiler: gcc‑13.2
blas: OpenBLAS 0.3.26
os: Ubuntu 22.04
class_version: v3.x‑pir‑gamma‑branch
compliance:
MATH_018: true
MATH_019: true
MATH_020: true
notes:

* "c_GW=c enforced (no non‑minimal curvature portals)."
* "No continuous mass exponents; topology is discrete."

---

D) Runnable Configs

D1. Cosmology (CLASS‑style INI)
cosmology.ini

# Base parameters

Omega_b=0.049
Omega_cdm=0.000      # replaced by Gamma sector
H0=67.4
n_s=0.965
A_s=2.1e-9
tau_reio=0.054

# Gamma sector

Gamma_species=on
Gamma_potential=quadratic_plus_tail
m_Gamma_eV=1.7e7
lambda4=0.0
V_tail_type=exp_shallow
V_tail_mu_eV=1.0e-33
V_tail_Gamma_star_Mpl=1.0
Gamma_ini_Mpl=1.2
Gamma_ini_prime=0.0
switch_threshold_m_over_H=50.0
kappa_switch=0.5

# Outputs

l_max_scalars=3000
output= tCl,pCl,lCl,mPk
P_k_max_h/Mpc=5.0
z_pk=0,0.5,1.0

# Consistency

Omega_gamma_auto=on  # auto‑compute Ω_Γ from initial conditions + potential

D2. Halo Solver (YAML)
halo_config.yaml
freeze_manifest: path/to/freeze_manifest.yaml
potential:
type: quadratic_plus_tail
m_Gamma_eV: ${from_freeze}
lambda4: ${from_freeze}
tail:
type: exp_shallow
mu_eV: ${from_freeze}
Gamma_star_Mpl: ${from_freeze}
geometry:
R_max_kpc: 300
baryons:
profile: burkert
params: {rho0_b: 0.02, r_b_kpc: 5.0}
solver:
scheme: spectral
N_points: 1024
tol: 1e-10
lensing:
distances_Mpc: {Dd: 800, Ds: 1800, Dds: 1200}
outputs:
save_profiles: true

D3. Merge Solver (YAML)
merge_config.yaml
freeze_manifest: path/to/freeze_manifest.yaml
potential:
type: quadratic_plus_tail
m_Gamma_eV: ${from_freeze}
lambda4: ${from_freeze}
tail:
type: exp_shallow
mu_eV: ${from_freeze}
Gamma_star_Mpl: ${from_freeze}
clusters:

* mass_Msun: 1.2e15
  T_index: 1
  gas_fraction: 0.12
* mass_Msun: 1.1e15
  T_index: 1
  gas_fraction: 0.12
  orbit:
  impact_parameter_kpc: 120
  v_in_kms: 2800
  z: 0.296
  numerics:
  box_Mpc: 8
  base_grid: 256
  AMR_levels: 3
  poisson: multigrid
  hydro: HLLC
  time_integrator: leapfrog
  tolerances:
  poisson_resid: 1e-6
  energy_err_frac: 0.01
  outputs:
  maps: [kappa, xray, sz]
  track_offsets: true

---

E) Validation Checklist (Copy‑Paste)
□ Background matches ΛCDM when V_tail→0 and m_Γ/H→∞ (≤0.1%).
□ Boltzmann run produces TT/TE/EE and lensing within Planck contours for frozen params.
□ fσ_8(z) agrees with COSMO‑Γ‑000 to within 0.2%.
□ Switching threshold scans stable (<0.2% spectra change for ×2 change).
□ Halo Σ₀ locus reproduced from same freeze.
□ MERGE Δx scaling consistent with frozen V(Γ); convergence passed.

End of COSMO‑Γ‑CMB‑APP v1.0

