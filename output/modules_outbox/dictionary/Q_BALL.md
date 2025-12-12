---
term: "Q-ball"
canonical_id: "Q_BALL"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-016"]
---

---
term: Q-ball
canonical_id: Q_BALL
symbol: 
aliases: [non-topological soliton]
parents: [MATH-016]
children: [Q_STAR]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-016
      lines: "L2.1-L2.3"
      snippet: |
        Define charge (Q=\int d^3x,i(C^*\dot C-\dot C^*C)). At fixed (Q), minimize energy
        [ E_\omega[\phi,\Gamma]=\int d^3x,\Big[ |\nabla\phi|^2+\tfrac12|\nabla\Gamma|^2+U_\omega(\phi,\Gamma)\Big],\quad U_\omega\equiv V(\phi^2,\Gamma)-\omega^2\phi^2. ]
  editors: [System Agent (Pirouette-Dict-Gen)]
  review_log: []
triad:
  art: |
    A self-contained storm of phase, spinning fast enough in an internal space to pull itself into a stable, luminous pearl. It is a knot of coherence that refuses to dissipate, bound by its own conserved rhythm.
  law: |
    A localized, finite-energy configuration of a complex scalar field C is a stable Q-ball if and only if its conserved charge Q increases as its internal phase frequency ω decreases (dQ/dω < 0).
  philosophy: |
    Q-balls demonstrate that coherence alone, through a conserved charge and temporal oscillation, is sufficient to create persistent, particle-like structures. They are a primary model for how energy can self-organize into stable lumps without topological knots or external confinement, representing matter as a self-trapped wave.
pirouette_definition: |
  A Q-ball is a non-topological soliton: a localized, stable, finite-energy solution for a complex scalar field `C`. Its stability arises from the conservation of a Noether charge `Q` associated with a global U(1) symmetry. The field configuration `C(t,x) = e^(iωt)φ(x)` has a time-dependent phase `e^(iωt)` which evades Derrick's theorem, allowing a balance between the field's potential energy, which favors expansion, and a 'centrifugal' pressure from the phase rotation, which favors confinement. Stable solutions exist for frequencies `ω` within a specific window below the mass `m_C` of the `C` particle, and are characterized by the stability criterion `dQ/dω < 0`.
operational_definition:
  units: Charge `Q` is dimensionless. Energy `E` is in Joules (or natural units).
  symbol_table:
    - name: Q
      meaning: Conserved Noether charge (particle number)
      dimensions: dimensionless
      default_range: "> 0"
    - name: ω
      meaning: Internal phase frequency
      dimensions: T⁻¹
      default_range: (0, m_C)
    - name: C
      meaning: Complex scalar field
      dimensions: M¹ L⁻¹ (Energy in natural units)
      default_range: contextual
    - name: φ(r)
      meaning: Radial profile of the field magnitude
      dimensions: M¹ L⁻¹ (Energy in natural units)
      default_range: "[0, φ(0)]"
    - name: V(|C|², Γ)
      meaning: Potential energy density
      dimensions: M¹ L⁻¹ T⁻² (Energy Density)
      default_range: contextual
  measurement:
    procedures:
      - name: Stability Curve Analysis
        outline: |
          1. For a given potential V(|C|²), numerically solve the Euler-Lagrange equations for the radial profile φ(r) across a range of frequencies ω.
          2. For each solution, compute the total charge Q = 8πω ∫r²φ²dr and energy E.
          3. Plot Q as a function of ω.
          4. The branch of the curve where dQ/dω < 0 corresponds to the set of classically stable Q-ball solutions.
        expected_signals: [A Q(ω) curve that starts at Q=0, rises, and turns over, creating a stable branch.]
        pitfalls: [Numerical instability near the boundaries of the stability window. Failure to correctly identify the true vacuum state for coupled fields.]
