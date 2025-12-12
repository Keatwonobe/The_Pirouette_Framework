---
term: "Overall Coherence"
canonical_id: "OVERALL_COHERENCE"
symbol: "Kτ_team"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-099"]
---

---
term: Overall Coherence
canonical_id: OVERALL_COHERENCE
symbol: Kτ_team
aliases: []
parents: [DOMA-099]
children: [VICTOR_TILT, SPREAD_DELTA]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-099
      lines: "L102-L106"
      snippet: |
        A. Calculate Overall Coherence (`Kτ_team`):
        This produces a single "health score" for each team, representing its overall adherence to its path of maximal coherence. It ranges from 3 (total collapse) to 30 (peak performance).
        `Kτ_team` = (Cohesion Score) + (Resilience Score) + (Morphogenesis Score)
  editors: [autogen_dict_compiler]
  review_log: []
triad:
  art: |
    The single number that sings the team's song. It is the chord struck by adding the notes of unity, toughness, and intelligence into a single, resonant measure of potential.
  law: |
    Overall Coherence is the arithmetic sum of a team's Rhythmic Cohesion, Composure Under Pressure, and Strategic Adaptability scores. Each component is measured on a 1-10 integer scale, yielding a final value between 3 and 30.
  philosophy: |
    To predict the outcome of a contest between two complex systems, one must first quantify their respective states. Overall Coherence provides this essential, scalar measure of system health, enabling direct comparison and calculation of relative potential.
pirouette_definition: |
  A scalar metric representing the total measured coherence of a team-scale system. It is calculated as the sum of its three primary coherence signatures: Rhythmic Cohesion, Composure Under Pressure, and Strategic Adaptability. This value serves as the primary input for calculating relative system health and predictive outputs like Victor Tilt.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Kτ_team
      meaning: Overall Coherence for a specific team.
      dimensions: dimensionless
      default_range: "[3, 30]"
    - name: Cohesion Score
      meaning: Measured score for Rhythmic Cohesion via the Cohesion Gauge.
      dimensions: dimensionless
      default_range: "[1, 10]"
    - name: Resilience Score
      meaning: Measured score for Composure Under Pressure via the Resilience Meter.
      dimensions: dimensionless
      default_range: "[1, 10]"
    - name: Morphogenesis Score
      meaning: Measured score for Strategic Adaptability via the Morphogenesis Index.
      dimensions: dimensionless
      default_range: "[1, 10]"
  measurement:
    procedures:
      - name: Summative Coherence Assessment
        outline: |
          1. For a given team, conduct a qualitative observation of its performance over a defined time window (e.g., 5-10 minutes of game time).
          2. Using the Cohesion Gauge, Resilience Meter, and Morphogenesis Index rubrics, assign an integer score from 1-10 for each of the three coherence signatures.
          3. Sum the three scores to calculate Kτ_team for that time window.
        expected_signals: [An integer value between 3 and 30.]
        pitfalls: [Observer bias in scoring, Inconsistent application of rubrics across different analysts, Failure to define a clear time window for assessment.]
context_windows:
  - module: DOMA-099
    excerpt: |
      A. Calculate Overall Coherence (`Kτ_team`):
      This produces a single "health score" for each team, representing its overall adherence to its path of maximal coherence. It ranges from 3 (total collapse) to 30 (peak performance).
      `Kτ_team` = (Cohesion Score) + (Resilience Score) + (Morphogenesis Score)
  - module: DOMA-099
    excerpt: |
      The Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`) mathematically describes a system's drive to find the path of highest internal coherence (`K_τ`) for the lowest environmental cost (`V_Γ`). A team in Laminar Flow is one that is successfully navigating its geodesic. Its actions are efficient, its internal rhythm is strong, and it is effectively managing the temporal pressure (`Γ`) applied by the opponent.
poetic_connections:
  motifs: [system health, vital signs, resonance, harmony, aggregate potential]
  evocative_lines:
    - "The scoreboard is an autopsy of the past. The flow of the game is a prophecy of the future."
    - "By seeing the coherence, we predict the collapse."
  association_matrix:
    - [ "RHYTHMIC_COHESION", 0.9 ]
    - [ "COMPOSURE_UNDER_PRESSURE", 0.9 ]
    - [ "STRATEGIC_ADAPTABILITY", 0.9 ]
    - [ "VICTOR_TILT", 0.8 ]
    - [ "LAMINAR_FLOW", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Kinetic Energy (T)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        𝓛_p = K_τ - V_Γ  ↔  𝓛 = T - V
      justification: |
        The source module (DOMA-099) explicitly structures its core equation, the Pirouette Lagrangian (𝓛_p), as a direct analog to the classical Lagrangian (𝓛). In this mapping, Kτ represents the system's internal, organized capacity for coherent action, analogous to how kinetic energy represents organized motion.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A team's calculated Kτ_team score, averaged over a game, correlates positively with its final point differential."
      domain: phenomenology
      falsifier: "A large-scale study of games across a sport shows no statistically significant correlation between the Kτ_team calculated by trained analysts and the final score margin."
      status: proposed
      links: [DOMA-099]
naming_notes:
  collisions: [The symbol K is often used for kinetic energy in physics, a connection which is intentional in this framework.]
  disambiguation: |
    "Kτ_team" specifically refers to the calculated, team-scale metric from DOMA-099. It should be distinguished from the more abstract concept of internal coherence, "Kτ", as it appears in the foundational Pirouette Lagrangian (CORE-006), of which Kτ_team is a specific operationalization.
crosslinks:
  near_synonyms: []
  antonyms: [SYSTEM_DISSONANCE]
  prerequisites: [RHYTHMIC_COHESION, COMPOSURE_UNDER_PRESSURE, STRATEGIC_ADAPTABILITY]
  downstream_effects: [VICTOR_TILT, SPREAD_DELTA]
license: CC-BY-SA-4.0
---

# Overall Coherence

## Canonical (Pirouette)
A scalar metric representing the total measured coherence of a team-scale system. It is calculated as the sum of its three primary coherence signatures: Rhythmic Cohesion, Composure Under Pressure, and Strategic Adaptability. This value serves as the primary input for calculating relative system health and predictive outputs like Victor Tilt.

## EFT-First Summary
In the language of classical mechanics, Overall Coherence (Kτ_team) is the operational measure of a system's "kinetic term" in the Pirouette Lagrangian. It quantifies the system's capacity for organized, internal action, representing its effective "energy" available to pursue its goals, as opposed to the "potential cost" imposed by environmental pressures (V_Γ).

## Glossary Links
- See also: [[Rhythmic Cohesion]], [[Composure Under Pressure]], [[Strategic Adaptability]], [[Victor Tilt]]