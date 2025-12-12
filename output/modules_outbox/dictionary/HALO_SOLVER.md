---
term: "Halo Solver"
canonical_id: "HALO_SOLVER"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-004"]
---

---
term: Halo Solver
canonical_id: HALO_SOLVER
symbol: 
aliases: []
parents: [COSMO-004, MATH-018, MATH-019]
children: [MERGE_SOLVER]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-004
      lines: "D2. Halo Solver (YAML)"
      snippet: |
        halo_config.yaml
        freeze_manifest: path/to/freeze_manifest.yaml
        potential:
          type: quadratic_plus_tail
          m_Gamma_eV: ${from_freeze}
        geometry:
          R_max_kpc: 300
        solver:
          scheme: spectral
          N_points: 1024
          tol: 1e-10
  editors: [writing-agent-L2]
  review_log: []
triad:
  art: |
    From a single frozen moment in cosmic time, the Halo Solver sculpts the invisible architecture of a galaxy. It breathes gravitational life into the Γ field's potential, revealing the dense, dark heart where stars will later gather.
  law: |
    Given a `Freeze Manifest` specifying the potential `V(Γ)` and a cosmic anchor, the Halo Solver computes a static, spherically symmetric, isolated halo profile by solving the coupled Poisson and scalar field equations to a specified tolerance (`tol`).
  philosophy: |
    The Halo Solver is the first bridge from universal cosmological parameters to local, astrophysical structure. It enforces the `Freeze Manifest` as a non-negotiable axiom, ensuring that all subsequent simulations of individual objects inherit the exact same fundamental physics, making cross-scale comparisons meaningful.
pirouette_definition: |
  A computational tool that calculates the radial density profile `ρ(r)` and scalar field profile `Γ(r)` for a static, isolated, spherically symmetric dark matter halo. It takes as input a `Freeze Manifest` which fixes the scalar potential `V(Γ)` and the global cosmological scale. The solver numerically integrates the coupled Einstein-Klein-Gordon equations, optionally including a fixed baryonic potential, to find a stable solution satisfying boundary conditions of regularity at the center and asymptotic flatness.
