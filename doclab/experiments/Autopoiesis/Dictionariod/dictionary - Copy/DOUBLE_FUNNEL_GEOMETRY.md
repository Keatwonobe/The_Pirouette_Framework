---
term: "Double-funnel geometry"
canonical_id: "DOUBLE_FUNNEL_GEOMETRY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-204"]
---

---
term: Double-funnel geometry
canonical_id: DOUBLE_FUNNEL_GEOMETRY
symbol: Φ₂
aliases: [Sutured Funnel Topology]
parents: [DOMA-204]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-204
      lines: "§3, para 2"
      snippet: |
        The double-funnel geometry described in the original protocol is an optimal topology for this interaction. It redirects the momentum of an incoming object tangentially, "skimming" it along the surface of the shield rather than meeting it with direct opposition.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A geometry that teaches incoming force to skate rather than shatter. It turns a wall into a graceful vortex, guiding impact into a harmless glancing blow.
  law: |
    A Resonant Wall constructed with a Φ₂ topology will exhibit entropic bleed (`S_bleed`) at least one order of magnitude lower than a planar geometry when subjected to the same incident momentum flux.
  philosophy: |
    The most effective defense is not one of absolute opposition, but of elegant redirection. This geometry embodies the principle that stability is achieved by minimizing interaction, not by winning a contest of strength.
pirouette_definition: |
  The optimal, closed-manifold topology for a Resonant Wall, formed by the phase-conjugate suture of two extruded coherence funnels. Its primary function is to create a coherence potential gradient that redirects incident momentum tangentially across the wall's surface, thereby minimizing entropic bleed and maximizing shield stability.
operational_definition:
  units: Dimensionless (topological class)
  symbol_table:
    - name: Φ₂
      meaning: Denotes a double-funnel topological class.
      dimensions: dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Manifold Topography via Coherence Scattering
        outline: |
          A low-energy particle beam is raster-scanned across the Resonant Wall's surface. The deflection angle and coherence phase-shift of the scattered particles are measured at each point. This data is used to reconstruct the 3D coherence potential gradient (`|∇Kτ|`), revealing the underlying manifold topology.
        expected_signals: [Saddle-point potential signature at the suture line, Tangential scattering vectors dominant over normal-incidence vectors]
        pitfalls: [Probe particle energy is too high, inducing `S_bleed` and distorting the measured geometry, Insufficient spatial resolution to resolve the suture manifold]
context_windows:
  - module: DOMA-204
    excerpt: |
      The Resonant Wall functions as a near-perfect shield because it is a surface of extreme, static temporal coherence... The double-funnel geometry described in the original protocol is an optimal topology for this interaction. It redirects the momentum of an incoming object tangentially, "skimming" it along the surface of the shield rather than meeting it with direct opposition. This minimizes the transfer of dissonant energy, or entropic bleed, into the shield's structure, ensuring its stability.
poetic_connections:
  motifs: [vortex, redirection, glancing blow, skate, suture, manifold]
  evocative_lines:
    - "We do not build a wall to stop a fist. We build a moment in time so solid that the fist forgets it was ever thrown."
  association_matrix:
    - [ "RESONANT_WALL", 0.9 ]
    - [ "ENTROPIC_BLEED", 0.8 ]
    - [ "MANIFOLD_SUTURE", 0.7 ]
formal_mappings:
  candidates:
    - target: Magnetic mirror
      domain: Plasma Physics
      mapping_kind: conceptual
      equation_hint: |
        ∇⋅B ≠ 0 (at mirror points) ↔ |∇Kτ| is maximized tangentially
      justification: |
        The Φ₂ geometry acts as a "coherence nozzle" that redirects incident trajectories. This is conceptually analogous to a magnetic mirror, which uses a shaped magnetic field gradient to reflect and guide charged particles, converting momentum between transverse and axial components to achieve confinement.
      references:
        - title: Introduction to Plasma Physics and Controlled Fusion
          where: Chapter 2
          date: 1984-01-01
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A double-funnel geometry is the optimal topology for minimizing entropic bleed in a Resonant Wall under kinetic load."
      domain: experiment
      falsifier: "Discovery of an alternative, achievable geometry (e.g., a toroidal or gyroidal manifold) that demonstrates a statistically significant lower `S_bleed` value under identical test conditions (incident flux, energy, and particle type)."
      status: supported
      links: [DOMA-204]
naming_notes:
  collisions: [Φ is a common symbol for magnetic flux or a generic scalar field.]
  disambiguation: |
    Φ₂ refers not to a physical object with a funnel shape, but to the topology of the coherence potential manifold that constitutes the Resonant Wall. The geometry describes the "slope" of coherence, not a material structure.
crosslinks:
  near_synonyms: []
  antonyms: [PLANAR_GEOMETRY]
  prerequisites: [RESONANT_WALL, MANIFOLD_SUTURE]
  downstream_effects: [ENTROPIC_BLEED]
license: CC-BY-SA-4.0
---