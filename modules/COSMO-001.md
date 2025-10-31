---
id: COSMO‑Γ‑HALO
title: "Γ‑Soliton Halos: Cores, Rotation Curves, and Lensing"
Version: 1.0 (proposal)
Status: Experimental (complies with MATH‑018/019/020; child of COSMO‑Γ‑000)
Parents: [MATH‑018, MATH‑019, MATH‑020, COSMO‑Γ‑000]
Children: [COSMO‑Γ‑MERGE]

Summary: "Purpose
Model galactic and cluster halos as stationary Γ‑condensate (soliton) solutions labeled by topological index T ∈ ℤ. Derive core properties, rotation curves V_c(r), and lensing convergence κ(θ) from the same potential V(Γ) fixed in COSMO‑Γ‑000, without introducing particulate DM. Provide reproducible FEM/spectral pipelines and falsifiable core–scaling predictions.

Summary of Claims
• A family of stationary solutions Γ_T(r) exists for allowed T, generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers and NFW‑like outer slopes.
• A near‑constant central surface density Σ_0 ≡ ρ_0 r_c emerges from the Γ equations across dwarf → L* → cluster scales, up to weak T‑dependent scatter.
• Lensing κ(θ) maps from Γ alone reproduce observed Einstein radii at fixed baryon fraction when V(Γ) is the same as in COSMO‑Γ‑000 (D3 freeze honored)."

---

## Section 1 — Equations and Reductions
Geometry: static, spherically symmetric spacetime; Newtonian limit for galaxies, weak‑field lensing for clusters.
Fields: Γ(r) stationary profile; optional small vector/gauge probe only for diagnostics.

Effective equations (Newtonian limit):
(1) Γ″ + (2/r) Γ′ − dV/dΓ = 0  \  (stationary field balance)
(2) ∇²Φ = 4πG (ρ_b(r) + ρ_Γ(r))
(3) ρ_Γ(r) ≡ ½(Γ′²) + V(Γ) − V(Γ_∞)   (subtract vacuum)
Boundary conditions:
• Core regularity: Γ′(0)=0, finite Γ(0)
• Asymptotic vacuum: Γ(r→∞) → Γ_∞ (minimum of V)
• Topology: T fixes allowed winding class; implemented by core holonomy or sign constraints on Γ(0).

Rotation curve and lensing:
M(<r) = 4π ∫*0^r ρ_tot(r′) r′² dr′ ;  V_c(r)=√[GM(<r)/r]
κ(θ) = Σ(θ)/Σ_crit with Σ(θ)=∫ ρ_tot dl;  Σ_crit = (c²/4πG) (D_s/(D_d D*{ds}))

---

## Section 2 — FEM/Spectral Solver (MATH‑020 A)
Domain: r ∈ [0, R_max], with R_max ≫ r_vir; compactify via x=r/(1+r).
Weak form: multiply (1) by test η, integrate over volume with weight r² and apply integration by parts.
Discretization: 1D spectral (Chebyshev) or 2D axisymmetric FEM for non‑spherical extensions.
Nonlinearity: Newton‑Krylov; line search; tolerance 1e‑10 for residual.
Mesh/points: N≥512 (spectral) or graded FEM with ≥4 core refinements.

Outputs (per solution):
• Core radius r_c (e.g., radius where ρ_Γ drops to ρ_0/2)
• Central density ρ_0 = ρ_Γ(0)
• Surface‑density product Σ_0 = ρ_0 r_c
• V_c(r) curve; maximum V_max and radius r_max
• κ(θ) profile and Einstein radius θ_E (if any)
• Discrete label T and stability flag

---

## Section 3 — Scaling Laws & Testable Predictions
P1 — **Core surface‑density locus**
Prediction: Σ_0 ≡ ρ_0 r_c ≈ Σ_* (nearly constant) across halo masses for fixed V(Γ); weak T‑indexed scatter ΔΣ/Σ_* ≲ 0.2.

P2 — **Cusp–core diversity**
Variation of T and baryon compression leads to a controlled family of inner slopes; reproduce dwarf diversity without stochastic sub‑grid feedback.

P3 — **Baryon–halo coupling**
Adiabatic contraction modifies r_c and V_max along a one‑parameter track predictable from Γ’s equation; publish a single‑track map relating stellar surface density to halo r_c.

P4 — **Lensing mass without particulate DM**
For clusters, κ(θ) from Γ + gas reproduces observed θ_E at given baryon fraction and total mass; offsets in mergers handled in COSMO‑Γ‑MERGE.

Falsification: failure to reproduce the Σ_0 locus or the V_c(r) diversity with the frozen V(Γ) invalidates Γ‑halo unification.

---

## Section 4 — Pipelines, Artifacts, and Configs
Artifacts (JSON)
halo_result.json
{
"T_index": int,
"rc": float,
"rho0": float,
"Sigma0": float,
"Vmax": float,
"r_Vmax": float,
"theta_E": float,
"kappa_profile": [[theta, kappa]],
"Vc_profile": [[r, Vc]],
"stability": "stable|unstable",
"commit": "<git>",
"freeze_manifest": "path/to/manifest.yaml"
}

Configs (YAML)
halo_config.yaml
anchor: from_COSMO_G0_freeze
potential:
type: quadratic_plus_quartic
m_Gamma: ${from_freeze}
lambda4: ${from_freeze}
geometry:
R_max_kpc: 300
baryons:
profile: burkert|hernquist|none
params: {rho0_b: 0.02, r_b: 5.0}
solver:
scheme: spectral
N_points: 1024
tol: 1e-10
outputs:
compute_kappa: true
distances: {Dd_Mpc: 800, Ds_Mpc: 1800, Dds_Mpc: 1200}

Compliance footer
□ Compliance MATH‑018/019/020 and COSMO‑Γ‑000. □ One‑shot anchor inherited; no retuning. □ Σ_0 locus reported. □ JSON/YAML artifacts emitted. □ Stability checked. □ Lensing computed when applicable.

End of COSMO‑Γ‑HALO v1.0
