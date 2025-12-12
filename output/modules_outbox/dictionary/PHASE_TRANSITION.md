---
term: "Phase Transition"
canonical_id: "PHASE_TRANSITION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-021"]
---

---
term: Phase Transition
canonical_id: GAMMA_PHASE_TRANSITION
symbol: T_c
aliases: [Γ Mass Transition, Cascade Decay Mechanism]
parents: [MATH-021]
children: [COSMO-Γ-CMB, HALO/MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-021
      lines: "Mechanism C — Phase Transition & Cascade (Γ_H → 2Γ_L)"
      snippet: |
        C1. Early‑universe Γ sits in a metastable well with curvature m_H; a late phase transition (T_c) moves it onto a shallow tail with small curvature.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The universe cooled and its energy landscape fractured. A heavy, vibrant potential froze into a shallow, crystalline plain, leaving behind a light, persistent echo of what it once was.
  law: |
    The Γ field's effective mass is a function of the cosmological background temperature, undergoing a transition from m_H ≈ 17 MeV to m_L ≈ 10⁻²² eV at a critical temperature T_c. This event imprints a step-like suppression in the matter power spectrum at a comoving wavenumber k_c corresponding to the cosmic horizon size at T_c.
  philosophy: |
    This mechanism resolves a fundamental hierarchy problem not by fine-tuning, but by cosmic dynamics. It suggests that observed physical "constants" can be relics of the universe's thermal history, with particle properties emerging from the evolution of the cosmos itself.
pirouette_definition: |
  A proposed cosmological event where the effective potential V(Γ) for the Γ sector changed as the universe cooled. This caused the field's background value to shift from a metastable, high-curvature minimum (mass m_H ≈ 17 MeV) to a true, low-curvature minimum (mass m_L ≈ 10⁻²² eV). The original heavy states (Γ_H) subsequently decayed into the light states (Γ_L), which now constitute the cosmological dark matter halo component.
operational_definition:
  units: Energy (eV) for masses and temperature; inverse length (Mpc⁻¹) for power spectrum features.
  symbol_table:
    - name: m_H
      meaning: Mass of the Γ quantum before the transition.
      dimensions: M
      default_range: ≈ 17 MeV
    - name: m_L
      meaning: Effective mass of the Γ quantum after the transition; the cosmological dark matter mass.
      dimensions: M
      default_range: ≈ 10⁻²² eV
    - name: T_c
      meaning: Critical temperature at which the phase transition occurs.
      dimensions: M L² T⁻² (Energy)
      default_range: contextual, inferred from k_c
    - name: k_c
      meaning: Comoving wave number of the suppression feature in the matter power spectrum.
      dimensions: L⁻¹
      default_range: contextual, inferred from CMB/LSS data
  measurement:
    procedures:
      - name: Matter Power Spectrum Cutoff Analysis
        outline: |
          Measure the matter power spectrum using large-scale structure (LSS) surveys (e.g., galaxy clustering, weak lensing) and the Lyman-alpha forest. Fit the data against a ΛCDM model containing a sharp, step-like suppression at scale k_c. A statistically significant detection of such a feature, which cannot be explained by baryonic physics or other models, would support this mechanism.
        expected_signals: [Step-like suppression in P(k) at a specific k_c, Correlated ISW signal in CMB]
        pitfalls: [Signal may be degenerate with baryonic feedback models, Cosmic variance in the ISW signal is large]
      - name: Relic Search
        outline: |
          Conduct direct and indirect searches for the heavy Γ_H state. Its non-detection is a necessary (but not sufficient) condition for this mechanism, which predicts Γ_H has completely decayed.
        expected_signals: [Null result for a 17 MeV Γ_H particle in the present day]
        pitfalls: [A null result does not rule out other mechanisms where Γ_H is absent or very weakly coupled]
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
      D2. Halo substructure: [...] (C) produces a step‑like cutoff.
      D3. Lab/precision: [...] (C) implies nothing current‑day but strong cosmological transition marks.
poetic_connections:
  motifs: [metamorphosis, cascade, freezing, cosmic relic, echo]
  evocative_lines:
    - "a late phase transition moves it onto a shallow tail with small curvature"
    - "transient early‑universe signature"
    - "no present‑day Γ_H abundance"
  association_matrix:
    - [ "MASS_TENSION", 0.9 ]
    - [ "GAMMA_FIELD", 0.9 ]
    - [ "HALO_SUBSTRUCTURE", 0.6 ]
    - [ "CMB_ANISOTROPIES", 0.7 ]
formal_mappings:
  candidates:
    - target: Cosmological first-order phase transition
      domain: Cosmology|QFT
      mapping_kind: conceptual
      justification: |
        The mechanism is a direct analogue to other proposed cosmological phase transitions (e.g., electroweak, QCD). A scalar field's potential V(Φ,T) evolves with temperature, leading to a shift in the vacuum state from a "false" to a "true" minimum, thereby changing the mass of the field's excitations.
      references:
        - title: "Cosmological Phase Transitions"
          where: "astro-ph/9601075"
          date: 1996-01-16
      confidence: 0.9
    - target: Axion-like potential
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        V(Γ) ⊃ μ⁴[1−cos(Γ/f)]
      justification: |
        The "shallow tail" of the potential responsible for the ultralight mass m_L is explicitly modeled in MATH-021 with a periodic cosine term. This is the characteristic potential for an axion or axion-like particle, where the small mass arises from non-perturbative effects.
      references:
        - title: "The Axion Dark Matter eXperiment (ADMX)"
          where: "Rev. Mod. Phys. 90, 045001"
          date: 2018-10-09
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Γ-field phase transition imprints a sharp, step-like suppression feature in the matter power spectrum at a comoving wave number k_c."
      domain: phenomenology
      falsifier: "High-precision LSS data (e.g., from DESI, Euclid) is fit perfectly by smooth ΛCDM or alternative DM models (e.g., warm DM) and statistically excludes a sharp cutoff."
      status: proposed
      links: [MATH-021, COSMO-Γ-CMB]
    - statement: "The heavy Γ_H state (m_H ≈ 17 MeV) is absent in the local universe due to its complete decay into Γ_L states."
      domain: experiment
      falsifier: "A particle consistent with Γ_H properties is discovered in lepton g-2 anomalies, beam-dump experiments, or direct detection, with an abundance too high to be explained by other means."
      status: proposed
      links: [MATH-021, XXP-015]
    - statement: "The transition causes a late-time change in the dark sector's equation of state, producing a detectable Integrated Sachs-Wolfe (ISW) signature in the CMB."
      domain: phenomenology
      falsifier: "Cross-correlation of CMB maps with galaxy surveys places stringent limits on any non-standard ISW signal, ruling out the amplitude predicted by the transition model."
      status: proposed
      links: [MATH-021, COSMO-Γ-CMB]
naming_notes:
  collisions: [QCD Phase Transition, Electroweak Phase Transition]
  disambiguation: |
    Within the Pirouette Framework, "Phase Transition" unqualified typically refers to this specific mechanism for the Γ field's mass evolution. If referring to standard model or other transitions, the relevant sector (e.g., "QCD") should be specified. This is a transition in the dark sector, not the baryonic or leptonic sectors.
crosslinks:
  near_synonyms: []
  antonyms: [MASS_TENSION_SOLUTION_CLOCKWORK]
  prerequisites: [GAMMA_FIELD, MASS_TENSION]
  downstream_effects: [HALO_SUBSTRUCTURE, CMB_LENSING, INTEGRATED_SACHS_WOLFE_EFFECT]
license: CC-BY-SA-4.0
---

# Phase Transition

## Canonical (Pirouette)
A proposed cosmological event where the effective potential V(Γ) for the Γ sector changed as the universe cooled. This caused the field's background value to shift from a metastable, high-curvature minimum (mass m_H ≈ 17 MeV) to a true, low-curvature minimum (mass m_L ≈ 10⁻²² eV). The original heavy states (Γ_H) subsequently decayed into the light states (Γ_L), which now constitute the cosmological dark matter halo component.

## EFT-First Summary
The Γ Phase Transition is modeled as a cosmological first-order phase transition in a dark sector governed by a scalar field. In the early universe, the field resides in a quadratic potential, giving it a large mass. As the universe's temperature drops below a critical value T_c, the field tunnels or rolls to a new minimum on a shallow, periodic potential of the form `V ∝ [1-cos(Γ/f)]`, characteristic of an axion-like particle. This dynamically generates the ultralight mass required by cosmological observations and resolves the Γ mass tension by linking the two mass scales to two different epochs of cosmic history.

## Glossary Links
- See also: [GAMMA_FIELD](./gamma-field.md), [MASS_TENSION](./mass-tension.md)