---
term: "Triaxial Lens"
canonical_id: "TRIAXIAL_LENS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XCM-000_crucible_template"]
---

---
term: Triaxial Lens
canonical_id: TRIAXIAL_LENS
symbol: (Γ, T_a, φ)
aliases: [Crucible Metrics, Γ-T_a-φ Framework]
parents: [XCM-000]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XCM-000
      lines: "II.3"
      snippet: |
        | Axis       | Description                             | Example Measures                                               |
        | ---------- | --------------------------------------- | -------------------------------------------------------------- |
        | Γ          | Power exerted / tools leveraged         | Total force used, energy consumed, resources spent             |
        | T_a        | Time-Adherence / coherence stability    | Fracture events, recovery time, entropy gradients              |
        | φ          | Phase / alignment with intended purpose | Goal deviation, motive transparency, synchronization with team |
  editors: [Agent-Scribe 7]
  review_log: []
triad:
  art: |
    A lens to see not just the force of a strike, but the clarity of its purpose and the integrity of the hand that held it. It distinguishes a brute victory from an elegant resolution, measuring the echo as much as the impact.
  law: |
    Any complete evaluation of a Crucible resolution must quantify the Power (Γ) exerted, the Coherence (T_a) maintained, and the Purpose-alignment (φ) achieved. An increase in Γ without corresponding stability or increase in T_a and φ constitutes a suboptimal, high-residue outcome.
  philosophy: |
    To shift evaluation from simplistic win/loss binaries to a nuanced understanding of performance quality. The Triaxial Lens prioritizes sustainable, coherent, and purpose-driven action over brute-force success, rewarding agents who can resolve conflict without fracturing the system or their own integrity.
pirouette_definition: |
  The Triaxial Lens is the standard three-dimensional metric framework for evaluating agent or system performance within a Pirouette Crucible. It measures: 1) **Γ (Gamma)**, the power, resources, or force exerted; 2) **T_a (Time-Adherence)**, the stability and coherence of the system under stress, particularly its ability to recover from fracture events; and 3) **φ (phi)**, the phase alignment with the scenario's intended purpose or shared goal. The framework is designed to value cooperative, high-coherence resolutions over high-power, low-coherence victories.
operational_definition:
  units: Context-dependent; often normalized to a dimensionless [0,1] scale for comparison.
  symbol_table:
    - name: Γ
      meaning: Power exerted; total energy or resources consumed to achieve an outcome.
      dimensions: Contextual (e.g., ML²T⁻² for energy).
      default_range: [0, ∞) before normalization.
    - name: T_a
      meaning: Time-Adherence; a measure of system coherence and resilience over time.
      dimensions: Dimensionless or Time (T).
      default_range: Typically normalized to [0, 1], where 1 is perfect coherence.
    - name: φ
      meaning: Phase; the degree of alignment with a stated goal or principle.
      dimensions: Dimensionless or Radians.
      default_range: Typically normalized to [0, 1], where 1 is perfect alignment.
  measurement:
    procedures:
      - name: Crucible Telemetry Analysis
        outline: |
          1. Instrument the Crucible environment to capture resource consumption (Γ), system state deviations and recovery times (T_a), and vector deviation from stated objectives (φ).
          2. Normalize raw data against a pre-defined baseline or theoretical maximum for the scenario.
          3. Plot the resulting (Γ, T_a, φ) vector in 3D outcome-space for post-trial analysis.
        expected_signals: [Spikes in Γ, dips in T_a during fracture events, drift in φ indicating mission creep.]
        pitfalls: [Mis-calibrating the baseline for φ, leading to false alignment signals; Confusing high system activity with low coherence (T_a).]
context_windows:
  - module: XCM-000
    excerpt: |
      Each crucible is a structured **challenge-scenario** that is:
      - Designed to test agents, individuals, or systems
      - Measured across a **triaxial lens** (Γ, T_a, φ)
      - Oriented toward **coherence and cooperation**, not just victory
  - module: XCM-000
    excerpt: |
      Describe a few likely outcomes and their implications:
      - "Crash and fragment"
      - "Success by force but low T_a"
      - "High-φ reframe that resolves without conflict"
      - "Unexpected innovation under constraint"
