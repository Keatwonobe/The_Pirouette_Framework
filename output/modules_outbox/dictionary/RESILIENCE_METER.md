---
term: "Resilience Meter"
canonical_id: "RESILIENCE_METER"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-099"]
---

---
term: Resilience Meter
canonical_id: RESILIENCE_METER
symbol: N/A
aliases: [Composure Under Pressure]
parents: [DOMA-099]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-099
      snippet: |
        ### 2. The Resilience Meter (Measures Composure Under Pressure)
        *   **1-3 (Brittle):** A single mistake consistently cascades into more errors; body language is defeated; the team appears rattled and descends into Turbulence.
        *   **4-6 (Standard):** Recovers from errors at an average pace; may show frustration but resets for the next play.
        *   **7-8 (Tough):** Actively "stops the bleeding" after a bad sequence; demonstrates short memory for mistakes; leadership is visible in calming the system.
        *   **9-10 (Antifragile):** Seems to use adversity as fuel; responds to an opponent's big play with an even better one; remains calm and focused in the most critical moments.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    The measure of a system's spine. It reveals whether a team shatters like glass, bends like a reed, or strengthens like tempered steel in the sudden fire of adversity.
  law: |
    A system's Resilience score is inversely correlated with the probability of an error cascade following a dissonant event. A high score (≥7) predicts rapid return to the prior state of coherence, while a low score (≤3) predicts a state transition into Turbulent Flow.
  philosophy: |
    Performance under ideal conditions is trivial; the true character of a coherent system is revealed by its stability when pressured. The Resilience Meter diagnoses this character, distinguishing robust systems that can absorb temporal shocks (high-Γ) from brittle ones that cannot. It quantifies a team's ability to remain itself when the game tries to force it to become something else.
pirouette_definition: |
  A conceptual instrument used within the Sports Flow Resonance framework to quantitatively score a team's Composure Under Pressure. It assesses, on a 1-10 scale, the stability of a system's collective coherence in response to dissonant events or high-Γ environments. The meter diagnoses a system's tendency to either absorb disruption and maintain Laminar Flow, or to fracture into error-cascading Turbulent Flow.
operational_definition:
  units: Dimensionless score [1-10]
  symbol_table:
    - name: S_R
      meaning: Resilience Score
      dimensions: dimensionless
      default_range: "[1, 10]"
  measurement:
    procedures:
      - name: Dissonant Event Response Analysis
        outline: |
          1. Identify a discrete, negative event (e.g., turnover, bad referee call, opponent scoring run). This is the impulse function.
          2. Observe the team's collective behavior over the next 1-3 plays or possessions.
          3. Score the response according to the 1-10 rubric, focusing on the prevention of error cascades, maintenance of strategic form, and collective body language.
        expected_signals: [Maintaining strategic discipline, preventing cascading errors, positive/neutral team communication, stable body language.]
        pitfalls: [Analyst subjectivity, confirmation bias, misattributing a subsequent independent error to a cascade.]
context_windows:
  - module: DOMA-099
    excerpt: |
      **Composure Under Pressure (The Signature of Resilience):**
      This measures how a team’s coherence holds up against dissonant injections of adversity—a bad call, a turnover, a sudden deficit. It is a direct measure of stability in a high-Γ environment. Observables include maintaining strategic discipline after a mistake and preventing one bad play from cascading into another. High composure indicates a robust and stable system, capable of resisting a descent into chaotic, Turbulent Flow.
  - module: DOMA-099
    excerpt: |
      The Resilience Meter (Measures Composure Under Pressure)
      *   **1-3 (Brittle):** A single mistake consistently cascades into more errors; body language is defeated; the team appears rattled and descends into Turbulence.
      *   **7-8 (Tough):** Actively "stops the bleeding" after a bad sequence; demonstrates short memory for mistakes; leadership is visible in calming the system.
      *   **9-10 (Antifragile):** Seems to use adversity as fuel; responds to an opponent's big play with an even better one.
poetic_connections:
  motifs: [brittleness, toughness, antifragility, stability, grace_under_fire]
  evocative_lines:
    - "Seems to use adversity as fuel."
    - "A single mistake consistently cascades into more errors."
    - "Actively 'stops the bleeding' after a bad sequence."
  association_matrix:
    - [ "TURBULENT_FLOW", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "STABILITY", 0.8 ]
formal_mappings:
  candidates:
    - target: Damping coefficient (ζ or γ)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        `m d²x/dt² + γ dx/dt + kx = F_ext(t)`
      justification: |
        The Resilience Meter is a heuristic measure of a system's response to an external shock (`F_ext`). A low score (Brittle) is analogous to an underdamped system (γ is small), where a shock leads to large, cascading oscillations (errors). A high score (Tough/Antifragile) is analogous to a critically damped or overdamped system (γ is large), where coherence is restored quickly and efficiently.
      references:
        - title: Classical Mechanics
          where: Chapter on Damped Oscillations
          date: 
      confidence: 0.7
  adopted:
    - target: Damping coefficient (ζ or γ)
      rationale: The damping analogy provides a clear, operational intuition for how the Resilience Meter quantifies a system's ability to absorb shocks and return to a stable state (Laminar Flow) without destructive oscillations (Turbulent Flow).
      confidence: 0.7
constraints_and_falsifiers:
  claims:
    - statement: "A team's Resilience Meter score, averaged over a game's first half, is a statistically significant predictor of their performance stability (e.g., lower variance in points-per-possession) during high-leverage situations in the second half."
      domain: phenomenology
      falsifier: "A longitudinal study of game data shows no significant correlation between a team's Resilience score and its late-game performance stability, or shows that the Cohesion Gauge is a far better predictor."
      status: proposed
      links: [DOMA-099]
naming_notes:
  collisions: ["Resilience" is a common term in psychology and engineering.]
  disambiguation: |
    Unlike individual psychological toughness, the Resilience Meter measures a *collective, systemic* property. It is not about an individual's grit, but about the whole team's ability to maintain its coherent structure (its Ki Pattern) against disruption. It is a measure of systemic stability, not personal fortitude.
crosslinks:
  near_synonyms: [COMPOSURE_UNDER_PRESSURE]
  antonyms: [BRITTLENESS]
  prerequisites: [LAMINAR_FLOW, TURBULENT_FLOW, TEMPORAL_PRESSURE]
  downstream_effects: [OVERALL_COHERENCE, VICTOR_TILT]
license: CC-BY-SA-4.0
---

# Resilience Meter

## Canonical (Pirouette)
A conceptual instrument used within the Sports Flow Resonance framework to quantitatively score a team's Composure Under Pressure. It assesses, on a 1-10 scale, the stability of a system's collective coherence in response to dissonant events or high-Γ environments. The meter diagnoses a system's tendency to either absorb disruption and maintain Laminar Flow, or to fracture into error-cascading Turbulent Flow.

## EFT-First Summary
The Resilience Meter provides a heuristic measure of a system's effective **damping coefficient (γ)**. A team is modeled as an oscillator in a state of coherent, Laminar Flow. An opponent's action or a mistake acts as an external driving force. A low Resilience score indicates low damping, where the shock induces large, destructive oscillations (cascading errors, a descent into Turbulence). A high score indicates high damping, where the system efficiently absorbs the energy and returns to its stable coherent state.

## Glossary Links
- See also: [Composure Under Pressure](./COMPOSURE_UNDER_PRESSURE.md), [Turbulent Flow](./TURBULENT_FLOW.md), [Laminar Flow](./LAMINAR_FLOW.md), [Temporal Pressure](./TEMPORAL_PRESSURE.md), [Overall Coherence](./OVERALL_COHERENCE.md)