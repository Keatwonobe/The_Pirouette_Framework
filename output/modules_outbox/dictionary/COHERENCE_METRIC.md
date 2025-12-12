---
term: "Coherence Metric"
canonical_id: "COHERENCE_METRIC"
symbol: "g_ij"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-005"]
---

---
term: Coherence Metric
canonical_id: COHERENCE_METRIC
symbol: g_ij
aliases: [Configuration Space Metric, Kinetic Metric]
parents: [MATH-005]
children: [MATH-006, MATH-007]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-005
      lines: "§2"
      snippet: |
        We define the metric tensor of the manifold directly from the kinetic energy term, K_tau, of the Pirouette Lagrangian. For a Lagrangian L_p = (1/2) * g_ij(phi) * d(phi)^i/dt * d(phi)^j/dt - V(phi), the metric g_ij is the matrix of coefficients of the velocity terms.
  editors: [Agent]
  review_log: []
triad:
  art: |
    The texture of reality's fabric, where the weave itself dictates the cost and effort of every possible change. It is the friction of becoming, made geometric.
  law: |
    The distance between two infinitesimally close system states φ and φ+dφ is given by ds² = g_ij(φ) dφ^i dφ^j, where g_ij is the Hessian of the kinetic energy term K_τ with respect to the state velocities (φ_dot).
  philosophy: |
    This metric transforms dynamics into geometry. It asserts that the 'laws of motion' are not externally imposed rules but are the intrinsic, shortest paths (geodesics) through a curved space of possibilities defined by the system's own inertia.
pirouette_definition: |
  The Coherence Metric, g_ij(φ), is a Riemannian metric tensor on the Coherence Manifold (the configuration space of Ki rhythms). It is defined as the matrix of coefficients of the quadratic velocity terms in the kinetic energy K_τ of the Pirouette Lagrangian, L_p. The metric establishes the geometry of the state space, defining distances and angles between possible configurations, such that the system's equations of motion are equivalent to the geodesic equation on this manifold.
operational_definition:
  units: Context-dependent. If φ is dimensionless, units are Action ⋅ Time, or [M L²].
  symbol_table:
    - name: g_ij(φ)
      meaning: The Coherence Metric tensor, a function of state φ.
      dimensions: Action ⋅ Time ([M L²])
      default_range: Positive-definite matrix
    - name: φ^i
      meaning: The i-th coordinate of the system state (a Ki rhythm).
      dimensions: Dimensionless
      default_range: Periodic, e.g., [0, 2π)
    - name: K_τ
      meaning: Kinetic energy term of the Pirouette Lagrangian.
      dimensions: Energy ([M L² T⁻²])
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: System Response Tomography
        outline: |
          1. Initialize the system in a stable state φ on the manifold.
          2. Apply a small, controlled impulse (a "kick") to induce a specific velocity dφ^i/dt in the state space.
          3. Measure the instantaneous change in kinetic energy ΔK_τ.
          4. The diagonal metric component g_ii is computed from the relation ΔK_τ = (1/2) g_ii (dφ^i/dt)².
          5. Use combined impulses along multiple directions to compute off-diagonal elements and map the full tensor g_ij at φ.
        expected_signals: [Quadratic energy response to velocity perturbations, Anisotropic response for non-diagonal metrics]
        pitfalls: [Signal-to-noise ratio for small impulses, Non-linear effects from large impulses, Difficulty in cleanly isolating state-space directions]
context_windows:
  - module: MATH-005
    excerpt: |
      We define the metric tensor of the manifold directly from the kinetic energy term, K_tau, of the Pirouette Lagrangian. The kinetic term represents the "cost" of moving between states. For a Lagrangian L_p = (1/2) * g_ij(phi) * d(phi)^i/dt * d(phi)^j/dt - V(phi), the metric g_ij is the matrix of coefficients of the velocity terms. It is the Hessian of K_tau, capturing the "inertia" of the system's resonance.
  - module: MATH-005
    excerpt: |
      The Coherence Manifold is the ultimate expression of this principle. Its metric defines what is possible, its curvature defines what is easy, and its geodesics define what is inevitable. The act of existence is an act of navigation, and every system is a perfect, unerring navigator of its own internal world.
poetic_connections:
  motifs: [the law is the landscape, cost of motion, fabric of possibility, intrinsic geometry]
  evocative_lines:
    - "What we perceive as 'force' is simply the curvature of this underlying reality."
    - "The act of existence is an act of navigation..."
  association_matrix:
    - [ "COHERENCE_MANIFOLD", 0.9 ]
    - [ "GEODESIC_EQUATION", 0.8 ]
    - [ "PIRQUETTE_LAGRANGIAN", 0.7 ]
    - [ "TEMPORAL_PRESSURE", 0.3 ]
formal_mappings:
  candidates:
    - target: Jacobi-Maupertuis Metric
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        ds² = 2(E - V(q)) T(q, dq)
      justification: |
        In classical mechanics, the Jacobi-Maupertuis principle re-formulates dynamics as geodesic motion. The Coherence Metric g_ij is directly analogous to the kinetic energy part of the Jacobi metric, but in Pirouette, the potential V(φ) is treated separately as a conformal factor warping spacetime rather than as part of the configuration space metric itself.
      references:
        - title: Mathematical Methods of Classical Mechanics
          where: V. I. Arnold, Springer (1989)
          date: 1989-01-01
      confidence: 0.9
  adopted:
    - target: G_ab(φ), the field-space metric in a non-linear sigma model.
      rationale: |
        This mapping is mathematically exact. Both g_ij and G_ab are functions of the configuration variables (rhythms/fields) and appear as the coefficient matrix of the kinetic term in the Lagrangian, L = (1/2) G_ab(φ) ∂_μ φ^a ∂^μ φ^b - V(φ). This structure defines a Riemannian geometry on the internal space of the fields, where curvature corresponds to interactions, perfectly mirroring the role of g_ij in the Pirouette Framework.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The observed trajectory of any system governed by a Pirouette Lagrangian is a geodesic of the Coherence Manifold defined by the metric g_ij derived from that Lagrangian's kinetic term."
      domain: theory
      falsifier: "Discovering a physical system described by a Pirouette Lagrangian whose observed evolution systematically deviates from the calculated geodesic path for the corresponding g_ij. This would demonstrate that the Euler-Lagrange equations are not equivalent to the geodesic equations for this system, falsifying the Geodesic Equivalence Theorem."
      status: proposed
      links: [MATH-005]
naming_notes:
  collisions: [g_μν (spacetime metric in General Relativity)]
  disambiguation: |
    The Coherence Metric g_ij should not be confused with the spacetime metric g_μν. The indices i, j of g_ij run over the dimensions of the system's internal configuration space (the Coherence Manifold), while the indices μ, ν of g_μν run over the 3+1 dimensions of external spacetime.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PIRQUETTE_LAGRANGIAN, COHERENCE_MANIFOLD]
  downstream_effects: [GEODESIC_EQUATION, CURVATURE_TENSOR]
license: CC-BY-SA-4.0
---