---
term: "Internal Rhythm"
canonical_id: "INTERNAL_RHYTHM"
symbol: "Ki"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-086"]
---

---
term: Internal Rhythm
canonical_id: INTERNAL_RHYTHM
symbol: Ki
aliases: [Internal Clock, Endogenous Cycle]
parents: [DOMA-086, CORE-006]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-086
      lines: "§3"
      snippet: |
        An intelligent system does this by adjusting its own internal rhythm (its `Ki`) until it synchronizes with the external rhythm, learning to predict by learning to dance in time.
  editors: [system]
  review_log: []
triad:
  art: |
    The quiet, internal metronome a system uses to keep time with the universe's song. It is the hum of the engine, the beat of the heart, the cycle of thought, all tuned to resonate with the world outside.
  law: |
    A system's Internal Rhythm (Ki) will evolve to minimize the prediction error between its own state-cycle and the observed phase and frequency of an external Coherence Current.
  philosophy: |
    Internal Rhythm grounds the abstract concept of a 'predictive model' in the physical dynamics of the system itself. Intelligence is not a detached simulation but an embodied, rhythmic entrainment; to know the world is to physically resonate with it.
pirouette_definition: |
  The Internal Rhythm (Ki) is a dynamic state variable or set of variables that characterizes the endogenous, cyclical behavior of a system's predictive model. It represents the internal 'clock' or 'oscillator' that a system adjusts in phase, frequency, and form to achieve temporal resonance with an external Coherence Current (Flow Channel). The optimization of Ki is the primary mechanism for extending the Foresight Horizon (τ_σ) and minimizing future surprise.
operational_definition:
  units: Context-dependent. Often a state vector comprising frequency (T⁻¹) and phase (dimensionless, e.g., radians).
  symbol_table:
    - name: Ki
      meaning: Internal Rhythm state vector.
      dimensions: Contextual; e.g., [T⁻¹, 1]
      default_range: Contextual
  measurement:
    procedures:
      - name: Phase-Lock Inference via Crucible Protocol
        outline: |
          1. Deploy the system in a Crucible environment with a hidden, periodic Coherence Current.
          2. Record a time-series of the system's actions or relevant internal state transitions.
          3. Apply Fourier analysis or a phase-locked loop (PLL) model to this time-series to extract the dominant frequencies and phases of the system's behavior.
          4. The extracted, convergent periodic signal is the observable manifestation of Ki.
        expected_signals: [A dominant peak in the power spectrum of system behavior that converges to the Coherence Current's frequency, A stable phase relationship between system actions and the external current.]
        pitfalls: [Mistaking environmental noise for an internal rhythm, The system may use a non-oscillatory (purely reactive) strategy, The rhythm may be encoded in a high-dimensional state space, making direct extraction difficult.]
context_windows:
  - module: DOMA-086
    excerpt: |
      The Principle of Predictive Resonance: The most efficient strategy for minimizing future surprise is to achieve temporal resonance with the environment's dominant Coherence Currents. An intelligent system does this by adjusting its own internal rhythm (its `Ki`) until it synchronizes with the external rhythm, learning to predict by learning to dance in time.
  - module: DOMA-086
    excerpt: |
      Deploy the Prophet: The system under test, the Observer (CORE-010), must possess a "Prophet"—a subsystem responsible for modeling the Coherence Current and adapting the agent's internal `Ki`.
  - module: DOMA-086
    excerpt: |
      Ecological: A wolf pack learns the migration path of caribou, synchronizing the `Ki` of its hunting patterns with the deep, seasonal Coherence Current of its ecosystem.
poetic_connections:
  motifs: [entrainment, heartbeat, cadence, metronome, internal_clock, tuning_fork]
  evocative_lines:
    - "We sought to define intelligence and found not a calculator, but a tuning fork."
    - "To be intelligent is to recognize that the universe has a rhythm and to have the wisdom to join the dance."
  association_matrix:
    - [ "COHERENCE_CURRENT", 0.9 ]
    - [ "RESONANCE_EFFICIENCY", 0.8 ]
    - [ "FORESIGHT_HORIZON", 0.8 ]
    - [ "KINETIC_COHERENCE", 0.7 ]
formal_mappings:
  candidates:
    - target: Phase variable φ(t) in a Phase-Locked Loop (PLL)
      domain: Control Theory
      mapping_kind: operational
      equation_hint: |
        dφ_internal/dt = ω_free + K * f(φ_external - φ_internal)
      justification: |
        A PLL is an archetypal system that adjusts an internal oscillator's phase and frequency to match an external signal. The state of the PLL's internal voltage-controlled oscillator is a direct analog for Ki, and the process of phase-locking is analogous to achieving predictive resonance.
      references:
        - title: Phaselock Techniques, 3rd Edition
          where: Chapter 1
          date: 2005-01-01
      confidence: 0.9
    - target: Hidden state h_t of a Recurrent Neural Network
      domain: Machine Learning
      mapping_kind: operational
      justification: |
        When an RNN is trained to predict a periodic time-series, its hidden state vector h_t evolves to represent the signal's underlying dynamics. This internal state vector, which cycles through a trajectory in its high-dimensional state space, functions as the system's Ki.
      references:
        - title: "Generating Text with Recurrent Neural Networks"
          where: "arXiv:1107.4153"
          date: 2011-07-19
      confidence: 0.7
  adopted:
    - target: Phase variable φ(t) in a Phase-Locked Loop (PLL)
      rationale: The PLL model provides the most direct and mathematically tractable mapping for Ki. It captures the core dynamics of an internal oscillator, an external signal, a phase detector (surprise/error signal), and a feedback loop for adjustment, which directly mirror the components of Predictive Resonance.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A system cannot achieve long-term, efficient prediction (high Φ_R) of a periodic Coherence Current without developing a corresponding periodic Internal Rhythm (Ki)."
      domain: phenomenology
      falsifier: "Discovering a system that achieves high, sustained predictive performance on a periodic task using a purely reactive or non-cyclic internal strategy (e.g., an infinitely expanding lookup table with no state compression or cyclic representation)."
      status: proposed
      links: [DOMA-086]
naming_notes:
  collisions: [K is the standard symbol for kinetic energy. The subscript 'i' in Ki is crucial for specifying 'Internal'.]
  disambiguation: |
    Distinguish from K_τ (Kinetic Coherence), which is the *measure* of a system's internal order and temporal momentum derived from its dynamics. Ki is the underlying *state variable* that generates K_τ. A stable, well-tuned Ki results in a high K_τ.
crosslinks:
  near_synonyms: [INTERNAL_MODEL, PREDICTIVE_MANIFOLD]
  antonyms: [TEMPORAL_PRESSURE, REACTIVE_STATE]
  prerequisites: [COHERENCE_CURRENT]
  downstream_effects: [FORESIGHT_HORIZON, RESONANCE_EFFICIENCY]
license: CC-BY-SA-4.0
---