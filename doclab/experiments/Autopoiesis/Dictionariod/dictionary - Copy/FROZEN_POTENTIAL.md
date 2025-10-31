---
term: "Frozen Potential"
canonical_id: "FROZEN_POTENTIAL"
symbol: "V(Γ)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-002"]
---

---
term: Frozen Potential
canonical_id: FROZEN_POTENTIAL
symbol: V(Γ)
aliases: [Anchor Potential, Inherited Potential]
parents: [COSMO-Γ-000, COSMO-Γ-HALO]
children: [COSMO-002]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-002
      snippet: |
        Demonstrate that collisionless behavior of Γ reproduces observed κ–X‑ray separations and their redshift/mass scaling **without particulate CDM**, using the same frozen potential V(Γ) from COSMO‑Γ‑000.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A landscape etched in stone, inherited from a prior cosmic epoch. Its contours dictate the flow and clash of all subsequent structures, a fixed stage for cosmic drama.
  law: |
    The potential V(Γ) is fixed by fits to galaxy-scale phenomena (e.g., the Σ₀ locus in `COSMO-Γ-HALO`) and is not tuned when modeling cluster-scale dynamics. All cluster-scale collisional properties are derived consequences of this fixed potential, not independent fitted parameters.
  philosophy: |
    To enforce predictive power and falsifiability across astrophysical scales. By freezing V(Γ), the framework prohibits ad-hoc tuning, forcing a unified explanation for phenomena from galaxy cores to cluster mergers and demanding that the model survives or is broken by its own rigid consistency.
pirouette_definition: |
  The scalar potential V(Γ) governing the self-interaction of the Γ-field, whose functional form and parameters (e.g., mass `m_Γ`, coupling `λ_4`) are calibrated and fixed ('frozen') in a parent module (e.g., `COSMO-Γ-000`, `COSMO-Γ-HALO`) using galaxy-scale observations. Subsequent modules, such as those for cluster mergers (`COSMO-002`), must inherit this potential without modification, treating its predictions as non-tunable outputs of the theory.
operational_definition:
  units: Energy density (J m⁻³ or natural units of GeV⁴)
  symbol_table:
    - name: V(Γ)
      meaning: Scalar potential of the Γ-field.
      dimensions: M L⁻¹ T⁻²
      default_range: contextual; parameters set in `COSMO-Γ-000`.
    - name: m_Γ
      meaning: Mass parameter of the Γ-field (quadratic term coefficient).
      dimensions: M
      default_range: fixed by `COSMO-Γ-HALO` fits.
    - name: λ_4
      meaning: Quartic self-coupling constant of the Γ-field.
      dimensions: dimensionless (in 4D)
      default_range: fixed by `COSMO-Γ-HALO` fits.
  measurement:
    procedures:
      - name: Hierarchical Inference & Falsification
        outline: |
          1. Calibrate the parameters of V(Γ) (e.g., `m_Γ`, `λ_4` in the `quadratic_plus_quartic` model) by fitting static Γ-halo solutions to a robust set of galaxy-scale observables, like the universal core surface density Σ₀ from `COSMO-Γ-HALO`.
          2. Freeze these parameter values in a framework-wide manifest.
          3. Use the fixed, non-tunable V(Γ) in simulations of a different physical regime, such as galaxy cluster mergers (`COSMO-002`).
          4. Compare derived predictions (e.g., lensing-gas offset Δx, effective cross-section σ_eff/m) against cluster-scale observations. A significant, persistent mismatch falsifies the chosen V(Γ).
        expected_signals: [A single set of V(Γ) parameters that successfully predicts observables across both galaxy and cluster scales, A derived σ_eff/m for clusters consistent with observed offsets.]
        pitfalls: [Degeneracies in the initial galaxy-scale fit, Incorrect functional form assumed for V(Γ), Neglecting baryonic feedback effects that mimic Γ-field dynamics.]
