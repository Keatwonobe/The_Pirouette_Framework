---
term: "Background coherence density"
canonical_id: "BACKGROUND_COHERENCE_DENSITY"
symbol: "Γ₀"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-007_pressuraon_constraint_atlas"]
---

---
term: Background coherence density
canonical_id: BACKGROUND_COHERENCE_DENSITY
symbol: Γ₀
aliases: []
parents: [XAP-007]
children: [XAP-008]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-007_pressuraon_constraint_atlas
      snippet: |
        All quantities are expressed through the two stiffness parameters
        Γ₀ (background coherence density) and λΓ (self-coupling).
  editors: [Auto-gen (Pirouette-Dict-Agent)]
  review_log: []
triad:
  art: |
    The silent, ambient tension of the cosmic substrate; the vacuum's deep hum from which all pressuron whispers arise.
  law: |
    The background coherence density Γ₀ sets the mass scale for composite pressuron excitations (mₚ = Γ₀√(2λΓ)) and, through its residual stiffness, determines the effective cosmological constant (Λ_eff ∝ Γ₀²).
  philosophy: |
    Γ₀ is the foundational scale linking the microphysics of the pressuron sector to macrophysical cosmology. It represents the non-zero ground state energy of the Γ-field, acting as both a mass-giver for its excitations and the source of residual vacuum stiffness observed as dark energy.
pirouette_definition: |
  A fundamental scalar parameter representing the background vacuum expectation value (VEV) of the Γ-field. It establishes the primary mass and energy scale for the pressuron sector. All derived observables, including the pressuron mass `mₚ` and the residual energy density `ρ_{Γ,res}` (identified with the cosmological constant Λ), are expressed in terms of Γ₀ and the self-coupling `λΓ`.
operational_definition:
  units: Energy (typically MeV)
  symbol_table:
    - name: Γ₀
      meaning: Background coherence density / Γ-field VEV
      dimensions: M L² T⁻² (Energy)
      default_range: 15–95 MeV
  measurement:
    procedures:
      - name: Inferential Constraint via Composite Observables
        outline: |
          Γ₀ is not measured directly but is constrained by a global fit of derived observables to data. Key inputs include: 1. Collider searches (e.g., Belle-II) for missing energy signatures, which constrain the pressuron mass `mₚ`. 2. Torsion-balance experiments searching for fifth forces, which constrain the interaction range `λΓ⁻¹/²` and strength `ε`. 3. Cosmological measurements (CMB, BAO) of the dark energy density `ρ_{Γ,res}`.
        expected_signals: [A non-zero pressuron mass `m_p` in the 10-30 MeV range, A fifth-force signal with a range of 1-100 μm, A residual vacuum energy matching the observed cosmological constant]
        pitfalls: [Parameter degeneracies between Γ₀ and `λΓ`, Systematic errors in fifth-force or cosmological measurements, Other new physics mimicking missing energy signatures]
context_windows:
  - module: XAP-007_pressuraon_constraint_atlas
    excerpt: |
      To map the viable parameter space of the pressuron sector predicted by the Pirouette framework and summarize current and future constraints. All quantities are expressed through the two stiffness parameters Γ₀ (background coherence density) and λΓ (self-coupling). Derived observables include: mₚ = Γ₀√(2λΓ), ε = V''(Γ₀)/KΓ, λΓ ≃ (1/4ξ)(mH²/Γ₀²).
  - module: XAP-007_pressuraon_constraint_atlas
    excerpt: |
      XAP-007 anchors the Pirouette cosmological sector in measurable reality. All known laboratory, astrophysical, and cosmological data are consistent with a 10–30 MeV composite pressuron with couplings κ ~ 10⁻³ and healing length 10⁻⁵–10⁻³ m. The remaining parameter window defines a decisive target for forthcoming experiments, bridging theoretical elegance with falsifiable prediction.
poetic_connections:
  motifs: [vacuum expectation, ground state, cosmic stiffness, ambient field]
  evocative_lines:
    - "Λ as Residual Γ-Stiffness"
    - "bridging theoretical elegance with falsifiable prediction"
  association_matrix:
    - [ "PRESSURON", 0.9 ]
    - [ "COSMOLOGICAL_CONSTANT_Λ", 0.8 ]
    - [ "SELF_COUPLING_λΓ", 0.7 ]
formal_mappings:
  candidates:
    - target: Vacuum Expectation Value (VEV) of a scalar field, `v`
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        mₚ = Γ₀√(2λΓ)  is analogous to  m_W = gv/2
      justification: |
        Γ₀ represents the non-zero value of the Γ-field in the vacuum state, analogous to the Higgs field VEV `v`. This VEV breaks a symmetry and gives mass to the field's excitations (pressurons), directly paralleling the role of the Higgs VEV in electroweak symmetry breaking.
      references: []
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The value of Γ₀ lies in the approximate range of 15–95 MeV."
      domain: phenomenology
      falsifier: "Concurrent experimental results from collider searches, stellar cooling bounds, and fifth-force experiments requiring a value of Γ₀ outside this range to be consistent."
      status: proposed
      links: [XAP-007]
    - statement: "The residual stiffness of the Γ₀ condensate is the source of the observed cosmological constant Λ."
      domain: theory
      falsifier: "Precision cosmological measurements showing the equation of state for dark energy `w` deviates significantly from -1, or evolves in a way inconsistent with the predicted RG flow of Γ₀ (e.g., if |w(a)+1| >> 0.01)."
      status: proposed
      links: [XAP-006E, XAP-007]
naming_notes:
  collisions: [The symbol Γ is commonly used for decay rates in particle physics and the Gamma function in mathematics.]
  disambiguation: |
    Within the Pirouette framework, Γ₀ always refers to the background VEV of the Γ-field, a parameter with dimensions of energy. It should not be confused with decay widths or mathematical functions.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [Γ-FIELD, VACUUM_EXPECTATION_VALUE]
  downstream_effects: [PRESSURON_MASS, COSMOLOGICAL_CONSTANT_Λ, FIFTH_FORCE]
license: CC-BY-SA-4.0
---

# Background coherence density

## Canonical (Pirouette)
A fundamental scalar parameter representing the background vacuum expectation value (VEV) of the Γ-field. It establishes the primary mass and energy scale for the pressuron sector. All derived observables, including the pressuron mass `mₚ` and the residual energy density `ρ_{Γ,res}` (identified with the cosmological constant Λ), are expressed in terms of Γ₀ and the self-coupling `λΓ`.

## EFT-First Summary
In standard effective field theory, Γ₀ is the vacuum expectation value (VEV) of the scalar Γ-field. Similar to the Higgs VEV, it sets the fundamental scale for the pressuron sector, giving mass to the composite pressuron excitations via `m_p = Γ₀√(2λΓ)`. Its residual potential energy density is identified with the cosmological constant, `Λ_eff ∝ Γ₀²`, providing a dynamical origin for dark energy. Current phenomenological constraints from colliders, fifth-force experiments, and cosmology place Γ₀ in the 15–95 MeV range.

## Glossary Links
- See also: Pressuron (`m_p`), Γ-Field Self-Coupling (`λΓ`), Cosmological Constant (`Λ`)