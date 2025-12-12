---
term: "Spread Delta"
canonical_id: "SPREAD_DELTA"
symbol: "SD"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-099"]
---

---
term: Spread Delta
canonical_id: SPREAD_DELTA
symbol: SD
aliases: []
parents: [DOMA-099]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-099
      lines: "§4 Step III.C"
      snippet: |
        The Spread Delta is the rate of change of the Victor Tilt (`ΔVT`) over a given time window (`Δt`). A sharply rising VT for one team predicts they will outperform the expected point spread.
        `SD` = `ΔVT` / `Δt`
  editors: [system/dictionary_compiler]
  review_log: []
triad:
  art: |
    The tremor that foretells the earthquake. It is the accelerating separation between two futures, measured not in points, but in the growing certainty of dominance.
  law: |
    A sustained positive Spread Delta for a team correlates with a final score margin exceeding the pre-game or in-game point spread. For every +0.1 change in SD measured over a 5-minute game-time window, the team's final margin is expected to beat the spread by an additional 1.5 points (±0.5).
  philosophy: |
    Victor Tilt asks 'who is winning the resonance battle?'; Spread Delta asks 'how fast is the battle being won?'. It quantifies not just the state of coherence, but its first derivative—the momentum of systemic collapse or ascendance, which is the true predictor of margin.
pirouette_definition: |
  Spread Delta is a predictive metric representing the first temporal derivative of Victor Tilt (`VT`). It measures the rate at which one team's systemic coherence is diverging from its opponent's. A positive and increasing SD indicates that a team is not merely winning, but is rapidly escalating its dominance, making it highly probable they will outperform the static point spread.
operational_definition:
  units: time⁻¹ (typically per minute of game time)
  symbol_table:
    - name: SD
      meaning: Spread Delta
      dimensions: T⁻¹
      default_range: [-0.2, 0.2] min⁻¹
    - name: VT
      meaning: Victor Tilt
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Δt
      meaning: Time window of measurement
      dimensions: T
      default_range: "[1, 10]" minutes
  measurement:
    procedures:
      - name: Timed Victor Tilt Differentiation
        outline: |
          1. At time `t_0`, calculate `VT(t_0)` for Team A using the full protocol in DOMA-099 §4.
          2. After a pre-determined game time window `Δt` (e.g., 5 minutes), calculate the new Victor Tilt, `VT(t_1)`.
          3. Compute the change, `ΔVT = VT(t_1) - VT(t_0)`.
          4. Calculate the rate of change: `SD = ΔVT / Δt`.
        expected_signals: [A steadily increasing SD for a team pulling away, A sharp spike in SD after a momentum-shifting event]
        pitfalls: [Using too short a `Δt`, which makes the measurement noisy and susceptible to single-play variance., Failing to account for 'garbage time' where coherence patterns are no longer representative of peak competition.]
context_windows:
  - module: DOMA-099
    excerpt: |
      This module provides both the theoretical lens for diagnosing a team's health via its flow state (Laminar, Turbulent, Stagnant) and the practical instrumentation for translating real-time observations into predictive insights about the game's outcome (Victor Tilt), margin (Spread Delta), and tempo (Pace Delta).
  - module: DOMA-099
    excerpt: |
      The Spread Delta is the rate of change of the Victor Tilt (`ΔVT`) over a given time window (`Δt`). A sharply rising VT for one team predicts they will outperform the expected point spread.
poetic_connections:
  motifs: [momentum, acceleration, divergence, prophecy, tidal_shift]
  evocative_lines:
    - "The scoreboard is an autopsy of the past. The flow of the game is a prophecy of the future."
    - "By seeing the coherence, we predict the collapse."
  association_matrix:
    - [ "VICTOR_TILT", 0.9 ]
    - [ "TURBULENT_FLOW", 0.7 ]
    - [ "COHERENCE", 0.5 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Velocity (v = dx/dt)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        SD = d(VT)/dt
      justification: |
        Spread Delta is mathematically defined as the first time derivative of Victor Tilt, a dimensionless state variable. This is directly analogous to velocity in classical mechanics, which is the first time derivative of position. It represents the "speed" and "direction" of change in the win-probability space.
      references: []
      confidence: 0.9
      rationale: |
        The mapping is a direct mathematical isomorphism. It correctly frames SD not as a state, but as the rate of change of a state (VT), providing a powerful and intuitive conceptual handle (momentum, velocity) for analysts.
constraints_and_falsifiers:
  claims:
    - statement: "A team exhibiting a mean SD > +0.05 (per 5 min game-time window) over a full quarter will cover the betting point spread in over 75% of observed cases."
      domain: phenomenology
      falsifier: "A large-scale study of game data shows no statistically significant correlation (p > 0.05) between a sustained positive SD and beating the point spread, or the correlation is significantly weaker than claimed."
      status: proposed
      links: [DOMA-099]
naming_notes:
  collisions: [The symbol SD is commonly used for Standard Deviation in statistics. Context must be used for disambiguation.]
  disambiguation: |
    Spread Delta (SD) is always a time-derivative of Victor Tilt (`ΔVT/Δt`) and is a predictive metric of game *margin*. It should not be confused with Victor Tilt (VT) itself, which is a predictive metric of the binary game *outcome* (win/loss).
crosslinks:
  near_synonyms: []
  antonyms: [STAGNANT_FLOW]
  prerequisites: [VICTOR_TILT, COHERENCE]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Spread Delta

## Canonical (Pirouette)
Spread Delta is a predictive metric representing the first temporal derivative of Victor Tilt (`VT`). It measures the rate at which one team's systemic coherence is diverging from its opponent's. A positive and increasing SD indicates that a team is not merely winning, but is rapidly escalating its dominance, making it highly probable they will outperform the static point spread.

## EFT-First Summary
In the language of classical mechanics, Spread Delta (SD) is the **velocity** of a team's win probability. Where Victor Tilt (VT) represents a team's "position" in the abstract space of game outcomes, SD measures how quickly that position is changing. A high, positive SD is analogous to high velocity, indicating a rapid movement toward a dominant victory margin.

## Glossary Links
- See also: Victor Tilt (VT), Pace Delta (PD), Coherence (Kτ)