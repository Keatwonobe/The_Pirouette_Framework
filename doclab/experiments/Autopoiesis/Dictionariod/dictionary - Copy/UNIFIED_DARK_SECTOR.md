---
term: "Unified Dark Sector"
canonical_id: "UNIFIED_DARK_SECTOR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-000"]
---

---
term: Unified Dark Sector
canonical_id: UNIFIED_DARK_SECTOR
symbol: Γ
aliases: ["Unified Dark Field", "Temporal Pressure Field"]
parents: [`COSMO-Γ-000`]
children: [`COSMO-Γ-HALO`, `COSMO-Γ-MERGE`]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-000
      snippet: |
        Early Universe (DM‑like): Γ oscillates about a quadratic minimum with m_Γ ≫ H → ⟨w_Γ⟩ → 0, c_s^2 → 0, clustering like CDM.
        Late Universe (DE‑like): Γ slow‑rolls on a flat segment of V(Γ) → w_Γ ≈ −1, nearly homogeneous, driving acceleration.
        ...“dark sector” is unified by Γ.
  editors: [GPT-4 via Pirouette Agent]
  review_log: []
triad:
  art: |
    A single actor plays two roles on the cosmic stage: first, a frantic, clumping dance of matter; then, a slow, vast stretch into accelerating emptiness.
  law: |
    A single, minimally-coupled scalar field Γ, with a potential V(Γ) fixed by D2 constraints and anchored by a single D3 measurement, must reproduce all observational evidence for both dark matter and dark energy without additional free parameters or fluids.
  philosophy: |
    To replace the dual mysteries of dark matter and dark energy with a single, falsifiable hypothesis, enforcing maximal parsimony and predictive power. It posits that the "dark sector" is not a collection of substances but a single dynamical process.
pirouette_definition: |
  A cosmological model where a single, real scalar field Γ is the sole constituent of the dark sector. In its early-universe, high-frequency oscillatory regime (m_Γ ≫ H), its time-averaged equation of state is ⟨w_Γ⟩ ≈ 0, mimicking Cold Dark Matter. In its late-universe, slow-roll regime, its equation of state is w_Γ ≈ −1, driving cosmic acceleration and mimicking Dark Energy.
