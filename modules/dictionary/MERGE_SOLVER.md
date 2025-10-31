---
term: "Merge Solver"
canonical_id: "MERGE_SOLVER"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-004"]
---

---
term: Merge Solver
canonical_id: MERGE_SOLVER
symbol: 
aliases: [Cluster Merger Simulator, Γ-Hydrodynamics Code]
parents: [COSMO-004]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-004
      lines: "D3"
      snippet: |
        D3. Merge Solver (YAML)
        merge_config.yaml
        freeze_manifest: path/to/freeze_manifest.yaml
        clusters:
        - mass_Msun: 1.2e15
          T_index: 1
          gas_fraction: 0.12
        - mass_Msun: 1.1e15
          T_index: 1
          gas_fraction: 0.12
          orbit:
            impact_parameter_kpc: 120
            v_in_kms: 2800
            z: 0.296
  editors: [GPT-4 (Dictionary Agent)]
  review_log: []
triad:
  art: |
    Two cosmic titans clash, their collision a bell that rings out the properties of the unseen Γ-field. The solver is the ear that listens to this echo, discerning the universe's fundamental score from the chaos of the merger.
  law: |
    Given a Freeze Manifest and initial conditions for two galaxy clusters (masses, gas fractions, T-indices, and orbital parameters), the Merge Solver evolves their N-body, hydrodynamic, and Γ-field interactions to produce synthetic observational maps and dynamical tracers, maintaining a fractional energy conservation of ≤1% over the simulation time.
  philosophy: |
    The Merge Solver bridges the abstract Γ cosmology, fixed by a Freeze Manifest, and the violent, observable reality of structure formation. It serves as the primary testbed for the non-linear, astrophysical consequences of the Γ-field, transforming a potential V(Γ) into falsifiable predictions for cluster dynamics and morphology.
