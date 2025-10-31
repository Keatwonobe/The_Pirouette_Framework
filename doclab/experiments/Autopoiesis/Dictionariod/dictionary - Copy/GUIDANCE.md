---
term: "Guidance"
canonical_id: "GUIDANCE"
symbol: ""
aliases: [Environmental Influence]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-130"]
---

---
term: Guidance
canonical_id: GUIDANCE
symbol:
aliases: [Environmental Influence]
parents: [DOMA-130]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-130
      snippet: |
        Guidance (Environmental Influence): An entity's "choices" are profoundly constrained by the pre-existing landscape. It navigates a world filled with the Wound Channels of countless other events. These historical echoes—from physical laws to cultural norms—create valleys and ridges in the coherence manifold. An entity following the path of maximal coherence will naturally be guided along these pre-carved geodesics. History directs the present by shaping the path of least resistance.
  editors: [GPT-4 Weaver]
  review_log: []
triad:
  art: |
    A river finds its course in the valleys carved by ancient waters; so too does an entity follow the grooves left in reality by history.
  law: |
    The influence of a pre-existing Wound Channel on an entity is quantified by the Geodesic Deviation (δG) of the entity's path from the null geodesic it would have followed in an unperturbed manifold.
  philosophy: |
    Guidance reveals that 'choice' is not an unconstrained act, but a navigation of a landscape of pre-existing probabilities. It quantifies how history, culture, and physical law shape the present by defining the paths of least resistance.
pirouette_definition: |
  A primary mode of geometric influence wherein an entity's trajectory is constrained by the geometry of pre-existing Wound Channels. These channels alter the local coherence manifold by adding a potential term (`V_Γ,channel`) to the ambient Temporal Pressure. In obeying the Principle of Maximal Coherence, the entity follows a new geodesic—a path of least resistance—through this composite landscape, effectively being "guided" by the echoes of past events.
operational_definition:
  units: Dependent on the specific metric; the primary metric, Geodesic Deviation (δG), has units of length (meters).
  symbol_table:
    - name: δG
      meaning: Geodesic Deviation
      dimensions: L
      default_range: contextual
    - name: V_Γ,channel
      meaning: Temporal Pressure potential of a Wound Channel
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
  measurement:
    procedures:
      - name: Geodesic Deviation Measurement
        outline: |
          1. Empirically map the observed trajectory of an entity through a region containing a known Wound Channel.
          2. Calculate the theoretical "null geodesic" the entity would have followed in the absence of that channel's influence, based on its initial state and the ambient manifold geometry.
          3. Compute the integrated, point-wise spatial difference between the observed trajectory and the null geodesic. The resulting scalar value is the Geodesic Deviation, δG.
        expected_signals: [Non-zero δG correlated with channel properties, localized gradient in V_Γ]
        pitfalls: [Failure to isolate the influence of the target Wound Channel from background noise, inaccurate modeling of the null geodesic.]
context_windows:
  - module: DOMA-130
    excerpt: |
      **Guidance (Environmental Influence):** An entity's "choices" are profoundly constrained by the pre-existing landscape. It navigates a world filled with the Wound Channels of countless other events. These historical echoes—from physical laws to cultural norms—create valleys and ridges in the coherence manifold. An entity following the path of maximal coherence will naturally be guided along these pre-carved geodesics.
  - module: DOMA-130
    excerpt: |
      The "force" of influence is therefore revealed to be the gradient of this potential (`-∇V_Γ,channel`), which emerges when applying the Euler-Lagrange equation to `𝓛_p`. The entity, in obeying the universal Principle of Maximal Coherence, will alter its trajectory—its geodesic—to navigate this new, composite landscape.
poetic_connections:
  motifs: [path of least resistance, historical echoes, carved valleys, navigating a landscape, following grooves]
  evocative_lines:
    - "History directs the present by shaping the path of least resistance."
    - "every thread they lay upon this loom alters the pattern for all who follow."
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "GEODESIC", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "INERTIA", 0.5 ]
    - [ "RESONANCE", 0.5 ]
formal_mappings:
  candidates:
    - target: Motion in a conservative potential field
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        F_guidance = -∇V_Γ,channel
      justification: |
        The influence of a Wound Channel is modeled as an additive term to the Temporal Pressure potential, `V_Γ,channel`. The resulting 'force' of Guidance is the negative gradient of this potential, directly analogous to a conservative force in classical mechanics guiding an object along a path of least potential energy.
      references: []
      confidence: 0.5
  adopted:
    - target: Geodesic motion in a curved manifold
      domain: GR
      mapping_kind: conceptual
      justification: |
        In General Relativity, test masses follow geodesics determined by spacetime curvature. In Pirouette, entities follow geodesics in a coherence manifold whose geometry is "curved" by the presence of Wound Channels. The 'force' of Guidance is an inertial effect of navigating this pre-existing geometry, analogous to how gravity is an effect of spacetime geometry rather than a classical force.
      references:
        - title: Gravitation
          where: Misner, Thorne, & Wheeler, Part II & III
          date: 1973-09-15
      confidence: 0.7
constraints_and_falsifiers:
  claims:
    - statement: "The trajectory of an entity entering the vicinity of a strong, isolated Wound Channel will deviate from its null geodesic by a predictable amount `δG` that is proportional to the coherence density of the channel."
      domain: experiment
      falsifier: "Observation of an entity passing through a strong Wound Channel with no measurable Geodesic Deviation (`δG` ≈ 0), or a deviation that is uncorrelated with the channel's known properties."
      status: proposed
      links: [DOMA-130]
naming_notes:
  collisions: []
  disambiguation: |
    Guidance refers to the influence of pre-existing, *external* Wound Channels on an entity's path. This is distinct from Inertia, which is the *self-influence* an entity experiences from the Wound Channel it is actively creating in its own immediate past.
crosslinks:
  near_synonyms: [INFLUENCE]
  antonyms: []
  prerequisites: [WOUND_CHANNEL, GEODESIC, TEMPORAL_PRESSURE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [GEODESIC_DEVIATION, RESONANCE]
license: CC-BY-SA-4.0
---

# Guidance

## Canonical (Pirouette)
A primary mode of geometric influence wherein an entity's trajectory is constrained by the geometry of pre-existing Wound Channels. These channels alter the local coherence manifold by adding a potential term (`V_Γ,channel`) to the ambient Temporal Pressure. In obeying the Principle of Maximal Coherence, the entity follows a new geodesic—a path of least resistance—through this composite landscape, effectively being "guided" by the echoes of past events.

## EFT-First Summary
Guidance is conceptually equivalent to geodesic motion in General Relativity. Just as a planet follows a curved path in spacetime sculpted by the sun's mass, an entity in Pirouette follows a path of least resistance (a geodesic) through a 'coherence manifold' sculpted by the geometric 'mass' of past events, known as Wound Channels. The influence is not a classical force but an emergent property of navigating a pre-structured landscape.

## Glossary Links
- See also: [Wound Channel](WOUND_CHANNEL), [Geodesic](GEODESIC), [Inertia](INERTIA), [Temporal Pressure](TEMPORAL_PRESSURE)