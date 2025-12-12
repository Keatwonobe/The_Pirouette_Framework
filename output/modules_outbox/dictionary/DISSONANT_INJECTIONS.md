---
term: "Dissonant injections"
canonical_id: "DISSONANT_INJECTIONS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["INST-SPRT-001_sports_flow_gauge"]
---

---
term: Dissonant injections
canonical_id: DISSONANT_INJECTIONS
symbol: δ_d
aliases: [mistakes, bad calls, flow disruptions, negative events]
parents: [INST-SPRT-001_sports_flow_gauge]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: INST-SPRT-001_sports_flow_gauge
      lines: "L35"
      snippet: |
        Purpose: To quantify a team's ability to absorb and recover from "dissonant injections" (mistakes, bad calls, opponent's big plays).
  editors: [persona:dictionary_compiler]
  review_log: []
triad:
  art: |
    A sharp, wrong note in the symphony of play. It is the broken string, the missed cue that threatens the entire performance and reveals the ensemble's true character.
  law: |
    A discrete, observable event that causes a negative inflection in a team's Cohesion Gauge score, providing the primary input for measurement by the Resilience Meter.
  philosophy: |
    Dissonant injections are the crucibles of coherence. They are not merely errors but tests that reveal a system's true integrity, distinguishing brittle structures that shatter from antifragile ones that strengthen under stress.
pirouette_definition: |
  A discrete, negative event, originating either internally (e.g., an unforced error, a miscommunication) or externally (e.g., a superior play by an opponent, a controversial referee decision), that disrupts a team's rhythmic cohesion and tests its composure. The severity of an injection is defined by the system's response to it.
operational_definition:
  units: dimensionless event count
  symbol_table:
    - name: δ_d
      meaning: A single dissonant injection event.
      dimensions: dimensionless
      default_range: N/A (discrete events)
  measurement:
    procedures:
      - name: Event-Triggered Resilience Assessment
        outline: |
          1. Analyst observes a game, identifying a candidate event (e.g., turnover, major defensive breakdown, surprising opponent score).
          2. The event is logged as a potential δ_d.
          3. Analyst immediately assesses the team's `Resilience Meter` score (1-10) based on their tactical and emotional response in the subsequent 1-3 plays.
          4. A low Resilience score (1-3, Brittle) confirms the event had a significant dissonant impact.
        expected_signals: [Immediate drop in Cohesion Gauge score, negative body language, cascading minor errors, tactical disarray.]
        pitfalls: [Observer bias in judging event severity, mistaking a routine error for a coherence-breaking injection, misattributing a team's poor play to a single event when it is a systemic failure.]
context_windows:
  - module: INST-SPRT-001_sports_flow_gauge
    excerpt: |
      The Resilience Meter (Measures Composure Under Pressure): Purpose: To quantify a team's ability to absorb and recover from "dissonant injections" (mistakes, bad calls, opponent's big plays).
  - module: INST-SPRT-001_sports_flow_gauge
    excerpt: |
      Scoring Rubric (1-10): 1-3 (Brittle): A single mistake consistently cascades into more errors; body language is defeated; team appears rattled. ... 9-10 (Antifragile): Seems to use adversity as fuel; responds to an opponent's big play with an even better one.
poetic_connections:
  motifs: [disruption, error, shock, test, fracture, brittleness, cascade]
  evocative_lines:
    - "A single mistake consistently cascades into more errors..."
    - "Seems to use adversity as fuel."
    - "Actively 'stops the bleeding' after a bad sequence."
  association_matrix:
    - [ "RESILIENCE_METER", 0.9 ]
    - [ "COHESION_GAUGE", -0.7 ]
    - [ "ANTIFRAGILE", 0.6 ]
formal_mappings:
  candidates:
    - target: Disturbance (d(t))
      domain: Control Theory
      mapping_kind: conceptual
      equation_hint: |
        y(t) = G(s)u(t) + H(s)d(t)
      justification: |
        In control theory, a disturbance is an uncommanded signal that adversely affects a system's output. A dissonant injection acts as a discrete disturbance to the "team system," disrupting its "flow state" (the output) and requiring the system's control loops (resilience, coaching) to compensate.
      references:
        - title: Modern Control Engineering
          where: "Katsuhiko Ogata, Chapter 5: Basic Control Actions and Response of Control Systems"
          date: 2010-01-01
      confidence: 0.5
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The measured team response to dissonant injections (via the Resilience Meter) is a better predictor of game outcome than the raw count of the events themselves (e.g., turnover differential)."
      domain: phenomenology
      falsifier: "A statistical analysis of 100+ games shows that a simple turnover differential is a statistically stronger predictor of the final score than the aggregated Resilience Meter scores following those events."
      status: proposed
      links: [INST-SPRT-001_sports_flow_gauge]
naming_notes:
  collisions: [The symbol δ is common for 'change' or 'variation'. The subscript 'd' for 'dissonant' provides necessary disambiguation.]
  disambiguation: |
    A Dissonant Injection is defined by its *impact* on team coherence, not just its occurrence. It is an event-plus-response. A turnover that the team immediately shrugs off would be logged as having a minimal dissonant effect, whereas a seemingly minor error that causes players to argue and lose focus would be a significant one.
crosslinks:
  near_synonyms: []
  antonyms: [COHERENT_FLOW, HARMONIOUS_EXECUTION]
  prerequisites: [COHESION_GAUGE]
  downstream_effects: [RESILIENCE_METER, VICTOR_TILT, SPREAD_DELTA]
license: CC-BY-SA-4.0