context_windows:
  - module: MATH-016
    excerpt: |
      In 3+1D, static finite-energy scalars are ruled out by Derrick for purely quadratic kinetics. Evasion routes: 1. Time-dependent phase (Q-balls): C(t,x)=e^(iωt)φ(r). We use (1) as the baseline since it preserves renormalizability of the leading terms.
  - module: MATH-016
    excerpt: |
      Perturb around the Q-ball: C=e^(iωt)[φ(r)+η₁(t,x)+iη₂(t,x)]. Quadratic action defines fluctuation operator H. Classical stability if H≥0 on the subspace orthogonal to zero modes. Equivalent criterion: dQ/dω < 0 ⇒ no negative modes (stable).
poetic_connections:
  motifs: [coherence, self-confinement, phase-locking, standing-wave, charge-as-substance]
  evocative_lines:
    - "solitons are local knots of coherence stabilized by temporal-pressure backreaction."
    - "A Q-ball baseline, then extensions where Γ supplies pressure/stiffness."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "SOLITON", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Non-topological soliton (Q-ball)
      domain: EFT|Cosmology
      mapping_kind: mathematical
      equation_hint: |
        C(t,x) = e^(iωt)φ(r)
      justification: |
        The Pirouette 'Q-ball' is mathematically identical to the non-topological soliton of the same name in field theory, first described by Sidney Coleman. It represents a stable, localized configuration of a complex scalar field whose existence is guaranteed by a conserved U(1) charge. The Pirouette framework uses it as a foundational example of stability arising from temporal dynamics rather than topology.
      references:
        - title: "Q-balls"
          where: Nuclear Physics B, Vol. 262, Issue 2, pp. 263-283
          date: 1985-10-21
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "For a given potential V(|C|²), stable Q-balls can exist only if there is a frequency ω < m_C such that the quantity U(φ)/φ² has a minimum value below m_C²/2."
      domain: theory
      falsifier: "Discovering a potential V that supports stable Q-balls but for which V(|C|²)/|C|² ≥ m_C²/2 for all |C| > 0."
      status: supported
      links: [MATH-016]
naming_notes:
  collisions: [The symbol Q for charge is ubiquitous and can be confused with heat in thermodynamics or the quality factor of an oscillator.]
  disambiguation: |
    Distinguish from *topological* solitons (e.g., monopoles, skyrmions) which are stabilized by a topological charge (a winding number), not a conserved Noether charge. A Q-ball's stability is dynamic; if its charge were allowed to dissipate, the object would decay.
crosslinks:
  near_synonyms: [NON_TOPOLOGICAL_SOLITON]
  antonyms: [TOPOLOGICAL_SOLITON]
  prerequisites: [NOETHER_THEOREM, COMPLEX_SCALAR_FIELD, DERRICKS_THEOREM]
  downstream_effects: [Q_STAR, PRESSURON]
license: CC-BY-SA-4.0
---

# Q-ball

## Canonical (Pirouette)
A Q-ball is a non-topological soliton: a localized, stable, finite-energy solution for a complex scalar field `C`. Its stability arises from the conservation of a Noether charge `Q` associated with a global U(1) symmetry. The field configuration `C(t,x) = e^(iωt)φ(x)` has a time-dependent phase `e^(iωt)` which evades Derrick's theorem, allowing a balance between the field's potential energy, which favors expansion, and a 'centrifugal' pressure from the phase rotation, which favors confinement. Stable solutions exist for frequencies `ω` within a specific window below the mass `m_C` of the `C` particle, and are characterized by the stability criterion `dQ/dω < 0`.

## EFT-First Summary
In effective field theory and cosmology, the Q-ball is a standard example of a non-topological soliton. It is a coherent, solitonic state of a complex scalar field, whose stability is ensured by the conservation of a global U(1) charge (particle number). These objects can be formed in the early universe and may play a role in baryogenesis or as dark matter candidates. Their properties are determined by the scalar potential, and their classical stability is famously linked to the sign of the derivative of charge with respect to their internal frequency, `dQ/dω < 0`. (Ref: Coleman, S. "Q-balls". *Nuclear Physics B*, 1985).

## Glossary Links
- See also: [SOLITON](<./SOLITON.md>), [DERRICKS_THEOREM](<./DERRICKS_THEOREM.md>), [Q_STAR](<./Q_STAR.md>)