---
term: "Lag"
canonical_id: "LAG"
symbol: "Δτ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-066"]
---

---
term: Lag
canonical_id: LAG
symbol: Δτ
aliases: [Transmission Delay, Propagation Time]
parents: [DOMA-066]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-066
      lines: "L60-L61"
      snippet: |
        - **Lag (Δτ):** The temporal delay of transmission across the edge. High lag can create destabilizing feedback loops and systemic dissonance.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The echo that returns too late, turning a dialogue into an argument. It is the gap between a cause and its effect, a space where understanding can curdle into noise.
  law: |
    The potential for a feedback loop to generate dissonance increases with the product of its total lag (ΣΔτ) and its effective conductivity (ΠΦ_C). When this product exceeds a system-specific threshold, spontaneous turbulent flow is expected.
  philosophy: |
    Lag reveals that connection is not enough; timing is paramount. It forces a shift from a static, structural view of a network to a dynamic, physiological one, where the rhythm of interaction determines health or pathology. Without accounting for lag, a map of a network is a lie.
pirouette_definition: |
  Lag (Δτ) is the finite time required for a signal, resource, or influence to traverse an edge from a source node to a target node. It is a fundamental parameter of a network's dynamic topology, co-equal with Conductivity (Φ_C) in determining the character of flow. While low lag is a feature of healthy, efficient flow channels (geodesics), high lag is a primary driver of systemic pathology, particularly when present in high-conductivity feedback loops, where it generates dissonant, self-amplifying turbulence (Coherence Fever).
operational_definition:
  units: seconds (s)
  symbol_table:
    - name: Δτ
      meaning: Temporal delay of transmission across a single edge.
      dimensions: T
      default_range: '> 0; contextual (e.g., ns for VLSI, days for supply chains)'
  measurement:
    procedures:
      - name: Ping-Echo Test
        outline: |
          1. Inject a tracer signal ('ping') at the source node of an edge at time t_ping.
          2. Detect the signal's arrival at the target node at time t_echo.
          3. Calculate Δτ = t_echo - t_ping.
          4. Average over multiple trials to mitigate jitter and measure a stable mean.
        expected_signals: [Tracer signal time-series at source and target nodes]
        pitfalls: [Signal jitter, signal degradation over the channel, ambiguity in defining the moment of 'arrival' for complex signals.]
context_windows:
  - module: DOMA-066
    excerpt: |
      Each edge represents a potential channel for the flow of coherence. It is not a static line but a dynamic vessel, characterized by: **Conductivity (Φ_C)**: The efficiency with which coherence can flow between two nodes... and **Lag (Δτ):** The temporal delay of transmission across the edge. High lag can create destabilizing feedback loops and systemic dissonance.
  - module: DOMA-066
    excerpt: |
      **Coherence Fever (The Dissonant Loop):** The primary pathology of *dynamics*, representing Turbulent Flow. A feedback loop with high conductivity (Φ_C) but also high lag (Δτ) creates a runaway cascade of dissonant information. The network expends immense energy in chaotic, self-amplifying noise.
  - module: DOMA-066
    excerpt: |
      The first step is to identify the primary paths of Laminar Flow—the network's healthy arteries. Algorithmically, this means finding the paths of maximal coherence (high `Φ_C`, low `Δτ`), where influence, resources, and information travel with the least resistance and highest fidelity.
poetic_connections:
  motifs: [echo, delay, dissonance, feedback, latency, rhythm, out-of-sync]
  evocative_lines:
    - "The fever of a runaway algorithm."
    - "The echo that returns too late."
  association_matrix:
    - [ "COHERENCE_FEVER", 0.9 ]
    - [ "CONDUCTIVITY", 0.7 ]
    - [ "LAMINAR_FLOW", -0.8 ]
formal_mappings:
  candidates:
    - target: Time delay (τ) in control systems
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        dx(t)/dt = f(x(t), x(t-τ))
      justification: |
        In control theory, time delays in feedback loops are a well-known source of instability and oscillation. High Pirouette Lag (Δτ) in a high-conductivity loop is mathematically analogous to a large delay term (τ) in a control system's feedback path, both leading to runaway oscillations (Dissonance).
      references:
        - title: Modern Control Engineering
          where: K. Ogata, Ch. 10
          date: 2010-01-01
      confidence: 0.9
  adopted:
    - target: Time Delay (τ) in Delay Differential Equations (Control Theory)
      rationale: |
        The mapping is direct and operational. The destabilizing effect of lag in high-gain feedback loops is a foundational concept in control theory, providing a rigorous mathematical basis for the Pirouette pathology of Coherence Fever.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A feedback loop's contribution to the system's Dissonance Index is a monotonically increasing function of the product of its total loop lag (ΣΔτ) and its effective loop conductivity (ΠΦ_C)."
      domain: phenomenology
      falsifier: "Demonstrating a system where increasing the lag in a high-conductivity feedback loop consistently stabilizes the system or reduces turbulent flow, without altering other parameters."
      status: proposed
      links: [DOMA-066]
naming_notes:
  collisions: [Δτ is sometimes used for proper time intervals in Special Relativity, but context (network edges vs. spacetime worldlines) prevents confusion.]
  disambiguation: |
    Distinguish from 'latency,' which often includes node processing time in its measurement. Lag (Δτ) in Pirouette strictly refers to the transit time *across an edge*.
crosslinks:
  near_synonyms: [LATENCY]
  antonyms: [LAMINAR_FLOW]
  prerequisites: [EDGE, NODE]
  downstream_effects: [COHERENCE_FEVER, DISSONANCE_INDEX]
license: CC-BY-SA-4.0
---

# Lag

## Canonical (Pirouette)
Lag (Δτ) is the finite time required for a signal, resource, or influence to traverse an edge from a source node to a target node. It is a fundamental parameter of a network's dynamic topology, co-equal with Conductivity (Φ_C) in determining the character of flow. While low lag is a feature of healthy, efficient flow channels (geodesics), high lag is a primary driver of systemic pathology, particularly when present in high-conductivity feedback loops, where it generates dissonant, self-amplifying turbulence (Coherence Fever).

## EFT-First Summary
In the language of control theory, Pirouette Lag (Δτ) is directly analogous to the time delay (τ) in a feedback system, a parameter known to introduce instability and oscillation. A network edge with high lag functions as a delay element in a control loop. When this loop also has high gain (analogous to high Conductivity, Φ_C), the system is prone to the runaway oscillations described by delay differential equations, which Pirouette identifies as the pathology of Coherence Fever. This provides a direct, mathematically rigorous bridge between network health and classical stability analysis.