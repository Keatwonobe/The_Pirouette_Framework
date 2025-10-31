---
term: "Vortex"
canonical_id: "VORTEX"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-006"]
---

---
term: Vortex
canonical_id: VORTEX
symbol: ℓ
aliases: [Quantized Vortex, Superfluid Vortex, Topological Defect]
parents: [COSMO-006]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-006
      lines: "SECT-Γ-A-HALO, part 1 & 3"
      snippet: |
        Vortices: quantized circulation ∮ v·dl = 2πℓ/m_H, ℓ∈ℤ; evolve via HVBK‑like mutual‑friction terms...
        Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ)...
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A silent storm in a frictionless sea, where rotation can only exist as a crystal of tiny, stable whirlpools. Each vortex is a thread of nothingness around which the universe must flow in perfect, measured steps. They are the gears of a quantum machine turning on a galactic scale.
  law: |
    The circulation of the velocity field `v` around any closed path `dl` enclosing a vortex core is quantized, equal to an integer `ℓ` times the fundamental constant `2π/m_H`. A vortex with `ℓ=0` is equivalent to no vortex. Systems rotating faster than a critical angular velocity `Ω_c` must nucleate vortices.
  philosophy: |
    Vortices are the definitive signature of macroscopic quantum coherence in an astrophysical fluid. They are not merely a feature of flow, but the physical manifestation of how an irrotational superfluid accommodates angular momentum. Their existence and arrangement provide a direct, observable link between the microphysics of the constituent particle (`m_H`) and the large-scale dynamics of galaxies.
pirouette_definition: |
  A line-like topological defect in a superfluid, characterized by a phase singularity around which the velocity field `v` circulates. The defining property is quantized circulation: the integral `∮ v·dl` over any closed loop enclosing the core must equal `2πℓ/m_H`, where `ℓ` is an integer quantum number and `m_H` is the fluid's constituent particle mass. Vortices are the mechanism by which the superfluid responds to external rotation exceeding a critical angular velocity `Ω_c`, typically arranging themselves into a regular lattice with spacing `d_v`.
operational_definition:
  units: Circulation has units of m²/s (L² T⁻¹). The vortex quantum number `ℓ` is dimensionless.
  symbol_table:
    - name: ℓ
      meaning: Vortex quantum number or "charge"
      dimensions: dimensionless
      default_range: ℤ (typically ±1 for stable vortices)
    - name: ∮ v·dl
      meaning: Kinematic circulation of the velocity field
      dimensions: L² T⁻¹
      default_range: N × (2π/m_H)
    - name: Ω_c
      meaning: Critical angular velocity for first vortex nucleation
      dimensions: T⁻¹
      default_range: contextual; scales with (core radius)⁻²
    - name: d_v
      meaning: Inter-vortex spacing in a vortex lattice
      dimensions: L
      default_range: contextual; scales with Ω⁻¹/²
  measurement:
    procedures:
      - name: Kinematic Mapping
        outline: |
          Using an Integral Field Unit (IFU), obtain a high-resolution 2D velocity map of a rotating, cored galactic halo. Search for localized, non-circular flow patterns or sharp velocity gradients inconsistent with smooth laminar rotation. A `ℓ=1` vortex core would appear as a ~kpc-scale velocity dipole superimposed on the global rotation.
        expected_signals: [Localized velocity dipoles, sharp gradients in velocity maps]
        pitfalls: [Insufficient spatial/spectral resolution (beam smearing), confusion with baryonic feedback or minor mergers, projection effects]
      - name: Stellar Stream Power Spectrum Analysis
        outline: |
          Identify a cold stellar stream passing through a candidate superfluid halo. Measure the density and/or velocity perturbations along the stream. Compute the 1D power spectrum of these perturbations. A vortex lattice acts as a periodic gravitational potential, which should imprint a corresponding feature.
        expected_signals: [A narrow peak or "wiggle" in the power spectrum at a wavenumber k ≈ 1/d_v]
        pitfalls: [Low stream signal-to-noise, epicyclic motion, contamination from globular clusters or dark subhalos]
