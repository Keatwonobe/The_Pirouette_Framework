---
term: "Constant surface-density locus"
canonical_id: "CONSTANT_SURFACE_DENSITY_LOCUS"
symbol: "Σ_0"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SECT-001"]
---

---
term: Constant surface-density locus
canonical_id: CONSTANT_SURFACE_DENSITY_LOCUS
symbol: Σ_0
aliases: ["Σ_0 locus", "Universal surface density"]
parents: [SECT-001]
children: [SECT-Γ-A-HALO]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SECT-001
      snippet: |
        Core predictions:
        • **Constant surface-density locus** Σ_0 ≡ ρ_0 r_c emerges from ξ and σ: Σ_0 ≈ C(α,β,σ,m_H) nearly mass-independent (matches COSMO-Γ-HALO P1).
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    Like a water droplet on a leaf, every dark matter halo balances its own weight against a universal surface tension. This balance dictates that a small, dense halo and a large, diffuse one maintain the same pressure against the vacuum, a constant footprint across cosmic scales.
  law: |
    The product of a dark matter halo's central core density (ρ₀) and its core radius (r_c) is a constant, Σ₀ = ρ₀ r_c. Its value, C(α,β,σ,m_H), is predicted to be nearly independent of total halo mass, and the measured scatter in this relation directly tests the superfluid's equation of state.
  philosophy: |
    The Σ₀ locus provides a direct, falsifiable bridge between the microscopic parameters of the Superfluid Pressuron EFT (α,β,σ,m_H) and a macroscopic, observable property of galactic halos. Its universality would imply that halo structure is not a stochastic outcome of hierarchical merging, but an equilibrium state governed by a fundamental equation of state, akin to the mass-radius relation for stars.
pirouette_definition: |
  A predicted, nearly mass-independent relationship for Superfluid Pressuron halos where the product of the central core density, ρ₀, and the core radius, r_c, equals a constant Σ₀. This constant is a derived quantity determined by the fundamental P(X) parameters (α,β), surface tension (σ), and pressuron mass (m_H). It arises from the equilibrium between gravitational self-attraction and the effective pressure gradient, including quantum pressure from the healing length (ξ) and interface effects from surface tension (σ).
operational_definition:
  units: M L⁻² (typically M_sun pc⁻²)
  symbol_table:
    - name: Σ₀
      meaning: Constant surface-density locus
      dimensions: M L⁻²
      default_range: contextual (predicted to be ~100-200 M_sun pc⁻²)
    - name: ρ₀
      meaning: Halo central core density
      dimensions: M L⁻³
      default_range: contextual
    - name: r_c
      meaning: Halo core radius
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Halo Kinematic Profile Fitting
        outline: |
          1. Obtain high-resolution kinematic data (e.g., stellar velocities, HI rotation curves) for a diverse sample of dark matter-dominated galaxies.
          2. Fit the kinematic data with a halo model that includes a cored density profile derived from the superfluid equilibrium equations.
          3. Extract the best-fit parameters for central density (ρ₀) and core radius (r_c) for each halo.
          4. Plot the product Σ₀ = ρ₀ r_c against total halo mass.
        expected_signals: ["A tight, mass-independent distribution of Σ₀ values.", "A slope statistically consistent with zero in a log(Σ₀) vs. log(M_halo) plot."]
        pitfalls: ["Baryonic feedback effects contaminating the central potential and altering ρ₀ or r_c.", "Insufficient kinematic resolution to resolve the core.", "Systematic errors in mass-to-light ratio assumptions for the stellar component."]
context_windows:
  - module: SECT-001
    excerpt: |
      Static spherical equilibrium with gravitational potential Φ:
      • Euler: ∇p = −ρ ∇Φ  → dP/dn · dn/dr = −ρ dΦ/dr.
      • With P(X)=α X^{1+β} and X≈μ−Φ−(∇θ)^2/2m_H, the core solves a **Lane–Emden‑like** equation with finite central pressure.
      Core predictions:
      • **Constant surface‑density locus** Σ_0 ≡ ρ_0 r_c emerges from ξ and σ: Σ_0 ≈ C(α,β,σ,m_H) nearly mass‑independent (matches COSMO‑Γ‑HALO P1).
  - module: SECT-001
    excerpt: |
      Section 6 — Distinctive, Falsifiable Signatures
      A) **Halo cores with universal Σ_0** and **vortex spectra** in fast rotators (IFU kinematics; stellar streams).
      ...
      Section 8 — Preregistered Targets (OOS)
      • Σ_0 locus slope ± scatter across dwarfs→clusters.
poetic_connections:
  motifs: [surface tension, equilibrium, universal scale, cosmic droplet]
  evocative_lines:
    - "tension to space… surface tension against gravity…"
    - "Constant surface-density locus Σ_0 ≡ ρ_0 r_c emerges from ξ and σ"
  association_matrix:
    - [ "SURFACE_TENSION", 0.9 ]
    - [ "HEALING_LENGTH", 0.8 ]
    - [ "HALO_CORE", 0.9 ]
formal_mappings:
  candidates:
    - target: Central surface density of dark matter halos
      domain: Astrophysics
      mapping_kind: operational
      equation_hint: |
        Σ_obs ≡ ρ_0 r_c ≈ 140 M_sun pc⁻²
      justification: |
        In observational astrophysics, the product of core density and core radius is a widely measured quantity found to be surprisingly constant across a wide range of galaxy types. The Pirouette Σ₀ is a theoretical prediction for this observed phenomenon, grounding it in the microphysics of the superfluid model.
      references:
        - title: A constant dark matter halo surface density in galaxies
          where: "MNRAS Letters, 397 (1), 1169–1173 (Donato et al.)"
          date: 2009-08-01
      confidence: 0.95
  adopted:
    - target: Central surface density of dark matter halos
      rationale: This is the direct observational counterpart. The Pirouette framework provides a specific physical mechanism for its existence and constancy.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Σ₀ is constant (slope of log(Σ₀) vs log(M_halo) is zero) across a wide range of halo masses, from dwarfs (10⁷ M_sun) to clusters (10¹⁵ M_sun)."
      domain: phenomenology
      falsifier: "Observational data shows a statistically significant, non-zero slope for the Σ₀-M_halo relation, or the scatter is much larger than predicted by simulations incorporating baryonic effects within the superfluid model."
      status: proposed
      links: [SECT-001]
naming_notes:
  collisions: ["Σ is a common symbol for surface density in many fields (e.g., stellar disks, lensing). Subscript 0 denotes its constant, foundational nature in this context."]
  disambiguation: |
    Distinguish from Σ, the generic symbol for a variable surface density, and from Σ_crit, the critical surface density in gravitational lensing. Σ₀ refers specifically to the product ρ₀ r_c and its predicted mass-invariance.
crosslinks:
  near_synonyms: []
  antonyms: [CUSP_DENSITY_PROFILE]
  prerequisites: [SURFACE_TENSION, HEALING_LENGTH, P_OF_X_EFT]
  downstream_effects: [HALO_CORE_PROFILE, GALAXY_ROTATION_CURVE]
license: CC-BY-SA-4.0
---