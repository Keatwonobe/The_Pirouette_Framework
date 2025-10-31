---
term: "Healing Length"
canonical_id: "HEALING_LENGTH"
symbol: "ξ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-006"]
---

---
term: Healing Length
canonical_id: HEALING_LENGTH
symbol: ξ
aliases: [Coherence Length]
parents: [COSMO-006]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-006
      lines: "SECT-Γ-A-HALO.3"
      snippet: |
        Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ); vortex lattice spacing d_v ∝ √(c_s/Ω).
  editors: [system-agent]
  review_log: []
triad:
  art: |
    The smallest tear a superfluid can mend; the quiet eye within the storm of a vortex. It is the measure of the fluid's self-awareness, the intrinsic scale that separates quantum wholeness from classical fracture.
  law: |
    The healing length ξ is the characteristic length scale below which the quantum pressure term `∇Q` dominates the hydrodynamics. It sets the minimum size of density variations, such as vortex cores, and is determined by the ratio of the quantum kinetic coefficient `κ` to the local fluid pressure or sound speed.
  philosophy: |
    The healing length provides the physical mechanism for regularizing singularities predicted by simpler fluid models. By introducing a fundamental quantum length scale, it allows the framework to model non-singular cored halos and structured topological defects (vortices), linking macroscopic astrophysical structures to the microphysics of the dark matter particle.
pirouette_definition: |
  The characteristic length scale over which the superfluid density `n` can vary significantly. It defines the minimum size of a density perturbation, such as the core of a quantum vortex where the density is suppressed. The healing length arises from the balance between the particle interaction energy (related to pressure) and the quantum kinetic energy (represented by the quantum pressure term, `Q`).
operational_definition:
  units: meters (m)
  symbol_table:
    - name: ξ
      meaning: Healing Length
      dimensions: L
      default_range: pc – kpc (in astrophysical contexts)
    - name: κ
      meaning: Quantum kinetic coefficient
      dimensions: M L⁴ T⁻²
      default_range: set by `m_H` (as `ħ²/m_H`)
    - name: Q
      meaning: Quantum pressure potential
      dimensions: M L² T⁻²
      default_range: contextual
    - name: m_H
      meaning: Mass of the superfluid constituent particle
      dimensions: M
      default_range: 1e-22 eV/c² – 100 MeV/c²
    - name: c_s
      meaning: Sound speed in the superfluid
      dimensions: L T⁻¹
      default_range: 1–1000 km/s
  measurement:
    procedures:
      - name: Vortex Core Sizing
        outline: |
          1. Generate a rotating superfluid halo model using the `SECT‑Γ‑A‑HALO` solver with an angular velocity `Ω > Ω_c`.
          2. Identify vortex locations from the `vortex_map` output artifact.
          3. Measure the radial density profile `n(r)` centered on a single vortex line from the `density` field.
          4. Fit the profile `n(r)` to a function of the form `n_0 tanh²(r/ξ_fit)`. The fitted parameter `ξ_fit` is the measured healing length.
        expected_signals: [Density-depleted vortex core, Azimuthal velocity field `v_θ ∝ 1/r` outside the core]
        pitfalls: [Insufficient numerical resolution (`Δx > ξ`) to resolve the core, Mesh grading distorting the core shape]
context_windows:
  - module: COSMO-006
    excerpt: |
      Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ); vortex lattice spacing d_v ∝ √(c_s/Ω). Observables: non‑circular flows in IFU maps; wiggles in stellar‑stream power spectra at k~1/d_v.
  - module: COSMO-006
    excerpt: |
      Euler (with quantum pressure Q and surface tension σ): ∂*t v + (v·∇)v = −∇h(n) − ∇Φ + ∇Q/m_H + ... where Q= −(κ/2) ∇²√n/√n ...
poetic_connections:
  motifs: [coherence, stiffness, vortex_eye, quantum_pixel]
  evocative_lines:
    - "cored profiles, vortex predictions"
    - "quantum pressure Q"
  association_matrix:
    - [ "QUANTUM_PRESSURE", 0.9 ]
    - [ "VORTEX", 0.8 ]
    - [ "CORED_HALO_PROFILE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: ξ (Gross-Pitaevskii Healing Length)
      domain: AMO|CM
      mapping_kind: mathematical
      equation_hint: |
        ξ = ħ / (√2 * m_H * c_s) where c_s² = (n/m_H) * dμ/dn
      justification: |
        The quantum pressure term `Q= −(κ/2) ∇²√n/√n` in `COSMO-006` is mathematically identical to the kinetic term arising from the Madelung transformation of the Gross-Pitaevskii Equation (GPE) if `κ=ħ²/m_H`. The healing length is the fundamental length scale in the GPE, describing the shortest distance over which the condensate wavefunction can heal to its bulk value.
      references:
        - title: Bose-Einstein Condensation in Dilute Gases
          where: Pethick, C. J., & Smith, H. (2008), Cambridge University Press.
          date: 2008-02-11
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The core radius `r_v` of a quantum vortex in a Pirouette superfluid halo is directly proportional to the local healing length, `r_v ≈ 1.738 ξ`."
      domain: theory
      falsifier: "Simulations using the `SECT‑Γ‑A‑HALO` solver showing measured vortex core sizes deviating '>>5%' from the predicted size based on the local `ξ` calculated from the equation of state, after accounting for numerical resolution effects."
      status: proposed
      links: [COSMO-006]
naming_notes:
  collisions: [ξ is a common symbol for correlation lengths in statistical mechanics and for coordinates in general relativity.]
  disambiguation: |
    Within Pirouette, ξ refers specifically to the superfluid coherence length arising from the quantum pressure term. It must be distinguished from `r_c` (the overall halo core radius, a result of hydrostatic equilibrium) and `d_v` (the vortex lattice spacing, set by rotation), although all three scales are physically related.
crosslinks:
  near_synonyms: [COHERENCE_LENGTH]
  antonyms: []
  prerequisites: [QUANTUM_PRESSURE, SUPERFLUID]
  downstream_effects: [VORTEX, CORED_HALO_PROFILE]
license: CC-BY-SA-4.0
---

# Healing Length

## Canonical (Pirouette)
The characteristic length scale over which the superfluid density `n` can vary significantly. It defines the minimum size of a density perturbation, such as the core of a quantum vortex where the density is suppressed. The healing length arises from the balance between the particle interaction energy (related to pressure) and the quantum kinetic energy (represented by the quantum pressure term, `Q`).

## EFT-First Summary
In the effective field theory of dark matter as a Bose-Einstein Condensate or superfluid, the Healing Length `ξ` corresponds to the coherence length of the condensate wavefunction. It is defined via the Gross-Pitaevskii equation, `ξ = ħ / (√2 * m * c_s)`, arising from the kinetic energy term that resists sharp density gradients. This length scale prevents the formation of singular central cusps in dark matter halos, replacing them with finite-sized cores and defining the structure of topological defects like quantum vortices.

## Glossary Links
- See also: [Quantum Pressure](link-to-quantum-pressure), [Vortex](link-to-vortex), [Cored Halo Profile](link-to-cored-halo-profile)