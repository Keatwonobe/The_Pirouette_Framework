---
term: "Derrick’s Theorem"
canonical_id: "DERRICK_S_THEOREM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-016"]
---

---
term: Derrick’s Theorem
canonical_id: DERRICKS_THEOREM
symbol: (none)
aliases: []
parents: [MATH-016]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-016
      lines: "15-18"
      snippet: |
        In 3+1D, static finite-energy scalars are ruled out by Derrick for purely quadratic kinetics. Evasion routes...
  editors: [Pirouette-LLM-v3]
  review_log: []
triad:
  art: |
    A knot of energy, left to itself in open space, will unravel. To persist, it must either spin, be woven from tougher thread, or be pinned to an external frame.
  law: |
    In D spatial dimensions, a static, finite-energy scalar field configuration with standard kinetic energy (T) and potential energy (V) is unstable to scaling x → λx. The energy functional E(λ) = λ^(2-D)T + λ^(-D)V has no stable minimum at λ=1 for D>2, as ∂E/∂λ is non-zero, forcing the configuration to collapse or dissipate.
  philosophy: |
    The theorem establishes a fundamental "no-go" for simple, persistent objects, forcing complexity. Stability cannot be static; it must be earned through dynamics (rotation in field space), internal stiffness (higher-order kinetics), or external support (gauge fields). It separates trivial lumps from structured, stable solitons.
pirouette_definition: |
  A theorem proving that static, non-topological, finite-energy scalar field solutions with standard kinetic terms `(∂φ)²` are unstable in `D>2` spatial dimensions. The instability arises from a scaling argument: shrinking the field profile always lowers the potential energy faster than the gradient energy increases, leading to collapse (or dissipation if expanded). The theorem's primary role is to motivate evasion mechanisms that enable stable solitons, such as time-dependent phases (Q-balls) or higher-derivative terms.
operational_definition:
  units: Dimensionless (theorem)
  symbol_table:
    - name: T
      meaning: Total kinetic energy of the field configuration
      dimensions: M L^2 T^-2
      default_range: "> 0"
    - name: V
      meaning: Total potential energy of the field configuration
      dimensions: M L^2 T^-2
      default_range: "> 0"
    - name: D
      meaning: Number of spatial dimensions
      dimensions: dimensionless
      default_range: "1, 2, 3, ..."
    - name: λ
      meaning: Dimensionless scaling factor for spatial coordinates
      dimensions: dimensionless
      default_range: "> 0"
  measurement:
    procedures:
      - name: Scaling Stability Test
        outline: |
          For a proposed static scalar field solution `φ₀(x)` in `D` spatial dimensions, construct a scaled family of solutions `φ_λ(x) = φ₀(x/λ)`. Calculate the total energy `E(λ) = T[φ_λ] + V[φ_λ]`. The original solution `φ₀` is stable only if `dE/dλ` is zero and `d²E/dλ²` is positive at `λ=1`. Derrick's theorem proves this is impossible for `D>2` under standard assumptions.
        expected_signals:
          - The energy function `E(λ)` will be monotonic with respect to `λ` around `λ=1`, indicating no local minimum and thus no stability against scaling.
        pitfalls:
          - Incorrectly applying the theorem to theories with non-standard kinetic terms (e.g., Skyrme model), gauge fields, or topological charges, which are known evasion mechanisms.
          - Misidentifying the effective number of spatial dimensions.
context_windows:
  - module: MATH-016
    excerpt: |
      In 3+1D, static finite-energy scalars are ruled out by Derrick for purely quadratic kinetics. Evasion routes:

      1. **Time-dependent phase (Q-balls):** C(t,**x**) = e^(iωt)φ(r).
      2. **Skyrme-like stiffness:** add λ(∂_μΓ ∂^μΓ)² or |∂C|⁴ suppressed by a high scale.
      3. **Gauge support:** minimal coupling gives magnetic pressure.
      
      We use (1) as the baseline since it preserves renormalizability of the leading terms.
poetic_connections:
  motifs: [instability, scale invariance, dynamic equilibrium, collapse, evasion]
  evocative_lines:
    - "static finite-energy scalars are ruled out"
    - "a knot of energy ... will unravel"
  association_matrix:
    - [ "Q_BALL", 0.9 ]
    - [ "STABILITY", 0.8 ]
    - [ "SOLITON", 0.7 ]
formal_mappings:
  candidates:
    - target: Derrick's Theorem
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        E(λ) = λ^(2-D) T + λ^(-D) V
      justification: |
        The term is a direct import of the well-established theorem by G.H. Derrick concerning the non-existence of stable, static, localized scalar field solutions in more than two spatial dimensions. The Pirouette Framework usage is identical to the standard definition in quantum field theory and serves as a crucial constraint motivating more complex soliton models.
      references:
        - title: Comments on particle-like solutions to nonlinear wave equations
          where: J. Math. Phys. 5, 1252 (1964)
          date: 1964-09-01
      confidence: 1.0
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A static, localized scalar field solution with a canonical kinetic term `(∂φ)²` and a positive-definite potential `V(φ)≥0` cannot be stable in 3+1 dimensions."
      domain: theory
      falsifier: "The discovery of a stable, static, finite-energy scalar field configuration in a 3D simulation or analytical model that uses only a standard `(∂φ)²` kinetic term and no other stabilizing fields. This would require a flaw in the original proof."
      status: supported
      links: [MATH-016]
naming_notes:
  collisions: []
  disambiguation: |
    Derrick's theorem applies to non-topological solitons. Topologically protected solitons (e.g., magnetic monopoles, skyrmions) evade the theorem because their energy functional has different scaling properties or is constrained by a conserved topological charge, preventing the simple scaling argument from applying.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [SCALAR_FIELD_THEORY]
  downstream_effects: [Q_BALL, SOLITON_STABILITY]
license: CC-BY-SA-4.0
---

# Derrick’s Theorem

## Canonical (Pirouette)
A theorem proving that static, non-topological, finite-energy scalar field solutions with standard kinetic terms `(∂φ)²` are unstable in `D>2` spatial dimensions. The instability arises from a scaling argument: shrinking the field profile always lowers the potential energy faster than the gradient energy increases, leading to collapse (or dissipation if expanded). The theorem's primary role is to motivate evasion mechanisms that enable stable solitons, such as time-dependent phases (Q-balls) or higher-derivative terms.

## EFT-First Summary
Derrick's theorem is a foundational result in field theory stating that static, localized scalar field lumps ("solitons") are unstable in more than two spatial dimensions. A simple scaling argument shows they must either collapse or dissipate. This forces stable solitons to have additional features, such as an internal time-dependence (like Q-balls), higher-derivative kinetic terms (as in Skyrme models), or interactions with gauge fields, all of which modify the energy scaling to permit a stable minimum. The result is mathematically identical to the original formulation by G.H. Derrick (1964).

## Glossary Links
- See also: Q-Ball, Soliton, Stability