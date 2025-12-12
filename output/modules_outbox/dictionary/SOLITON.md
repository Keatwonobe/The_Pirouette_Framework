---
term: "Soliton"
canonical_id: "SOLITON"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-016"]
---

---
term: Soliton
canonical_id: SOLITON
symbol: 
aliases: [Q-ball, Local Knot of Coherence]
parents: [MATH-016]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-016
      lines: "Section 7"
      snippet: |
        Mapping to Pirouette: solitons are **local knots of coherence** stabilized by temporal-pressure backreaction.
  editors: [Aether AI]
  review_log: []
triad:
  art: |
    A persistent knot of energy, holding its form against the void. It is a wave that remembers itself, a self-trapped whisper of coherence stable against dispersion.
  law: |
    A localized, finite-energy field configuration is a stable soliton if and only if it is a non-trivial, time-independent solution to the classical equations of motion in its comoving frame, and evades scale-invariance decay arguments (Derrick's Theorem) via a stabilizing mechanism, such as an internal time-dependent phase or higher-order kinetic terms.
  philosophy: |
    Solitons represent the principle of emergent stability, where non-linear interactions conspire to create persistent, particle-like objects from a seemingly undifferentiated field continuum. They are the simplest models of self-contained structure arising from fundamental laws.
pirouette_definition: |
  A soliton is a localized, non-dispersive, finite-energy solution to the classical field equations, maintaining its shape and structure due to a balance between kinetic energy and non-linear potential energy. In Pirouette, solitons are considered **local knots of coherence**, often stabilized by an internal time-dependent phase (e.g., Q-balls) or inherent field stiffness, representing the most basic form of persistent, self-organized structure.
operational_definition:
  units: Energy (eV) or dimensionless (in natural units).
  symbol_table:
    - name: E
      meaning: Total energy of the soliton configuration.
      dimensions: M L^2 T^-2
      default_range: contextual
    - name: Q
      meaning: Conserved Noether charge.
      dimensions: dimensionless
      default_range: contextual
    - name: ω
      meaning: Internal oscillation frequency of the fields.
      dimensions: T^-1
      default_range: (0, m_C)
    - name: φ, Γ
      meaning: Radial profiles of the constituent scalar fields.
      dimensions: M L T^-2
      default_range: contextual
  measurement:
    procedures:
      - name: Numerical Profile Search
        outline: |
          1. Define a scalar field Lagrangian with a potential V(|C|², Γ) that supports Q-balls.
          2. For a chosen internal frequency ω, numerically solve the radial Euler-Lagrange equations for the field profiles φ(r) and Γ(r) using a shooting or relaxation method.
          3. Impose boundary conditions: φ'(0)=Γ'(0)=0 (regularity) and φ(∞)=0, Γ(∞)=Γ_vac (decay to vacuum).
          4. A non-trivial solution with finite integrated energy E and charge Q is a soliton candidate.
        expected_signals:
          - A localized, non-zero radial profile for the scalar field(s).
          - A stable branch of solutions where the stability criterion `dQ/dω < 0` is satisfied.
        pitfalls:
          - Numerical methods may fail to converge or may find unstable saddle-point solutions instead of true energy minima.
          - The chosen potential V might not have a "Q-ball window," yielding no non-trivial solutions.
context_windows:
  - module: MATH-016
    excerpt: |
      In 3+1D, static finite-energy scalars are ruled out by Derrick for purely quadratic kinetics. Evasion routes:
      1. **Time-dependent phase (Q-balls):** (C(t,\mathbf x)=e^{i\omega t},\phi(r)).
      2. **Skyrme-like stiffness:** add (\lambda(\partial_\mu\Gamma\partial^\mu\Gamma)^2) or (|\partial C|^4) suppressed by a high scale.
      3. **Gauge support:** minimal coupling gives magnetic pressure.
      We use (1) as the baseline since it preserves renormalizability of the leading terms.
  - module: MATH-016
    excerpt: |
      Perturb around the Q-ball: (C=e^{i\omega t}[\phi(r)+\eta_1(t,\mathbf x)+i\eta_2(t,\mathbf x)],;\Gamma=\Gamma_\omega(r)+\xi(t,\mathbf x).)
      Quadratic action defines fluctuation operator (\mathcal H). **Classical stability** if (\mathcal H\ge0) on the subspace orthogonal to zero modes (translations and global phase). Equivalent criterion:
      [ \frac{dQ}{d\omega} < 0 \quad \Rightarrow \quad \text{no negative modes (stable).} ]
poetic_connections:
  motifs: [self-trapping, coherence, persistence, emergent structure, balance]
  evocative_lines:
    - "solitons are local knots of coherence stabilized by temporal-pressure backreaction."
    - "A wave that remembers itself."
  association_matrix:
    - [ "Q-ball", 0.9 ]
    - [ "Coherence", 0.7 ]
    - [ "Emergent Structure", 0.6 ]
formal_mappings:
  candidates:
    - target: Q-ball
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        C(t, x) = e^(iωt)φ(|x|)
      justification: |
        The baseline model for a soliton in MATH-016 is explicitly a Q-ball, a non-topological soliton whose stability is guaranteed by a conserved Noether charge Q associated with a U(1) symmetry. The internal time-dependent phase `e^(iωt)` is the primary mechanism used to evade Derrick's theorem for scalar fields in 3+1 dimensions.
      references:
        - title: "Q-balls"
          where: "Nucl. Phys. B262 (1985) 263"
          date: 1985-01-01
      confidence: 0.95
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "A stable, non-topological soliton composed of fundamental scalar fields in 3+1D must either possess an internal time-dependent phase (like a Q-ball) or have non-standard kinetic terms (e.g., Skyrme-like)."
      domain: theory
      falsifier: "The discovery of a stable, static, finite-energy scalar field configuration with only a canonical kinetic term `|∂φ|^2` and a potential V(φ). This would violate Derrick's Theorem."
      status: supported
      links: [MATH-016]
naming_notes:
  collisions: [Topological Soliton (monopole, instanton), Optical Soliton]
  disambiguation: |
    In physics, "soliton" has many meanings. This entry refers specifically to non-topological, particle-like field configurations stabilized by conserved Noether charge (like Q-balls) or kinetic stiffness. It should be distinguished from *topological solitons* (e.g., domain walls, monopoles) which are stabilized by the topology of the vacuum manifold and have a conserved topological charge.
crosslinks:
  near_synonyms: []
  antonyms: [Dispersive Wave Packet]
  prerequisites: [CLASSICAL_FIELD_THEORY, NOETHER_THEOREM]
  downstream_effects: [GRAVITATIONAL_SOURCE, PARTICLE_PHENOMENOLOGY]
license: CC-BY-SA-4.0
---

# Soliton

## Canonical (Pirouette)
A soliton is a localized, non-dispersive, finite-energy solution to the classical field equations, maintaining its shape and structure due to a balance between kinetic energy and non-linear potential energy. In Pirouette, solitons are considered **local knots of coherence**, often stabilized by an internal time-dependent phase (e.g., Q-balls) or inherent field stiffness, representing the most basic form of persistent, self-organized structure.

## EFT-First Summary
A soliton is a particle-like, non-perturbative field configuration, such as a Q-ball, that appears in the classical limit of a field theory. It is a stable, finite-energy lump whose existence depends on specific properties of the scalar potential V(φ) and whose stability is often tied to a conserved Noether charge Q, satisfying the condition dQ/dω < 0. These objects can be treated as heavy, classical states in the low-energy effective theory and can have significant phenomenological implications.

## Glossary Links
- See also: Q-ball, Derrick's Theorem, Emergent Structure