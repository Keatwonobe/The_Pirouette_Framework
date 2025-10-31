---
term: "Base Mass Scale"
canonical_id: "BASE_MASS_SCALE"
symbol: "μ_ν"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-002_the_neutrino_knot"]
---

---
term: Base Mass Scale
canonical_id: BASE_MASS_SCALE
symbol: μ_ν
aliases: []
parents: [DOMA-PHYS-002]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-002_the_neutrino_knot
      snippet: |
        μ_ν (Base Mass Scale): A fundamental mass parameter for the neutrino sector, representing the baseline energy scale.
  editors: [GeneratorAgent]
  review_log: []
triad:
  art: |
    The fundamental pitch from which the universe tunes the neutrino's resonant mass. It is the scale of the canvas upon which the geometric knots of reality are tied.
  law: |
    A dimensionful parameter [eV] that converts the dimensionless geometric factors of the Pirouette Neutrino Mass Law into the absolute mass of a neutrino eigenstate. Its value is inferred by fitting the Law to observed mass-squared differences.
  philosophy: |
    μ_ν is not a universal constant but a coordinate on the Prime Resonance Manifold. It represents the energy scale of a specific self-consistent 'knot.' Its variability challenges the notion of fixed constants, replacing it with a principle of co-varying geometric relationships.
pirouette_definition: |
  The Base Mass Scale, μ_ν, is a parameter of the Pirouette Neutrino Mass Law that establishes the energy scale for the neutrino sector. For any given 'knot' configuration on the Prime Resonance Manifold, μ_ν is the specific mass value which is scaled by dimensionless geometric factors (Purity and Participation Ratio, raised to their respective exponents) to yield the absolute masses of the neutrino mass eigenstates.
operational_definition:
  units: eV (electron-volts)
  symbol_table:
    - name: μ_ν
      meaning: Base Mass Scale
      dimensions: M (Mass)
      default_range: ~0.017–0.019 eV
  measurement:
    procedures:
      - name: Inferential Derivation from Oscillation Data
        outline: |
          μ_ν is not measured directly. Its value is inferred via a numerical fit of the Pirouette Neutrino Mass Law parameters (μ_ν, p, q) to high-precision measurements of neutrino mass-squared differences (Δm²₂₁ and Δm²₃₁), using the measured PMNS mixing matrix to calculate Purity and Participation Ratio inputs.
        expected_signals: [A consistent best-fit value for μ_ν that, along with co-fit exponents p and q, accurately reproduces experimental Δm² values.]
        pitfalls: [Strong degeneracy with exponents p and q (the Prime Resonance Manifold) prevents an independent determination. The derived value is specific to a 'knot' and may depend on environmental context (Γ-toggle).]
context_windows:
  - module: DOMA-PHYS-002_the_neutrino_knot
    excerpt: |
      The Law:
      $$ m_i = \mu_\nu; \left(\frac{\mathrm{PR}_i}{3}\right)^{p}; \left(\mathrm{Purity}_i\right)^{q} $$
      Where:
      μ_ν (Base Mass Scale): A fundamental mass parameter for the neutrino sector, representing the baseline energy scale.
  - module: DOMA-PHYS-002_the_neutrino_knot
    excerpt: |
      The fundamental parameters (μ_ν,p,q) are not universal constants. Instead, they define a continuous, two-dimensional surface within their three-dimensional parameter space. Any point on this surface represents a valid, self-consistent physical reality. A neutrino is not defined by a single set of parameters, but by a "knot" configuration that lies somewhere on this prime resonance manifold.
poetic_connections:
  motifs: [baseline, scale, anchor, resonance, knot]
  evocative_lines:
    - "We began by seeking a single point of light in the darkness... Instead, we found a constellation."
    - "A knot of pure geometry, tied perfectly on a surface of possibility."
  association_matrix:
    - [ "PARTICIPATION_EXPONENT", 0.9 ]
    - [ "PURITY_EXPONENT", 0.9 ]
    - [ "PRIME_RESONANCE_MANIFOLD", 0.8 ]
formal_mappings:
  candidates:
    - target: Overall neutrino mass scale (e.g., v²/Λ in seesaw models)
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        μ_ν ~ <y> v²/Λ
      justification: |
        In Standard Model extensions like the seesaw mechanism, neutrino masses are generated with a characteristic scale determined by the Higgs VEV (v) and the scale of new, lepton-number-violating physics (Λ). μ_ν plays the role of this overall energy scale, which is then modulated by dimensionless geometric factors, analogous to how different Yukawa couplings (y) modulate a base scale.
      confidence: 0.5
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The value of μ_ν is not a universal constant but co-varies with exponents p and q along a continuous two-dimensional manifold."
      domain: theory
      falsifier: "Future high-precision oscillation and absolute mass measurements yielding a unique solution for (μ_ν, p, q), or a point inconsistent with the predicted manifold shape."
      status: proposed
      links: [DOMA-PHYS-002]
    - statement: "Neutrinos from different production environments may possess different values of μ_ν, corresponding to different knots on the Prime Resonance Manifold."
      domain: phenomenology
      falsifier: "High-precision absolute neutrino mass experiments (e.g., KATRIN, Project 8) on solar, atmospheric, and reactor neutrinos finding an invariant value for the absolute mass scale."
      status: proposed
      links: [DOMA-PHYS-002]
naming_notes:
  collisions: [`μ` (general mass scale), `μ` (chemical potential), `μ` (muon)]
  disambiguation: |
    μ_ν specifically refers to the baseline mass parameter within the Pirouette Neutrino Mass Law. It should not be confused with the mass of a specific neutrino eigenstate (m_i), the sum of neutrino masses (Σm), or the muon (μ).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PARTICIPATION_RATIO, PURITY]
  downstream_effects: [NEUTRINO_KNOT_HYPOTHESIS, PRIME_RESONANCE_MANIFOLD]
license: CC-BY-SA-4.0
---

# Base Mass Scale

## Canonical (Pirouette)
The Base Mass Scale, μ_ν, is a parameter of the Pirouette Neutrino Mass Law that establishes the energy scale for the neutrino sector. For any given 'knot' configuration on the Prime Resonance Manifold, μ_ν is the specific mass value which is scaled by dimensionless geometric factors (Purity and Participation Ratio, raised to their respective exponents) to yield the absolute masses of the neutrino mass eigenstates.

## EFT-First Summary
The Base Mass Scale μ_ν acts as the fundamental energy scale for the neutrino sector. Conceptually, it is analogous to the overall mass scale in effective field theories like the seesaw mechanism (e.g., v²/Λ), which is then modulated by dimensionless geometric factors specific to each neutrino state. Unlike a fixed constant, μ_ν is a coordinate on the Prime Resonance Manifold, co-varying with other parameters to define a self-consistent physical state.

## Glossary Links
- See also: [[PARTICIPATION_RATIO]], [[PURITY]], [[PRIME_RESONANCE_MANIFOLD]]