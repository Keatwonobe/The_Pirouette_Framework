---
term: "Gravitational Slip"
canonical_id: "GRAVITATIONAL_SLIP"
symbol: "η"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-000"]
---

---
term: Gravitational Slip
canonical_id: GRAVITATIONAL_SLIP
symbol: η
aliases: [Anisotropic Slip, Anisotropic Stress Parameter]
parents: [COSMO-000]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-000
      lines: "Section 2, Section 4"
      snippet: |
        Slip η ≡ Φ/Ψ ≈ 1 on linear scales (minimal coupling)
  editors: [pirouette-agent-v1.3]
  review_log: []
triad:
  art: |
    A measure of discord in gravity's voice. Does spacetime curve space and time in unison, or does one warp more than the other?
  law: |
    In the COSMO-Γ model with minimal coupling, the gravitational slip η ≡ Φ/Ψ must equal 1 on linear scales (k ≲ 0.1 h/Mpc) to within model prediction uncertainties. A measured deviation from unity would falsify the minimal coupling assumption.
  philosophy: |
    Gravitational slip serves as a sharp test for modifications to General Relativity or the presence of exotic fluids with anisotropic stress. It directly probes the tensor structure of the theory governing cosmic structure formation, distinguishing canonical scalar fields from more complex theories.
pirouette_definition: |
  Gravitational Slip (η) is the ratio of the two scalar metric potentials, Φ and Ψ, in a perturbed Friedmann-Lemaître-Robertson-Walker (FLRW) spacetime. Within the COSMO-Γ framework, η is a preregistered, out-of-sample prediction used to test the model's fundamental assumptions, such as minimal coupling of the Γ-field to gravity.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: η
      meaning: Gravitational Slip, defined as the ratio Φ/Ψ.
      dimensions: dimensionless
      default_range: ≈ 1
    - name: Φ
      meaning: Curvature potential, describing spatial curvature perturbations.
      dimensions: dimensionless
      default_range: contextual
    - name: Ψ
      meaning: Newtonian gravitational potential, describing perturbations to the time-time metric component.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Lensing-Growth Comparison
        outline: |
          Infer η by comparing two distinct cosmological measurements. The growth of large-scale structure, measured via galaxy clustering and redshift-space distortions (RSDs), is primarily sensitive to the potential Ψ. Gravitational lensing, which measures the deflection of light from distant sources, is sensitive to the sum of the potentials, Φ+Ψ. A statistically significant discrepancy between the mass distribution inferred from structure growth and that inferred from lensing constrains η.
        expected_signals: [fσ₈(z) from RSDs, S₈(z) from weak lensing surveys]
        pitfalls: [Systematic errors from galaxy bias, intrinsic alignments of galaxy shapes, photometric redshift uncertainties]
context_windows:
  - module: COSMO-000
    excerpt: |
      Predicted functions:
      • H(z), DA(z), DV(z) (geometry)
      • fσ_8(z) (growth)
      • Slip η ≡ Φ/Ψ ≈ 1 on linear scales (minimal coupling)
  - module: COSMO-000
    excerpt: |
      Preregistered, Out-of-Sample Predictions (P4)
      Targets (no further tuning):
      4. Gravitational slip η(k,z) on linear scales (k ≲ 0.1 h/Mpc) with 1σ band.
poetic_connections:
  motifs: [gravity, curvature, lensing, structure, discord]
  evocative_lines:
    - "Slip η ≡ Φ/Ψ ≈ 1"
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "MINIMAL_COUPLING", 0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Gravitational Slip (η)
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        In the Newtonian gauge, g_{μν} = a^2(\tau) [ -(1+2Ψ)d\tau^2 + (1-2Φ)δ_{ij}dx^i dx^j ].
        η is defined as the ratio Φ/Ψ.
      justification: |
        This is the standard definition in physical cosmology. In General Relativity sourced by matter with zero anisotropic stress (e.g., a perfect fluid or a canonical scalar field like Γ), the perturbed Einstein equations imply Φ=Ψ, and therefore η=1. Deviations from unity are a model-independent signature of either a modification to GR or the presence of a fluid with significant anisotropic stress.
      references:
        - title: Probing Gravity with Lensing and Redshift Surveys
          where: Physical Review D 78, 043531 (arXiv:0803.0987)
          date: 2008-08-27
      confidence: 1.0
      rationale: Direct adoption of the standard term and definition from the physical cosmology literature, which aligns perfectly with its usage in COSMO-000.
constraints_and_falsifiers:
  claims:
    - statement: "The minimal-coupling COSMO-Γ model predicts η(k,z) = 1 for linear scales k ≲ 0.1 h/Mpc."
      domain: phenomenology
      falsifier: "A statistically significant measurement of η ≠ 1 on linear scales from a combination of weak lensing and redshift-space distortion data would refute the minimal-coupling assumption of the base COSMO-Γ model."
      status: proposed
      links: [COSMO-000]
naming_notes:
  collisions: [The symbol η is also commonly used for conformal time in cosmology and for viscosity in fluid dynamics.]
  disambiguation: |
    In the context of metric potentials (Φ, Ψ) and cosmological perturbations, η refers to gravitational slip. Be aware that some literature sources define slip as the inverse ratio, Ψ/Φ. The Pirouette Framework consistently uses η ≡ Φ/Ψ as specified in COSMO-000.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: []
  downstream_effects: [GROWTH_OF_STRUCTURE, WEAK_LENSING]
license: CC-BY-SA-4.0
---

# Gravitational Slip

## Canonical (Pirouette)
Gravitational Slip (η) is the ratio of the two scalar metric potentials, Φ and Ψ, in a perturbed Friedmann-Lemaître-Robertson-Walker (FLRW) spacetime. Within the COSMO-Γ framework, η is a preregistered, out-of-sample prediction used to test the model's fundamental assumptions, such as minimal coupling of the Γ-field to gravity.

## EFT-First Summary
Gravitational Slip η is a standard cosmological observable corresponding to the ratio of the two scalar metric potentials, Φ/Ψ. In General Relativity with matter sources that have no anisotropic stress (e.g., a perfect fluid or a canonical scalar field like Γ), theory predicts η=1. Thus, measurements of η serve as a powerful null test for non-standard physics, such as modified gravity or exotic dark energy models.

## Glossary Links
- See also: Metric Potentials, Growth of Structure