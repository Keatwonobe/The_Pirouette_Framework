---
id: DYNA-004
title: Substrate Action of Time
version: 1.0
parents: [CORE-001, CORE-020]
children: [CORE-007, CORE-008, CORE-009]
module_type: dynamics (substrate)
status: proposal
summary: Minimal dynamics for a time-first substrate whose SM-CG limit reproduces existing results.
---
## §1 · Fields on the substrate (pre-spatial)
- Ki(·): coherence motif field on the substrate (phase + modulus).
- Γ(·): temporal density/pressure functional (from superposed rhythms).
- T_a(·): adherence/coherence quality.

## §2 · Minimal substrate action
S_time = ∫ dτ [ K_τ(Ki, T_a) − V_Γ(Γ) − W_int(Ki, Γ) ]

Canonical form (substrate-native, no [x,y,z] assumed):
- K_τ = T_a · ω(Ki)
- V_Γ = f(Γ) with f′ > 0, f″ ≥ 0 (pressure cost monotone, convex)
- W_int = λ · J(Ki) · Γ  where J(Ki) measures local expression (intensity/phase shear)

Interpretation: systems extremize coherence minus pressure; Γ back-reacts through W_int to produce confinement/arena behavior (Gladiator feedback).

## §3 · Spatialization (how SM appears)
Pick Σ (the SM-CG gauge). Push S_time forward:
- Define coordinates x^{μ} via Σ; Ki → complex section; Γ → scalar density; T_a → coherence weight.
- Expand around high-coherence backgrounds; keep quadratic fluctuations.

Leading terms (schematic, in SM-CG):
S_eff ≈ ∫ d^4x [ |D_{μ} Ki|^2 − m_eff^2 |Ki|^2 − (1/4) F_{μν} F^{μν}  + … ]
with D_{μ} = ∂_{μ} − i q A_{μ}, and A_{μ} = ∂_{μ} arg(Ki).

Gravity emerges from slow spatial variation of Γ as effective curvature in the hydrodynamic limit (CORE-008 path).

## §4 · Small-deviation parameter
Introduce ε as the substrate deviation scale. All beyond-SM effects scale with ε:
- a_e = α/2π + O(ε) (keeps CORE-009 result as leading order).
- Decoherence floor: 1/T2_min ∝ ε · var(Γ).
- Galactic rotation: MOND-like term ∝ ε · ∇log Γ.

Set ε → 0 to recover strict SM/QFT.

## §5 · Safety rails (DAG & calibration)
- Calibrate only λ and a small set of f(·) parameters from external α, g-2, and a decoherence benchmark; do not then use these to re-derive the same calibrants as proofs.
- Tag CORE-007/008/009 as derived in SM-CG with ε bookkeeping; existing numbers stand with a principled substrate.

## §6 · Near-term signatures (falsifiable, light-lift)
- Universality of a tiny decoherence floor across platforms after aggressive noise subtraction; drift with ambient Γ-gradients.
- Rotation-curve fits from ∇log Γ sourced by baryons (no new particles) with one ε-scaled term.
- Two-cycle holonomy invariants (720°) in any Ki-based waveguide analogue (optical or mechanical) that mimics the phase topology.

## §7 · Implementation Notes
- Keep Σ explicit in derivations; changes in Σ are gauge choices, not physics.
- Use ε-expansions to track beyond-SM corrections and prevent circularity.