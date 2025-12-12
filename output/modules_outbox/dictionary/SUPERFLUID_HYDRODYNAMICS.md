---
term: "Superfluid Hydrodynamics"
canonical_id: "SUPERFLUID_HYDRODYNAMICS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-006"]
---

---
term: Superfluid Hydrodynamics
canonical_id: SUPERFLUID_HYDRODYNAMICS
symbol:
aliases: [Quantum Fluid Dynamics, Irrotational Fluid Halos, BEC Dark Matter Hydrodynamics]
parents: [SECT‑Γ‑A, COSMO‑Γ‑HALO, COSMO‑Γ‑MERGE, MATH‑020]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-006
      lines: "all"
      snippet: |
        Purpose: Replace scalar‑field halo solvers with a superfluid hydrodynamics solver that includes surface tension and healing‑length physics. Produce cored profiles, vortex predictions, and merger offsets consistent with SECT‑Γ‑A.
  editors: [auto-compiler]
  review_log: []
triad:
  art: |
    Galactic halos as silent, frictionless oceans of quantum fluid, where gravity sculpts vast, cored structures and angular momentum crystallizes into lattices of quantized vortices.
  law: |
    The evolution of a halo's density (n) and velocity (v=∇θ/m_H) is governed by the continuity and quantum Euler equations, ∂_t v + (v·∇)v = −∇h(n) − ∇Φ + ∇Q/m_H + ∇σ_eff. This system produces stationary solutions with central cores of radius r_c and predicts quantized vortices for angular velocities Ω > Ω_c.
  philosophy: |
    Replaces the particle-collisionless paradigm of cold dark matter with a fluid-dynamic description, positing that the collective quantum behavior of the underlying field dictates halo structure (cores vs. cusps), angular momentum transport (vortices), and merger dynamics (offsets).
pirouette_definition: |
  A theoretical framework modeling astrophysical dark matter halos as an irrotational, zero-viscosity quantum fluid. The system is described by a density `n` and a velocity potential `θ`. Its dynamics are governed by the coupled Euler-Poisson equations, augmented by a quantum pressure term `Q` (proportional to `∇²√n/√n`) that prevents gravitational collapse into a cusp, and an effective surface tension `σ` that governs interface dynamics during mergers. This model predicts centrally-cored density profiles, the formation of quantized vortices above a critical angular velocity `Ω_c`, and observable offsets in halo mergers.
operational_definition:
  units: SI, with particle masses in MeV/c²
  symbol_table:
    - name: n
      meaning: Number density
      dimensions: L⁻³
      default_range: contextual
    - name: v
      meaning: Fluid velocity
      dimensions: L T⁻¹
      default_range: contextual
    - name: Q
      meaning: Quantum pressure potential
      dimensions: L² T⁻²
      default_range: contextual
    - name: σ
      meaning: Surface tension
      dimensions: M T⁻²
      default_range: contextual
    - name: m_H
      meaning: Constituent particle mass
      dimensions: M
      default_range: 1e-22 eV/c² to 100 MeV/c²
    - name: r_c
      meaning: Core radius
      dimensions: L
      default_range: 0.1–5 kpc
    - name: Ω_c
      meaning: Critical angular velocity for first vortex
      dimensions: T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Static Halo Profile Fitting
        outline: |
          Solve the 1D stationary equations (∇p = −ρ ∇Φ) for a given pressure function P(X) using a shooting or spectral solver to a residual <1e-10. Fit the resulting density profile ρ(r) and circular velocity V_c(r) to observational data from stellar/gas rotation curves or gravitational lensing.
        expected_signals: [A central density core ρ(r→0)=ρ_0, A specific relation between core radius r_c and total halo mass]
        pitfalls: [Degeneracies between superfluid parameters (m_H, P(X)) and baryonic physics, Projection effects in lensing/kinematic data]
      - name: Vortex Lattice Detection
        outline: |
          For a rotating halo model with Ω > Ω_c, calculate the predicted vortex lattice spacing d_v. Analyze high-resolution integral field unit (IFU) velocity maps of tracers (stars/gas) for coherent non-circular motions. Separately, analyze stellar stream power spectra for excess power at wavenumber k ≈ 1/d_v.
        expected_signals: [Periodic velocity residuals in IFU maps, A "wiggle" or peak in a stream's power spectrum]
        pitfalls: [Signal contamination from baryonic feedback or satellite perturbations, Insufficient kinematic resolution]
      - name: Merger Offset Analysis
        outline: |
          Simulate a halo merger using the hydro-Poisson solver with interface tracking. Calculate the predicted effective drag (σ/m)_eff and the resulting spatial offset Δ_x between the halo center (lensing) and the baryonic center (light). Compare with observed offsets in merging systems like the Bullet Cluster.
        expected_signals: [A non-zero offset Δ_x dependent on merger velocity and halo density]
        pitfalls: [Uncertainty in 3D merger geometry from 2D projected observations, Difficulty in precisely locating halo and galaxy centroids]
context_windows:
  - module: COSMO-006
    excerpt: |
      Purpose: Replace scalar‑field halo solvers with a superfluid hydrodynamics solver that includes surface tension and healing‑length physics. Produce cored profiles, vortex predictions, and merger offsets consistent with SECT‑Γ‑A.
  - module: COSMO-006
    excerpt: |
      Euler (with quantum pressure Q and surface tension σ): ∂*t v + (v·∇)v = −∇h(n) − ∇Φ + ∇Q/m_H + (σ/ρ) κ_s  n̂*⊥. Where Q= −(κ/2) ∇²√n/√n... Vortices: quantized circulation ∮ v·dl = 2πℓ/m_H, ℓ∈ℤ.
  - module: COSMO-006
    excerpt: |
      Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ); vortex lattice spacing d_v ∝ √(c_s/Ω). Observables: non‑circular flows in IFU maps; wiggles in stellar‑stream power spectra at k~1/d_v.
