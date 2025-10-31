---
term: "Wound Channel Inertia"
canonical_id: "WOUND_CHANNEL_INERTIA"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-185"]
---

---
term: Wound Channel Inertia
canonical_id: WOUND_CHANNEL_INERTIA
symbol: I_wc
aliases: [Modal Memory, Habitual Inertia]
parents: [DOMA-185]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-185
      snippet: |
        Persistence in a mode carves a **Wound Channel** (CORE-011) into the manifold, geometrically deepening its basin over time. This increases the `Stability Depth`, making the state a "habit" that is gravitationally harder to leave. It is the memory of the state.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A river's memory, etched in stone. The more a path is walked, the deeper it becomes, until gravity itself guides the next footstep. This is the inertia of habit.
  law: |
    The stability depth of a modal basin increases as a function of the cumulative time integral of coherence within that basin. A system's history is physically inscribed onto its state landscape, creating a path-dependent resistance to change. `d(Δ𝓛_p)/dt_p ∝ 𝓛_p,m`.
  philosophy: |
    This mechanism grounds history and memory in the geometry of the system's dynamics. It asserts that what a system *has done* directly alters what it *can do* next. It is the physical basis for habit, practice, and entrenchment, turning transient states into enduring features of the landscape.
pirouette_definition: |
  A measure of a modal basin's historically-acquired resistance to change, distinct from its instantaneous stability. It is the geometric deepening of a basin on the Coherence Manifold, caused by the carving of a Wound Channel (CORE-011) through persistent occupation of the corresponding mode. This process increases the mode's Stability Depth (Δ𝓛_p), making it a more entrenched, "habitual" state that requires a larger perturbation to exit.
operational_definition:
  units: Units of Pirouette Lagrangian (𝓛_p), often dimensionless "Coherence".
  symbol_table:
    - name: I_wc
      meaning: Wound Channel Inertia; the portion of Stability Depth attributable to persistence.
      dimensions: Same as 𝓛_p
      default_range: "≥ 0"
    - name: Δ𝓛_p
      meaning: Stability Depth; the difference in coherence between a modal peak and the lowest adjacent saddle.
      dimensions: Same as 𝓛_p
      default_range: "> 0 for stable modes"
    - name: t_p
      meaning: Persistence Time; the cumulative time a system has spent in a given mode.
      dimensions: T
      default_range: "≥ 0"
  measurement:
    procedures:
      - name: Perturbative Titration over Time
        outline: |
          1. Identify a stable system mode (`Ki_m`).
          2. Hold the system in this mode for a duration `t_p`.
          3. Apply a calibrated dissonant injection (a perturbation) with incrementally increasing amplitude until a phase leap to a different mode is induced.
          4. The minimum perturbation amplitude required to cause the leap is a proxy for the current Stability Depth, `Δ𝓛_p(t_p)`.
          5. Repeat for various `t_p` values while holding external Temporal Pressure (Γ) constant.
          6. The increase in `Δ𝓛_p` as a function of `t_p` quantifies the accumulation of `I_wc`.
        expected_signals: [System state time-series, perturbation signal amplitude]
        pitfalls: [Failure to hold external Γ constant, misidentifying phase leaps, system noise obscuring the threshold]
context_windows:
  - module: DOMA-185
    excerpt: |
      **Wound Channel Inertia**: Persistence in a mode carves a **Wound Channel** (CORE-011) into the manifold, geometrically deepening its basin over time. This increases the `Stability Depth`, making the state a "habit" that is gravitationally harder to leave. It is the memory of the state.
  - module: DOMA-185
    excerpt: |
      For each mode, measure its resistance to perturbation to determine its `Stability Depth (Δ𝓛_p)`. Analyze its persistence over time to estimate the contribution of its `Wound Channel Inertia`. This reveals how "sticky" or habitual each state is.
poetic_connections:
  motifs: [habit, memory, grooves, path-dependence, entrenchment, gravity well, practice, scar tissue]
  evocative_lines:
    - "It is the memory of the state."
    - "A deeper basin requires more disruption to exit."
    - "Stability is not a prison, but a choice among many."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "STABILITY_DEPTH", 0.8 ]
    - [ "COHERENCE_MANIFOLD", 0.6 ]
    - [ "KI_MORPHOGENESIS", -0.7 ] # Inertia resists this
formal_mappings:
  candidates:
    - target: Hebbian Learning / Spike-timing-dependent plasticity (STDP)
      domain: Neuroscience|CompSci
      mapping_kind: conceptual
      equation_hint: |
        Δw_ij ∝ a_i * a_j
      justification: |
        Hebbian learning posits that repeated, persistent activation of a neural pathway strengthens its synaptic connections. This is a direct analog to Wound Channel Inertia, where persistent occupation of a modal basin (equivalent to a stable pattern of neural activity) strengthens its stability (equivalent to synaptic weights), making that pattern more likely to recur and harder to disrupt.
      references:
        - title: The Organization of Behavior
          where: Hebb, D.O. (1949)
          date: 1949-01-01
      confidence: 0.8
    - target: Work hardening (strain hardening)
      domain: Materials Science
      mapping_kind: conceptual
      justification: |
        In work hardening, plastic deformation of a metal increases its resistance to further deformation. Similarly, the "work" of maintaining a coherent mode for a period of time hardens the system's state against perturbations that would deform it into a new state. Both are forms of path-dependent resistance acquired through the system's history.
      references: []
      confidence: 0.6
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The Stability Depth (Δ𝓛_p) of a modal basin increases monotonically with the cumulative persistence time (t_p) spent in that basin, holding external Temporal Pressure (Γ) constant."
      domain: phenomenology
      falsifier: "Demonstration of a system where prolonged, uninterrupted occupation of a stable mode systematically decreases its Stability Depth ('modal fatigue') or has no effect, under constant external conditions."
      status: proposed
      links: [DOMA-185]
naming_notes:
  collisions: [Moment of inertia (I), Electrical current (I)]
  disambiguation: |
    Wound Channel Inertia is not the physical inertia (mass) of a system's components. It is an emergent property of the system's *state* on the Coherence Manifold, representing a resistance to a *change in mode*, not a resistance to a change in motion. The "inertia" is one of habit or configuration.
crosslinks:
  near_synonyms: []
  antonyms: [Modal Fluidity, State-Space Annealing]
  prerequisites: [WOUND_CHANNEL, STABILITY_DEPTH, COHERENCE_MANIFOLD, MODAL_BASIN]
  downstream_effects: [KI_MORPHOGENESIS] # Inertia increases the cost/barrier for Ki Morphogenesis
license: CC-BY-SA-4.0
---