pirouette_definition: |
  A numerical simulation tool that models the gravitational and hydrodynamical evolution of merging galaxy clusters within the Γ cosmology. The solver takes a `Freeze Manifest` to fix the cosmological background and Γ-field potential, along with initial conditions for two clusters (mass, gas content, topological index T, and orbital elements). It co-evolves dark matter (N-body), gas (hydrodynamics, e.g., HLLC), and the Γ-field on an adaptive mesh grid, solving the Poisson equation for the total gravitational potential. Its primary outputs are time-dependent synthetic observational maps (lensing convergence κ, X-ray, Sunyaev-Zel'dovich effect) and dynamical tracers.
operational_definition:
  units: Inputs use standard astrophysical units (Msun, kpc, km/s); outputs are dimensionless maps (e.g., κ, Compton-y) or physical maps (e.g., X-ray surface brightness).
  symbol_table:
    - name: M_cluster
      meaning: Initial total mass of a cluster
      dimensions: M
      default_range: 1e14–1e16 Msun
    - name: T_index
      meaning: Topological index defining the halo's internal Γ-field structure
      dimensions: dimensionless
      default_range: [-2, -1, 0, 1, 2]
    - name: f_gas
      meaning: Baryonic gas mass fraction
      dimensions: dimensionless
      default_range: 0.10–0.15
    - name: b
      meaning: Impact parameter of the collision
      dimensions: L
      default_range: 0–1000 kpc
    - name: v_in
      meaning: Initial relative velocity at infinity
      dimensions: L T⁻¹
      default_range: 1000–3000 km/s
  measurement:
    procedures:
      - name: Executing a Merger Simulation
        outline: |
          1. Define a `Freeze Manifest` to fix the Γ cosmology.
          2. Create a `merge_config.yaml` referencing the manifest.
          3. Specify the masses, T-indices, gas fractions, and orbital parameters for two clusters.
          4. Set numerical parameters (box size, grid resolution, AMR levels, solvers).
          5. Execute the simulation code, which time-integrates the coupled system.
          6. Post-process the output snapshots into synthetic observational maps and track dynamical quantities like core offsets.
        expected_signals: [Lensing convergence maps (κ), Thermal Sunyaev-Zel'dovich maps (Compton-y), X-ray surface brightness maps, Time-series of core separations (gas vs. dark matter)]
        pitfalls: [Numerical instability from poorly chosen timesteps or grid resolution, Violation of energy conservation tolerance ('>>1%'), Incorrect mapping of T-index to initial halo profile]
context_windows:
  - module: COSMO-004
    excerpt: |
      D3. Merge Solver (YAML)
      merge_config.yaml
      freeze_manifest: path/to/freeze_manifest.yaml
      potential:
        type: quadratic_plus_tail
        m_Gamma_eV: ${from_freeze}
      clusters:
        - mass_Msun: 1.2e15
          T_index: 1
          gas_fraction: 0.12
        - mass_Msun: 1.1e15
          ...
          orbit: {impact_parameter_kpc: 120, v_in_kms: 2800, z: 0.296}
      numerics:
        box_Mpc: 8
        base_grid: 256
        AMR_levels: 3
        poisson: multigrid
        hydro: HLLC
  - module: COSMO-004
    excerpt: |
      E) Validation Checklist (Copy-Paste)
      □ Background matches ΛCDM when V_tail→0 and m_Γ/H→∞ (≤0.1%).
      □ Boltzmann run produces TT/TE/EE and lensing within Planck contours for frozen params.
      ...
      □ MERGE Δx scaling consistent with frozen V(Γ); convergence passed.
poetic_connections:
  motifs: [cosmic collision, structural echo, frozen potential, numerical crucible]
  evocative_lines:
    - "...model the dynamics of merging galaxy clusters within the Γ cosmology."
    - "...a bell that rings out the properties of the unseen Γ-field."
  association_matrix:
    - [ "FREEZE_MANIFEST", 1.0 ]
    - [ "GAMMA_COSMOLOGY", 0.9 ]
    - [ "HALO_SOLVER", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: N-body/Hydrodynamics simulation code (e.g., GADGET, ENZO, AREPO)
      domain: Computational Astrophysics
      mapping_kind: operational
      justification: |
        The solver employs standard numerical techniques for astrophysical simulations: N-body methods for collisionless matter (dark matter), a hydrodynamics solver (HLLC) for baryonic gas, and a Poisson solver (multigrid) for gravity. Its specific contribution is the addition of a coupled, self-gravitating scalar field (Γ) to this standard framework.
      references: []
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The morphology and separation of gas and dark matter cores in a simulated merger, as predicted by the Merge Solver for a given Freeze Manifest, will match observations of real merging clusters (e.g., the Bullet Cluster)."
      domain: phenomenology
      falsifier: "A statistically significant sample of observed merging clusters shows core offsets or gas dynamics (e.g., shock front properties) inconsistent with any merger simulation run with a valid `Freeze Manifest` from the allowed parameter space."
      status: proposed
      links: [COSMO-004]
naming_notes:
  collisions: [The term "Solver" is generic in computational science.]
  disambiguation: |
    Distinguish from the `Halo Solver`, which models static, isolated halos, and the `Boltzmann Solver` (e.g., the CLASS patch), which computes linear cosmological perturbations. The `Merge Solver` specifically handles the non-linear dynamics of interacting, extended objects.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [FREEZE_MANIFEST, HALO_SOLVER]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Merge Solver

## Canonical (Pirouette)
A numerical simulation tool that models the gravitational and hydrodynamical evolution of merging galaxy clusters within the Γ cosmology. The solver takes a `Freeze Manifest` to fix the cosmological background and Γ-field potential, along with initial conditions for two clusters (mass, gas content, topological index T, and orbital elements). It co-evolves dark matter (N-body), gas (hydrodynamics, e.g., HLLC), and the Γ-field on an adaptive mesh grid, solving the Poisson equation for the total gravitational potential. Its primary outputs are time-dependent synthetic observational maps (lensing convergence κ, X-ray, Sunyaev-Zel'dovich effect) and dynamical tracers.

## EFT-First Summary
The Merge Solver is operationally equivalent to an N-body/Hydrodynamics simulation code used in computational astrophysics. It simulates the behavior of dark matter, baryonic gas, and gravity using standard numerical techniques (e.g., N-body, HLLC hydro, multigrid Poisson solver). Its novel feature within the Pirouette Framework is the inclusion of a dynamic, self-gravitating scalar field (the Γ-field) whose properties are determined by the cosmological model, enabling unique phenomenological predictions in the non-linear regime of structure formation.

## Glossary Links
- See also: FREEZE_MANIFEST, HALO_SOLVER, GAMMA_COSMOLOGY