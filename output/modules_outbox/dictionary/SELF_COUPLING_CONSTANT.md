---
term: "Self-coupling constant"
canonical_id: "SELF_COUPLING_CONSTANT"
symbol: "λ_Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-007_pressuraon_constraint_atlas"]
---

---
term: Self-coupling constant
canonical_id: SELF_COUPLING_CONSTANT
symbol: λ_Γ
aliases: []
parents: [XAP-007_pressuraon_constraint_atlas, MATH-026]
children: [XAP-008]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-007_pressuraon_constraint_atlas
      lines: "§2, Table"
      snippet: |
        Self-coupling constant | λ_Γ | 0.05–0.2 | fits EW sector
  editors: [system]
  review_log: []
triad:
  art: |
    The measure of a field's conversation with itself; the internal tension that sculpts its own form and sets the scale of its reach.
  law: |
    The mass of the composite pressuron excitation, `m_p`, is determined by the self-coupling and the background coherence density `Γ_0` via the relation `m_p = Γ_0 * sqrt(2λ_Γ)`.
  philosophy: |
    This constant is a linchpin, connecting the microscopic, internal dynamics of the Γ-field to macroscopic, observable phenomena. It translates the abstract strength of self-interaction into the concrete mass of a particle and the physical range of a new force, making the framework's core assumptions falsifiable.
pirouette_definition: |
  A fundamental, dimensionless parameter that specifies the strength of the quartic self-interaction term in the Γ-field's potential. It determines the mass of the composite pressuron excitation (`m_p`) and the field's healing length (`λ_Γ^-1/2`), thereby setting the characteristic range of associated fifth-force interactions.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: λ_Γ
      meaning: Self-coupling constant
      dimensions: dimensionless
      default_range: 0.05–0.2
    - name: m_p
      meaning: Pressuron constituent mass
      dimensions: M
      default_range: 10–30 MeV
    - name: Γ_0
      meaning: Background coherence density
      dimensions: M^2
      default_range: contextual
  measurement:
    procedures:
      - name: Inference from Fifth-Force Range
        outline: |
          Conduct high-precision tests of the inverse-square law of gravity using torsion balances or atom interferometry. A confirmed deviation exhibiting a Yukawa-like potential `exp(-r/d)/r` would measure the interaction range `d`. The self-coupling is then inferred as `λ_Γ = d^-2`.
        expected_signals: [Yukawa-potential deviation from 1/r^2 gravity]
        pitfalls: [Systematic errors from electrostatic or magnetic forces, difficulty distinguishing from other exotic physics]
      - name: Inference from Collider Signatures
        outline: |
          Search for missing energy signatures in processes like `e+e- -> γ + MET` or `B -> K + MET`, where MET is from a `ΓΓ` pair. The production cross-section depends on `m_p` and the lepton coupling `κ`. By combining cross-section limits with a value for `Γ_0` derived from cosmological data, `λ_Γ` can be constrained via `λ_Γ = m_p^2 / (2 Γ_0^2)`.
        expected_signals: [Excess events in missing energy channels]
        pitfalls: [Model degeneracy (dependence on `κ` and `Γ_0`), standard model background contamination]
context_windows:
  - module: XAP-007_pressuraon_constraint_atlas
    excerpt: |
      To map the viable parameter space of the pressuron sector predicted by the Pirouette framework and summarize current and future constraints. All quantities are expressed through the two stiffness parameters `Γ_0` (background coherence density) and `λ_Γ` (self-coupling).
  - module: XAP-007_pressuraon_constraint_atlas
    excerpt: |
      Fifth-Force / Casimir-Type Tests. The effective Yukawa potential is `V_Γ(r) = ε^2 * exp(-r / λ_Γ^-1/2) / r`. Current torsion-balance data exclude `ε > 10^-3` for ranges `λ_Γ^-1/2 > 10^-4` m. The predicted `10^-5 – 10^-3` m window remains open—ideal for near-term laboratory search.
poetic_connections:
  motifs: [self-interaction, stiffness, cohesion, interaction-range]
  evocative_lines:
    - "All quantities are expressed through the two stiffness parameters."
    - "bridging theoretical elegance with falsifiable prediction."
  association_matrix:
    - [ "PRESSURON_MASS", 0.9 ]
    - [ "HEALING_LENGTH", 0.9 ]
    - [ "BACKGROUND_COHERENCE_DENSITY", 0.8 ]
    - [ "FIFTH_FORCE", 0.7 ]
formal_mappings:
  candidates:
    - target: Quartic coupling constant (λ)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        V(Γ) ≈ (λ_Γ/4)(|Γ|^2 - Γ_0^2)^2
      justification: |
        `λ_Γ` governs the strength of the non-quadratic term in the Γ-field's potential, analogous to the `λ` in a standard `Φ⁴` scalar field theory which describes self-interaction. This term is responsible for generating the mass of the field's excitations (pressurons) after spontaneous symmetry breaking around the vacuum expectation value `Γ_0`.
      references: []
      confidence: 0.95
  adopted:
    - target: Quartic coupling constant (λ) in Φ⁴ theory
      rationale: This is a direct and standard analogy in quantum field theory for a scalar field self-interaction term that generates mass via a Mexican-hat potential. The Pirouette phenomenology is built directly on this formal structure.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The value of `λ_Γ` is constrained to the range 0.05–0.2 to be consistent with electroweak sector data."
      domain: phenomenology
      falsifier: "A global fit of collider, cosmological, and precision measurement data requires a value of `λ_Γ` outside this range, or demonstrates no preference for any value."
      status: supported
      links: [XAP-007_pressuraon_constraint_atlas]
    - statement: "The fifth-force interaction range `λ_Γ^-1/2`, derived from the self-coupling, is between 1 μm and 100 μm."
      domain: experiment
      falsifier: "Null results from torsion-balance or atom interferometry experiments definitively rule out any new forces in this range down to the predicted coupling strength, or a new force is discovered with a range outside this window."
      status: under-test
      links: [XAP-007_pressuraon_constraint_atlas]
naming_notes:
  collisions: [λ (wavelength), Λ (cosmological constant)]
  disambiguation: |
    Distinguish from the cosmological constant, `Λ`. In Pirouette, `Λ` is an emergent property related to residual Γ-stiffness, whereas `λ_Γ` is a fundamental parameter of the Γ-field potential. The subscript `Γ` is essential to distinguish it from other coupling constants or wavelength.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GAMMA_FIELD, BACKGROUND_COHERENCE_DENSITY]
  downstream_effects: [PRESSURON_MASS, HEALING_LENGTH, FIFTH_FORCE]
license: CC-BY-SA-4.0
---

# Self-coupling constant

## Canonical (Pirouette)
A fundamental, dimensionless parameter that specifies the strength of the quartic self-interaction term in the Γ-field's potential. It determines the mass of the composite pressuron excitation (`m_p`) and the field's healing length (`λ_Γ^-1/2`), thereby setting the characteristic range of associated fifth-force interactions.

## EFT-First Summary
In the language of Effective Field Theory, `λ_Γ` is the dimensionless quartic coupling constant for the scalar Γ-field. It parameterizes the strength of the `|Γ|⁴` term in the potential, which drives self-interaction and, after spontaneous symmetry breaking around the vacuum expectation value `Γ_0`, generates the mass for the pressuron excitation. Its value is constrained by a combination of collider, astrophysical, and precision measurement data to the range 0.05–0.2.

## Glossary Links
- See also: [Pressuron Mass](<#>), [Healing Length](<#>), [Γ-field](<#>), [Background Coherence Density](<#>)