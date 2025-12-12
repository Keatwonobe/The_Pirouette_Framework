---
term: "Healing scale"
canonical_id: "HEALING_SCALE"
symbol: "k_ξ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-005"]
---

---
term: Healing scale
canonical_id: HEALING_SCALE
symbol: k_ξ
aliases: ['inverse healing length']
parents: ['COSMO-005']
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-005
      lines: "SECT-Γ-A-CMB, §1"
      snippet: |
        Scale‑dependent effective sound speed used in Boltzmann evolution:
        c_{s,eff}²(k,a) = c_s²(a) / [1 + (k/k_ξ(a))²],  with k_ξ(a)≡1/ξ(a),  ξ(a)=(2 m_H c_s(a))^{−1}.
  editors: ['system-generator']
  review_log: []
triad:
  art: |
    The scale at which a cosmic fluid's pressure asserts itself, mending the vacuum's indifference and smoothing the clumpy nature of matter into a coherent whole. Below this length, particles scatter; above it, they flow as one.
  law: |
    The effective sound speed squared, `c_{s,eff}²`, of a superfluid phonon gas is suppressed relative to its microscopic value `c_s²` by a factor of `[1 + (k/k_ξ)²]⁻¹`, where `k` is the comoving wave number and `k_ξ` is the healing scale.
  philosophy: |
    The healing scale parameterizes the transition from a pressureless, particle-like state (CDM) to a pressure-supported, fluid-like state. It embodies the principle that effective descriptions of nature are scale-dependent, allowing a single substance to mimic cold dark matter on cosmological scales while simultaneously resolving small-scale structure problems like the core-cusp issue.
pirouette_definition: |
  The healing scale `k_ξ` is the characteristic comoving wave number that defines the transition in the scale-dependent effective sound speed `c_{s,eff}²` for a superfluid phonon gas. For wave numbers `k ≪ k_ξ`, the fluid behaves like pressureless Cold Dark Matter (`c_{s,eff}² ≈ c_s² → 0`). For wave numbers `k ≫ k_ξ`, pressure support becomes significant, suppressing structure growth (`c_{s,eff}² ∝ k⁻²`). It is defined as the inverse of the healing length `ξ`, where `k_ξ ≡ 1/ξ = 2 m_H c_s` in natural units, with `m_H` being the mass of the heavy quanta and `c_s` the microscopic sound speed.
operational_definition:
  units: comoving Mpc⁻¹
  symbol_table:
    - name: k_ξ
      meaning: Healing scale (comoving wave number)
      dimensions: L⁻¹
      default_range: '~0.1 – 10 h/Mpc'
    - name: ξ
      meaning: Healing length (comoving)
      dimensions: L
      default_range: 'contextual'
    - name: c_{s,eff}²
      meaning: Scale-dependent effective sound speed squared
      dimensions: 'dimensionless'
      default_range: '[0, c_s²]'
    - name: m_H
      meaning: Mass of the heavy quanta
      dimensions: M
      default_range: '~17 MeV'
  measurement:
    procedures:
      - name: Cosmological Parameter Inference
        outline: |
          Infer `k_ξ(a)` or its underlying parameters (`m_H`, `c_s`) by fitting the superfluid phonon model to cosmological data. The primary signal is a scale-dependent suppression in the matter power spectrum `P(k)` for `k > k_ξ`, affecting galaxy clustering and Lyman-alpha forest statistics. A secondary signal can appear in the CMB power spectra through the integrated Sachs-Wolfe effect.
        expected_signals: ['Suppression of P(k) relative to ΛCDM at small scales', 'Formation of cored dark matter halos', 'Negligible deviation (<0.1%) from ΛCDM in CMB TT/TE/EE spectra for ℓ < 2500']
        pitfalls: ['Degeneracies with baryonic feedback effects', 'Model dependence on the P(X) theory parameters that set c_s(a)']
context_windows:
  - module: COSMO-005
    excerpt: |
      Phonon dispersion: ω² = c_s² k² + m_eff² with m_eff² from weak tail breaking; typically m_eff→0 on CMB scales.

      Scale‑dependent effective sound speed used in Boltzmann evolution:
      c_{s,eff}²(k,a) = c_s²(a) / [1 + (k/k_ξ(a))²],  with k_ξ(a)≡1/ξ(a),  ξ(a)=(2 m_H c_s(a))^{−1}.
  - module: COSMO-005
    excerpt: |
      Perturbations (Newtonian gauge, effective fluid):
      δ_Γ′ = −(1+w_Γ)(θ_Γ − 3Φ′) − 3ℋ (c_{s,eff}² − w_Γ) δ_Γ
      θ_Γ′ = −ℋ θ_Γ + k² Ψ + k² c_{s,eff}² δ_Γ/(1+w_Γ)
      with w_Γ≈0 through recombination (ensure c_{s,eff}² ≪ 10^{−6} on k relevant to ℓ≲2500).
