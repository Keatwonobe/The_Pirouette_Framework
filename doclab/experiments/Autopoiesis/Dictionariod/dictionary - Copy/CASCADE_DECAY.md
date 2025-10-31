---
term: "Cascade Decay"
canonical_id: "CASCADE_DECAY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-021"]
---

---
term: Cascade Decay
canonical_id: CASCADE_DECAY
symbol: Γ_{H→LL}
aliases: [Phase Transition Decay]
parents: [MATH-021]
children: [SECT-Γ-C]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-021
      snippet: |
        Mechanism C — Phase Transition & Cascade (Γ_H → 2Γ_L)
        Hypothesis
        C1. Early‑universe Γ sits in a metastable well with curvature m_H; a late phase transition (T_c) moves it onto a shallow tail with small curvature.
        C2. Decay channel opens: Γ_H → 2Γ_L with tiny coupling ε; relic Γ_L forms the macroscopic mode; Γ_H today is absent or sub‑dominant.
  editors: [Pirouette Scribe AI]
  review_log: []
triad:
  art: |
    A fleeting, heavy state shatters in the cooling cosmos, its fragments settling into a vast, quiet sea of dark matter.
  law: |
    The relic abundance of the light state Γ_L is determined by the decay rate Γ_{H→LL} and the cosmic expansion rate H at the time of the phase transition T_c, producing a sharp cutoff in the matter power spectrum at a characteristic scale k_c.
  philosophy: |
    This mechanism demonstrates how a single unified sector can dynamically generate the vast mass hierarchy required by particle physics and cosmology, not through static tuning, but through a unique, irreversible event in cosmic history.
pirouette_definition: |
  A cosmological mechanism for generating the light dark matter state (Γ_L) from a heavy precursor state (Γ_H) within the Γ sector. In the early universe, the sector is in a metastable state with a high effective mass (m_H ≈ 17 MeV). A late-time cosmological phase transition at temperature T_c alters the potential, moving the field to a new minimum with a much shallower curvature (m_L ≈ 10⁻²² eV) and opening a decay channel Γ_H → 2Γ_L. The subsequent decay of the Γ_H population sources the entire present-day Γ_L dark matter abundance, leaving behind a distinct signature in the matter power spectrum.
operational_definition:
  units: The decay rate Γ_{H→LL} is measured in units of inverse time (T⁻¹) or energy (e.g., eV).
  symbol_table:
    - name: Γ_{H→LL}
      meaning: The decay rate of the heavy state Γ_H into two light state particles Γ_L.
      dimensions: T⁻¹
      default_range: contextual; set by cosmic history at T_c
    - name: T_c
      meaning: The critical temperature at which the phase transition enabling the decay occurs.
      dimensions: Θ (Temperature) or M L² T⁻² (Energy)
      default_range: contextual (late universe)
    - name: k_c
      meaning: The characteristic wave-number of the suppression feature in the matter power spectrum.
      dimensions: L⁻¹
      default_range: cosmological scales (e.g., Mpc⁻¹)
  measurement:
    procedures:
      - name: Matter Power Spectrum Analysis
        outline: |
          Using large-scale structure surveys (e.g., galaxy clustering, weak lensing, Lyman-α forest), measure the matter power spectrum P(k) over a wide range of scales. Fit the data with a ΛCDM model that includes a sharp, step-like suppression feature at a free scale k_c. The detection of such a feature, inconsistent with warm dark matter's smooth cutoff, would constitute evidence for the cascade.
        expected_signals:
          - A step-like suppression in P(k) at a characteristic scale k_c.
          - An associated Integrated Sachs-Wolfe (ISW) imprint in the CMB due to the rapid change in the dark matter equation of state during the transition.
        pitfalls:
          - The suppression feature may be degenerate with baryonic feedback effects or have low signal-to-noise.
          - The ISW signal is typically weak and difficult to isolate from cosmic variance.
context_windows:
  - module: MATH-021
    excerpt: |
      Mechanism C — Phase Transition & Cascade (Γ_H → 2Γ_L)
      Hypothesis
      C1. Early‑universe Γ sits in a metastable well with curvature m_H; a late phase transition (T_c) moves it onto a shallow tail with small curvature.
      C2. Decay channel opens: Γ_H → 2Γ_L with tiny coupling ε; relic Γ_L forms the macroscopic mode; Γ_H today is absent or sub‑dominant.
  - module: MATH-021
    excerpt: |
      Decision Tree (Discriminants)
      D2. **Halo substructure**: (A) yields phonon‑pressure cores with vortex spectra; (B) yields standard fuzzy‑like suppression with sharp m_L; (C) produces a step‑like cutoff.
      D3. **Lab/precision**: (B) implies definite coupling patterns...; (A) implies medium‑dependent optical signatures; (C) implies nothing current‑day but strong cosmological transition marks.
