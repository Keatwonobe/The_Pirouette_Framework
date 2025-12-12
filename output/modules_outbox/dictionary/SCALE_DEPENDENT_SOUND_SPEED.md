---
term: "Scale-dependent sound speed"
canonical_id: "SCALE_DEPENDENT_SOUND_SPEED"
symbol: "c_s,eff(k)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SECT-001"]
---

---
term: Scale-dependent sound speed
canonical_id: SCALE_DEPENDENT_SOUND_SPEED
symbol: c_s,eff(k)
aliases: []
parents: [SECT-001]
children: [SECT-Γ-A-HALO, SECT-Γ-A-CMB]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SECT-001
      lines: "Section 2 — Cosmology Mapping (Background & Linear)"
      snippet: |
        Linear perturbations (Newtonian gauge):
        • Fluid form with **scale‑dependent** c_s,eff^2(k) from the phonon dispersion:
        c_s,eff^2(k) ≈ c_s^2 · [1 + (k/k_ξ)^2]^{−1},  k_ξ ≡ 1/ξ.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A cosmic fluid that acts like a rigid jelly against long, gentle waves, yet crumbles like dust under a focused push. This dual nature protects cosmic ripples while allowing galaxies to gather and form.
  law: |
    The effective sound speed squared, `c_s,eff^2(k)`, is suppressed relative to the bulk sound speed `c_s^2` by a factor of `[1 + (k/k_ξ)^2]⁻¹`, where `k` is the wavenumber and `k_ξ` is the inverse healing length. This suppression becomes dominant for scales smaller than the healing length (`k > k_ξ`), permitting gravitational collapse.
  philosophy: |
    Reconciles a fluid dark matter with cosmic structure by introducing an internal scale (the healing length `ξ`) below which pressure support vanishes. This allows the model to pass CMB tests, which probe large scales, while still forming cored halos on small scales—a key requirement of the Superfluid Pressuron hypothesis.
pirouette_definition: |
  The effective sound speed `c_s,eff(k)` for linear perturbations in the Superfluid Pressuron model, derived from its phonon dispersion relation. It is a function of wavenumber `k` that transitions between two regimes. On scales much larger than the healing length `ξ` (i.e., `k ≪ 1/ξ`), it asymptotes to the constant bulk sound speed `c_s`. On scales smaller than the healing length (`k ≫ 1/ξ`), it is suppressed, scaling as `c_s / (kξ)`, which allows gravitational collapse to overcome pressure support and form structure.
operational_definition:
  units: m s⁻¹
  symbol_table:
    - name: c_s,eff(k)
      meaning: Scale-dependent effective sound speed
      dimensions: L T⁻¹
      default_range: "0 < c_s,eff(k) ≤ c_s ≪ c"
    - name: c_s
      meaning: Bulk sound speed (k→0 limit)
      dimensions: L T⁻¹
      default_range: "< 10⁻³ c at recombination"
    - name: k
      meaning: Perturbation wavenumber
      dimensions: L⁻¹
      default_range: contextual (e.g., 10⁻⁴ to 10¹ Mpc⁻¹)
    - name: k_ξ
      meaning: Wavenumber corresponding to the healing length (k_ξ = 1/ξ)
      dimensions: L⁻¹
      default_range: contextual, sets the transition scale (~0.1-1 Mpc⁻¹)
  measurement:
    procedures:
      - name: Cosmological Power Spectrum Analysis
        outline: |
          Measure the matter power spectrum `P(k)` using galaxy surveys (e.g., DESI, Euclid) and CMB lensing data. Fit the data with a ΛCDM model modified to include a fluid component with sound speed `c_s,eff(k)`. The shape of the `P(k)` suppression at high `k` constrains the transition scale `k_ξ` and bulk sound speed `c_s`.
        expected_signals: [A characteristic suppression or cutoff in the matter power spectrum for `k > k_ξ` relative to the standard ΛCDM prediction.]
        pitfalls: [Degeneracy with other physical effects that suppress small-scale power, such as warm dark matter or baryonic feedback. Requires precise modeling of non-linear evolution and galaxy bias.]
context_windows:
  - module: SECT-001
    excerpt: |
      Linear perturbations (Newtonian gauge):
      • Fluid form with **scale‑dependent** c_s,eff^2(k) from the phonon dispersion:
      c_s,eff^2(k) ≈ c_s^2 · [1 + (k/k_ξ)^2]^{−1},  k_ξ ≡ 1/ξ.
      • Jeans‑like cutoff at k_J ~ aH/c_s where growth is suppressed; choose α,β to match halo core scales while keeping CMB acoustic peaks intact (c_s ≪ 10^{−3} at recombination on relevant k).
  - module: SECT-001
    excerpt: |
      **CMB safety**: negligible extra phase shift; c_s at recombination small on ℓ≲2500 scales (explicit numbers in SECT‑Γ‑A‑CMB).
