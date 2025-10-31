---
term: "Cored Center"
canonical_id: "CORED_CENTER"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Cored Center
canonical_id: CORED_CENTER
symbol: 
aliases: [Flat Core, Solitonic Core, Γ-Core]
parents: [COSMO-001]
children: [COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-001
      snippet: |
        A family of stationary solutions Γ_T(r) exists for allowed T, generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers and NFW‑like outer slopes.
  editors: [Agent: Pirouette-Dict-Gen]
  review_log: []
triad:
  art: |
    Where gravity would forge a singularity, the Γ-field lays down a tranquil floor, a stable heart from which the halo's vast architecture extends.
  law: |
    The product of a halo's central density (ρ₀) and core radius (r_c) is a near-constant (Σ₀ ≈ Σ_*) across all mass scales, from dwarf galaxies to clusters, with only weak, predictable scatter indexed by topology T.
  philosophy: |
    A Cored Center resolves the tension between standard collisionless dark matter predictions (cusps) and galactic observations (cores) by positing a fundamental field pressure, replacing stochastic baryonic feedback with deterministic, geometric self-regulation.
pirouette_definition: |
  A Cored Center is a region of finite, near-constant mass density (ρ ≈ ρ₀) at the geometric center (r→0) of a Γ-soliton halo. It is a necessary consequence of the regularity boundary condition Γ′(0)=0 for the stationary field solution, which forces the kinetic energy density term (½Γ′²) to vanish at the origin. The core is operationally characterized by its central density ρ₀ and core radius r_c.
operational_definition:
  units: ρ₀ in kg⋅m⁻³, r_c in m, Σ₀ in kg⋅m⁻²
  symbol_table:
    - name: ρ_Γ(r)
      meaning: Mass-energy density of the Γ-field as a function of radius.
      dimensions: M L⁻³
      default_range: 10⁻²⁴ – 10⁻²⁰ kg⋅m⁻³
    - name: ρ₀
      meaning: Central density, defined as ρ_Γ(r=0).
      dimensions: M L⁻³
      default_range: contextual
    - name: r_c
      meaning: Core radius, defined as the radius where ρ_Γ(r_c) = ρ₀/2.
      dimensions: L
      default_range: 0.1 – 10 kpc
    - name: Σ₀
      meaning: Central surface density product, defined as ρ₀⋅r_c.
      dimensions: M L⁻²
      default_range: ~10² M_☉⋅pc⁻²
  measurement:
    procedures:
      - name: Density Profile Inference from Kinematics or Lensing
        outline: |
          1. Observe galactic rotation curves V_c(r) via stellar/gas kinematics, or gravitational lensing maps κ(θ) for clusters.
          2. Invert the mass relation M(<r) = r⋅V_c(r)²/G to derive the total enclosed mass profile, and differentiate to find the total density ρ_tot(r).
          3. Model and subtract baryonic components (ρ_b) to isolate the halo density ρ_Γ(r) = ρ_tot(r) − ρ_b(r).
          4. Fit the inner profile (r ≪ r_vir) to determine the central density ρ₀ = ρ_Γ(0) and the core radius r_c (radius where ρ_Γ(r_c) = ρ₀/2).
        expected_signals: [A flat or shallow inner slope (α ≈ 0) in the log ρ – log r plot, A near-constant central surface density Σ₀ across a population of halos.]
        pitfalls: [Baryonic contamination and uncertainty in stellar mass-to-light ratios, Non-spherical halo geometry, Observational resolution limits smearing the central region.]
context_windows:
  - module: COSMO-001
    excerpt: |
      A family of stationary solutions Γ_T(r) exists for allowed T, generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers and NFW‑like outer slopes. A near‑constant central surface density Σ_0 ≡ ρ_0 r_c emerges from the Γ equations across dwarf → L* → cluster scales, up to weak T‑dependent scatter.
  - module: COSMO-001
    excerpt: |
      Variation of T and baryon compression leads to a controlled family of inner slopes; reproduce dwarf diversity without stochastic sub‑grid feedback. Adiabatic contraction modifies r_c and V_max along a one‑parameter track predictable from Γ’s equation; publish a single‑track map relating stellar surface density to halo r_c.
poetic_connections:
  motifs: [Stillness, Foundation, Plateau, Regularity]
  evocative_lines:
    - "Core regularity: Γ′(0)=0, finite Γ(0)"
    - "reproduce dwarf diversity without stochastic sub‑grid feedback"
  association_matrix:
    - [ "GAMMA_SOLITON", 0.9 ]
    - [ "CUSP_PROFILE", -0.9 ]
formal_mappings:
  candidates:
    - target: Soliton core (Fuzzy/Wave Dark Matter)
      domain: Cosmology|EFT
      mapping_kind: mathematical|conceptual
      equation_hint: |
        ∇²Φ = 4πGρ  ;  (ℏ²/2m)∇²√ρ + (V_eff − Φ)√ρ = 0  (Gross-Pitaevskii-Poisson)
        Γ″ + (2/r)Γ′ − dV/dΓ = 0  ;  ∇²Φ = 4πG(ρ_b + ρ_Γ)  (Pirouette)
      justification: |
        The Γ-soliton is a classical scalar field condensate analogous to the ground state of a Bose-Einstein Condensate (BEC) in ultralight axion or Fuzzy Dark Matter (FDM) models. In both frameworks, a gradient energy or effective quantum pressure counteracts gravity, preventing cusp formation and creating a stable, cored soliton at the halo's center. The governing equations are mathematically cognate.
      references:
        - title: Ultralight scalars as cosmological dark matter
          where: Physical Review D, 95(4), 043541
          date: 2017-02-28
      confidence: 0.9
  adopted:
    - target: Soliton core (Fuzzy/Wave Dark Matter)
      rationale: The mathematical and physical origin of the core—a balance between self-gravity and a field's self-interaction or gradient energy—is identical. This provides the most direct theoretical anchor.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The product of the central density and core radius, Σ₀ ≡ ρ₀r_c, is a near-constant across halo masses spanning at least five decades (from dwarf galaxies to clusters)."
      domain: phenomenology
      falsifier: "Observational data shows a strong, systematic trend of Σ₀ with halo mass, or scatter significantly exceeding the predicted ΔΣ/Σ_* ≲ 0.2, that cannot be accounted for by baryonic effects or variation in the topological index T."
      status: proposed
      links: [COSMO-001]
naming_notes:
  collisions: []
  disambiguation: |
    This term refers specifically to the central region of a dark matter halo's density profile. It should not be confused with the baryonic "core" of a galaxy (e.g., the stellar bulge or active nucleus) or the core of a star or planet.
crosslinks:
  near_synonyms: []
  antonyms: [CUSP_PROFILE]
  prerequisites: [GAMMA_SOLITON, COSMO-Γ-000]
  downstream_effects: [DWARF_GALAXY_DIVERSITY, ROTATION_CURVE_SHAPE]
license: CC-BY-SA-4.0
---