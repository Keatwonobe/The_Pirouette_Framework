---
term: "Resonant Altruism"
canonical_id: "RESONANT_ALTRUISM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-042"]
---

---
term: Resonant Altruism
canonical_id: RESONANT_ALTRUISM
symbol: 
aliases: []
parents: [DOMA-042]
children: [CORE-012]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-042
      lines: "60-65"
      snippet: |
        The only path to a global maximum of coherence—to unbounded growth and resilience—is through **Resonant Altruism**. This is the strategy of seeking actions that maximize *both* the internal and external dividends simultaneously.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    An action that tunes not just one's own string, but brings the entire orchestra into resonant harmony. It is the sound an instrument makes when it realizes it is part of a song, strengthening itself by enriching the whole.
  law: |
    An agent maximizes its long-term Coherence Dividend (`C_D`) by selecting actions that simultaneously increase its internal Temporal Coherence (`ΔK_τ > 0`) and decrease the ambient Temporal Pressure of its environment (`ΔV_Γ < 0`).
  philosophy: |
    Resonant Altruism reconciles self-interest with collective well-being, framing compassion not as a moral imposition but as the most efficient strategy for navigating the universe's fundamental drive toward coherence. It replaces the zero-sum logic of myopic selfishness with the positive-sum calculus of systemic cultivation.
pirouette_definition: |
  The optimal strategic principle of selecting actions that simultaneously maximize an agent's internal Temporal Coherence (`K_τ`) and minimize the ambient Temporal Pressure (`V_Γ`) of its environment. By increasing its own integrity while reducing friction for the entire system, an agent engages in a positive feedback loop that maximizes the total, long-term Coherence Dividend (`C_D`) for both itself and its surroundings.
operational_definition:
  units: Dimensionless (strategy/principle)
  symbol_table: []
  measurement:
    procedures:
      - name: Coherence Dividend Attribution
        outline: |
          1. For a given agent action `a`, measure the change in the agent's internal coherence, `ΔK_τ(a)`.
          2. Simultaneously, measure the integrated change in the environmental temporal pressure, `ΔV_Γ(a)`, across all affected neighbor systems.
          3. Classify the action as Resonant Altruism if both `ΔK_τ(a) > 0` and `ΔV_Γ(a) < 0`. The magnitude is a function of both terms.
        expected_signals: [Positive correlation between an agent's `K_τ` and the `K_τ` of its neighbors over time, System-wide decrease in `V_Γ` following actions by the agent]
        pitfalls: [Difficulty in isolating the causal impact of a single action in a complex system, Defining the boundary of the 'environment' to measure `V_Γ`, Time-lag effects where `ΔV_Γ` is not immediate]
context_windows:
  - module: DOMA-042
    excerpt: |
      A "selfish" act, defined as one that seeks to maximize its own `K_τ` by externalizing cost and thus increasing the ambient `V_Γ` for others, is a fool's bargain. It is like shouting in a library to better hear the sound of one's own voice... The only path to a global maximum of coherence—to unbounded growth and resilience—is through Resonant Altruism. This is the strategy of seeking actions that maximize *both* the internal and external dividends simultaneously.
  - module: DOMA-042
    excerpt: |
      Each act of resonant altruism lowers the ambient `V_Γ`, making it easier for all other agents to act coherently. This creates a virtuous, self-reinforcing cycle. The basins of chaos and accident are not merely walled off; they are actively and collectively drained. Coherence—stable, generative, and complex—becomes the system's natural resting state, its gravitational center.
poetic_connections:
  motifs: [harmony, resonance, tuning, gardening, virtuous cycle, draining the swamp]
  evocative_lines:
    - "Altruism is simply the sound of an instrument perfectly in tune."
    - "To act with compassion is to act in perfect harmony with the fundamental forces of creation."
  association_matrix:
    - [ "COHERENCE_DIVIDEND", 0.9 ]
    - [ "ALCHEMICAL_UNION", 0.7 ]
    - [ "TEMPORAL_COHERENCE", 0.8 ]
    - [ "TEMPORAL_PRESSURE", -0.8 ]
formal_mappings:
  candidates:
    - target: Cooperative Equilibrium / Pareto Improvement
      domain: Game Theory
      mapping_kind: conceptual
      equation_hint:
      justification: |
        Resonant Altruism describes a strategy that moves a system towards a Pareto-optimal state, where one party's situation (`K_τ`) is improved while actively improving the situation for others (lowering `V_Γ`). It is a dynamic implementation of finding cooperative equilibria in an iterated, multi-agent game, rejecting zero-sum or 'selfish' local maxima for a global, positive-sum outcome.
      references:
        - title: The Evolution of Cooperation
          where: Robert Axelrod, Basic Books
          date: 1984-01-01
      confidence: 0.5
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "In any sufficiently complex, interconnected system, agents employing Resonant Altruism will, over a long enough time horizon, accumulate a greater Coherence Dividend than agents employing purely selfish (K_τ-maximizing, V_Γ-increasing) strategies."
      domain: phenomenology
      falsifier: "Observation of a long-term stable system where the dominant, most successful agents consistently employ strategies that increase environmental Temporal Pressure (`V_Γ`) as a means of maximizing their own `K_τ`."
      status: proposed
      links: [DOMA-042]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from 'pure altruism' (self-sacrifice), which may involve decreasing one's own `K_τ` to lower `V_Γ`. Resonant Altruism requires a positive `ΔK_τ`; it is not self-sacrifice but enlightened self-interest that aligns with the system's interest.
crosslinks:
  near_synonyms: []
  antonyms: [MYOPIC_SELFISHNESS]
  prerequisites: [COHERENCE_DIVIDEND, TEMPORAL_COHERENCE, TEMPORAL_PRESSURE]
  downstream_effects: [ALCHEMICAL_UNION, LAMINAR_FLOW]
license: CC-BY-SA-4.0
---

# Resonant Altruism

## Canonical (Pirouette)
The optimal strategic principle of selecting actions that simultaneously maximize an agent's internal Temporal Coherence (`K_τ`) and minimize the ambient Temporal Pressure (`V_Γ`) of its environment. By increasing its own integrity while reducing friction for the entire system, an agent engages in a positive feedback loop that maximizes the total, long-term Coherence Dividend (`C_D`) for both itself and its surroundings.

## Game Theory Summary
In the language of game theory, Resonant Altruism is the dynamic strategy for achieving and sustaining a cooperative, Pareto-optimal equilibrium. It reframes the agent's utility function to include the 'health' of the environment, recognizing that reducing systemic friction (cf. `V_Γ`) is a necessary precondition for maximizing one's own long-term success (cf. `K_τ`). It is the physical basis for the emergence of robust cooperation.

## Glossary Links
- See also: Coherence Dividend, Alchemical Union, Myopic Selfishness, Laminar Flow