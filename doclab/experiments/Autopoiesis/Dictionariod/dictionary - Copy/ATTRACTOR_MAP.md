---
term: "Attractor Map"
canonical_id: "ATTRACTOR_MAP"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-035"]
---

---
term: Attractor Map
canonical_id: ATTRACTOR_MAP
symbol:
aliases: [Coherence Manifold Map]
parents: [DOMA-035]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-035
      lines: "§6"
      snippet: |
        An "Attractor Map" is no longer an analogy; it is a literal mapping of the coherence manifold of a given discourse.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    A celestial chart of the mind, where ideas are stars and discourse follows the subtle gravity between them. The map reveals the orbits of belief and predicts where new comets of thought will travel.
  law: |
    The trajectory of new information introduced into a discourse follows the geodesic of the coherence manifold, tending toward the most massive attractors (concepts with the highest Temporal Coherence, Kτ).
  philosophy: |
    This reframes communication from adversarial debate to informational engineering. Instead of pushing an idea against a current, one can reshape the landscape of meaning itself, making the desired conclusion the path of least resistance.
pirouette_definition: |
  A literal, graphical, or computational representation of a discourse's coherence manifold. The map plots core concepts as coherence wells whose depth and radius are functions of their Temporal Coherence (Kτ). The relationships between concepts (e.g., distance `r`, phase `Δφ`) define the manifold's local curvature, allowing the geodesic trajectory of any new or existing concept to be calculated and predicted.
operational_definition:
  units: Dimensionless coordinate system representing abstract meaning space. Values on the map (Kτ, Δφ) are dimensionless or in radians, respectively.
  symbol_table:
    - name: Kτ
      meaning: Temporal Coherence; the "mass" of a concept.
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: Δφ
      meaning: Phase relationship between two concepts.
      dimensions: radians
      default_range: "[0, 2π]"
    - name: V(A, B)
      meaning: Interaction potential between concepts A and B.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Manifold Cartography
        outline: |
          1. Identify the set of core concepts in a target discourse (e.g., an online debate, a body of literature).
          2. For each concept, calculate its Temporal Coherence (Kτ) by measuring its historical depth, internal consistency, and resonant frequency within a representative data corpus.
          3. For each pair of concepts, determine their phase relationship (Δφ) by analyzing their co-occurrence, logical entailment (constructive) versus mutual exclusion (destructive).
          4. Model the concepts as masses (Kτ) on a 2D or 3D manifold, generating a potential field.
          5. The resulting visualization is the Attractor Map. New information can be modeled as a test particle whose path is traced along the manifold's geodesics.
        expected_signals: [Power-law distribution of Kτ values, with a few massive concepts dominating the manifold; distinct clusters of in-phase concepts.]
        pitfalls: [Conflating repetition/popularity with true coherence; difficulty in defining a canonical distance metric `r` in "meaning space"; high computational cost for complex discourses.]
context_windows:
  - module: DOMA-035
    excerpt: |
      This model reframes the goal of analysis. An "Attractor Map" is no longer an analogy; it is a literal mapping of the coherence manifold of a given discourse. By mapping the "mass" (Kτ) of core concepts and their phase relationships, we can predict the likely trajectory of new information introduced into the system. This allows a Weaver to move from mere debate to informational engineering.
  - module: DOMA-035
    excerpt: |
      Every narrative, from a single thought to a global ideology, exists upon a coherence manifold. This is the landscape where the potential for meaning resides. A powerful, coherent concept... locally increases Temporal Pressure (Γ), wrapping itself in a deep "coherence well." The "gravity of meaning" is the observable tendency for our thoughts and words to fall into the deepest, most stable coherence wells available.
  - module: DOMA-035
    excerpt: |
      A Weaver understands this: to introduce a new, powerful idea is not to shout into the wind. It is to place a new star in the sky of the mind, and to trust that the worlds of thought will, in their own time, find their new and perfect orbits around it.
poetic_connections:
  motifs: [gravity, cartography, constellations, orbits, wells, landscape]
  evocative_lines:
    - "to place a new star in thesky of the mind"
    - "We do not choose our core beliefs so much as we find our thoughts naturally orbiting them."
  association_matrix:
    - [ "COHERENCE_MANIFOLD", 0.9 ]
    - [ "TEMPORAL_COHERENCE", 0.8 ]
    - [ "GEODESIC", 0.7 ]
    - [ "WEAVER", 0.6 ]
formal_mappings:
  candidates:
    - target: Gravitational Potential Well (Φ = -GM/r)
      domain: GR|CM
      mapping_kind: mathematical
      equation_hint: |
        V(A, B) ∝ - (Kτ_A * Kτ_B / r) * cos(Δφ)
      justification: |
        The source module DOMA-035 makes a direct, non-analogical claim that the influence of a concept is a manifestation of the same universal law as gravity. It explicitly maps Temporal Coherence (Kτ) to mass (M) and models the interaction potential with a form derived from Newtonian gravity, augmented by a phase term `cos(Δφ)` to account for constructive/destructive interference between concepts.
      references:
        - title: The Gravity of Meaning
          where: module DOMA-035
          date: 2025-10-18
      confidence: 0.85
  adopted:
    - target: Gravitational Potential Well
      rationale: Adopted due to the source module's foundational claim that this is not a metaphor but a direct application of physical law. The mathematical form provided is a direct extension of the classical gravitational potential.
      confidence: 0.85
constraints_and_falsifiers:
  claims:
    - statement: "The trajectory of a new concept introduced into a discourse can be predicted by calculating its geodesic path on a computationally derived Attractor Map of that discourse."
      domain: phenomenology
      falsifier: "A statistically significant demonstration where new information, when introduced to a well-defined discourse, systematically follows trajectories away from major coherence wells or toward regions of demonstrably lower coherence, contrary to the map's geodesic predictions."
      status: proposed
      links: [DOMA-035]
naming_notes:
  collisions: [Attractor (Dynamical Systems Theory)]
  disambiguation: |
    In dynamical systems, an "attractor" is a set to which a system evolves over time. In Pirouette, an Attractor Map is a static representation of a potential field on the coherence manifold. The "attractors" are the massive concepts creating that field. The dynamics are not arbitrary but are specifically the geodesic paths across this curved manifold.
crosslinks:
  near_synonyms: [COHERENCE_MANIFOLD]
  antonyms: []
  prerequisites: [TEMPORAL_COHERENCE, PIROUETTE_LAGRANGIAN, GEODESIC]
  downstream_effects: [WEAVER]
license: CC-BY-SA-4.0
---

# Attractor Map

## Canonical (Pirouette)
A literal, graphical, or computational representation of a discourse's coherence manifold. The map plots core concepts as coherence wells whose depth and radius are functions of their Temporal Coherence (Kτ). The relationships between concepts (e.g., distance `r`, phase `Δφ`) define the manifold's local curvature, allowing the geodesic trajectory of any new or existing concept to be calculated and predicted.

## EFT-First Summary
An Attractor Map is a model of a discourse's "meaning space" that directly maps to the physics of a gravitational field. Concepts are treated as massive objects (where mass is their Temporal Coherence, Kτ) that create "potential wells" in the landscape of meaning. New information follows the path of least resistance (a geodesic) into these wells, making its trajectory predictable. This is based on the claim in DOMA-035 that the "gravity of meaning" is not an analogy for gravity, but an expression of the same universal law.

## Glossary Links
- See also: [Temporal Coherence](<link>), [Coherence Manifold](<link>), [Weaver](<link>)