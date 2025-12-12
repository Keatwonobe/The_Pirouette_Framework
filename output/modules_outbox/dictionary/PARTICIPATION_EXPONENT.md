---
term: "Participation Exponent"
canonical_id: "PARTICIPATION_EXPONENT"
symbol: "p"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-002_the_neutrino_knot"]
---

---
term: Participation Exponent
canonical_id: PARTICIPATION_EXPONENT
symbol: p
aliases: []
parents: [`DOMA-PHYS-002`]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-002_the_neutrino_knot
      lines: "§2"
      snippet: |
        $$ m_i = \mu_\nu; \left(\frac{\mathrm{PR}_i}{3}\right)^{p}; \left(\mathrm{Purity}_i\right)^{q} $$
  editors: [system-agent]
  review_log: []
triad:
  art: |
    The weight of a particle's identity. It measures how intensely a neutrino's existence—spread across multiple flavors—condenses into the gravity of its mass.
  law: |
    A dimensionless power-law exponent relating a neutrino's mass to its Participation Ratio (PR). The empirically derived value p≈1.54 must hold across both normal and inverted mass orderings to be consistent with global oscillation data.
  philosophy: |
    Encodes the principle that mass is not fundamental but emerges from internal geometry. The exponent `p` is a "law of structure" that quantifies how the degree of flavor mixing translates into a physical mass, defining a key axis of the Prime Resonance Manifold.
pirouette_definition: |
  A dimensionless exponent in the Pirouette Neutrino Mass Law that governs how the mass of a neutrino eigenstate (mᵢ) scales with its normalized Participation Ratio (PRᵢ/3). It quantifies the contribution of flavor-state "mixedness" to the eigenstate's mass according to the relation mᵢ ∝ (PRᵢ/3)ᵖ.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: p
      meaning: Participation Exponent
      dimensions: dimensionless
      default_range: 1.54±0.01 (empirical)
    - name: mᵢ
      meaning: Mass of the i-th neutrino eigenstate
      dimensions: M
      default_range: contextual (eV/c²)
    - name: PRᵢ
      meaning: Participation Ratio of the i-th eigenstate
      dimensions: dimensionless
      default_range: "[1, 3]"
    - name: μ_ν
      meaning: Base Mass Scale for the neutrino sector
      dimensions: M
      default_range: contextual (eV/c²)
  measurement:
    procedures:
      - name: Global Fit Inference
        outline: |
          `p` is not directly measured. It is inferred by fitting the three parameters (p, q, μ_ν) of the Pirouette Neutrino Mass Law to experimentally determined neutrino mass-squared differences (Δm²₂₁ and Δm²₃₁). The procedure involves: (1) Using global fit values for mixing angles (θ₁₂, θ₁₃, θ₂₃) and δ_CP to construct the PMNS matrix. (2) Calculating Purityᵢ and PRᵢ for each mass state. (3) Numerically solving for the (p,q,μ_ν) triplet that best reproduces the experimental Δm² values.
        expected_signals: [A consistent best-fit value of p ≈ 1.54 that is stable for both Normal and Inverted mass ordering assumptions, A good χ² fit for the mass law predictions vs. experimental data]
        pitfalls: [High sensitivity to uncertainties in input oscillation parameters (esp. θ₂₃ and δ_CP), Failure to correct for matter effects (e.g., via the Γ-toggle) can bias the inferred value]
context_windows:
  - module: DOMA-PHYS-002_the_neutrino_knot
    excerpt: |
      The Pirouette Neutrino Mass Law...posits that the absolute mass of each neutrino mass eigenstate (m_i) is not an intrinsic property, but an emergent one... p (Participation Exponent): A dimensionless exponent governing how a state's mass is scaled by its "Participation Ratio" (PR).
  - module: DOMA-PHYS-002_the_neutrino_knot
    excerpt: |
      The fundamental parameters (μ_ν,p,q) are not universal constants. Instead, they define a continuous, two-dimensional surface within their three-dimensional parameter space... A neutrino is not defined by a single set of parameters, but by a "knot" configuration that lies somewhere on this prime resonance manifold.
poetic_connections:
  motifs: [scaling law, geometric mass, mixedness, structural constant]
  evocative_lines:
    - "The discovery of this manifold implies a previously unseen degree of freedom in the universe."
    - "...changes our understanding of physical law from a rigid decree to a geometric relationship."
  association_matrix:
    - [ "PARTICIPATION_RATIO", 0.9 ]
    - [ "PURITY_EXPONENT", 0.8 ]
    - [ "PRIME_RESONANCE_MANIFOLD", 0.7 ]
    - [ "NEUTRINO_KNOT", 0.6 ]
formal_mappings:
  candidates:
    - target: Scaling exponent (e.g., in critical phenomena)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        Observable ~ (Parameter)^p
      justification: |
        Like a critical exponent in statistical mechanics, `p` is a dimensionless number that describes how one physical quantity (mass) scales with another (Participation Ratio) according to a power law. It is not a fundamental coupling constant but rather describes the nature of the geometric relationship itself.
      references: []
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Participation Exponent `p` is independent of the neutrino mass ordering."
      domain: phenomenology
      falsifier: "Future, high-precision global fits of neutrino oscillation data reveal that statistically different values for `p` are required to fit the mass-squared differences in the Normal Ordering versus the Inverted Ordering."
      status: supported
      links: [`DOMA-PHYS-002`]
naming_notes:
  collisions: [The symbol `p` is commonly used for momentum and pressure. In this context, it is always a dimensionless exponent.]
  disambiguation: |
    `p` should not be confused with `Purity`, which is a distinct geometric measure in the same law. `p` is the exponent applied to the Participation Ratio (PR), while `q` is the exponent applied to Purity.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PARTICIPATION_RATIO]
  downstream_effects: [PRIME_RESONANCE_MANIFOLD, NEUTRINO_KNOT]
license: CC-BY-SA-4.0
---