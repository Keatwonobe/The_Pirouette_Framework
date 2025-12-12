---
term: "Outward Pole"
canonical_id: "OUTWARD_POLE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-002_the_nomad's_grammar"]
---

---
term: Outward Pole
canonical_id: OUTWARD_POLE
symbol: 
aliases: [Divergence, Expansion, Emission]
parents: [CORE-002_the_nomad's_grammar]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-002_the_nomad's_grammar
      lines: "§2"
      snippet: |
        Outward Pole: The system's dynamic is dominated by divergence, expansion, or emission. It projects itself onto the environment. Manifestations: Radiation, positive electric charge, explosions, expression.
  editors: [system_agent]
  review_log: []
triad:
  art: |
    To be a sun, a voice, a volcano. It is the fundamental act of giving, of projecting the self into the world, whether as light, force, or idea.
  law: |
    A system is defined as net-Outward when the integral of its energy-momentum flux across a bounding surface is positive, directed away from its center of mass. The magnitude of its Outward state is proportional to the net positive value of this flux.
  philosophy: |
    The Outward pole represents the principle of expression and influence. It is the necessary counterpoint to Inward absorption, enabling systems to interact, shape their environment, and participate in the cosmic dialogue. Without it, all matter would collapse into silent, isolated points.
pirouette_definition: |
  The positive pole of the Vector axis, characterized by a system dynamic dominated by divergence, expansion, or emission. An Outward system projects energy, matter, or information onto its environment, increasing its influence at the cost of its internal reserves. It is the fundamental behavioral verb for all forms of radiation, expression, and explosion.
operational_definition:
  units: Dimensionless polarity or normalized ratio
  symbol_table:
    - name: V⃗
      meaning: State on the Vector axis. Outward corresponds to a positive value.
      dimensions: dimensionless
      default_range: [-1, 1], where +1 is maximally Outward.
  measurement:
    procedures:
      - name: Bounding Sphere Flux Analysis
        outline: |
          1. Define a Gaussian surface around the system's center of mass.
          2. Integrate the flux of all relevant fields (e.g., Poynting vector, stress-energy tensor, particle flow) across the surface over a characteristic time interval.
          3. A sustained positive net flux (outflow > inflow) indicates an Outward state.
          4. Normalize the result against the system's total internal energy or a theoretical maximum to determine magnitude.
        expected_signals: [Net positive energy-momentum flux, particle emission, radiation pressure]
        pitfalls: [Ambiguous system boundary definition, accounting for all forms of flux, time-averaging artifacts]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: CORE-002_the_nomad's_grammar
    excerpt: |
      Outward Pole: The system's dynamic is dominated by divergence, expansion, or emission. It projects itself onto the environment. Manifestations: Radiation, positive electric charge, explosions, expression.
  - module: CORE-002_the_nomad's_grammar
    excerpt: |
      A Star: Highly Outward (radiation), highly Random (thermonuclear chaos), and moderately Isolated (self-contained by its own gravity).
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [sun, broadcast, explosion, spring, voice, fountain]
  evocative_lines:
    - "These are the verbs of existence..."
    - "...the choices every particle and every person makes at every moment."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "INWARD_POLE", -1.0 ]
    - [ "RADIATION", 0.9 ]
    - [ "RANDOM_POLE", 0.5 ]
    - [ "TRANSACTIONAL_POLE", 0.3 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Positive divergence of a vector field (∇ ⋅ F > 0)
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        ∫_V (∇ ⋅ F) dV = ∮_S (F ⋅ n̂) dS > 0
      justification: |
        The Outward pole is the physical manifestation of a source or positive divergence. The Divergence Theorem directly relates the internal "source" behavior to the net "outflow" across a boundary, mirroring the operational definition.
      references: []
      confidence: 0.9
    - target: Positive electric charge (+q)
      domain: SM
      mapping_kind: conceptual
      equation_hint: |
        ∇ ⋅ E = ρ/ε₀ where ρ > 0
      justification: |
        The source text explicitly lists positive electric charge as a manifestation. A positive charge acts as a source for the electric field, causing field lines to diverge outwards, a direct geometric analogue to the Outward pole.
      references: []
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "All phenomena classified as 'radiation' (e.g., thermal, EM, particle) will measure as having a positive (Outward) Vector pole."
      domain: phenomenology
      falsifier: "Discovery of a form of radiation that is fundamentally convergent or which does not involve a net outflow of energy/matter from a source system."
      status: proposed
      links: [CORE-002_the_nomad's_grammar]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from the Transactional pole of the Communion axis. Outward describes the *direction* of flow (emission), while Transactional describes the *intent* to connect or bond. A star is highly Outward (emits radiation) but not highly Transactional; a conversation is highly Transactional but may have a neutral Vector.
crosslinks:
  near_synonyms: [DIVERGENCE, EMISSION]
  antonyms: [INWARD_POLE]
  prerequisites: [VECTOR_AXIS]
  downstream_effects: []
license: CC-BY-SA-4.0