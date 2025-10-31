---
term: "Particle Mass"
canonical_id: "PARTICLE_MASS"
symbol: "m_H"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-006"]
---

---
term: Particle Mass
canonical_id: PARTICLE_MASS
symbol: m_H
aliases: []
parents: [COSMO-006]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-006
      lines: "SECT-Γ-A-HALO.5"
      snippet: |
        m_H_MeV: 17.0
  editors: [generative-agent]
  review_log: []
triad:
  art: |
    The indivisible grain of cosmic ether, whose collective dance weaves the superfluid's form. Each particle carries a whisper of phase, and together they flow as one, shaping the silent cores of galaxies.
  law: |
    The circulation of the superfluid velocity field `v` around any closed loop is quantized in integer multiples of `2π/m_H`. The value of `m_H` thus sets the fundamental scale for vorticity and the critical angular velocity for vortex formation in rotating halos.
  philosophy: |
    `m_H` bridges the quantum and cosmic scales. It is the microphysical parameter that governs the emergent, macroscopic hydrodynamics of the halo, dictating core sizes, vortex dynamics, and the effective stiffness of the superfluid against rotation. Without `m_H`, the superfluid lacks a fundamental quantum scale.
pirouette_definition: |
  The mass `m_H` of the fundamental particle comprising the superfluid described in module `COSMO-006`. It sets the relationship between the superfluid phase `θ` and the velocity field `v = ∇θ/m_H`. It also determines the quantum of circulation `∮ v·dl = 2πℓ/m_H` and the scale of the quantum pressure term `Q`. Its value directly impacts the core radius `r_c` of halos and the critical angular velocity `Ω_c` for vortex nucleation.
operational_definition:
  units: MeV/c²
  symbol_table:
    - name: m_H
      meaning: Mass of the fundamental superfluid particle
      dimensions: M
      default_range: 17.0 MeV/c² (fiducial)
  measurement:
    procedures:
      - name: Vortex Lattice Spacing Inversion
        outline: |
          Measure non-circular flows in galaxy IFU maps or identify periodic wiggles in stellar stream power spectra. The characteristic wavenumber `k` of these features corresponds to the inverse vortex lattice spacing `1/d_v`. Given a measurement of the system's angular velocity `Ω` and sound speed `c_s`, infer `m_H` via the relations `d_v ∝ √(c_s/Ω)` and the quantized circulation condition.
        expected_signals: [periodic velocity residuals in IFU maps, sharp peaks in stellar stream power spectra]
        pitfalls: [distinguishing vortex-induced signals from baryonic feedback or spiral structure, poorly constrained local sound speed c_s]
      - name: Halo Core Profile Fitting
        outline: |
          Fit the cored density profiles of dwarf galaxies using the stationary halo solver (`SECT-Γ-A-HALO`). The core radius `r_c` and central density `ρ_0` depend on the equation of state `P(X)` and `m_H`. By fitting a population of halos, `m_H` can be constrained.
        expected_signals: [characteristic core radii in low-mass halos]
        pitfalls: [degeneracy with equation of state parameters (PofX), baryonic effects mimicking a core]
context_windows:
  - module: COSMO-006
    excerpt: |
      Variables: density n, phase θ (velocity v=∇θ/m_H), pressure p=P(X), with X=μ−∂_t θ−v²/2−Φ. ... Euler (with quantum pressure Q and surface tension σ): ∂*t v + (v·∇)v = −∇h(n) − ∇Φ + ∇Q/m_H ... Poisson: ∇²Φ=4πG(ρ_b + m_H n)
  - module: COSMO-006
    excerpt: |
      Vortices: quantized circulation ∮ v·dl = 2πℓ/m_H, ℓ∈ℤ; evolve via HVBK‑like mutual‑friction terms (optional). ... Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ); vortex lattice spacing d_v ∝ √(c_s/Ω).
  - module: COSMO-006
    excerpt: |
      YAML config (excerpt):
      superfluid:
        PofX: {alpha: ..., beta: 0|0.5|1, delta: ...}
        ...
        m_H_MeV: 17.0
      solver:
        scheme: FV+HLLC | spectral
