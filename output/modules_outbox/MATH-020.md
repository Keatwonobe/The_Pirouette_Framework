---
id: MATH-020
title: "Non‑Perturbative Solvers"
version: 1.0
status: Normative (global)
parents: [MATH‑018, MATH‑019]
children: []
summary: "Purpose
Provide concrete, reproducible procedures to compute Pirouette predictions beyond perturbation by (A) solving the soliton echo problem that generates lepton a_ℓ non‑perturbatively and (B) running a coarse‑graining renormalization group (RG) flow on (Γ,K) to expose UV/IR structure, confinement‑like behavior, and gravity‑limit phenomenology.

Scope
• Observables: a_ℓ (ℓ∈{e,μ,τ}), muonium hyperfine Δν, running α(q²) corrections, EDM suppression checks, and ratio tests (hadronic insulation).
• Outputs are used by the Preregistered Prediction Docket (MATH‑018 P4) and must comply with Dictionary mappings (MATH‑019)."
module_type: core-mathematics
scale: universal
engrams:
keywords: []
uncertainty_tag: Foundational
---

A) SOLITON ECHO SOLVER (FEM/SPECTRAL)

A1 — Model Statement
Goal: compute the Pauli term coefficient κ_ℓ in the presence of a topological defect (“wound channel” with index T) and background fields (Γ,𝔉). Then a_ℓ=κ_ℓ/2.

Fields & Equations (referencing MATH‑019):
• Dirac sector: (iγ^μ D_μ − m_ℓ − Σ_Γ[Γ] − Σ_T[T])Ψ = 0
• Γ‑sector (static background or relaxed field): −□Γ + f′(Γ) + 𝒮(Γ,𝔉,Ψ)=0 with f constrained by MATH‑018 D2.
• Gauge/background: F_{μν} from 𝔉 with external probe B to extract κ via linear response.

A2 — Domain & Symmetry Reductions
• Choose defect codimension and symmetry class (e.g., axial symmetry for line defects; spherical for point defects).
• Reduce to 2D/3D effective domain Ω with appropriate spin connection if curved.

A3 — Weak Formulation (Dirac + Γ)
Write the coupled weak form over Ω:
• For test spinor Φ: ⟨Φ, iγ^μ D_μΨ⟩ − m_ℓ⟨Φ,Ψ⟩ − ⟨Φ, (Σ_Γ+Σ_T)Ψ⟩ = 0
• For test scalar η: ⟨∇η,∇Γ⟩ + ⟨η f′(Γ)⟩ + ⟨η 𝒮(Γ,𝔉,Ψ)⟩ = 0

A4 — Boundary Conditions
• Outer boundary ∂Ω: absorbing/silver‑Müller type for fermion; Neumann (∂_nΓ=0) for Γ; gauge potential fixed to generate infinitesimal B.
• Core boundary: topology enforced by holonomy condition around the defect; discrete index T ∈ ℤ fixes twist/phase.

A5 — Discretization & Elements
• Mesh: adaptive tetra (3D) or tri (2D axisymmetric) with near‑core refinement; grading factor ≤ 0.25 per level.
• Elements: Hermite or higher‑order Lagrange for Γ (P2+); compatible spinor elements for Dirac (e.g., mixed formulation or spectral spinor basis on subdomains).

A6 — Linearization & Solver Stack
• Nonlinear Picard or Newton‑Krylov with line search.
• Linear solves via preconditioned GMRES; ILU/AMG for scalar block; block preconditioners for Dirac block.

A7 — Extraction of κ (Linear Response)
• Apply probe B→B+δB; compute induced current and spin density; fit σ^{μν}F_{μν} coefficient.
• Alternative: compute two‑point function and project onto Pauli form factor F_2(q²→0). Then κ=F_2(0).

A8 — Convergence & Certification
• h‑refinement study: three meshes with DOF growth ~×4; require |Δκ|/κ < 1e‑3 between last two.
• p‑refinement cross‑check where feasible.
• Residual norms < 1e‑8; boundary reflection error < 1e‑4 (measured by energy leakage).

