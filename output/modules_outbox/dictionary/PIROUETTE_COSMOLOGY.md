---
term: "Pirouette Cosmology"
canonical_id: "PIROUETTE_COSMOLOGY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-000"]
---

---
term: Pirouette Cosmology
canonical_id: PIROUETTE_COSMOLOGY
symbol: 
aliases: [Unified Dark Sector, Γ-Cosmology]
parents: [MATH-018, MATH-019, MATH-020]
children: [COSMO-Γ-HALO, COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-Γ-000
      snippet: |
        • Early Universe (DM‑like): Γ oscillates about a quadratic minimum with m_Γ ≫ H → ⟨w_Γ⟩ → 0, c_s^2 → 0, clustering like CDM.
        • Late Universe (DE‑like): Γ slow‑rolls on a flat segment of V(Γ) → w_Γ ≈ −1, nearly homogeneous, driving acceleration.
        • No additional fluids beyond standard baryons/radiation; “dark sector” is unified by Γ."
  editors: [AI Agent]
  review_log: []
triad:
  art: |
    A single field, Γ, pirouettes across cosmic history. In the universe's youth, it twirls and gathers into the seeds of galaxies; in its maturity, it unfurls to drive all things apart.
  law: |
    The observed phenomena of dark matter and dark energy are not caused by two separate substances, but are the early-time oscillatory and late-time slow-roll dynamical regimes, respectively, of a single, minimally-coupled scalar field, Γ, whose potential V(Γ) is fixed by D2 constraints and anchored by a single D3 measurement.
  philosophy: |
    Pirouette Cosmology replaces the two greatest unknowns in the standard model with one, unifying the dark sector under a single physical entity. It enforces radical predictivity by disallowing ad-hoc parameter tuning, instead demanding that all U-class parameters be derived from a single, preregistered anchor measurement, with all other cosmological observations serving as out-of-sample falsification tests.
pirouette_definition: |
  A cosmological model built upon a single, real scalar field, Γ (the temporal pressure field), which unifies the dark sector. The dynamics of Γ, governed by a D2-compliant potential V(Γ), naturally transition between two regimes. In the early universe, when its mass exceeds the Hubble rate (m_Γ ≫ H), the field oscillates rapidly, behaving as pressureless Cold Dark Matter (⟨w_Γ⟩≈0, c_eff^2≈0). In the late universe, as H decreases, the field enters a slow-roll phase where its potential energy dominates, behaving as Dark Energy (w_Γ≈−1) and driving cosmic acceleration. The model's parameters are not fit to data but are fixed by a D3 One-Shot Anchor, with its validity judged by its ability to match preregistered, out-of-sample P4 observables.
operational_definition:
  units: Field units: Energy (eV); Cosmological observables: standard (Mpc, km/s/Mpc, dimensionless ratios).
  symbol_table:
    - name: Γ
      meaning: Temporal pressure scalar field amplitude.
      dimensions: Energy (ML²T⁻²)
      default_range: contextual
    - name: V(Γ)
      meaning: Potential energy density of the Γ field.
      dimensions: Energy Density (ML⁻¹T⁻²)
      default_range: contextual
    - name: w_Γ
      meaning: Equation of state parameter for the Γ field (p_Γ/ρ_Γ).
      dimensions: dimensionless
      default_range: [-1, 1]
    - name: m_Γ
      meaning: Mass parameter in the V(Γ) potential, sets oscillation frequency.
      dimensions: Energy (ML²T⁻²)
      default_range: ~10⁻²⁷ eV
    - name: H(z)
      meaning: Hubble parameter as a function of redshift.
      dimensions: T⁻¹
      default_range: 60-80 km/s/Mpc
    - name: fσ_8(z)
      meaning: The product of the linear growth rate and the amplitude of matter fluctuations.
      dimensions: dimensionless
      default_range: 0.3-0.8
  measurement:
    procedures:
      - name: Cosmological Inference via Unified Field Dynamics
        outline: |
          1. Select a single D3 anchor measurement (e.g., Ω_m0 from the CMB).
          2. Use this anchor and D2 symmetry constraints to derive and freeze the U-class parameters of the potential V(Γ) (e.g., m_Γ).
          3. Numerically integrate the coupled field and Friedmann equations from high redshift to today to obtain the background evolution (H(z), D_A(z)).
          4. Solve the linearized perturbation equations for the Γ-baryon-radiation fluid to compute the growth of structure (fσ_8(z)) and lensing potential.
          5. Compare these un-tuned P4 predictions against independent cosmological datasets (e.g., RSD from DESI, weak lensing from Euclid).
        expected_signals: [A consistent prediction for H(z), D_V(z)/r_s, fσ_8(z), and S_8 from a single parameter set, A specific, non-Λ evolution of w_dark(z)]
        pitfalls: [Numerical instability during the stiff oscillatory phase, Underestimated systematic errors in observational data, Misidentification of the D3 anchor.]
context_windows:
  - module: COSMO-Γ-000
    excerpt: |
      Establish a single-field Pirouette cosmology in which the temporal-pressure scalar Γ reproduces the observed phenomenology attributed to cold dark matter (CDM) and dark energy (DE) as two dynamical regimes of the same field. All functional choices obey MATH-018 D2 (local, analytic, scale-covariant), with one-shot anchoring (D3) and preregistered, out-of-sample predictions (P4).
  - module: COSMO-Γ-000
    excerpt: |
      The *effective* sound speed for oscillatory condensates time-averages to c_eff^2 ≈ 0 → CDM-like clustering.
      Predicted functions:
      • H(z), DA(z), DV(z) (geometry)
      • fσ_8(z) (growth)
      • Slip η ≡ Φ/Ψ ≈ 1 on linear scales (minimal coupling)
      • GW speed c_GW = c (no non-minimal curvature portals)
poetic_connections:
  motifs: [unification, cosmic dance, emergent behavior, shadow and light, early-vs-late]
  evocative_lines:
    - "...reproduces the observed phenomenology...as two dynamical regimes of the same field."
    - "Falsification conditions are met if any of the above require an extra fluid beyond Γ to match data..."
  association_matrix:
    - [ "TEMPORAL_PRESSURE_FIELD", 1.0 ]
    - [ "ONE_SHOT_ANCHORING", 0.9 ]
    - [ "DARK_MATTER", 0.8 ]
    - [ "DARK_ENERGY", 0.8 ]
formal_mappings:
  candidates:
    - target: Quintessence
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        w_Γ = (½ Γ̇² − V(Γ)) / (½ Γ̇² + V(Γ)) ≈ -1 for Γ̇² ≪ V(Γ)
      justification: |
        In its late-time, slow-roll regime, Γ is a canonical scalar field with w_Γ ≈ -1, which is the definition of a quintessence model for dark energy. This mapping applies only to the late-universe behavior of the Γ field.
      references:
        - title: Cosmological constant problem and quintessence
          where: Class.Quant.Grav.15:1753-1777, 1998
          date: 1998-06-18
      confidence: 0.9
    - target: Axion-like / Fuzzy Dark Matter
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        ⟨ρ_Γ⟩ ∝ a⁻³, ⟨w_Γ⟩ = 0 for m_Γ ≫ H
      justification: |
        In the early universe, Γ oscillates in a quadratic potential, causing its time-averaged energy density to redshift like matter and its effective sound speed to approach zero. This is the characteristic behavior of axion-like or "fuzzy" dark matter models.
      references:
        - title: Wavelike cold dark matter
          where: Phys.Rev.D 62, 103517
          date: 2000-09-18
      confidence: 0.8
  adopted:
    - target: Unified Dark Sector Model (Quartessence)
      rationale: This is the most accurate high-level description, as the model's primary feature is the unification of both dark components into a single dynamical entity, rather than just being one or the other. It captures the essential concept that DM and DE are different evolutionary phases of the same substance.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The Pirouette Cosmology, with parameters fixed by a single anchor (e.g., Ω_m0), simultaneously predicts the observed H(z) expansion history and fσ_8(z) growth history without additional free parameters."
      domain: phenomenology
      falsifier: "A statistically significant (p<0.01) discrepancy between the model's P4 predictions for BAO/RSD observables and data from surveys like DESI or Euclid."
      status: proposed
      links: [COSMO-Γ-000]
    - statement: "The gravitational slip parameter η ≡ Φ/Ψ is unity on linear scales."
      domain: theory
      falsifier: "Observation of η ≠ 1 on linear scales, which would imply non-minimal coupling or anisotropic stress not generated by a canonical scalar field."
      status: proposed
      links: [COSMO-Γ-000]
    - statement: "The speed of gravitational waves is equal to the speed of light (c_GW = c)."
      domain: theory
      falsifier: "An observation of c_GW ≠ c from a multi-messenger event, which would falsify the entire class of minimally-coupled scalar-tensor theories upon which this model is built."
      status: supported
      links: [COSMO-Γ-000]
naming_notes:
  collisions: ["Cosmology" is a generic term.]
  disambiguation: |
    Distinguish from multi-field dark sector models or models where Dark Matter and Dark Energy interact non-gravitationally. In Pirouette Cosmology, they are two phases of the *same* field, not two interacting fields. The name "Pirouette" evokes the field's change in dynamic behavior over time, like a dancer changing from a rapid spin (oscillation) to a slow extension (slow-roll).
crosslinks:
  near_synonyms: [UNIFIED_DARK_SECTOR_GAMMA]
  antonyms: [LAMBDA_CDM]
  prerequisites: [TEMPORAL_PRESSURE_FIELD, ONE_SHOT_ANCHORING, D2_COMPLIANCE]
  downstream_effects: [COSMO_GAMMA_HALO, COSMO_GAMMA_MERGE]
license: CC-BY-SA-4.0
---

# Pirouette Cosmology

## Canonical (Pirouette)
A cosmological model built upon a single, real scalar field, Γ (the temporal pressure field), which unifies the dark sector. The dynamics of Γ, governed by a D2-compliant potential V(Γ), naturally transition between two regimes. In the early universe, when its mass exceeds the Hubble rate (m_Γ ≫ H), the field oscillates rapidly, behaving as pressureless Cold Dark Matter (⟨w_Γ⟩≈0, c_eff^2≈0). In the late universe, as H decreases, the field enters a slow-roll phase where its potential energy dominates, behaving as Dark Energy (w_Γ≈−1) and driving cosmic acceleration. The model's parameters are not fit to data but are fixed by a D3 One-Shot Anchor, with its validity judged by its ability to match preregistered, out-of-sample P4 observables.

## EFT-First Summary
Pirouette Cosmology is a type of Unified Dark Sector model, often called Quartessence in the literature. It posits a single, canonical scalar field that first behaves like Axion/Fuzzy Dark Matter in the early universe due to rapid oscillations in its potential, and later transitions to a Quintessence-like field driving cosmic acceleration. Unlike many models, its parameters are fixed by principle rather than fit, and it predicts c_GW=c and no gravitational slip on linear scales.

## Glossary Links
- See also: [TEMPORAL_PRESSURE_FIELD](./temporal_pressure_field.md), [ONE_SHOT_ANCHORING](./one_shot_anchoring.md), [LAMBDA_CDM](./lambda_cdm.md)