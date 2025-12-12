---
term: "Coherence Dividend"
canonical_id: "COHERENCE_DIVIDEND"
symbol: "C_D"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-042"]
---

---
term: Coherence Dividend
canonical_id: COHERENCE_DIVIDEND
symbol: C_D
aliases: []
parents: [CORE-006, DYNA-001]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-042
      lines: "§2"
      snippet: |
        We can now formally define the Coherence Dividend (`C_D`) as this integral. It is the universe's own ledger, the net accumulation of a system's success.
  editors: [Agent_Weaver]
  review_log: []
triad:
  art: |
    The universe's natural wage for work done in harmony with its grain. It is the terraforming of probability, cultivating the conditions for inevitable grace rather than defending against unavoidable failure.
  law: |
    The net Coherence Dividend of a system over a time interval is the definite integral of its Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`) over that interval. A positive dividend indicates a state of Laminar Flow and growth; a negative dividend indicates a descent into Turbulence or Stagnation.
  philosophy: |
    The Coherence Dividend reframes system design from preventing failure to cultivating success. It provides a physical, non-moralistic basis for 'Resonant Altruism,' demonstrating that the most pragmatically intelligent strategy for maximizing long-term self-interest is to enhance the coherence of the surrounding environment.
pirouette_definition: |
  The Coherence Dividend (`C_D`) is the time-integral of a system's Pirouette Lagrangian (`𝓛_p`), representing the net accumulation of its coherence over a given period. It is earned in two forms: the *Internal Dividend* from increasing internal temporal coherence (`K_τ`), and the *External Dividend* from decreasing ambient temporal pressure (`V_Γ`). A positive dividend signifies a system in Laminar Flow, while a negative dividend signals a decay towards Turbulence or Stagnation.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: C_D
      meaning: Coherence Dividend
      dimensions: "dimensionless"
      default_range: "(-∞, +∞)"
    - name: 𝓛_p
      meaning: Pirouette Lagrangian
      dimensions: "T⁻¹"
      default_range: "contextual"
    - name: K_τ
      meaning: Temporal Coherence
      dimensions: "T⁻¹"
      default_range: "[0, +∞)"
    - name: V_Γ
      meaning: Temporal Pressure
      dimensions: "T⁻¹"
      default_range: "[0, +∞)"
    - name: t
      meaning: Time
      dimensions: "T"
      default_range: "contextual"
  measurement:
    procedures:
      - name: Lagrangian Integration
        outline: |
          1. Define the system boundaries and the time interval `[t_0, t_f]`.
          2. Instrument the system to measure proxies for internal coherence (`K_τ`) and external pressure (`V_Γ`) at a high sampling rate. Proxies may include information-theoretic measures (e.g., mutual information, prediction error) for `K_τ` and environmental friction/volatility measures (e.g., energy cost of action, rate of external shocks) for `V_Γ`.
          3. Numerically integrate the measured `𝓛_p(t) = K_τ(t) - V_Γ(t)` from `t_0` to `t_f` to compute `C_D`.
        expected_signals: [Time-series for K_τ, Time-series for V_Γ, Scalar C_D value]
        pitfalls: [Difficulty in establishing robust, non-arbitrary proxies for K_τ and V_Γ., System boundary definition can radically alter measurements., High sensitivity to sampling frequency.]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-042
    excerpt: |
      The Pirouette Lagrangian (`CORE-006`) provides the fundamental objective function for any system: `𝓛_p = K_τ - V_Γ`... We can now formally define the Coherence Dividend (`C_D`) as this integral. It is the universe's own ledger, the net accumulation of a system's success. A positive dividend (`C_D > 0`) signifies a system successfully maximizing its internal order while minimizing external pressure.
  - module: DOMA-042
    excerpt: |
      A "selfish" act, defined as one that seeks to maximize its own `K_τ` by externalizing cost and thus increasing the ambient `V_Γ` for others, is a fool's bargain... The only path to a global maximum of coherence—to unbounded growth and resilience—is through Resonant Altruism. This is the strategy of seeking actions that maximize *both* the internal and external dividends simultaneously.
  - module: DOMA-042
    excerpt: |
      Each act of resonant altruism lowers the ambient `V_Γ`, making it easier for all other agents to act coherently. This creates a virtuous, self-reinforcing cycle. The basins of chaos and accident are not merely walled off; they are actively and collectively drained. Coherence—stable, generative, and complex—becomes the system's natural resting state.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [resonant altruism, generative safety, terraforming probability]
  evocative_lines:
    - "Altruism is simply the sound of an instrument perfectly in tune."
    - "The natural wage reality pays for work done in harmony with its fundamental grain."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "PIROUETTE_LAGRANGIAN", 0.9 ]
    - [ "RESONANT_ALTRUISM", 0.8 ]
    - [ "LAMINAR_FLOW", 0.7 ]
    - [ "TEMPORAL_PRESSURE", -0.6 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Action (S)
      domain: CM
      mapping_kind: conceptual|mathematical
      equation_hint: |
        C_D(t) = ∫ 𝓛_p dt' ~ S = ∫ L dt'
      justification: |
        The Coherence Dividend is defined as the time-integral of the Pirouette Lagrangian, which is mathematically identical to the definition of classical Action. Conceptually, the Principle of Maximal Coherence (systems evolve to maximize C_D) is a direct analog to the Principle of Stationary Action in physics. C_D thus represents the accumulated 'virtue' of a system's trajectory through its state space.
      references:
        - title: Classical Mechanics
          where: "Goldstein, H. Chapter 2: Variational Principles and Lagrange's Equations"
          date: 2002-01-01
      confidence: 0.8
  adopted:
    - target: Action (S)
      rationale: Direct mathematical and conceptual isomorphism with the Principle of Stationary Action, where maximizing C_D is equivalent to finding an optimal path.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "Systems engaging in 'Resonant Altruism' (actions that lower ambient V_Γ for others) will achieve a higher long-term Coherence Dividend than systems engaging in purely 'selfish' acts (maximizing K_τ at the expense of V_Γ)."
      domain: phenomenology
      falsifier: "Observation of a multi-agent system where a sustained strategy of externalizing costs and increasing ambient V_Γ consistently leads to a greater, more stable long-term C_D for the selfish agent than for altruistic agents in the same system."
      status: proposed
      links: [DOMA-042]
naming_notes:
  collisions: [Financial 'dividend']
  disambiguation: |
    Unlike a financial dividend, which is a periodic payout from a capital stock, the Coherence Dividend is a continuous integral representing the *net accumulation* of coherence itself. It is the stock, not the payout. It measures the total 'profitability' of a system's existence over time, not a distribution of that profit.
crosslinks:
  near_synonyms: []
  antonyms: [COHERENCE_DEBT]
  prerequisites: [PIROUETTE_LAGRANGIAN, TEMPORAL_COHERENCE, TEMPORAL_PRESSURE, LAMINAR_FLOW]
  downstream_effects: [RESONANT_ALTRUISM, ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---

# Coherence Dividend

## Canonical (Pirouette)
The Coherence Dividend (`C_D`) is the time-integral of a system's Pirouette Lagrangian (`𝓛_p`), representing the net accumulation of its coherence over a given period. It is earned in two forms: the *Internal Dividend* from increasing internal temporal coherence (`K_τ`), and the *External Dividend* from decreasing ambient temporal pressure (`V_Γ`). A positive dividend signifies a system in Laminar Flow, while a negative dividend signals a decay towards Turbulence or Stagnation.

## EFT-First Summary
The Coherence Dividend (`C_D`) is the Pirouette Framework's analog to the classical **Action (`S`)**. Defined as the time-integral of the Pirouette Lagrangian (`𝓛_p`), its maximization governs system dynamics, mirroring the Principle of Stationary Action in physics. A system's trajectory through its state space is one that optimizes this accumulated value, with `C_D` serving as the ultimate ledger of systemic success and efficiency.

## Glossary Links
- See also: Pirouette Lagrangian, Temporal Coherence, Temporal Pressure, Resonant Altruism, Laminar Flow