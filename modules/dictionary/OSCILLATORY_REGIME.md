---
term: "Oscillatory Regime"
canonical_id: "OSCILLATORY_REGIME"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-000"]
---

---
term: Oscillatory Regime
canonical_id: OSCILLATORY_REGIME
symbol: 
aliases: [CDM-like Regime, Matter-like Regime]
parents: [COSMO-Γ-000]
children: [COSMO-Γ-HALO, COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-Γ-000
      lines: "L24-L25"
      snippet: |
        Regimes:
        • Oscillatory (m_Γ ≫ H): time‑average over many cycles gives ⟨w_Γ⟩ ≈ 0 (quadratic potential), ⟨ρ_Γ⟩ ∝ a^−3.
  editors: [Pirouette-Agent-v2.3]
  review_log: []
triad:
  art: |
    The universe's primordial hum, a field vibrating too fast for cosmic expansion to notice. Its time-averaged presence is the silent, steady gravity of dark matter.
  law: |
    When the field mass `m_Γ` is much greater than the Hubble rate `H`, the time-averaged equation of state `⟨w_Γ⟩` approaches 0, and its energy density `⟨ρ_Γ⟩` redshifts as `a⁻³`, becoming dynamically indistinguishable from a pressureless fluid on cosmological scales.
  philosophy: |
    To unify the dark sector by demonstrating that apparent particle-like matter can emerge from the high-frequency dynamics of a fundamental scalar field, eliminating the need for a separate, stable cold dark matter particle.
pirouette_definition: |
  The dynamical state of the temporal pressure field Γ, typically in the early universe, defined by the condition `m_Γ ≫ H`. In this state, Γ undergoes rapid oscillations around the minimum of its potential `V(Γ)`. This behavior leads to a time-averaged equation of state `⟨w_Γ⟩ ≈ 0` and an energy density scaling `⟨ρ_Γ⟩ ∝ a⁻³`, which reproduces the large-scale gravitational effects of cold dark matter. The effective sound speed of perturbations `c_eff²` also approaches zero, permitting gravitational clustering.
operational_definition:
  units: Dimensionless (a dynamical condition)
  symbol_table:
    - name: m_Γ
      meaning: Mass of the Γ field
      dimensions: M
      default_range: ~1e-27 eV/c²
    - name: H
      meaning: Hubble expansion rate
      dimensions: T⁻¹
      default_range: contextual
    - name: w_Γ
      meaning: Equation of state parameter for Γ
      dimensions: dimensionless
      default_range: [-1, 1]
    - name: ρ_Γ
      meaning: Energy density of Γ
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: a
      meaning: Cosmological scale factor
      dimensions: dimensionless
      default_range: (0, 1]
  measurement:
    procedures:
      - name: Cosmological Parameter Inference
        outline: |
          Infer the background evolution `H(z)` and the growth of structure `fσ_8(z)` from cosmological surveys (CMB, BAO, RSD, lensing). Fit these data with a Pirouette cosmology model containing Γ. The oscillatory regime is confirmed if the model successfully fits the matter-dominated era (e.g., z > 1) with parameters satisfying `m_Γ ≫ H(z)` in that epoch.
        expected_signals: [A matter-like expansion history (`ρ ∝ a⁻³`), A structure growth rate consistent with CDM for z ~ 1-1100]
        pitfalls: [Degeneracy with ΛCDM parameters, Insufficient data precision to distinguish subtle deviations from a pure pressureless fluid]
context_windows:
  - module: COSMO-Γ-000
    excerpt: |
      Early Universe (DM‑like): Γ oscillates about a quadratic minimum with m_Γ ≫ H → ⟨w_Γ⟩ → 0, c_s^2 → 0, clustering like CDM. Late Universe (DE‑like): Γ slow‑rolls on a flat segment of V(Γ) → w_Γ ≈ −1... “dark sector” is unified by Γ.
  - module: COSMO-Γ-000
    excerpt: |
      Sound speed: for canonical Γ, c_s^2 = 1 in field rest frame, but the *effective* sound speed for oscillatory condensates time‑averages to c_eff^2 ≈ 0 → CDM‑like clustering.
poetic_connections:
  motifs: [vibrating field, emergent matter, cosmic hum, time-averaging]
  evocative_lines:
    - "Γ oscillates rapidly, mimicking cold dark matter"
    - "the effective sound speed for oscillatory condensates time‑averages to c_eff^2 ≈ 0"
  association_matrix:
    - [ "COLD_DARK_MATTER", 0.9 ]
    - [ "SLOW_ROLL_REGIME", 0.5 ]
formal_mappings:
  candidates:
    - target: Scalar Field Dark Matter (SFDM) / Axion-like Particle (ALP) condensate
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        For V(ϕ) = ½m²ϕ², the time average ⟨p_ϕ⟩ = ⟨½ϕ̇² - V(ϕ)⟩ → 0.
      justification: |
        Models of a light scalar field oscillating in a quadratic potential are a well-established candidate for cold dark matter. The time-averaging of kinetic and potential energy over many oscillations results in an effective zero-pressure fluid on cosmological timescales. The Oscillatory Regime is a direct, specific implementation of this concept within the Pirouette Framework.
      references:
        - title: Coherent scalar-field oscillations in an expanding universe
          where: Phys. Rev. D 28, 1243
          date: 1983-09-15
      confidence: 0.95
  adopted:
    - target: Scalar Field Dark Matter (SFDM)
      rationale: This is the most direct and widely understood analogue in modern cosmology for the phenomenon described. It captures both the scalar field nature and the emergent matter-like behavior.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The Oscillatory Regime of Γ correctly reproduces the observed growth of structure (fσ_8(z)) and background expansion history (H(z)) during the matter-dominated era without a separate CDM particle."
      domain: phenomenology
      falsifier: "A statistically significant (>5σ) discrepancy between the Γ model's preregistered predictions for fσ_8(z) or BAO scales and data from next-generation surveys, where the discrepancy cannot be resolved by the anchored parameters."
      status: proposed
      links: [COSMO-Γ-000]
naming_notes:
  collisions: [Neutrino oscillations, Oscillatory integral]
  disambiguation: |
    Refers to a cosmological *epoch* defined by the high-frequency dynamics of the Γ field, not to particle-level quantum oscillations. It is the direct dynamical antecedent and counterpart to the late-time Slow-Roll Regime of the same field.
crosslinks:
  near_synonyms: []
  antonyms: [SLOW_ROLL_REGIME]
  prerequisites: [TEMPORAL_PRESSURE, ONE_SHOT_ANCHOR]
  downstream_effects: [COSMO-Γ-HALO]
license: CC-BY-SA-4.0
---

# Oscillatory Regime

## Canonical (Pirouette)
The dynamical state of the temporal pressure field Γ, typically in the early universe, defined by the condition `m_Γ ≫ H`. In this state, Γ undergoes rapid oscillations around the minimum of its potential `V(Γ)`. This behavior leads to a time-averaged equation of state `⟨w_Γ⟩ ≈ 0` and an energy density scaling `⟨ρ_Γ⟩ ∝ a⁻³`, which reproduces the large-scale gravitational effects of cold dark matter. The effective sound speed of perturbations `c_eff²` also approaches zero, permitting gravitational clustering.

## EFT-First Summary
In standard cosmological terms, the Oscillatory Regime is a realization of Scalar Field Dark Matter (SFDM). A scalar field (Γ) with mass `m_Γ` begins oscillating coherently around its quadratic potential minimum when the Hubble rate `H` drops below its mass. The time-averaged pressure vanishes (`⟨w_Γ⟩ ≈ 0`), and the energy density scales as non-relativistic matter (`ρ_Γ ∝ a⁻³`), thus providing a microphysical origin for cold dark matter.

## Glossary Links
- See also: [Slow-Roll Regime](<link>), [Temporal Pressure](<link>)