A9 — Uncertainty & Error Budget
• Discretization: from h/p study.
• Topology choice: if multiple T classes admissible, report discrete spread (do not average continuously).
• Parameter propagation: from frozen U,T per MATH‑018 D3.

A10 — Outputs (Artifact Schema)
result_soliton.json
{
"observable": "a_l",
"lepton": "muon|electron|tau",
"kappa": float,
"a_l": float,
"T_index": int,
"mesh_dofs": int,
"residual_norm": float,
"h_refinement_ratio": [float,float],
"err_discretization_frac": float,
"commit": "<git-hash>",
"freeze_manifest": "path/to/manifest.yaml"
}

Config Template (YAML)
soliton_config.yaml
anchor: ae|amu  # per D3
lepton: e|mu|tau
symmetry: axial|spherical
T_index: 1
mesh:
type: tetra
refinement_core: 4
grading: 0.25
solver:
nonlinear: newton
tol_residual: 1e-8
probe:
B0: 1e-6
method: pauli_form_factor

---

B) RG COARSE‑GRAINING ON (Γ,K)

B1 — Flow Definition
Let couplings g ≡ {λ_Γ, c_K, …}. Define coarse‑graining at scale b>1 by averaging Γ over blocks and recomputing effective action S_eff[Γ,K]. Extract β_i ≡ d g_i/d ln μ via matching of 2‑point and 4‑point vertices.

B2 — Numerical Scheme
• Lattice Ω_L with spacing a; block‑spin transform by factor b=2.
• Monte‑Carlo or deterministic quadrature for vertex extraction; stochastic estimator variance ≤ 1e‑3.
• Integrate flows with adaptive RK45 in ln μ.

B3 — Fixed Points & Phases
• Solve β(g*)=0; compute stability matrix M_ij=∂β_i/∂g_j|_{g*}.
• Identify UV/IR fixed points; relevant/irrelevant directions; map phases (free, confined‑like, gravitational‑limit).

B4 — Observables from Flow
• Running α(q²): compute Δα_Pir(q²) via vacuum polarization kernels along flow.
• EDM suppression: ensure CP‑even classes keep d_e at zero to leading order; quantify next‑order via irrelevant operator scaling.
• Ratio stability: confirm hadron‑insulating ratios R remain scale‑stable within tolerance.

B5 — Outputs (Artifact Schema)
result_rg.json
{
"beta_traj": [{"mu": float, "g": {"lambda_G": float, "c_K": float, "...": float}}],
"fixed_points": [{"name":"UV","g":{...},"eigs":[...]},{"name":"IR",...}],
"alpha_running": [{"q2": float, "Delta_alpha_Pir": float}],
"edm_bound": {"de_abs_max": float, "order": "leading|next"},
"ratio_R": {"value": float, "scale_variation": float},
"commit": "<git-hash>",
"freeze_manifest": "path/to/manifest.yaml"
}

Config Template (YAML)
rg_config.yaml
lattice:
L: 128
a: 1.0
block:
factor: 2
mc:
sweeps: 1_000_000
seed: 1337
integrator:
method: rk45
tol_abs: 1e-8
tol_rel: 1e-8

---

C) REPRODUCIBILITY & COMPLIANCE

C1 — Freeze Manifest Hooks
All runs must reference a single Freeze Manifest (MATH‑018 D3/P2). Changing anchors or priors invalidates prior artifacts.

C2 — Environment Lock
Record compiler/interpreter versions; dump an environment lockfile (e.g., Python requirements.txt + exact BLAS/LAPACK info) and OS kernel version.

C3 — Ablations & Model Checks
Run (i) full model, (ii) no‑portal, (iii) free‑fit powers (diagnostic only). Report AIC/BIC/Bayes factors (MATH‑018 D5).

C4 — Benchmarks
• QED check: reproduce Schwinger limit numerically to 6+ significant digits in the perturbative limit.
• Mesh sanity: vacuum case recovers κ→α/π as B→0.

C5 — Compliance Footer (to paste in dependent modules)
□ References MATH‑018/019/020. □ Freeze Manifest linked. □ Config YAML archived. □ JSON artifacts emitted. □ Ablations reported. □ Benchmarks passed.

End of MATH‑020 v1.0

