---
term: "Coherence Curvature"
canonical_id: "COHERENCE_CURVATURE"
symbol: "γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-140"]
---

---
term: Coherence Curvature
canonical_id: COHERENCE_CURVATURE
symbol: γ
aliases: []
parents: [DOMA-140, CORE-006, CORE-008]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-140
      snippet: |
        **Coherence Curvature (γ):** The rate of change in a trajectory's direction. High curvature signifies that the path is being sharply bent by a strong pull towards a central attractor.
  editors: [Weaver-Agent-7]
  review_log: []
triad:
  art: |
    Curvature is the arc of the skater's blade on the ice, a visible trace of the invisible center of gravity they orbit. It is the signature of a bond, the bend in a path that reveals a relationship.
  law: |
    Coherence Curvature is the rate of change of a trajectory's directional vector within a state space, normalized by the observation interval. A sustained, non-zero γ is a necessary condition for a system to be in a state of Gladiator Confinement.
  philosophy: |
    A straight path signifies inertia or freedom; a curved path signifies influence. Measuring curvature is to map the invisible forces of attraction and constraint that define a system's world. It makes the architecture of confinement visible.
pirouette_definition: |
  Coherence Curvature (γ) is a dimensionless measure of the rate of change of a system's trajectory through a state space. As a component of Confinement Strength (κ_G), it quantifies the degree to which a system's path is being actively bent by a local gradient in the coherence manifold, such as a Gladiator well. It is calculated as the practical gradient of a coherence metric over a defined interval, serving as a direct geometric proxy for the intensity of a local confining force.
operational_definition:
  units: Dimensionless (or radians per interval)
  symbol_table:
    - name: γ
      meaning: Coherence Curvature
      dimensions: dimensionless
      default_range: "[0, 1] after normalization"
  measurement:
    procedures:
      - name: Gladiator Compass Protocol (§4)
        outline: |
          1. Ingest an ordered stream of events and vectorize them into a sequence of state vectors {v_1, v_2, ... v_n}.
          2. Within a sliding window, calculate the initial directional vector (e.g., v_2 - v_1) and the final directional vector (e.g., v_n - v_{n-1}).
          3. Compute the angle or distance between the normalized initial and final directional vectors.
          4. Normalize this change by the window size to get the rate of change, γ.
        expected_signals: [High, stable γ within stable orbits or near ideological centers., Low, noisy γ for chaotic or unconstrained trajectories.]
        pitfalls: [Selection of window size is critical; too small captures noise, too large smooths over local features., State space vectorization must be meaningful for the domain to yield a valid coherence metric.]
context_windows:
  - module: DOMA-140
    excerpt: |
      **Coherence Curvature (γ):** The rate of change in a trajectory's direction. High curvature signifies that the path is being sharply bent by a strong pull towards a central attractor. ... A high κ_G value emerges where paths are both short (high δ) and sharply bent (high γ). This is the unambiguous signature of a confinement well—the heart of an arena.
  - module: DOMA-140
    excerpt: |
      Within such a well, the geodesics of maximal coherence are no longer straight lines. They are short, tightly curved paths that orbit the well's center. The Gladiator Compass works by observing these distorted paths. By measuring the degree of distortion, we can infer the depth of the well and thus the strength of the confining force that created it.
poetic_connections:
  motifs: [gravity wells, orbits, arena walls, carving arcs, bent light, geodesic deviation]
  evocative_lines:
    - "We are watching the dancer to understand the shape of the stage."
    - "We sought to measure the strength of the cage and instead learned how to draw a map of its walls."
  association_matrix:
    - [ "CONFINEMENT_STRENGTH", 0.9 ]
    - [ "GLADIATOR_FORCE", 0.8 ]
    - [ "PATH_DENSITY", 0.6 ]
    - [ "TEMPORAL_PRESSURE", 0.4 ]
formal_mappings:
  candidates:
    - target: Geodesic deviation / Curvature tensor (R^a_{bcd})
      domain: GR|Math
      mapping_kind: conceptual
      equation_hint: |
        d²Vª/dλ² = Rª_{bcd} U^b U^c V^d  (Equation of geodesic deviation)
      justification: |
        Coherence Curvature measures the bending of a system's worldline (geodesic) in its coherence manifold. This is conceptually analogous to how the Riemann curvature tensor in General Relativity describes the tidal forces or geodesic deviation caused by the curvature of spacetime. A high γ implies a highly curved local manifold.
      references:
        - title: "Gravitation"
          where: "Misner, Thorne, & Wheeler, Ch. 1"
          date: 1973-09-15
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "In any stable, self-reinforcing system (e.g., a political ideology, a planetary orbit), the average Coherence Curvature (γ) of its constituent entities will be significantly non-zero and positively correlated with the system's overall stability."
      domain: phenomenology
      falsifier: "Discovery of a highly stable, long-lived system where the trajectories of its components show near-zero average curvature. This would imply that confinement can be achieved without geometric bending, falsifying the core claim of the Gladiator Compass protocol."
      status: proposed
      links: [DOMA-140]
naming_notes:
  collisions: [The symbol γ is commonly used for the Lorentz factor in special relativity and as the symbol for a photon.]
  disambiguation: |
    Distinguish from Path Density (δ), which measures path *length*, not path *bending*. A system can have high δ (short, random paths) but low γ (no consistent turning), as in Brownian motion. Coherence Curvature requires directed, sustained bending toward an attractor.
crosslinks:
  near_synonyms: []
  antonyms: [GEODESIC_STRAIGHTNESS]
  prerequisites: [CONFINEMENT_DERIVATION, PIROUETTE_LAGRANGIAN]
  downstream_effects: [CONFINEMENT_STRENGTH, COGNITIVE_GRAVITY_WELL]
license: CC-BY-SA-4.0