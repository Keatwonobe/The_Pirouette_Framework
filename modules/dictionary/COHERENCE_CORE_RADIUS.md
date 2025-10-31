---
term: "Coherence Core Radius"
canonical_id: "COHERENCE_CORE_RADIUS"
symbol: "r_c"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SOCIO-FIELD-001"]
---

---
term: Coherence Core Radius
canonical_id: COHERENCE_CORE_RADIUS
symbol: r_c
aliases: []
parents: [SOCIO-FIELD-001]
children: [SOCIO-FIELD-002, DOMA-096]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SOCIO-FIELD-001
      lines: "L§5"
      snippet: |
        ### Hypothesis:

        Social systems self-organize into coherence halos analogous to cosmological (\Gamma)-halos.

        ### Prediction:

        * (|\mathbf{D}| \sim r^{-1}) outside a coherence core radius (r_c)
        * ...

        ### Measurement:

        * Derive (r_c) by locating maximal (\nabla|\mathbf{D}|)
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A social body has a membrane, a living boundary where its internal order meets the external chaos. The Coherence Core Radius is this shoreline, the place of highest tension and greatest leverage. It is the skin of the social organism.
  law: |
    The Coherence Core Radius (r_c) is the radial distance from a system's social center of mass at which the spatial gradient of the Dissonance Field magnitude (∇|**D**|) is maximal. For r > r_c, dissonance magnitude is predicted to decay as a power law, |**D**| ~ r⁻¹.
  philosophy: |
    The Coherence Core Radius marks the natural boundary of a system's ability to self-stabilize through coherent information flow. It identifies the most energetically efficient location for interventions intended to restore systemic integrity, acting as a resonant surface for resource application. It is the boundary between "us" and the dissonant "other".
pirouette_definition: |
  The boundary of a self-organizing, stable social core, separating the inner region of high coherence from the outer "halo" region characterized by power-law dissonance decay. Operationally, it is defined as the locus of points where the gradient of the Social Dissonance Field magnitude, ∇|**D**|, is maximal. It represents a phase transition in the dominant mode of social interaction, from cooperative to antagonistic or circulatory.
operational_definition:
  units: Length (e.g., meters, graph distance/path cost)
  symbol_table:
    - name: r_c
      meaning: Coherence Core Radius
      dimensions: L
      default_range: contextual
    - name: D
      meaning: Social Dissonance Field
      dimensions: context-dependent (flow units / L)
      default_range: contextual
  measurement:
    procedures:
      - name: Dissonance Field Gradient Maximization
        outline: |
          1. Construct a weighted social graph with nodes embedded in a metric space (geographic or abstract).
          2. Compute the observed interaction flow (**J**_obs) and the coherence-optimal flow (**J**_opt) derived from the Pirouette Lagrangian.
          3. Calculate the residual flow **r** = **J**_obs - **J**_opt.
          4. Apply Hodge decomposition to **r** to isolate the Dissonance Field **D**.
          5. Compute the field magnitude |**D**| at all points in the embedding space.
          6. Calculate the gradient of the magnitude, ∇|**D**|.
          7. Identify the radius `r_c` corresponding to the maximum value of ∇|**D**|.
        expected_signals: [A sharp peak in ∇|**D**| at a specific radius, Power-law decay of |**D**| ~ r⁻¹ for r > r_c]
        pitfalls: [Noisy interaction data obscuring the gradient peak, Non-existence of a stable core (multi-polar or chaotic systems), Poor choice of spatial embedding distorting the geometry of **D**]
context_windows:
  - module: SOCIO-FIELD-001
    excerpt: |
      Social systems self-organize into coherence halos analogous to cosmological Γ-halos. The prediction is that |**D**| ~ r⁻¹ outside a coherence core radius (r_c). To test this, one must derive r_c by locating the maximal gradient ∇|**D**|. This radius marks the boundary of the stable core.
  - module: SOCIO-FIELD-001
    excerpt: |
      The Coherence Core Radius is critical for policy optimization. Interventions, such as aid or information campaigns, should be placed at r ≈ r_c to minimize coherence residue per unit resource. Aid placed near the coherence boundary is expected to restore alignment at minimal energetic cost, verifying a resonance-based efficiency model.
poetic_connections:
  motifs: [membrane, shoreline, event horizon, phase boundary, resonant shell]
  evocative_lines:
    - "crisis zones exhibit halo-like (r⁻¹) dissonance scaling."
    - "Aid placed near the coherence boundary restores alignment at minimal energetic cost."
  association_matrix:
    - [ "DISSONANCE_FIELD", 0.9 ]
    - [ "COHERENCE_HALO", 0.8 ]
    - [ "AID_OPTIMIZATION_TARGET", 0.7 ]
formal_mappings:
  candidates:
    - target: Shock front radius
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        ∇P → max
      justification: |
        A shock front in fluid dynamics is a boundary characterized by an extremely high gradient in physical properties like pressure and density. Similarly, r_c is defined by the maximum gradient of the Dissonance Field, marking a phase transition from a coherent (laminar-like) inner flow to a turbulent/dissonant outer halo.
      references:
        - title: Fluid Mechanics
          where: Chapter on Shock Waves
          date: 
      confidence: 0.6
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A stable Coherence Core Radius r_c, characterized by max(∇|**D**|) and an outer r⁻¹ decay of |**D**|, is a universal feature of self-organizing social systems."
      domain: phenomenology
      falsifier: "Empirical measurement of social dissonance fields fails to show a stable, well-defined radius where the gradient peaks, or the field does not follow a power-law decay in the halo region. The feature is either non-existent or highly variable and non-predictive."
      status: proposed
      links: [SOCIO-FIELD-001]
naming_notes:
  collisions: [The symbol r_c is commonly used for "critical radius" in various fields of physics (e.g., nucleation, stellar mechanics). Context is essential.]
  disambiguation: |
    Distinguish from a simple physical radius. The Coherence Core Radius is a geometric feature of an abstract social field (**D**) projected onto a spatial or network substrate. It is not necessarily a geographic or administrative boundary, though it may correlate with them.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [DISSONANCE_FIELD]
  downstream_effects: [CASCADE_THRESHOLD, AID_OPTIMIZATION_TARGET]
license: CC-BY-SA-4.0
---

# Coherence Core Radius

## Canonical (Pirouette)
The boundary of a self-organizing, stable social core, separating the inner region of high coherence from the outer "halo" region characterized by power-law dissonance decay. Operationally, it is defined as the locus of points where the gradient of the Social Dissonance Field magnitude, ∇|**D**|, is maximal. It represents a phase transition in the dominant mode of social interaction, from cooperative to antagonistic or circulatory.

## EFT-First Summary
Conceptually, the Coherence Core Radius `r_c` is analogous to the boundary of a shock front in fluid mechanics. Just as a shock is defined by a maximal pressure gradient, `r_c` is defined by the maximal gradient of the social dissonance field. This boundary marks the transition from a smooth, coherent "laminar" state within the core to a turbulent, dissonant state in the outer halo, providing a measurable geometric feature for analyzing social system stability and intervention points.

## Glossary Links
- See also: Dissonance Field