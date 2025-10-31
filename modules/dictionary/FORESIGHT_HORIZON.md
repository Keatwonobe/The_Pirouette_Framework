---
term: "Foresight Horizon"
canonical_id: "FORESIGHT_HORIZON"
symbol: "τ_σ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-086"]
---

---
term: Foresight Horizon
canonical_id: FORESIGHT_HORIZON
symbol: τ_σ
aliases: [Predictive Horizon]
parents: [DOMA-086]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-086
      lines: "35-39"
      snippet: |
        Foresight Horizon (τ_σ): This is the temporal distance into the future over which a system's internal model of a Coherence Current remains stable and predictive. It is the measure of how far ahead the system can "see" the rhythm before its predictions dissolve back into uncertainty.
  editors: [synth-agent]
  review_log: []
triad:
  art: |
    The edge of the known future, the shimmering line where the melody of a Coherence Current dissolves into the noise of tomorrow. It is the furthest point a system can see by the light of its own understanding.
  law: |
    The Foresight Horizon, τ_σ, is the maximum time Δt for which a system's prediction P(t+Δt) of a Coherence Current C(t) remains within a specified error bound ε of the actual current: |P(t+Δt) - C(t+Δt)| < ε.
  philosophy: |
    Foresight Horizon quantifies the practical limit of an entity's intelligence. It establishes that foresight is not an infinite faculty but a bounded, dynamic capability—a measure of how much future a system can reliably grasp and act upon, making it the primary dimension of its temporal agency.
pirouette_definition: |
  The Foresight Horizon (τ_σ) is the temporal duration into the future for which an Observer's predictive model of a specific Coherence Current maintains an accuracy above a defined stability threshold. It quantifies the reach of a system's predictive power along a specific Flow Channel, representing the boundary between its modeled future and unmodeled uncertainty. An increase in τ_σ signifies successful learning and attunement to the environment's rhythms.
operational_definition:
  units: Time (seconds, cycles)
  symbol_table:
    - name: τ_σ
      meaning: Foresight Horizon for a specific Coherence Current σ.
      dimensions: T
      default_range: contextual
  measurement:
    procedures:
      - name: Crucible Protocol τ_σ Measurement
        outline: |
          An Observer's predictive subsystem (Prophet) is exposed to a controlled environment with a hidden Coherence Current. At discrete intervals, the Prophet's model is queried to predict the state of the current at a future time Δt. τ_σ is determined as the maximum Δt where the prediction error consistently remains below a pre-defined threshold (ε). This process is repeated to plot τ_σ over time as the system learns.
        expected_signals: [Time-series of prediction error, τ_σ(t) learning curve]
        pitfalls: [Overfitting the model to a short sample of the current, Choosing a stability threshold (ε) that is too permissive or too strict]
context_windows:
  - module: DOMA-086
    excerpt: |
      Foresight Horizon (τ_σ): This is the temporal distance into the future over which a system's internal model of a Coherence Current remains stable and predictive. It is the measure of how far ahead the system can "see" the rhythm before its predictions dissolve back into uncertainty. A higher τ_σ signifies a more refined and accurate internal model.
  - module: DOMA-086
    excerpt: |
      The system is rewarded not for mere task completion, but for maximizing its Resonance Efficiency (Φ_R). This is quantified by periodically testing the Prophet's Foresight Horizon (τ_σ) and rewarding its rate of increase per unit of action cost. A system's intelligence is not a final score, but the ascent rate and plateau of its τ_σ curve over time.
poetic_connections:
  motifs: [vision, boundary, rhythm]
  evocative_lines:
    - "To be intelligent is not to know the future, but to be in rhythm with it."
    - "We sought to define intelligence and found not a calculator, but a tuning fork."
  association_matrix:
    - [ "COHERENCE_CURRENT", 0.9 ]
    - [ "RESONANCE_EFFICIENCY", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates:
    - target: Lyapunov time (T_λ)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        τ_σ ≈ 1/λ_max
      justification: |
        Lyapunov time measures the characteristic timescale on which a dynamical system becomes unpredictable due to exponential divergence of nearby trajectories. This aligns directly with the Foresight Horizon's role as the limit of stable prediction before a system's model diverges from reality due to chaotic dynamics inherent in the Coherence Current.
      references:
        - title: "Nonlinear Dynamics and Chaos"
          where: "Strogatz, S. H. (2015). Section 9.3"
          date: 2015-01-01
      confidence: 0.8
  adopted:
    - target: Lyapunov time (T_λ)
      rationale: "The mapping to Lyapunov time provides a rigorous, falsifiable mathematical foundation from chaos theory for what is otherwise a conceptual term. It grounds the 'stability' of a prediction in the well-understood dynamics of error growth in complex systems."
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "For any given Coherence Current with a positive maximal Lyapunov exponent, the Foresight Horizon τ_σ is finite and fundamentally bounded."
      domain: theory
      falsifier: "The discovery of a learning system that can achieve an arbitrarily large or infinite τ_σ for a non-trivial chaotic Coherence Current, indicating its predictive error does not grow exponentially."
      status: proposed
      links: [DOMA-086]
naming_notes:
  collisions: [τ (time constant, lifetime), H (horizon, e.g., event horizon)]
  disambiguation: |
    τ_σ should not be confused with a generic time constant. It is not an intrinsic property of the system or the environment alone, but of the *interaction* between the system's predictive model and the environment's dynamics. It is a measure of predictive stability, not decay.
crosslinks:
  near_synonyms: []
  antonyms: [TEMPORAL_PRESSURE]
  prerequisites: [COHERENCE_CURRENT, OBSERVER]
  downstream_effects: [RESONANCE_EFFICIENCY, PATH_OF_COHERENCE]
license: CC-BY-SA-4.0
---

# Foresight Horizon

## Canonical (Pirouette)
The Foresight Horizon (τ_σ) is the temporal duration into the future for which an Observer's predictive model of a specific Coherence Current maintains an accuracy above a defined stability threshold. It quantifies the reach of a system's predictive power along a specific Flow Channel, representing the boundary between its modeled future and unmodeled uncertainty. An increase in τ_σ signifies successful learning and attunement to the environment's rhythms.

## EFT-First Summary
The Foresight Horizon (τ_σ) is operationally analogous to the Lyapunov time (T_λ) from chaos theory. It represents the characteristic timescale over which a system's predictive model of a Coherence Current remains valid before errors, growing exponentially at a rate determined by the current's maximal Lyapunov exponent, render the prediction useless. A high τ_σ implies the system has built a model that effectively mitigates or compensates for the underlying chaotic dynamics.

## Glossary Links
- See also: Coherence Current, Resonance Efficiency, Temporal Pressure