---
term: "Tetrad"
canonical_id: "TETRAD"
symbol: "e^a_μ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-QED-002_spinor_ki_defects_as_dirac"]
---

---
term: Tetrad
canonical_id: TETRAD
symbol: e^a_μ
aliases: [Vierbein, Frame Field]
parents: [MATH-QED-002]
children: [MATH-QED-003, MATH-QED-004, DYNA-QED-005]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-QED-002_spinor_ki_defects_as_dirac
      snippet: |
        Let (e^a{}*\mu(x)) be a tetrad with (g*{\mu\nu}=e^a{}*\mu e^b{}*\nu \eta_{ab}).
        Introduce the spin connection (\omega_\mu^{ab}) and gamma matrices...
  editors: [Pirouette-Agent-v2.1]
  review_log: []
triad:
  art: |
    The tetrad is a local compass for spacetime. At every point, it provides a perfect North, South, East, and West, allowing a spinning particle to know its orientation even as the universe curves and warps around it.
  law: |
    At any spacetime point `x`, the tetrad `e^a_μ(x)` maps the curved spacetime metric `g_μν(x)` to the flat Minkowski metric `η_ab` via the relation `g_μν = e^a_μ e^b_ν η_ab`. Its inverse `e_a^μ` is required to define the spin connection and couple spinor fields to gravity.
  philosophy: |
    The tetrad embodies the equivalence principle for spinning particles. It asserts that while spacetime is globally curved, it is locally flat, allowing the laws of special relativity and quantum field theory to hold in any infinitesimal neighborhood. It is the fundamental interface between the geometric language of gravity and the algebraic language of quantum fields.
pirouette_definition: |
  A field of local orthonormal frames, `e^a_μ(x)`, defined at each point `x` of a spacetime manifold. The tetrad provides a bridge between the curved coordinate basis (indexed by `μ, ν, ...`) and a local, flat, non-coordinate Minkowski basis (indexed by `a, b, ...`), satisfying `g_μν = e^a_μ e^b_ν η_ab`. It is essential for defining the spin connection `ω_μ^ab`, which parallel transports spinors, and for coupling spinor fields (like the Ki-defect `Ψ`) to gravity.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: e^a_μ
      meaning: Tetrad field component; maps from local Lorentz frame to coordinate frame.
      dimensions: Dimensionless
      default_range: contextual
    - name: e_a^μ
      meaning: Inverse tetrad field component; maps from coordinate frame to local Lorentz frame.
      dimensions: Dimensionless
      default_range: contextual
    - name: g_μν
      meaning: Spacetime metric tensor
      dimensions: Dimensionless (geometric units)
      default_range: contextual
    - name: η_ab
      meaning: Minkowski metric tensor (diag(-1, 1, 1, 1) or (+1, -1, -1, -1))
      dimensions: Dimensionless
      default_range: fixed
  measurement:
    procedures:
      - name: Metric Decomposition
        outline: |
          The tetrad is not directly measured. It is a mathematical construct inferred from the spacetime metric `g_μν`. Given a measured `g_μν` from gravitational observations (e.g., lensing, orbital dynamics), a tetrad field can be constructed. This choice is non-unique and subject to a local Lorentz transformation gauge freedom.
        expected_signals: [Not directly applicable. Effects are seen in spinor dynamics, e.g., spin precession in a gravitational field.]
        pitfalls: [Gauge fixing is required for calculations; physical observables must be independent of the specific tetrad choice.]
context_windows:
  - module: MATH-QED-002_spinor_ki_defects_as_dirac
    excerpt: |
      Let (e^a{}*\mu(x)) be a tetrad with (g*{\mu\nu}=e^a{}*\mu e^b{}*\nu \eta_{ab}). Introduce the spin connection (\omega_\mu^{ab}) and gamma matrices ({\gamma^a,\gamma^b}=2\eta^{ab}). Define the covariant spinor derivative... Lorentz/CPT: guaranteed by tetrad+spin connection formalism on the Coherence-Preserving Manifold (CPM).
poetic_connections:
  motifs: [local compass, spacetime scaffolding, geometric soldering, equivalence principle]
  evocative_lines:
    - "The tetrad is the local stage on which a knot in time performs its two-turn dance."
  association_matrix:
    - [ "Spin Connection", 0.9 ]
    - [ "Metric Tensor", 0.8 ]
    - [ "Spinor", 0.7 ]
    - [ "Lorentz Symmetry", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Vierbein / Frame Field
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        g_{μν}(x) = e^a_μ(x) e^b_ν(x) η_{ab}
      justification: |
        The term "Tetrad" and its German equivalent "Vierbein" are used interchangeably in the physics literature. The mathematical role and defining equation are identical to the standard formalism used in general relativity to couple fermions to gravity.
      references:
        - title: Gravitation
          where: C. Misner, K. Thorne, J. Wheeler, Part IX
          date: 1973-09-15
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "A local Lorentz-invariant frame field (tetrad) is necessary to consistently couple spin-½ fields to a general spacetime metric."
      domain: theory
      falsifier: "A consistent, empirically verified theory of quantum gravity that couples spinors to gravity without using a local frame field or an equivalent structure."
      status: proposed
      links: [MATH-QED-002]
naming_notes:
  collisions: ["Tetrad" is used in genetics for a group of four chromatids.]
  disambiguation: |
    In the Pirouette Framework, "Tetrad" always refers to the frame field `e^a_μ` from general relativity. It provides the mathematical structure required to define spinors and the spin connection in a curved spacetime, effectively translating between the curved "world" coordinates and a flat "lab" frame that exists at every point.
crosslinks:
  near_synonyms: [VIERBEIN]
  antonyms: []
  prerequisites: [METRIC_TENSOR, LORENTZ_SYMMETRY]
  downstream_effects: [SPIN_CONNECTION, DIRAC_EQUATION, SPINOR_HOLONOMY]
license: CC-BY-SA-4.0
---

# Tetrad

## Canonical (Pirouette)
A field of local orthonormal frames, `e^a_μ(x)`, defined at each point `x` of a spacetime manifold. The tetrad provides a bridge between the curved coordinate basis (indexed by `μ, ν, ...`) and a local, flat, non-coordinate Minkowski basis (indexed by `a, b, ...`), satisfying `g_μν = e^a_μ e^b_ν η_ab`. It is essential for defining the spin connection `ω_μ^ab`, which parallel transports spinors, and for coupling spinor fields (like the Ki-defect `Ψ`) to gravity.

## EFT-First Summary
In standard general relativity (GR) and effective field theory (EFT), the tetrad `e^a_μ` (or "vierbein") is an essential tool. It provides a local orthonormal (Minkowskian) frame at each point in a curved spacetime, allowing for a consistent definition of spinor fields and their coupling to gravity. The defining relation is `g_μν = e^a_μ e^b_ν η_ab`, making it the "scaffolding" needed to write the Dirac equation in a curved background (Ref: Misner, Thorne, & Wheeler, *Gravitation*).

## Glossary Links
- See also: Spin Connection, Ki Loop, Metric Tensor