---
term: "Quantum Pressure"
canonical_id: "QUANTUM_PRESSURE"
symbol: "Q"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-006"]
---

---
term: Quantum Pressure
canonical_id: QUANTUM_PRESSURE
symbol: Q
aliases: [Bohm Potential]
parents: [COSMO-006, MATH-020]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-006
      lines: "SECT-Γ-A-HALO, Eq. 1"
      snippet: |
        Euler (with quantum pressure Q and surface tension σ):
        ∂*t v + (v·∇)v = −∇h(n) − ∇Φ + ∇Q/m_H + ...
        where Q= −(κ/2) ∇²√n/√n ...
  editors: [Pirouette-Agent-v2.1]
  review_log: []
triad:
  art: |
    A quantum stiffness resisting the crush of gravity, where a fluid's own curvature pushes back. It is the breath of uncertainty that holds a star-less galaxy's core open against collapse.
  law: |
    The quantum pressure `Q` is a scalar potential proportional to the Laplacian of the density amplitude (`√n`), generating a force `−∇Q` that acts to smooth sharp density gradients and prevent divergences at a characteristic "healing length" scale.
  philosophy: |
    Quantum Pressure introduces a fundamental length scale into the dark matter fluid, resolving the cusp-core problem of CDM halos by preventing gravitational singularity. It embodies the principle that the wavelike nature of constituent particles becomes dynamically significant on astrophysical scales.
pirouette_definition: |
  A scalar potential, `Q = −(κ/2) ∇²√n/√n`, that contributes a force term `∇Q/m_H` to the Euler fluid dynamics equation. This force opposes the formation of sharp density gradients, effectively acting as a pressure to regularize solutions and establish a minimum length scale (the healing length, `ξ`) below which density cannot vary sharply. It is parameterized by the coefficient `kappa_quantum` (`κ`).
operational_definition:
  units: Joules (J) or MeV
  symbol_table:
    - name: Q
      meaning: Quantum pressure potential
      dimensions: M L^2 T^-2
      default_range: contextual
    - name: κ
      meaning: Quantum pressure coefficient, `kappa_quantum`
      dimensions: M L^4 T^-2
      default_range: contextual; corresponds to ħ²
    - name: n
      meaning: Number density of the fluid
      dimensions: L^-3
      default_range: contextual
    - name: m_H
      meaning: Mass of the constituent fluid particle
      dimensions: M
      default_range: 1e-22 eV to 100 MeV
  measurement:
    procedures:
      - name: Halo Core Profile Inversion
        outline: |
          Measure the central density profile `ρ(r)` of a dark matter-dominated galaxy (e.g., dwarf spheroidal) via stellar kinematics or lensing. Fit the profile using the stationary superfluid Euler equation, where the gravitational force is balanced by forces from `P(X)` and `Q`. The value of `kappa_quantum` is inferred from the measured core radius `r_c`, which is set by the balance between gravity and quantum pressure.
        expected_signals: [A cored (non-cuspy) central density profile, A specific relation between core radius `r_c` and central density `ρ_0`]
        pitfalls: [Degeneracy with baryonic feedback effects which can also form cores, Observational uncertainties in tracing the central mass distribution]
context_windows:
  - module: COSMO-006
    excerpt: |
      Euler (with quantum pressure Q and surface tension σ):
      ∂*t v + (v·∇)v = −∇h(n) − ∇Φ + ∇Q/m_H + (σ/ρ) κ_s  n̂*⊥  (interface curvature term)
      where Q= −(κ/2) ∇²√n/√n and κ_s is mean curvature of iso‑n surfaces.
  - module: COSMO-006
    excerpt: |
      Stationary Halos (Core Profiles)
      Spherical equilibrium: ∇p = −ρ ∇Φ with p=P(X(n)).
      Numerics: 1D shooting/spectral or FEM with regularization by Q and σ; residual <1e‑10.