poetic_connections:
  motifs: [quantum, fluid, core, vortex, ether]
  evocative_lines:
    - "Replace scalar‑field halo solvers with a superfluid hydrodynamics solver"
    - "quantized circulation ∮ v·dl = 2πℓ/m_H"
  association_matrix:
    - [ "VORTEX", 0.9 ]
    - [ "HALO_CORE_RADIUS", 0.8 ]
    - [ "QUANTUM_PRESSURE", 0.6 ]
formal_mappings:
  candidates:
    - target: Axion mass m_a
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        ∇²Φ ≈ 4πG m_a n_a
      justification: |
        In axion BEC or Fuzzy Dark Matter models, dark matter is a light scalar boson which forms a condensate. The dynamics are described by the Gross-Pitaevskii equation, which is equivalent to the provided hydrodynamical equations. `m_H` plays the role of the fundamental particle mass, `m_a`.
      references:
        - title: "Ultralight scalars as cosmological dark matter"
          where: "arXiv:1407.7762"
          date: 2014-07-28
      confidence: 0.9
  adopted:
    - target: Axion mass m_a in Fuzzy/BEC Dark Matter models.
      rationale: |
        The mathematical structure of the `SECT-Γ-A-HALO` equations—continuity and Euler with a quantum pressure term—is isomorphic to the Gross-Pitaevskii formulation for a self-gravitating Bose-Einstein condensate. The parameter `m_H` maps directly to the mass of the constituent boson.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The dark matter particle mass `m_H` is approximately 17 MeV/c², leading to the formation of quantum vortices and characteristic non-circular flows in rotating dwarf galaxies."
      domain: phenomenology
      falsifier: "Astrophysical observation of dwarf galaxy kinematics showing no evidence for vortex-induced non-circular flows, or Lyman-alpha forest constraints ruling out a particle mass in this range via its effect on small-scale structure."
      status: proposed
      links: [COSMO-006]
naming_notes:
  collisions: [m_p (proton mass), m_e (electron mass), m_h (Higgs boson mass)]
  disambiguation: |
    `m_H` refers specifically to the mass of the superfluid halo particle within the `COSMO-006` context. It should not be confused with the Hubble parameter `H` or the mass of the Higgs boson. The `_H` subscript denotes 'Halo'.
crosslinks:
  near_synonyms: [AXION_MASS]
  antonyms: []
  prerequisites: [EQUATION_OF_STATE_P_X]
  downstream_effects: [VORTEX, HALO_CORE_RADIUS, QUANTUM_PRESSURE]
license: CC-BY-SA-4.0
---

# Particle Mass

## Canonical (Pirouette)
The mass `m_H` of the fundamental particle comprising the superfluid described in module `COSMO-006`. It sets the relationship between the superfluid phase `θ` and the velocity field `v = ∇θ/m_H`. It also determines the quantum of circulation `∮ v·dl = 2πℓ/m_H` and the scale of the quantum pressure term `Q`. Its value directly impacts the core radius `r_c` of halos and the critical angular velocity `Ω_c` for vortex nucleation.

## EFT-First Summary
In the context of Effective Field Theory, `m_H` is identified with the mass `m_a` of a bosonic dark matter particle in Fuzzy or BEC Dark Matter models. The superfluid hydrodynamics of `SECT-Γ-A-HALO` are a direct macroscopic manifestation of the particle's quantum nature, governed by the Gross-Pitaevskii equation. The fiducial value of 17 MeV/c² (from `COSMO-006`) is significantly heavier than typical ultralight candidates, implying a unique phenomenological regime for the Pirouette Framework. See [arXiv:1407.7762](https://arxiv.org/abs/1407.7762) for a review of the underlying theory.

## Glossary Links
- See also: [[VORTEX]], [[HALO_CORE_RADIUS]], [[QUANTUM_PRESSURE]]