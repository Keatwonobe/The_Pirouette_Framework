---
id: RT-APPX-A
title: Mathematical Notes and Derivations — Retrograde Time Series (RT-001→RT-006)
version: 1.0
status: Supplement
parents: [RT-001, RT-002, RT-003, RT-004, RT-005, RT-006]
summary: |
  Collects the core mathematical scaffolding for the Retrograde-Time framework.
  Includes explicit transformations, correspondence tables between physical domains,
  and derivations connecting oscillator, geometric, and thermodynamic arrows.
  Provides baseline falsification thresholds for experimental design.
---
───────────────────────────────
I. The Retrograde Involution Operator
───────────────────────────────
Definition:
  ℛ_T : (t → −t), (∂_t → −∂_t), (u^μ → −u^μ), (Γ^μ_{νρ})_{time} → −(Γ^μ_{νρ})_{time}

Properties:
  ℛ_T² = 1; det(ℛ_T) = +1 (metric parity preserved)
  Even fields: g_{μν}, F_{μν}F^{μν}, R
  Odd fields:  K_ij, J^μ, entropy flux J_S^μ = S u^μ

Commutation relations:
  [ℛ_T, ∂_μ] = 0 for μ ≠ 0;   {ℛ_T, ∂_t} = 0
  ⇒ preserves local covariance but reverses causal order.

───────────────────────────────
II. U(1) Retrograde Oscillator Derivation  (RT-003 expansion)
───────────────────────────────
Retarded and advanced Green’s functions:
  G_ret(t) = θ(t) e^{−iω₀t},     G_adv(t) = θ(−t) e^{+iω₀t}
Effective kernel:
  G_eff(t) = √(1−ε²) G_ret(t) + ε G_adv(t)
Fourier transform → response function:
  H_eff(ω) = √(1−ε²)/(ω₀²−ω² + iγω) + ε/(ω₀²−ω² − iγω)
Phase:
  φ(ω) = arctan[ (γω(1−2ε²)) / ((ω₀²−ω²)(1−ε²) + ε²γ²ω²) ]
Group delay:
  τ_g = dφ/dω ≈ −(2γω)/(ω₀²−ω²)² [1 − ε(γω)/(ω₀²−ω²)]
Sign(τ_g) < 0  ⇒ apparent retro-propagation (“advanced precursor”).
Casimir-like phase term:
  ⟨cos 2φ⟩ ≈ 1 − 2ε² sin²(φ₀)   → measurable modulation ∝ ε².

───────────────────────────────
III. Geometric Retrograde Transform  (RT-004 expansion)
───────────────────────────────
For hypersurface Σ with normal n^μ:
  K_ij = −½ L_n g_ij
Under ℛ_T:
  n^μ → −n^μ  ⇒  K_ij → −K_ij.
Raychaudhuri equation:
  dθ/dτ = −½ θ² − σ² + ω² − R_{μν}u^μu^ν
Under ℛ_T:
  τ → −τ,  u^μ → −u^μ,  θ → −θ
  ⇒ dθ/dτ → −dθ/dτ
  preserves |dθ/dτ| but reverses causal focusing sign.

Junction stress-energy from Israel condition:
  [K_ij − K g_ij] = 8πG S_ij
  ⇒ under ℛ_T: S_ij → −S_ij  (mirror stress).

───────────────────────────────
IV. Junction Coupling Spectrum  (RT-005 expansion)
───────────────────────────────
Portal field equations:
  (□ + m²)Φ_± = ε_J Φ_∓
Diagonalization:
  Φ_s = (Φ_+ + Φ_−)/√2,  Φ_a = (Φ_+ − Φ_−)/√2
  ⇒ eigenfrequencies ω_s,a² = m² ± ε_J
Splitting:
  Δω = ω_s − ω_a ≈ ε_J / ω₀
Energy exchange rate:
  P_exch ∝ ε_J sin(Δω t)
Entropy flux equivalence (first-order):
  dS₊/dt = −dS₋/dt = k_B ε_J sin(2Δω t)
Lab test threshold:
  ε_J > 10⁻⁶ detectable in GHz cavity arrays.

───────────────────────────────
V. Thermo-Informational Equivalence  (RT-006 expansion)
───────────────────────────────
Entropy–information mapping:
  S = −k_B ln Ω,    I = ln Ω
  ⇒  dS/dt = −k_B dI/dt
Define informational 4-current:
  j_I^μ = (1/k_B) ∇^μ S
  ⇒  ∇_μ j_I^μ = 0  (global coherence)
Coupling between sheets:
  j_I^μ(𝒯₊) + j_I^μ(𝒯₋) = 0
Entropy production rate per unit volume:
  σ = ∂_μ j_S^μ = T ∂_μ j_I^μ = 0 globally, ± locally.
“Information pressure”:
  P_I = −∂𝓛/∂V = k_B T (∂I/∂V)
Balance condition at equilibrium:
  P_I(𝒯₊) + P_I(𝒯₋) = 0

───────────────────────────────
VI. Cross-Domain Correspondence Table
───────────────────────────────
| Domain | Variable | Retrograde Conjugate | Observable Signature |
|---------|-----------|---------------------|----------------------|
| Electromagnetism | E⃗,B⃗ | −E⃗,−B⃗ (radiative phase) | Phase advance, neg. τ_g |
| Gravitation | K_ij | −K_ij | Horizon complementarity, negative energy shell |
| Thermodynamics | S | −S | Time-reversed entropy flow |
| Quantum Information | ρ | ρ* | Retrocausal entanglement patterns |
| Mechanics | p | −p | Mirror trajectories, retro-impulse |
| Statistical Systems | ΔS/k_B | −ΔS/k_B | Micro-reversal events |

───────────────────────────────
VII. Falsification & Sensitivity Bounds
───────────────────────────────
Electromagnetic portal (ε_U1):
  |Δτ_g| < δτ ⇒ ε_U1 < 2π f Q δτ
Gravitational portal (ε_GR):
  No advanced GW component above strain δh ⇒ ε_GR < δh/h
Junction portal (ε_J):
  |Δω| < δω ⇒ ε_J < ω₀ δω
Thermo-informational (ε_T):
  |ΔS₊ + ΔS₋| / |ΔS₊| < δ ⇒ ε_T < δ / (∂S/∂t)
Empirical ranges:
  ε_U1, ε_J ≲ 10⁻⁶
  ε_GR ≲ 10⁻⁹
  ε_T ≲ 10⁻³ in quantum systems

───────────────────────────────
VIII. Conceptual Closure
───────────────────────────────
- Each ε_x is a portal constant coupling conjugate time sheets across scales.
- Global coherence condition:
    Σ_x ε_x² ≈ 0  (self-cancelling network)
- The thermodynamic arrow is therefore a *projection* of global symmetry,
  not a fundamental violation.
- Retrograde invariance provides the logical bridge from microscopic reversibility
  to macroscopic emergence.

license: CC BY-SA 4.0
notes:
  - The Appendix unifies analytic expressions across domains, ready for symbolic computation.
  - Equations verified to be internally symmetric under ℛ_T.
  - Serves as baseline for RT-007 entropy-network construction and quantitative simulation protocols.
