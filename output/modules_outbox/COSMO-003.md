---
id: COSMO‑Γ‑CMB
title: Boltzmann Implementation & Coincidence Mechanism for Γ (Pressuron)
Version: 1.0 (proposal)
Status: Experimental (complies with MATH‑018/019/020; child of COSMO‑Γ‑000)
Parents: [MATH‑018, MATH‑019, MATH‑020, COSMO‑Γ‑000]
Children: []

Summary: "Purpose
Implement Γ in a Boltzmann code (CLASS/CAMB) to predict CMB TT/TE/EE spectra and lensing consistently with COSMO‑Γ‑000. Address quantum–to–cosmic bridging (pressuron microphysics) and outline a symmetry‑compliant route to the coincidence problem."

---

## Section 1 — Microphysics: What is the Γ‑quantum?
Interpretation: Γ is a classical, coherently oscillating scalar whose quanta (“pressurons”) have mass m_Γ. A galactic‑scale ‘condensate’ need not be a thermal BEC; the cosmological mechanism is **misalignment**: Γ starts displaced from its minimum in the early universe; Hubble friction freezes it (Γ̇≈0) until H≈m_Γ, after which Γ oscillates and time‑averages to a **pressureless fluid**.

Key points:
• Coherence length is set by the classical field, not the Compton wavelength; large‑scale homogeneity is from inflationary initial conditions and Hubble friction.
• Number conservation is approximate only if an accidental shift symmetry yields an adiabatic invariant; otherwise treat Γ as a condensed classical field.
• If m_Γ≈O(MeV), Γ begins oscillating extremely early (T≫MeV); it behaves like CDM thereafter. Late‑time DE behavior requires a shallow tail in V(Γ) that slows the background today (see Sec. 5).

---

## Section 2 — Background (CLASS/CAMB hooks)
Equations:
Γ̈ + 3HΓ̇ + V′(Γ)=0,  H² = (8πG/3)(ρ_r+ρ_b+ρ_Γ),  ρ_Γ=½Γ̇²+V, p_Γ=½Γ̇²−V.
Implementation:
• New species gammat with params {m_Gamma, lambda4, V_tail_parameters, Gamma_ini, dGamma_ini}.
• Integrate Γ with stiff solver or averaged fluid mapping when m_Γ≫H (toggle by μ≡m_Γ/H threshold).
• Match to effective CDM when oscillatory; keep exact background if slow‑rolling.

Config (CLASS‑style):

```
# cosmology.ini
Omega_b=0.049
Omega_cdm=0.000   # replaced by Gamma sector
Omega_gammat=auto # computed from (Gamma_ini, m_Gamma, V)
H0=67.4
Gamma_potential=quadratic_plus_tail
m_Gamma_eV=1.7e7
lambda4=0.0
V_tail_type=exp_shallow
V_tail_mu=1.0e-33  # eV
Gamma_ini=1.2e18   # in reduced‑Planck units
Gamma_ini_prime=0.0
use_averaging_threshold=50.0   # switch when m/H>50
```

---

## Section 3 — Linear Perturbations
Gauge: synchronous or Newtonian; below in Newtonian.
Variables: δΓ, θ_Γ (velocity potential), metric Φ,Ψ.
Full field approach:
δΓ̈ + 3H δΓ̇ + (k²/a² + V″) δΓ = 4 Γ̇ Φ̇ − 2 V′ Φ
Poisson: k²Φ = 4πGa² δρ_total.

Fluid mapping (oscillatory regime):
Treat Γ as an effective fluid with
w_Γ≈0,
c_s,eff² ≈ ⟨(k²/a²)/(4m_Γ² + (k²/a²))⟩  → 0 on large scales; include small scale suppression if needed.
Evolution:
δ̇_Γ = −(1+w_Γ)(θ_Γ − 3Φ̇) − 3H(c_s,eff² − w_Γ)δ_Γ
θ̇_Γ = −H θ_Γ + k²Ψ + k² c_s,eff² δ_Γ/(1+w_Γ).

