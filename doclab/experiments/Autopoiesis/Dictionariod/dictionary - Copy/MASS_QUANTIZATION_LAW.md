---
term: "Mass Quantization Law"
canonical_id: "MASS_QUANTIZATION_LAW"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-Γ-006_the_flavor_problem"]
---

---
term: Mass Quantization Law
canonical_id: MASS_QUANTIZATION_LAW
symbol: mₙ ∝ n²
aliases: [Harmonic Mass Law, Quadratic Mass Scaling]
parents: [MATH-Γ-005, DYNA-Γ-004]
children: [MATH-Γ-007, XXP-BRIDGE-Γ-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-Γ-006
      lines: "L31-L36"
      snippet: |
        Because mass reflects temporal curvature (m ∝ ωₙ² / Γc), the generational mass ratios follow
        [ m_{n+1}/m_n = ((n+1)/n)² ]
        Introducing small coherence-damping corrections...
        [ m_n = m_1 n² (1+εₙ) ]
  editors: [Automated Agent]
  review_log: []
triad:
  art: |
    Generations are not coincidences but octaves in the song of time. The electron, muon, and tau are the first three notes of a chord struck upon the temporal field; their masses are the volumes of that resonance.
  law: |
    The mass of a fermion in generation `n` (where n=1,2,3) is proportional to the square of its generation number, `mₙ = m₁ n² (1+εₙ)`, where `m₁` is the first-generation mass and `εₙ` is a small, calculable logarithmic correction from Higgs coupling.
  philosophy: |
    This law replaces the arbitrary Yukawa couplings of the Standard Model with a single, predictive physical principle. It posits that the flavor problem is not a question of arbitrary parameters but of quantized dynamics, grounding the fermion mass hierarchy in the harmonic structure of temporal resonance.
pirouette_definition: |
  The Mass Quantization Law is the core principle of the Pirouette flavor model, stating that the masses of elementary fermions are determined by quantized harmonics of the temporal Γ-field. Each successive generation (n=1, 2, 3) corresponds to a higher standing-wave mode (ψₙ) of temporal curvature. Because mass is proportional to the square of the temporal frequency (m ∝ ωₙ²), the masses of the generations scale quadratically with their harmonic number `n`. This relationship, mₙ ∝ n², explains the vast mass hierarchy between the electron, muon, and tau, and similarly for quarks, without invoking free parameters for each generation.
operational_definition:
  units: dimensionless (mass ratio)
  symbol_table:
    - name: mₙ
      meaning: Mass of the n-th generation fermion
      dimensions: M
      default_range: 0.5 MeV – 173 GeV
    - name: n
      meaning: Harmonic number / Generation index
      dimensions: dimensionless
      default_range: 1, 2, 3
    - name: m₁
      meaning: Mass of the first-generation fermion (base mass)
      dimensions: M
      default_range: contextual (e.g., ~0.511 MeV for leptons)
    - name: εₙ
      meaning: Coherence-damping correction factor
      dimensions: dimensionless
      default_range: 10⁻³ – 10⁻²
  measurement:
    procedures:
      - name: Lepton Mass Ratio Verification
        outline: |
          1. Obtain the high-precision pole masses for the electron (m₁, n=1), muon (m₂, n=2), and tau (m₃, n=3).
          2. Calculate the mass ratios m₂/m₁ and m₃/m₁.
          3. Compare the observed ratios to the theoretical predictions 2²(1+ε₂) and 3²(1+ε₃).
          4. The logarithmic correction term εₙ can be independently constrained by measuring Higgs-fermion couplings.
        expected_signals: [m₂/m₁ ≈ 4, m₃/m₁ ≈ 9, with deviations matching the predicted form of εₙ]
        pitfalls: [Ambiguities in quark mass definitions (pole vs. running mass), higher-order radiative corrections, experimental precision limits.]
context_windows:
  - module: MATH-Γ-006
    excerpt: |
      Because mass reflects temporal curvature (m ∝ ωₙ² / Γ_c), the generational mass ratios follow `(m_{n+1}/m_n) = ((ω_{n+1})/ω_n)² = ((n+1)/n)²`. Introducing small coherence-damping corrections ((1+ε_n)) from coupling to the Higgs (DYNA-Γ-004), the corrected masses become: `m_n = m_1 n² (1+ε_n)`, where `ε_n ≈ (λ_{HΓ}/(8π²))ln n`. This generates hierarchical scaling consistent with observed lepton masses.
  - module: MATH-Γ-006
    excerpt: |
      Quarks follow the same harmonic rule but with an additional color-coherence factor (C_f): `m_{q,n} = m_{q,1} n² C_f`, where `C_f = 1 + α_s (ln n)/π`. This predicts the approximate up–charm–top mass scaling, yielding the logarithmic spacing seen across the Standard Model spectrum without free Yukawa parameters.
poetic_connections:
  motifs: [harmonic series, resonance, octaves, quantization, temporal chord]
  evocative_lines:
    - "Generations are not coincidences but octaves in the song of time."
    - "In this harmony, flavor is the geometry of coherence itself."
  association_matrix:
    - [ "TEMPORAL_RESONANCE", 0.9 ]
    - [ "FLAVOR_GENERATION", 0.9 ]
    - [ "FLAVOR_MIXING", 0.7 ]
    - [ "THREE_GENERATION_LIMIT", 0.8 ]
formal_mappings:
  candidates:
    - target: Yukawa Couplings (Y_f)
      domain: SM
      mapping_kind: conceptual
      equation_hint: |
        SM: m_f = (Y_f * v) / √2
        Pirouette: m_n ≈ (m₁ * n²)
      justification: |
        The Standard Model requires a separate, arbitrary Yukawa coupling parameter for each massive fermion to explain the mass hierarchy. The Mass Quantization Law replaces this set of 9+ free parameters with a single base mass scale and a predictive integer rule (n²), deriving the hierarchy from a physical principle (quantized temporal modes) rather than empirical fitting.
      references:
        - title: Standard Model Lagrangian
          where: PDG Review, "The CKM Quark-Mixing Matrix"
          date: 2024-08-08
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The mass ratios of charged leptons (and quarks) follow a quadratic scaling law mₙ ∝ n²."
      domain: phenomenology
      falsifier: "Precision measurements of lepton masses that deviate from the n² scaling beyond the predicted logarithmic corrections (εₙ). For example, finding m_μ / m_e is significantly different from 4 * (1+ε₂)."
      status: supported
      links: [MATH-Γ-006]
    - statement: "The law is universal for all fermion types, with modifications only from other gauge interactions (e.g., color coherence factor C_f)."
      domain: theory
      falsifier: "Observing that one fermion sector (e.g., up-type quarks) follows a fundamentally different scaling law (e.g., exponential) while another (e.g., leptons) follows the n² law."
      status: proposed
      links: [MATH-Γ-006]
naming_notes:
  collisions: [Quantization of mass-energy levels in bound quantum systems (e.g., hydrogen atom).]
  disambiguation: |
    This law does not refer to the quantization of a single particle's energy levels. It specifically describes the relationship between the rest masses of distinct particles belonging to different generations of the same family (e.g., electron vs. muon). It is a law of *inter-generational* mass scaling.
crosslinks:
  near_synonyms: []
  antonyms: [YUKAWA_ARBITRARINESS]
  prerequisites: [TEMPORAL_RESONANCE, GAMMA_FIELD]
  downstream_effects: [FLAVOR_MIXING, THREE_GENERATION_LIMIT, CKM_HIERARCHY]
license: CC-BY-SA-4.0
---

# Mass Quantization Law

## Canonical (Pirouette)
The Mass Quantization Law is the core principle of the Pirouette flavor model, stating that the masses of elementary fermions are determined by quantized harmonics of the temporal Γ-field. Each successive generation (n=1, 2, 3) corresponds to a higher standing-wave mode (ψₙ) of temporal curvature. Because mass is proportional to the square of the temporal frequency (m ∝ ωₙ²), the masses of the generations scale quadratically with their harmonic number `n`. This relationship, mₙ ∝ n², explains the vast mass hierarchy between the electron, muon, and tau, and similarly for quarks, without invoking free parameters for each generation.

## EFT-First Summary
In the Standard Model Effective Field Theory (SMEFT), the masses of fermions are set by arbitrary Yukawa coupling constants (Y_f). The Pirouette Mass Quantization Law replaces this parametric freedom with a predictive physical law. It posits that the hierarchy of couplings `Y₁ : Y₂ : Y₃` is not random but follows the integer ratio `1² : 2² : 3²`, modified by small, calculable logarithmic corrections. This law provides a first-principles explanation for the observed fermion mass spectrum, which in the SM is merely an input.

## Glossary Links
- See also: [Temporal Resonance](<link>), [Flavor Generation](<link>), [Three-Generation Limit](<link>)