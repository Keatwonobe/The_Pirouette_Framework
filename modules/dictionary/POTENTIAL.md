---
term: "Potential"
canonical_id: "POTENTIAL"
symbol: "V(Γ)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-000"]
---

---
term: Potential
canonical_id: POTENTIAL
symbol: V(Γ)
aliases: [Scalar Potential, Γ-Potential]
parents: [COSMO-Γ-000, MATH-018]
children: [COSMO-Γ-HALO, COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-Γ-000
      snippet: |
        Potential class (fixed by D2):
        V(Γ) = ½ m_Γ^2 Γ^2 + λ_4 Γ^4 / 4!  (quartic optional, sign chosen for stability)
        Leading power and the presence of Γ^4 follow from analyticity and scale‑covariance;
  editors: [system]
  review_log: []
triad:
  art: |
    The landscape upon which the cosmic field Γ journeys. Its valleys cradle oscillating matter, while its vast, flat plateaus guide the accelerating expansion of spacetime.
  law: |
    The potential V(Γ) is a local, analytic, and scale-covariant function whose parameters are determined by a single, D3-compliant one-shot anchor measurement, after which its form is frozen for all P4 predictions.
  philosophy: |
    The Potential embodies the principle of dynamical unification. It asserts that disparate cosmic phenomena like dark matter and dark energy are not distinct substances but different behaviors of a single entity, elicited by the topology of its governing function.
pirouette_definition: |
  The scalar function V(Γ) that determines the self-interaction of the temporal pressure field Γ. Its D2-constrained form, typically a low-order polynomial like `½ m_Γ^2 Γ^2 + λ_4 Γ^4 / 4!`, provides two distinct dynamical regimes: a quadratic minimum enabling rapid oscillations (emulating CDM), and a flatter region enabling slow-roll (emulating DE). The potential's parameters are not fit to data but are derived from a one-shot anchor (D3) and then frozen.
operational_definition:
  units: Energy density (J/m³ or eV⁴)
  symbol_table:
    - name: V(Γ)
      meaning: Scalar potential of the Γ field
      dimensions: M·L⁻¹·T⁻²
      default_range: >0 for vacuum stability; shape is context-dependent.
    - name: m_Γ
      meaning: Mass parameter of Γ, sets oscillation frequency
      dimensions: M
      default_range: Cosmological scales (~10⁻²⁷ eV)
    - name: λ_4
      meaning: Quartic self-coupling constant
      dimensions: dimensionless
      default_range: Small, non-negative
  measurement:
    procedures:
      - name: Cosmological Inversion
        outline: |
          The shape of V(Γ) is not measured directly. Its free parameters (e.g., `m_Γ`, `λ_4`) are derived from a 'one-shot anchor' measurement (e.g., today's matter density `Ω_m0`) via symmetry constraints. The resulting potential is then used to predict the cosmic expansion history H(z) and structure growth `fσ_8(z)`. The validity of the inferred V(Γ) is tested by comparing these predictions to independent datasets (BAO, RSD, Weak Lensing).
        expected_signals: [A specific `H(z)` curve, A specific `fσ_8(z)` curve, A value for S₈]
        pitfalls: [Degeneracy with other cosmological parameters (e.g., H₀), Model misspecification if the true potential deviates from the assumed D2-compliant form, Failure to pass P4 out-of-sample prediction tests.]
context_windows:
  - module: COSMO-Γ-000
    excerpt: |
      • Early Universe (DM‑like): Γ oscillates about a quadratic minimum with m_Γ ≫ H → ⟨w_Γ⟩ → 0, c_s^2 → 0, clustering like CDM.
      • Late Universe (DE‑like): Γ slow‑rolls on a flat segment of V(Γ) → w_Γ ≈ −1, nearly homogeneous, driving acceleration.
  - module: COSMO-Γ-000
    excerpt: |
      Potential class (fixed by D2):
      V(Γ) = ½ m_Γ^2 Γ^2 + λ_4 Γ^4 / 4! (quartic optional, sign chosen for stability)
      Leading power and the presence of Γ^4 follow from analyticity and scale‑covariance; coefficients become U‑class parameters (MATH‑018 D1) set by D3 one‑shot anchor.
poetic_connections:
  motifs: [landscape, valley, plateau, engine, oscillation, rolling]
  evocative_lines:
    - "Γ oscillates about a quadratic minimum"
    - "Γ slow-rolls on a flat segment of V(Γ)"
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "ONE_SHOT_ANCHOR", 0.8 ]
    - [ "EQUATION_OF_STATE", 0.7 ]
formal_mappings:
  candidates:
    - target: Quintessence Potential
      domain: GR
      mapping_kind: conceptual
      justification: |
        Quintessence models use a scalar field potential to explain dark energy. V(Γ) is a specific class of quintessence potential that is constrained by D2 principles and additionally incorporates a CDM-like phase through its shape, unifying the dark sector.
      confidence: 0.9
    - target: Axion-like Particle (ALP) Potential
      domain: Particle Physics
      mapping_kind: mathematical
      equation_hint: |
        For small field values, an axion potential V(φ) ∝ (1 - cos(φ/f)) ≈ ½ m²φ²
      justification: |
        The oscillatory regime of V(Γ) in its quadratic minimum is mathematically and phenomenologically analogous to the behavior of a coherently oscillating ALP field, which is a well-studied candidate for cold dark matter.
      references:
        - title: "Cosmological and Astrophysical Probes of Axions and Axion-Like Particles"
          where: arXiv:2203.09545
          date: 2022-03-18
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A single, polynomial potential V(Γ) can simultaneously reproduce cosmological observables attributed to both CDM (clustering, growth) and DE (late-time acceleration) using parameters fixed by one D3 anchor."
      domain: phenomenology
      falsifier: "The model fails a P4 test: for example, if the V(Γ) parameters required to fit `fσ_8(z)` data are statistically inconsistent (p<0.01) with those required to fit `H(z)` data, violating the one-shot anchor principle."
      status: proposed
      links: [COSMO-Γ-000]
naming_notes:
  collisions: [V (Volume), V (Voltage), U (common symbol for potential energy)]
  disambiguation: |
    In Pirouette cosmology, 'Potential' or V(Γ) specifically refers to the scalar field's self-interaction energy density. It must be distinguished from the gravitational potential Φ, which is a metric perturbation.
crosslinks:
  near_synonyms: []
  antonyms: [KINETIC_ENERGY]
  prerequisites: [TEMPORAL_PRESSURE]
  downstream_effects: [EQUATION_OF_STATE, GROWTH_OF_STRUCTURE, HUBBLE_PARAMETER]
license: CC-BY-SA-4.0
---

# Potential

## Canonical (Pirouette)
The scalar function V(Γ) that determines the self-interaction of the temporal pressure field Γ. Its D2-constrained form, typically a low-order polynomial like `½ m_Γ^2 Γ^2 + λ_4 Γ^4 / 4!`, provides two distinct dynamical regimes: a quadratic minimum enabling rapid oscillations (emulating CDM), and a flatter region enabling slow-roll (emulating DE). The potential's parameters are not fit to data but are derived from a one-shot anchor (D3) and then frozen.

## EFT-First Summary
The Potential V(Γ) is conceptually a specific form of a **Quintessence Potential** used in some Dark Energy models, but with the added feature of a quadratic minimum. In this minimum, its dynamics are mathematically analogous to an **Axion-like Particle (ALP) Potential**, where coherent oscillations of the field behave as a cold, pressureless fluid (dark matter). The Pirouette Framework constrains V(Γ) to be an analytic, scale-covariant function whose parameters are fixed by a single cosmological measurement, rather than being freely fit to multiple datasets.

## Glossary Links
- See also: [Temporal Pressure](<link>), [One-Shot Anchor](<link>), [Equation of State](<link>)