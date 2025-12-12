---
term: "Composure Under Pressure"
canonical_id: "COMPOSURE_UNDER_PRESSURE"
symbol: ""
aliases: [Resilience]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-099"]
---

---
term: Composure Under Pressure
canonical_id: COMPOSURE_UNDER_PRESSURE
symbol: 
aliases: [Resilience]
parents: [DOMA-099]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-099
      snippet: |
        **2. Composure Under Pressure (The Signature of Resilience):**
        This measures how a team’s coherence holds up against dissonant injections of adversity—a bad call, a turnover, a sudden deficit. It is a direct measure of stability in a high-Γ environment.
        *   **Observables:** Maintaining strategic discipline after a mistake; preventing one bad play from cascading into another; consistent fundamentals and communication during high-stakes moments.
        *   **Diagnostic Insight:** High composure indicates a robust and stable system, capable of resisting a descent into chaotic, Turbulent Flow.
  editors: [system]
  review_log: []
triad:
  art: |
    A ship holding its course through a sudden squall, its rigging taut but unbroken. It is the quiet center of a storm, the system's refusal to shatter when struck. It is the difference between a bell that rings true and one that cracks.
  law: |
    A system's resistance to a state transition into Turbulence is directly proportional to its ability to dampen, rather than amplify, the effects of dissonant impulses. High composure minimizes the temporal and performance cost of error recovery.
  philosophy: |
    Composure measures a system's internal stability and the integrity of its feedback loops. It reveals whether a system is merely functional under ideal conditions or genuinely robust. This quality is paramount, as it is the guarantor of coherence when facing the inevitable friction and adversity (Γ) of a competitive environment.
pirouette_definition: |
  A core signature of coherence that quantifies a system's ability to maintain its structural and strategic integrity when subjected to dissonant events or high temporal pressure (Γ). It is a measure of dynamic stability, specifically the capacity to absorb shocks, prevent cascading failures, and avoid lapsing from Laminar into Turbulent Flow.
