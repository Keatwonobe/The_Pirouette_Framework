---
term: "Coherence Gain"
canonical_id: "COHERENCE_GAIN"
symbol: "`S_p`"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-085"]
---

---
term: Coherence Gain
canonical_id: COHERENCE_GAIN
symbol: `S_p`
aliases: []
parents: [DOMA-085]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-085
      lines: "L104-L105"
      snippet: |
        The integral of this Lagrangian over a characteristic cycle determines the **Coherence Gain (`S_p`)**. This single, predictive metric dictates the verdict.
  editors: [synthesizer-alpha]
  review_log: []
triad:
  art: |
    The single note that resolves a complex chord, revealing whether the song is one of growth or decay. It is the calculated intuition that reads the future's welcome in the present's echo.
  law: |
    The time-integrated value of the system-environment Lagrangian (`𝓛_seed`) over one characteristic cycle; a positive value (`S_p > S_threshold`) mandates engagement (`PLANT`), a negative value (`S_p < 0`) mandates retreat (`ABORT`), and a near-zero value mandates observation (`HOLD`).
  philosophy: |
    Coherence Gain reframes strategic action from an expression of will into a response to environmental potential. It replaces the drive to colonize with a search for resonance, ensuring that acts of creation are sustainable, symbiotic, and ethically grounded in a forecast of mutual flourishing.
pirouette_definition: |
  The Coherence Gain (`S_p`) is a dimensionless scalar quantity representing the net change in a system's coherence over a characteristic cycle when introduced to a new environment. It is calculated as the action integral of the specialized Pirouette Lagrangian (`𝓛_seed`) for that interaction. `S_p` serves as the primary predictive metric in the Sower's Gambit protocol, determining the strategic verdict of whether to engage, wait, or retreat.
operational_definition:
  units: Dimensionless (normalized action)
  symbol_table:
    - name: `S_p`
      meaning: Coherence Gain
      dimensions: Dimensionless
      default_range: "[-1, 1]"
    - name: `𝓛_seed`
      meaning: The Viability Lagrangian specific to a Seed in an environment
      dimensions: Energy (M L^2 T^-2)
      default_range: contextual
    - name: `τ`
      meaning: Characteristic cycle time for the integration
      dimensions: Time (T)
      default_range: contextual
  measurement:
    procedures:
      - name: Sower's Gambit Forecast
        outline: |
          1. Deploy a Scout Probe to measure Harmonic Compatibility, Geodesic Availability, and local Temporal Pressure (`Γ`).
          2. Construct the Viability Lagrangian `𝓛_seed = K_τ(potential) - V_Γ(cost)` using these parameters and the Seed's intrinsic coherence.
          3. Numerically integrate `𝓛_seed` over one characteristic temporal cycle (`τ`) of the Seed-environment system to yield `S_p`.
          4. Compare `S_p` to the decision thresholds.
        expected_signals: [Scalar value `S_p`]
        pitfalls: [Mischaracterizing the 'characteristic cycle' can lead to integration errors. Probe-induced turbulence (Observer's Shadow) can contaminate the measurement of `V_Γ`, artificially lowering the calculated `S_p`.]
context_windows:
  - module: DOMA-085
    excerpt: |
      The integral of this Lagrangian over a characteristic cycle determines the **Coherence Gain (`S_p`)**. This single, predictive metric dictates the verdict.
  - module: DOMA-085
    excerpt: |
      The Coherence Gain (`S_p`) translates directly into a strategic choice, moving the Seed from diagnosis to action... PLANT (`S_p` > `S_threshold`)... HOLD (`S_p` ≈ 0 OR High Turbulence)... ABORT (`S_p` < 0).
poetic_connections:
  motifs: [Verdict, Forecast, Harvest, Resonance, Go/No-Go]
  evocative_lines:
    - "The Sower's Gambit is the art of asking for permission from the future."
    - "This single, predictive metric dictates the verdict."
  association_matrix:
    - [ "Pirouette Lagrangian", 0.9 ]
    - [ "Alchemical Union", 0.7 ]
    - [ "Scout Probe", 0.6 ]
    - [ "Temporal Pressure", 0.5 ]
formal_mappings:
  candidates:
    - target: `S` (The Action)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        S = ∫ L(q, q̇, t) dt
      justification: |
        Coherence Gain is explicitly defined as the integral of a Lagrangian (`𝓛_seed`) over time, directly mirroring the definition of Action in classical mechanics. Where classical systems follow paths that extremize the action, a Pirouette 'Seed' uses the calculated action value itself as a predictive metric for viability and strategic choice.
      references:
        - title: Classical Mechanics
          where: Chapter 2, "Variational Principles and Lagrange's Equations"
          date: 1980-01-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system's long-term viability in a new environment is positively correlated with its calculated Coherence Gain (`S_p`) prior to engagement."
      domain: phenomenology
      falsifier: "Observing a statistically significant number of systems with `S_p < 0` achieving stable, long-term Alchemical Union, or systems with `S_p > S_threshold` consistently failing."
      status: proposed
      links: [DOMA-085]
naming_notes:
  collisions: [`S` is the standard symbol for Action in physics and Entropy in thermodynamics. Subscript `p` (for Pirouette or predictive) is crucial for disambiguation.]
  disambiguation: |
    Distinguish from raw energy gain or resource capture efficiency. Coherence Gain is a measure of *resonant potential* and pattern stability, not material accumulation. A system can have a high energy throughput but a negative `S_p` if the environment is decohering its structure.
crosslinks:
  near_synonyms: []
  antonyms: [DECOHERENCE_RATE]
  prerequisites: [PIROUETTE_LAGRANGIAN, SCOUT_PROBE, TEMPORAL_PRESSURE]
  downstream_effects: [ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---