poetic_connections:
  motifs: ['scale-dependence', 'fluid-particle duality', 'healing', 'pressure support', 'core formation']
  evocative_lines:
    - "reproduces CDM on CMB scales while generating small‑scale suppression and halo cores."
    - "c_{s,eff}² ∝ 1 / [1 + (k/k_ξ)²]"
  association_matrix:
    - [ "EFFECTIVE_SOUND_SPEED", 0.9 ]
    - [ "JEANS_SCALE", 0.7 ]
    - [ "CORE_CUSP_PROBLEM", 0.8 ]
formal_mappings:
  candidates:
    - target: Superfluid healing length, ξ
      domain: AMO|Condensed Matter
      mapping_kind: conceptual
      equation_hint: |
        ξ = ħ / (√2 m c_s) for a Bose-Einstein Condensate. The Pirouette definition ξ = (2 m_H c_s)⁻¹ is a variant in natural units.
      justification: |
        The term is a direct cosmological application of the 'healing length' from the theory of superfluids (e.g., Gross-Pitaevskii equation). In that context, ξ is the characteristic scale over which the superfluid order parameter recovers its bulk value after a perturbation. Here, its inverse k_ξ marks the momentum scale where the collective fluid description (phonons) transitions to particle-like behavior.
      references:
        - title: Bose-Einstein Condensation in Dilute Gases
          where: 'Pethick, C. J., & Smith, H. (2008), Cambridge University Press'
          date: 2008-01-01
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The healing scale `k_ξ` must be sufficiently large such that `c_{s,eff}²` is negligible (`≪ 10⁻⁶`) for all wave numbers `k` relevant to CMB primary anisotropies (ℓ ≲ 2500)."
      domain: phenomenology
      falsifier: "Detection of deviations from ΛCDM angular power spectra at ℓ ≲ 2500 exceeding the 0.1% tolerance specified in COSMO-005, attributable to this effect."
      status: proposed
      links: ['COSMO-005']
    - statement: "A value of k_ξ in the range `~0.1 - 10 h/Mpc` can simultaneously match large-scale structure data and produce cored halo profiles consistent with dwarf galaxy observations."
      domain: phenomenology
      falsifier: "A joint analysis showing that no value of k_ξ can fit both LSS data (e.g., galaxy clustering) and small-scale observations (e.g., halo density profiles) without significant tension."
      status: proposed
      links: ['COSMO-005']
naming_notes:
  collisions: ['k (generic wave number)', 'ξ (quintessence field, correlation length)']
  disambiguation: |
    Distinguish `k_ξ`, the healing *scale* (a wave number, L⁻¹), from `ξ`, the healing *length* (L). Note that `k_ξ` is distinct from the Jeans wave number `k_J`. The Jeans instability governs gravitational collapse against a static pressure, whereas the healing scale modifies the propagation speed of perturbations itself, making it a property of the fluid's kinetic nature.
crosslinks:
  near_synonyms: ['INVERSE_HEALING_LENGTH']
  antonyms: []
  prerequisites: ['EFFECTIVE_SOUND_SPEED', 'SUPERFLUID_PHONON']
  downstream_effects: ['HALO_CORE_FORMATION', 'SMALL_SCALE_POWER_SUPPRESSION']
license: CC-BY-SA-4.0
---

# Healing scale

## Canonical (Pirouette)
The healing scale `k_ξ` is the characteristic comoving wave number that defines the transition in the scale-dependent effective sound speed `c_{s,eff}²` for a superfluid phonon gas. For wave numbers `k ≪ k_ξ`, the fluid behaves like pressureless Cold Dark Matter (`c_{s,eff}² ≈ c_s² → 0`). For wave numbers `k ≫ k_ξ`, pressure support becomes significant, suppressing structure growth (`c_{s,eff}² ∝ k⁻²`). It is defined as the inverse of the healing length `ξ`, where `k_ξ ≡ 1/ξ = 2 m_H c_s` in natural units, with `m_H` being the mass of the heavy quanta and `c_s` the microscopic sound speed.

## EFT-First Summary
In the context of effective field theories for dark matter, such as the Pressuron `P(X)` model, the healing scale `k_ξ` is a phenomenological parameter emerging from the underlying theory. It is the inverse of the healing length `ξ`, a concept borrowed from the physics of superfluids and Bose-Einstein condensates. This scale marks the transition where the dark matter fluid's effective pressure (`c_{s,eff}^2`) becomes significant, causing it to deviate from standard Cold Dark Matter. Observationally, `k_ξ` governs the scale of suppression in the matter power spectrum, which is constrained by galaxy surveys and the Lyman-alpha forest.

## Glossary Links
- See also: EFFECTIVE_SOUND_SPEED, CORE_CUSP_PROBLEM, JEANS_SCALE