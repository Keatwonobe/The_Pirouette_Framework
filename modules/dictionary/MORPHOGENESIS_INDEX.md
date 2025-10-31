---
term: "Morphogenesis Index"
canonical_id: "MORPHOGENESIS_INDEX"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-099"]
---

---
term: Morphogenesis Index
canonical_id: MORPHOGENESIS_INDEX
symbol: I_M
aliases: ['Ki Morphogenesis Score', 'Strategic Adaptability Score']
parents: ['DOMA-099']
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-099
      lines: "L65-L71"
      snippet: |
        3. The Morphogenesis Index (Measures Strategic Adaptability)
        *   1-3 (Rigid): Sticks to a single game plan even when it is failing...
        *   4-6 (Reactive): Makes adjustments, but often a step behind the opponent...
        *   7-8 (Proactive): Successfully imposes its will and tempo on the game...
        *   9-10 (Visionary): Appears to be "playing chess" while the opponent plays checkers...
  editors: [Cognitive Weaver Agent]
  review_log: []
triad:
  art: |
    The measure of a system's mind; not how well it follows the map, but how skillfully it redraws it mid-journey to discover a better destination.
  law: |
    The Morphogenesis Index is the 1-10 scalar value assigned to a team's observed capacity to alter its strategic pattern (`Ki`) to maintain or increase its coherence relative to an opponent. A higher index correlates directly with a greater ability to control game tempo, as measured by Pace Delta (`PD`).
  philosophy: |
    Beyond mere execution or resilience, the Morphogenesis Index quantifies the *intelligence* of a system. It asserts that victory in a complex environment belongs not to the most stable system, but to the most adaptable one—the one capable of generative, creative responses to pressure.
pirouette_definition: |
  The Morphogenesis Index (`I_M`) is a conceptual instrument that quantifies a system's Strategic Adaptability on a 1-10 scale. It measures the ability to impose a preferred resonant pattern (`Ki`) onto a competitive environment and to adapt or generate new patterns (`Ki` Morphogenesis) in response to opponent pressure or changing conditions. It is a direct input for calculating a system's Overall Coherence (`Kτ_team`) and the Pace Delta (`PD`) between two competing systems.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: I_M
      meaning: Morphogenesis Index score
      dimensions: dimensionless
      default_range: '[1, 10]'
  measurement:
    procedures:
      - name: Analyst Rubric Scoring
        outline: |
          An analyst observes a team's performance over a set time window (e.g., 5-10 minutes of game time) and scores their Strategic Adaptability using a 4-tier rubric (Rigid, Reactive, Proactive, Visionary) based on observables like in-game adjustments, tempo control, and strategic novelty.
        expected_signals: ['successful counter-strategies', 'tempo control', 'neutralization of opponent strengths']
        pitfalls: ['confusing tactical execution with strategic adaptation', 'analyst bias toward a favored team or strategy', 'insufficient observation window to judge adaptability']
context_windows:
  - module: DOMA-099
    excerpt: |
      **Strategic Adaptability (The Signature of Ki Morphogenesis):**
      This measures a team's ability to impose its preferred resonant pattern (`Ki`) on the game and to adapt that pattern when necessary. Observables include successfully dictating the tempo and making effective in-game adjustments. High adaptability shows a system that is not just stable, but intelligent—capable of finding new paths to coherence in a complex, changing landscape.
  - module: DOMA-099
    excerpt: |
      **D. Calculate Pace Delta (PD):**
      The Pace Delta is the difference in the Morphogenesis Index scores. A significant positive value for Team A suggests they will control the game's tempo.
      `PD` = (Morphogenesis_A) - (Morphogenesis_B)
poetic_connections:
  motifs: ['intelligence', 'adaptation', 'creativity', 'chess-master', 'evolution', 'fluidity']
  evocative_lines:
    - "Appears to be 'playing chess' while the opponent plays checkers."
    - "A system that is not just stable, but intelligent."
    - "Unable to escape a Stagnant Flow."
  association_matrix:
    - [ "Ki", 0.9 ]
    - [ "PACE_DELTA", 0.8 ]
    - [ "STAGNANT_FLOW", 0.7 ]
    - [ "OVERALL_COHERENCE", 0.6 ]
formal_mappings:
  candidates:
    - target: Optimal Control Policy (π*)
      domain: Control Theory|Reinforcement Learning
      mapping_kind: conceptual
      equation_hint: |
        π_new ← update(π_old, environment_feedback)
      justification: |
        The Morphogenesis Index is analogous to the quality and adaptability of a system's control policy (π). A 'Rigid' system (low `I_M`) uses a fixed policy, while a 'Visionary' system (high `I_M`) dynamically updates its policy toward a new optimum in response to feedback, akin to online policy optimization.
      references:
        - title: Reinforcement Learning: An Introduction
          where: Sutton and Barto, Chapter 13
          date: 2018-11-13
      confidence: 0.7
  adopted:
    - target: null
      rationale: null
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A team's Morphogenesis Index score, as measured by a trained analyst, is a positive and statistically significant predictor of its ability to control game tempo (e.g., time of possession, pace of play statistics)."
      domain: phenomenology
      falsifier: "A large-scale study of games scored using the Sports Flow Resonance protocol shows no correlation, or a negative correlation, between a team's assigned `I_M` score and its objective tempo-control metrics."
      status: proposed
      links: ['DOMA-099']
naming_notes:
  collisions: ["The term 'morphogenesis' is used in developmental biology for the process by which an organism develops its shape. The Pirouette usage is a direct analogy, referring to the development of a system's strategic 'shape' or form (`Ki`) during a contest."]
  disambiguation: |
    Distinguish from the Resilience Meter, which measures a system's ability to *withstand* pressure and maintain its current form. The Morphogenesis Index measures the ability to *change* form productively in response to pressure. A system can be resilient but not adaptive (tough but rigid).
crosslinks:
  near_synonyms: ['STRATEGIC_ADAPTABILITY']
  antonyms: ['STRATEGIC_RIGIDITY']
  prerequisites: ['Ki', 'COHERENCE']
  downstream_effects: ['PACE_DELTA', 'OVERALL_COHERENCE']
license: CC-BY-SA-4.0
---