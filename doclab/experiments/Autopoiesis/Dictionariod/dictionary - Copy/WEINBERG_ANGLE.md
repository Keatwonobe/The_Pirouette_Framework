---
term: "Weinberg Angle"
canonical_id: "WEINBERG_ANGLE"
symbol: "θ_W"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-WEAK-001_l_from_the_temporal_triad"]
---

---
term: Weinberg Angle
canonical_id: WEINBERG_ANGLE
symbol: θ_W
aliases: [Weak Mixing Angle]
parents: [DYNA-WEAK-001_l_from_the_temporal_triad]
children: [MATH-YM-002, DYNA-COLOR-001, DYNA-Γ-004]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-WEAK-001_l_from_the_temporal_triad
      lines: "§3"
      snippet: |
        [
        \boxed{\ \sin^2\theta_W(\mu_c) ;=; \frac{g'^2}{g^2+g'^2} ;=; \frac{\rho_{\text{stiff}}}{1+\rho_{\text{stiff}}}\ }.
        ]
  editors: [writing-agent-001]
  review_log: []
triad:
  art: |
    A trinity of degenerate time-like resonances is twisted to align with the universal clock. The angle of this twist, a measure of their relative resistance to change, sets the character of the weak force.
  law: |
    At the coherence barrier scale (μ_c), the squared sine of the Weinberg angle is determined by the ratio of the SU(2) triad stiffness (K₂) to the U(1) clock stiffness (K₁), according to sin²θ_W(μ_c) = ρ_stiff / (1 + ρ_stiff), where ρ_stiff = K₂/K₁.
  philosophy: |
    The Weinberg angle is not a fundamental, tunable parameter but an emergent structural property of the medium. It mechanistically encodes the relative pliability of the temporal triad (SU(2)) versus the temporal clock (U(1)), making electroweak unification a matter of frame mechanics.
pirouette_definition: |
  The mixing angle between the neutral SU(2)_L gauge boson (W³) and the U(1)_Y gauge boson (B) that yields the physical photon and Z boson. In Pirouette, its value is fixed at the coherence barrier (μ_c) by the fundamental stiffness ratio ρ_stiff = K₂/K₁ of the temporal medium, where K₂ is the stiffness of the SU(2) triad frame and K₁ is the stiffness of the U(1) clock frame. This value at μ_c serves as the boundary condition for Renormalization Group flow to experimental energy scales.
operational_definition:
  units: dimensionless (radians or degrees)
  symbol_table:
    - name: θ_W
      meaning: Weinberg Angle
      dimensions: dimensionless
      default_range: "[0, π/2]"
    - name: ρ_stiff
      meaning: Ratio of triad-to-clock frame stiffness, K₂/K₁
      dimensions: dimensionless
      default_range: "Order(1), fixed by Resonance Atlas"
    - name: K₁, K₂
      meaning: Frame stiffness for U(1) and SU(2) fields, respectively
      dimensions: dimensionless
      default_range: "contextual"
    - name: g, g'
      meaning: Gauge couplings for SU(2) and U(1)
      dimensions: dimensionless
      default_range: "contextual; scale-dependent"
    - name: μ_c
      meaning: Coherence barrier energy scale
      dimensions: M L² T⁻² (Energy)
      default_range: "near GUT scale"
  measurement:
    procedures:
      - name: Stiffness-to-Angle RG Flow
        outline: |
          1. Select a stiffness ratio, ρ_stiff, from the Pirouette Resonance Atlas (XXP-BRIDGE-Γ-001).
          2. At the coherence scale μ_c, calculate the boundary conditions for the gauge couplings: g'(μ_c)²/g(μ_c)² = ρ_stiff. (Often K₂ is chosen as a reference, fixing both g and g').
          3. Using Standard Model one-loop (or higher) β-functions, run the fine-structure constants α₁(μ) and α₂(μ) down from μ_c to the Z-pole mass, M_Z.
          4. Compute the predicted value sin²θ_W(M_Z) = (⅗ α₁(M_Z)) / (⅗ α₁(M_Z) + α₂(M_Z)).
          5. Compare the result with high-precision experimental measurements of sin²θ_W from Z-pole observables.
        expected_signals: [A value of sin²θ_W(M_Z) matching the experimental value (≈0.231) for a specific ρ_stiff prior. A correlated sub-percent shift in the Higgs width (DYNA-Γ-004).]
        pitfalls: [Incorrect choice of μ_c. Higher-order loop corrections altering the RG flow. Priors for ρ_stiff from the Resonance Atlas being incorrect.]
