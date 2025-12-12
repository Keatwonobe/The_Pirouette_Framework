---
term: "Γ-Soliton Halo"
canonical_id: "SOLITON_HALO"
symbol: ""
aliases: [Γ-condensate]
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Γ-Soliton Halo
canonical_id: GAMMA_SOLITON_HALO
symbol: 
aliases: ['Γ-condensate']
parents: ['COSMO-Γ-000', 'MATH-018', 'MATH-019', 'MATH-020']
children: ['COSMO-Γ-MERGE']
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-001
      snippet: |
        Model galactic and cluster halos as stationary Γ‑condensate (soliton) solutions labeled by topological index T ∈ ℤ.
  editors: ['System Agent']
  review_log: []
triad:
  art: |
    A quiet knot of potential energy, held together by its own gravity, forming a stable, ghost-like heart within a galaxy.
  law: |
    The product of a halo's central density and core radius, Σ_0 ≡ ρ_0 r_c, remains nearly constant across all halo mass scales, from dwarf galaxies to massive clusters.
  philosophy: |
    To model dark matter not as a sea of undiscovered particles, but as a macroscopic, coherent state of a fundamental field, unifying galactic structure (cores, rotation curves) and cosmology (lensing) under a single potential.
pirouette_definition: |
  A Γ-Soliton Halo is a stationary, spherically symmetric, topologically non-trivial solution of the Γ-field equations, characterized by an integer topological index T. It describes a localized, stable, and gravitationally self-bound configuration of the Γ-field, forming a mass distribution ρ_Γ(r) with a soft central core (r_c, ρ_0) and an NFW-like outer profile. These solutions are posited as first-principles models for galactic and cluster-scale dark matter halos, with their structural properties determined entirely by the field's potential V(Γ) defined in COSMO-Γ-000.
operational_definition:
  units: Properties are measured in standard astrophysical units (e.g., M_☉, kpc, M_☉/kpc³, km/s).
  symbol_table:
    - name: Γ(r)
      meaning: Γ-field amplitude profile
      dimensions: Contextual (depends on V(Γ) definition)
      default_range: contextual
    - name: ρ_Γ
      meaning: Mass-energy density of the Γ-field
      dimensions: M L⁻³
      default_range: 10⁻²⁶ – 10⁻²¹ kg m⁻³
    - name: V_c(r)
      meaning: Circular velocity at radius r
      dimensions: L T⁻¹
      default_range: 10–1000 km/s
    - name: T
      meaning: Topological index
      dimensions: dimensionless
      default_range: T ∈ ℤ
    - name: r_c
      meaning: Core radius (e.g., radius at half-central-density)
      dimensions: L
      default_range: 0.1–100 kpc
    - name: ρ_0
      meaning: Central density (at r=0)
      dimensions: M L⁻³
      default_range: 10⁻²⁴ – 10⁻²⁰ kg m⁻³
    - name: Σ_0
      meaning: Central surface density product (ρ_0 r_c)
      dimensions: M L⁻²
      default_range: ~140 M_☉ pc⁻²
  measurement:
    procedures:
      - name: Inferential Model Fitting
        outline: |
          1. Obtain observational data for a galaxy or cluster, such as its rotation curve V_c(r) from spectroscopy or its lensing convergence map κ(θ).
          2. Numerically solve the Γ-field equations for a given V(Γ) to generate a library of theoretical halo profiles (ρ_Γ(r), V_c(r), κ(θ)) corresponding to different topological indices T.
          3. Perform a statistical fit (e.g., MCMC, χ²) of the theoretical profiles to the observational data, marginalizing over baryonic components, to infer the best-fit Γ-soliton halo parameters (T, r_c, ρ_0).
        expected_signals: ['Cored density profiles', 'A near-constant Σ_0 value across a population of galaxies', 'Specific relations between stellar and halo properties (Baryon-halo coupling)']
        pitfalls: ['Degeneracy with baryonic mass models', 'Observational systematics (e.g., inclination angle, beam smearing)', 'Non-sphericity of real halos']
context_windows:
  - module: COSMO-001
    excerpt: |
      Model galactic and cluster halos as stationary Γ‑condensate (soliton) solutions labeled by topological index T ∈ ℤ. Derive core properties, rotation curves V_c(r), and lensing convergence κ(θ) from the same potential V(Γ) fixed in COSMO‑Γ‑000, without introducing particulate DM.
  - module: COSMO-001
    excerpt: |
      A near‑constant central surface density Σ_0 ≡ ρ_0 r_c emerges from the Γ equations across dwarf → L* → cluster scales, up to weak T‑dependent scatter. ... Lensing κ(θ) maps from Γ alone reproduce observed Einstein radii at fixed baryon fraction when V(Γ) is the same as in COSMO‑Γ‑000.
