---
term: "Behavioral Triad"
canonical_id: "BEHAVIORAL_TRIAD"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-002_the_nomad's_grammar"]
---

---
term: Behavioral Triad
canonical_id: BEHAVIORAL_TRIAD
symbol: (V, C, K)
aliases: [The Nomad's Grammar]
parents: [CORE-002_the_nomad's_grammar]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-002_the_nomad's_grammar
      lines: "§2"
      snippet: |
        The state of any entity can be described by its position within this three-dimensional behavioral space.
  editors: [Agent_GPT-4]
  review_log: []
triad:
  art: |
    The dance of existence choreographed in three movements: flow, form, and fellowship. It is the posture of a particle, the gesture of a galaxy, and the intention of a mind, all described by the same universal grammar.
  law: |
    The dynamic state of any system, at any scale, can be fully characterized by its coordinates (v, c, k) within the three orthogonal axes of Vector (inward/outward flow), Cohesion (ordered/random state), and Communion (transactional/isolated interaction). Any observable change in a system is a trajectory in this state space.
  philosophy: |
    To move beyond labeling effects (forces) to describing the fundamental causal geometry of behavior. This universal grammar seeks to unify descriptions of physical, biological, and conscious systems, revealing a shared underlying dynamic and a universal bias towards complexity and connection (the "time attractor").
pirouette_definition: |
  A universal, triaxial coordinate system for describing the dynamic posture of any entity. The three orthogonal axes are: **Vector (V)**, the axis of flow, describing a system's convergence (Inward) or divergence (Outward) with its environment; **Cohesion (C)**, the axis of order, describing the internal alignment (Aligned) or disorder (Random) of a system's components; and **Communion (K)**, the axis of connection, describing a system's tendency to bond (Transactional) or self-contain (Isolated).
operational_definition:
  units: Dimensionless, with each axis typically normalized to [-1, 1].
  symbol_table:
    - name: V
      meaning: Vector axis coordinate; positive values denote Outward flow, negative values denote Inward flow.
      dimensions: dimensionless
      default_range: "[-1, 1]"
    - name: C
      meaning: Cohesion axis coordinate; positive values denote Aligned order, negative values denote Random disorder.
      dimensions: dimensionless
      default_range: "[-1, 1]"
    - name: K
      meaning: Communion axis coordinate; positive values denote Transactional connection, negative values denote Isolation.
      dimensions: dimensionless
      default_range: "[-1, 1]"
  measurement:
    procedures:
      - name: Observational Mapping
        outline: |
          1. Define the system boundary and timescale of interest.
          2. Measure net energy/mass/information flux across the boundary to determine the Vector coordinate (net efflux = Outward, net influx = Inward).
          3. Measure the system's internal entropy or component correlation (e.g., spin alignment, phase coherence) to determine the Cohesion coordinate (low entropy/high correlation = Aligned).
          4. Measure the rate, stability, and type of bond formation/exchange with external systems to determine the Communion coordinate (high interaction rate = Transactional).
        expected_signals: [Divergence in energy flow fields (Vector), phase transitions/entropy shifts (Cohesion), changes in chemical bonding rates or network connectivity (Communion).]
        pitfalls: [Ambiguous system boundaries, scale-dependence of measurements, mistaking static properties for dynamic posture.]
context_windows:
  - module: CORE-002_the_nomad's_grammar
    excerpt: |
      This protocol introduces a universal, scale-invariant language for describing entity behavior, called the Behavioral Triad. This is a triaxial system designed to describe the dynamic nature or interactive posture of any system, from a quark to a galaxy to a living organism. It moves beyond labeling forces (effects) to describing the fundamental geometric and relational actions (causes) that produce those forces.
  - module: CORE-002_the_nomad's_grammar
    excerpt: |
      This triad allows us to move past labels and describe causes. We can now describe any phenomenon by its behavioral coordinates. A Star: Highly Outward (radiation), highly Random (thermonuclear chaos), and moderately Isolated (self-contained by its own gravity). A Magnet: Neutral Vector, highly Aligned (its domains are ordered), and highly Isolated (it maintains its own state). An Act of Kindness: Neutral Vector, highly Aligned (requires focused intention), and maximally Transactional (it exists only to form a bond).
poetic_connections:
  motifs: [geometry of behavior, universal grammar, flow, form, connection, posture, dance]
  evocative_lines:
    - "These are the verbs of existence, the choices every particle and every person makes at every moment."
    - "Connect, align, become more than you are."
  association_matrix:
    - [ "TIME_ATTRACTOR", 0.9 ]
    - [ "Entropy", 0.7 ]
    - [ "Information", 0.6 ]
formal_mappings:
  candidates:
    - target: Divergence of a vector field (∇ ⋅ F)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        V ∝ ∫_V (∇ ⋅ F) dV
      justification: |
        The Vector axis maps directly to the concept of sources (Outward, V > 0) and sinks (Inward, V < 0) in field theory. Positive divergence signifies a net flow out of a region, while negative divergence signifies a net flow in.
      references:
        - title: "Div, Grad, Curl, and All That"
          where: "Chapter 1"
          date: 2005-01-20
      confidence: 0.8
    - target: Entropy (S)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        C ∝ -S
      justification: |
        The Cohesion axis is inversely related to thermodynamic entropy. The Random pole is a state of maximum entropy (disorder) as described by the Second Law of Thermodynamics, while the Aligned pole represents a low-entropy, highly ordered state (e.g., a crystal at low temperature).
      references:
        - title: "Introduction to Thermal Physics"
          where: "Chapter 2"
          date: 1999-08-26
      confidence: 0.9
    - target: Interaction Cross-Section (σ)
      domain: SM
      mapping_kind: conceptual
      equation_hint: |
        K ∝ σ
      justification: |
        The Communion axis maps to the propensity of systems to interact. A high interaction cross-section (e.g., for Coulomb scattering) corresponds to a highly Transactional state. A low cross-section (e.g., for neutrinos) or chemical inertness (noble gases) corresponds to an Isolated state.
      references:
        - title: "Introduction to Elementary Particles"
          where: "Chapter 6"
          date: 2008-06-23
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "All observable phenomena can be uniquely and non-degenerately mapped to a coordinate in the Behavioral Triad space."
      domain: theory
      falsifier: "Discovering a fundamental phenomenon that requires a fourth orthogonal behavioral axis for its description, or demonstrating that two distinct phenomena consistently and irreducibly map to the exact same coordinate."
      status: proposed
      links: [CORE-002_the_nomad's_grammar]
naming_notes:
  collisions: [The term "Vector" is heavily overloaded in mathematics and physics. "Cohesion" is a specific term in materials science and chemistry. "Communion" carries theological and social connotations.]
  disambiguation: |
    Within the Pirouette Framework, these terms refer specifically to the three orthogonal axes of dynamic posture. They are abstract descriptors of behavior, not direct replacements for their counterparts in other domains. For instance, Vector here means "net flow directionality," not a mathematical object with magnitude and direction in Euclidean space.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: []
  downstream_effects: [TIME_ATTRACTOR]
license: CC-BY-SA-4.0
---

# Behavioral Triad

## Canonical (Pirouette)
A universal, triaxial coordinate system for describing the dynamic posture of any entity. The three orthogonal axes are: **Vector (V)**, the axis of flow, describing a system's convergence (Inward) or divergence (Outward) with its environment; **Cohesion (C)**, the axis of order, describing the internal alignment (Aligned) or disorder (Random) of a system's components; and **Communion (K)**, the axis of connection, describing a system's tendency to bond (Transactional) or self-contain (Isolated).

## EFT-First Summary
The Behavioral Triad provides a state-space for dynamics where physical concepts find conceptual analogues. The Vector axis is analogous to the divergence of a physical field (e.g., `∇ ⋅ E`), describing net flux from sources and sinks. The Cohesion axis inversely maps to entropy (S), describing states from maximum disorder (Random) to perfect order (Aligned). The Communion axis relates to a system's propensity for interaction, conceptually mapping to quantities like interaction cross-section (σ) or chemical potential.

## Glossary Links
- See also: TIME_ATTRACTOR