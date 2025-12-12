---
term: "Dynamic Parametric Gates"
canonical_id: "DYNAMIC_PARAMETRIC_GATES"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["PDM-001_the_boundary_condition"]
---

---
term: Dynamic Parametric Gates
canonical_id: DYNAMIC_PARAMETRIC_GATES
symbol: None (a set of thresholds)
aliases: [The Shield, Pre-Act Gating]
parents: [PDM-001-Sentinel_Protocol-v2.0]
children: [PDM-002-Simulation_Workshop_Implementation]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: PDM-001-Sentinel_Protocol-v2.0
      lines: "§4, Phase 1"
      snippet: |
        Phase 1: Pre-Act Gating (The Shield)
        * Mechanism: Before execution, any proposed action is evaluated against a set of Dynamic Parametric Gates.
        * Parameters: These gates define acceptable thresholds for: Time-Adherence ($T_a$), Gladiator Force ($\Gamma$), Ki-Modulated Interaction Rate ($K_i$), Cumulative Residue ($R_c$).
  editors: [Lexicographer-Agent-7]
  review_log: []
triad:
  art: |
    A living shield whose weave tightens around those who act recklessly and loosens for those who move in harmony. It does not merely block, but learns the shape of what it must contain.
  law: |
    An action is permitted to execute only if its defining parameters ($T_a, \Gamma, K_i$) and the actor's historical impact ($R_c$) fall within a set of continuously updated thresholds. Violations trigger elevated review.
  philosophy: |
    The gates embody Anticipatory Accountability by shifting responsibility from a post-hoc tribunal to a pre-emptive check. They ensure an actor's state of readiness and past conduct are evaluated *before* they can inflict harm.
pirouette_definition: |
  A set of adaptive, actor-specific thresholds applied to a proposed action prior to its execution. These gates, which measure an actor's internal coherence ($T_a$), boundary rigidity ($\Gamma$), interaction rate ($K_i$), and cumulative historical impact ($R_c$), are continuously recalibrated by the measured consequences (Wound Channels) of past actions. They function as a preventative control layer ("The Shield") within the Sentinel Protocol to enforce accountability dynamically.
operational_definition:
  units: A vector of heterogeneous thresholds; units are specific to each parameter.
  symbol_table:
    - name: $T_a$
      meaning: Time-Adherence; an actor's internal coherence and temporal stability.
      dimensions: Contextual (often dimensionless or normalized).
      default_range: [0, 1]
    - name: $\Gamma$
      meaning: Gladiator Force; an actor's boundary rigidity or resistance to perturbation.
      dimensions: Contextual (often force or energy).
      default_range: Contextual
    - name: $K_i$
      meaning: Ki-Modulated Interaction Rate; the proposed action's interaction frequency and intensity.
      dimensions: T⁻¹ (rate)
      default_range: Contextual
    - name: $R_c$
      meaning: Cumulative Residue; the integrated, time-decayed sum of an actor's past Wound Channels.
      dimensions: Action-dependent (integrated perturbation).
      default_range: [0, ∞)
  measurement:
    procedures:
      - name: Pre-Act Gating Check
        outline: |
          1. An actor proposes an action.
          2. The system retrieves the actor's current, specific Gate threshold values for $T_a, \Gamma, K_i, R_c$.
          3. The proposed action's parameters and the actor's state are compared against the Gate thresholds.
          4. If all parameters are within bounds, the action proceeds.
          5. If any threshold is exceeded, the action is paused and flagged for the Reflexive Boundary Ritual.
        expected_signals: [Binary pass/fail signal for action, Elevated review flag]
        pitfalls: [Overly restrictive gates stifling innovation (brittleness), Gate recalibration lagging behind novel gaming strategies (porosity)]
context_windows:
  - module: PDM-001-Sentinel_Protocol-v2.0
    excerpt: |
      Phase 1: Pre-Act Gating (The Shield)
      * Mechanism: Before execution, any proposed action is evaluated against a set of Dynamic Parametric Gates.
      * Function: Actions outside gate parameters are paused for elevated review. The gates are not static; they are continuously recalibrated by the feedback from Phase 4.
  - module: PDM-001-Sentinel_Protocol-v2.0
    excerpt: |
      An entity's history of creating residue, even if "compliant," will tighten its future gates. The sum of the harm is tracked, ensuring the "death by a thousand cuts" vector is closed.
  - module: PDM-001-Inversion_Proposal-v1.0
    excerpt: |
      Systems with a high [Cumulative Coherence Dividend] would experience wider, less restrictive Parametric Gates, granting them greater freedom and velocity of action.
poetic_connections:
  motifs: [adaptive armor, living threshold, conscience filter, the shield, brittle boundaries]
  evocative_lines:
    - "A system without a defined boundary is a system bleeding coherence into the void."
    - "An entity's history of creating residue... will tighten its future gates."
  association_matrix:
    - [ "CUMULATIVE_RESIDUE", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "ANTICIPATORY_ACCOUNTABILITY", 0.7 ]
    - [ "COHERENCE_DIVIDEND", 0.5 ]
formal_mappings:
  candidates:
    - target: Adaptive Control Thresholds
      domain: Control Theory
      mapping_kind: conceptual
      equation_hint: |
        Let U(t) be the control input (action). Allow U(t) if ||x(t), P_U|| < G(R_c(t)), where G is the Gate function dependent on state x and proposal P_U, with threshold G adapting based on cumulative error R_c.
      justification: |
        In adaptive control, system parameters are adjusted in real-time based on performance. The Dynamic Gates function similarly, where the "control law" (permission to act) has thresholds that are updated based on a history of measured system error (Residue).
      references:
        - title: Adaptive Control: Stability, Convergence and Robustness
          where: P. A. Ioannou & J. Sun, Prentice-Hall, 1996
          date: 1996-01-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Continuously tightening Gate thresholds based on an actor's Cumulative Residue ($R_c$) effectively prevents strategic gaming via cumulative micro-harm."
      domain: phenomenology
      falsifier: "A simulation demonstrates that actors can find exploits in the Gate recalibration algorithm itself, generating significant cumulative harm faster than the Gates can adapt and tighten."
      status: under-test
      links: [PDM-002-Simulation_Workshop_Implementation]
naming_notes:
  collisions: [Logic Gate (Electronics), Quantum Gate (Quantum Computing)]
  disambiguation: |
    In Pirouette, 'Gates' are not binary logical operators but adaptive, multi-parameter governance thresholds for actions. They are analogous to a dynamic risk policy or a variable-permeability membrane, not a simple on/off switch.
crosslinks:
  near_synonyms: []
  antonyms: [STATIC_BOUNDARY]
  prerequisites: [CUMULATIVE_RESIDUE, WOUND_CHANNEL, TIME_ADHERENCE, GLADIATOR_FORCE]
  downstream_effects: [REFLEXIVE_BOUNDARY_RITUAL, COHERENCE_DIVIDEND]
license: CC-BY-SA-4.0
---