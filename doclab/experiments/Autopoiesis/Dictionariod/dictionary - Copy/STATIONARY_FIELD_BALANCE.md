---
term: "Stationary Field Balance"
canonical_id: "STATIONARY_FIELD_BALANCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Stationary Field Balance
canonical_id: STATIONARY_FIELD_BALANCE
symbol:
aliases: [Γ-soliton equation]
parents: [COSMO-001, MATH-018, MATH-019, MATH-020, COSMO-Γ-000]
children: [COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-001
      lines: "L21"
      snippet: |
        (1) Γ″ + (2/r) Γ′ − dV/dΓ = 0  \  (stationary field balance)
  editors: [AetherpediaBot]
  review_log: []
triad:
  art: |
    A star held in shape not by gravity but by its own inner light. It is the silent equilibrium where a field's will to expand is perfectly checked by the pull of its own potential, carving a stable form out of the vacuum.
  law: |
    For a given potential V(Γ), there exists a family of spherically symmetric, non-trivial, finite-energy field profiles Γ(r) that solve the balance equation. These solutions map directly to astrophysical halo properties (cores, rotation curves), and if this mapping fails to match observation, the underlying potential V(Γ) is falsified.
  philosophy: |
    This equation replaces the statistical mechanics of countless dark matter particles with the fluid dynamics of a single, continuous field. It asserts that cosmic structure is not an accident of particle aggregation but an inevitable consequence of field self-interaction, seeking its lowest energy state. Its purpose is to derive macroscopic structure from microscopic laws without particulate intermediaries.
pirouette_definition: |
  The Stationary Field Balance is a second-order nonlinear ordinary differential equation that governs the radial profile, Γ(r), of a static, spherically symmetric scalar field condensate (Γ-soliton). It defines equilibrium by balancing the field's gradient energy (first and second derivative terms), which resists spatial variation, against the force exerted by its self-interaction potential, dV/dΓ. Its solutions, subject to boundary conditions of core regularity and asymptotic decay to a vacuum value, represent the structure of non-particulate dark matter halos.
operational_definition:
  units: The equation relates terms with units of force per unit field strength, typically expressed in a system where energy density and pressure are interchangeable.
  symbol_table:
    - name: Γ(r)
      meaning: Scalar field amplitude as a function of radius r.
      dimensions: M^1/2 L^1/2 T^-1 (derived from ρ_Γ ~ (Γ')²)
      default_range: [Γ_∞, Γ(0)]; context-dependent.
    - name: r
      meaning: Radial coordinate.
      dimensions: L
      default_range: [0, R_max]
    - name: V(Γ)
      meaning: The self-interaction potential of the Γ field.
      dimensions: M L^-1 T^-2 (energy density)
      default_range: Fixed by `COSMO-Γ-000` freeze.
    - name: ′
      meaning: Derivative with respect to radius, d/dr.
      dimensions: L^-1
      default_range: n/a
  measurement:
    procedures:
      - name: Indirect Inference via Halo Observation
        outline: |
          1. Fix the potential V(Γ) according to the `COSMO-Γ-000` freeze.
          2. Numerically solve the Stationary Field Balance equation for Γ(r) using a spectral or FEM solver with boundary conditions Γ'(0)=0 and Γ(∞)→Γ_∞.
          3. From the solution Γ(r), compute the effective dark matter density ρ_Γ(r) = ½(Γ′²) + V(Γ) − V(Γ_∞).
          4. Compute observable quantities from ρ_Γ(r) + ρ_b(r), such as the rotation curve V_c(r) and the lensing convergence κ(θ).
          5. Compare the computed observables against astronomical data (e.g., SPARC galaxy rotation curves, cluster lensing maps from Hubble/JWST). A match validates the V(Γ) and the balance equation as a model for halos.
        expected_signals: [Cored density profiles, a nearly constant core surface density (Σ_0) across a wide range of halo masses, specific V_c(r) shapes.]
        pitfalls: [Numerical solver convergence failure, degeneracy with baryonic physics (e.g., feedback, adiabatic contraction), incorrect boundary conditions applied at finite radius.]
context_windows:
  - module: COSMO-001
    excerpt: |
      A family of stationary solutions Γ_T(r) exists for allowed T, generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers and NFW‑like outer slopes. A near‑constant central surface density Σ_0 ≡ ρ_0 r_c emerges from the Γ equations across dwarf → L* → cluster scales, up to weak T‑dependent scatter.
  - module: COSMO-001
    excerpt: |
      Effective equations (Newtonian limit):
      (1) Γ″ + (2/r) Γ′ − dV/dΓ = 0  \  (stationary field balance)
      (2) ∇²Φ = 4πG (ρ_b(r) + ρ_Γ(r))
      (3) ρ_Γ(r) ≡ ½(Γ′²) + V(Γ) − V(Γ_∞)   (subtract vacuum)
poetic_connections:
  motifs: [cosmic equilibrium, field pressure, soliton core, structural integrity]
  evocative_lines:
    - "cored centers and NFW-like outer slopes."
    - "Lensing mass without particulate DM."
  association_matrix:
    - [ "GAMMA_SOLITON_HALO", 0.9 ]
    - [ "CORE_SURFACE_DENSITY", 0.7 ]
    - [ "FIELD_POTENTIAL_V_GAMMA", 0.8 ]
formal_mappings:
  candidates:
    - target: Static scalar field equation of motion
      domain: GR|EFT
      mapping_kind: mathematical
      equation_hint: |
        In a static, spherically symmetric metric, the Klein-Gordon equation ∇_μ∇^μ φ - m²φ = 0 becomes φ'' + (2/r)φ' - m²φ = 0, a linear version of the balance equation. The dV/dΓ term generalizes this to a nonlinear potential.
      justification: |
        This is the Euler-Lagrange equation for a static, spherically symmetric scalar field derived from a standard Lagrangian L = ½(∂_μΓ)² - V(Γ). The two derivative terms represent the kinetic/gradient energy, while dV/dΓ is the force from the potential. It is a direct analogue used in scalar field dark matter models.
      references:
        - title: "Scalar Field Dark Matter"
          where: "Living Reviews in Relativity, 24(1), 1"
          date: 2021-01-07
      confidence: 0.95
  adopted:
    - target: Static scalar field equation of motion
      rationale: The mapping is mathematically direct and serves the same physical purpose of defining a stable, localized field configuration.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The core surface density, Σ_0 ≡ ρ_0 r_c, derived from solutions to the Stationary Field Balance, is nearly constant (Σ_0 ≈ Σ_*) across all halo mass scales for a fixed potential V(Γ)."
      domain: phenomenology
      falsifier: "Observational data shows a strong, systematic scaling of Σ_0 with halo mass, or the value of Σ_* predicted by the equation for the `COSMO-Γ-000` potential V(Γ) does not match the observed value."
      status: proposed
      links: [COSMO-001]
naming_notes:
  collisions: [The symbol Γ is heavily overloaded in physics, representing the Gamma function, Christoffel symbols in GR, and decay widths in particle physics. Context is critical.]
  disambiguation: |
    Within Pirouette, this equation is distinct from any dynamic or cosmological evolution equation for Γ. It specifically describes the *static*, time-independent structure of a bound halo, not the field's behavior during inflation or structure formation.
crosslinks:
  near_synonyms: [GAMMA_SOLITON_EQUATION]
  antonyms: []
  prerequisites: [GAMMA_FIELD, FIELD_POTENTIAL_V_GAMMA]
  downstream_effects: [CORE_SURFACE_DENSITY, ROTATION_CURVE, LENSING_CONVERGENCE]
license: CC-BY-SA-4.0
---

# Stationary Field Balance

## Canonical (Pirouette)
The Stationary Field Balance is a second-order nonlinear ordinary differential equation that governs the radial profile, Γ(r), of a static, spherically symmetric scalar field condensate (Γ-soliton). It defines equilibrium by balancing the field's gradient energy (first and second derivative terms), which resists spatial variation, against the force exerted by its self-interaction potential, dV/dΓ. Its solutions, subject to boundary conditions of core regularity and asymptotic decay to a vacuum value, represent the structure of non-particulate dark matter halos.

## EFT-First Summary
In the language of effective field theory, the Stationary Field Balance is the equation of motion for a static, spherically symmetric scalar field, `Γ`. It is derived from a canonical Lagrangian `L = ½(∂_μΓ)² - V(Γ)`. The equation `Γ″ + (2/r) Γ′ = dV/dΓ` sets the kinetic/gradient energy terms against the force from the potential `V(Γ)`. Its solutions are non-topological solitons, or Q-balls, whose profiles are interpreted as the density distributions of galactic halos, providing a direct link between a fundamental scalar potential and astrophysical observables.

## Glossary Links
- See also: [GAMMA_SOLITON_HALO](...), [CORE_SURFACE_DENSITY](...), [FIELD_POTENTIAL_V_GAMMA](...)