---
term: "Γ-field"
canonical_id: "FIELD"
symbol: "Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Γ-field
canonical_id: GAMMA_FIELD
symbol: Γ
aliases: []
parents: ['COSMO-001', 'COSMO-Γ-000', 'MATH-018', 'MATH-019', 'MATH-020']
children: ['COSMO-Γ-MERGE']
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-001
      snippet: |
        Model galactic and cluster halos as stationary Γ‑condensate (soliton) solutions labeled by topological index T ∈ ℤ. Derive core properties, rotation curves V_c(r), and lensing convergence κ(θ) from the same potential V(Γ) fixed in COSMO‑Γ‑000, without introducing particulate DM.
  editors: ['system']
  review_log: []
triad:
  art: |
    An unseen ocean whose quiet currents sculpt the stars. It is the silent, cohesive architecture of the cosmos, a standing wave of potential that holds galaxies in its gravitational embrace.
  law: |
    Across all halo mass scales, the product of a Γ-halo's central energy density and its core radius (Σ_0 ≡ ρ_0 r_c) remains nearly constant, up to a predictable, weak scatter indexed by the halo's topological class T.
  philosophy: |
    The Γ-field replaces the hypothesis of particulate dark matter with a continuous field, unifying diverse halo phenomena (cores, rotation curves, lensing) as emergent properties of a single, non-linear equation of state, thereby favoring deterministic structure formation over stochastic feedback models.
pirouette_definition: |
  The Γ-field is a fundamental, stationary, real scalar field whose potential energy V(Γ) and spatial gradient energy ½(∇Γ)² collectively source the gravitational potential of galactic and cluster halos. Its dynamics are governed by a balance between its potential gradient (dV/dΓ) and its curvature (∇²Γ), yielding stable, cored soliton solutions (Γ-halos) characterized by a topological index T ∈ ℤ. The field's vacuum expectation value is Γ_∞, and its excitations manifest as the mass distribution ρ_Γ.
operational_definition:
  units: In natural units (ħ=c=1), Γ has dimensions of energy or inverse length (e.g., GeV or kpc⁻¹). ρ_Γ has dimensions of energy density (e.g., GeV⁴ or M_☉/kpc³).
  symbol_table:
    - name: Γ(r)
      meaning: Radial profile of the stationary scalar field.
      dimensions: M L⁻¹ (Energy)
      default_range: Contextual; depends on potential V(Γ) and boundary conditions.
    - name: ρ_Γ
      meaning: Energy density contributed by the Γ-field, acting as a gravitational source.
      dimensions: M L⁻¹ T⁻² (Energy Density)
      default_range: 10⁻³ – 10² M_☉/pc³
    - name: T
      meaning: Topological index, a discrete integer classifying the soliton solution.
      dimensions: dimensionless
      default_range: Low integers (e.g., T ∈ {0, 1, 2, ...})
    - name: Σ_0
      meaning: Central surface density of the Γ-halo (ρ_0 * r_c).
      dimensions: M L⁻² (Mass/Area)
      default_range: ~100 M_☉/pc²
  measurement:
    procedures:
      - name: Gravitational Inference via Halo Fitting
        outline: |
          1. Measure the total gravitational potential of a galaxy or cluster via observational probes (stellar/gas kinematics for V_c(r), or gravitational lensing for κ(θ)).
          2. Model and subtract the contribution from visible baryons (ρ_b).
          3. Numerically solve the coupled Γ-field and Poisson equations (Eqs. 1-2) for a given potential V(Γ) and topological index T.
          4. Fit the resulting theoretical mass profile ρ_Γ to the inferred dark matter distribution to constrain the parameters of the solution (e.g., r_c, ρ_0).
        expected_signals: [Cored central density profiles, A specific relationship between core radius and central density across a galaxy population, Specific lensing signatures (κ(θ)) determined by the extended ρ_Γ profile]
        pitfalls: [Degeneracies with baryonic physics (e.g., feedback), Uncertainty in the baryonic mass distribution, The true form of the potential V(Γ) is an unconstrained assumption]