context_windows:
  - module: DYNA-WEAK-001_l_from_the_temporal_triad
    excerpt: |
      The weak mixing angle at (μ_c) is **fixed** by the *triad-to-clock* stiffness ratio — a direct mechanical property of the temporal medium. (μ_c) is the **coherence-barrier energy** (from XXP-BRIDGE-Γ-001 / MATH-Γ-007). All “matching” happens here before standard RG running.
  - module: DYNA-WEAK-001_l_from_the_temporal_triad
    excerpt: |
      The **alignment energy** (\propto \lambda v^4) couples to the triad via (H^\dagger H,\Gamma^2) (DYNA-Γ-004), giving a calculable, sub-percent shift in Higgs width correlated with (\rho_{\text{stiff}}). A **joint fit** to ({\sin^2\theta_W(M_Z),,\Gamma_H,,\text{rare }H\to \ell^+\ell^-}) overconstrains (\rho_{\text{stiff}}).
poetic_connections:
  motifs: [stiffness, rotation, alignment, triad, clock, mixing]
  evocative_lines:
    - "Weak interactions are triad bookkeeping."
    - "The angle... is the ratio of how stiff time is as a triad versus as a clock."
  association_matrix:
    - [ "FRAME_STIFFNESS", 0.9 ]
    - [ "TEMPORAL_TRIAD", 0.8 ]
    - [ "HIGGS_ALIGNMENT", 0.7 ]
    - [ "COHERENCE_BARRIER", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: sin²θ_W (Weak Mixing Angle)
      domain: SM
      mapping_kind: operational
      equation_hint: |
        sin²θ_W(μ) = g'(μ)² / (g(μ)² + g'(μ)²)
      rationale: |
        The Pirouette definition is constructed to reproduce the Standard Model's weak mixing angle. The framework provides a physical origin for the ratio g'/g at a high-energy scale μ_c, but the quantity, its running, and its low-energy phenomenological role are identical to the SM parameter.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "A Pirouette-allowed stiffness ratio ρ_stiff from the Resonance Atlas predicts the experimentally measured value of sin²θ_W(M_Z) after RG evolution."
      domain: phenomenology
      falsifier: "No value of ρ_stiff consistent with Pirouette priors can reproduce sin²θ_W(M_Z) within experimental and theoretical uncertainties."
      status: proposed
      links: [DYNA-WEAK-001_l_from_the_temporal_triad, XXP-BRIDGE-Γ-001]
    - statement: "The Higgs width exhibits a calculable deviation from the SM prediction that is correlated in magnitude and sign with the value of ρ_stiff required to match sin²θ_W."
      domain: phenomenology
      falsifier: "A precise measurement of the Higgs width shows a deviation that is uncorrelated with, or contradicts, the prediction from the ρ_stiff value."
      status: proposed
      links: [DYNA-WEAK-001_l_from_the_temporal_triad, DYNA-Γ-004]
    - statement: "The value of sin²θ_W drifts on cosmological timescales at a rate suppressed by (⟨Γ²⟩/M_coh²)."
      domain: experiment
      falsifier: "Observation of a temporal variation in α or other constants implying a drift in sin²θ_W significantly larger than the Γ-tail prediction, or of the opposite sign."
      status: proposed
      links: [DYNA-WEAK-001_l_from_the_temporal_triad]
naming_notes:
  collisions: [The symbol θ is generic for angles (e.g., θ_C for the Cabibbo angle, θ₁₃ for neutrino mixing). The subscript W is standard and sufficient for disambiguation.]
  disambiguation: |
    The value of θ_W is energy-scale dependent ("runs"). In Pirouette, the term often refers to its fundamental value at the coherence barrier μ_c, from which the low-energy experimental value at M_Z is derived. Always specify the energy scale, e.g., sin²θ_W(M_Z), in calculations.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [FRAME_STIFFNESS, COHERENCE_BARRIER, TEMPORAL_TRIAD]
  downstream_effects: [Z_BOSON, PHOTON, HIGGS_DECAY_WIDTH]
license: CC-BY-SA-4.0
---

# Weinberg Angle

## Canonical (Pirouette)
The mixing angle between the neutral SU(2)_L gauge boson (W³) and the U(1)_Y gauge boson (B) that yields the physical photon and Z boson. In Pirouette, its value is fixed at the coherence barrier (μ_c) by the fundamental stiffness ratio ρ_stiff = K₂/K₁ of the temporal medium, where K₂ is the stiffness of the SU(2) triad frame and K₁ is the stiffness of the U(1) clock frame. This value at μ_c serves as the boundary condition for Renormalization Group flow to experimental energy scales.

## EFT-First Summary
The Weinberg Angle, θ_W, is operationally identical to the weak mixing angle in the Standard Model of particle physics. It parameterizes the mixing of the neutral electroweak gauge bosons. Pirouette provides a physical mechanism that fixes its value at a high energy scale (the coherence barrier, μ_c) as a ratio of mechanical-like "stiffnesses" of the vacuum. This high-scale value is then run down to experimental scales like the Z-boson mass using standard Renormalization Group equations to predict the observed low-energy value.

## Glossary Links
- See also: [FRAME_STIFFNESS](<#>), [COHERENCE_BARRIER](<#>), [TEMPORAL_TRIAD](<#>), [Z_BOSON](<#>)