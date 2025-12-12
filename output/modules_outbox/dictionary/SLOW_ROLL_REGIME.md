---
term: "Slow-roll Regime"
canonical_id: "SLOW_ROLL_REGIME"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-000"]
---

---
term: Slow-roll Regime
canonical_id: SLOW_ROLL_REGIME
symbol: w_Γ ≈ -1
aliases: [Dark Energy Phase, Accelerating Epoch, de Sitter-like Phase]
parents: [COSMO-Γ-000]
children: [COSMO-Γ-HALO, COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-Γ-000
      snippet: |
        • Late Universe (DE‑like): Γ slow‑rolls on a flat segment of V(Γ) → w_Γ ≈ −1, nearly homogeneous, driving acceleration.
  editors: [Agent]
  review_log: []
triad:
  art: |
    The universe, weary from its frantic, oscillating youth, settles into a long, quiet coast. The temporal pressure field Γ now glides almost effortlessly down a shallow potential, its near-constant energy gently pushing spacetime apart.
  law: |
    In the late universe (z ≲ 1), the temporal pressure field Γ enters a state where its kinetic energy is negligible compared to its potential energy (½ Γ̇² ≪ V(Γ)), causing its equation of state w_Γ to approach -1. This regime is falsified if measurements of H(z) or fσ₈(z) require w(z) to deviate significantly from the prediction derived from the one-shot anchored potential V(Γ).
  philosophy: |
    The Slow-roll Regime unifies dark energy with dark matter by framing cosmic acceleration not as a new substance, but as the final, quiescent dynamical phase of the same field Γ that previously behaved as cold matter. This fulfills the framework's principle of parsimony, attributing two major cosmic mysteries to one underlying mechanism.
pirouette_definition: |
  The dynamical state of the temporal pressure scalar field Γ, typically occurring at low redshift (z ≲ 1), characterized by a kinetic energy density significantly smaller than its potential energy density (ε_Γ ≡ ½ Γ̇² / V(Γ) ≪ 1). This condition leads to an effective equation of state w_Γ ≈ -1, driving the accelerated expansion of the universe. The slow-roll is sustained by a sufficiently flat region of the potential V(Γ) and is the terminal phase of Γ's evolution after the Oscillatory Regime.
operational_definition:
  units: Dimensionless (conditions defining the regime)
  symbol_table:
    - name: w_Γ
      meaning: Equation of state parameter for the Γ field (p_Γ/ρ_Γ).
      dimensions: dimensionless
      default_range: ≈ -1
    - name: ε_Γ
      meaning: The primary slow-roll parameter for Γ (ρ_kinetic/V).
      dimensions: dimensionless
      default_range: ≪ 1
    - name: Γ̇
      meaning: Time derivative of the Γ field.
      dimensions: M¹ L⁻¹ T⁻² (in natural units c=ħ=1)
      default_range: ≈ 0
    - name: V(Γ)
      meaning: Potential energy density of the Γ field.
      dimensions: M¹ L⁻¹ T⁻² (energy density)
      default_range: ≈ ρ_crit,0
  measurement:
    procedures:
      - name: Cosmological Background and Growth Inference
        outline: |
          Combine measurements of the cosmic expansion history (H(z) from BAO, D_A(z) from SNe Ia) and the growth of structure (fσ₈(z) from RSDs). Fit these data to the background and perturbation equations derived in COSMO-Γ-000. Infer the evolution of w_Γ(z) and check for consistency with the w_Γ ≈ -1 prediction from the one-shot anchored potential V(Γ).
        expected_signals: [Reconstructed w(z) consistent with -1 for z < 1, Measured fσ₈(z) matching the Γ-only cosmology prediction]
        pitfalls: [Systematic errors in distance ladder calibration, Biases in redshift-space distortion modeling, Baryonic feedback contamination]
context_windows:
  - module: COSMO-Γ-000
    excerpt: |
      • Late Universe (DE‑like): Γ slow‑rolls on a flat segment of V(Γ) → w_Γ ≈ −1, nearly homogeneous, driving acceleration.
      • No additional fluids beyond standard baryons/radiation; “dark sector” is unified by Γ.
  - module: COSMO-Γ-000
    excerpt: |
      Regimes:
      • Oscillatory (m_Γ ≫ H): time‑average over many cycles gives ⟨w_Γ⟩ ≈ 0 (quadratic potential), ⟨ρ_Γ⟩ ∝ a^−3.
      • Slow‑roll: ε_Γ ≡ (½ Γ̇^2)/V ≪ 1 → w_Γ ≈ −1 + 2ε_Γ.
poetic_connections:
  motifs: [cosmic exhaustion, quiet coasting, final state, gentle push, unification]
  evocative_lines:
    - "...nearly homogeneous, driving acceleration."
    - "...the terminal phase of Γ's evolution."
  association_matrix:
    - [ "OSCILLATORY_REGIME", 0.9 ]
    - [ "UNIFIED_DARK_SECTOR", 0.8 ]
formal_mappings:
  candidates:
    - target: Quintessence
      domain: GR
      mapping_kind: conceptual
      justification: |
        Like quintessence models, the Slow-roll Regime attributes cosmic acceleration to a dynamical scalar field slowly rolling down a potential. However, within Pirouette, this is not a separate field but a specific late-time behavior of the unified Γ field, which also acts as dark matter.
      references:
        - title: Cosmological consequences of a rolling homogeneous scalar field
          where: Phys. Rev. D 37, 3406 (1988)
          date: 1988-06-15
      confidence: 0.8
  adopted:
    - target: Dynamical Dark Energy
      rationale: This general term captures the essence of the phenomenon—a non-constant source for cosmic acceleration—while avoiding the implication of a separate, dedicated quintessence fluid, thereby preserving the unified nature of the Γ field.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The late-universe acceleration is fully described by the Γ field entering the Slow-roll Regime, with an equation of state w_Γ ≈ -1, without requiring a cosmological constant or additional dark energy fluid."
      domain: phenomenology
      falsifier: "A statistically significant measurement (p < 0.01) from combined BAO, SNe, and CMB data showing that the dark energy equation of state is exactly w = -1 (favoring Λ) or deviates from the Γ-potential's prediction in a way that cannot be explained by systematics."
      status: proposed
      links: [COSMO-Γ-000]
naming_notes:
  collisions: [Inflationary slow-roll]
  disambiguation: |
    Distinguish from the *Inflationary* Slow-roll Regime, which describes a similar dynamical process for the inflaton field in the very early universe. The Γ Slow-roll Regime occurs at low redshift (z ≲ 1) and involves a much lower energy scale.
crosslinks:
  near_synonyms: [DYNAMIC_DARK_ENERGY]
  antonyms: [OSCILLATORY_REGIME]
  prerequisites: [UNIFIED_DARK_SECTOR, TEMPORAL_PRESSURE_GAMMA]
  downstream_effects: [COSMIC_ACCELERATION, STRUCTURE_GROWTH_SUPPRESSION]
license: CC-BY-SA-4.0
---

# Slow-roll Regime

## Canonical (Pirouette)
The dynamical state of the temporal pressure scalar field Γ, typically occurring at low redshift (z ≲ 1), characterized by a kinetic energy density significantly smaller than its potential energy density (ε_Γ ≡ ½ Γ̇² / V(Γ) ≪ 1). This condition leads to an effective equation of state w_Γ ≈ -1, driving the accelerated expansion of the universe. The slow-roll is sustained by a sufficiently flat region of the potential V(Γ) and is the terminal phase of Γ's evolution after the Oscillatory Regime.

## EFT-First Summary
In standard cosmological terms, the Slow-roll Regime is the Pirouette Framework's realization of **Dynamical Dark Energy**. It describes the late-time behavior of the unified scalar field Γ, where its dynamics are equivalent to a quintessence field rolling on a very flat potential. The field's kinetic energy becomes negligible, causing its equation of state `w_Γ` to approach -1 and drive cosmic acceleration. This behavior is a direct consequence of the potential `V(Γ)` anchored by the one-shot procedure, not an independent degree of freedom.

## Glossary Links
- See also: Oscillatory Regime, Unified Dark Sector, Temporal Pressure Γ