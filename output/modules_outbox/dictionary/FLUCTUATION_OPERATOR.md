---
term: "Fluctuation operator"
canonical_id: "FLUCTUATION_OPERATOR"
symbol: "H"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-016"]
---

---
term: Fluctuation operator
canonical_id: FLUCTUATION_OPERATOR
symbol: H
aliases: [Stability operator]
parents: [MATH-016]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-016
      lines: "L40-L46"
      snippet: |
        Perturb around the Q-ball:
        (C=e^{i\omega t}[\phi(r)+\eta_1(t,\mathbf x)+i\eta_2(t,\mathbf x)],;\Gamma=\Gamma_\omega(r)+\xi(t,\mathbf x).)
        Quadratic action defines fluctuation operator (\mathcal H). **Classical stability** if (\mathcal H\ge0) on the subspace orthogonal to zero modes (translations and global phase).
  editors: [auto-agent-v0.2]
  review_log: []
triad:
  art: |
    The resonance of a bell struck softly; a stable form hums with positive energy, refusing to shatter, its every tremor a return to center.
  law: |
    For a soliton solution to be classically stable, the spectrum of its fluctuation operator (H) must be non-negative when acting on perturbations orthogonal to the soliton's zero modes. Any negative eigenvalue signifies an exponentially growing instability.
  philosophy: |
    The fluctuation operator is the system's internal critic, testing the integrity of a constructed coherence. It separates fleeting patterns from enduring structures by determining whether small disturbances are self-correcting or catastrophic, thus defining what is 'real' at the non-perturbative level.
pirouette_definition: |
  The Fluctuation operator, `H`, is the Hessian of the energy functional, evaluated at a soliton solution. It acts on the space of small, square-integrable perturbations to determine their linearized time evolution. Classical stability of the soliton requires that `H` be a non-negative operator, ensuring that the energy cost of any small deviation is non-negative and thus does not trigger a runaway decay.
operational_definition:
  units: Mass^2 (natural units, corresponding to squared frequency or mass)
  symbol_table:
    - name: H
      meaning: The fluctuation operator.
      dimensions: M^2 T^0 L^0 (in a system with c=ħ=1)
      default_range: Eigenvalues must be >= 0 for stability.
    - name: λ_i
      meaning: The i-th eigenvalue of H.
      dimensions: M^2 T^0 L^0
      default_range: contextual
    - name: δψ
      meaning: A field perturbation vector, e.g., (η₁, η₂, ξ).
      dimensions: M^1 T^0 L^0
      default_range: infinitesimal
  measurement:
    procedures:
      - name: Spectral Analysis of the Linearized System
        outline: |
          1. Numerically solve the Euler-Lagrange equations to find the soliton profile `(φ_ω, Γ_ω)`.
          2. Expand the Lagrangian to second order in perturbations `δψ` around this profile.
          3. Isolate the quadratic terms, which define the operator `H` via the equation of motion `∂_t² δψ = -H δψ`.
          4. Discretize the operator `H` on a spatial grid and solve the resulting matrix eigenvalue problem for its spectrum `{λ_i}`.
          5. Verify that all `λ_i ≥ 0` after projecting out the zero modes corresponding to continuous symmetries (e.g., translations, global phase).
        expected_signals:
          - A set of eigenvalues `{λ_i}`.
          - Eigenvalues at λ=0 corresponding to broken continuous symmetries (zero modes).
          - A positive spectral gap above the zero modes for a robustly stable soliton.
        pitfalls:
          - Numerical errors in the soliton profile can contaminate the spectrum.
          - Incorrectly identifying or projecting out zero modes can lead to false stability conclusions.
          - Insufficient grid resolution or range can miss shallow negative modes.
