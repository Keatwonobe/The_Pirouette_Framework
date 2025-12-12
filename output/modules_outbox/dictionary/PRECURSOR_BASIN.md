---
term: "Precursor Basin"
canonical_id: "PRECURSOR_BASIN"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-177"]
---

---
term: Precursor Basin
canonical_id: PRECURSOR_BASIN
symbol: B(ψ_target)
aliases: [Watershed of Precursor States]
parents: [DOMA-177]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-177
      lines: "L70-L73"
      snippet: |
        The result is not a single point, but a **Precursor Basin**: a probability map of the high-energy, lower-coherence starting conditions that would naturally flow down to form the target.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    The mountain watershed from which the river of creation flows. It is the set of all possible rains that will eventually form the same sea.
  law: |
    The Precursor Basin for a target state `ψ_target` is the set of all initial states `ψ_precursor` whose time-evolved geodesic paths under the Pirouette Lagrangian terminate within the target's coherence well, with each initial state weighted by its probability density.
  philosophy: |
    Synthesis is not an act of force but of discovery. The Basin reveals what *wants* to be made, transforming creation from building a fortress to tending a garden whose seeds are already present in the soil.
pirouette_definition: |
  A region on the coherence manifold representing the probability distribution of higher-energy, lower-coherence precursor states that will naturally evolve into a specified target coherence well. It is identified by tracing the time-reversed geodesic (or anti-geodesic) upstream from the target state, effectively mapping the "watershed" of all viable starting conditions for a given synthesis.
operational_definition:
  units: Dimensionless probability density over the coherence manifold.
  symbol_table:
    - name: B(ψ_target)
      meaning: The probability density function defining the Precursor Basin for a target state `ψ_target`.
      dimensions: Dimensionless (Probability Density)
      default_range: Integral over any sub-region is in [0, 1].
  measurement:
    procedures:
      - name: Retrosynthetic Geodesic Trace
        outline: |
          1. Define the target state `ψ_target` by its `Ki` pattern and coherence well depth, fixing its location on the coherence manifold.
          2. Numerically integrate backward in time from a perturbed position out of the well, following paths of maximal coherence decrease (steepest ascent in Temporal Pressure, V_Γ).
          3. Sample a statistically significant number of these anti-geodesic paths, tracing them back to higher-pressure regions of the manifold.
          4. Aggregate the path origins into a probability density map, which constitutes the Precursor Basin. Peaks in the map indicate the most likely starting conditions.
        expected_signals: [A high-dimensional probability density function, often with a fractal or dendritic structure, peaking at the most probable precursor states.]
        pitfalls: [Computational expense due to the curse of dimensionality, numerical instability in regions of high Temporal Pressure, mischaracterization of the target well leading to an invalid trace.]
context_windows:
  - module: DOMA-177
    excerpt: |
      Starting from the target well, the Alchemist's Compass follows the "path of steepest ascent" back into the chaotic highlands of possibility. The result is not a single point, but a **Precursor Basin**: a probability map of the high-energy, lower-coherence starting conditions that would naturally flow down to form the target.
  - module: DOMA-177
    excerpt: |
      Retrosynthesis: The act of solving the inverse problem: given `ψ_target`, find the set of `ψ_precursor` states that naturally evolve into it. This is computationally equivalent to finding the "anti-geodesic" leading away from the target's attractor basin.
poetic_connections:
  motifs: [river, watershed, source, seed, blueprint, rain, highlands]
  evocative_lines:
    - "From which mountains does this river flow?"
    - "It shows us where the rain must fall."
  association_matrix:
    - [ "COHERENCE_WELL", 0.9 ]
    - [ "RETROSYNTHESIS", 0.8 ]
    - [ "GEODESIC", 0.7 ]
    - [ "COHERENCE_COST", 0.6 ]
formal_mappings:
  candidates:
    - target: Basin of Attraction
      domain: Math (Dynamical Systems)
      mapping_kind: conceptual
      equation_hint: |
        B(A) = {x ∈ X | φ(t, x) → A as t → ∞}
      justification: |
        In dynamical systems, a basin of attraction is the set of initial conditions whose trajectories approach a specific attractor. A Precursor Basin is the basin of attraction for a Coherence Well (the attractor), defined on the coherence manifold and governed by the dynamics of the Pirouette Lagrangian.
      references:
        - title: Nonlinear Dynamics and Chaos
          where: S. H. Strogatz, Section on Fixed Points and Stability
          date: 2014-01-01
      confidence: 0.9
  adopted:
    - target: Basin of Attraction
      rationale: The mapping is a direct conceptual analogy between a set of initial conditions leading to a stable state under a system's dynamics. Pirouette re-contextualizes this mathematical concept in a physical framework of coherence.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "For any stable coherence well, a non-empty, computable Precursor Basin exists from which it can be formed with a finite Coherence Cost."
      domain: theory
      falsifier: "The discovery of a stable state (`ψ_target` with Kτ > 0) for which no precursor states `ψ_precursor` can be found through retrosynthetic trace, implying it is a 'primordial' or un-creatable state."
      status: proposed
      links: [DOMA-177]
naming_notes:
  collisions: ["Basin of attraction" in dynamical systems, addressed in formal mappings.]
  disambiguation: |
    A Precursor Basin should not be mistaken for a specific list of chemical reactants. It is a continuous probability map over the entire state space of possible precursors, describing 'what could be' rather than 'what is'. It is the high-energy source region, distinct from the Coherence Well, which is the low-energy destination.
crosslinks:
  near_synonyms: []
  antonyms: [COHERENCE_WELL]
  prerequisites: [COHERENCE_MANIFOLD, COHERENCE_WELL, GEODESIC]
  downstream_effects: [ALCHEMICAL_UNION, COHERENCE_COST]
license: CC-BY-SA-4.0
---