operational_definition:
  units: Field Γ has dimensions of Energy ([M]); Potential V(Γ) has dimensions of Energy Density ([M L⁻³]) in units where c=1. In natural units (ħ=c=1), [M] and [M⁴] respectively.
  symbol_table:
    - name: Γ
      meaning: The Unified Dark Sector scalar field.
      dimensions: M
      default_range: contextual
    - name: V(Γ)
      meaning: The scalar potential for the Γ field.
      dimensions: M⁴
      default_range: contextual
    - name: m_Γ
      meaning: The mass parameter of the Γ field in its quadratic potential term.
      dimensions: M
      default_range: ~10⁻²⁷ eV
    - name: w_Γ
      meaning: Equation of state parameter for the Γ fluid, p_Γ/ρ_Γ.
      dimensions: dimensionless
      default_range: "[-1, 1]"
  measurement:
    procedures:
      - name: Global Cosmological Fit
        outline: |
          Using a Boltzmann code implementing the Γ field equations, compute theoretical power spectra (CMB, matter) and background expansion history (H(z), DA(z)). Anchor the U-class parameters {m_Γ, ...} with a single D3 measurement (e.g., Ω_m0). Perform a Bayesian analysis against a joint dataset (CMB, BAO, SNe, RSD, WL) to test the model's consistency across all preregistered (P4) observables.
        expected_signals: ["A specific evolution of fσ_8(z) and H(z)", "An S_8 value consistent with both high-z CMB and low-z weak lensing posteriors", "Gravitational slip parameter η ≡ Φ/Ψ ≈ 1 on linear scales"]
        pitfalls: ["Ignoring baryonic feedback effects, which can mimic or mask Γ-induced changes in the matter power spectrum", "Using an incorrectly calibrated D3 anchor measurement, propagating systematic error through all derived parameters", "Numerical instability in the background solver during the transition between oscillatory and slow-roll regimes"]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: COSMO-Γ-000
    excerpt: |
      Early Universe (DM‑like): Γ oscillates about a quadratic minimum with m_Γ ≫ H → ⟨w_Γ⟩ → 0, c_s^2 → 0, clustering like CDM. Late Universe (DE‑like): Γ slow‑rolls on a flat segment of V(Γ) → w_Γ ≈ −1, nearly homogeneous, driving acceleration. No additional fluids beyond standard baryons/radiation; “dark sector” is unified by Γ.
  - module: COSMO-Γ-000
    excerpt: |
      Sound speed: for canonical Γ, c_s^2 = 1 in field rest frame, but the *effective* sound speed for oscillatory condensates time‑averages to c_eff^2 ≈ 0 → CDM‑like clustering. Growth equation... S_Γ encodes residual pressure/anisotropic stress from Γ; under minimal coupling and oscillatory regime S_Γ → 0.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: ["unification", "duality", "cosmic chameleon", "oscillation", "slow-roll"]
  evocative_lines:
    - "“dark sector” is unified by Γ."
    - "a single‑field Pirouette cosmology"
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "D3_ONE_SHOT_ANCHOR", 0.9 ]
    - [ "D2_COMPLIANCE", 0.8 ]
    - [ "P4_PREREGISTERED_PREDICTION", 0.9 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Quintessence
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        w_Γ = (½ Γ̇² − V(Γ)) / (½ Γ̇² + V(Γ)) ≈ −1  (for Γ̇² ≪ V(Γ))
      justification: |
        In the late-time, slow-roll regime, the Γ field's dynamics are identical to that of a canonical quintessence field, providing a dynamical source for the observed cosmic acceleration.
      references: []
      confidence: 0.95
    - target: Axion-like Particle / Fuzzy Dark Matter
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        ⟨ρ_Γ⟩ ∝ a⁻³  (for V(Γ) = ½ m_Γ² Γ² and H ≪ m_Γ)
      justification: |
        In the early-universe, oscillatory regime, the time-averaged energy density of the Γ field in a quadratic potential redshifts like matter (a⁻³) and its effective sound speed approaches zero. This is the same behavior as a coherently oscillating scalar field, a common model for axionic or fuzzy dark matter.
      references: []
      confidence: 0.95
  adopted:
    - target: Quintaxion / Axion Quintessence
      rationale: "The Unified Dark Sector model is a specific implementation of the 'quintaxion' concept, where a single scalar field plays the role of both dark matter (axion-like oscillatory phase) and dark energy (quintessence-like slow-roll phase). The Pirouette framework enforces additional D2/D3/P4 constraints on this general idea."
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The Γ-field, with parameters fixed by a single D3 anchor, can simultaneously fit geometric expansion probes (BAO, SNe) and growth of structure probes (RSD, WL) without requiring additional dark sector components."
      domain: phenomenology
      falsifier: "A statistically significant tension (p<0.01) is found between the model's P4 predictions for geometry (e.g., H(z)) and structure growth (e.g., fσ_8(z)), or between its predictions and weak lensing S_8 measurements, after accounting for systematics."
      status: proposed
      links: [`COSMO-Γ-000`]
naming_notes:
  collisions: ["Γ (Gamma function)", "γ (photon particle symbol)"]
  disambiguation: |
    Within Pirouette cosmology modules, Γ refers exclusively to the Unified Dark Sector scalar field. It should not be confused with the photon (γ), often written with the same Greek letter, or the mathematical Gamma function. The context of a cosmological action or field equation makes the usage unambiguous.
crosslinks:
  near_synonyms: []
  antonyms: [`LAMBDA_CDM`]
  prerequisites: [`D2_COMPLIANCE`, `D3_ONE_SHOT_ANCHOR`, `P4_PREREGISTERED_PREDICTION`]
  downstream_effects: [`COSMO-Γ-HALO`, `COSMO-Γ-MERGE`]
license: CC-BY-SA-4.0
---