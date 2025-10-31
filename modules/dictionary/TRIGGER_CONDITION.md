---
term: "Trigger Condition"
canonical_id: "TRIGGER_CONDITION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-081"]
---

---
term: Trigger Condition
canonical_id: TRIGGER_CONDITION
symbol: 
aliases: []
parents: [DOMA-081]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-081
      lines: "50-53"
      snippet: |
        1.  **Trigger Condition:** The specific pattern of system state and Temporal Pressure (Γ) that activates the template. It is the signature of a situation where this shortcut is valid (e.g., "when Γ is high and rising, but internal coherence Kτ is stable").
  editors: [Cognitive Agent]
  review_log: []
triad:
  art: |
    The scent of rain on dry earth, the specific tension in the air before the storm breaks. It is the moment of recognition that precedes a reflex, transforming a complex world into a simple, immediate call to action.
  law: |
    A Trigger Condition is a boolean function of system state variables (e.g., Kτ, Γ, dΓ/dt) and their thresholds. When the function evaluates to true, it activates its corresponding Prescribed Action within a Geodesic Template.
  philosophy: |
    Universal laws are inert without context. The Trigger Condition provides this context, defining the precise 'when' and 'where' a simplified heuristic is not merely useful, but wiser than a more complex calculation that would arrive too late. It is the formal bridge between universal principle and timely, situated action.
pirouette_definition: |
  The specific, pre-defined pattern of system state variables, primarily Coherence (Kτ) and Temporal Pressure (Γ) and their derivatives, that activates a Geodesic Template. It acts as a computationally inexpensive pattern-matcher, identifying the precise circumstances under which a template's Prescribed Action is a valid and efficient approximation of a full Lagrangian analysis.
operational_definition:
  units: boolean (dimensionless)
  symbol_table:
    - name: Kτ
      meaning: System Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Γ
      meaning: Temporal Pressure
      dimensions: "T⁻¹"
      default_range: "contextual"
    - name: dΓ/dt
      meaning: Rate of change of Temporal Pressure
      dimensions: "T⁻²"
      default_range: "contextual"
  measurement:
    procedures:
      - name: State Vector Monitoring
        outline: |
          1. Continuously monitor the system's core state variables (Kτ, Γ, dΓ/dt).
          2. Define a set of thresholds and logical relationships for a specific template (e.g., `Γ > Γ_critical` AND `dΓ/dt > Γ_acceleration_threshold`).
          3. The Trigger Condition evaluates to 'true' when the live state vector satisfies these relationships.
        expected_signals: ["Boolean flag state change (false → true)", "Activation of associated Prescribed Action"]
        pitfalls: ["Thresholds set too sensitively, leading to false positives (thrashing).", "Thresholds set too coarsely, leading to missed activations (sluggishness).", "Ignoring higher-order derivatives, masking impending critical state changes."]
context_windows:
  - module: DOMA-081
    excerpt: |
      **Trigger Condition:** The specific pattern of system state and Temporal Pressure (Γ) that activates the template. It is the signature of a situation where this shortcut is valid (e.g., "when Γ is high and rising, but internal coherence Kτ is stable").
  - module: DOMA-081
    excerpt: |
      **The Turbulence Forecaster**
      > *Anticipate conditions for a phase transition and proactively allocate resources to stabilize the system through the change.*
      - **Trigger:** The rate of change of Γ is accelerating, signaling an impending shock.
      - **Action:** Pre-emptively allocate resources to core functions and stabilization protocols.
poetic_connections:
  motifs: [recognition, threshold, signature, key-in-lock, pattern-matching]
  evocative_lines:
    - "the skill to navigate by the compass when the storm is upon them"
    - "when Γ is high and rising, but internal coherence Kτ is stable"
  association_matrix:
    - [ "GEODESIC_TEMPLATE", 0.9 ]
    - [ "PRESCRIBED_ACTION", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "COHERENCE", 0.7 ]
formal_mappings:
  candidates:
    - target: Boundary Condition
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        e.g., f(x)|x=x₀
      justification: |
        A Trigger Condition defines a boundary in the system's state space where one dynamical regime (e.g., full calculation) ends and another (e.g., heuristic approximation) begins. It specifies the conditions under which a particular simplified solution, the Geodesic Template, is applicable.
      references: []
      confidence: 0.6
  adopted:
    - target: Activation Function / Heaviside Step Function (Θ)
      domain: Math|Control Theory
      mapping_kind: operational
      equation_hint: |
        Activation = Θ(f(Kτ, Γ, ...) - threshold)
      justification: |
        Like an activation function in a neural network or a step function in a control system, a Trigger Condition is a non-linear function that switches from an 'off' state (0) to an 'on' state (1) when a specific combination of input variables crosses a defined threshold. It translates a continuous state space into a discrete decision.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A well-defined Trigger Condition for a given domain reliably activates its Geodesic Template *before* a full Lagrangian calculation would yield the same conclusion, with a coherence loss remaining within the template's Coherence Bound."
      domain: phenomenology
      falsifier: "Observing a system where the trigger activates too late, after the optimal window for action has passed, or where its activation leads to an action that violates the Coherence Bound, resulting in catastrophic failure."
      status: proposed
      links: [DOMA-081]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from a generic 'condition' or 'event'. A Trigger Condition is a formal, pre-calculated component of a Geodesic Template, representing a specific, recurring dynamic for which a heuristic is a known-good response. It is not just any observed state.
crosslinks:
  near_synonyms: []
  antonyms: [UNIVERSAL_APPLICABILITY]
  prerequisites: [GEODESIC_TEMPLATE, TEMPORAL_PRESSURE, COHERENCE]
  downstream_effects: [PRESCRIBED_ACTION]
license: CC-BY-SA-4.0
---

# Trigger Condition

## Canonical (Pirouette)
The specific, pre-defined pattern of system state variables, primarily Coherence (Kτ) and Temporal Pressure (Γ) and their derivatives, that activates a Geodesic Template. It acts as a computationally inexpensive pattern-matcher, identifying the precise circumstances under which a template's Prescribed Action is a valid and efficient approximation of a full Lagrangian analysis.

## EFT-First Summary
Operationally, a Trigger Condition functions as an activation function or Heaviside step function applied to the system's state-space variables (e.g., Γ, Kτ). It is a non-linear predicate that evaluates to true only within a specific region of the state space, thereby activating a pre-computed heuristic response (the Prescribed Action). This maps continuous system dynamics to a discrete, computationally efficient decision point.

## Glossary Links
- See also: Geodesic Template, Prescribed Action, Temporal Pressure, Coherence