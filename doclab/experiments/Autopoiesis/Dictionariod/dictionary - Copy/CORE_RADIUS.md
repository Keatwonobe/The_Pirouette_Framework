---
term: "Core Radius"
canonical_id: "CORE_RADIUS"
symbol: "r_c"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Core Radius
canonical_id: CORE_RADIUS
symbol: r_c
aliases: []
parents: [COSMO-001]
children: [COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-001
      lines: "Section 2"
      snippet: |
        Outputs (per solution):
        • Core radius r_c (e.g., radius where ρ_Γ drops to ρ_0/2)
        • Central density ρ_0 = ρ_Γ(0)
        • Surface-density product Σ_0 = ρ_0 r_c
  editors: [system]
  review_log: []
triad:
  art: |
    The core radius marks the edge of a halo's quiet heart, a calm, flat region of spacetime from which the larger gravitational storm gathers. It is the scale of the soliton's stillness before its influence fades into the cosmos.
  law: |
    The core radius `r_c` is the radial distance at which the Γ-field mass density `ρ_Γ(r)` drops to one-half of its central value `ρ_0`. It combines with `ρ_0` to form the central surface density `Σ_0 = ρ_0 r_c`, a quantity predicted to be nearly constant across halo masses.
  philosophy: |
    The existence of a non-zero core radius is a primary physical consequence of modeling dark matter as a Γ-soliton. It provides a first-principles explanation for the observed cores in galactic halos, replacing phenomenological models or sub-grid feedback with a fundamental length scale derived from the potential `V(Γ)`.
pirouette_definition: |
  The characteristic length scale of the central, approximately constant-density region of a stationary Γ-soliton halo. Operationally, it is the half-density radius, defined as the radius `r` where the Γ-field's effective mass density equals half its value at the center: `ρ_Γ(r_c) = ½ ρ_Γ(0)`. The core radius is a direct output of the numerical solution to the stationary field balance equation for a given topological index `T`.
operational_definition:
  units: kiloparsecs (kpc)
  symbol_table:
    - name: r_c
      meaning: Core Radius
      dimensions: L
      default_range: 0.1 – 50 kpc
    - name: ρ_Γ(r)
      meaning: Mass density of the Γ-field at radius r
      dimensions: M L⁻³
      default_range: contextual
    - name: ρ_0
      meaning: Central mass density of the Γ-field, ρ_Γ(0)
      dimensions: M L⁻³
      default_range: contextual
  measurement:
    procedures:
      - name: Numerical Solution and Profile Analysis
        outline: |
          1.  For a given Γ-field potential `V(Γ)` and baryon profile `ρ_b(r)`, numerically solve the stationary field equation `Γ″ + (2/r) Γ′ − dV/dΓ = 0` with boundary conditions `Γ′(0)=0` and `Γ(∞)→Γ_∞`.
          2.  Calculate the resulting Γ-field mass density profile `ρ_Γ(r) ≡ ½(Γ′²) + V(Γ) − V(Γ_∞)`.
          3.  Identify the central density `ρ_0 = ρ_Γ(0)`.
          4.  The core radius `r_c` is the value of `r` for which `ρ_Γ(r) = ρ_0 / 2`.
        expected_signals:
          - A `halo_result.json` artifact containing a floating-point value for `"rc"`.
          - A rotation curve `Vc_profile` that rises linearly for `r ≪ r_c`.
        pitfalls:
          - Insufficient numerical resolution near `r=0` can artificially flatten or sharpen the core, leading to an inaccurate `r_c` measurement.
          - Failure of the nonlinear solver to converge to the correct physical solution for a given topological index `T`.
context_windows:
  - module: COSMO-001
    excerpt: |
      A family of stationary solutions Γ_T(r) exists for allowed T, generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers and NFW-like outer slopes. A near-constant central surface density Σ_0 ≡ ρ_0 r_c emerges from the Γ equations across dwarf → L* → cluster scales, up to weak T-dependent scatter.
  - module: COSMO-001
    excerpt: |
      Outputs (per solution):
      • Core radius r_c (e.g., radius where ρ_Γ drops to ρ_0/2)
      • Central density ρ_0 = ρ_Γ(0)
      • Surface-density product Σ_0 = ρ_0 r_c
      • V_c(r) curve; maximum V_max and radius r_max
poetic_connections:
  motifs: [soliton heart, flat potential well, still center]
  evocative_lines:
    - "A family of stationary solutions... with cored centers."
    - "reproduce dwarf diversity without stochastic sub-grid feedback."
  association_matrix:
    - [ "CENTRAL_DENSITY", 0.9 ]
    - [ "CENTRAL_SURFACE_DENSITY", 1.0 ]
    - [ "TOPOLOGICAL_INDEX", 0.7 ]
formal_mappings:
  candidates:
    - target: Burkert Profile Core Radius (r₀)
      domain: CM
      mapping_kind: operational
      equation_hint: |
        ρ_Burkert(r) = ρ₀ / ((1 + r/r₀)(1 + (r/r₀)²))
      justification: |
        The Γ-soliton profile is well-approximated in its inner region by the empirical Burkert profile, widely used to fit observed rotation curves of cored galaxies. The Pirouette term `r_c` is the physically-derived analog to the phenomenological parameter `r₀` in the Burkert model.
      references:
        - title: A Universal Density Profile from Hierarchical Clustering
          where: The Astrophysical Journal, 447, L25
          date: 1995-07-01
      confidence: 0.9
  adopted:
    - target: Burkert Profile Core Radius (r₀)
      rationale: This mapping provides the most direct and testable link between the Pirouette Framework's theoretical predictions and standard observational analyses of galactic rotation curves. It positions the Γ-halo model as a fundamental explanation for an established phenomenological model.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The core radius `r_c` and central density `ρ_0` combine to form a surface density `Σ_0 = ρ_0 r_c` that is nearly constant across many decades of halo mass."
      domain: phenomenology
      falsifier: "Observational data from a large sample of galaxies shows `Σ_0` varies systematically with halo mass beyond the predicted weak, T-indexed scatter."
      status: proposed
      links: [COSMO-001]
    - statement: "Baryonic compression (adiabatic contraction) modifies `r_c` along a predictable, one-parameter track determined by the Γ-field's potential."
      domain: phenomenology
      falsifier: "The observed correlation between stellar surface density and halo core radius does not follow the unique track predicted by the framework."
      status: proposed
      links: [COSMO-001]
naming_notes:
  collisions: [The symbol `r_c` is used widely in astrophysics for various scales, including the core radius of globular clusters, the critical radius for accretion, and more. Context is critical.]
  disambiguation: |
    Within Pirouette's cosmological modules, `r_c` refers exclusively to the core radius of the Γ-field (dark matter) halo. It should not be confused with the baryonic scale length (e.g., `r_b` from the config), the half-light radius of a galaxy (`r_e`), or the scale radius of a cuspy NFW profile (`r_s`).
crosslinks:
  near_synonyms: []
  antonyms: [NFW_SCALE_RADIUS]
  prerequisites: [CENTRAL_DENSITY, GAMMA_POTENTIAL]
  downstream_effects: [CENTRAL_SURFACE_DENSITY, ROTATION_CURVE]
license: CC-BY-SA-4.0
---

# Core Radius

## Canonical (Pirouette)
The characteristic length scale of the central, approximately constant-density region of a stationary Γ-soliton halo. Operationally, it is the half-density radius, defined as the radius `r` where the Γ-field's effective mass density equals half its value at the center: `ρ_Γ(r_c) = ½ ρ_Γ(0)`. The core radius is a direct output of the numerical solution to the stationary field balance equation for a given topological index `T`.

## EFT-First Summary
The Γ-soliton's Core Radius `r_c` provides a first-principles, field-theoretic origin for the empirically successful cored dark matter profiles observed in galaxies. It is the direct analog to the core radius `r₀` in the phenomenological Burkert profile. Instead of being a free parameter fit to data, its value and scaling behavior (e.g., the constant `ρ₀ r_c` relation) are falsifiable predictions derived from the underlying Γ-field potential `V(Γ)`.

## Glossary Links
- See also: [Central Density](<./CENTRAL_DENSITY.md>), [Central Surface Density](<./CENTRAL_SURFACE_DENSITY.md>)