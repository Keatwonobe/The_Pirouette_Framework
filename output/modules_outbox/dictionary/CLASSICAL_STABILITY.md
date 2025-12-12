---
term: "Classical stability"
canonical_id: "CLASSICAL_STABILITY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-016"]
---

---
term: Classical Stability
canonical_id: CLASSICAL_STABILITY
symbol: dQ/dω < 0
aliases: [Perturbative stability, Q-ball stability, Vakhitov-Kolokolov criterion]
parents: [MATH-016]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-016
      lines: "Section 4"
      snippet: |
        Quadratic action defines fluctuation operator (H). **Classical stability** if (H≥0) on the subspace orthogonal to zero modes (translations and global phase). Equivalent criterion:
        [ dQ/dω < 0  ⇒  no negative modes (stable). ]
  editors: [Pirouette AI Assistant]
  review_log: []
triad:
  art: |
    A knot of coherence, once tied, must not unravel when gently tugged. It holds its form not by rigid force but by a dynamic balance, a dance of phase and pressure that sheds excess energy rather than shattering.
  law: |
    A non-topological soliton solution is classically stable if and only if its Noether charge `Q` is a monotonically decreasing function of its internal frequency `ω` (i.e., `dQ/dω < 0`). This condition ensures the absence of negative energy modes in the spectrum of small fluctuations around the solution.
  philosophy: |
    Classical stability delineates true objects from ephemeral configurations. It is the minimal condition for a localized energy solution to persist long enough to be considered a particle-like entity, ensuring that small agitations decay or radiate away rather than triggering catastrophic collapse.
pirouette_definition: |
  Classical stability is the property of a time-dependent, localized field solution (a soliton) whereby small, finite-energy perturbations to the solution do not grow exponentially in time. For solutions of the Q-ball type, characterized by a Noether charge `Q` and an internal frequency `ω`, this property is met when the spectrum of the quadratic fluctuation operator `H` is non-negative. Operationally, this is equivalent to the Vakhitov-Kolokolov criterion, `dQ/dω < 0`.
operational_definition:
  units: The criterion `dQ/dω < 0` is a condition on the sign of a quantity, so the condition itself is dimensionless. The quantity `dQ/dω` has dimensions of Time.
  symbol_table:
    - name: Q
      meaning: Conserved Noether charge associated with the U(1) symmetry of the complex field C.
      dimensions: dimensionless
      default_range: "> 0"
    - name: ω
      meaning: Internal phase frequency of the soliton, `C(t,x) = exp(iωt)φ(x)`.
      dimensions: T⁻¹
      default_range: (0, m_C)
    - name: H
      meaning: Operator governing the dynamics of small perturbations around the soliton solution.
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
  measurement:
    procedures:
      - name: Stability Branch Analysis
        outline: |
          1. For a given potential `V(|C|², Γ)`, numerically solve the Euler-Lagrange equations to find a family of soliton solutions parameterized by the frequency `ω`.
          2. For each solution `(φ_ω, Γ_ω)`, calculate the corresponding Noether charge `Q(ω) = ∫ d³x 2ω|φ_ω|²`.
          3. Plot `Q` as a function of `ω`.
          4. Identify the branch(es) of the curve where the slope `dQ/dω` is negative. Solutions on these branches are classically stable.
        expected_signals: [A Q(ω) curve containing at least one region with a negative slope. The curve often exhibits a turning point where stability begins or ends.]
        pitfalls: [Numerical errors near turning points (`dQ/dω ≈ 0`), failure to find all solution branches, misinterpreting branches that are unstable to other decay channels.]
context_windows:
  - module: MATH-016
    excerpt: |
      Perturb around the Q-ball: (C=e^{iω t}[\phi(r)+\eta_1(t,\mathbf x)+i\eta_2(t,\mathbf x)],;\Gamma=\Gamma_\omega(r)+\xi(t,\mathbf x).)
      Quadratic action defines fluctuation operator (\mathcal H). **Classical stability** if (\mathcal H\ge0) on the subspace orthogonal to zero modes (translations and global phase). Equivalent criterion:
      [ \frac{dQ}{d\omega} < 0 \quad \Rightarrow \quad \text{no negative modes (stable).} ]
      Include (\Gamma) mixing; the condition persists provided the mixed mass matrix is positive in the vacuum and (U_\omega) stays coercive.
poetic_connections:
  motifs: [resilience, coherence, dynamic equilibrium, backreaction]
  evocative_lines:
    - "solitons are local knots of coherence stabilized by temporal-pressure backreaction."
    - "no negative modes (stable)."
  association_matrix:
    - [ "SOLITON", 1.0 ]
    - [ "NOETHER_CHARGE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Vakhitov-Kolokolov stability criterion
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        dQ/dω < 0
      justification: |
        This is the direct mathematical equivalent, derived for solutions to nonlinear wave equations like the nonlinear Schrödinger equation. It provides a powerful, integrated condition for stability that bypasses the need to solve the full spectral problem for the perturbation operator. Pirouette's use is a direct application of this theorem to scalar field theories.
      references:
        - title: Stationary solutions of the wave equation in a medium with nonlinearity of saturation
          where: Radiophys. Quantum Electron. 16, 343–350
          date: 1973-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "For a soliton family parameterized by ω, any solution on a branch where dQ/dω < 0 is stable against small, linear perturbations."
      domain: theory
      falsifier: "The discovery of a potential V(|C|²,Γ) that yields a soliton branch with dQ/dω < 0, but for which a direct spectral analysis of the fluctuation operator reveals a negative eigenvalue, indicating an unstable mode."
      status: supported
      links: [MATH-016]
naming_notes:
  collisions: [The symbol `H` is used for the fluctuation operator, which can be confused with the Hamiltonian.]
  disambiguation: |
    Distinguish from *thermodynamic stability* (related to free energy minima in a thermal bath) and *topological stability* (protection by a discrete, conserved topological charge). Classical stability concerns only the linear response to small perturbations for a non-topological solution and does not guarantee stability against large fluctuations or quantum tunneling.
crosslinks:
  near_synonyms: [VAKHITOV_KOLOKOLOV_CRITERION]
  antonyms: [CLASSICAL_INSTABILITY]
  prerequisites: [SOLITON, NOETHER_CHARGE]
  downstream_effects: [SOLITON_LIFETIME, COHERENCE_RADIUS]
license: CC-BY-SA-4.0
---

# Classical Stability

## Canonical (Pirouette)
Classical stability is the property of a time-dependent, localized field solution (a soliton) whereby small, finite-energy perturbations to the solution do not grow exponentially in time. For solutions of the Q-ball type, characterized by a Noether charge `Q` and an internal frequency `ω`, this property is met when the spectrum of the quadratic fluctuation operator `H` is non-negative. Operationally, this is equivalent to the Vakhitov-Kolokolov criterion, `dQ/dω < 0`.

## EFT-First Summary
In effective field theories admitting non-topological solitons like Q-balls, classical stability is the primary condition for a solution to be physically meaningful. It is mathematically identical to the Vakhitov-Kolokolov criterion, which states that a solution is stable if its charge `Q` decreases as its internal frequency `ω` increases. This criterion is a powerful computational tool, allowing stability to be assessed by tracking an integrated quantity (`Q`) across a family of solutions, rather than by solving a complex spectral problem for perturbation modes.

## Glossary Links
- See also: Soliton, Noether Charge, Perturbative Spectrum