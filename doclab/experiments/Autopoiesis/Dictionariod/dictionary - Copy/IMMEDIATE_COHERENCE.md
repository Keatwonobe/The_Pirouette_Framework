---
term: "Immediate Coherence"
canonical_id: "IMMEDIATE_COHERENCE"
symbol: "*K*<sub>i</sub>"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-018"]
---

---
term: Immediate Coherence
canonical_id: IMMEDIATE_COHERENCE
symbol: *K*<sub>i</sub>
aliases: []
parents: [DOMA-018]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-018
      lines: "§2"
      snippet: |
        2. Immediate Coherence (Ki): Resonance with the Present
        This is a system's ability to act, react, and harmonize with its current environment. It governs interaction, exchange, and response.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    This is the touch of what a system is now, the resonant handshake with its world. It is the clarity of a note sung into an awaiting chamber, the responsive grace of a dancer in the flow of the music.
  law: |
    A system's rate of energy and information exchange with its environment is directly proportional to its Immediate Coherence. As *K*<sub>i</sub> → 0, the system becomes functionally isolated, leading to Coherence Atrophy.
  philosophy: |
    To exist is to interact. *K*<sub>i</sub> asserts that presence is not a passive state but an active, continuous process of coupling with the environment. It is the dimension of coherence that makes a system a participant in its world, rather than a mere object passing through it.
pirouette_definition: |
  Immediate Coherence, *K*<sub>i</sub>, is the component of the Temporal Coherence vector (**K**_τ) that quantifies a system's capacity to interact, exchange, and resonate with its immediate environment in real-time. It is the measure of a system's active presence and responsiveness. Governed by the mechanisms of the Resonant Handshake and the projection of a clear Observer's Shadow, it manifests as communication, symbiosis, empathy, and flow states.
operational_definition:
  units: Dimensionless, typically normalized to the range [0, 1].
  symbol_table:
    - name: *K*<sub>i</sub>
      meaning: Immediate Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: **K**_τ
      meaning: Temporal Coherence Vector
      dimensions: dimensionless
      default_range: contextual
    - name: *K*<sub>p</sub>
      meaning: Prospective Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: *K*<sub>r</sub>
      meaning: Retrospective Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Transactional Bandwidth Analysis
        outline: |
          1. Define the system boundary and the interface with its environment.
          2. Identify all channels of energy and information exchange (e.g., communication links, resource flows, sensory inputs).
          3. Over a defined time interval, measure the bit rate, energy flux, and signal-to-noise ratio across these channels.
          4. Normalize these values against channel capacity and theoretical maximums.
          5. *K*<sub>i</sub> is the integrated, normalized measure of this transactional throughput and fidelity.
        expected_signals: [High signal-to-noise ratio in communication, low-latency stimulus-response cycles, high volume of successful transactions (e.g., trade, mutualistic exchange).]
        pitfalls: [Observer effects altering the interaction, mischaracterizing the system boundary, mistaking noise for signal.]
context_windows:
  - module: DOMA-018
    excerpt: |
      **2. Immediate Coherence (*K*<sub>i</sub>): *Resonance with the Present***
      This is a system's ability to act, react, and harmonize with its current environment. It governs interaction, exchange, and response.
      *   **Mechanism:** The Resonant Handshake of an Alchemical Union (CORE-012) and the projection of a clear Observer's Shadow (CORE-010). It is the active, real-time process of resonant coupling.
      *   **Manifestation:** Communication, empathy, symbiosis, trade, the flow state of an athlete responding to the game in real-time.
  - module: DOMA-018
    excerpt: |
      This model provides a compass for the act of observation itself... The nature of a Weaver's observation—their tools, their questions, their intent—preferentially engages one of the three coherence axes.
      *   A quantum measurement or strategic forecast probes **Prospective Coherence**.
      *   A social network analysis or real-time dialogue probes **Immediate Coherence**.
      *   An archaeological dig or a study of memory probes **Retrospective Coherence**.
poetic_connections:
  motifs: [Resonant Handshake, Flow State, Dialogue, Symbiosis, The Present Moment]
  evocative_lines:
    - "the touch of what it is now"
    - "a chord, struck in the resonant chamber of the present moment"
  association_matrix:
    - [ "Observer's Shadow", 0.9 ]
    - [ "Alchemical Union", 0.8 ]
    - [ "Isolation", -1.0 ]
    - [ "Prospective Coherence", 0.0 ]
    - [ "Retrospective Coherence", 0.0 ]
formal_mappings:
  candidates:
    - target: Coupling constant (*g*)
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        Interaction Lagrangian: 𝓛_int ∝ *g* ψ̄Γφ
      justification: |
        *K*<sub>i</sub> measures the strength of a system's real-time interaction with its environment. This is conceptually equivalent to a coupling constant *g* in field theory, which sets the strength of the vertex interaction between a field (the system) and another field (the environment). A high *K*<sub>i</sub> implies a large interaction cross-section, just as a large *g* does.
      references:
        - title: An Introduction to Quantum Field Theory
          where: M. Peskin & D. Schroeder, Chapter 4
          date: 1995-10-01
      confidence: 0.4
    - target: Dynamic susceptibility (χ(ω))
      domain: CM
      mapping_kind: operational
      equation_hint: |
        Response(ω) = χ(ω) × Force(ω)
      justification: |
        *K*<sub>i</sub> describes the ability to "react and harmonize." This is directly measured by a system's response function or susceptibility, which quantifies how strongly a system's state is affected by an external, time-varying field. High *K*<sub>i</sub> would correspond to a large, resonant peak in the susceptibility spectrum.
      references:
        - title: Statistical Mechanics
          where: R. K. Pathria, Chapter on Linear Response Theory
          date: 2011-02-15
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system with vanishing Immediate Coherence (*K*<sub>i</sub> → 0) is empirically indistinguishable from a non-interacting, solipsistic system and will undergo Coherence Atrophy."
      domain: phenomenology
      falsifier: "The discovery of a stable, long-lived system that is demonstrably non-interactive with its environment yet does not decay or lose internal complexity."
      status: proposed
      links: [DOMA-018]
naming_notes:
  collisions: [The symbol *K* is commonly used for kinetic energy in physics. The subscript 'i' can denote 'initial' or an index.]
  disambiguation: |
    *K*<sub>i</sub> is not a measure of motion or energy, but of interaction potential and efficacy. It is one of three orthogonal components of the *Temporal* Coherence vector, specifically the one oriented to the present moment. Contrast with *K*<sub>p</sub> (future potential) and *K*<sub>r</sub> (past inertia).
crosslinks:
  near_synonyms: []
  antonyms: [ISOLATION]
  prerequisites: [TEMPORAL_COHERENCE, OBSERVERS_SHADOW]
  downstream_effects: [COHERENCE_ATROPHY]
license: CC-BY-SA-4.0
---