---
term: "Halo Mass Density"
canonical_id: "HALO_MASS_DENSITY"
symbol: "ρ_Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Halo Mass Density
canonical_id: HALO_MASS_DENSITY
symbol: ρ_Γ
aliases: []
parents: [COSMO-Γ-HALO]
children: [COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-001
      lines: "Section 1"
      snippet: |
        (3) ρ_Γ(r) ≡ ½(Γ′²) + V(Γ) − V(Γ_∞)   (subtract vacuum)
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A halo's gravity is the echo of a field settling into its vacuum, a density born not of substance but of strain. This mass is the weight of the field's own tension, a gravitational ghost haunting spacetime.
  law: |
    The Halo Mass Density ρ_Γ is the effective gravitational source term derived from the kinetic (½Γ′²) and potential (V(Γ)) energy densities of a stationary Γ-field, relative to its vacuum energy V(Γ_∞).
  philosophy: |
    ρ_Γ reifies gravitational mass as a property of field configuration, eliminating the need for a separate dark matter particle species. Its existence grounds halo phenomenology—cores, rotation curves, and lensing—in the dynamics of a single field potential V(Γ), unifying disparate observations under one set of laws.
pirouette_definition: |
  The effective gravitational mass density, ρ_Γ, sourced by a stationary, spherically symmetric Γ-field. It is defined as the sum of the field's kinetic energy density, ½(dΓ/dr)², and its potential energy density, V(Γ), with the vacuum energy V(Γ_∞) subtracted to ensure ρ_Γ vanishes at infinity. It serves as the source term in the Newtonian Poisson equation, generating the gravitational potential of Γ-soliton halos.
operational_definition:
  units: M L⁻³ (kg m⁻³)
  symbol_table:
    - name: ρ_Γ
      meaning: Halo Mass Density from the Γ-field.
      dimensions: M L⁻³
      default_range: 10⁻²² to 10⁻²⁰ kg m⁻³
    - name: Γ
      meaning: The fundamental scalar field.
      dimensions: M¹ᐟ² L¹ᐟ² T⁻¹
      default_range: contextual
    - name: Γ′
      meaning: Radial derivative of the Γ-field, dΓ/dr.
      dimensions: M¹ᐟ² L⁻¹ᐟ² T⁻¹
      default_range: contextual
    - name: V(Γ)
      meaning: Potential energy density of the Γ-field.
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: V(Γ_∞)
      meaning: Vacuum energy density at the minimum of the potential.
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
  measurement:
    procedures:
      - name: Inferential Measurement via Gravitational Tracers
        outline: |
          1. Measure the total enclosed gravitational mass profile, M_tot(<r), using observational tracers such as galactic rotation curves (gas/stars) or gravitational lensing shear maps.
          2. Model and measure the baryonic mass profile, M_b(<r), from visible components (stars, gas).
          3. Calculate the Γ-halo mass profile by subtraction: M_Γ(<r) = M_tot(<r) - M_b(<r).
          4. Differentiate the resulting mass profile to obtain the density: ρ_Γ(r) = (1 / 4πr²) dM_Γ/dr.
        expected_signals: [A cored inner density profile, An NFW-like outer slope (ρ ∝ r⁻³), A near-constant central surface density Σ₀ across a range of halo masses]
        pitfalls: [Baryon-halo degeneracies in mass modeling, Observational uncertainties in rotation velocities or lensing shear, Departures from assumed spherical symmetry]
context_windows:
  - module: COSMO-001
    excerpt: |
      A family of stationary solutions Γ_T(r) exists for allowed T, generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers and NFW‑like outer slopes. A near‑constant central surface density Σ_0 ≡ ρ_0 r_c emerges from the Γ equations across dwarf → L* → cluster scales, up to weak T‑dependent scatter.
  - module: COSMO-001
    excerpt: |
      The effective equations in the Newtonian limit are a coupled system where the gravitational potential Φ is sourced by both baryonic density ρ_b and the halo mass density ρ_Γ. The halo density itself is defined by the field's energy: ρ_Γ(r) ≡ ½(Γ′²) + V(Γ) − V(Γ_∞). This term is inserted into the Poisson equation, ∇²Φ = 4πG (ρ_b(r) + ρ_Γ(r)), to compute total gravitational effects.
poetic_connections:
  motifs: [field stress, emergent mass, soliton core, gravitational shadow, vacuum structure]
  evocative_lines:
    - "density born not of substance but of strain."
    - "reproduce observed Einstein radii... without introducing particulate DM."
  association_matrix:
    - [ "GAMMA_FIELD", 0.9 ]
    - [ "GAMMA_SOLITON_HALO", 0.8 ]
    - [ "SURFACE_DENSITY_PRODUCT", 0.7 ]
formal_mappings:
  candidates:
    - target: T₀₀ (Energy Density)
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        T₀₀ = ½(∂₀Γ)² + ½(∇Γ)² + V(Γ)
      justification: |
        In General Relativity, the 00-component of the stress-energy tensor (T₀₀) for a scalar field in a static spacetime represents the total energy density, which acts as the source of gravity (gravitational mass). The definition of ρ_Γ is a direct rest-frame, weak-field limit of T₀₀, where time derivatives vanish and a vacuum baseline is subtracted.
      references:
        - title: "Scalar Fields in Cosmology"
          where: "Carroll, S. M. (2004). Spacetime and Geometry. Chapter 8."
          date: 2004-01-01
      confidence: 0.9
  adopted:
    - target: T₀₀ (Energy Density)
      rationale: The mapping is direct and mathematically robust; ρ_Γ is the non-relativistic limit of the gravitational mass-energy density for a scalar field.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The central surface density Σ_0 ≡ ρ_0 r_c, derived from ρ_Γ profiles, is nearly constant across halo masses from dwarfs to clusters for a fixed potential V(Γ)."
      domain: phenomenology
      falsifier: "Observational data shows a strong, systematic trend of Σ_0 with halo mass, or scatter far exceeding the predicted ΔΣ/Σ_* ≲ 0.2, using the V(Γ) potential frozen in COSMO-Γ-000."
      status: proposed
      links: [COSMO-Γ-HALO]
    - statement: "The diversity of inner halo slopes (cusps vs. cores) is a direct consequence of the interplay between the topological index T of the Γ-soliton and baryonic compression, without requiring stochastic feedback mechanisms."
      domain: phenomenology
      falsifier: "The model fails to simultaneously reproduce observed cored profiles in dwarf galaxies and cuspy profiles in clusters without re-tuning the potential V(Γ) for different object classes."
      status: proposed
      links: [COSMO-Γ-HALO]
naming_notes:
  collisions: [The symbol ρ is standard for density. The Γ subscript is crucial to distinguish it from baryonic density (ρ_b), total matter density (ρ_m), or a hypothetical particle dark matter density (ρ_DM).]
  disambiguation: |
    ρ_Γ is an *effective* mass density derived from field energy, not a density of discrete particles. It describes how the Γ-field's self-interaction and spatial variation source a gravitational field, analogous to how electromagnetic field energy contributes to the stress-energy tensor.
crosslinks:
  near_synonyms: []
  antonyms: [PARTICULATE_DARK_MATTER_DENSITY]
  prerequisites: [GAMMA_FIELD, GAMMA_FIELD_POTENTIAL_V]
  downstream_effects: [HALO_ROTATION_CURVE, LENSING_CONVERGENCE_KAPPA, HALO_MASS_FUNCTION]
license: CC-BY-SA-4.0
---

# Halo Mass Density

## Canonical (Pirouette)
The effective gravitational mass density, ρ_Γ, sourced by a stationary, spherically symmetric Γ-field. It is defined as the sum of the field's kinetic energy density, ½(dΓ/dr)², and its potential energy density, V(Γ), with the vacuum energy V(Γ_∞) subtracted to ensure ρ_Γ vanishes at infinity. It serves as the source term in the Newtonian Poisson equation, generating the gravitational potential of Γ-soliton halos.

## EFT-First Summary
The Halo Mass Density ρ_Γ is the non-relativistic limit of the T₀₀ component (energy density) of the stress-energy tensor for a classical scalar field. In this limit, it acts as the source for the Newtonian gravitational potential, replacing the need for a particulate dark matter component. Its functional form, derived from the field's kinetic and potential energies, naturally gives rise to galactic halo profiles with cored centers and predictable scaling relations.

## Glossary Links
- See also: [GAMMA_SOLITON_HALO](...), [SURFACE_DENSITY_PRODUCT](...), [HALO_ROTATION_CURVE](...)