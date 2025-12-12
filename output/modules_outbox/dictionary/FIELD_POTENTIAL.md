---
term: "Field Potential"
canonical_id: "FIELD_POTENTIAL"
symbol: "V(Γ)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Field Potential
canonical_id: FIELD_POTENTIAL
symbol: V(Γ)
aliases: [Γ Potential, Self-interaction Potential]
parents: [COSMO-Γ-000, COSMO-Γ-HALO]
children: [COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-001
      snippet: |
        (1) Γ″ + (2/r) Γ′ − dV/dΓ = 0  \  (stationary field balance)
        (3) ρ_Γ(r) ≡ ½(Γ′²) + V(Γ) − V(Γ_∞)   (subtract vacuum)
  editors: [AI Agent]
  review_log: []
triad:
  art: |
    The invisible landscape that guides the Γ-field, carving cosmic structures from its own self-interaction. It defines the energy cost of existing, shaping halos as stable valleys in a field of pure potential.
  law: |
    The Field Potential V(Γ) is a fixed scalar function whose gradient, dV/dΓ, provides the conservative force governing the dynamics and equilibrium configurations of the Γ-field. Its functional form is frozen by `COSMO-Γ-000` and must unitarily explain halo cores, rotation curves, and lensing across all mass scales.
  philosophy: |
    To replace particulate dark matter with a unified field theory, the Field Potential serves as the central 'genetic code.' By fixing V(Γ) *a priori*, the framework commits to a non-negotiable set of physical laws, making all subsequent halo predictions falsifiable consequences of this single entity, not results of multi-parameter tuning.
pirouette_definition: |
  The Field Potential, V(Γ), is a scalar function specifying the potential energy density of the Γ-field. Its gradient, dV/dΓ, acts as a source term in the Γ-field's equation of motion, governing self-interaction. Its value, V(Γ), contributes directly to the energy-momentum tensor and thus the total mass-energy density, ρ_Γ. The functional form of V(Γ) is fixed by the `COSMO-Γ-000` freeze and determines the existence, stability, and physical properties (core radius, central density) of Γ-soliton solutions.
operational_definition:
  units: Energy density (M L⁻¹ T⁻²)
  symbol_table:
    - name: V(Γ)
      meaning: Potential energy density of the Γ-field
      dimensions: M L⁻¹ T⁻²
      default_range: contextual, determined by `COSMO-Γ-000` freeze
    - name: Γ
      meaning: Γ-field amplitude
      dimensions: M¹/² L⁻¹/² T⁻¹
      default_range: contextual
    - name: Γ_∞
      meaning: Vacuum expectation value of Γ; the value at the minimum of V(Γ)
      dimensions: M¹/² L⁻¹/² T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Halo Profile Inversion
        outline: |
          Invert the coupled field equations from `COSMO-Γ-HALO` using high-resolution observational data for galactic rotation curves Vc(r) and gravitational lensing maps κ(θ). Constrain the underlying mass profile ρ_tot(r). After subtracting the baryonic component ρ_b(r), the resulting dark matter profile ρ_Γ(r) is used to find the functional form of V(Γ) that supports it as a stable soliton solution.
        expected_signals: [A consistent family of cored halo profiles fit by a single V(Γ), Emergence of the constant central surface density (Σ₀) locus]
        pitfalls: [Degeneracy with baryonic physics (feedback), Insufficient observational resolution to distinguish models, Assuming spherical symmetry when it is broken]
context_windows:
  - module: COSMO-001
    excerpt: |
      Derive core properties, rotation curves V_c(r), and lensing convergence κ(θ) from the same potential V(Γ) fixed in COSMO‑Γ‑000, without introducing particulate DM. Provide reproducible FEM/spectral pipelines and falsifiable core–scaling predictions.
  - module: COSMO-001
    excerpt: |
      Effective equations (Newtonian limit):
      (1) Γ″ + (2/r) Γ′ − dV/dΓ = 0  \  (stationary field balance)
      ...
      (3) ρ_Γ(r) ≡ ½(Γ′²) + V(Γ) − V(Γ_∞)   (subtract vacuum)
poetic_connections:
  motifs: [self-interaction, landscape, vacuum, confinement, structure formation]
  evocative_lines:
    - "...dV/dΓ = 0 (stationary field balance)"
    - "Asymptotic vacuum: Γ(r→∞) → Γ_∞ (minimum of V)"
  association_matrix:
    - [ "GAMMA_SOLITON_HALO", 0.9 ]
    - [ "ENERGY_DENSITY", 0.8 ]
    - [ "VACUUM_STATE", 0.7 ]
formal_mappings:
  candidates:
    - target: V(φ) (Scalar field potential)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L = ½(∂μφ)² − V(φ)
      justification: |
        V(Γ) is mathematically identical to the potential term for a real scalar field in classical or quantum field theory. It governs self-interactions (e.g., via a λΓ⁴ term) and mass (via a m²Γ² term), and its minima define the vacuum states. The equation of motion for Γ is the static, spherically symmetric Klein-Gordon equation with V(Γ) as the potential.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter 4, Peskin & Schroeder
          date: 1995-10-01
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A single, fixed V(Γ) from `COSMO-Γ-000` must simultaneously reproduce the near-constant core surface density (Σ_0) locus across halo masses and the observed diversity of inner rotation curve slopes."
      domain: phenomenology
      falsifier: "Observational failure to reproduce the Σ_0 locus or V_c(r) diversity with the frozen V(Γ). If different potentials are required for different halo types, the unification claim is falsified."
      status: proposed
      links: [COSMO-Γ-HALO]
naming_notes:
  collisions: [V is also used for volume and electrostatic potential; context and the argument V(Γ) are sufficient to distinguish.]
  disambiguation: |
    Distinguish from the gravitational potential Φ. V(Γ) is the potential of the Γ-field itself, which then *sources* the gravitational potential Φ via its contribution to the energy density ρ_Γ. V(Γ) is an input to the theory; Φ is a resulting output.
crosslinks:
  near_synonyms: []
  antonyms: [KINETIC_ENERGY_DENSITY]
  prerequisites: [GAMMA_FIELD]
  downstream_effects: [GAMMA_SOLITON_HALO, ENERGY_DENSITY]
license: CC-BY-SA-4.0
---

# Field Potential

## Canonical (Pirouette)
The Field Potential, V(Γ), is a scalar function specifying the potential energy density of the Γ-field. Its gradient, dV/dΓ, acts as a source term in the Γ-field's equation of motion, governing self-interaction. Its value, V(Γ), contributes directly to the energy-momentum tensor and thus the total mass-energy density, ρ_Γ. The functional form of V(Γ) is fixed by the `COSMO-Γ-000` freeze and determines the existence, stability, and physical properties (core radius, central density) of Γ-soliton solutions.

## EFT-First Summary
In the language of Effective Field Theory (EFT), V(Γ) is the self-interaction potential for a real scalar field, analogous to the `V(φ)` term in a standard Lagrangian `L = ½(∂μφ)² − V(φ)`. It encodes the field's mass and any non-linear self-couplings. The Pirouette Framework constrains this potential using cosmological data (`COSMO-Γ-000`) and then tests it against astrophysical observations of galactic halos, demanding that one function explains phenomena across many scales.

## Glossary Links
- See also: GAMMA_FIELD, GAMMA_SOLITON_HALO, ENERGY_DENSITY