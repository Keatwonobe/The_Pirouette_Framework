---
term: "Vector"
canonical_id: "VECTOR"
symbol: ""
aliases: [Axis of Flow]
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-002_the_nomad's_grammar"]
---

---
term: Vector
canonical_id: VECTOR
symbol: V⃗
aliases: ["Axis of Flow"]
parents: ["CORE-002_the_nomad's_grammar"]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-002_the_nomad's_grammar
      lines: "L15-L23"
      snippet: |
        **Vector (Axis of Flow):** Describes the primary direction of a system's interaction with its environment.
        Inward Pole: The system's dynamic is dominated by convergence, contraction, or absorption. It pulls the environment into itself.
        Outward Pole: The system's dynamic is dominated by divergence, expansion, or emission. It projects itself onto the environment.
  editors: [auto-agent-alpha]
  review_log: []
triad:
  art: |
    The universe breathes, its pulse a rhythm of gathering and release. A system's Vector is its part in this cosmic respiration, inhaling the world or exhaling its own essence upon the void.
  law: |
    The Vector of a system is determined by the net flux of energy, matter, or information across its defined boundary. A net influx defines an Inward Vector (V⃗ < 0); a net outflux defines an Outward Vector (V⃗ > 0).
  philosophy: |
    Vector re-casts fundamental interactions not as static properties but as dynamic postures of 'giving' or 'taking'. It replaces the 'what' of a force (e.g., gravity) with the 'how' of its action (a persistent inward pull), providing a universal geometric language for interaction.
pirouette_definition: |
  Vector is a primary axis of the Behavioral Triad, describing the net directional flow of interaction between a system and its environment. It is a continuous bipolar axis ranging from the Inward Pole (net absorption, convergence, contraction) to the Outward Pole (net emission, divergence, expansion). Any system's state can be characterized by its position along this axis, indicating whether it is primarily drawing from or projecting onto its surroundings.
operational_definition:
  units: dimensionless, normalized to [-1, 1]
  symbol_table:
    - name: V⃗
      meaning: Net interactive flow; position on the Inward-Outward axis.
      dimensions: dimensionless
      default_range: [-1, 1]
  measurement:
    procedures:
      - name: Boundary Flux Analysis
        outline: |
          1. Define a system boundary (a topological 2-surface).
          2. Select a conserved quantity (e.g., energy-momentum, particle number) relevant to the system's primary interactions.
          3. Integrate the flux of this quantity across the boundary over a characteristic timescale.
          4. Normalize the resulting net flow to the range [-1, 1], where -1 is maximum observed influx and +1 is maximum observed outflux.
        expected_signals: [Net energy-momentum flux (T⁰ⁱ), particle number current, Poynting vector flux]
        pitfalls: [Ambiguous boundary definition, timescale dependency, selection of the relevant flux quantity]
context_windows:
  - module: CORE-002_the_nomad's_grammar
    excerpt: |
      **Vector (Axis of Flow):** Describes the primary direction of a system's interaction with its environment. Inward Pole: The system's dynamic is dominated by convergence, contraction, or absorption... Manifestations: Gravity (confinement of baryonic matter), negative electric charge, collapse, consumption. Outward Pole: The system's dynamic is dominated by divergence, expansion, or emission... Manifestations: Radiation, positive electric charge, explosions, expression.
  - module: CORE-002_the_nomad's_grammar
    excerpt: |
      This triad allows us to move past labels and describe causes. We can now describe any phenomenon by its behavioral coordinates. A Star: Highly Outward (radiation), highly Random (thermonuclear chaos), and moderately Isolated (self-contained by its own gravity). A Magnet: Neutral Vector, highly Aligned (its domains are ordered), and highly Isolated (it maintains its own state).
  - module: CORE-002_the_nomad's_grammar
    excerpt: |
      We must learn the grammar. Inward or Outward. Aligned or Random. Transactional or Isolated. These are the verbs of existence, the choices every particle and every person makes at every moment. They are the notes that compose the resonant signal propagating through the wake of the Traveler.
poetic_connections:
  motifs: [breath, tide, source/sink, give/take, focus/radiate]
  evocative_lines:
    - "Inward or Outward... These are the verbs of existence."
    - "A system of purely Isolated entities is simple and fragile."
  association_matrix:
    - [ "GRAVITY", 0.9 ]
    - [ "RADIATION", 0.9 ]
    - [ "COHESION", 0.5 ]
    - [ "COMMUNION", 0.5 ]
formal_mappings:
  candidates:
    - target: Divergence of a flux 4-vector, ∂μJμ
      domain: Math|EFT
      mapping_kind: mathematical
      equation_hint: |
        V⃗ ∝ ∫ ∂μJμ d⁴x
      justification: |
        The divergence of a conserved current measures the local density of its source or sink. Integrating this over a spacetime volume yields the net creation or annihilation (outflow or inflow) within that volume, which is a direct mathematical analog of the Vector concept. A positive divergence (source) maps to Outward; negative (sink) maps to Inward.
      references:
        - title: Peskin & Schroeder, An Introduction to Quantum Field Theory
          where: "Ch. 2: The Klein-Gordon Field"
          date: 1995-10-01
      confidence: 0.9
    - target: Electric Charge (Sign)
      domain: SM
      mapping_kind: conceptual
      equation_hint: |
        sgn(V⃗) = sgn(q)
      justification: |
        The module explicitly maps negative charge to the Inward Pole and positive charge to the Outward Pole. This aligns with the convention of positive charges as sources of electric field lines (positive divergence) and negative charges as sinks (negative divergence) per Gauss's Law.
      references:
        - title: Griffiths, Introduction to Electrodynamics
          where: "Ch. 2: Electrostatics"
          date: 2017-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "All fundamental attractive long-range forces manifest a net Inward Vector, while repulsive ones manifest a net Outward Vector."
      domain: theory
      falsifier: "The discovery of a fundamental interaction that is purely attractive but is operationally associated with a net outflux of a primary conserved quantity (e.g., energy), or vice-versa for a repulsive force."
      status: proposed
      links: ["CORE-002_the_nomad's_grammar"]
naming_notes:
  collisions: ["Vector (mathematical quantity with magnitude and direction)"]
  disambiguation: |
    In Pirouette, 'Vector' is a scalar value along the single Inward-Outward axis, not a general mathematical vector. The arrow symbol `V⃗` is used metaphorically to indicate this axis of flow and its two poles, not spatial directionality.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [SYSTEM_BOUNDARY]
  downstream_effects: [COHESION, COMMUNION]
license: CC-BY-SA-4.0