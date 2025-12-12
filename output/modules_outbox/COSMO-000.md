---
id: COSMO‑Γ‑000
title: Unified Dark Sector from Temporal Pressure Γ
Version: 1.0 (proposal)
Status: Experimental (complies with MATH‑018/019/020)
Parents: [MATH‑018, MATH‑019, MATH‑020]
Children: [COSMO‑Γ‑HALO, COSMO‑Γ‑MERGE]

Summary: "Purpose
Establish a single‑field Pirouette cosmology in which the temporal‑pressure scalar Γ reproduces the observed phenomenology attributed to cold dark matter (CDM) and dark energy (DE) as two dynamical regimes of the same field. All functional choices obey MATH‑018 D2 (local, analytic, scale‑covariant), with one‑shot anchoring (D3) and preregistered, out‑of‑sample predictions (P4).

Summary
• Early Universe (DM‑like): Γ oscillates about a quadratic minimum with m_Γ ≫ H → ⟨w_Γ⟩ → 0, c_s^2 → 0, clustering like CDM.
• Late Universe (DE‑like): Γ slow‑rolls on a flat segment of V(Γ) → w_Γ ≈ −1, nearly homogeneous, driving acceleration.
• No additional fluids beyond standard baryons/radiation; “dark sector” is unified by Γ."

---

## Section 1 — Action, Field Content, and Constraints
Spacetime: FLRW (M, g) with scale factor a(t).
Field: real scalar Γ: M→ℝ.
Action (low‑energy, D2‑compliant):
S = ∫ d^4x √−g [ ½ ∂_μΓ ∂^μΓ − V(Γ) + L_int(Γ; g) ]
with L_int constrained to first‑derivative, analytic, scale‑covariant terms (typically negligible in background evolution; bounded below in P5).

Potential class (fixed by D2):
V(Γ) = ½ m_Γ^2 Γ^2 + λ_4 Γ^4 / 4!  (quartic optional, sign chosen for stability)
Leading power and the presence of Γ^4 follow from analyticity and scale‑covariance; coefficients become U‑class parameters (MATH‑018 D1) set by D3 one‑shot anchor.

Field equations:
Γ̈ + 3H Γ̇ + V′(Γ) = 0
Friedmann:
H^2 = (8πG/3) [ ρ_b + ρ_r + ρ_Γ ]
with ρ_Γ = ½ Γ̇^2 + V(Γ), p_Γ = ½ Γ̇^2 − V(Γ).

Regimes:
• Oscillatory (m_Γ ≫ H): time‑average over many cycles gives ⟨w_Γ⟩ ≈ 0 (quadratic potential), ⟨ρ_Γ⟩ ∝ a^−3.
• Slow‑roll: ε_Γ ≡ (½ Γ̇^2)/V ≪ 1 → w_Γ ≈ −1 + 2ε_Γ.

---

## Section 2 — Linear Perturbations & Observables
Synchronous/Newtonian gauge; Γ perturbation δΓ couples to metric (Φ,Ψ).
Sound speed: for canonical Γ, c_s^2 = 1 in field rest frame, but the *effective* sound speed for oscillatory condensates time‑averages to c_eff^2 ≈ 0 → CDM‑like clustering.

Growth equation (matter‑era, sub‑horizon):
δ_m'' + [2 + (H′/H)] δ_m' − 3/2 Ω_m(a) δ_m = S_Γ(a,k)
where S_Γ encodes residual pressure/anisotropic stress from Γ; under minimal coupling and oscillatory regime S_Γ → 0.

Predicted functions:
• H(z), DA(z), DV(z) (geometry)
• fσ_8(z) (growth)
• Slip η ≡ Φ/Ψ ≈ 1 on linear scales (minimal coupling)
• α running modifications negligible at cosmological q^2 (consistency check; main α effects live at particle scales)
• GW speed c_GW = c (no non‑minimal curvature portals)

---

## Section 3 — One‑Shot Anchor and Freeze Manifest
Anchor choice (pick exactly one per D3): {Ω_m0, H0, or a_e in QED sector with proven bridge}. Once chosen, derive U‑class parameter set {m_Γ, λ_4, …} via symmetry constraints and freeze.
Emit a Freeze Manifest (YAML) with commit hash, anchor, U/T values, and seeds.

---

## Section 4 — Preregistered, Out‑of‑Sample Predictions (P4)
Targets (no further tuning):

1. fσ_8(z) curve at z ∈ {0.2…1.2}; report χ^2 vs. current RSD datasets.
2. Weak‑lensing S_8 ≡ σ_8 (Ω_m/0.3)^0.5 from Γ‑cosmology; compare to Planck prior and low‑z WL posteriors.
3. BAO distances (DV/r_s) across z bins using the same V(Γ).
4. Gravitational slip η(k,z) on linear scales (k ≲ 0.1 h/Mpc) with 1σ band.
5. c_GW = c bound satisfied by construction (record as a compliance line item).

Falsification conditions are met if any of the above require an extra fluid beyond Γ to match data at p<0.01 once systematics are accounted for.

---

## Section 5 — Nuisance Bounds & Portals
• Non‑minimal couplings ξΓ^2 R are disallowed unless they preserve c_GW=c; any allowed ξ must be symmetry‑fixed and entered as U, not fit.
• Derivative interactions L_int may renormalize the effective sound speed; bound their impact with a prior consistent with CMB damping tail.

---

## Section 6 — Pipelines, Artifacts, and Compliance
Computation pipeline:

1. Background integrator (RK45) for {Γ(t), H(t)} with stiffness handling in oscillatory era (averaging or multiple‑scales method).
2. Linear perturbations via Boltzmann code branch (Γ‑module) or bespoke fluid‑approximation with validated mapping.
3. Parameter propagation from Freeze Manifest; no retuning.

Artifacts (JSON):
result_background.json
{
"H_z": [[z, H]],
"DA_z": [[z, DA]],
"DV_over_rs": [[z, DV_over_rs]],
"Omega_m_z": [[z, Omega_m]],
"commit": "<git>",
"freeze_manifest": "path/to/manifest.yaml"
}

result_growth.json
{
"fsigma8": [[z, fs8, err_model]],
"eta_linear": [[z, eta, band_low, band_high]],
"S8": {"value": float, "band": [low, high]},
"commit": "<git>",
"freeze_manifest": "path/to/manifest.yaml"
}

Config (YAML):
cosmology_config.yaml
anchor: Omega_m0
Omega_m0: 0.315
H0: 67.4
potential:
type: quadratic_plus_quartic
m_Gamma: 1.0e-27   # eV (example placeholder, set by anchor)
lambda4: 0.0
integration:
z_max: 1100
method: rk45
tol_abs: 1e-9
tol_rel: 1e-9
perturbations:
fluid_mapping: oscillatory_average
kmax_linear: 0.1  # h/Mpc
outputs: [fsigma8, eta]

Compliance footer (paste into dependent modules):
□ Compliance MATH‑018/019/020. □ One‑shot anchor used and frozen. □ No continuous exponents. □ Preregistered targets set. □ JSON artifacts emitted. □ c_GW=c satisfied.

End of COSMO‑Γ‑000 v1.0


