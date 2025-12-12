---
term: "Cohesion Gauge"
canonical_id: "COHESION_GAUGE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-099"]
---

---
term: Cohesion Gauge
canonical_id: COHESION_GAUGE
symbol: 
aliases: []
parents: [DOMA-099]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-099
      snippet: |
        1. The Cohesion Gauge (Measures Rhythmic Cohesion)
        *   1-3 (Dissonant): Frequent unforced errors, broken plays, visible frustration between players. Actions are chaotic and self-defeating.
        *   4-6 (Functional): Standard execution, plays run as designed but without exceptional flow, some hesitation or inefficiency is present.
        *   7-8 (Harmonious): Crisp, efficient execution; players are "in sync," anticipating each other's moves; complex plays look easy.
        *   9-10 (Telepathic): A state of peak flow; improvisational, creative, and perfectly timed plays unfold, seemingly without effort.
  editors: [AI Agent]
  review_log: []
triad:
  art: |
    The conductor's baton for a team's symphony, making audible the silent music of shared intention. It measures not individual skill, but the resonance between players.
  law: |
    The Cohesion Gauge assigns a quantitative score (1-10) to a team's Rhythmic Cohesion by classifying observable on-field actions into four distinct qualitative bands: Dissonant (1-3), Functional (4-6), Harmonious (7-8), and Telepathic (9-10).
  philosophy: |
    To quantify the health of a system, one must first measure its internal harmony. The Cohesion Gauge provides the fundamental measurement of a team's ability to act as a singular, coherent entity, grounding the abstract concept of 'team flow' in observable, scorable phenomena.
pirouette_definition: |
  A conceptual instrument and structured scoring rubric used by an analyst to quantify a team's Rhythmic Cohesion. The gauge translates qualitative observations of synchronized, efficient, and anticipatory actions into a single score on a 1-10 scale. This score serves as a primary input for calculating a team's Overall Coherence (`Kτ`), providing a real-time measure of its expression of Laminar Flow.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: C_S
      meaning: Cohesion Score; the quantitative output of the Cohesion Gauge.
      dimensions: dimensionless
      default_range: 1-10 (integer)
  measurement:
    procedures:
      - name: Observational Scoring
        outline: |
          1. Define an observation window (e.g., 5-10 minutes of game time).
          2. Observe the team's collective actions, focusing on the observables of Rhythmic Cohesion (e.g., timing, anticipation, efficiency of movement).
          3. Compare the holistic character of the team's actions against the four rubric bands (Dissonant, Functional, Harmonious, Telepathic).
          4. Assign a single integer score `C_S` from 1 to 10 that best represents the performance within the window.
        expected_signals: [Crisp, efficient player/ball movement, plays unfolding with effortless timing, players anticipating each other's actions, palpable shared momentum.]
        pitfalls: [Analyst subjectivity, confirmation bias from the scoreboard, confusing a series of successful individual plays with genuine team cohesion.]
context_windows:
  - module: DOMA-099
    excerpt: |
      **1. Rhythmic Cohesion (The Signature of Laminar Flow):**
      This measures the team's ability to act as a single, unified entity. It is the visible evidence of a shared, high-fidelity Ki pattern.
      *   **Observables:** Crisp, efficient ball or player movement; plays that unfold with effortless timing; players anticipating each other's actions; a palpable sense of shared purpose and momentum.
      *   **Diagnostic Insight:** High Rhythmic Cohesion is the primary indicator of a healthy, laminar system that is efficiently converting intention into action.
  - module: DOMA-099
    excerpt: |
      To move from qualitative observation to quantitative prediction, the analyst employs three conceptual instruments. Each instrument is a structured rubric for scoring one of the three signatures of coherence on a 1-10 scale, where 5 represents an average or expected level of performance.
poetic_connections:
  motifs: [rhythm, harmony, resonance, telepathy, synchronicity]
  evocative_lines:
    - "The scoreboard is an autopsy of the past. The flow of the game is a prophecy of the future."
    - "complex plays look easy."
  association_matrix:
    - [ "RHYTHMIC_COHESION", 0.9 ]
    - [ "LAMINAR_FLOW", 0.7 ]
    - [ "KI_PATTERN", 0.6 ]
formal_mappings:
  candidates:
    - target: Order parameter
      domain: Statistical Mechanics|Complex Systems
      mapping_kind: conceptual
      equation_hint:
      justification: |
        The Cohesion Score acts as a proxy for an order parameter in a many-body system. A low score (Dissonant) corresponds to a disordered, high-entropy state where agents act randomly. A high score (Telepathic) corresponds to a highly ordered, phase-locked state where agents act as a single coherent entity, minimizing internal friction and maximizing collective output.
      references: []
      confidence: 0.3
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A team's average Cohesion Gauge score over a match is a stronger predictor of victory than its individual player statistics."
      domain: phenomenology
      falsifier: "A large-scale study across multiple sports shows that models based on aggregated individual player stats consistently outperform models using analyst-assigned Cohesion Scores in predicting game outcomes."
      status: proposed
      links: [DOMA-099]
naming_notes:
  collisions: ["Cohesion" is a common term in sociology (social bonds) and software engineering (code modularity).]
  disambiguation: |
    In Pirouette, the Cohesion Gauge does not measure social bonds or system architecture. It strictly refers to the observable, real-time synchronization of actions (`Rhythmic Cohesion`) within a competitive performance context.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [RHYTHMIC_COHESION, LAMINAR_FLOW]
  downstream_effects: [OVERALL_COHERENCE, VICTOR_TILT]
license: CC-BY-SA-4.0
---

# Cohesion Gauge

## Canonical (Pirouette)
A conceptual instrument and structured scoring rubric used by an analyst to quantify a team's Rhythmic Cohesion. The gauge translates qualitative observations of synchronized, efficient, and anticipatory actions into a single score on a 1-10 scale. This score serves as a primary input for calculating a team's Overall Coherence (`Kτ`), providing a real-time measure of its expression of Laminar Flow.

## EFT-First Summary
Conceptually, the Cohesion Gauge provides an operational measure analogous to an order parameter in a complex system. It quantifies the degree of phase-locking among individual agents (players), where a high score indicates a globally coherent, low-entropy state, and a low score indicates a disordered, high-entropy state.

## Glossary Links
- See also: Rhythmic Cohesion, Overall Coherence (Kτ), Laminar Flow