operational_definition:
  units: Astrophysical (kpc, M_sun/kpc^3, etc.) for profiles; eV, M_pl for potential parameters.
  symbol_table:
    - name: freeze_manifest
      meaning: Input file path fixing the physics (`V(Γ)`) and cosmic scale.
      dimensions: dimensionless
      default_range: contextual (path)
    - name: V(Γ)
      meaning: Scalar field potential, specified by the manifest.
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: R_max_kpc
      meaning: Outer boundary radius for the numerical integration.
      dimensions: L
      default_range: 100-1000
    - name: tol
      meaning: Numerical tolerance for the solver's convergence.
      dimensions: dimensionless
      default_range: 1e-8 to 1e-12
    - name: ρ(r)
      meaning: Output radial mass-energy density profile of the halo.
      dimensions: M L⁻³
      default_range: contextual
    - name: Γ(r)
      meaning: Output radial scalar field profile of the halo.
      dimensions: M¹ᐟ² L¹ᐟ² T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Single Halo Structure Inference
        outline: |
          1. Obtain a `Freeze Manifest` from a cosmological fit (e.g., CMB analysis via COSMO-Γ-CMB).
          2. Configure the `halo_config.yaml` with the manifest path, a maximum radius `R_max_kpc`, and solver numerics (`N_points`, `tol`).
          3. Execute the solver.
          4. The output is the radial profile `ρ(r)` and lensing potential.
        expected_signals: [Predicted gravitational lensing profiles (convergence `κ`, shear `γ`), stellar velocity dispersions in dwarf galaxies, halo mass-concentration relations.]
        pitfalls: [Assuming halo isolation (neglecting tidal fields), incorrect baryonic profile assumptions, numerical instability if `R_max_kpc` is too large or `N_points` too small for the potential's characteristic scale.]
context_windows:
  - module: COSMO-004
    excerpt: |
      halo_config.yaml
      freeze_manifest: path/to/freeze_manifest.yaml
      potential:
        type: quadratic_plus_tail
        m_Gamma_eV: ${from_freeze}
      geometry:
        R_max_kpc: 300
      baryons:
        profile: burkert
      solver:
        scheme: spectral
        N_points: 1024
        tol: 1e-10
  - module: COSMO-004
    excerpt: |
      Validation Checklist (Copy-Paste)
      □ Background matches ΛCDM when V_tail→0 and m_Γ/H→∞ (≤0.1%).
      □ Boltzmann run produces TT/TE/EE and lensing within Planck contours for frozen params.
      □ Halo Σ₀ locus reproduced from same freeze.
      □ MERGE Δx scaling consistent with frozen V(Γ); convergence passed.
poetic_connections:
  motifs: [freezing, sculpting, isolation, structure formation]
  evocative_lines:
    - "One-shot global scale set; all U,T frozen thereafter."
    - "Halo Σ₀ locus reproduced from same freeze."
  association_matrix:
    - [ "FREEZE_MANIFEST", 0.9 ]
    - [ "MERGE_SOLVER", 0.7 ]
formal_mappings:
  candidates:
    - target: Einstein-Klein-Gordon (EKG) equations for a static, spherically symmetric metric
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        G_{μν} = 8πG T_{μν}[Γ]  ;  □Γ = V'(Γ)
      justification: |
        The solver finds stationary solutions (∂_t = 0) to the coupled equations for the metric components (via Poisson's equation in the weak-field limit) and the scalar field Γ. This is the definition of a gravitating scalar field configuration, analogous to early work on boson stars.
      references:
        - title: General relativistic boson stars
          where: Class.Quant.Grav. 20 (2003) R301
          date: 2003-09-12
      confidence: 0.9
  adopted:
    - target: Einstein-Klein-Gordon (EKG) static solution finder
      rationale: |
        The mapping is direct. The solver is a numerical implementation for finding solutions to the EKG system under the specific potential V(Γ) defined by the Freeze Manifest. It produces objects conceptually identical to scalar solitons or ground-state boson stars.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "For a given `Freeze Manifest`, the Halo Solver produces a unique, stable, ground-state halo profile for any mass."
      domain: theory
      falsifier: "Discovering multiple stable solutions (isomers) for the same mass and manifest, or finding that no stable solution exists above a certain mass (a maximum mass limit)."
      status: supported
      links: [COSMO-004]
    - statement: "The central density of halos predicted by the solver, using a CMB-inferred `Freeze Manifest`, is consistent with observed dark matter densities in ultra-faint dwarf galaxies."
      domain: phenomenology
      falsifier: "A systematic discrepancy where observations show cored profiles while the solver predicts cuspy profiles (or vice versa) that cannot be resolved by baryonic feedback models."
      status: under-test
      links: []
naming_notes:
  collisions: [None within Pirouette. In the literature, 'halo solver' is generic; this version is specifically tied to the `Freeze Manifest` and the Γ field.]
  disambiguation: |
    Distinguish from N-body simulation codes which form halos dynamically. The Halo Solver computes a static, equilibrium configuration for an *isolated* halo, serving as an initial condition or a theoretical benchmark, not a simulation of formation.
crosslinks:
  near_synonyms: []
  antonyms: [N_BODY_SIMULATOR]
  prerequisites: [FREEZE_MANIFEST, GAMMA_FIELD]
  downstream_effects: [MERGE_SOLVER, LENSING_PIPELINE]
license: CC-BY-SA-4.0
---

# Halo Solver

## Canonical (Pirouette)
A computational tool that calculates the radial density profile `ρ(r)` and scalar field profile `Γ(r)` for a static, isolated, spherically symmetric dark matter halo. It takes as input a `Freeze Manifest` which fixes the scalar potential `V(Γ)` and the global cosmological scale. The solver numerically integrates the coupled Einstein-Klein-Gordon equations, optionally including a fixed baryonic potential, to find a stable solution satisfying boundary conditions of regularity at the center and asymptotic flatness.

## EFT-First Summary
The Halo Solver is a numerical tool for finding static, spherically symmetric solutions to the Einstein-Klein-Gordon equations. It models a dark matter halo as a stable, gravitating scalar field configuration (a "boson star" or "scalar soliton") governed by a potential `V(Γ)`. The specific form of `V(Γ)` is fixed by a cosmological `Freeze Manifest`, ensuring consistency between large-scale cosmology and the small-scale structure of individual halos.

## Glossary Links
- See also: `FREEZE_MANIFEST`, `MERGE_SOLVER`, `GAMMA_FIELD`