context_windows:
  - module: COSMO-006
    excerpt: |
      Vortices: quantized circulation ∮ v·dl = 2πℓ/m_H, ℓ∈ℤ; evolve via HVBK‑like mutual‑friction terms (optional) with coefficient set by P(X) parameters.
  - module: COSMO-006
    excerpt: |
      Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ); vortex lattice spacing d_v ∝ √(c_s/Ω). Observables: non‑circular flows in IFU maps; wiggles in stellar‑stream power spectra at k~1/d_v.
poetic_connections:
  motifs: [quantum whirlpool, topological knot, lattice of flow, spinning void]
  evocative_lines:
    - "wiggles in stellar-stream power spectra"
    - "quantized circulation"
    - "critical angular velocity for first vortex"
  association_matrix:
    - [ "SUPERFLUID_HYDRODYNAMICS", 0.9 ]
    - [ "ANGULAR_MOMENTUM", 0.8 ]
    - [ "DARK_MATTER_HALO_CORE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Quantized vortex (in Superfluid Helium / Bose-Einstein Condensate)
      domain: AMO|CM
      mapping_kind: mathematical
      equation_hint: |
        ∮ v·dl = ℓ (2πħ / m_particle)
      justification: |
        The Pirouette definition of a vortex, including quantized circulation, a critical angular velocity for nucleation, and the formation of a vortex lattice (Abrikosov lattice), is a direct transposition of the physics of vortices in laboratory superfluids and Bose-Einstein Condensates to a cosmological fluid. The governing equations are formally identical.
      references:
        - title: "Theory of Bose-Einstein condensation in trapped gases"
          where: "Reviews of Modern Physics, 71(3), 463"
          date: 1999-04-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "A superfluid halo rotating faster than its Ω_c must contain a lattice of quantized vortices."
      domain: phenomenology
      falsifier: "A high-resolution kinematic observation of a rapidly rotating, cored dark matter halo that exhibits a smooth, laminar velocity field without localized perturbations consistent with vortex cores."
      status: proposed
      links: [COSMO-006]
    - statement: "The characteristic spacing `d_v` between vortices in a lattice scales with the system's angular velocity as `d_v ∝ Ω⁻¹/²`."
      domain: theory
      falsifier: "Observational inference of vortex lattice spacing across multiple halos showing a scaling with Ω significantly different from -1/2."
      status: proposed
      links: [COSMO-006]
naming_notes:
  collisions: [The term "vortex" is generic in classical fluid dynamics (e.g., hurricane, whirlpool).]
  disambiguation: |
    In Pirouette, Vortex implies a *quantized* vortex, a topological defect whose circulation is mandated by the particle mass `m_H`. This is fundamentally different from a classical vortex, whose circulation can take any continuous value. The existence of a Pirouette Vortex is a direct consequence of the fluid's quantum nature.
crosslinks:
  near_synonyms: [QUANTIZED_VORTEX]
  antonyms: [LAMINAR_FLOW]
  prerequisites: [SUPERFLUID_HYDRODYNAMICS, ANGULAR_MOMENTUM]
  downstream_effects: [NON_CIRCULAR_FLOWS, STREAM_PERTURBATIONS]
license: CC-BY-SA-4.0
---

# Vortex

## Canonical (Pirouette)
A line-like topological defect in a superfluid, characterized by a phase singularity around which the velocity field `v` circulates. The defining property is quantized circulation: the integral `∮ v·dl` over any closed loop enclosing the core must equal `2πℓ/m_H`, where `ℓ` is an integer quantum number and `m_H` is the fluid's constituent particle mass. Vortices are the mechanism by which the superfluid responds to external rotation exceeding a critical angular velocity `Ω_c`, typically arranging themselves into a regular lattice.

## EFT-First Summary
A Vortex is the astrophysical analogue of a quantized vortex in a laboratory Bose-Einstein Condensate (BEC) or superfluid. It is a topological defect where the phase of the complex scalar field winds by `2πℓ`. This quantization of circulation is a direct consequence of the field's coherence over macroscopic scales. The presence and regular arrangement of these vortices in a rotating dark matter halo are key observational signatures that distinguish this model from classical fluid or particle-based dark matter candidates.

## Glossary Links
- See also: SUPERFLUID_HYDRODYNAMICS, ANGULAR_MOMENTUM, DARK_MATTER_HALO_CORE, NON_CIRCULAR_FLOWS