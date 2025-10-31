---
term: "Effective Sound Speed"
canonical_id: "EFFECTIVE_SOUND_SPEED"
symbol: "c_eff^2"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-000"]
---

---
term: Effective Sound Speed
canonical_id: EFFECTIVE_SOUND_SPEED
symbol: c_eff^2
aliases: []
parents: [COSMO-000]
children: [COSMO-Γ-HALO, COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-000
      snippet: |
        Sound speed: for canonical Γ, c_s^2 = 1 in field rest frame, but the *effective* sound speed for oscillatory condensates time‑averages to c_eff^2 ≈ 0 → CDM‑like clustering.
  editors: [AI Agent]
  review_log: []
triad:
  art: |
    A cosmic hum, vibrating too fast to push back, settles into a silent, heavy dust. The field's rapid jitters average out to stillness, allowing gravity's patient whisper to gather worlds.
  law: |
    In the oscillatory regime where field frequency `m_Γ` greatly exceeds the Hubble rate `H`, the time-averaged effective sound speed `c_eff^2` of the Γ condensate approaches zero. This permits gravitational collapse on all cosmological scales, mimicking Cold Dark Matter by removing pressure support against gravity.
  philosophy: |
    This concept resolves the tension between a fundamental scalar field's inherent pressure (`c_s^2=1`) and the observed "coldness" of dark matter (`c_s^2=0`). It demonstrates how a single, simple field can manifest complex, scale-dependent emergent properties, unifying disparate phenomena through dynamical state changes rather than new particles.
pirouette_definition: |
  The effective sound speed, c_eff^2, is the time-averaged propagation speed of linear density perturbations in the Γ-field condensate during its oscillatory, matter-like regime (m_Γ ≫ H). While the fundamental sound speed of the canonical scalar field is unity (c_s^2 = 1), rapid oscillations cause the kinetic and potential energy densities to exchange roles, averaging the pressure perturbations to near zero. This results in c_eff^2 ≈ 0, suppressing pressure support and allowing Γ to cluster under gravity on all sub-horizon scales, thus providing a dynamical basis for Cold Dark Matter.
operational_definition:
  units: Dimensionless (as v^2/c^2)
  symbol_table:
    - name: c_eff^2
      meaning: Effective sound speed squared for the Γ-condensate
      dimensions: dimensionless
      default_range: "[0, 1]; approaches 0 in oscillatory regime"
    - name: c_s^2
      meaning: Fundamental sound speed squared of the Γ scalar field
      dimensions: dimensionless
      default_range: "1 (for canonical scalar)"
    - name: m_Γ
      meaning: Mass of the Γ field quantum
      dimensions: M
      default_range: "cosmological (e.g., ~10⁻²⁷ eV)"
    - name: H
      meaning: Hubble expansion rate
      dimensions: T⁻¹
      default_range: "cosmological"
  measurement:
    procedures:
      - name: Cosmological Structure Constraint
        outline: |
          Infer an upper bound on c_eff^2 by measuring its impact on the matter power spectrum and the Cosmic Microwave Background (CMB). A non-zero c_eff^2 would introduce a Jeans length, λ_J ∝ c_eff, below which structure growth is suppressed by pressure. This suppression manifests as a cutoff in the small-scale power spectrum measured by galaxy surveys or the Lyman-alpha forest, and alters the CMB damping tail.
        expected_signals: [Suppression of power spectrum on scales k > k_J, where k_J is the Jeans wavenumber; Altered shape of CMB TT/EE angular power spectra at high-l.]
        pitfalls: [Degeneracy with baryonic feedback effects on small scales; distinguishing the signal from a warm dark matter (WDM) cutoff; measurement precision limited by non-linear evolution.]
context_windows:
  - module: COSMO-000
    excerpt: |
      Sound speed: for canonical Γ, c_s^2 = 1 in field rest frame, but the *effective* sound speed for oscillatory condensates time‑averages to c_eff^2 ≈ 0 → CDM‑like clustering.
  - module: COSMO-000
    excerpt: |
      Derivative interactions L_int may renormalize the effective sound speed; bound their impact with a prior consistent with CMB damping tail.
poetic_connections:
  motifs: [Emergent coldness, Cosmic hum, Averaged stillness, Gravitational seed]
  evocative_lines:
    - "...the *effective* sound speed for oscillatory condensates time‑averages to c_eff^2 ≈ 0..."
    - "...clustering like CDM."
  association_matrix:
    - [ "TEMPORAL_PRESSURE_Γ", 0.8 ]
    - [ "OSCILLATORY_REGIME", 1.0 ]
    - [ "COLD_DARK_MATTER", 0.9 ]
formal_mappings:
  candidates:
    - target: Adiabatic sound speed c_ad^2
      domain: GR
      mapping_kind: operational
      equation_hint: |
        c_eff^2 = ⟨δp_Γ⟩ / ⟨δρ_Γ⟩
      justification: |
        The effective sound speed is precisely the time-averaged adiabatic sound speed for the Γ field fluid. For a rapidly oscillating scalar field, this average approaches zero, distinguishing it from the fundamental phase velocity of the field's excitations. This is a standard result for scalar field dark matter models.
      references:
        - title: Fuzzy Cold Dark Matter
          where: Phys. Rev. Lett. 85, 1141 (2000)
          date: 2000-08-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The effective sound speed c_eff^2 of the Γ-condensate is sufficiently close to zero to be observationally indistinguishable from standard CDM on all currently measured cosmological scales."
      domain: phenomenology
      falsifier: "Detection of a cutoff in the matter power spectrum at small scales (e.g., from Lyman-α forest or future 21cm cosmology) that is not attributable to baryonic physics or a free-streaming scale, corresponding to a non-zero c_eff^2."
      status: under-test
      links: [COSMO-000]
naming_notes:
  collisions: [c_s^2 (fundamental sound speed), c_ad^2 (adiabatic sound speed)]
  disambiguation: |
    Distinguish the *effective* sound speed (c_eff^2), an emergent property of the time-averaged oscillatory condensate relevant for structure formation, from the *fundamental* sound speed (c_s^2=1) of the underlying canonical scalar Γ field, which describes the propagation of high-frequency, field-level excitations.
crosslinks:
  near_synonyms: []
  antonyms: [FUNDAMENTAL_SOUND_SPEED]
  prerequisites: [TEMPORAL_PRESSURE_Γ, OSCILLATORY_REGIME]
  downstream_effects: [STRUCTURE_FORMATION, MATTER_POWER_SPECTRUM]
license: CC-BY-SA-4.0
---

# Effective Sound Speed

## Canonical (Pirouette)
The effective sound speed, c_eff^2, is the time-averaged propagation speed of linear density perturbations in the Γ-field condensate during its oscillatory, matter-like regime (m_Γ ≫ H). While the fundamental sound speed of the canonical scalar field is unity (c_s^2 = 1), rapid oscillations cause the kinetic and potential energy densities to exchange roles, averaging the pressure perturbations to near zero. This results in c_eff^2 ≈ 0, suppressing pressure support and allowing Γ to cluster under gravity on all sub-horizon scales, thus providing a dynamical basis for Cold Dark Matter.

## EFT-First Summary
In the language of general relativity and cosmology, the effective sound speed `c_eff^2` is the time-averaged adiabatic sound speed `⟨δp/δρ⟩` of the Γ scalar field condensate. Standard treatments of oscillating scalar fields (e.g., axion-like particles or fuzzy dark matter) show that this quantity approaches zero when the field's mass is much larger than the Hubble rate, `m_Γ ≫ H`. This allows the field to behave as a pressureless fluid, i.e., Cold Dark Matter, permitting structure to form via gravitational instability.

## Glossary Links
- See also: Temporal Pressure Γ, Oscillatory Regime, Cold Dark Matter