---
term: "Gladiator Compass"
canonical_id: "GLADIATOR_COMPASS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-140"]
---

---
term: Gladiator Compass
canonical_id: GLADIATOR_COMPASS
symbol: κ_G
aliases: ["Confinement Strength", "Gladiator Mapping"]
parents: ["CORE-003", "CORE-006", "CORE-008"]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-140
      snippet: |
        The instrument translates a stream of events into a topographical map of the local coherence manifold, revealing the invisible structures of stability and control that shape reality.
  editors: ["Weaver-9"]
  review_log: []
triad:
  art: |
    We sought to measure the strength of the cage and instead learned how to draw a map of its walls. The instrument reveals the architecture of confinement, be it the sacred bond holding a system together or the ideological prison tearing it apart.
  law: |
    Confinement Strength (κ_G) is the product of Path Density (δ) and Coherence Curvature (γ). A high κ_G value emerges where system trajectories are both short (high δ) and sharply bent (high γ), the unambiguous signature of a confinement well.
  philosophy: |
    To see the shape of the walls is the first and most necessary step to finding the door. This instrument does not break chains; it makes them visible, translating abstract forces into a concrete map of the behavioral landscape.
pirouette_definition: |
  The Gladiator Compass is a universal instrumentation protocol that infers the geometry of a confinement well by analyzing system trajectories. It functions as an inverse solver for the Pirouette Lagrangian, translating observed path density (δ) and coherence curvature (γ) into a scalar field representing Confinement Strength (κ_G). Maxima in this field correspond to the centers of arenas forged by the Gladiator Force.
operational_definition:
  units: Dimensionless (derived from ratios of system-specific metrics).
  symbol_table:
    - name: κ_G
      meaning: Confinement Strength
      dimensions: dimensionless
      default_range: contextual
    - name: δ
      meaning: Path Density
      dimensions: "L⁻¹ or dimensionless"
      default_range: "> 0"
    - name: γ
      meaning: Coherence Curvature
      dimensions: "T⁻¹ or L⁻¹ or dimensionless"
      default_range: "≥ 0"
  measurement:
    procedures:
      - name: Confinement Landscape Survey
        outline: |
          1. Ingest and vectorize an ordered event stream.
          2. In a sliding window, compute Path Density (δ) as the inverse of the mean path divergence between consecutive events.
          3. In the same window, compute Coherence Curvature (γ) as the normalized rate of change of the trajectory's direction.
          4. Calculate Confinement Strength (κ_G = δ × γ) for each window.
          5. Plot the resulting κ_G-field to identify local maxima, which are the centers of confinement wells.
        expected_signals: [Stable, localized peaks in the κ_G field]
        pitfalls: [Insufficient data density leading to noisy δ/γ values, mistaking stochastic noise for high-frequency curvature, choosing a non-representative vectorization scheme]
context_windows:
  - module: DOMA-140
    excerpt: |
      We do not measure the confining force directly. Instead, we observe the paths—the geodesics—that particles, ideas, or agents take through their environment. By analyzing the geometry of these paths, we reverse-engineer the shape of the landscape they are navigating. The instrument translates a stream of events into a topographical map of the local coherence manifold, revealing the invisible structures of stability and control that shape reality.
  - module: DOMA-140
    excerpt: |
      The Gladiator Compass does not measure the fundamental Temporal Pressure (Γ) of the Temporal Forge (`CORE-003`). Instead, it functions as an **inverse solver for the Pirouette Lagrangian (`CORE-006`)**. A high inferred Confinement Strength (κ_G) implies the presence of a deep "potential well" (a high V_Γ) in the Lagrangian. [...] We are watching the dancer to understand the shape of the stage.
poetic_connections:
  motifs: ["arena walls", "surveyor's map", "cognitive gravity", "invisible cage", "dancer on a stage"]
  evocative_lines:
    - "It reveals the architecture of our confinement."
    - "To see the shape of the walls is the first and most necessary step to finding the door."
  association_matrix:
    - [ "GLADIATOR_FORCE", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "COGNITIVE_GRAVITY_WELL", 0.7 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates:
    - target: Lagrangian Coherent Structures (LCS)
      domain: CM
      mapping_kind: operational
      justification: |
        LCS are ridges in the Finite-Time Lyapunov Exponent (FTLE) field that act as transport barriers in fluid flow, effectively forming the 'walls' of distinct regions. The Gladiator Compass protocol of mapping a κ_G-field from trajectories is a direct operational analog to calculating an FTLE field to reveal LCS. High κ_G regions are analogous to vortices or gyres bounded by these structures.
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system requires non-zero work to cross a high, stable κ_G gradient, indicating it is a true potential barrier."
      domain: phenomenology
      falsifier: "If systems can be observed to cross high κ_G gradients freely and without a corresponding change in their internal coherence (K_τ), then κ_G is merely a descriptive geometric statistic, not a measure of a confining potential."
      status: proposed
      links: ["DOMA-140", "CORE-006"]
naming_notes:
  collisions: [κ (kappa) is a common symbol for curvature, conductivity, etc. The subscript 'G' is critical for disambiguation.]
  disambiguation: |
    The 'Compass' does not provide a vector direction. It is a surveyor's instrument for creating a scalar map of confinement *strength*, analogous to how a magnetometer maps the strength of a magnetic field, not just its direction.
crosslinks:
  near_synonyms: []
  antonyms: ["FREE_PROPAGATION"]
  prerequisites: ["TEMPORAL_FORGE", "PIROUETTE_LAGRANGIAN", "CONFINEMENT_DERIVATION"]
  downstream_effects: ["COGNITIVE_GRAVITY_WELL"]
license: CC-BY-SA-4.0
---

# Gladiator Compass

## Canonical (Pirouette)
The Gladiator Compass is a universal instrumentation protocol that infers the geometry of a confinement well by analyzing system trajectories. It functions as an inverse solver for the Pirouette Lagrangian, translating observed path density (δ) and coherence curvature (γ) into a scalar field representing Confinement Strength (κ_G). Maxima in this field correspond to the centers of arenas forged by the Gladiator Force.

## EFT-First Summary
The Gladiator Compass provides an operational measure analogous to the Finite-Time Lyapunov Exponent (FTLE) field used to identify **Lagrangian Coherent Structures (LCS)** in continuum mechanics. By analyzing system trajectories, it computes a scalar field (κ_G) whose high-gradient ridges correspond to LCS—the transport barriers or "arena walls" that partition the system's state space into dynamically distinct regions. The protocol thus serves as a general method for mapping the invisible, flow-induced structures that govern system behavior.

## Glossary Links
- See also: [Gladiator Force](<#>), [Pirouette Lagrangian](<#>), [Cognitive Gravity Well](<#>)