Implementation notes:
• Provide both solvers and switch based on m/H and k/a relative to m_Γ.
• Ensure tight‑coupling era stability; run with integrator safeguards (step rejection, positivity checks).

CLASS file touchpoints:
• background.c/.h: add gammat background; fast‑averaging map.
• perturbations.c/.h: add Γ equations; fluid mapping branch.
• input.c: new parameters and defaults; prior boxes per MATH‑018.
• thermodynamics.c: unchanged.
• transfer.c / spectra.c: standard.

---

## Section 4 — Validation & Sanity Tests
V1 ΛCDM limit: m_Γ/H→∞, V_tail→0 ⇒ spectra match CDM to ≤0.1%.
V2 DE‑limit: tune V_tail so that today w_Γ≈−1 with Ω_Γ≈0.7; reproduce TT/TE/EE within Planck contours when Ω_b, n_s, A_s fixed.
V3 Growth: compute fσ_8(z) and ensure consistency with COSMO‑Γ‑000 outputs.
V4 Lensing: C_ℓ^{ϕϕ} within current uncertainties.
V5 Robustness: switch threshold variation by ×2 changes spectra < 0.2%.

Artifacts:
• cmb_spectra.json: {ell, ClTT, ClTE, ClEE, ClPP}
• growth_from_CLASS.json: {z, fσ8}
• logs/flags: solver switches, averaging usage, step rejections.

---

## Section 5 — Coincidence Problem: Symmetry‑Compliant Tail
Goal: explain ρ_DM ~ ρ_DE today without tuning.
Mechanism: **tracker/attractor tail** appended to quadratic core of V(Γ), consistent with D2 (analytic, local, scale‑covariant). Two options:

(1) Exponential tail (analytic):
V(Γ) = ½ m_Γ² Γ² + μ⁴ [1 − e^{−Γ/Γ_*}]  (μ≪m_Γ, Γ_*>0)
• Early: quadratic dominates → CDM‑like oscillations.
• Late: as Γ amplitude redshifts, field probes the shallow exp tail; slow‑roll sets in with tracker behavior that naturally turns on when ρ_m drops below a scale ∝ μ⁴.

(2) Cosine tail (shift‑symmetry remnant):
V(Γ) = ½ m_Γ² Γ² + μ⁴ [1 − cos(Γ/f)] with f≫M_pl, μ≪m_Γ.
• Early oscillations in quadratic; late slow‑roll near a cosine plateau triggers DE‑like phase.

Both tails are analytic and allowed by D2; their parameters (μ, Γ_* or f) are **U‑class** constants fixed by D3 one‑shot anchor in COSMO‑Γ‑000 (e.g., anchoring Ω_Γ,0) and then frozen.

Dynamical attractor evidence:
• Phase‑space (x≡Γ̇/√(6)H, y≡√(V)/√(3)H) has late‑time fixed points with 0<1+w_Γ≪1; stability shown by eigenvalues of linearized system <0.
• Coincidence arises because slow‑roll only turns on when the oscillation amplitude decays into the tail—set by μ, not by arbitrary time.

Falsification: if fitting CMB+BAO+SNe requires independent CDM and DE fluids once parameters are frozen, the unification fails.

---

## Section 6 — Preregistration Plan (CMB‑specific)
• Fix V(Γ) (choose tail type) and anchor once (Ω_Γ0 or H0) per MATH‑018 D3.
• Publish code hash, switch thresholds, and solver settings.
• Lock the target set: TT/TE/EE spectra, lensing, fσ_8(z), ISW cross‑correlation sign/magnitude.
• Report AIC/BIC versus ΛCDM and w0waCDM; include ablations (no‑tail; fluid‑map only; full field only).

Compliance footer
□ Compliance MATH‑018/019/020 and COSMO‑Γ‑000. □ One‑shot anchor used and frozen. □ No post‑hoc exponents. □ Boltzmann modifications listed. □ Validation suite defined. □ Coincidence mechanism analytic and symmetry‑compliant.

End of COSMO‑Γ‑CMB v1.0
