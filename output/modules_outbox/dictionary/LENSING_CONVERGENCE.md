---
term: "Lensing Convergence"
canonical_id: "LENSING_CONVERGENCE"
symbol: "κ(θ)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Lensing Convergence
canonical_id: LENSING_CONVERGENCE
symbol: κ(θ)
aliases: [Convergence]
parents: [COSMO-Γ-HALO]
children: [COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-Γ-HALO
      lines: "Section 1"
      snippet: |
        κ(θ) = Σ(θ)/Σ_crit with Σ(θ)=∫ ρ_tot dl;  Σ_crit = (c²/4πG) (D_s/(D_d D*{ds}))
  editors: [system]
  review_log: []
triad:
  art: |
    A lens forged from gravity's well, it magnifies and distorts the distant cosmos, revealing the unseen architecture of spacetime shaped by a halo's core.
  law: |
    The lensing convergence κ(θ) is a non-local projection of the total mass density ρ_Γ + ρ_b, uniquely determined by a stationary Γ-soliton solution and a specified baryon profile, without free parameters beyond the fixed potential V(Γ).
  philosophy: |
    κ(θ) serves as a primary observational bridge, translating the abstract dynamics of the Γ-soliton into a measurable distortion of background light. Its successful prediction validates the Γ-condensate model as a physical dark matter alternative, replacing particulate hypotheses with field-theoretic structure.
pirouette_definition: |
  The Lensing Convergence, κ(θ), is a dimensionless scalar field on the observer's sky plane that quantifies the local magnification of light due to a foreground mass distribution. Within the Γ-Soliton Halo model, it is calculated as the ratio of the total projected surface mass density, Σ(θ), to the critical surface mass density, Σ_crit. Σ(θ) is derived by integrating the mass density of the Γ-field (ρ_Γ) and baryons (ρ_b) along the line of sight. Σ_crit is a geometric factor dependent on the angular diameter distances to the lens (D_d), the source (D_s), and between them (D_ds).
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: κ(θ)
      meaning: Lensing Convergence at angular position θ
      dimensions: dimensionless
      default_range: "[0, 5]"
    - name: Σ(θ)
      meaning: Projected surface mass density
      dimensions: M L⁻²
      default_range: contextual
    - name: Σ_crit
      meaning: Critical surface mass density for lensing
      dimensions: M L⁻²
      default_range: contextual
    - name: ρ_tot
      meaning: Total mass density (ρ_Γ + ρ_b)
      dimensions: M L⁻³
      default_range: contextual
    - name: θ
      meaning: Angular position on the sky
      dimensions: dimensionless
      default_range: contextual
    - name: D_d, D_s, D_ds
      meaning: Angular diameter distances to lens, source, and between them
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Weak/Strong Lensing Inversion
        outline: |
          Observe the statistical distortion (shear) of a large sample of background galaxies behind a foreground halo (weak lensing), or the positions and magnifications of multiple images of a single background source (strong lensing). Invert the shear field or model the multiple images to reconstruct the projected mass distribution, Σ(θ). Normalize by the calculated Σ_crit for the system's redshift geometry to obtain a map of κ(θ).
        expected_signals: [A centrally peaked κ(θ) profile, Einstein rings/arcs where κ(θ) ≈ 1]
        pitfalls: [Contamination by foreground/background structures (mass-sheet degeneracy), uncertainty in source redshifts, baryon-dark matter modeling degeneracy]
context_windows:
  - module: COSMO-Γ-HALO
    excerpt: |
      Lensing κ(θ) maps from Γ alone reproduce observed Einstein radii at fixed baryon fraction when V(Γ) is the same as in COSMO‑Γ‑000 (D3 freeze honored).
  - module: COSMO-Γ-HALO
    excerpt: |
      For clusters, κ(θ) from Γ + gas reproduces observed θ_E at given baryon fraction and total mass; offsets in mergers handled in COSMO‑Γ‑MERGE. Falsification: failure to reproduce the Σ_0 locus or the V_c(r) diversity with the frozen V(Γ) invalidates Γ‑halo unification.
poetic_connections:
  motifs: [gravity's lens, distorted light, mass map, cosmic telescope]
  evocative_lines:
    - "Lensing κ(θ) maps from Γ alone reproduce observed Einstein radii..."
    - "A lens forged from gravity's well..."
  association_matrix:
    - [ "Γ_SOLITON_HALO", 0.9 ]
    - [ "CORE_SURFACE_DENSITY", 0.7 ]
    - [ "ROTATION_CURVE", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: κ (Convergence)
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        κ = (1/2) ∇²ψ, where ψ is the 2D lensing potential.
        κ = Σ / Σ_crit
      justification: |
        The Pirouette definition of κ(θ) = Σ/Σ_crit is mathematically identical to the standard definition of convergence in weak gravitational lensing theory. It represents the trace of the lensing magnification tensor's Jacobian, describing isotropic magnification.
      references:
        - title: Gravitational Lensing
          where: Schneider, P., Ehlers, J., Falco, E. E. (1992). Springer-Verlag.
          date: 1992-01-01
      confidence: 1.0
      rationale: The term is adopted directly from standard cosmological literature without modification, ensuring interoperability and direct comparison with observational data from lensing surveys.
constraints_and_falsifiers:
  claims:
    - statement: "For a given halo mass and baryon fraction, the κ(θ) profile and its derived Einstein radius θ_E are uniquely predicted by the Γ-soliton model with the potential V(Γ) frozen from COSMO-Γ-000."
      domain: phenomenology
      falsifier: "A statistically significant discrepancy between the predicted κ(θ) profiles from Γ-soliton solutions and the observed mass maps from cluster lensing, assuming well-constrained baryon models, would falsify the Γ-halo model."
      status: proposed
      links: [COSMO-Γ-HALO, COSMO-Γ-000]
naming_notes:
  collisions: [The symbol κ is also used for spacetime curvature in some contexts. The angular argument, κ(θ), is a key differentiator.]
  disambiguation: |
    This term refers specifically to gravitational lensing convergence, a 2D field on the sky. It should not be confused with the convergence of a numerical algorithm or a mathematical series.
crosslinks:
  near_synonyms: [PROJECTED_SURFACE_DENSITY]
  antonyms: [SHEAR]
  prerequisites: [Γ_SOLITON_HALO]
  downstream_effects: [EINSTEIN_RADIUS]
license: CC-BY-SA-4.0
---

# Lensing Convergence

## Canonical (Pirouette)
The Lensing Convergence, κ(θ), is a dimensionless scalar field on the observer's sky plane that quantifies the local magnification of light due to a foreground mass distribution. Within the Γ-Soliton Halo model, it is calculated as the ratio of the total projected surface mass density, Σ(θ), to the critical surface mass density, Σ_crit. Σ(θ) is derived by integrating the mass density of the Γ-field (ρ_Γ) and baryons (ρ_b) along the line of sight.

## EFT-First Summary
In standard General Relativity, Lensing Convergence (κ) is the isotropic component of the magnification of light from distant sources. It is defined as the projected surface mass density Σ normalized by the geometric critical density Σ_crit, `κ = Σ/Σ_crit`. Pirouette's Γ-Soliton model provides a first-principles prediction for Σ, and thus for κ, directly from the field dynamics, offering a testable alternative to particulate dark matter models. (See: Schneider, Ehlers & Falco, *Gravitational Lensing*, 1992).

## Glossary Links
- See also: Γ-Soliton Halo, Core Surface Density, Einstein Radius, Shear