---
term: "Predicted Coherence"
canonical_id: "PREDICTED_COHERENCE"
symbol: "K_τ_pred(t)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-038"]
---

---
term: Predicted Coherence
canonical_id: PREDICTED_COHERENCE
symbol: K_τ_pred(t)
aliases: [Model Coherence, Ideal Coherence, On-Shell Coherence]
parents: [DOMA-038]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-038
      lines: "§3"
      snippet: |
        *   **`K_τ_pred(t)`** is the coherence the system *would have* exhibited if it had perfectly followed the geodesic dictated by the model's hypothesized Lagrangian, `𝓛̂_model`.
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    The perfect, frictionless path drawn on a map; the blueprint of a journey before it meets the mud and resistance of the real world.
  law: |
    The temporal coherence value calculated for the trajectory that extremizes the action (`S_p`) of a given hypothesized Lagrangian (`𝓛̂_model`). It is a theoretical construct, not a direct measurement.
  philosophy: |
    To make a theory falsifiable, it must first make a prediction. Predicted Coherence is the formal prediction of a system's model, a necessary and idealized baseline against which the messiness of reality is measured to reveal deeper truths.
pirouette_definition: |
  The theoretical, time-dependent Temporal Coherence (`K_τ`) a system would exhibit if its evolution perfectly followed the optimal path (geodesic) that maximizes the action integral of a specific, hypothesized Pirouette Lagrangian (`𝓛̂_model`). It serves as the model-generated baseline for calculating the Coherence Deficit (`ΔK_τ`).
operational_definition:
  units: dimensionless
  symbol_table:
    - name: K_τ_pred(t)
      meaning: Predicted Coherence at time `t`.
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: 𝓛̂_model
      meaning: The hypothesized Lagrangian of the system.
      dimensions: Coherence/Time
      default_range: contextual
    - name: t
      meaning: Time.
      dimensions: T
      default_range: contextual
    - name: τ
      meaning: The temporal scale or window over which coherence is measured.
      dimensions: T
      default_range: contextual
  measurement:
    procedures:
      - name: Computational Derivation from Hypothesized Lagrangian
        outline: |
          1. Define a hypothesized Lagrangian `𝓛̂_model = K_τ - V_Γ` for the system.
          2. Apply the principle of stationary action (e.g., via Euler-Lagrange equations) to `𝓛̂_model` to solve for the system's predicted trajectory, `q_pred(t)`.
          3. Calculate the `K_τ` component of the Lagrangian *along this predicted trajectory* `q_pred(t)`. This resulting time-series is `K_τ_pred(t)`.
        expected_signals: [A time-series representing the model's expectation of system coherence. Often smoother than the observed coherence.]
        pitfalls: [Ill-posed or non-integrable `𝓛̂_model`, Numerical instability in path-finding algorithms, Misidentification of the true action-extremizing path (e.g., finding a local instead of global maximum).]
context_windows:
  - module: DOMA-038
    excerpt: |
      ΔK_τ(t) = K_τ_obs(t) − K_τ_pred(t). Where: K_τ_obs(t) is the actual, measured coherence of the system at time t, derived from real-world data—the truth of the territory. K_τ_pred(t) is the coherence the system would have exhibited if it had perfectly followed the geodesic dictated by the model's hypothesized Lagrangian, 𝓛̂_model.
  - module: DOMA-038
    excerpt: |
      Predict: Calculate the system's optimal path and its corresponding predicted coherence, K_τ_pred(t). Observe: Measure the system's real-world behavior to determine its observed coherence, K_τ_obs(t). Measure the Shadow: Compute the Coherence Deficit time-series, ΔK_τ(t).
poetic_connections:
  motifs: [blueprint, map, ideal, hypothesis, prediction, shadow's source]
  evocative_lines:
    - "the map that redraws itself"
    - "a compass pointing not to what is known, but to what is knowable"
  association_matrix:
    - [ "HYPOTHESIZED_LAGRANGIAN", 0.9 ]
    - [ "COHERENCE_DEFICIT", 0.8 ]
    - [ "OBSERVED_COHERENCE", 0.7 ]
    - [ "SEMANTIC_DARK_MATTER", 0.5 ]
formal_mappings:
  candidates:
    - target: "On-shell" value of an observable
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        δS/δφ = 0 ⇒ φ_cl(x); K_pred = K[φ_cl(x)]
      justification: |
        In field theory, "on-shell" refers to configurations that satisfy the classical equations of motion (i.e., that extremize the action). `K_τ_pred` is the value of coherence calculated from this "on-shell" or classical path derived from the model Lagrangian.
      references: []
      confidence: 0.8
  adopted:
    - target: "On-shell" value of the coherence observable
      rationale: The mapping directly aligns the Pirouette concept of a path extremizing a model action with the well-established "on-shell" formalism in physics, where system behavior is determined by solutions to the equations of motion.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "For any computationally tractable, well-formed `𝓛̂_model`, a unique `K_τ_pred(t)` time-series can be calculated."
      domain: theory
      falsifier: "The existence of a class of physically relevant Lagrangians for which the action-extremizing path is non-unique, non-existent, or computationally intractable, preventing the calculation of a stable `K_τ_pred(t)`."
      status: proposed
      links: [DOMA-038, CORE-006]
naming_notes:
  collisions: [K is often used for kinetic energy in classical mechanics. The subscript τ and `_pred` label are critical for disambiguation.]
  disambiguation: |
    Predicted Coherence must not be confused with `OBSERVED_COHERENCE` (`K_τ_obs`), which is empirically measured from system data. `K_τ_pred` is a pure theoretical construct derived from a model (`𝓛̂_model`); it represents what *should* happen according to the model, not what *does* happen.
crosslinks:
  near_synonyms: []
  antonyms: [OBSERVED_COHERENCE]
  prerequisites: [HYPOTHESIZED_LAGRANGIAN, TEMPORAL_COHERENCE]
  downstream_effects: [COHERENCE_DEFICIT]
license: CC-BY-SA-4.0
---

# Predicted Coherence

## Canonical (Pirouette)
The theoretical, time-dependent Temporal Coherence (`K_τ`) a system would exhibit if its evolution perfectly followed the optimal path (geodesic) that maximizes the action integral of a specific, hypothesized Pirouette Lagrangian (`𝓛̂_model`). It serves as the model-generated baseline for calculating the Coherence Deficit (`ΔK_τ`).

## EFT-First Summary
Predicted Coherence is the conceptual equivalent of the "on-shell" value of the coherence observable in Effective Field Theory. Just as an on-shell configuration is a solution to the classical equations of motion derived from a Lagrangian, the Predicted Coherence is the value of `K_τ` calculated along the specific trajectory that extremizes the action of the model's hypothesized Lagrangian, `𝓛̂_model`. It represents the idealized, classical prediction of the model, which is then compared to observation to reveal unmodeled dynamics.

## Glossary Links
- See also: Coherence Deficit, Hypothesized Lagrangian, Observed Coherence