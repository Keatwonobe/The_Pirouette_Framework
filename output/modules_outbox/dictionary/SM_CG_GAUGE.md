---
term: "SM-CG Gauge"
canonical_id: "SM_CG_GAUGE"
symbol: "Σ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-004_substrate_action_of_time"]
---

---
term: SM-CG Gauge
canonical_id: SM_CG_GAUGE
symbol: Σ
aliases: [Standard Model-Coherent Gauge]
parents: [DYNA-004]
children: [CORE-007, CORE-008, CORE-009]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-004
      lines: "§3"
      snippet: |
        Pick Σ (the SM-CG gauge). Push S_time forward:
        - Define coordinates x^{μ} via Σ; Ki → complex section; Γ → scalar density; T_a → coherence weight.
  editors: [AI Agent]
  review_log: []
triad:
  art: |
    The compass that orients the substrate's formless potential into the familiar grid of spacetime. It is the act of naming coordinates, a choice that crystallizes a world from the flux.
  law: |
    The SM-CG Gauge (Σ) is a specific, non-dynamical choice of functional mapping from the substrate's coherence motif field (Ki) and temporal density (Γ) to a set of spacetime coordinates (x^μ). Physical observables, computed via ε-expansions, must be independent of the choice of Σ.
  philosophy: |
    Σ embodies the principle that the substrate's dynamics are pre-geometric. By explicitly choosing a coordinate system, we separate the arbitrary 'map' (the gauge) from the invariant 'territory' (the substrate physics), ensuring that emergent spacetime phenomena are not artifacts of our description.
pirouette_definition: |
  The Standard Model-Coherent Gauge (SM-CG) is a specific, non-dynamical choice of gauge that establishes a coordinate system x^μ on the pre-spatial substrate. This choice enables the push-forward of the substrate action (S_time) into an effective spacetime action (S_eff). Operationally, Σ provides the explicit mapping rules for interpreting the substrate's Ki, Γ, and T_a fields as, respectively, a complex scalar section, a scalar density, and a coherence weight within this coordinate system, thereby recovering the Standard Model and General Relativity in the ε → 0 limit.
operational_definition:
  units: Dimensionless mapping or procedure.
  symbol_table:
    - name: Σ
      meaning: The SM-CG Gauge choice; a specific mapping from substrate fields to spacetime coordinates.
      dimensions: dimensionless
      default_range: N/A (a choice, not a value)
    - name: Ki(·)
      meaning: Substrate coherence motif field.
      dimensions: contextual
      default_range: contextual
    - name: Γ(·)
      meaning: Substrate temporal density functional.
      dimensions: contextual
      default_range: contextual
    - name: x^μ
      meaning: Emergent spacetime coordinates.
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Gauge Invariance Test
        outline: |
          1. Define a physical observable, O (e.g., a scattering amplitude, decoherence rate).
          2. Choose two distinct but valid gauges, Σ₁ and Σ₂.
          3. Calculate O(Σ₁) and O(Σ₂) by pushing the substrate action forward in each gauge and expanding to a consistent order in ε.
          4. Verify that O(Σ₁) = O(Σ₂). The choice of Σ is a computational intermediate; it is not directly measured.
        expected_signals: [Equality of calculated physical observables (e.g., cross-sections, particle masses) between calculations using different valid Σ choices.]
        pitfalls: [Mistaking a gauge-dependent intermediate quantity for a physical observable., Truncation errors in the ε-expansion that break apparent gauge invariance.]
context_windows:
  - module: DYNA-004
    excerpt: |
      Pick Σ (the SM-CG gauge). Push S_time forward: Define coordinates x^{μ} via Σ; Ki → complex section; Γ → scalar density; T_a → coherence weight. Expand around high-coherence backgrounds; keep quadratic fluctuations.
  - module: DYNA-004
    excerpt: |
      Keep Σ explicit in derivations; changes in Σ are gauge choices, not physics. Use ε-expansions to track beyond-SM corrections and prevent circularity.
poetic_connections:
  motifs: [cartography, crystallization, orientation]
  evocative_lines:
    - "Pick Σ (the SM-CG gauge). Push S_time forward..."
    - "...changes in Σ are gauge choices, not physics."
  association_matrix:
    - [ "SUBSTRATE", 0.9 ]
    - [ "SPACETIME_METRIC", 0.8 ]
    - [ "EPSILON_DEVIATION", 0.5 ]
formal_mappings:
  candidates:
    - target: Gauge fixing (e.g., Lorenz gauge ∂_μ A^μ = 0)
      domain: QFT
      mapping_kind: conceptual
      equation_hint: |
        Σ: {Ki(·), Γ(·)} → {x^μ}
      justification: |
        Like gauge fixing in QFT, Σ is a user-defined choice that simplifies calculations by removing unphysical degrees of freedom. It selects a specific 'slice' through the configuration space to define coordinates, analogous to how Lorenz gauge selects a specific representative for the photon field.
      references: []
      confidence: 0.8
  adopted:
    - target: Choice of coordinate chart (in General Relativity)
      rationale: |
        This mapping is adopted because Σ's primary function is to define the coordinates x^μ from the pre-geometric substrate, making it a direct analogue of selecting a coordinate system to describe a manifold in GR. It highlights the separation between the description (the gauge/chart) and the invariant reality.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "All physical observables calculated from the substrate action S_time are invariant under the choice of SM-CG Gauge Σ."
      domain: theory
      falsifier: "Discovering a physical observable (e.g., a particle mass, a decoherence rate) whose calculated value to all orders in ε demonstrably depends on the specific functional form of Σ."
      status: proposed
      links: [DYNA-004]
naming_notes:
  collisions: [summation symbol (Σ), scattering cross-section (σ), Pauli matrices (σ_i), Stefan-Boltzmann constant (σ)]
  disambiguation: |
    SM-CG stands for 'Standard Model-Coherent Gauge', indicating it is the specific choice that recovers the Standard Model in a high-coherence limit. Context is critical: within Pirouette, Σ is almost always this gauge choice, not a summation, unless explicit indices are present (e.g., Σ_i).
crosslinks:
  near_synonyms: []
  antonyms: [GAUGE_INVARIANT_OBSERVABLE]
  prerequisites: [SUBSTRATE_ACTION_OF_TIME, COHERENCE_MOTIF_FIELD]
  downstream_effects: [SPACETIME_METRIC, EFFECTIVE_ACTION]
license: CC-BY-SA-4.0
---

# SM-CG Gauge (Σ)

## Canonical (Pirouette)
The Standard Model-Coherent Gauge (SM-CG) is a specific, non-dynamical choice of gauge that establishes a coordinate system x^μ on the pre-spatial substrate. This choice enables the push-forward of the substrate action (S_time) into an effective spacetime action (S_eff). Operationally, Σ provides the explicit mapping rules for interpreting the substrate's Ki, Γ, and T_a fields as, respectively, a complex scalar section, a scalar density, and a coherence weight within this coordinate system, thereby recovering the Standard Model and General Relativity in the ε → 0 limit.

## EFT-First Summary
The SM-CG Gauge (Σ) is a theoretical tool analogous to choosing a coordinate chart in General Relativity. It is a non-physical, user-defined procedure that maps the fundamental, pre-geometric substrate fields onto a familiar four-dimensional spacetime grid. This allows the substrate dynamics to be expressed in the language of quantum field theory, but all physically measurable predictions must be independent of the specific Σ chosen.

## Glossary Links
- See also: [[Substrate]], [[Gauge Invariance]], [[Push-forward]]