poetic_connections:
  motifs: [scale-suppression, fluid-to-dust transition, healing-length, phonon-dispersion]
  evocative_lines:
    - "choose α,β to match halo core scales while keeping CMB acoustic peaks intact"
    - "Jeans‑like cutoff at k_J ~ aH/c_s where growth is suppressed"
  association_matrix:
    - [ "HEALING_LENGTH", 0.9 ]
    - [ "HALO_CORE", 0.8 ]
    - [ "MATTER_POWER_SPECTRUM", 0.8 ]
    - [ "SURFACE_TENSION", 0.5 ]
formal_mappings:
  candidates:
    - target: c_s^2(k) in Generalized Dark Matter (GDM)
      domain: Cosmology
      mapping_kind: operational
      equation_hint: |
        δ' = -(θ + 3Φ'), θ' = -Hθ + k²Φ + c_s^2(k) k²δ
      justification: |
        In the GDM formalism, dark matter is treated as a fluid with a pressure perturbation defined by a sound speed `c_s^2`. The Pirouette Framework provides a specific, physically-motivated functional form `c_s,eff^2(k)` derived from an underlying superfluid EFT, which can be directly implemented in this formalism.
      references:
        - title: "Generalized Dark Matter in CLASS"
          where: "arXiv:1104.2933"
          date: 2011-04-15
      confidence: 0.95
  adopted:
    - target: c_s^2(k) in Generalized Dark Matter (GDM)
      rationale: Direct operational and mathematical correspondence within standard cosmological perturbation theory codes like CLASS and CAMB.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The effective sound speed is suppressed on scales smaller than the healing length (`k > k_ξ`), producing a measurable cutoff in the linear matter power spectrum relative to ΛCDM."
      domain: phenomenology
      falsifier: "Observations of small-scale power from Lyman-alpha forest or dwarf galaxy counts are inconsistent with the predicted suppression for any value of `k_ξ` that also produces correct halo cores."
      status: proposed
      links: [SECT-Γ-A-HALO]
    - statement: "The transition scale `k_ξ` is physically determined by the superfluid's healing length `ξ`, which is itself a function of the bulk sound speed `c_s` and pressuron mass `m_H` (`k_ξ = 1/ξ` with `ξ = (2 m_H c_s)⁻¹` for ħ=1)."
      domain: theory
      falsifier: "A successful joint fit to CMB, LSS, and halo core data requires `k_ξ` and `c_s` to be treated as independent, un-correlated parameters, breaking their theoretical consistency relation."
      status: proposed
      links: [SECT-001]
naming_notes:
  collisions: [The symbol `c_s` is the standard symbol for sound speed in many fields of physics.]
  disambiguation: |
    Must be distinguished from the *bulk* sound speed `c_s`, which is the `k→0` (large-scale) limit of `c_s,eff(k)`. Also distinct from the sound speed of the baryon-photon fluid, which is responsible for the acoustic oscillations seen in the CMB power spectrum.
crosslinks:
  near_synonyms: []
  antonyms: [SCALE_INVARIANT_SOUND_SPEED]
  prerequisites: [HEALING_LENGTH, SUPERFLUID_PRESSURON, P_OF_X_LAGRANGIAN]
  downstream_effects: [HALO_CORE, MATTER_POWER_SPECTRUM_CUTOFF]
license: CC-BY-SA-4.0
---

# Scale-dependent sound speed

## Canonical (Pirouette)
The effective sound speed `c_s,eff(k)` for linear perturbations in the Superfluid Pressuron model, derived from its phonon dispersion relation. It is a function of wavenumber `k` that transitions between two regimes. On scales much larger than the healing length `ξ` (i.e., `k ≪ 1/ξ`), it asymptotes to the constant bulk sound speed `c_s`. On scales smaller than the healing length (`k ≫ 1/ξ`), it is suppressed, scaling as `c_s / (kξ)`, which allows gravitational collapse to overcome pressure support and form structure.

## EFT-First Summary
In cosmological frameworks like Generalized Dark Matter (GDM), the properties of dark matter beyond the cold, collisionless paradigm are often parameterized by an effective sound speed. The Pirouette Framework provides a concrete physical origin for this parameter via the Superfluid Pressuron model. The scale-dependent sound speed `c_s,eff(k)` arises from the phonon dispersion relation, behaving like a standard fluid on large scales but losing pressure support on scales smaller than the superfluid's healing length, thereby enabling structure formation (see `arXiv:1104.2933` for GDM context).

## Glossary Links
- See also: HEALING_LENGTH, HALO_CORE, SUPERFLUID_PRESSURON, MATTER_POWER_SPECTRUM_CUTOFF