context_windows:
  - module: COSMO-002
    excerpt: |
      The peak offset Δx ≡ |x_κ − x_X| follows a universal scaling law Δx ≃ 𝔽(M_1,M_2,b,v_in,z; V(Γ)) determined by the Γ halo structure, not by an elastic DM cross‑section... The redshift evolution of Δx and the survival of κ peaks after core passage are fixed by the same parameters that set galactic cores (Σ₀ locus in COSMO‑Γ‑HALO).
  - module: COSMO-002
    excerpt: |
      An apparent “σ/m” constraint inferred in CDM language maps in Pirouette to a **derived** (non‑tunable) effective collisional proxy σ_eff/m determined by Γ soliton overlap; prediction: σ_eff/m ≲ 0.2 cm² g⁻¹ for Bullet‑like events when V(Γ) is COSMO‑Γ‑000‑frozen.
poetic_connections:
  motifs: [inheritance, rigidity, blueprint, foundation, anchor]
  evocative_lines:
    - "no tunable cross-section."
    - "fixed by the same parameters that set galactic cores."
    - "One‑shot anchor inherited; no retuning."
  association_matrix:
    - [ "Γ-Condensate", 0.9 ]
    - [ "Σ₀ Locus", 0.8 ]
    - [ "Effective Cross-Section", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Scalar Field Potential V(φ)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L ⊃ -V(φ) = -½m²φ² - (λ/4)φ⁴
      justification: |
        The dynamics of the Γ-field are governed by a standard Klein-Gordon equation with a self-interaction term V'(Γ). The `COSMO-002` configuration specifies a `quadratic_plus_quartic` form, which is a direct analogue to the potential used for a real scalar field in Effective Field Theory to model particle self-interactions.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter 4
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "A single, fixed V(Γ) derived from galaxy-scale data can simultaneously reproduce the observed core surface density (Σ₀ locus) of galaxies and the lensing-gas offsets (Δx) in merging clusters."
      domain: phenomenology
      falsifier: "Observations show that the V(Γ) required to fit galaxy cores predicts a cluster-merger effective cross-section (σ_eff/m) that is inconsistent with observed Δx values, for example by requiring σ/m > 0.2 cm²/g in Bullet-like systems where observations suggest higher values."
      status: proposed
      links: [COSMO-002, COSMO-Γ-HALO]
naming_notes:
  collisions: [V (electric potential), U (potential energy)]
  disambiguation: |
    The term 'Frozen' refers to the parameters of the potential being fixed and invariant across a hierarchy of models within the Pirouette Framework. It does not refer to a thermal state, a phase transition, or a "frozen-out" relic density in the standard cosmological sense.
crosslinks:
  near_synonyms: []
  antonyms: [TUNABLE_POTENTIAL, FREE_PARAMETER]
  prerequisites: [GAMMA_FIELD]
  downstream_effects: [EFFECTIVE_CROSS_SECTION, LENSING_GAS_OFFSET, HALO_SURVIVABILITY]
license: CC-BY-SA-4.0
---

# Frozen Potential

## Canonical (Pirouette)
The scalar potential V(Γ) governing the self-interaction of the Γ-field, whose functional form and parameters (e.g., mass `m_Γ`, coupling `λ_4`) are calibrated and fixed ('frozen') in a parent module (e.g., `COSMO-Γ-000`, `COSMO-Γ-HALO`) using galaxy-scale observations. Subsequent modules, such as those for cluster mergers (`COSMO-002`), must inherit this potential without modification, treating its predictions as non-tunable outputs of the theory.

## EFT-First Summary
In the language of Effective Field Theory (EFT), the Frozen Potential V(Γ) is a classical scalar field potential, typically a polynomial like `V(φ) = ½m²φ² + (λ/4!)φ⁴`. Its key feature within Pirouette is that its parameters (`m`, `λ`) are fixed by low-energy (galaxy-scale) data and are not re-tuned for high-energy (cluster-scale) phenomena. This enforces a rigid, predictive structure, analogous to how the electron's mass is a fixed input across all QED calculations, making the framework highly falsifiable.

## Glossary Links
- See also: Γ-Field, Effective Cross-Section, Σ₀ Locus