context_windows:
  - module: MATH-016
    excerpt: |
      Perturb around the Q-ball: (C=e^{i\omega t}[\phi(r)+\eta_1(t,\mathbf x)+i\eta_2(t,\mathbf x)],;\Gamma=\Gamma_\omega(r)+\xi(t,\mathbf x).)
      Quadratic action defines fluctuation operator (\mathcal H). **Classical stability** if (\mathcal H\ge0) on the subspace orthogonal to zero modes (translations and global phase). Equivalent criterion: `dQ/d\omega < 0` => no negative modes (stable).
  - module: MATH-016
    excerpt: |
      What to Prove (checklist)
      1. Existence via concentration–compactness for the chosen (V).
      2. Monotonic branch with (dQ/d\omega<0).
      3. Spectral gap of (\mathcal H) (no negative modes).
      4. Robustness to small curvature and weak portal couplings.
poetic_connections:
  motifs: [stability, resonance, integrity, spectral-test, self-correction]
  evocative_lines:
    - "solitons are **local knots of coherence** stabilized by temporal-pressure backreaction."
    - "**Classical stability** if (\mathcal H\ge0) on the subspace orthogonal to zero modes."
  association_matrix:
    - [ "SOLITON", 0.9 ]
    - [ "ZERO_MODE", 0.8 ]
    - [ "CLASSICAL_STABILITY", 1.0 ]
formal_mappings:
  candidates:
    - target: Hessian matrix / Mass-squared matrix
      domain: QFT|CM
      mapping_kind: mathematical
      equation_hint: |
        E[ψ₀+δψ] ≈ E[ψ₀] + ½ ∫ δψ H δψ d³x + ...
      justification: |
        The fluctuation operator is derived from the second variation of the energy functional with respect to field perturbations. This is mathematically identical to the Hessian of a multi-variable potential, which determines the stability of a critical point. Its eigenvalues correspond to the squared masses of the fluctuation modes.
      references:
        - title: "Solitons and Instantons"
          where: "R. Rajaraman, North-Holland, 1982, Chapter 4"
          date: 1982-01-01
      confidence: 0.95
  adopted:
    - target: Mass-squared matrix for perturbations
      rationale: This is the standard interpretation in field theory, directly linking the operator's spectrum to the physical properties (masses, instabilities) of the soliton's vibrational modes.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "A soliton solution is classically stable if and only if the spectrum of its fluctuation operator H is non-negative, after projecting out zero modes."
      domain: theory
      falsifier: "Discovering a physically stable, long-lived soliton in simulation whose corresponding fluctuation operator possesses a negative eigenvalue. This would imply that linear stability analysis is insufficient and that non-linear effects are essential for stability even against small perturbations."
      status: supported
      links: [MATH-016]
naming_notes:
  collisions: [H is conventionally used for the Hamiltonian.]
  disambiguation: |
    This operator `H` should not be confused with the full system Hamiltonian. The fluctuation operator is specifically the quadratic part of the Hamiltonian governing *small perturbations* around a specific classical solution, not the full energy operator of the theory.
crosslinks:
  near_synonyms: [STABILITY_OPERATOR]
  antonyms: []
  prerequisites: [SOLITON, CLASSICAL_STABILITY]
  downstream_effects: [SOLITON_LIFETIME, SCATTERING_CROSS_SECTION]
license: CC-BY-SA-4.0
---

# Fluctuation operator

## Canonical (Pirouette)
The Fluctuation operator, `H`, is the Hessian of the energy functional, evaluated at a soliton solution. It acts on the space of small, square-integrable perturbations to determine their linearized time evolution. Classical stability of the soliton requires that `H` be a non-negative operator, ensuring that the energy cost of any small deviation is non-negative and thus does not trigger a runaway decay.

## EFT-First Summary
In effective field theory, the fluctuation operator is the mass-squared matrix for field perturbations around a background classical solution, such as a Q-ball or domain wall. Its spectrum reveals the physical masses of the vibrational modes of the soliton. A non-negative spectrum is required for the background to be a stable, local minimum of the energy; a negative eigenvalue (a 'tachyonic' mode) signals a classical instability that causes the solution to decay.

## Glossary Links
- See also: Soliton, Zero Mode, Classical Stability