context_windows:
  - module: COSMO-001
    excerpt: |
      A family of stationary solutions Γ_T(r) exists for allowed T, generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers and NFW‑like outer slopes. A near‑constant central surface density Σ_0 ≡ ρ_0 r_c emerges from the Γ equations across dwarf → L* → cluster scales, up to weak T‑dependent scatter.
  - module: COSMO-001
    excerpt: |
      Lensing κ(θ) maps from Γ alone reproduce observed Einstein radii at fixed baryon fraction when V(Γ) is the same as in COSMO‑Γ‑000 (D3 freeze honored). Adiabatic contraction modifies r_c and V_max along a one‑parameter track predictable from Γ’s equation.
poetic_connections:
  motifs: [soliton, condensate, standing_wave, gravitational_scaffolding, halo_core]
  evocative_lines:
    - "A family of stationary solutions Γ_T(r) exists... generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers..."
    - "Lensing κ(θ) maps from Γ alone reproduce observed Einstein radii..."
  association_matrix:
    - [ "HALO_PROFILE", 0.9 ]
    - [ "SCALAR_POTENTIAL", 0.8 ]
    - [ "PARTICULATE_DARK_MATTER", -0.7 ]
    - [ "GRAVITATIONAL_LENSING", 0.6 ]
formal_mappings:
  candidates:
    - target: Scalar Field Dark Matter (SFDM) / Boson Star
      domain: Astroparticle Physics/GR
      mapping_kind: conceptual
      equation_hint: |
        ∇²Φ = 4πG(ρ_b + ½|∂_tΦ|² + ½|∇Φ|² + m²|Φ|²) (where Γ is the static part of a complex scalar Φ)
      justification: |
        The Γ-field framework models galactic halos as stable, gravitationally bound condensates of a scalar field, known as solitons or boson stars. The governing equations for a static, spherically symmetric profile are identical. This approach is a prominent alternative to particle dark matter, intended to resolve small-scale structure problems like the cusp-core issue.
      references:
        - title: "Ultralight scalars as cosmological dark matter"
          where: "Phys.Rev.D 62 (2000) 103517"
          date: 2000-08-29
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The central surface density of Γ-halos, Σ_0 ≡ ρ_0 r_c, is nearly constant (~Σ_*) across a wide range of halo masses."
      domain: phenomenology
      falsifier: "An observational finding that Σ_0 systematically scales with halo mass (e.g., Σ_0 ∝ M_h^α with α significantly different from zero) after accounting for baryonic effects and T-scatter."
      status: proposed
      links: ['COSMO-001']
    - statement: "The V(Γ) potential constrained by cosmology is sufficient to reproduce observed lensing Einstein radii in clusters without particulate dark matter."
      domain: phenomenology
      falsifier: "A systematic failure to match observed cluster lensing convergence κ(θ) using Γ-halo profiles generated from the cosmologically fixed potential, requiring either a different potential or an additional dark component."
      status: proposed
      links: ['COSMO-001']
    - statement: "The diversity in dwarf galaxy rotation curves (cusp vs. core) is fully explained by the combination of the topological index T and baryonic gravitational influence on the Γ-field."
      domain: phenomenology
      falsifier: "Finding observed inner rotation curve shapes that cannot be generated by any solution of the Γ-field equations for any T, given the observed baryonic distribution."
      status: proposed
      links: ['COSMO-001']
naming_notes:
  collisions: [The symbol Γ is standard for the Gamma function in mathematics, Gamma matrices in quantum field theory, and the photon in particle physics. Context is critical.]
  disambiguation: |
    In the Pirouette Framework, Γ specifically refers to this fundamental, halo-forming scalar field and its radial profile Γ(r). It should not be confused with other uses of the symbol unless explicitly stated. It is a field, not a particle or a mathematical function.
crosslinks:
  near_synonyms: [SOLITONIC_DARK_MATTER_FIELD]
  antonyms: [PARTICULATE_DARK_MATTER]
  prerequisites: [SCALAR_FIELD_THEORY, GRAVITATIONAL_POTENTIAL]
  downstream_effects: [HALO_PROFILE, ROTATION_CURVE, GRAVITATIONAL_LENSING, BARYONIC_FEEDBACK_COUPLING]
license: CC-BY-SA-4.0
---