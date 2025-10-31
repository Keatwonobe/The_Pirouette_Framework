---
term: "Geodesic Deviation"
canonical_id: "GEODESIC_DEVIATION"
symbol: "δG"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-130"]
---

---
term: Geodesic Deviation
canonical_id: GEODESIC_DEVIATION
symbol: δG
aliases: []
parents: [DOMA-130]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-130
      snippet: |
        Geodesic Deviation (δG): The primary metric for influence. It is the quantitative difference between a system's observed trajectory and the calculated "null geodesic" it would have followed in an unperturbed coherence manifold.
  editors: [system_agent]
  review_log: []
triad:
  art: |
    A measure of a path bent by memory. It is the shadow cast by an alternate history—the one that would have been, had the past not been a landscape with its own gravity.
  law: |
    Geodesic Deviation (δG) is the integrated path difference between an entity's observed worldline and its calculated null geodesic in an unperturbed coherence manifold; it is the definitive measure of the total influence exerted by one or more Wound Channels upon that entity.
  philosophy: |
    δG makes influence a measurable, geometric quantity, not a statistical abstraction. It quantifies the 'weight of history,' demonstrating that causality is not an external force but the shape of the terrain upon which the present must travel. It is the physical proof that no action is isolated.
pirouette_definition: |
  The primary metric of influence, defined as the quantitative difference between an entity's actual trajectory (worldline) and its theoretical unperturbed path (the null geodesic). This deviation is caused by the geometric curvature of the local coherence manifold, which is sculpted by the Temporal Pressure (V_Γ) of one or more Wound Channels. δG is the direct, integrated measure of the total causal influence a historical echo exerts over a given interval.
operational_definition:
  units: meters (m)
  symbol_table:
    - name: δG
      meaning: Total Geodesic Deviation over a path.
      dimensions: L
      default_range: "> 0"
    - name: x_actual(t)
      meaning: The observed trajectory of an entity as a function of time.
      dimensions: L
      default_range: contextual
    - name: x_null(t)
      meaning: The calculated unperturbed (null geodesic) trajectory of an entity.
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Trajectory Subtraction Analysis
        outline: |
          1. Isolate the entity under study and the source(s) of influence (the Wound Channels).
          2. Record the entity's actual trajectory `x_actual(t)` over a defined interval `[t₀, t₁]`.
          3. Model the local coherence manifold *without* the influence of the source Wound Channel(s) to establish the ambient background.
          4. Calculate the theoretical null geodesic `x_null(t)` the entity would have followed on this unperturbed manifold, given identical initial conditions at `t₀`.
          5. Compute δG as the time-integrated magnitude of the difference vector: `δG = ∫[t₀, t₁] |x_actual(t) - x_null(t)| dt`.
        expected_signals: [Anomalous acceleration, Deviation from predicted linear or periodic motion]
        pitfalls: [Inaccurate modeling of the unperturbed manifold, Failure to isolate all relevant Wound Channels, leading to confounding variables]
context_windows:
  - module: DOMA-130
    excerpt: |
      The "force" of influence is therefore revealed to be the gradient of this potential (`-∇V_Γ,channel`), which emerges when applying the Euler-Lagrange equation to `𝓛_p`. The entity, in obeying the universal Principle of Maximal Coherence, will alter its trajectory—its geodesic—to navigate this new, composite landscape.
  - module: DOMA-130
    excerpt: |
      Geodesic Deviation (δG): The primary metric for influence. It is the quantitative difference between a system's observed trajectory and the calculated "null geodesic" it would have followed in an unperturbed coherence manifold. `δG` is the direct, integrated measure of a Wound Channel's total influence over a given path.
poetic_connections:
  motifs: [bent_path, echo's_gravity, shadow_history, weight_of_the_past]
  evocative_lines:
    - "To change is to climb out of the very furrow one has just plowed..."
    - "History directs the present by shaping the path of least resistance."
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "INFLUENCE_QUANTIFICATION", 0.8 ]
    - [ "COHERENCE_MANIFOLD", 0.7 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.5 ]
formal_mappings:
  candidates:
    - target: Equation of Geodesic Deviation
      domain: GR
      mapping_kind: conceptual
      justification: |
        The term is a direct analogue to the concept in General Relativity, which measures the relative acceleration of nearby test particles due to spacetime curvature (tidal forces). In Pirouette, it measures the 'acceleration' of a single particle away from its unperturbed path due to the 'curvature' of the coherence manifold induced by a Wound Channel's Temporal Pressure.
      confidence: 0.9
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "The measured Geodesic Deviation (δG) of an entity is directly proportional to the integrated Temporal Pressure (V_Γ) of the influencing Wound Channel(s) along its path."
      domain: experiment
      falsifier: "Observation of a non-zero δG in a region with a demonstrably flat coherence manifold (V_Γ,channel = 0), or a δG that does not scale with the measured strength of V_Γ."
      status: proposed
      links: [DOMA-130]
naming_notes:
  collisions: [General Relativity]
  disambiguation: |
    While the name and mathematical spirit are borrowed from General Relativity, δG in Pirouette refers to the deviation of a *single* path from its hypothetical, unperturbed state, not the relative deviation between two nearby paths. The 'curvature' is in the coherence manifold (a landscape of memory), not spacetime itself.
crosslinks:
  near_synonyms: [INFLUENCE_QUANTIFICATION]
  antonyms: [NULL_GEODESIC]
  prerequisites: [WOUND_CHANNEL, PIRouette_LAGRANGIAN, COHERENCE_MANIFOLD]
  downstream_effects: [RESONANT_COUPLING, ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---