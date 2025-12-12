---
term: "Lagrangian of Intent"
canonical_id: "LAGRANGIAN_OF_INTENT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-064"]
---

---
term: Lagrangian of Intent
canonical_id: LAGRANGIAN_OF_INTENT
symbol: 𝓛_I
aliases: [Objective Function of Influence]
parents: [DOMA-064, CORE-006]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-064
      snippet: |
        The ethical and physical distinction between these two modes is not a matter of opinion; it is a mathematical certainty, governed by the system's objective function...
        Maximize  ∫ ( 𝓛_p(System A) + 𝓛_p(System B) ) dt
        Maximize  ∫ ( 𝓛_p(Actor) - 𝓛_p(Target) ) dt
  editors: [AI Agent]
  review_log: []
triad:
  art: |
    To speak is to alter another's world. The Lagrangian of Intent asks a simple question with every word: are you building a shared cathedral, or are you mining another's soul for stone?
  law: |
    An influence interaction is governed by an objective function that seeks to maximize an action. Persuasion maximizes the summed coherence of the participants (∫(𝓛_A + 𝓛_B)dt). Manipulation maximizes the manipulator's coherence at the expense of the target's (∫(𝓛_Actor - 𝓛_Target)dt).
  philosophy: |
    Ethics are not an arbitrary overlay on dynamics but an emergent, diagnostic property. The mathematical form of an interaction's governing principle reveals its intent—cooperative or parasitic—making morality a measurable feature of the system's physics.
pirouette_definition: |
  The Lagrangian of Intent is the core mathematical principle that diagnoses the ethical and dynamic nature of influence. It models the interaction's objective function by combining the Pirouette Lagrangians (𝓛_p) of the participants. A cooperative, positive-sum form (𝓛_A + 𝓛_B) defines persuasion, while a parasitic, zero-sum form (𝓛_A - 𝓛_B) defines manipulation.
operational_definition:
  units: Coherence-seconds (Kτ·s) or dimensionless action.
  symbol_table:
    - name: 𝓛_I
      meaning: Lagrangian of Intent; the objective function of the interaction.
      dimensions: Coherence (Kτ)
      default_range: contextual
    - name: 𝓛_p
      meaning: Pirouette Lagrangian; a measure of a system's instantaneous coherence.
      dimensions: Coherence (Kτ)
      default_range: contextual
    - name: Kτ
      meaning: Coherence; a dimensionless measure of a system's internal stability and efficiency.
      dimensions: dimensionless
      default_range: [0, 1]
  measurement:
    procedures:
      - name: Influence Vector Analysis
        outline: |
          1. Over the course of an interaction, measure the change in coherence (ΔKτ), flow state (laminar, turbulent, stagnant), and autonomy for each participant.
          2. Construct a vector of these changes in the joint state space of the participants.
          3. Determine the gradient the system is following. A vector pointing toward mutual increase in Kτ and autonomy indicates a cooperative Lagrangian. A vector pointing toward an increase for one participant and a decrease for the other indicates a parasitic Lagrangian.
        expected_signals: [ΔKτ_target > 0 (persuasion), ΔKτ_target < 0 (manipulation), shift in flow state, change in size of choice-space]
        pitfalls: [Hidden variables, delayed consequences, observer effect on the interaction, sophisticated mimicry of cooperative signals.]
context_windows:
  - module: DOMA-064
    excerpt: |
      The ethical and physical distinction between these two modes is not a matter of opinion; it is a mathematical certainty, governed by the system's objective function as described by the Pirouette Lagrangian (CORE-006). The "intent" of the interaction is encoded in the Lagrangian the system seeks to optimize.
  - module: DOMA-064
    excerpt: |
      This is the core diagnostic. One need only ask: which equation is the interaction trying to solve? Is it building a greater whole, or is one part feeding on the other?
