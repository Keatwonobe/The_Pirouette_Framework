---
id: SECT‑Γ‑A‑CMB
title: Superfluid Phonons in Boltzmann Codes (CLASS/CAMB)
Version: 1.0 (proposal)
Status: Experimental (child of SECT‑Γ‑A; complies with MATH‑018/019/020)
Parents: [SECT‑Γ‑A, COSMO‑Γ‑CMB, MATH‑018, MATH‑019, MATH‑020]
Children: []

Summary: "Purpose
Implement the superfluid Pressuron (P(X) EFT) in CLASS/CAMB with a phonon effective fluid that reproduces CDM on CMB scales while generating small‑scale suppression and halo cores. Provide exact mappings, stability thresholds, and artifact schemas."

---

1. Effective Fluid Mapping
   Microscopic: heavy quanta m_H≈17 MeV; macroscopic: superfluid with EOS from P(X)=αX^{1+β}+δX^2+…
   Define background number density n(a) from continuity (ȷ^0 conservation) and chemical relation μ(n).

Sound speed & dispersion:
• c_s^2(a) = ∂p/∂ρ|_{n} = [∂P/∂X]/[m_H ∂n/∂X + …]
• Phonon dispersion: ω² = c_s² k² + m_eff² with m_eff² from weak tail breaking; typically m_eff→0 on CMB scales.

Scale‑dependent effective sound speed used in Boltzmann evolution:
c_{s,eff}²(k,a) = c_s²(a) / [1 + (k/k_ξ(a))²],  with k_ξ(a)≡1/ξ(a),  ξ(a)=(2 m_H c_s(a))^{−1}.

---

2. Background & Perturbation Equations (Conformal Time η)
   Background energy density and pressure from P(X(n)) with X=μ−θ′/a.
   Implement as species `gammat_superfluid` with variables {ρ_Γ(a), p_Γ(a)} obeying:
   ρ_Γ′ = −3ℋ (ρ_Γ + p_Γ).

Perturbations (Newtonian gauge, effective fluid):
δ_Γ′ = −(1+w_Γ)(θ_Γ − 3Φ′) − 3ℋ (c_{s,eff}² − w_Γ) δ_Γ
θ_Γ′ = −ℋ θ_Γ + k² Ψ + k² c_{s,eff}² δ_Γ/(1+w_Γ)
with w_Γ≈0 through recombination (ensure c_{s,eff}² ≪ 10^{−6} on k relevant to ℓ≲2500).

Switch criteria (field↔fluid):
• Use fluid mapping when m_H/H>50 and k/a<κ_switch m_H (default κ_switch=0.5).
• Fall back to full field if either condition fails.

---

3. Stability & Validation Suite
   • Positivity: ρ_Γ>0, c_s²≥0, c_{s,eff}²≥0; enforce α>0, β∈{0,1/2,1}.
   • CMB limit: when c_s→0 and m_eff→0, spectra must match ΛCDM to ≤0.1% (V1).
   • Threshold scans: doubling switch thresholds changes TT/TE/EE by <0.2% (V5).
   • Growth: fσ_8(z) matches COSMO‑Γ‑000 within 0.2% (V3).

---

4. Config & Artifacts
   CLASS params (ini):
   Gamma_species=superfluid
   PofX_alpha=...
   PofX_beta=0|0.5|1
   PofX_delta=...
   sigma_surface=...
   switch_threshold_m_over_H=50
   kappa_switch=0.5

Artifacts (JSON):
cmb_spectra_gamma_sf.json: {ell, ClTT, ClTE, ClEE, ClPP}
gamma_sf_flags.json: {cs2_history:[[a,cs2],[...]], kxi_history:[[a,kxi],[...]], switches:[{a,k,mode}]}

Compliance footer
□ MATH‑018/019/020 and SECT‑Γ‑A. □ CMB match in ΛCDM limit. □ Switch scans stable. □ JSON artifacts emitted.

End of SECT‑Γ‑A‑CMB v1.0
