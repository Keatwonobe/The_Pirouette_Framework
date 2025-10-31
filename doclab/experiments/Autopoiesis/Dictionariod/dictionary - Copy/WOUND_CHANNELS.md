---
term: "Wound Channels"
canonical_id: "WOUND_CHANNELS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-055"]
---

---
term: Wound Channels
canonical_id: WOUND_CHANNELS
symbol: Ψ_W
aliases: []
parents: [DOMA-055, CORE-011]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-055
      lines: "L24-L26"
      snippet: |
        It is not a passive stage but an active, responsive fabric, shaped and textured by the history of every resonance that has ever occurred, physically encoded as Wound Channels (CORE-011).
  editors: [system]
  review_log: []
triad:
  art: |
    A scar left in spacetime by the passage of a resonance, a memory groove that gives inertia to the present. The deeper the scar, the harder it is for the system to change course.
  law: |
    A system's mass is directly proportional to the integrated coherence density of its Wound Channel. To alter a system's momentum is to overcome the geometric inertia of this channel.
  philosophy: |
    Wound Channels establish that history is not an abstract record but a physical, causal structure. The past is not gone; it is the landscape upon which the present must move, making mass an emergent property of memory.
pirouette_definition: |
  A Wound Channel is a persistent, geometric deformation of the Coherence Manifold, encoding the integrated history of a system's resonance (Ki). This channel represents a region of high coherence density that the system has carved through its own existence. The interaction of a system with its own Wound Channel is the source of its resonant inertia, which is measured macroscopically as mass.
operational_definition:
  units: kg (as its emergent property, mass)
  symbol_table:
    - name: Ψ_W
      meaning: Wound Channel Coherence Density
      dimensions: M L⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Historical Geodesic Deflection
        outline: |
          Measure the deflection of a low-coherence probe system (e.g., a photon) as it passes near the historical path (the Wound Channel) of a high-coherence, massive system, even after the massive system is no longer present on that trajectory. The measurement detects the residual curvature of the channel itself.
        expected_signals: [Anomalous gravitational lensing, Path-dependent time dilation]
        pitfalls: [Signal is predicted to be extremely weak and may decay over time, Confounding signals from background manifold fluctuations or other gravitational sources]
context_windows:
  - module: DOMA-055
    excerpt: |
      The Loom is the Coherence Manifold. This is not a metaphor for spacetime; it is the dynamic, geometric substance of spacetime itself. It is not a passive stage but an active, responsive fabric, shaped and textured by the history of every resonance that has ever occurred, physically encoded as Wound Channels (CORE-011). The Manifold is the living sum of all these histories.
  - module: DOMA-055
    excerpt: |
      Mass Is The Inertia of Memory (CORE-011): A system's mass is a measure of its resonant inertia—its resistance to a change in state. This arises from the system's interaction with its own Wound Channel. A massive particle has carved a deep, stable groove in the Manifold; changing its trajectory requires expending energy to fight the geometry of its own past.
poetic_connections:
  motifs: [memory, inertia, scars, history, grooves, persistence, ghosts]
  evocative_lines:
    - "Mass Is The Inertia of Memory."
    - "...changing its trajectory requires expending energy to fight the geometry of its own past."
  association_matrix:
    - [ "MASS", 0.9 ]
    - [ "COHERENCE_MANIFOLD", 0.8 ]
    - [ "GEODESIC", 0.7 ]
formal_mappings:
  candidates:
    - target: Gravitational self-force / Radiation reaction
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        F_self ~ G m^2 / r^2
      justification: |
        The Wound Channel describes the effect of a system's own history on its dynamics, which manifests as inertia. This is conceptually parallel to the self-force in GR, where a body's own gravitational field affects its trajectory. Both concepts model a particle interacting with the "groove" it leaves in spacetime.
      references:
        - title: The motion of a classical charged particle
          where: "P. A. M. Dirac, Proc. R. Soc. Lond. A 167, 148 (1938)"
          date: 1938-08-24
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system's inertial mass is determined by its entire causal history, not solely its instantaneous configuration."
      domain: phenomenology
      falsifier: "Observation of two systems with identical instantaneous properties (e.g., charge, internal energy) but vastly different formation histories (e.g., one primordial, one freshly created from energy) exhibiting identical inertial mass to within measurement error."
      status: proposed
      links: [CORE-011]
naming_notes:
  collisions: []
  disambiguation: |
    A Wound Channel should not be confused with a geodesic. A geodesic is the path of maximal coherence a system *takes*, while the Wound Channel is the physical trace or geometric groove *left behind* by that passage, which in turn influences future geodesics.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_MANIFOLD, PIRouette_LAGRANGIAN]
  downstream_effects: [MASS, GLADIATOR_FORCE]
license: CC-BY-SA-4.0
---