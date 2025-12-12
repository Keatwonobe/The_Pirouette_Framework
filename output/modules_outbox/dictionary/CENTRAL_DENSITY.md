---
term: "Central Density"
canonical_id: "CENTRAL_DENSITY"
symbol: "ρ_0"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Central Density
canonical_id: CENTRAL_DENSITY
symbol: ρ_0
aliases: [Central Γ-field Density, Core Density]
parents: [COSMO-Γ-HALO]
children: [COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-001
      snippet: |
        Outputs (per solution):
        • Core radius r_c (e.g., radius where ρ_Γ drops to ρ_0/2)
        • Central density ρ_0 = ρ_Γ(0)
        • Surface-density product Σ_0 = ρ_0 r_c
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    The still, dense heart of the soliton halo, where the Γ-field's potential energy is most concentrated. It is the gravitational anchor from which the halo's extended structure unfurls, a point of maximum calm and substance.
  law: |
    The central density ρ_0, multiplied by the core radius r_c, yields a nearly constant surface density Σ_0 across a wide range of halo masses. This product, Σ_0, is a primary, falsifiable prediction of the Γ-halo model.
  philosophy: |
    ρ_0 anchors the physical scale of a Γ-soliton halo. Unlike cuspy profiles where density diverges, ρ_0 is finite—a direct consequence of the field's potential V(Γ) and topological index T. It represents a fundamental scale of the theory, a bulwark against the unphysical infinities of simpler models.
pirouette_definition: |
  The mass-energy density of the stationary Γ-field, ρ_Γ(r), evaluated at the center of a spherically symmetric halo (r=0). Given the core regularity condition Γ′(0)=0, ρ_0 simplifies to the potential energy density difference between the central field value Γ(0) and the vacuum value Γ_∞, according to ρ_0 = V(Γ(0)) − V(Γ_∞). It is a direct output of the numerical field equation solver and a key parameter in halo mass models.
operational_definition:
  units: M_☉ kpc⁻³ (or kg m⁻³)
  symbol_table:
    - name: ρ_0
      meaning: Central mass density of the Γ-field.
      dimensions: M L⁻³
      default_range: 10⁻² – 10 M_☉ pc⁻³
    - name: Γ(r)
      meaning: Radial profile of the scalar Γ-field.
      dimensions: Contextual (depends on potential V)
      default_range: contextual
    - name: V(Γ)
      meaning: Self-interaction potential of the Γ-field.
      dimensions: M L⁻¹ T⁻² (Energy Density)
      default_range: contextual
  measurement:
    procedures:
      - name: Numerical Solution
        outline: |
          Solve the stationary field equation Γ″ + (2/r)Γ′ − dV/dΓ = 0 for Γ(r) using a spectral or FEM solver with boundary conditions Γ′(0)=0 and Γ(∞)→Γ_∞. Compute the density profile ρ_Γ(r) ≡ ½(Γ′²) + V(Γ) − V(Γ_∞). ρ_0 is the value ρ_Γ(0).
        expected_signals: [A stable, convergent numerical solution for Γ(r), A finite, positive value for ρ_Γ(0)]
        pitfalls: [Numerical instability near r=0, Failure to subtract the vacuum energy V(Γ_∞), Insufficient solver precision leading to inaccurate core values]
      - name: Observational Inference
        outline: |
          Fit the rotation curve V_c(r) or lensing convergence κ(θ) derived from the Γ-halo model to observational data (e.g., galactic HI velocity fields, cluster lensing maps). ρ_0 is a primary parameter of the cored density profile ρ_Γ(r) that is determined by the fit, along with the core radius r_c.
        expected_signals: [A good χ² fit to kinematic or lensing data, A plateau in the inner rotation curve consistent with a finite ρ_0]
        pitfalls: [Degeneracy with baryonic mass components, Beam smearing effects mimicking a core, Assuming a specific topological index T instead of fitting for it]
context_windows:
  - module: COSMO-Γ-HALO
    excerpt: |
      A family of stationary solutions Γ_T(r) exists for allowed T, generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers and NFW-like outer slopes.
  - module: COSMO-Γ-HALO
    excerpt: |
      A near-constant central surface density Σ_0 ≡ ρ_0 r_c emerges from the Γ equations across dwarf → L* → cluster scales, up to weak T-dependent scatter.
poetic_connections:
  motifs: [core, anchor, stillness, peak, condensation, ground-state]
  evocative_lines:
    - "A family of stationary solutions... with cored centers."
    - "The still, dense heart of the soliton halo."
  association_matrix:
    - [ "CORE_RADIUS", 0.9 ]
    - [ "TOPOLOGICAL_INDEX", 0.7 ]
    - [ "CENTRAL_SURFACE_DENSITY", 1.0 ]
formal_mappings:
  candidates:
    - target: ρ_core
      domain: Cosmology/Astrophysics
      mapping_kind: operational
      justification: |
        ρ_0 is operationally equivalent to the central core density parameter in phenomenological dark matter halo models (e.g., Burkert, pseudo-isothermal). It parameterizes the density plateau that observations of dwarf galaxy rotation curves often favor over the cusps predicted by simple CDM.
      confidence: 0.9
    - target: Bose-Einstein Condensate (BEC) central density
      domain: AMO/Cosmology
      mapping_kind: conceptual
      equation_hint: |
        ρ_0 ∝ m |ψ(0)|²
      justification: |
        If the Γ-field is interpreted as the macroscopic wavefunction ψ of a BEC (e.g., Fuzzy Dark Matter), then ρ_0 corresponds to the peak particle number density at the center of the gravitational potential well. The cored profile arises from quantum pressure balancing gravity.
      references:
        - title: "Ultralight scalars as cosmological dark matter"
          where: "Phys.Rev.D 62 (2000) 103517"
          date: 2000-08-29
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The central density ρ_0 is finite for all stable Γ-soliton halos."
      domain: theory
      falsifier: "Discovery of a stable, physical solution to the Γ-field equations that has a divergent (cuspy) density at r=0."
      status: proposed
      links: [COSMO-Γ-HALO]
    - statement: "The product ρ_0 r_c forms a nearly constant surface density Σ_0 across halo masses."
      domain: phenomenology
      falsifier: "Observational data showing a strong, systematic scaling of the inferred Σ_0 = ρ_0 r_c with halo mass, beyond the weak T-indexed scatter predicted by the model."
      status: proposed
      links: [COSMO-Γ-HALO]
naming_notes:
  collisions: ["The symbol ρ_0 is standard for central density in many fields of astrophysics (e.g., stellar structure) and for present-day cosmological density. Context is critical."]
  disambiguation: |
    Distinguish from the baryonic central density, ρ_{b,0}, and the cosmological critical density, ρ_{crit,0}. In the Pirouette Framework, ρ_0 specifically refers to the density of the Γ-field component at r=0 unless otherwise specified.
crosslinks:
  near_synonyms: [CORE_DENSITY]
  antonyms: []
  prerequisites: [GAMMA_FIELD, FIELD_POTENTIAL_V]
  downstream_effects: [CORE_RADIUS, CENTRAL_SURFACE_DENSITY, ROTATION_CURVE]
license: CC-BY-SA-4.0
---