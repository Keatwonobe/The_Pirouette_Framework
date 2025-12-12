---
term: "Ki_dynamic"
canonical_id: "KI_DYNAMIC"
symbol: ""
aliases: [The Outward Song]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-149"]
---

---
term: Ki_dynamic
canonical_id: KI_DYNAMIC
symbol: K_{i,dynamic}
aliases: [The Outward Song]
parents: [DOMA-149]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-149
      lines: "L30-L34"
      snippet: |
        **Ki_dynamic (The Outward Song):** This is the resonant pattern that maximizes coherence when the system is in motion. It is an externally-focused harmony, optimized for efficient propagation along a geodesic on the coherence manifold. Its structure is shaped to surf the surrounding currents with minimal friction; it is the resonance of being *on a path*.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    The resonance of a body in flight, a song shaped not for its own chamber but for the open air. It is the harmony of a river, finding the path of least resistance not by force, but by becoming one with the flow.
  law: |
    For any system capable of motion, there exists a discrete, stable Temporal Resonance pattern, K_{i,dynamic}, which maximizes its coherence and minimizes propagation friction while in motion relative to its environment. A system must undergo a non-linear phase transition (the Inertial Leap) to occupy this state.
  philosophy: |
    Ki_dynamic represents the state of *becoming* rather than *being*. It embodies the principle that existence is not monolithic; a system must adopt a different mode of being to effectively navigate and interact with the world, trading the deep stability of stasis for the efficient harmony of passage.
pirouette_definition: |
  The stable, externally-focused Temporal Resonance pattern (Ki) that maximizes a system's coherence during propagation. As one of two fundamental solutions to the Pirouette Lagrangian for a given system, it is optimized for efficient travel along a geodesic on the coherence manifold. A system transitions to this state from Ki_static via the Inertial Leap, a non-linear phase change that requires overcoming an activation energy barrier.
operational_definition:
  units: Dimensionless (Coherence Ratio)
  symbol_table:
    - name: K_{i,dynamic}
      meaning: The Temporal Resonance pattern of a system in its stable dynamic state.
      dimensions: dimensionless
      default_range: contextual, typically a positive real number
  measurement:
    procedures:
      - name: Hysteretic Loop Spectroscopy
        outline: |
          1. Prepare a system at rest in a controlled environment and measure its baseline Temporal Resonance, establishing K_{i,static}.
          2. Apply a gradually increasing external force to induce motion, monitoring the system's velocity (v) and its composite Ki(v).
          3. Identify the sharp, non-linear increase in Ki at the critical velocity (v_c↑). The new, stable Ki value post-transition is K_{i,dynamic}.
          4. Gradually decrease the applied force, allowing the system to decelerate. Observe that the system remains at K_{i,dynamic} until a lower critical velocity (v_c↓), confirming hysteresis and the stability of the dynamic state.
        expected_signals: [Step-function change in measured Ki, Hysteresis loop in the Ki-v plot]
        pitfalls: [Insufficient energy to overcome the Coherence Dam, Environmental noise masking the discrete 'snap' of the transition]
context_windows:
  - module: DOMA-149
    excerpt: |
      **Ki_dynamic (The Outward Song):** This is the resonant pattern that maximizes coherence when the system is in motion. It is an externally-focused harmony, optimized for efficient propagation along a geodesic on the coherence manifold. Its structure is shaped to surf the surrounding currents with minimal friction; it is the resonance of being *on a path*.
  - module: DOMA-149
    excerpt: |
      `Ki_static` and `Ki_dynamic` represent two distinct peaks, or "local maxima," of coherence on this landscape. The Coherence Dam is the potential energy barrier...that separates them. The Inertial Leap is the jump from one peak to another, occurring when the system calculates that the path through the `Ki_dynamic` maximum will yield a higher net coherence, even accounting for the energy cost of the leap.
poetic_connections:
  motifs: [flow, journey, propagation, harmony-with-environment, surfing, pathfinding, song-of-the-road]
  evocative_lines:
    - "it is the resonance of being *on a path*."
    - "motion is the art of convincing the past to let go."
    - "Its structure is shaped to surf the surrounding currents with minimal friction."
  association_matrix:
    - [ "KI_STATIC", 1.0 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "INERTIAL_LEAP", 0.9 ]
    - [ "HYSTERESIS", 0.7 ]
formal_mappings:
  candidates:
    - target: Soliton or traveling wave solution
      domain: Math|EFT
      mapping_kind: conceptual|mathematical
      equation_hint: |
        \phi(x, t) = f(x - vt)
      justification: |
        A soliton is a stable, self-reinforcing wave packet that maintains its shape while propagating at a constant velocity. Like Ki_dynamic, it is a specific, non-dispersive solution to a non-linear Lagrangian, representing a system in a coherent state of motion, distinct from a static or dispersive state.
      references:
        - title: Solitons and Instantons
          where: "Chapter 1"
          date: 1982-01-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system in the K_{i,dynamic} state experiences lower propagation friction (i.e., less coherence loss per unit distance) than a system forced to move at the same velocity without having undergone the Inertial Leap."
      domain: experiment|phenomenology
      falsifier: "Observation of a system whose propagation efficiency is a smooth, continuous function of velocity, with no discrete 'snap' or evidence of a distinct, more efficient dynamic state. Or, if the post-snap state is measured to be less efficient."
      status: proposed
      links: [DOMA-149]
naming_notes:
  collisions: []
  disambiguation: |
    Ki_dynamic is not simply "the value of Ki while a system is moving." It is a discrete, stable, and fundamentally different *mode* of resonance, analogous to a distinct phase of matter. It should be contrasted with Ki_static, its counterpart state of rest. The transition between them is a non-linear leap, not a smooth ramp.
crosslinks:
  near_synonyms: []
  antonyms: [KI_STATIC]
  prerequisites: [TEMPORAL_RESONANCE, WOUND_CHANNEL, PIROUETTE_LAGRANGIAN]
  downstream_effects: [HYSTERESIS, INERTIAL_LEAP, ACTIVATION_ENERGY]
license: CC-BY-SA-4.0
---