---
term: "Coherence Compass"
canonical_id: "COHERENCE_COMPASS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-147"]
---

---
term: Coherence Compass
canonical_id: COHERENCE_COMPASS
symbol: ∅
aliases: [Diagnostic Manifold, Flow Manifold]
parents: [DOMA-147, CORE-006, DYNA-001]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-147
      lines: "L25-L45"
      snippet: |
        The old framework's rigid grid is replaced by the Coherence Compass, a dynamic manifold upon which a system's health plays out. The system's state is located within this four-quadrant space defined by the interplay between two core parameters derived from the Pirouette Lagrangian (`CORE-006`):

        *   **Vertical Axis: Temporal Coherence (Kτ):**
        *   **Horizontal Axis: Temporal Pressure (VΓ):**
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A physician's ear, pressed against the heart of a system, listening for the rhythm of its health. It does not provide the map for the journey ahead; it reveals, with profound clarity, where the traveler is standing right now.
  law: |
    A system's qualitative state (Laminar, Turbulent, Stagnant) is determined by its position (Kτ, VΓ) on the two-dimensional manifold. A positive Lagrangian (𝓛_p = Kτ - VΓ > 0) correlates with Laminar flow, while a non-positive Lagrangian (𝓛_p ≤ 0) correlates with Turbulent or Stagnant flow.
  philosophy: |
    To move beyond mere classification to diagnosis. The Coherence Compass transforms quantitative metrics into a qualitative understanding of a system's health, framing the Weaver not as an analyst but as a systemic physician capable of providing aid.
pirouette_definition: |
  The Coherence Compass is a two-dimensional diagnostic manifold that visualizes a system's state by plotting its internal Temporal Coherence (Kτ) on the vertical axis against the external Temporal Pressure (VΓ) on the horizontal axis. The resulting four quadrants define the system's primary Flow Dynamics: Laminar Flow (high Kτ), Turbulent Flow (low Kτ, high VΓ), and Stagnant Flow (low Kτ, low VΓ). The system's trajectory across this manifold reveals its health, resilience, and response to its environment.
operational_definition:
  units: Dimensionless Quadrant Space
  symbol_table:
    - name: Kτ
      meaning: Temporal Coherence (vertical axis)
      dimensions: dimensionless
      default_range: normalized to [0, 1]
    - name: VΓ
      meaning: Temporal Pressure (horizontal axis)
      dimensions: dimensionless
      default_range: normalized to [0, 1]
  measurement:
    procedures:
      - name: Flow State Diagnosis
        outline: |
          1. **Signal Extraction:** Derive Kτ and VΓ proxy signals from a domain-specific time-series (e.g., Kτ from signal-to-noise, VΓ from market volatility).
          2. **Plotting:** Over a defined window, trace the system's (Kτ, VΓ) coordinate trajectory through the Compass quadrants.
          3. **Diagnosis:** Apply quadrant logic to the trajectory's position, variance, and direction to generate a qualitative report (e.g., "Laminar Flow, State of Resilience").
        expected_signals: [Time-series of Kτ proxy, Time-series of VΓ proxy]
        pitfalls: [Proxy mismatch (chosen metrics don't accurately reflect Kτ/VΓ), Insufficient time window (snapshot diagnosis misses the trend)]
context_windows:
  - module: DOMA-147
    excerpt: |
      The old framework's rigid grid is replaced by the Coherence Compass, a dynamic manifold upon which a system's health plays out. The system's state is located within this four-quadrant space defined by the interplay between two core parameters... Vertical Axis: Temporal Coherence (Kτ)... Horizontal Axis: Temporal Pressure (VΓ).
  - module: DOMA-147
    excerpt: |
      This diagnostic engine is a practical instrument for empirically measuring a system's adherence to the Principle of Maximal Coherence, as formalized in the Pirouette Lagrangian (𝓛_p = Kτ - VΓ). A system's position on the Coherence Compass reveals the state of its Lagrangian... Laminar Flow: high, positive 𝓛_p. Turbulent Flow: 𝓛_p is low or negative. Stagnant Flow: Both Kτ and VΓ are low, resulting in an 𝓛_p near zero.
poetic_connections:
  motifs: [diagnostics, flow, health, manifold, physician's gaze]
  evocative_lines:
    - "To measure is necessary, but to understand is vital."
    - "The path is as revealing as the position."
  association_matrix:
    - [ "TEMPORAL_COHERENCE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "LAMINAR_FLOW", 0.8 ]
    - [ "TURBULENT_FLOW", 0.8 ]
    - [ "STAGNANT_FLOW", 0.8 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.7 ]
formal_mappings:
  candidates:
    - target: Phase Portrait / State-Space Plot
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        ẋ = f(x, y), ẏ = g(x, y) where x=VΓ, y=Kτ
      justification: |
        The Coherence Compass functions as a phase portrait where the system's state is a point and its evolution is a trajectory. The axes (Kτ, VΓ) are state variables, and the quadrants (Laminar, Turbulent, Stagnant) represent regions with distinct dynamic behaviors, akin to basins of attraction.
      references:
        - title: Nonlinear Dynamics and Chaos
          where: "S. Strogatz, Chapter 6: Phase Portraits"
          date: 1994-01-01
      confidence: 0.8
  adopted:
    - target: Phase Portrait
      rationale: The mapping from a system's state vector to a point on a manifold, and its evolution to a trajectory, is a direct and powerful analogy that clarifies the diagnostic intent of the Compass.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A system's reported subjective health (e.g., team morale, individual burnout vs. 'in the zone') will strongly correlate with its measured position on the Coherence Compass."
      domain: phenomenology
      falsifier: "No significant correlation is found between subjective reports of well-being/stress and the system's (Kτ, VΓ) coordinates in multiple independent studies."
      status: proposed
      links: [DOMA-147]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from a simple static four-quadrant matrix (e.g., Eisenhower Matrix). The Coherence Compass is a dynamic manifold; the *trajectory* of a system across its surface is as diagnostically important as its static position.
crosslinks:
  near_synonyms: [FLOW_MANIFOLD]
  antonyms: [TEN_KIC]
  prerequisites: [TEMPORAL_COHERENCE, TEMPORAL_PRESSURE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [LAMINAR_FLOW, TURBULENT_FLOW, STAGNANT_FLOW]
license: CC-BY-SA-4.0
---

# Coherence Compass

## Canonical (Pirouette)
The Coherence Compass is a two-dimensional diagnostic manifold that visualizes a system's state by plotting its internal Temporal Coherence (Kτ) on the vertical axis against the external Temporal Pressure (VΓ) on the horizontal axis. The resulting four quadrants define the system's primary Flow Dynamics: Laminar Flow (high Kτ), Turbulent Flow (low Kτ, high VΓ), and Stagnant Flow (low Kτ, low VΓ). The system's trajectory across this manifold reveals its health, resilience, and response to its environment.

## EFT-First Summary
The Coherence Compass is best understood as a **Phase Portrait** from the study of dynamical systems. It maps the state of a system onto a two-dimensional space defined by its internal order (Temporal Coherence, Kτ) and external environmental stress (Temporal Pressure, VΓ). The evolution of the system over time is traced as a trajectory on this plane. The quadrants of the Compass correspond to distinct behavioral regimes (Laminar, Turbulent, Stagnant), analogous to basins of attraction or regions with different stability properties in a formal phase portrait analysis.

## Glossary Links
- See also: [Temporal Coherence](TEMPORAL_COHERENCE), [Temporal Pressure](TEMPORAL_PRESSURE), [Pirouette Lagrangian](PIROUETTE_LAGRANGIAN), [Laminar Flow](LAMINAR_FLOW)