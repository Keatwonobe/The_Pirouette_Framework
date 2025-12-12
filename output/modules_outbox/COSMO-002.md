---
id: COSMO‑Γ‑MERGE
title: "Cluster Collisions: κ–X‑ray Offsets from Γ‑Condensate Dynamics"
Version: 1.0 (proposal)
Status: Experimental (complies with MATH‑018/019/020; children of COSMO‑Γ‑000/‑HALO)
Parents: [MATH‑018, MATH‑019, MATH‑020, COSMO‑Γ‑000, COSMO‑Γ‑HALO]
Children: []

Summary: "Purpose
Simulate and predict lensing–gas centroid offsets in cluster mergers using Γ‑condensates (topological index T) plus collisional baryonic gas. Demonstrate that collisionless behavior of Γ reproduces observed κ–X‑ray separations and their redshift/mass scaling **without particulate CDM**, using the same frozen potential V(Γ) from COSMO‑Γ‑000.

Summary of Claims
• Γ condensates behave as effectively collisionless mass components across cluster‑scale encounters; gas shocks and lags.
• The peak offset Δx ≡ |x_κ − x_X| follows a universal scaling law Δx ≃ 𝔽(M_1,M_2,b,v_in,z; V(Γ)) determined by the Γ halo structure, not by an elastic DM cross‑section.
• The redshift evolution of Δx and the survival of κ peaks after core passage are fixed by the same parameters that set galactic cores (Σ₀ locus in COSMO‑Γ‑HALO)."

---

## Section 1 — Model and Equations
Components: two Γ‑halos (indices T_1, T_2) + baryonic gas (ideal fluid) + passive galaxy tracers.

Field–gravity sector (weak‑field, 3D):
(1) Γ̈ − ∇²Γ + V′(Γ) = 0
(2) ∇²Φ = 4πG [ρ_Γ + ρ_gas + ρ_*]
(3) ρ_Γ = ½(Γ̇² + |∇Γ|²) + V(Γ) − V(Γ_∞)

Gas (Euler + energy with cooling off for first pass):
(4) ∂_t ρ_g + ∇·(ρ_g u) = 0
(5) ∂_t (ρ_g u) + ∇·(ρ_g u⊗u + P I) = −ρ_g ∇Φ
(6) ∂_t E + ∇·[(E+P)u] = −ρ_g u·∇Φ  ,  P=(γ−1)(E−½ρ_g|u|²)

Initial conditions (t→−∞): two equilibrium Γ‑halo solutions from COSMO‑Γ‑HALO positioned at separation d_0, relative velocity v_in, impact parameter b; gas in hydrostatic balance within each potential well.

Observables:
• Lensing κ(x,y) from Σ(x,y)=∫(ρ_Γ+ρ_g+ρ_*) dl.
• X‑ray surface brightness S_X∝∫ n_e² Λ(T) dl (adiabatic: proxy via ρ_g^2 √T).
• Centroid offset Δx(t) between κ peak(s) and S_X peak(s).
• Shock Mach number 𝓜 from gas jump conditions; SZ Compton‑y map (optional).

---

## Section 2 — Numerics (MATH‑020 compliant)
Domain: 3D box with open boundaries; AMR or nested grids recommended.
Discretization:
• Γ: finite‑difference or spectral on AMR; time‑integrator leapfrog/Verlet or RK with CFL control.
• Gravity: multigrid Poisson solver each step.
• Gas: shock‑capturing (HLLC/Roe) finite‑volume scheme; γ=5/3.

Tolerances & checks:
• Energy conservation error < 1% pre‑ and post‑pericenter (excluding shocks’ numerical dissipation).
• Poisson residual < 1e‑6 per V‑cycle.
• Convergence under refinement by factor 2 → Δ(Δx)/Δx < 5%.

---

## Section 3 — Predictions & Scaling Laws
P1 — Offset scaling
For equal‑mass mergers (M,M) near head‑on (b≪r_c):
Δx_max ≈ A(V)
· (v_in/2000 km s⁻¹)^{α} · (M/10^{15} M_⊙)^{β} · (1+z)^{γ}
with A,α,β,γ **fixed** once V(Γ) is frozen; no tunable cross‑section.

P2 — Survivability of κ peaks
Post‑pericenter, the Γ peaks re‑emerge with fractional mass retention f_ret(M,b,v_in) prescribed by the Γ halo binding; gas lags with an arc‑like shock.

P3 — Weak self‑interaction proxy
An apparent “σ/m” constraint inferred in CDM language maps in Pirouette to a **derived** (non‑tunable) effective collisional proxy σ_eff/m determined by Γ soliton overlap; prediction: σ_eff/m ≲ 0.2 cm² g⁻¹ for Bullet‑like events when V(Γ) is COSMO‑Γ‑000‑frozen.

Falsification:
• Required σ/m to match Δx exceeds σ_eff/m bound from the frozen V(Γ).
• κ peaks do not survive with observed strengths for real systems at given (M,b,v), contradicting f_ret predictions.

---

## Section 4 — Artifacts & Configs
Artifacts (JSON)
merge_result.json
{
"M1": 1.2e15,
"M2": 1.1e15,
"b_kpc": 120,
"v_in_kms": 2800,
"z": 0.296,
"T1": 1,
"T2": 1,
"Delta_x_peak_kpc": 180.0,
"t_at_Delta_x_Gyr": 0.12,
"f_ret_1": 0.86,
"f_ret_2": 0.84,
"M_mach": 3.1,
"theta_E_arcsec": 29.5,
"kappa_map": "path/to/κ.fits",
"xray_map": "path/to/SX.fits",
"sz_map": "path/to/y.fits",
"commit": "<git>",
"freeze_manifest": "path/to/manifest.yaml"
}

Config (YAML)
merge_config.yaml
anchor: from_COSMO_G0_freeze
potential:
type: quadratic_plus_quartic
m_Gamma: ${from_freeze}
lambda4: ${from_freeze}
clusters:

* mass: 1.2e15  # Msun
  T_index: 1
  gas_fraction: 0.12
* mass: 1.1e15
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
  solver:
  poisson: multigrid
  hydro: HLLC
  time_integrator: leapfrog
  tolerances:
  poisson_resid: 1e-6
  energy_err_frac: 0.01
  outputs:
  save_maps: [kappa, xray, sz]
  track_offsets: true

Compliance footer
□ Compliance MATH‑018/019/020 and COSMO‑Γ‑000/‑HALO. □ One‑shot anchor inherited; no retuning. □ Δx scaling reported with uncertainties. □ JSON/YAML artifacts emitted. □ Convergence tests passed.

End of COSMO‑Γ‑MERGE v1.0