poetic_connections:
  motifs: ['soliton', 'condensate', 'core', 'gravity well', 'standing wave']
  evocative_lines:
    - "A near‑constant central surface density Σ_0 ... emerges from the Γ equations."
    - "reproduce dwarf diversity without stochastic sub‑grid feedback."
  association_matrix:
    - [ "Baryon-halo coupling", 0.8 ]
    - [ "Lensing Convergence", 0.7 ]
    - [ "Topological Index", 0.9 ]
formal_mappings:
  candidates:
    - target: Scalar Field Dark Matter (SFDM) / Bose-Einstein Condensate (BEC) Dark Matter
      domain: EFT
      mapping_kind: mathematical|conceptual
      equation_hint: |
        Γ″ + (2/r) Γ′ − dV/dΓ = 0  is the static, spherically-symmetric limit of the Gross-Pitaevskii or Klein-Gordon equation for a self-gravitating scalar condensate.
      justification: |
        The Γ-soliton is a non-perturbative, classical configuration of a scalar field (Γ) that is self-gravitating and forms a stable, localized structure. This is mathematically and conceptually identical to models of SFDM, where a BEC of ultralight bosons forms a galactic halo. The characteristic cored profile is a key prediction of both frameworks.
      references:
        - title: "Ultralight scalars as cosmological dark matter"
          where: Phys. Rev. D 62, 103517
          date: 2000-11-20
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The central surface density product Σ_0 ≡ ρ_0 r_c is nearly constant (ΔΣ/Σ_* ≲ 0.2) across all halo mass scales for the fixed potential V(Γ)."
      domain: phenomenology
      falsifier: "An observational survey of galaxies shows that Σ_0 correlates strongly and systematically with halo mass, or exhibits scatter significantly larger than predicted by the T-indexed family of solutions."
      status: proposed
      links: ['COSMO-001']
    - statement: "The observed diversity of inner rotation curve shapes in dwarf galaxies can be fully explained by the combination of the halo's topological index (T) and predictable baryonic compression effects, without invoking stochastic feedback."
      domain: phenomenology
      falsifier: "A statistically significant population of observed dwarf galaxies possess inner density profiles that are irreconcilable with any Γ_T soliton solution, even after accounting for baryons, thus requiring an alternative mechanism."
      status: proposed
      links: ['COSMO-001']
naming_notes:
  collisions: ['Γ is the standard symbol for the Gamma function in mathematics and for Christoffel symbols in General Relativity.']
  disambiguation: |
    In the Pirouette Framework, Γ consistently refers to a fundamental scalar field. A "Γ-Soliton Halo" is a specific solution of this field's equations of motion, not a mathematical function. The term "soliton" emphasizes its nature as a stable, localized, non-dispersive wave-like solution.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: ['COSMO-Γ-000', 'MATH-018', 'MATH-019', 'MATH-020']
  downstream_effects: ['COSMO-Γ-MERGE']
license: CC-BY-SA-4.0
---

# Γ-Soliton Halo

## Canonical (Pirouette)
A Γ-Soliton Halo is a stationary, spherically symmetric, topologically non-trivial solution of the Γ-field equations, characterized by an integer topological index T. It describes a localized, stable, and gravitationally self-bound configuration of the Γ-field, forming a mass distribution ρ_Γ(r) with a soft central core (r_c, ρ_0) and an NFW-like outer profile. These solutions are posited as first-principles models for galactic and cluster-scale dark matter halos, with their structural properties determined entirely by the field's potential V(Γ) defined in COSMO-Γ-000.

## EFT-First Summary
The Γ-Soliton Halo is the Pirouette Framework's realization of Scalar Field Dark Matter (SFDM) or Bose-Einstein Condensate (BEC) Dark Matter. It models a galaxy's dark matter halo as a macroscopic quantum state, or condensate, of a fundamental scalar field Γ. This approach naturally produces the cored density profiles observed in many galaxies, a key feature that distinguishes it from particulate Cold Dark Matter models which predict central cusps. The framework's core predictions, such as a near-constant central surface density, are directly testable against astrophysical observations.

## Glossary Links
- See also: `COSMO-Γ-000` (Γ-Field Potential), `COSMO-Γ-MERGE` (Soliton Mergers)