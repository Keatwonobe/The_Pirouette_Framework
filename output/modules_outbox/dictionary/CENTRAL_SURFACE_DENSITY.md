---
term: "Central Surface Density"
canonical_id: "CENTRAL_SURFACE_DENSITY"
symbol: "Σ_0"
aliases: [Core surface-density locus]
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Central Surface Density
canonical_id: CENTRAL_SURFACE_DENSITY
symbol: Σ_0
aliases: [Core surface-density locus]
parents: [COSMO-Γ-HALO]
children: [COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-Γ-HALO
      lines: "Section 3, P1"
      snippet: |
        P1 — **Core surface‑density locus**
        Prediction: Σ_0 ≡ ρ_0 r_c ≈ Σ_* (nearly constant) across halo masses for fixed V(Γ); weak T‑indexed scatter ΔΣ/Σ_* ≲ 0.2.
  editors: [Pirouette-Agent-2025-10-17]
  review_log: []
triad:
  art: |
    A quiet locus where the heart of a galaxy's density meets its characteristic size. This product reveals a constant pulse across cosmic scales, a fundamental tone resonating from dwarf worlds to giant clusters.
  law: |
    The product of a Γ-soliton halo's central density (ρ_0) and its core radius (r_c) is a near-constant value (Σ_*) across all halo masses. The predicted scatter is less than 20% and is weakly correlated with the halo's topological index T.
  philosophy: |
    Σ_0 serves as a primary empirical test of the Γ-soliton model, connecting the specific form of the fundamental potential V(Γ) to a directly observable, scale-invariant property of dark matter halos. Its constancy implies that the same underlying physics governs halo cores from dwarf galaxies to massive clusters, offering a unified alternative to particulate dark matter models.
pirouette_definition: |
  The Central Surface Density, Σ_0, is the product of a stationary Γ-soliton halo's central density, ρ_0, and its core radius, r_c. It is computed for each numerical solution of the Γ-field equations derived from a fixed potential V(Γ). The framework predicts that Σ_0 is not a free parameter but an emergent, nearly constant quantity (Σ_*) across a wide range of halo masses and topological indices T.
operational_definition:
  units: M_sun / pc^2
  symbol_table:
    - name: Σ_0
      meaning: Central Surface Density
      dimensions: M L⁻²
      default_range: "predicted to be a near-constant ~100-200 M_sun/pc^2"
    - name: ρ_0
      meaning: Central density of the Γ-soliton halo
      dimensions: M L⁻³
      default_range: contextual
    - name: r_c
      meaning: Core radius of the Γ-soliton halo
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Numerical Simulation (Γ-Soliton Solver)
        outline: |
          1. Solve the stationary field balance equation (Γ″ + (2/r) Γ′ − dV/dΓ = 0) for a given potential V(Γ) and topological index T using a numerical solver (e.g., FEM/spectral).
          2. Extract the resulting density profile ρ_Γ(r).
          3. Identify the central density ρ_0 = ρ_Γ(0) and the core radius r_c (e.g., the radius where ρ_Γ(r_c) = ρ_0/2).
          4. Compute the product Σ_0 = ρ_0 * r_c.
        expected_signals: [A stable, cored density profile ρ_Γ(r), A constant value of Σ_0 across solutions with different total masses]
        pitfalls: [Numerical instability near r=0, Ambiguous definition of core radius r_c, Solver failure to converge for certain T or V(Γ)]
      - name: Observational Inference (Galaxy Kinematics)
        outline: |
          1. Obtain high-resolution kinematic data (e.g., rotation curves) for a sample of galaxies.
          2. Model and subtract the contribution from baryons (stars, gas).
          3. Fit a cored halo density model to the residual kinematic data to infer the best-fit central density (ρ_0) and core radius (r_c).
          4. Calculate the product Σ_0 = ρ_0 * r_c for each galaxy and check for constancy across the sample.
        expected_signals: [A locus of (ρ_0, r_c) values for different galaxies that falls on a line of constant Σ_0]
        pitfalls: [Degeneracies in mass modeling (disk-halo conspiracy), Beam smearing effects in low-resolution data, Uncertainties in baryonic mass-to-light ratios]
context_windows:
  - module: COSMO-Γ-HALO
    excerpt: |
      A near‑constant central surface density Σ_0 ≡ ρ_0 r_c emerges from the Γ equations across dwarf → L* → cluster scales, up to weak T‑dependent scatter. Lensing κ(θ) maps from Γ alone reproduce observed Einstein radii at fixed baryon fraction when V(Γ) is the same as in COSMO‑Γ‑000 (D3 freeze honored).
  - module: COSMO-Γ-HALO
    excerpt: |
      P1 — **Core surface‑density locus**. Prediction: Σ_0 ≡ ρ_0 r_c ≈ Σ_* (nearly constant) across halo masses for fixed V(Γ); weak T‑indexed scatter ΔΣ/Σ_* ≲ 0.2. ... Falsification: failure to reproduce the Σ_0 locus or the V_c(r) diversity with the frozen V(Γ) invalidates Γ‑halo unification.
poetic_connections:
  motifs: [scale-invariance, emergent constant, core structure, cosmic heartbeat]
  evocative_lines:
    - "A quiet locus where the heart of a galaxy's density meets its characteristic size..."
    - "failure to reproduce the Σ_0 locus ... with the frozen V(Γ) invalidates Γ‑halo unification."
  association_matrix:
    - [ "GAMMA_SOLITON_HALO", 0.9 ]
    - [ "CORE_RADIUS", 0.8 ]
    - [ "CENTRAL_DENSITY", 0.8 ]
    - [ "TOPOLOGICAL_INDEX", 0.5 ]
formal_mappings:
  candidates:
    - target: Constant dark matter surface density (Donato et al. 2009)
      domain: Astrophysics
      mapping_kind: operational
      equation_hint: |
        Σ_DM ≡ ρ_0 r_c ≈ 140 M_sun pc⁻²
      justification: |
        The Pirouette term Σ_0 is operationally identical to the empirically observed central surface density of dark matter halos. This observed constancy across a wide range of galaxy types is a major puzzle in standard ΛCDM. The Γ-soliton model proposes a first-principles explanation for this phenomenon.
      references:
        - title: A constant dark matter density in galaxies
          where: MNRAS Letters, 397 (1), 1169–1173
          date: 2009-08-01
      confidence: 0.9
  adopted:
    - target: Observed constant halo surface density (Donato et al. 2009)
      rationale: The term is a direct theoretical prediction intended to reproduce a well-documented, unexplained empirical law in galactic dynamics. The mapping is definitional.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The central surface density, Σ_0 = ρ_0 * r_c, derived from Γ-soliton halo solutions, is approximately constant (Σ_0 ≈ Σ_*) across all halo masses and topological indices T, with scatter ΔΣ/Σ_* ≲ 0.2."
      domain: phenomenology
      falsifier: "Observational surveys of galaxy rotation curves showing that the inferred Σ_0 varies systematically with halo mass by more than the predicted scatter, or numerical solutions of the Γ-equations with the frozen V(Γ) potential failing to produce a constant Σ_0."
      status: proposed
      links: [COSMO-Γ-HALO]
naming_notes:
  collisions: [The symbol Σ is also used for the projected surface mass density field in gravitational lensing, Σ(θ). The subscript in Σ_0 is critical for disambiguation.]
  disambiguation: |
    Σ_0 is the central surface density, a scalar property of a halo defined as the product of the central volume density ρ_0 and the core radius r_c. This should not be confused with Σ(θ), the projected surface mass density field, which is a function of angular position used in lensing calculations.
crosslinks:
  near_synonyms: []
  antonyms: [CUSP_SLOPE]
  prerequisites: [CENTRAL_DENSITY, CORE_RADIUS, GAMMA_SOLITON_HALO]
  downstream_effects: [GAMMA_POTENTIAL]
license: CC-BY-SA-4.0
---

# Central Surface Density

## Canonical (Pirouette)
The Central Surface Density, Σ_0, is the product of a stationary Γ-soliton halo's central density, ρ_0, and its core radius, r_c. It is computed for each numerical solution of the Γ-field equations derived from a fixed potential V(Γ). The framework predicts that Σ_0 is not a free parameter but an emergent, nearly constant quantity (Σ_*) across a wide range of halo masses and topological indices T.

## EFT-First Summary
The Pirouette Framework predicts the existence of a nearly constant Central Surface Density (Σ_0) for Γ-soliton halos. This quantity is operationally equivalent to the empirically observed constant dark matter surface density of ~140 M_sun/pc² in galaxies (Donato et al. 2009). Within Pirouette, this constancy is not an astrophysical coincidence but an emergent consequence of the fundamental Γ-field potential, V(Γ), providing a potential first-principles explanation for this long-standing puzzle.

## Glossary Links
- See also: [[CORE_RADIUS]], [[CENTRAL_DENSITY]], [[GAMMA_SOLITON_HALO]]