poetic_connections:
  motifs: [Clarity under pressure, Force vs. Finesse, Three-body problem, Signal integrity]
  evocative_lines:
    - "The goal is not success. The goal is synchronization in the face of stress."
    - "Would you burn the rope to save the knot?"
  association_matrix:
    - [ "CRUCIBLE", 0.9 ]
    - [ "COHERENCE", 0.8 ]
    - [ "RESIDUE", 0.6 ]
    - [ "PIRQUETTE_INTELLIGENCE_PROFILE", 0.7 ]
formal_mappings:
  candidates:
    - target: Action (S)
      domain: CM
      mapping_kind: conceptual
      equation_hint: Γ ∝ ∫ L dt
      justification: |
        Γ represents the total "effort" or "cost" to traverse a path in state space, analogous to how the Action principle in classical mechanics quantifies the total path-dependent cost. High Γ corresponds to a costly, brute-force trajectory.
      references:
        - title: "Classical Mechanics"
          where: "Goldstein, Chapter 2"
          date: 2002-01-01
      confidence: 0.5
    - target: Order Parameter (η)
      domain: Condensed Matter
      mapping_kind: conceptual
      justification: |
        T_a behaves like an order parameter, where T_a=1 represents a perfectly coherent, ordered state and T_a=0 represents a fractured, chaotic, or high-entropy state. Fracture events are analogous to phase transitions where the order parameter drops precipitously.
      references:
        - title: "Principles of Condensed Matter Physics"
          where: "Chaikin & Lubensky, Chapter 1"
          date: 2000-01-01
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Outcomes with high T_a and φ values are more memetically resilient and replicable (i.e., generate lower residue) than outcomes with high Γ and low T_a/φ."
      domain: phenomenology
      falsifier: "A longitudinal study of Crucible outcomes shows that high-power, 'brute force' solutions are consistently adopted and remembered as more successful and desirable archetypes than high-coherence, low-power solutions."
      status: proposed
      links: [XCM-000]
naming_notes:
  collisions: [Γ (photon; Gamma function), φ (golden ratio; scalar field)]
  disambiguation: |
    In this context, Γ is always Power/Resources, never a particle. T_a is specifically "Time-Adherence" and measures coherence stability, not simply the passage of time. φ represents purpose-alignment as a vector or phase lock, not a generic angle or scalar potential.
crosslinks:
  near_synonyms: []
  antonyms: [UNIAXIAL_EVALUATION, WIN_LOSS_BINARY]
  prerequisites: [CRUCIBLE]
  downstream_effects: [PIRQUETTE_INTELLIGENCE_PROFILE, RESIDUE, AUDIENCE_SENATE]
license: CC-BY-SA-4.0
---

# Triaxial Lens

## Canonical (Pirouette)
The Triaxial Lens is the standard three-dimensional metric framework for evaluating agent or system performance within a Pirouette Crucible. It measures: 1) **Γ (Gamma)**, the power, resources, or force exerted; 2) **T_a (Time-Adherence)**, the stability and coherence of the system under stress, particularly its ability to recover from fracture events; and 3) **φ (phi)**, the phase alignment with the scenario's intended purpose or shared goal. The framework is designed to value cooperative, high-coherence resolutions over high-power, low-coherence victories.

## EFT-First Summary
The Triaxial Lens provides a three-part state vector (Γ, T_a, φ) for evaluating system performance. Conceptually, it maps loosely to physical principles: Γ as the total Action or energetic cost of an operation, T_a as an order parameter measuring the system's coherence against entropic decay, and φ as the phase-lock between the system's trajectory and a target vector. This provides a qualitative framework for assessing not just the outcome, but the elegance and sustainability of the process.

## Glossary Links
- See also: [CRUCIBLE](link), [COHERENCE](link), [RESIDUE](link)