operational_definition:
  units: Dimensionless ordinal score (1-10)
  symbol_table:
    - name: Resilience Score
      meaning: A quantified value of a team's Composure Under Pressure, derived from the Resilience Meter rubric.
      dimensions: dimensionless
      default_range: 1-10
  measurement:
    procedures:
      - name: Resilience Meter Assessment
        outline: |
          1.  Identify a discrete dissonant event (e.g., turnover, crucial referee error, opponent's momentum-shifting play).
          2.  Observe the team's immediate response over the next several plays or minutes.
          3.  Assess observables like body language, strategic discipline, communication, and error propagation.
          4.  Assign a score from 1 (Brittle) to 10 (Antifragile) using the rubric defined in DOMA-099, where 5 is an average or expected level of resilience.
        expected_signals: [Error cascade (low score), emotional reset (high score), maintained strategic discipline (high score), visible frustration/blame (low score)]
        pitfalls: [Analyst subjectivity, conflating a lucky outcome with a composed process, difficulty isolating the impact of a single event in a complex game.]
context_windows:
  - module: DOMA-099
    excerpt: |
      **2. Composure Under Pressure (The Signature of Resilience):**
      This measures how a team’s coherence holds up against dissonant injections of adversity—a bad call, a turnover, a sudden deficit. It is a direct measure of stability in a high-Γ environment. High composure indicates a robust and stable system, capable of resisting a descent into chaotic, Turbulent Flow.
  - module: DOMA-099
    excerpt: |
      **The Resilience Meter (Measures Composure Under Pressure)**
      *   **1-3 (Brittle):** A single mistake consistently cascades into more errors; body language is defeated; the team appears rattled and descends into Turbulence.
      *   **4-6 (Standard):** Recovers from errors at an average pace; may show frustration but resets for the next play.
      *   **7-8 (Tough):** Actively "stops the bleeding" after a bad sequence; demonstrates short memory for mistakes.
      *   **9-10 (Antifragile):** Seems to use adversity as fuel; responds to an opponent's big play with an even better one.
poetic_connections:
  motifs: [stability, equilibrium, dampening, antifragility, grace_under_fire, shock_absorption]
  evocative_lines:
    - "prevents one bad play from cascading into another"
    - "actively 'stops the bleeding' after a bad sequence"
    - "seems to use adversity as fuel"
  association_matrix:
    - [ "TURBULENCE", -0.9 ]
    - [ "COHERENCE", 0.7 ]
    - [ "TEMPORAL_PRESSURE", 0.6 ]
    - [ "STABILITY", 0.9 ]
formal_mappings:
  candidates:
    - target: Damping Ratio (ζ)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        mẍ + cẋ + kx = F(t)
        Resilience Score ~ c (damping coefficient)
      justification: |
        In a damped harmonic oscillator, the damping coefficient `c` or ratio `ζ` determines how quickly the system returns to equilibrium after being perturbed. A team with high composure (high `c`) quickly dampens the "oscillation" caused by an error, preventing a cascade (overdamped/critically damped). A brittle team (low `c`) oscillates wildly or has its errors amplified (underdamped).
      references:
        - title: Classical Mechanics
          where: Chapter on Oscillations
          date: 
      confidence: 0.8
    - target: System Stability (in Control Theory)
      domain: Engineering
      mapping_kind: conceptual
      justification: |
        Composure maps to the stability of a feedback control system. A resilient team utilizes strong negative feedback loops to correct deviations from its intended state (game plan). A brittle team is dominated by positive feedback, where initial errors are amplified, leading to systemic collapse (Turbulence).
      references:
        - title: Feedback Control of Dynamic Systems
          where: Chapter 2, "Modeling and Block Diagrams"
          date: 
      confidence: 0.9
  adopted:
    - target: System Stability (in Control Theory)
      rationale: This mapping best captures the dynamic, process-oriented nature of preventing cascading failures through internal corrective actions, which is central to the Pirouette definition. It emphasizes feedback loops, which are conceptually aligned with team communication and strategic discipline.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "In a controlled study of teams, a higher mean Resilience Score over a season will correlate with lower in-game performance variance, especially in high-stakes situations."
      domain: phenomenology
      falsifier: "No correlation is found, or an inverse correlation is found, between the measured Resilience Score and performance stability. This would indicate the metric fails to capture a real, predictive quality of the system."
      status: proposed
      links: [DOMA-099]
naming_notes:
  collisions: [Resilience is a widely used term in psychology and engineering. In Pirouette, it is not a general trait but specifically measures the stability of a system's *coherence* against disruption.]
  disambiguation: |
    Must be distinguished from **Rhythmic Cohesion**, which is about the efficiency of action in an undisturbed state, and **Strategic Adaptability**, which is about changing the system's overall strategy. Composure is about executing the *current* strategy robustly despite interference.
crosslinks:
  near_synonyms: [STABILITY]
  antonyms: [BRITTLENESS, TURBULENCE]
  prerequisites: [COHERENCE, TEMPORAL_PRESSURE]
  downstream_effects: [VICTOR_TILT, SPREAD_DELTA]
license: CC-BY-SA-4.0
---

# Composure Under Pressure

## Canonical (Pirouette)
A core signature of coherence that quantifies a system's ability to maintain its structural and strategic integrity when subjected to dissonant events or high temporal pressure (Γ). It is a measure of dynamic stability, specifically the capacity to absorb shocks, prevent cascading failures, and avoid lapsing from Laminar into Turbulent Flow.

## EFT-First Summary
Composure Under Pressure is conceptually mapped to the stability of a dynamic system in control theory. A system with high composure employs effective negative feedback loops to dampen perturbations (errors, adversity) and rapidly return to its desired operational state (its coherent game plan). A brittle system, by contrast, suffers from positive feedback where small errors are amplified, leading to a cascading, chaotic failure mode analogous to Turbulent Flow. This stability is a key component of a system's overall health and predictability.

## Glossary Links
- See also: Rhythmic Cohesion, Strategic Adaptability, Coherence, Turbulence