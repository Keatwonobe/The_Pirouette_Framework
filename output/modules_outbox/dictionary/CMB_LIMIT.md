---
term: "CMB limit"
canonical_id: "CMB_LIMIT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-005"]
---

---
term: CMB limit
canonical_id: CMB_LIMIT
symbol: 
aliases: [ΛCDM limit, Large-scale limit]
parents: [COSMO-005]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-005
      lines: "Section 3"
      snippet: |
        • CMB limit: when c_s→0 and m_eff→0, spectra must match ΛCDM to ≤0.1% (V1).
  editors: [Agent: Pirouette Definer]
  review_log: []
triad:
  art: |
    On the universe's oldest canvas, the new physics must be a perfect forger, leaving no trace of its handiwork where the ancient light still glows.
  law: |
    In a superfluid dark matter model, the effective sound speed `c_{s,eff}²` must be sufficiently small (`≪ 10⁻⁶`) for all wavenumbers `k` relevant to primary CMB anisotropies (`ℓ ≲ 2500`). This ensures the resulting power spectra (TT, TE, EE) match standard ΛCDM predictions to within a specified tolerance, typically 0.1%.
  philosophy: |
    To propose new physics on small scales, one must first earn the right by perfectly reproducing established physics on large scales. The CMB limit is the gatekeeper, ensuring that any proposed deviation from Cold Dark Matter is a localized phenomenon, not a rewriting of cosmic history.
pirouette_definition: |
  The CMB limit is a phenomenological constraint on superfluid dark matter models, requiring that the effective sound speed of the fluid approaches zero on large comoving scales and at early times. This ensures the model behaves identically to Cold Dark Matter (CDM) during recombination, thereby reproducing the CMB angular power spectra of the standard ΛCDM cosmology to a specified precision.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: c_{s,eff}²
      meaning: Scale-dependent effective sound speed squared
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ℓ
      meaning: Angular multipole moment
      dimensions: dimensionless
      default_range: "[2, 2500]"
    - name: ΔCl/Cl
      meaning: Fractional deviation of angular power spectrum from ΛCDM
      dimensions: dimensionless
      default_range: "[-0.001, 0.001]"
  measurement:
    procedures:
      - name: ΛCDM Concordance Test (V1)
        outline: |
          1. Configure a Boltzmann code (e.g., CLASS) with the `gammat_superfluid` species and a set of `P(X)` parameters.
          2. Compute the CMB angular power spectra (ClTT, ClTE, ClEE) up to ℓ ≈ 2500.
          3. Run a standard ΛCDM simulation using identical background cosmological parameters.
          4. For each spectrum, calculate the percentage difference between the superfluid and ΛCDM results at each multipole ℓ.
          5. The model passes if the maximum absolute deviation across all relevant spectra and multipoles is below the tolerance (e.g., 0.1%).
        expected_signals: [A plot of `ΔCl/Cl` vs `ℓ` that remains within the `±0.1%` tolerance band.]
        pitfalls: [Mismatch in background cosmological parameters between runs, Numerical instability from the fluid/field switch criteria, Model parameters that prevent `c_s²` from decaying sufficiently fast at early times.]
context_windows:
  - module: COSMO-005
    excerpt: |
      Perturbations (Newtonian gauge, effective fluid):
      δ_Γ′ = −(1+w_Γ)(θ_Γ − 3Φ′) − 3ℋ (c_{s,eff}² − w_Γ) δ_Γ
      θ_Γ′ = −ℋ θ_Γ + k² Ψ + k² c_{s,eff}² δ_Γ/(1+w_Γ)
      with w_Γ≈0 through recombination (ensure c_{s,eff}² ≪ 10⁻⁶ on k relevant to ℓ≲2500).
  - module: COSMO-005
    excerpt: |
      Stability & Validation Suite
      • Positivity: ρ_Γ>0, c_s²≥0, c_{s,eff}²≥0; enforce α>0, β∈{0,1/2,1}.
      • CMB limit: when c_s→0 and m_eff→0, spectra must match ΛCDM to ≤0.1% (V1).
      • Threshold scans: doubling switch thresholds changes TT/TE/EE by <0.2% (V5).
poetic_connections:
  motifs: [cosmic background, large-scale fidelity, phenomenological anchor, asymptotic safety]
  evocative_lines:
    - "reproduces CDM on CMB scales"
    - "match ΛCDM to ≤0.1%"
  association_matrix:
    - [ "EFFECTIVE_SOUND_SPEED", 0.9 ]
    - [ "LAMBDA_CDM", 0.8 ]
    - [ "STABILITY_VALIDATION", 0.7 ]
formal_mappings:
  candidates:
    - target: Large-scale structure constraint
      domain: Cosmology
      mapping_kind: conceptual
      equation_hint: |
        (ΔCl / Cl)_ℓ < ε  for ℓ < ℓ_max
      justification: |
        This constraint is conceptually identical to the requirement imposed on many alternative dark matter models (e.g., Fuzzy DM, Self-Interacting DM) that they must not alter the successful predictions of ΛCDM on scales constrained by the CMB and Baryon Acoustic Oscillations. It ensures new physics is confined to smaller, less-constrained scales where it is invoked to solve specific problems.
      references:
        - title: "Dark Matter Self-Interactions and Small Scale Structure"
          where: "Physics Reports, 730, 1-59"
          date: 2018-02-15
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A `gammat_superfluid` model can resolve small-scale structure anomalies while satisfying the CMB limit."
      domain: phenomenology
      falsifier: "No region of the model's parameter space can be found that simultaneously produces sufficient small-scale power suppression (for halo cores) while also keeping CMB spectral deviations below the 0.1% threshold. This would indicate an inextricable coupling between large-scale and small-scale physics in the model, making it non-viable."
      status: proposed
      links: [COSMO-005]
naming_notes:
  collisions: [The term "limit" is generic in physics (e.g., Newtonian limit, classical limit).]
  disambiguation: |
    Distinguish from the *small-scale limit*, where the model's behavior is expected to deviate significantly from ΛCDM to resolve issues like the core-cusp problem. The CMB limit concerns large-scale, early-universe behavior, whereas the small-scale limit concerns non-linear structure formation at late times.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [EFFECTIVE_SOUND_SPEED, SUPERFLUID_DARK_MATTER]
  downstream_effects: [HALO_CORE_FORMATION]
license: CC-BY-SA-4.0
---

# CMB limit

## Canonical (Pirouette)
The CMB limit is a phenomenological constraint on superfluid dark matter models, requiring that the effective sound speed of the fluid approaches zero on large comoving scales and at early times. This ensures the model behaves identically to Cold Dark Matter (CDM) during recombination, thereby reproducing the CMB angular power spectra of the standard ΛCDM cosmology to a specified precision.

## EFT-First Summary
In the context of an Effective Field Theory for a dark matter superfluid, the CMB limit is the regime where the kinetic term `P(X)` and its derivatives result in a negligible sound speed (`c_s² → 0`) at early times. This ensures the fluid behaves as a pressureless component, equivalent to standard Cold Dark Matter, thus preserving the well-measured CMB power spectrum. Any new physics is thereby restricted to later times and smaller scales where the sound speed becomes dynamically important.

## Glossary Links
- See also: `EFFECTIVE_SOUND_SPEED`, `SUPERFLUID_DARK_MATTER`, `LAMBDA_CDM`