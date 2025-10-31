---
term: "Fixed Point"
canonical_id: "FIXED_POINT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-020"]
---

---
term: Fixed Point
canonical_id: FIXED_POINT
symbol: g*
aliases: [RG Fixed Point, Scale-Invariant Point]
parents: [MATH-020]
children: [MATH-018]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-020
      lines: "B3"
      snippet: |
        B3 — Fixed Points & Phases
        • Solve β(g*)=0; compute stability matrix M_ij=∂β_i/∂g_j|_{g*}.
        • Identify UV/IR fixed points; relevant/irrelevant directions; map phases (free, confined‑like, gravitational‑limit).
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A silent hub in the wheel of scale, where the universe's rules cease their running. It is the destination and the origin, the eye of the storm in the flow between the infinitesimal and the infinite.
  law: |
    A fixed point g* is a set of couplings for which all beta functions vanish, β(g*)=0. The eigenvalues of the stability matrix M_ij = ∂β_i/∂g_j at g* determine its stability, classifying it as UV (repulsive), IR (attractive), or a saddle point.
  philosophy: |
    Fixed points reveal the fundamental, asymptotic nature of the theory. They define the universality classes and phases of the vacuum, exposing its character at extreme energy scales and providing the anchor points for understanding its emergent complexity.
pirouette_definition: |
  A fixed point, denoted g*, is a specific set of values for the theory's couplings, g ≡ {λ_Γ, c_K, …}, where the renormalization group (RG) flow halts. This condition is defined by the vanishing of all beta functions, β_i(g*) ≡ d g_i/d ln μ = 0 for all i. Fixed points characterize the scale-invariant behavior of the theory, typically at its ultraviolet (UV) or infrared (IR) limits, and are classified by the eigenvalues of the stability matrix M_ij = ∂β_i/∂g_j |_{g*}.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: g*
      meaning: Vector of coupling constants at the fixed point.
      dimensions: dimensionless
      default_range: contextual
    - name: β_i
      meaning: Beta function for the i-th coupling g_i.
      dimensions: dimensionless
      default_range: contextual
    - name: μ
      meaning: Renormalization group energy scale.
      dimensions: M L^2 T^-2 (Energy)
      default_range: contextual
    - name: M_ij
      meaning: Stability matrix element ∂β_i/∂g_j.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: RG Coarse-Graining Simulation
        outline: |
          1. Define the theory on a lattice Ω_L with spacing a.
          2. Perform a block-spin transform by a factor b>1 to coarse-grain the system.
          3. Compute the effective couplings of the coarse-grained theory via matching of n-point vertices, using Monte-Carlo or deterministic quadrature.
          4. From the change in couplings with scale, determine the beta functions β(g).
          5. Numerically solve the system of equations β(g)=0 to find the fixed point g*.
          6. Evaluate the stability matrix M_ij at g* and compute its eigenvalues to classify the fixed point.
        expected_signals: [A stable numerical solution g* where ||β(g*)|| is below solver tolerance (e.g., 1e-8), A set of real or complex eigenvalues of M_ij classifying the point's stability]
        pitfalls: [Lattice artifacts from finite size effects, Slow convergence or high variance in Monte-Carlo vertex estimators, Numerical solvers failing to find all physically relevant fixed points]
context_windows:
  - module: MATH-020
    excerpt: |
      B3 — Fixed Points & Phases
      • Solve β(g*)=0; compute stability matrix M_ij=∂β_i/∂g_j|_{g*}.
      • Identify UV/IR fixed points; relevant/irrelevant directions; map phases (free, confined‑like, gravitational‑limit).
  - module: MATH-020
    excerpt: |
      ...running a coarse‑graining renormalization group (RG) flow on (Γ,K) to expose UV/IR structure, confinement‑like behavior, and gravity‑limit phenomenology.
formal_mappings:
  candidates:
    - target: Fixed Point (Renormalization Group)
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        β(g*) = d g / d(ln μ) |_(g=g*) = 0
      justification: |
        The Pirouette definition directly implements the standard definition of a fixed point in the Wilsonian Renormalization Group formalism. It is a point in the abstract space of couplings that is invariant under a change of energy scale μ, signifying scale-invariance. The stability analysis via the Jacobian matrix is also standard.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter 12
          date: 1995-10-11
      confidence: 0.98
  adopted:
    - target: Fixed Point (Renormalization Group)
      rationale: The procedure in MATH-020 is a direct numerical implementation of the Wilsonian RG concept from QFT. The terminology, symbols, and goals are identical.
      confidence: 0.98
constraints_and_falsifiers:
  claims:
    - statement: "The Pirouette theory possesses a non-trivial, interacting UV fixed point, rendering it asymptotically safe."
      domain: theory
      falsifier: "All numerical RG flows from the physically relevant parameter space either diverge or run to a trivial (Gaussian) fixed point in the UV limit, indicating the theory is not UV-complete."
      status: under-test
      links: [MATH-020]
naming_notes:
  collisions: [The symbol g* is used for complex conjugation in some mathematical contexts, but within RG theory it unambiguously denotes a fixed point.]
  disambiguation: |
    Distinguish from a fixed point of a dynamical system evolving in time. An RG fixed point is a fixed point in the abstract space of theories under a change of *scale* (energy), not time.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [BETA_FUNCTION, RENORMALIZATION_GROUP_FLOW]
  downstream_effects: [ASYMPTOTIC_SAFETY, CONFINEMENT, PHASE_DIAGRAM]
license: CC-BY-SA-4.0
---