poetic_connections:
  motifs: [weaving vs unraveling, building vs draining, synthesis vs parasitism, harmony vs dissonance]
  evocative_lines:
    - "One need only ask: which equation is the interaction trying to solve?"
    - "The shadow we cast upon others is, in the end, the truest measure of our own light."
  association_matrix:
    - [ "PERSUASION_AS_SYNTHESIS", 0.95 ]
    - [ "MANIPULATION_AS_PARASITISM", 0.95 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "COHERENCE", 0.7 ]
formal_mappings:
  candidates:
    - target: Game Theory Payoff Function (U)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        Maximize U_total(A, B)
      justification: |
        The Lagrangian of Intent defines the objective function for a multi-agent interaction, analogous to a payoff function in game theory. The persuasion form (maximize U_A + U_B) corresponds to a cooperative (positive-sum) game, while the manipulation form (maximize U_A - U_B) corresponds to a competitive (zero-sum) game.
      references:
        - title: Theory of Games and Economic Behavior
          where: Von Neumann, J., & Morgenstern, O.
          date: 1944
      confidence: 0.9
    - target: Interaction Lagrangian (L_int)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        L_total = L_A + L_B + L_int
      justification: |
        In physics, the interaction term in a Lagrangian dictates the nature of the force between particles. The Lagrangian of Intent can be seen as a model where the 'intent' sets the form of L_int, determining whether the interaction is binding/attractive (cooperative) or repulsive/destructive (parasitic).
      references:
        - title: Classical Mechanics
          where: Goldstein, H.
          date: 1950
      confidence: 0.7
  adopted:
    - target: Game Theory Payoff Function
      rationale: The mapping is more direct. The Lagrangian of Intent is explicitly an objective function for agents making choices, which is the core subject of game theory, rather than a description of fundamental particle forces.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Any multi-agent influence dynamic can be modeled as an optimization problem where the objective function is either the sum (cooperation) or the difference (parasitism) of the agents' individual Pirouette Lagrangians."
      domain: phenomenology
      falsifier: "The discovery of a stable, widespread class of influence that robustly maximizes a different function, such as the product (𝓛_A * 𝓛_B) or a more complex, non-separable function, which cannot be reduced to the two primary forms."
      status: proposed
      links: [DOMA-064]
naming_notes:
  collisions: [Lagrangian (Classical Mechanics)]
  disambiguation: |
    This is not the standard physical Lagrangian (`L = T - V`). It is an objective function constructed from the Pirouette Lagrangian (𝓛_p), a measure of system coherence. The "Intent" qualifier specifies its application to diagnosing the governing objective of a goal-oriented interaction.
crosslinks:
  near_synonyms: [OBJECTIVE_FUNCTION_OF_INFLUENCE]
  antonyms: []
  prerequisites: [PIROUETTE_LAGRANGIAN, COHERENCE]
  downstream_effects: [PERSUASION_AS_SYNTHESIS, MANIPULATION_AS_PARASITISM]
license: CC-BY-SA-4.0
---

# Lagrangian of Intent

## Canonical (Pirouette)
The Lagrangian of Intent is the core mathematical principle that diagnoses the ethical and dynamic nature of influence. It models the interaction's objective function by combining the Pirouette Lagrangians (𝓛_p) of the participants. A cooperative, positive-sum form (𝓛_A + 𝓛_B) defines persuasion, while a parasitic, zero-sum form (𝓛_A - 𝓛_B) defines manipulation.

## EFT-First Summary
The Lagrangian of Intent is conceptually mapped to a **Game Theory Payoff Function**. It defines the "rules of the game" for an influence interaction. Persuasion is a cooperative game aiming to maximize the joint payoff (`U_A + U_B`), leading to a Pareto improvement. Manipulation is a zero-sum game where one player's gain is axiomatically linked to the other's loss, maximizing a competitive payoff (`U_A - U_B`). The framework posits that all influence dynamics can be reduced to one of these two games. (Ref: Von Neumann & Morgenstern, 1944).

## Glossary Links
- See also: [Pirouette Lagrangian](PIROUETTE_LAGRANGIAN), [Persuasion as Synthesis](PERSUASION_AS_SYNTHESIS), [Manipulation as Parasitism](MANIPULATION_AS_PARASITISM)