poetic_connections:
  motifs: [quantum ocean, vortex lattice, frictionless flow, cored heart]
  evocative_lines:
    - "Replace scalar‑field halo solvers with a superfluid hydrodynamics solver..."
    - "...wiggles in stellar‑stream power spectra at k~1/d_v."
  association_matrix:
    - [ "VORTEX_QUANTIZATION", 0.9 ]
    - [ "CORE_PROFILE", 0.9 ]
    - [ "MERGER_OFFSET", 0.7 ]
    - [ "SCALAR_FIELD_HALO", 0.5 ]
formal_mappings:
  candidates:
    - target: Gross-Pitaevskii-Poisson (GPP) System
      domain: AMO
      mapping_kind: mathematical
      equation_hint: |
        iħ ∂_t Ψ = (-ħ²/2m ∇² + V(x) + g|Ψ|²) Ψ  <=>  Continuity + Quantum Euler
      justification: |
        The Superfluid Hydrodynamics equations are the Madelung transformation of the GPP equation, which describes a self-interacting Bose-Einstein Condensate. The wavefunction Ψ is rewritten in polar form, Ψ=√n e^(iθ), where n is the number density and θ is the phase, yielding the fluid-like equations for n and v=∇θ/m_H. The quantum pressure Q arises directly from the kinetic term `∇²Ψ`.
      references:
        - title: "Bose-Einstein condensation in dilute gases"
          where: "Rev. Mod. Phys. 71, 463"
          date: 1999-04-01
      confidence: 1.0
    - target: Healing Length (ξ)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        Q ∝ κ ∇²√n/√n  ;  ξ ~ √κ
      justification: |
        The quantum pressure term, scaled by `kappa_quantum`, resists sharp density gradients and smooths structures below a characteristic scale known as the healing length, ξ. This scale sets the minimum size of features like vortex cores and is mathematically analogous to the healing length in terrestrial superfluids, representing the distance over which the wavefunction "heals" to its bulk value.
      references:
        - title: <internal>
          where: MATH-019
          date:
      confidence: 1.0
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Astrophysical dark matter halos possess central density cores with radii `r_c` set by the superfluid parameters (`m_H`, `P(X)`), rather than NFW-like cusps."
      domain: phenomenology
      falsifier: "Consistent high-resolution observations of a steep central density cusp (ρ ∝ r⁻¹, γ≥1) in a dark-matter-dominated dwarf galaxy with no plausible baryonic explanation."
      status: under-test
      links: [COSMO-006]
    - statement: "Galaxy mergers exhibit a spatial offset between dark matter and stellar components, caused by an effective drag predictable from the superfluid surface tension `σ`."
      domain: phenomenology
      falsifier: "A statistically significant sample of merging clusters showing zero average offset between dark matter and galaxies, after accounting for projection effects and other biases."
      status: proposed
      links: [COSMO-006]
    - statement: "Rapidly rotating halos contain a lattice of quantized vortices, inducing detectable non-circular motions in tracer populations at the level predicted by the HVBK mutual-friction terms."
      domain: phenomenology
      falsifier: "Deep IFU observations of rapidly rotating, DM-dominated galaxies revealing perfectly circular velocity fields, ruling out vortex-induced perturbations at the predicted amplitude."
      status: proposed
      links: [COSMO-006]
naming_notes:
  collisions: [The symbol `σ` is used for surface tension, which can conflict with its common use for velocity dispersion in galactic dynamics. The symbol `κ` is used for the quantum pressure coefficient, not to be confused with epicyclic frequency.]
  disambiguation: |
    Distinguish from classical hydrodynamics by the presence of the quantum pressure term `Q` (from `kappa_quantum`) and quantized vorticity. Differentiate from simpler scalar field/Fuzzy DM models by the explicit inclusion of a general self-interaction pressure `P(X)` and a surface tension term `σ_surface`.
crosslinks:
  near_synonyms: [SCALAR_FIELD_HALO, FUZZY_DARK_MATTER]
  antonyms: [NFW_PROFILE, COLLISIONLESS_DARK_MATTER]
  prerequisites: [EULER_EQUATIONS, POISSON_EQUATION]
  downstream_effects: [CORE_PROFILE, VORTEX_QUANTIZATION, MERGER_OFFSET]
license: CC-BY-SA-4.0
---