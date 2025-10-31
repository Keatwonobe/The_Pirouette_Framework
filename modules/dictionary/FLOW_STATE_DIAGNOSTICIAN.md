---
term: "Flow State Diagnostician"
canonical_id: "FLOW_STATE_DIAGNOSTICIAN"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-147"]
---

---
term: Flow State Diagnostician
canonical_id: FLOW_STATE_DIAGNOSTICIAN
symbol: n/a
aliases: ["Diagnostic Engine", "TEN-KIC-1.0 (replaces)"]
parents: ["DYNA-001", "CORE-006"]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-147
      lines: "§1"
      snippet: |
        The Flow State Diagnostician is its direct evolution, serving as the interpretive heart of the modern framework. We do not seek to label a system; we seek to diagnose its health... It is the bridge from raw numbers to actionable wisdom, transforming the Weaver from a data analyst into a systemic physician.
  editors: ["GPT-4o (2025-10-18)"]
  review_log: []
triad:
  art: |
    A physician's ear pressed against the heart of a system, listening not for a label, but for the rhythm of its health—the effortless grace, resilient struggle, or silent decay within its flow.
  law: |
    The quantitative state of a system, defined by its coordinates of internal Temporal Coherence (Kτ) and external Temporal Pressure (VΓ), maps directly to one of three qualitative diagnoses: Laminar, Turbulent, or Stagnant Flow.
  philosophy: |
    To move beyond mere classification to active diagnosis. The goal is not to assign a static label but to understand a system's dynamic condition in relation to its environment, enabling intervention and fostering health.
pirouette_definition: |
  The Flow State Diagnostician is the primary interpretive engine of the Pirouette Framework. It ingests time-series data representing a system's internal Temporal Coherence (Kτ) and its external Temporal Pressure (VΓ), plotting the system's trajectory on the Coherence Compass. The engine translates these quantitative dynamics into a qualitative diagnosis of the system's health, classifying its state as Laminar, Turbulent, or Stagnant Flow.
operational_definition:
  units: Dimensionless classification (Laminar, Turbulent, Stagnant) and an associated diagnostic report.
  symbol_table:
    - name: Kτ
      meaning: Temporal Coherence; a measure of internal system order and integrity.
      dimensions: contextual
      default_range: "[0, ∞)"
    - name: VΓ
      meaning: Temporal Pressure; a measure of external environmental complexity and dissonance.
      dimensions: contextual
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: Flow State Diagnosis
        outline: |
          1. **Signal Extraction:** Derive Kτ and VΓ proxy signals from raw domain-specific time-series data.
          2. **Plotting & Quantification:** Over a defined time window, calculate the mean and variance of both signals, and trace the system's (Kτ, VΓ) trajectory on the Coherence Compass.
          3. **Diagnosis:** Apply the quadrant-based classification logic to generate a diagnostic report detailing the primary flow state and its interpretation.
        expected_signals: ["(Kτ, VΓ) time-series", "Primary Diagnosis {Laminar, Turbulent, Stagnant}", "Diagnostic Report"]
        pitfalls: ["Poor choice of proxy signals for Kτ or VΓ can lead to misdiagnosis.", "Failing to account for statistical variance; a low-variance Stagnant state can be mistaken for a transient low-coherence state."]
context_windows:
  - module: DOMA-147
    excerpt: |
      The old framework's rigid grid is replaced by the Coherence Compass, a dynamic manifold upon which a system's health plays out. The system's state is located within this four-quadrant space defined by the interplay between two core parameters derived from the Pirouette Lagrangian (`CORE-006`)...
  - module: DOMA-147
    excerpt: |
      This diagnostic engine is a practical instrument for empirically measuring a system's adherence to the Principle of Maximal Coherence... A system's position on the Coherence Compass reveals the state of its Lagrangian, which represents its total coherence and ability to follow its geodesic (its optimal path).
poetic_connections:
  motifs: ["physician's gaze", "systemic health", "coherence compass", "flow dynamics"]
  evocative_lines:
    - "To name a thing is to claim a shallow power over it. To diagnose it is to understand its struggle."
    - "It is a physician's ear, pressed against the heart of a system, listening for the rhythm of its health."
  association_matrix:
    - [ "COHERENCE_COMPASS", 1.0 ]
    - [ "TEMPORAL_COHERENCE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.7 ]
formal_mappings:
  candidates:
    - target: Phase Diagram (e.g., P-T diagram)
      domain: SM
      mapping_kind: conceptual
      justification: |
        The Coherence Compass functions as a phase diagram for system health. It uses two state variables (Kτ, VΓ) as axes to partition a state space into distinct qualitative phases (Laminar, Turbulent, Stagnant), analogous to how a P-T diagram classifies matter into solid, liquid, or gas phases based on pressure and temperature.
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system's state of health and its probable trajectory can be sufficiently diagnosed by plotting its internal Temporal Coherence (Kτ) against its external Temporal Pressure (VΓ)."
      domain: phenomenology
      falsifier: "Discovery of a system whose critical failure mode or state of health is orthogonal to both Kτ and VΓ. For example, a system could exhibit high Kτ and low VΓ (Laminar Grace) but be pathologically isolated, a condition not captured by the two primary axes, leading to a false-positive diagnosis of health."
      status: supported
      links: ["DOMA-147"]
naming_notes:
  collisions: ["The term 'Flow State' is widely used in psychology to describe a state of deep focus and immersion (Csikszentmihalyi)."]
  disambiguation: |
    Pirouette's 'Flow State' is a technical, systemic diagnosis applicable to any system (e.g., ecological, economic, computational), not exclusively a state of human consciousness. While a person experiencing psychological flow would likely be diagnosed as having Laminar Flow, the terms are not interchangeable.
crosslinks:
  near_synonyms: ["SYSTEM_HEALTH_MONITOR"]
  antonyms: ["RAW_DATA_LOGGER"]
  prerequisites: ["TEMPORAL_COHERENCE", "TEMPORAL_PRESSURE", "COHERENCE_COMPASS", "PIROUETTE_LAGRANGIAN"]
  downstream_effects: ["STRATEGIC_INTERVENTION_PLANNING"]
license: CC-BY-SA-4.0
---