poetic_connections:
  motifs: [shattering, cosmic echo, relic sea, irreversible fall]
  evocative_lines:
    - "a late phase transition ... moves it onto a shallow tail"
    - "transient early‑universe signature; no present-day Γ_H abundance"
  association_matrix:
    - [ "PHASE_TRANSITION", 0.9 ]
    - [ "DARK_MATTER_ABUNDANCE", 0.8 ]
    - [ "GAMMA_MASS_TENSION", 0.6 ]
formal_mappings:
  candidates:
    - target: Late-decaying particle
      domain: BSM|Cosmology
      mapping_kind: conceptual
      justification: |
        The scenario is an example of a late-decaying particle model, where a heavy, non-thermal relic decays after recombination, altering the composition and structure of the universe. Unlike typical models, the decay product here constitutes the entirety of the dark matter.
      references:
        - title: "Cosmological implications of the decay of a heavy neutral lepton"
          where: Phys.Lett.B 174 (1986) 45-50
          date: 1986-07-03
      confidence: 0.8
  adopted:
    - target: Boltzmann equations for decay
      rationale: The math sketch in MATH-021 explicitly provides the coupled Boltzmann equations governing the number densities of Γ_H and Γ_L, which is the standard, operational formalism for tracking interacting species in an expanding universe.
      equation_hint: |
        ṅ_H + 3H n_H = − Γ_{H→LL} n_H
        ṅ_L + 3H n_L = + 2 Γ_{H→LL} n_H
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Cascade Decay produces a sharp, step-like feature in the matter power spectrum at a scale k_c set by the transition epoch."
      domain: phenomenology
      falsifier: "Multi-probe cosmological surveys (LSS, WL, Lyman-α) failing to find such a feature, instead measuring a smooth power spectrum or a cutoff inconsistent with a sharp transition."
      status: proposed
      links: [MATH-021]
    - statement: "The Cascade Decay mechanism implies no significant present-day abundance of the heavy state Γ_H (≈17 MeV)."
      domain: experiment
      falsifier: "Direct or indirect detection of a relic 17 MeV particle with couplings consistent with the Γ sector, which would indicate its survival, not its decay."
      status: proposed
      links: [MATH-021, XXP-015]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from multi-step particle decay chains in high-energy physics (e.g., supersymmetric cascades). The Pirouette Cascade Decay is a singular, cosmologically-timed event where one species transforms into the final dark matter population.
crosslinks:
  near_synonyms: []
  antonyms: [COMPOSITE_SUPERFLUID_MODEL, CLOCKWORK_HIERARCHY]
  prerequisites: [GAMMA_MASS_TENSION, PHASE_TRANSITION]
  downstream_effects: [DARK_MATTER_ABUNDANCE, MATTER_POWER_SPECTRUM]
license: CC-BY-SA-4.0
---

# Cascade Decay

## Canonical (Pirouette)
A cosmological mechanism for generating the light dark matter state (Γ_L) from a heavy precursor state (Γ_H) within the Γ sector. In the early universe, the sector is in a metastable state with a high effective mass (m_H ≈ 17 MeV). A late-time cosmological phase transition at temperature T_c alters the potential, moving the field to a new minimum with a much shallower curvature (m_L ≈ 10⁻²² eV) and opening a decay channel Γ_H → 2Γ_L. The subsequent decay of the Γ_H population sources the entire present-day Γ_L dark matter abundance, leaving behind a distinct signature in the matter power spectrum.

## EFT-First Summary
The Cascade Decay mechanism is operationally described within standard cosmology by a set of coupled Boltzmann equations. These equations track the depletion of the heavy species (Γ_H) and the sourcing of the light species (Γ_L) through a decay term Γ_{H→LL} competing against the Hubble expansion. This process, triggered by a late phase transition, is observationally constrained by its impact on large-scale structure, specifically by predicting a sharp, step-like suppression in the matter power spectrum.

## Glossary Links
- See also: [GAMMA_MASS_TENSION](<#>), [PHASE_TRANSITION](<#>), [MATTER_POWER_SPECTRUM](<#>)