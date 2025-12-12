---
id: SECT‑Γ‑A‑HALO
title: Superfluid Hydro & Surface Tension
Version: 1.0 (proposal)
Status: Experimental (child of SECT‑Γ‑A; complies with MATH‑018/019/020)
Parents: [SECT‑Γ‑A, COSMO‑Γ‑HALO, COSMO‑Γ‑MERGE, MATH‑020]
Children: []
Summary: "Purpose
Replace scalar‑field halo solvers with a superfluid hydrodynamics solver that includes surface tension and healing‑length physics. Produce cored profiles, vortex predictions, and merger offsets consistent with SECT‑Γ‑A."
---

1. Equations (Newtonian, irrotational + vortices)
   Variables: density n, phase θ (velocity v=∇θ/m_H), pressure p=P(X), with X=μ−∂_t θ−v²/2−Φ.
   Continuity: ∂_t n + ∇·(n v)=0
   Euler (with quantum pressure Q and surface tension σ):
   ∂*t v + (v·∇)v = −∇h(n) − ∇Φ + ∇Q/m_H + (σ/ρ) κ_s  n̂*⊥  (interface curvature term)
   where Q= −(κ/2) ∇²√n/√n and κ_s is mean curvature of iso‑n surfaces.
   Poisson: ∇²Φ=4πG(ρ_b + m_H n)

Vortices: quantized circulation ∮ v·dl = 2πℓ/m_H, ℓ∈ℤ; evolve via HVBK‑like mutual‑friction terms (optional) with coefficient set by P(X) parameters.

---

2. Stationary Halos (Core Profiles)
   Spherical equilibrium: ∇p = −ρ ∇Φ with p=P(X(n)).
   Numerics: 1D shooting/spectral or FEM with regularization by Q and σ; residual <1e‑10.
   Outputs: (r_c, ρ_0, Σ_0, V_c(r), κ(θ)); vortex stability threshold vs. Ω.

---

3. Rotating Systems & Vortex Predictions
   Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ); vortex lattice spacing d_v ∝ √(c_s/Ω).
   Observables: non‑circular flows in IFU maps; wiggles in stellar‑stream power spectra at k~1/d_v.

---

4. Mergers (Offsets Without σ/m)
   Hydro‑Poisson + interface tracking (level set). Effective drag from interface work and phonon radiation → (σ/m)_eff prediction as a function of (v_rel, n, σ, ξ).

---

5. Configs & Artifacts
   YAML config (excerpt):
   superfluid:
   PofX: {alpha: ..., beta: 0|0.5|1, delta: ...}
   sigma_surface: ...
   kappa_quantum: ...  # coefficient of Q term
   m_H_MeV: 17.0
   solver:
   scheme: FV+HLLC | spectral
   mesh: {N_r: 2048, grading: 0.25}
   tol: 1e-10
   outputs:
   save: [density, velocity, vortex_map, Vc, kappa]

JSON artifacts:
halo_sf.json: {rc, rho0, Sigma0, Vc_profile, vortex_thresholds, …}
merge_sf.json: {Delta_x, sigma_over_m_eff, shock_Mach, …}

Compliance footer
□ MATH‑018/019/020 and SECT‑Γ‑A. □ One‑shot anchor inherited; no retuning. □ Surface tension & healing length active. □ JSON/YAML artifacts emitted.

End of SECT‑Γ‑A‑HALO v1.0
