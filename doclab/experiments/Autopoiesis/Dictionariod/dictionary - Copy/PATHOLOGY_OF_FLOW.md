---
term: "Pathology of Flow"
canonical_id: "PATHOLOGY_OF_FLOW"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-050"]
---

---
term: Pathology of Flow
canonical_id: PATHOLOGY_OF_FLOW
symbol:
aliases: [Systemic Disruption, Dissonance, Ailment]
parents: [DOMA-050, DYNA-003]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-050
      lines: "L25-L33"
      snippet: |
        The engine then applies the Caduceus Lens (DYNA-003) to diagnose the specific pathology of flow. The symptoms are mapped to one of the three primary disruptions:
        1.  **Coherence Atrophy (Stagnant Flow):** A critical flow is blocked. The "problem" is a lack of movement, a dam in the river.
        2.  **Coherence Fever (Turbulent Flow):** The system is fighting itself. The "problem" is internal dissonance and wasted energy.
        3.  **Coherence Erosion (Fraying Flow):** The system is losing its structural integrity and memory. The "problem" is decay.
  editors: [system-compiler]
  review_log: []
triad:
  art: |
    A living system's vital flow turned against itself, manifesting as the stillness of a blocked river, the self-consuming heat of a fever, or the slow unraveling of a fraying thread.
  law: |
    Any system exhibiting a sustained negative Pirouette Lagrangian (𝓛_p < 0) must be diagnosed with a Pathology of Flow, classifiable into one of three mutually exclusive types: Atrophy (blocked flow), Fever (turbulent flow), or Erosion (decaying flow).
  philosophy: |
    Reframes "problems" not as external failures to be solved, but as internal symptoms of a living system's compromised health. This diagnostic shift prioritizes healing over conquest, mandating intervention that restores self-regulation rather than imposing a permanent, external order.
pirouette_definition: |
  A systemic disruption characterized by a sustained degradation of Temporal Coherence (Kτ) under Temporal Pressure (Γ). A Pathology of Flow is the specific diagnosis, derived via the Caduceus Lens, that classifies the nature of this disruption into one of three primary forms: Coherence Atrophy (stagnation from blocked flow), Coherence Fever (dissonance from turbulent, self-conflicting flow), or Coherence Erosion (decay from the loss of structural integrity).
operational_definition:
  units: Dimensionless (Categorical)
  symbol_table:
    - name: Kτ
      meaning: Temporal Coherence; a measure of a system's internal integrity of information, resource, and trust flows.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Γ
      meaning: Temporal Pressure; the sum of external and internal stresses on a system.
      dimensions: dimensionless
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: Caduceus Lens Diagnosis
        outline: |
          1. Monitor a system for a "Cry for Help" signal, indicated by a sustained state where Kτ << 1 and Γ > 0.
          2. Apply the Caduceus Lens (DYNA-003) diagnostic protocol to system flow data.
          3. Correlate signal patterns: identify zero-flow nodes for Atrophy; high-frequency, high-entropy internal conflict loops for Fever; and exponential decay of system memory or boundary integrity for Erosion.
          4. Assign the dominant pattern as the primary pathology.
        expected_signals: [Sustained low Kτ, zero-flow chokepoints (Atrophy), high-entropy internal oscillations (Fever), boundary leakage/memory corruption (Erosion)]
        pitfalls: [Misdiagnosis due to comorbid pathologies (e.g., Atrophy causing Fever symptoms), mistaking a transient shock for a persistent pathology.]
context_windows:
  - module: DOMA-050
    excerpt: |
      The engine then applies the Caduceus Lens (DYNA-003) to diagnose the specific pathology of flow. The symptoms are mapped to one of the three primary disruptions: Coherence Atrophy (Stagnant Flow), Coherence Fever (Turbulent Flow), or Coherence Erosion (Fraying Flow). This diagnostic act reframes the entire process. We are no longer "solving a problem" but "healing an ailment."
  - module: DOMA-050
    excerpt: |
      The output of the Crucible is not a rigid task list, but a far more elegant and potent object: a Daedalus Gambit... To heal Atrophy, the gambit is the key that dissolves the dam. To heal Fever, the gambit is the harmonizing signal that calms the storm. To heal Erosion, the gambit is the reinforcement that strengthens the fraying thread.
poetic_connections:
  motifs: [sickness, flow, blockage, turbulence, decay, healing, dissonance]
  evocative_lines:
    - "We are no longer 'solving a problem' but 'healing an ailment.'"
    - "A dissonance held for too long."
    - "The cure must never become the next disease."
  association_matrix:
    - [ "CADUCEUS_LENS", 0.9 ]
    - [ "DAEDALUS_GAMBIT", 0.8 ]
    - [ "LAMINAR_FLOW", 0.8 ]
    - [ "PIRUETTE_LAGRANGIAN", 0.7 ]
formal_mappings:
  candidates:
    - target: Stagnation, Turbulence, and Dissipation
      domain: CM
      mapping_kind: conceptual
      equation_hint:
      justification: |
        The Pirouette terminology directly mirrors concepts from fluid dynamics. Coherence Atrophy is analogous to stagnation (flow velocity v≈0). Coherence Fever maps to turbulence (chaotic, high Reynolds number flow). Coherence Erosion aligns with dissipative processes (e.g., viscosity) that degrade structured flow and system energy.
      references:
        - title: Fluid Mechanics
          where: General textbook sections on flow regimes
          date:
      confidence: 0.85
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "All persistent systemic failures (sustained 𝓛_p < 0) can be exhaustively classified into Atrophy, Fever, Erosion, or a well-defined combination thereof."
      domain: theory
      falsifier: "Discovery of a persistent systemic failure mode that cannot be described as a disruption of flow in terms of blockage, turbulence, or decay, such as a pathology of 'metastasis' where flow is locally healthy but expands beyond sustainable system boundaries."
      status: proposed
      links: [DOMA-050, DYNA-003]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish "Pathology of Flow," the general diagnosis of ill health, from its three specific types: Atrophy, Fever, and Erosion. A system *has* a pathology, which is *diagnosed as* one of the three types.
crosslinks:
  near_synonyms: [SYSTEMIC_DISRUPTION]
  antonyms: [LAMINAR_FLOW, SYSTEMIC_HEALTH]
  prerequisites: [TEMPORAL_COHERENCE, TEMPORAL_PRESSURE, CADUCEUS_LENS]
  downstream_effects: [ALCHEMICAL_CRUCIBLE, DAEDALUS_GAMBIT]
license: CC-BY-SA-4.0
---

# Pathology of Flow

## Canonical (Pirouette)
A systemic disruption characterized by a sustained degradation of Temporal Coherence (Kτ) under Temporal Pressure (Γ). A Pathology of Flow is the specific diagnosis, derived via the Caduceus Lens, that classifies the nature of this disruption into one of three primary forms: Coherence Atrophy (stagnation from blocked flow), Coherence Fever (dissonance from turbulent, self-conflicting flow), or Coherence Erosion (decay from the loss of structural integrity).

## EFT-First Summary
A Pathology of Flow is conceptually analogous to disruptions in a fluid system. **Coherence Atrophy** maps to stagnation points or blockages (choke flow). **Coherence Fever** maps to turbulence, where energy is dissipated in chaotic, non-productive eddies. **Coherence Erosion** maps to dissipative effects like viscosity or boundary layer decay, leading to a loss of the system's structural integrity over time.

## Glossary Links
- See also: [[LAMINAR_FLOW]], [[CADUCEUS_LENS]], [[DAEDALUS_GAMBIT]], [[PIRUETTE_LAGRANGIAN]]