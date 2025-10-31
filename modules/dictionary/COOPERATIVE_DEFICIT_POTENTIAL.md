---
term: "Cooperative Deficit Potential"
canonical_id: "COOPERATIVE_DEFICIT_POTENTIAL"
symbol: "φ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SOCIO-FIELD-001"]
---

---
term: Cooperative Deficit Potential
canonical_id: COOPERATIVE_DEFICIT_POTENTIAL
symbol: φ
aliases: []
parents: [SOCIO-FIELD-001]
children: [SOCIO-FIELD-002, DOMA-096]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SOCIO-FIELD-001
      lines: "L43-L44"
      snippet: |
        * (φ): cooperative deficit potential (gradient field)
  editors: [AI-Assistant]
  review_log: []
triad:
  art: |
    A silent tension across the social landscape, a gravitational pull where aid has yet to flow. It is the shape of unreciprocated gifts and unmet needs, a map of social debt waiting to be balanced.
  law: |
    The Cooperative Deficit Potential (φ) is the scalar field whose gradient (∇φ) constitutes the curl-free (irrotational) component of the Social Dissonance Field (D). It is measured by applying Hodge decomposition to the residual flow (J_obs - J_opt) on a social graph, isolating the system's sources and sinks of cooperative exchange.
  philosophy: |
    By isolating imbalance from antagonism, φ provides a formal tool to diagnose and address failures of reciprocity without misinterpreting them as structural conflict. It transforms abstract concepts like inequality and social debt into a measurable potential field, allowing interventions to be targeted with geometric precision to restore coherent flow.
pirouette_definition: |
  The Cooperative Deficit Potential (φ) is the scalar potential field component of the Social Dissonance Field (D), isolated via Hodge decomposition of the residual flow (r = J_obs - J_opt). Its gradient (∇φ) represents the irrotational (curl-free) part of dissonance, quantifying sources and sinks of social exchange. High potential indicates a locus of unmet need or unreciprocated contribution (a "social creditor"), while low potential indicates a locus of unearned benefit (a "social debtor").
operational_definition:
  units: Context-dependent; typically dimensionless or units of [graph edge weight].
  symbol_table:
    - name: φ
      meaning: Cooperative Deficit Potential
      dimensions: Context-dependent
      default_range: Contextual; depends on normalization of the flow graph.
  measurement:
    procedures:
      - name: Hodge Decomposition of Residual Flow
        outline: |
          1. Construct a social graph with weighted edges representing observed flow (J_obs).
          2. Compute the ideal, coherence-optimal flow (J_opt) by minimizing entropy production or maximizing the system's Lagrangian.
          3. Calculate the residual flow field on the graph: r = J_obs - J_opt.
          4. Apply Hodge decomposition to r, typically by solving a Poisson equation on the graph Laplacian, to isolate the scalar potential φ such that ∇φ is the gradient component of r.
        expected_signals:
          - A scalar field (φ) mapped over the social graph's nodes.
          - "Hills" of high φ indicating net cooperative outflow (unmet need, unreciprocated aid).
          - "Valleys" of low φ indicating net cooperative inflow.
        pitfalls:
          - Mis-specification of the ideal flow (J_opt) leads to artifactual potentials.
          - High sensitivity to the choice of graph structure and edge weighting.
          - Numerical instability in the decomposition for sparse or poorly conditioned graphs.
context_windows:
  - module: SOCIO-FIELD-001
    excerpt: |
      The Social Dissonance Field (D) measures the difference between the real and idealized fluxes: D = ∇φ + ∇ × A, where (φ) captures unbalanced cooperative potential (gradient term), and (A) captures antagonistic or circulatory motion (curl term). The Hodge Decomposition of the residual flow is r = ∇φ + ∇ × A + h, where (φ) is the cooperative deficit potential (gradient field).
  - module: SOCIO-FIELD-001
    excerpt: |
      In interpretation, the Cooperative deficit (φ) serves as an observable proxy for unmet aid, unreciprocated exchange, or an inequality index. Its counterpart, Antagonistic circulation (A), manifests as protest loops or factional echo chambers. The magnitude and geometry of the dissonance field indicate where coherence flow is most obstructed.
poetic_connections:
  motifs: [social debt, imbalance, potential, gradient, thirst, reciprocity gap]
  evocative_lines:
    - "Aid placed near the coherence boundary restores alignment at minimal energetic cost."
    - "unmet aid, unreciprocated exchange, inequality index"
  association_matrix:
    - [ "Social Dissonance Field (D)", 0.9 ]
    - [ "Antagonistic Circulation (A)", 0.7 ]
    - [ "Coherence", 0.8 ]
formal_mappings:
  candidates:
    - target: Electrostatic Potential (V)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        E = -∇V  <==>  D_gradient = ∇φ
      justification: |
        The Hodge decomposition of a vector field is a direct generalization of the Helmholtz decomposition in electromagnetism. φ is mathematically analogous to the electrostatic potential V, where its gradient defines a conservative field component driven by sources and sinks ("social charges").
      references:
        - title: Introduction to Electrodynamics
          where: Griffiths, D.J., Chapter 2
          date: 2017-01-01
      confidence: 0.9
  adopted:
    - target: Electrostatic Potential (V)
      rationale: The mathematical structure is identical, providing a powerful and well-understood model for a potential field driven by localized sources (unmet need) and sinks (unreciprocated benefit) of social exchange.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The spatial variance of the φ field in a social system correlates strongly with established metrics of economic inequality, such as the Gini coefficient."
      domain: phenomenology
      falsifier: "A cross-societal study shows no significant correlation between var(φ) and the Gini coefficient, suggesting φ measures a different kind of imbalance."
      status: proposed
      links: [SOCIO-FIELD-001]
    - statement: "Social interventions (e.g., aid distribution) are maximally efficient at reducing total system dissonance |D| when applied to regions of high |∇φ|."
      domain: experiment
      falsifier: "A/B testing of intervention strategies shows that targeting high-curl regions (high |A|) or random nodes is equally or more effective at reducing total dissonance."
      status: proposed
      links: [SOCIO-FIELD-001]
naming_notes:
  collisions: [The symbol φ is widely used in physics for scalar fields (e.g., Higgs), wave functions, and phase angles.]
  disambiguation: |
    In the Pirouette Framework, φ is an *emergent* potential derived from residual social flows, not a fundamental field of the substrate. It is analogous to an electrostatic potential, quantifying imbalance, and should not be confused with a phase or a quantum field.
crosslinks:
  near_synonyms: [Social Potential, Reciprocity Imbalance]
  antonyms: [Antagonistic Circulation (A)]
  prerequisites: [Social Dissonance Field (D), Hodge Decomposition]
  downstream_effects: [Systemic Cascade, Coherence Halo]
license: CC-BY-SA-4.0
---