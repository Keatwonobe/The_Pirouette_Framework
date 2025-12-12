---
term: "Conductivity"
canonical_id: "CONDUCTIVITY"
symbol: "Φ_C"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-066"]
---

---
term: Conductivity
canonical_id: CONDUCTIVITY
symbol: Φ_C
aliases: []
parents: [DOMA-066]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-066
      lines: "§2"
      snippet: |
        **Conductivity (Φ_C):** The efficiency with which coherence (information, resources, trust) can flow between two nodes. High conductivity implies a healthy, laminar channel.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The measure of a channel's generosity. It is the width of the river that allows life to flow, rather than the sturdiness of the bridge that merely connects two shores. A connection without conductivity is just a line on a dead map.
  law: |
    The rate of coherence transfer between two nodes is proportional to the edge's conductivity and the coherence gradient between them. All systemic pathologies—stagnation, turbulence, and decay—manifest as a local or global degradation of conductivity.
  philosophy: |
    Conductivity reveals that a connection's existence is less important than its vitality. A network is defined not by its static lines but by its living currents; Φ_C quantifies the health of those currents, distinguishing a functioning system from a mere schematic.
pirouette_definition: |
  Conductivity (Φ_C) is a scalar property of a network edge that quantifies the efficiency of coherence transfer between its two connected nodes. It represents the channel's capacity to transmit information, resources, or other forms of coherence with high fidelity and minimal loss. High conductivity is a hallmark of a healthy, laminar flow channel, while low or degrading conductivity is a primary indicator of systemic pathologies such as bottlenecks (Coherence Atrophy) and structural decay (Coherence Erosion).
operational_definition:
  units: Dimensionless ratio [0, 1]
  symbol_table:
    - name: Φ_C
      meaning: Edge Conductivity
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Ping-Echo Coherence Test
        outline: |
          1. Induce a standardized coherence packet (a known signal or resource bundle) at the source node (N_a).
          2. Measure the received coherence packet at the target node (N_b) after a single characteristic cycle.
          3. Calculate Φ_C as the ratio of received coherence to sent coherence: Φ_C = Coherence_received / Coherence_sent.
        expected_signals: [A clear signal at N_b correlated with the signal from N_a, high signal-to-noise ratio.]
        pitfalls: [Confounding effects from network noise, high Lag (Δτ) delaying the measurement, difficulty defining a "standardized packet" in non-informational networks (e.g., social trust).]
context_windows:
  - module: DOMA-066
    excerpt: |
      Each edge represents a potential channel for the flow of coherence. It is not a static line but a dynamic vessel, characterized by: **Conductivity (Φ_C):** The efficiency with which coherence (information, resources, trust) can flow between two nodes. High conductivity implies a healthy, laminar channel.
  - module: DOMA-066
    excerpt: |
      **Coherence Atrophy (The Bottleneck):** The primary pathology of *structure*, representing Stagnant Flow. **Symptoms:** A node or edge with critically low conductivity (`Φ_C`) acts as a "coherence dam." Nodes "downstream" become starved and atrophied, while nodes "upstream" experience a dangerous build-up of Temporal Pressure (`Γ`).
poetic_connections:
  motifs: [flow, artery, channel, vitality, friction, bandwidth]
  evocative_lines:
    - "High conductivity implies a healthy, laminar channel."
    - "...to clear the blockages, to soothe the fevers, and to mend the connections that allow life to flow."
  association_matrix:
    - [ "Coherence", 0.9 ]
    - [ "Lag (Δτ)", 0.7 ]
    - [ "Bottleneck", 0.8 ]
    - [ "Temporal Pressure (Γ)", 0.5 ]
formal_mappings:
  candidates:
    - target: Electrical Conductance (G)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        I = G * V  <=>  Coherence Flow = Φ_C * Δ(Coherence)
      justification: |
        Electrical conductance measures the ease with which current flows through a material for a given voltage difference. Similarly, Φ_C measures the ease with which "coherence current" flows across an edge for a given "coherence potential" gradient between nodes. The analogy supports importing circuit theory concepts.
      references:
        - title: Physics for Scientists and Engineers
          where: Chapter on DC Circuits
          date: 2008-01-01
      confidence: 0.8
    - target: Diffusion Coefficient (D)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        J = -D * ∇φ
      justification: |
        In diffusion, the coefficient D relates the flux of a substance to the concentration gradient. Φ_C plays an identical role, relating the flux of coherence to its gradient across an edge, framing coherence flow as a diffusion process across a discrete boundary.
      references:
        - title: Fick's laws of diffusion
          where: Wikipedia
          date: 2024-01-01
      confidence: 0.7
  adopted:
    - target: Electrical Conductance (G)
      rationale: "The analogy is direct, intuitive, and operationally useful. It allows the import of circuit theory concepts (e.g., resistance as 1/Φ_C, Kirchhoff's laws for coherence flow at nodes) to analyze network dynamics, aligning with the 'Weaver's Multimeter' instrumentation metaphor from DOMA-066."
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A sustained decrease in the average edge conductivity (Φ_C) of a network reliably predicts an impending fragmentation event or systemic failure."
      domain: phenomenology
      falsifier: "Observing a system that maintains long-term stability and function despite a continuous, significant decline in its average Φ_C, or a system that undergoes sudden fragmentation without a preceding decline in Φ_C."
      status: proposed
      links: [DOMA-066]
naming_notes:
  collisions: [Electrical Conductance, Thermal Conductivity]
  disambiguation: |
    Distinguish from Lag (Δτ). Conductivity (Φ_C) measures the *quantity* or *efficiency* of flow per cycle (a measure of bandwidth). Lag (Δτ) measures the *speed* or *delay* of that flow (a measure of latency). An edge can have high conductivity but also high lag (a 'wide but long pipe'), a combination indicative of a Dissonant Loop pathology.
crosslinks:
  near_synonyms: [BANDWIDTH, CHANNEL_CAPACITY]
  antonyms: [RESISTANCE, FRICTION, IMPEDANCE]
  prerequisites: [COHERENCE, NODE, EDGE]
  downstream_effects: [BOTTLENECK, COHERENCE_EROSION, FLOW_EFFICIENCY]
license: CC-BY-SA-4.0
---