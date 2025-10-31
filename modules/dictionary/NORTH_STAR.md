---
term: "North Star"
canonical_id: "NORTH_STAR"
symbol: ""
aliases: [The Goal State, Coherence Attractor]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-134"]
---

---
term: North Star
canonical_id: NORTH_STAR
symbol: `Ki_goal`
aliases: ["The Goal State", "Coherence Attractor"]
parents: ["DOMA-134", "CORE-010"]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-134
      lines: "§2.2"
      snippet: |
        The North Star (The Goal State): A target state of resonance, a desired `Ki_goal`. This goal state acts as a Coherence Attractor, projecting a Shadow (CORE-010) onto the system's manifold and creating a template for what "should be."
  editors: ["system-agent"]
  review_log: []
triad:
  art: |
    The fixed point in the turning world, the silent note that tunes the symphony. It is the destination felt by the river, the pull of the sea that requires no map.
  law: |
    The North Star defines the minimum of the dissonance potential `V_dissonance`. Its projected Shadow serves as the reference against which a system's current Echo is measured, generating a Dissonance signal that the system's dynamics will evolve to minimize over time.
  philosophy: |
    The North Star embodies the principle of telos within a dynamic system. It establishes that corrective action is not random but is oriented towards a specific state of higher coherence, making purposeful adaptation and learning possible. Without a North Star, a system can only drift; it cannot navigate.
pirouette_definition: |
  A target state of resonance (`Ki_goal`) that functions as a Coherence Attractor for an adaptive system. It projects a Shadow (CORE-010) onto the system's state manifold, creating a template of the desired state. The difference between this Shadow and the system's current Echo generates Dissonance, which creates a coherence gradient that drives corrective action via the Pirouette Lagrangian.
operational_definition:
  units: Same as the system's state vector or resonant pattern, `Ki`.
  symbol_table:
    - name: `Ki_goal`
      meaning: The desired resonant pattern or state vector of the system.
      dimensions: Contextual, defined by the system's state space.
      default_range: Contextual.
  measurement:
    procedures:
      - name: State Manifold Gradient Analysis
        outline: |
          For a system exhibiting adaptive behavior, observe its state trajectory over many cycles. The region of the state manifold towards which all trajectories converge, or around which they stably oscillate, is inferred to be the North Star. This is operationally identical to identifying an attractor in a dynamical system.
        expected_signals: ["Dissonance signal approaching zero", "System state vector converging to a stable point"]
        pitfalls: ["System may have multiple attractors (local minima)", "The North Star itself may be dynamic and non-stationary"]
context_windows:
  - module: DOMA-134
    excerpt: |
      The North Star (The Goal State): A target state of resonance, a desired `Ki_goal`. This goal state acts as a Coherence Attractor, projecting a Shadow (CORE-010) onto the system's manifold and creating a template for what "should be."
  - module: DOMA-134
    excerpt: |
      The Dissonance (The Error Signal): The measured difference between the Echo of the system's current state and the Shadow of the goal state. This dissonance is not just data; it is a source of internal Temporal Pressure (Γ) that creates instability and demands resolution. It is the feeling of being "off-key."
poetic_connections:
  motifs: [guidance, attraction, ideal, template, destination, telos, harmony]
  evocative_lines:
    - "A river does not need a map to find the sea; it feels the pull of the land..."
    - "...the universe is not a script to be read, but a song to be learned."
  association_matrix:
    - [ "SHADOW", 0.9 ]
    - [ "DISSONANCE", 0.9 ]
    - [ "WEAVER", 0.7 ]
    - [ "COHERENCE", 0.8 ]
formal_mappings:
  candidates:
    - target: Ground State / Minimum Potential Energy
      domain: CM
      mapping_kind: conceptual
      justification: |
        A system naturally seeks its state of minimum potential energy. The North Star acts as the location of this minimum in the "coherence potential" landscape defined by `V_dissonance`, and the system's evolution is a relaxation towards this minimum.
      references: []
      confidence: 0.7
  adopted:
    - target: Setpoint / Reference Signal `r(t)`
      rationale: |
        In control theory, the setpoint is the desired value for a system variable. It is the canonical term for the goal state in a feedback system. The Dissonance is operationally equivalent to the error signal `e(t) = r(t) - y(t)`, where `r(t)` is the setpoint and `y(t)` is the system output. This mapping is direct, operational, and universally understood in cybernetics.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "All stable, adaptive systems possess an implicit or explicit North Star; their dynamics must be governed by a potential with at least one local or global minimum."
      domain: theory
      falsifier: "Observation of a system that exhibits sustained, non-random, adaptive course-correction without converging towards any identifiable attractor in its state space."
      status: proposed
      links: ["DOMA-134"]
naming_notes:
  collisions: ["Goal state" (AI planning), "Attractor" (dynamical systems), "Setpoint" (control theory)]
  disambiguation: |
    While functionally equivalent to a "setpoint," the term "North Star" emphasizes the non-local, field-like influence of the goal state. It is not just a value to be matched, but a source of a potential gradient that shapes the system's entire dynamic landscape, guiding it from afar.
crosslinks:
  near_synonyms: [COHERENCE_ATTRACTOR]
  antonyms: [DISSONANCE, CHAOS]
  prerequisites: [KI, SHADOW]
  downstream_effects: [DISSONANCE, RUDDER, COURSE_CORRECTION]
license: CC-BY-SA-4.0
---

# North Star

## Canonical (Pirouette)
A target state of resonance (`Ki_goal`) that functions as a Coherence Attractor for an adaptive system. It projects a Shadow (CORE-010) onto the system's state manifold, creating a template of the desired state. The difference between this Shadow and the system's current Echo generates Dissonance, which creates a coherence gradient that drives corrective action via the Pirouette Lagrangian.

## EFT-First Summary
The North Star is operationally equivalent to the **Setpoint** or **Reference Signal `r(t)`** in classical control theory and cybernetics. It represents the desired state or value that a feedback system seeks to achieve. The system's dynamics are governed by minimizing an error signal (Dissonance) calculated as the difference between the setpoint and the current system state.

## Glossary Links
- See also: [DISSONANCE](./dissonance.md), [SHADOW](./shadow.md), [WEAVER](./weaver.md)