poetic_connections:
  motifs: [Wave mechanics, Repulsive force, Zero-point energy, Cosmic architecture, Fluid stiffness]
  evocative_lines:
    - "regularization by Q and σ"
    - "healing‑length physics"
  association_matrix:
    - [ "HALO_CORE_RADIUS", 0.9 ]
    - [ "HEALING_LENGTH", 0.8 ]
    - [ "SURFACE_TENSION", 0.5 ]
formal_mappings:
  candidates:
    - target: Bohm Potential / Quantum Potential
      domain: Quantum Mechanics
      mapping_kind: mathematical
      equation_hint: |
        Q = - (ħ² / 2m) (∇²R / R), where Ψ = R exp(iS/ħ)
      justification: |
        The term is mathematically identical to the Bohm potential, which arises in the hydrodynamical (Madelung) formulation of the Schrödinger equation. In the context of BEC/Fuzzy Dark Matter, this term represents the internal kinetic energy due to the wave nature of the particles, often called a "quantum stress tensor". The module's `κ` corresponds to `ħ²`.
      references:
        - title: "Ultralight scalars as cosmological dark matter"
          where: "Phys. Rev. D 95, 043541"
          date: 2017-02-28
      confidence: 0.95
  adopted:
    - target: Bohm Potential
      rationale: The mathematical form, physical interpretation (a pressure-like effect from wave mechanics), and application context (BEC-like dark matter) are identical. This connects the Pirouette framework directly to the standard literature on Fuzzy Dark Matter.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Quantum pressure is the primary mechanism setting the core size in ultra-faint dwarf galaxies, following a predictable relation between core radius and halo mass."
      domain: phenomenology
      falsifier: "Observation of cored dwarf galaxies whose core properties are inconsistent with the Q-pressure relation for a single particle mass `m_H`, or strong evidence that baryonic feedback is the dominant core-formation mechanism in these systems."
      status: under-test
      links: [COSMO-006]
naming_notes:
  collisions: [The symbol `Q` is common for heat (thermodynamics), charge (electromagnetism), and quality factor (oscillators).]
  disambiguation: |
    Distinct from thermal pressure `P` or effective pressure from surface tension `σ`. Quantum Pressure `Q` depends explicitly on the spatial derivatives of the density field's amplitude (`√n`), not the density `n` itself, reflecting its origin in wave mechanics and uncertainty.
crosslinks:
  near_synonyms: [BOHM_POTENTIAL]
  antonyms: [GRAVITATIONAL_POTENTIAL]
  prerequisites: [NUMBER_DENSITY, EULER_EQUATION]
  downstream_effects: [HALO_CORE_RADIUS, VORTEX_FORMATION_THRESHOLD, HEALING_LENGTH]
license: CC-BY-SA-4.0
---

# Quantum Pressure

## Canonical (Pirouette)
A scalar potential, `Q = −(κ/2) ∇²√n/√n`, that contributes a force term `∇Q/m_H` to the Euler fluid dynamics equation. This force opposes the formation of sharp density gradients, effectively acting as a pressure to regularize solutions and establish a minimum length scale (the healing length, `ξ`) below which density cannot vary sharply. It is parameterized by the coefficient `kappa_quantum` (`κ`).

## EFT-First Summary
Within the effective field theory of a non-relativistic scalar field (e.g., axion-like dark matter), Quantum Pressure is identical to the Bohm Potential. It arises from the kinetic term `|∇Ψ|²` when the Schrödinger equation is cast in hydrodynamical form. This "pressure" represents the energy cost of gradients in the field's amplitude, preventing the formation of singular, cuspy structures predicted by collisionless cold dark matter and instead producing cored halos on scales set by the de Broglie wavelength of the particles.

## Glossary Links
- See also: [HALO_CORE_RADIUS](./HALO_CORE_RADIUS.md), [HEALING_LENGTH](./HEALING_LENGTH.md), [VORTEX](./VORTEX.md)