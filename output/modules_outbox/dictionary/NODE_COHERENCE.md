---
term: "Node Coherence"
canonical_id: "NODE_COHERENCE"
symbol: "Kτ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-158"]
---

---
term: Node Coherence
canonical_id: NODE_COHERENCE
symbol: Kτ
aliases: [Rhythmic Purity, T_a_node (legacy)]
parents: [DOMA-158]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-158
      lines: "§2"
      snippet: |
        Node Coherence (Kτ): This replaces T_a_node. It measures the stability and integrity of an individual node's resonant pattern. It is the purity of its rhythm.
  editors: [Weaver-Agent-073]
  review_log: []
triad:
  art: |
    The unwavering hum of a single, well-tuned string. It is the steady heartbeat that gives the network its pulse, the pure tone from which all systemic harmony originates.
  law: |
    The total Coherence Flow `J` originating from a node cannot exceed its intrinsic Coherence `Kτ`. A node with `Kτ = 0` is a pure sink or passive conduit; it cannot generate productive, resonant flow.
  philosophy: |
    Systemic health begins with the integrity of the component parts. A network of incoherent nodes is merely a collection of noise generators; true resonance and collective action can only emerge from a foundation of stable, coherent individuals.
pirouette_definition: |
  Node Coherence (Kτ) is a dimensionless scalar quantity measuring the rhythmic purity and temporal stability of an individual node's activity pattern. It quantifies the degree to which a node's signal is a predictable, resonant pattern versus random noise, serving as the ultimate source of all Coherence Flow (`J`) that the node can emit into the network. It replaces the legacy `T_a_node` parameter.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: Kτ
      meaning: Node Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Spectral Purity Analysis
        outline: |
          1. Record the time-series data of the node's primary activity signal (e.g., neural firing rate, packet transmission).
          2. Perform a Fourier Transform on the signal to obtain its power spectrum.
          3. Calculate Kτ as the ratio of power concentrated in the dominant frequency peak to the total power integrated across the entire spectrum.
        expected_signals: [User activity logs, neural firing data, power grid phase measurements, economic cycle data]
        pitfalls: [Insufficient sampling rate leading to aliasing; non-stationary signals requiring windowed analysis.]
context_windows:
  - module: DOMA-158
    excerpt: |
      Node Coherence (Kτ): ... It measures the stability and integrity of an individual node's resonant pattern. It is the purity of its rhythm. Inference: Look for regularity and predictability. In a social network, this is the consistency of a user's activity and role. In a power grid, it is the phase stability of a generator. ... Scaling: `0` (pure noise) to `1` (a perfect, unwavering rhythm).
  - module: DOMA-158
    excerpt: |
      The flow from node `i` to node `j` is given by: `J_ij = Kτ_i * cos(φ_i - φ_j) * (1 - Γ_ij)`. This formula elegantly captures the core dynamics: Source Coherence (`Kτ_i`): Flow can only originate from a coherent source. A noisy node cannot create a strong, directed current.
  - module: DOMA-158
    excerpt: |
      This entire analysis is a practical application of the Principle of Maximal Coherence (CORE-006). A healthy network is one whose components are successfully navigating the geodesic on their shared coherence manifold, optimizing the Pirouette Lagrangian: `𝓛_p = Kτ - f(Γ)`. Coherence (`Kτ`): The "kinetic" term is the sum of the network's productive, laminar flows.
poetic_connections:
  motifs: [rhythm, purity, stability, heartbeat, signal, source, integrity]
  evocative_lines:
    - "It is the purity of its rhythm."
    - "Flow can only originate from a coherent source."
    - "A noisy node cannot create a strong, directed current."
  association_matrix:
    - [ "COHERENCE_FLOW", 0.9 ]
    - [ "TEMPORAL_PHASE", 0.7 ]
    - [ "TURBULENCE", -0.8 ]
    - [ "CHANNEL_PRESSURE", 0.3 ]
formal_mappings:
  candidates:
    - target: Quality Factor (Q)
      domain: Physics
      mapping_kind: operational
      equation_hint: |
        Kτ ∝ Q = ω₀ / Δω
      justification: |
        The Q factor of an oscillator measures its frequency selectivity and low rate of energy loss. A high-Q resonator has a very sharp power spectrum peak, analogous to a high-Kτ node whose activity is concentrated in a pure, stable rhythm. The operational measurement via spectral analysis is nearly identical for both.
      references:
        - title: The Feynman Lectures on Physics, Vol. I
          where: "Chapter 25: The Linear Systems"
          date: 1964-01-01
      confidence: 0.8
    - target: Order Parameter
      domain: SM
      mapping_kind: conceptual
      justification: |
        Kτ acts as a local order parameter. It measures the degree to which a node's internal state or activity aligns with a coherent, ordered pattern (Kτ=1) versus a disordered, high-entropy state (Kτ=0), much like magnetization measures spin alignment in an Ising model.
      references: []
      confidence: 0.6
  adopted:
    - target: Quality Factor (Q)
      rationale: The mapping is direct, operational, and shares the same measurement technique (spectral analysis of a resonator's output). It provides a concrete physical intuition for Kτ as a measure of resonance purity.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A network composed exclusively of nodes with an average Kτ < 0.1 cannot sustain large-scale, low-frequency resonant modes (i.e., global laminar flow)."
      domain: phenomenology
      falsifier: "Demonstration of a network where all individual nodes are demonstrably noisy and unstable (low Kτ), yet the network as a whole exhibits a strong, stable, and coherent global rhythm. This would imply that high-level coherence can emerge from pure noise without coherent sources, violating the `J_ij = Kτ_i * ...` model."
      status: proposed
      links: [DOMA-158, DYNA-001]
naming_notes:
  collisions: [K is used for kinetic energy, spring constants, and temperature (Kelvin). τ is used for time constants and torque. The combined symbol Kτ is unique within the framework.]
  disambiguation: |
    Node Coherence (Kτ) is a property of a single vertex. It must be distinguished from Channel Coherence (an edge property related to `1-Γ`) and System Coherence (a global network property derived from the Coherence Laplacian's spectrum).
crosslinks:
  near_synonyms: [T_a_node]
  antonyms: [TURBULENCE]
  prerequisites: []
  downstream_effects: [COHERENCE_FLOW, COHERENCE_LAPLACIAN]
license: CC-BY-SA-4.0
---

# Node Coherence

## Canonical (Pirouette)
Node Coherence (Kτ) is a dimensionless scalar quantity measuring the rhythmic purity and temporal stability of an individual node's activity pattern. It quantifies the degree to which a node's signal is a predictable, resonant pattern versus random noise, serving as the ultimate source of all Coherence Flow (`J`) that the node can emit into the network. It replaces the legacy `T_a_node` parameter.

## EFT-First Summary
Node Coherence is operationally equivalent to the **Quality Factor (Q factor)** of a resonator in physics. Just as a high-Q mechanical or electrical system resonates very cleanly at a specific frequency with minimal energy loss, a high-Kτ node exhibits a pure, stable rhythm. This "purity" is measured by the sharpness of its peak in the frequency domain. As the primary "kinetic" term in the system's Lagrangian, Kτ represents the potential for a node to perform coherent work on the network.

## Glossary Links
- See also: [Channel Pressure](<glossar_entry_for_gamma>), [Coherence Flow](<glossar_entry_for_j>), [Temporal Phase](<glossar_entry_for_phi>), [Turbulence](<glossar_entry_for_turbulence>)