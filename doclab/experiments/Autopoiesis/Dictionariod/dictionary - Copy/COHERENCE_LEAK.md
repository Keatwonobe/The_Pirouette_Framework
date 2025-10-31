---
term: "Coherence Leak"
canonical_id: "COHERENCE_LEAK"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-038"]
---

---
term: Coherence Leak
canonical_id: COHERENCE_LEAK
symbol: ΔK_τ < 0
aliases: [Negative Deficit, Systemic Drag]
parents: [DOMA-038]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-038
      lines: "L43-L45"
      snippet: |
        A **negative deficit (`ΔK_τ < 0`)** indicates an unmodeled source of Temporal Pressure or friction. The system is struggling more than the model can account for. This is a **Coherence Leak**.
  editors: [auto-compiler]
  review_log: []
triad:
  art: |
    A ship inexplicably loses speed, pulled by an unseen current not on any chart. This drag is the Coherence Leak—a measure of the hidden tides and frictions that the real world imposes upon an idealized course. It is the signature of an unmapped burden.
  law: |
    A persistent negative Coherence Deficit (ΔK_τ = K_τ_obs − K_τ_pred < 0) is a direct, measurable signal of unmodeled Temporal Pressure (Γ_shadow > 0) or internal dissonance. The integral of the leak over time quantifies the total action lost to these hidden forces.
  philosophy: |
    A Coherence Leak is not a model failure but a discovery of cost. It forces a reconciliation between an idealized plan and the territory's true difficulty, revealing the hidden work, forgotten constraints, and systemic frictions that govern all real-world dynamics. It makes the invisible tax on a system's progress visible and thus manageable.
pirouette_definition: |
  A Coherence Leak is a specific instantiation of the Coherence Deficit where the observed Temporal Coherence (K_τ_obs) is persistently lower than the coherence predicted by a model's hypothesized Lagrangian (K_τ_pred). This negative deficit (ΔK_τ < 0) quantitatively measures the performance-degrading impact of unmodeled forces, typically hidden sources of Temporal Pressure (Γ) or internal dissonance. It is the primary diagnostic for identifying and characterizing the "pressure" terms of a system's Shadow Lagrangian (𝓛_shadow).
operational_definition:
  units: Joules (J) or other unit of Energy, consistent with the Lagrangian.
  symbol_table:
    - name: ΔK_τ
      meaning: Coherence Deficit; the value of the leak when negative.
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
    - name: K_τ_obs
      meaning: Observed Temporal Coherence of the system.
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
    - name: K_τ_pred
      meaning: Predicted Temporal Coherence from the model Lagrangian (𝓛̂_model).
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
  measurement:
    procedures:
      - name: Deficit Calculation
        outline: |
          1. Define a model Lagrangian (𝓛̂_model) for the system.
          2. Use the model to predict the ideal coherence trajectory, K_τ_pred(t).
          3. Empirically measure the system's actual coherence trajectory, K_τ_obs(t), from real-world data.
          4. Calculate the Coherence Deficit: ΔK_τ(t) = K_τ_obs(t) − K_τ_pred(t).
          5. A persistent negative value, ΔK_τ(t) < 0, confirms and quantifies a Coherence Leak.
        expected_signals: [A time-series consistently below zero, correlations between leak magnitude and specific external events or internal states.]
        pitfalls: [Model misspecification (a bad model creating an artificial leak), measurement noise in K_τ_obs obscuring the signal, insufficient observation time to confirm persistence.]
context_windows:
  - module: DOMA-038
    excerpt: |
      A negative deficit (`ΔK_τ < 0`) indicates an unmodeled source of Temporal Pressure or friction. The system is struggling more than the model can account for. This is a **Coherence Leak**.
  - module: DOMA-038
    excerpt: |
      The sources of this dark matter typically fall into three categories: 1. Unmodeled Pressure (Hidden Γ): The system's environment contains a source of temporal pressure—a hidden constraint, a competitor, a social friction—that was not included in our model of V_Γ. The system is fighting a current our map does not show.
poetic_connections:
  motifs: [friction, drag, shadow cost, hidden burden, unseen current, dissipation, viscosity]
  evocative_lines:
    - "The system is fighting a current our map does not show."
    - "The shadow of the map is a compass, pointing not to what is known, but to what is knowable."
  association_matrix:
    - [ "COHERENCE_DEFICIT", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "SHADOW_LAGRANGIAN", 0.7 ]
    - [ "COHERENCE_SPRING", -1.0 ]
formal_mappings:
  candidates:
    - target: Dissipative force term (e.g., -γẋ)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        L = L_conservative - L_dissipative
        A Coherence Leak corresponds to an unaccounted-for L_dissipative > 0.
      justification: |
        In classical mechanics, dissipative forces like friction or drag remove energy from a system, preventing it from following a purely conservative (ideal) trajectory. A Coherence Leak plays the same role: it quantifies the "drag" from unmodeled pressures that reduce a system's achieved coherence below its modeled potential.
      references:
        - title: Classical Mechanics
          where: Chapter on non-conservative forces
          date: 1950-01-01
      confidence: 0.8
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A persistent Coherence Leak is always caused by a physical or systemic interaction that was omitted from the model Lagrangian."
      domain: theory
      falsifier: "Discovering a system where ΔK_τ < 0 is a fundamental, irreducible property of the system's evolution, not attributable to any missing interaction term. This would challenge the completeness assumption of the Lagrangian refinement process."
      status: proposed
      links: [DOMA-038]
    - statement: "Mitigating the real-world source of a Coherence Leak (e.g., reducing friction, removing a constraint) will measurably decrease the magnitude of the observed |ΔK_τ|."
      domain: phenomenology
      falsifier: "An intervention designed to mitigate a hypothesized source of a leak has no effect on the measured ΔK_τ, indicating the hypothesis about the source was incorrect."
      status: proposed
naming_notes:
  collisions: [Data leak (Machine Learning)]
  disambiguation: |
    Unlike a "data leak" in machine learning where information improperly flows between datasets, a Coherence Leak refers to a loss or "leakage" of a system's potential coherence due to unmodeled real-world pressures. It is a concept of system dynamics, not information security.
crosslinks:
  near_synonyms: []
  antonyms: [COHERENCE_SPRING]
  prerequisites: [COHERENCE_DEFICIT, TEMPORAL_PRESSURE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [LAGRANGIAN_REFINEMENT]
license: CC-BY-SA-4.0
---

# Coherence Leak

## Canonical (Pirouette)
A Coherence Leak is a specific instantiation of the Coherence Deficit where the observed Temporal Coherence (K_τ_obs) is persistently lower than the coherence predicted by a model's hypothesized Lagrangian (K_τ_pred). This negative deficit (ΔK_τ < 0) quantitatively measures the performance-degrading impact of unmodeled forces, typically hidden sources of Temporal Pressure (Γ) or internal dissonance. It is the primary diagnostic for identifying and characterizing the "pressure" terms of a system's Shadow Lagrangian (𝓛_shadow).

## EFT-First Summary
A Coherence Leak is conceptually analogous to the effect of a **dissipative force** (like friction or viscosity) in a classical mechanical system. Just as friction causes a system to lose energy and deviate from its ideal, energy-conserving path, a Coherence Leak signals that unmodeled pressures are causing a system to achieve less coherence than its idealized model predicts. The leak quantifies the "energy" lost to these hidden drag-like interactions, prompting a search for the missing dissipative terms in the system's effective Lagrangian.

## Glossary Links
- See also: Coherence Deficit, Coherence Spring, Temporal Pressure, Shadow Lagrangian