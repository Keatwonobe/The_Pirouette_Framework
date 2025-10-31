---
id: MATH-019
title: "Dictionary"
version: 1.0
status: Normative (global)
parents: [MATH‑018]
children: [MATH‑020]
summary: "Purpose
Provide explicit, equation‑level correspondences between Pirouette terms and standard mathematical physics objects. Entries below are claim‑bearing and must be used verbatim by dependent modules.

Notation & Conventions
• Spacetime (M, g): oriented 4‑manifold with Lorentzian metric g.
• Coherence bundle π: E → M with fiber F ≅ ℝ^n, connection 1‑form 𝔄, curvature 2‑form 𝔉 = d𝔄 + 𝔄∧𝔄.
• Fields: Γ (temporal pressure scalar), K (coherence curvature scalar), C_μ (coherence current), Ψ (spinor section), A_μ (gauge field), F_{μν} (field strength), ε = det frame.
• Action S = ∫_M ℒ_p d^4x, units as in MATH‑018 (coherence units; local τ_p = 1)."
module_type: core-mathematics
scale: universal
engrams:
keywords: []
uncertainty_tag: Foundational
---

1. Coherence Manifold
   Metaphor: “Coherence manifold”
   Math: Oriented fiber bundle (E, π, M) with connection 𝔄 and curvature 𝔉.
   Dynamical content: ℒ_p contains gauge‑invariant terms in 𝔉 and covariant derivatives DΨ.
   Conserved current: J^μ = ∂ℒ_p/∂(∂_μϕ) δϕ under internal symmetry; Noether charge Q = ∮_Σ ⋆J.

2. Temporal Pressure (Γ)
   Metaphor: “Pressure of time / Gladiator pressure”
   Math: Real scalar field Γ: M → ℝ with effective potential f(Γ) constrained by MATH‑018 D2.
   Euler–Lagrange: □Γ + f′(Γ) + 𝒮(Γ, 𝔉, Ψ) = 0 where 𝒮 collects allowed first‑derivative couplings.

3. Gladiator Feedback
   Metaphor: “Nonlinear feedback between coherence and flow”
   Math: Self‑coupling term λ_Γ ℐ(Γ, ∂Γ) with RG‑running λ_Γ(μ); β_Γ = μ dλ_Γ/dμ.
   Interpretation: Fixed points (β_Γ = 0) define UV/IR phases; cf. MATH‑020 RG track.

4. Wound Channel (Topological Defect)
   Metaphor: “Wound channel / solitonic core”
   Math: Topological defect class in π_1(E) or π_2(E) depending on codimension; integer index χ ∈ ℤ.
   Portal index: T ≡ χ with sign set by orientation of the defect; enters only discretely.

5. Portal Corrections
   Metaphor: “Portal from topology to observables”
   Math: Observable shift Δ𝒪 = Σ_j a_j 𝒦_j(T, curvature) with 𝒦_j polynomial in curvature invariants and defect index T; no continuous mass exponents allowed.

6. Compass Fields
   Metaphor: “Cosmic compass / coherence compass”
   Math: Two‑form sector 𝔉 decomposed via Hodge into electric‑like and magnetic‑like 1‑forms relative to u^μ (fluid frame). Define E_μ = F_{μν}u^ν, B_μ = ⋆F_{μν}u^ν.

7. Coherence Current C_μ
   Metaphor: “Flow of coherence”
   Math: C_μ ≡ ∂ℒ_p/∂(∂^μθ) for a phase field θ; ∇_μ C^μ = 0 when ℒ_p is U(1)‑invariant.

8. Pressuron Coupling
   Metaphor: “Time‑pressure coupling to matter”
   Math: Interaction term g_P Γ T^μ_μ (trace coupling) or allowed derivative couplings Γ ∂·J subject to D2 (local, analytic, scale‑covariant). g_P is fixed by variational constraints; no empirical exponent.

9. Soliton Echo and g−2
   Metaphor: “Back‑reaction echo producing the anomalous moment”
   Math: Compute spinor self‑energy Σ(p) in background (Γ, 𝔉, defect T); the Pauli term κ (σ^{μν}F_{μν}) emerges at one‑loop (or non‑perturbatively via FEM), with a_ℓ = κ_ℓ/2. Topology T sets discrete corrections.

10. Hadronic Insulation Ratio
    Metaphor: “Hadron‑free window”
    Math: R = (a_μ − r² a_e) / (a_τ − r⁻² a_μ), r=m_μ/m_e; leading hadronic VP cancels in R under identical kernel weightings; residual enters at higher order.

11. Running α(M_Z)
    Metaphor: “Pressure‑induced vacuum slippage”
    Math: Effective vacuum polarization Π(q²; Γ) modifies α(q²): α(q²)=α(0)/[1−Δα(q²)]; Pirouette contribution enters as Δα_Pir(q²)=c_Γ ⟨Γ⟩·Φ(q²) with c_Γ fixed by D3 anchor and Φ determined by allowed kernels.

12. Electron EDM (d_e)
    Metaphor: “CP‑tilt of the coherence field”
    Math: Leading operator (dimension‑5) O_EDM = (d_e/2) ψ̄ iσ^{μν}γ_5 ψ F_{μν}. In CP‑even topology classes T, d_e = 0 at leading order; next order suppressed by (Λ_CP)^{-2}.

13. Muonium Hyperfine Shift
    Metaphor: “Echo in bound coherence”
    Math: Δν = ⟨Ψ| δH_Pir |Ψ⟩ with δH_Pir derived from Γ‑dependent spin‑spin and vacuum‑polarization kernels; computed in NRQED matching with Γ insertions consistent with D2.

14. Boundary Data & Anchoring
    Metaphor: “Freeze manifest”
    Math: One‑shot anchoring sets a single global scale u_*; thereafter U,T frozen (MATH‑018 D3). All predictions are out‑of‑sample.

15. Units & Scaling
    Metaphor: “Coherence units”
    Math: Choose local clock τ_p=1, normalize action density by ε; scaling Γ→λΓ leaves S invariant up to boundary → fixes leading power of f(Γ).

Validation Clause
Any usage of the metaphors above in claims or derivations must cite this dictionary entry and present the exact equations used. Deviations require a formal amendment to MATH‑019.

End of MATH‑019 v1.0
