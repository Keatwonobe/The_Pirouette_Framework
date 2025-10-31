---
term: "Discursive Flow"
canonical_id: "DISCURSIVE_FLOW"
symbol: ""
aliases: [Coherence Flow]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-127"]
---

---
term: Discursive Flow
canonical_id: DISCURSIVE_FLOW
symbol: 
aliases: [Coherence Flow]
parents: [DOMA-127, DYNA-001]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-127
      lines: "§2"
      snippet: |
        Before intervening, a Weaver must diagnose. The health of any discourse can be understood by observing the state of its coherence flow, as defined in Flow Dynamics (DYNA-001). This lens replaces the old, granular parameters with a single, holistic assessment.
  editors: [Weaver-Agent]
  review_log: []
triad:
  art: |
    The currents of discourse reveal its destination: a battlefield where truths drown, an impasse where they stagnate, or a crucible where they merge and flow toward a greater sea of understanding.
  law: |
    A discourse is in a state of Laminar Flow if and only if the rate of new, shared concept formation is positive and the rate of direct, negating refutations is less than 1% of total utterances.
  philosophy: |
    To reframe discourse from a zero-sum conflict to a positive-sum act of co-creation. Diagnosing the flow state is the first step in transforming an arena of combat into a crucible for synthesis.
pirouette_definition: |
  A holistic, qualitative diagnostic of a discourse's health, categorized into three states: Laminar (constructive, coherent), Turbulent (adversarial, dissonant), or Stagnant (paralyzed, repetitive). It serves as the primary indicator for applying the Crucible Protocol to facilitate a Resonant Synthesis.
operational_definition:
  units: Categorical (Laminar, Turbulent, Stagnant)
  symbol_table:
    - name: S_D
      meaning: The categorical state of the Discursive Flow.
      dimensions: dimensionless
      default_range: "{Laminar, Turbulent, Stagnant}"
  measurement:
    procedures:
      - name: Discourse State Classification
        outline: |
          Analyze a transcript or live recording of the discourse. Classify utterances into categories: clarifying questions, additive statements, direct refutations, ad hominem attacks, repeated points. The dominant category and interaction pattern determines the overall state.
        expected_signals:
          - Laminar: High ratio of clarifying questions to statements; novel concept linkages; use of collaborative language ("How does that connect...", "What if we combine...").
          - Turbulent: High frequency of interruptions; prevalence of logical fallacies and personal attacks; low turn-taking latency.
          - Stagnant: High repetition of core arguments; long pauses; circular dialogue patterns.
        pitfalls:
          - The Observer's Shadow (CORE-010) can bias the classification.
          - Mistaking passionate debate for Turbulence.
          - Misclassifying strategic silence as Stagnation.
context_windows:
  - module: DOMA-127
    excerpt: |
      This module replaces the calculation of argumentative "force" with the diagnosis of discursive "flow." The goal is no longer to achieve "vector alignment" through persuasion, but to facilitate a **Resonant Synthesis**—an **Alchemical Union** (CORE-012) of perspectives into a new, more coherent, shared understanding.
  - module: DOMA-127
    excerpt: |
      *   **Laminar Flow (The Weaving):** The ideal state of a healthy debate. Arguments build upon one another, questions seek to clarify, and participants act in good faith toward a shared goal.
      *   **Turbulent Flow (The Battlefield):** The state of combat. Characterized by logical fallacies, ad hominem attacks, and interruptions.
      *   **Stagnant Flow (The Impasse):** A "Coherence Dam" has formed. Participants are locked into rigid positions, repeating the same points.
poetic_connections:
  motifs: [river dynamics, crucible, weaving, resonance chamber]
  evocative_lines:
    - "A battlefield is where two truths go to die. A crucible is where they go to be reborn as one."
    - "The rules make it *easier* to build together than to fight apart."
  association_matrix:
    - [ "RESONANT_SYNTHESIS", 0.9 ]
    - [ "CRUCIBLE_PROTOCOL", 0.8 ]
    - [ "PIRQUETTE_LAGRANGIAN", 0.6 ]
    - [ "OBSERVERS_SHADOW", 0.5 ]
formal_mappings:
  candidates:
    - target: Reynolds number (Re)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        Re = ρuL/μ ; where ρ is idea density, u is interaction velocity, L is topic scale, and μ is participant 'viscosity' (good faith).
      justification: |
        Discursive Flow conceptually maps to fluid dynamics regimes. Laminar flow corresponds to low Reynolds number (smooth, orderly), while Turbulent flow corresponds to high Reynolds number (chaotic, eddy currents). Stagnant flow is analogous to a no-flow or dammed state.
      references: []
      confidence: 0.3
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Application of the Crucible Protocol (§3, DOMA-127) to a Turbulent or Stagnant discourse will measurably shift its state toward Laminar Flow within five conversational turns."
      domain: phenomenology
      falsifier: "Controlled studies of debates where the protocol is applied fail to show a statistically significant decrease in interruptions and fallacies, and/or fail to show an increase in collaborative utterances, compared to control groups."
      status: proposed
      links: [DOMA-127]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from the 'flow state' of an individual participant (psychological immersion). Discursive Flow is a collective, systemic property of the discourse itself, not the internal state of the actors.
crosslinks:
  near_synonyms: [COHERENCE_FLOW]
  antonyms: [DISSONANT_INJECTION, COHERENCE_DAM]
  prerequisites: [GEOMETRY_OF_DEBATE]
  downstream_effects: [RESONANT_SYNTHESIS, ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---

# Discursive Flow

## Canonical (Pirouette)
A holistic, qualitative diagnostic of a discourse's health, categorized into three states: Laminar (constructive, coherent), Turbulent (adversarial, dissonant), or Stagnant (paralyzed, repetitive). It serves as the primary indicator for applying the Crucible Protocol to facilitate a Resonant Synthesis.

## First-Principles Summary
Discursive Flow is a diagnostic for the collective state of a discourse, analogous to fluid dynamics regimes. A healthy, constructive discourse exhibits Laminar Flow (conceptually, low Reynolds number), while adversarial or chaotic discourse is Turbulent (high Reynolds number). The Crucible Protocol (DOMA-127) acts as a flow conditioner, altering the boundary conditions of the conversation to favor the Laminar state, thereby enabling Resonant Synthesis.

## Glossary Links
- See also: Resonant Synthesis, Crucible Protocol, Coherence Dam, Alchemical Union